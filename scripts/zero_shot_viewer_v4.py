#!/usr/bin/env python3
"""Zero-shot viewer v4: GT vs prediksi model N-RDD2024 pada data RDD-indo-v4.

Jalankan: streamlit run scripts/zero_shot_viewer_v4.py
Inferensi berjalan on-demand di GPU (model di-cache per pilihan).
"""

from pathlib import Path
import random
import sys
from typing import Any, cast

import pandas as pd
import streamlit as st
import torch
from PIL import Image
from ultralytics.engine.results import Results

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "code/models"))
sys.path.insert(0, str(REPO / "scripts"))
from visualize_streamlit import draw_bounding_boxes  # noqa: E402

REM = REPO / "runs/rdd_yolov8n_local/indo_v4_remapped"
EV = REPO / "runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4"
WEIGHTS = {
    "yolov8n": REPO / "runs/rdd_yolov8n_local/experiments/yolov8n_class_weight/weights/best.pt",
    "yolov12n": REPO / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt",
    "yolov26n": REPO / "runs/rdd_yolov8n_local/experiments/yolov26n_class_weight/weights/best.pt",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/experiments/yolov8_pd_class_weight/weights/best.pt",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/experiments/yolo_rd_class_weight/weights/best.pt",
}
NAMES = ["Longitudinal_Crack", "Transverse_Crack", "Alligator_Crack", "Pothole", "manhole", "patchy_road"]
DEVICE = 0 if torch.cuda.is_available() else "cpu"
IOU_THR = 0.5


def _box_iou(a: list, b: list) -> float:
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    aa = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    bb = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = aa + bb - inter
    return inter / union if union > 0 else 0.0


def _score_image(gt: list, pred: list, iou_thr: float = IOU_THR) -> dict:
    """Greedy matching per kelas, pred terurut conf desc. Skor gaya deteksi IoU>=thr."""
    order = sorted(range(len(pred)), key=lambda i: pred[i].get("conf", 0.0), reverse=True)
    matched = [False] * len(gt)
    tp = 0
    for i in order:
        best, best_iou = -1, iou_thr
        for j, g in enumerate(gt):
            if matched[j] or g["class_id"] != pred[i]["class_id"]:
                continue
            v = _box_iou(pred[i]["px"], g["px"])
            if v >= best_iou:
                best, best_iou = j, v
        if best >= 0:
            matched[best] = True
            tp += 1
    fp = len(pred) - tp
    fn = len(gt) - tp
    prec = tp / (tp + fp) if (tp + fp) > 0 else (1.0 if len(gt) == 0 else 0.0)
    rec = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": prec, "recall": rec, "f1": f1}


st.set_page_config(page_title="Zero-Shot RDD-indo-v4 Viewer", page_icon="🛣️", layout="wide")
st.title("Zero-Shot ke RDD-indo-v4 — GT vs Prediksi")
st.caption("Bobot N-RDD2024 (sumber) diuji langsung pada RDD-indo-v4 (307 citra, isi valid/v4 sebagai split test remap; 5 kelas target tanpa manhole) tanpa fine-tuning. Label GT sudah di-remap ke urutan kelas sumber.")

@st.cache_data(show_spinner=False)
def load_index():
    imgs = sorted((REM / "test/images").glob("*"))
    rows = []
    for p in imgs:
        lf = REM / "test/labels" / (p.stem + ".txt")
        gt_ids: list = []
        n = 0
        if lf.exists():
            for l in lf.read_text().splitlines():
                parts = l.split()
                if len(parts) < 5:
                    continue
                try:
                    gt_ids.append(int(float(parts[0])))
                    n += 1
                except ValueError:
                    continue
        rows.append({"filename": p.name, "path": str(p), "n_gt": n,
                     "gt_ids": gt_ids,
                     "gt_classes": [NAMES[c] for c in gt_ids if 0 <= c < len(NAMES)]})
    return pd.DataFrame(rows)

@st.cache_data(show_spinner=False)
def load_gap():
    csv = EV / "domain_gap.csv"
    if csv.exists():
        return pd.read_csv(csv)
    return pd.DataFrame([
        {"model": "yolov12n", "src_test": 0.654, "indo_v4_zs": 0.332},
        {"model": "yolo_rd", "src_test": 0.661, "indo_v4_zs": 0.297},
        {"model": "yolov8_pd", "src_test": 0.646, "indo_v4_zs": 0.279},
        {"model": "yolov8n", "src_test": 0.648, "indo_v4_zs": 0.250},
        {"model": "yolov26n", "src_test": 0.625, "indo_v4_zs": 0.239},
    ])

@st.cache_resource(show_spinner="Memuat bobot model...")
def load_model(name):
    if name in ("yolov8_pd", "yolo_rd"):
        from custom_modules import patch_ultralytics
        patch_ultralytics()
    from ultralytics import YOLO
    return YOLO(str(WEIGHTS[name]))

@st.cache_data(show_spinner="Inferensi batch 307 citra untuk filter akurasi...")
def compute_all_metrics(model_name: str, conf_thr: float):
    """Inferensi seluruh test set + skor per-citra (IoU 0.5, greedy per kelas)."""
    m = load_model(model_name)
    df_idx = load_index()
    paths = df_idx["path"].tolist()
    results = list(m.predict(paths, imgsz=640, conf=conf_thr, iou=0.6, verbose=False, device=DEVICE) or [])
    out = []
    for row_t, r in zip(df_idx.itertuples(), results, strict=False):
        row = cast(Any, row_t)
        gt = read_gt_boxes(row.path)
        preds_px = []
        r = cast(Results, r)
        if r.boxes is not None:
            for b in r.boxes:
                x1, y1, x2, y2 = (float(v) for v in b.xyxy[0].tolist())
                preds_px.append({"class_id": int(b.cls), "conf": float(b.conf),
                                 "px": [x1, y1, x2, y2]})
        s = _score_image(gt, preds_px)
        out.append({"filename": row.filename, "n_pred": len(preds_px), **s})
    return pd.DataFrame(out)

def read_gt_boxes(img_path):
    lf = REM / "test/labels" / (Path(img_path).stem + ".txt")
    boxes = []
    if not lf.exists():
        return boxes
    W, H = Image.open(img_path).size
    for line in lf.read_text().splitlines():
        p = line.split()
        if len(p) < 5:
            continue
        c, xc, yc, w, h = int(p[0]), float(p[1]), float(p[2]), float(p[3]), float(p[4])
        boxes.append({"class_id": c, "class_name": NAMES[c], "xc": xc, "yc": yc, "w": w, "h": h,
                      "px": [int((xc - w / 2) * W), int((yc - h / 2) * H),
                             int((xc + w / 2) * W), int((yc + h / 2) * H)]})
    return boxes

df = load_index()
if df.empty:
    st.error(f"Tidak ada citra di {REM / 'test/images'}. Pastikan notebook 05_zero_shot_indo_v4.ipynb sel remap sudah dijalankan.")
    st.stop()

with st.expander("Ringkasan domain gap (mAP50 sumber vs zero-shot v4)", expanded=False):
    gap = load_gap()
    st.dataframe(gap, hide_index=True, width="stretch")

# ---------------- Sidebar: model + filter ----------------
st.sidebar.header("Pengaturan model")
model = st.sidebar.selectbox("Model", options=sorted(WEIGHTS.keys()),
                             index=sorted(WEIGHTS.keys()).index("yolov12n"))
conf_thr = st.sidebar.slider("Threshold confidence prediksi", 0.05, 0.9, 0.25, 0.05)
show_labels = st.sidebar.checkbox("Tampilkan label box", value=True)

st.sidebar.header("Pencarian & filter citra")
q = st.sidebar.text_input("Cari nama file", placeholder="cth: 0440")
sel_classes = st.sidebar.multiselect("Kelas GT yang harus ada", options=NAMES, default=[])
match_mode = st.sidebar.radio("Mode filter kelas", ["Salah satu (OR)", "Semua (AND)"], index=0) if sel_classes else "Salah satu (OR)"
max_gt = int(cast(Any, df["n_gt"]).max()) if len(df) else 0
n_gt_range = st.sidebar.slider("Range jumlah GT box", 0, max(1, max_gt), (0, max(1, max_gt)))
gt_status = st.sidebar.radio("Status GT", ["Semua", "Ber-GT saja", "Background saja"], index=0)

use_scores = st.sidebar.checkbox("Filter by skor per-citra (F1/prec/rec)", value=False,
                                 help="Menjalankan inferensi batch seluruh 307 citra (di-cache per model+threshold). Aktifkan jika ingin filter/sort by akurasi.")
f1_range = (0.0, 1.0)
prec_min = 0.0
rec_min = 0.0
pred_status = "Semua"
sort_by = "Nama file"
n_pred_range = None
metrics_df = None
if use_scores:
    metrics_df = compute_all_metrics(model, float(conf_thr))
    f1_range = st.sidebar.slider("Range F1 per-citra (IoU 0.5)", 0.0, 1.0, (0.0, 1.0), 0.05)
    c_pr1, c_pr2 = st.sidebar.columns(2)
    with c_pr1:
        prec_min = st.slider("Min precision", 0.0, 1.0, 0.0, 0.05)
    with c_pr2:
        rec_min = st.slider("Min recall", 0.0, 1.0, 0.0, 0.05)
    pred_status = st.sidebar.selectbox("Status prediksi", ["Semua", "Ada prediksi", "Tanpa prediksi",
                                                           "Perfect (F1=1)", "Missed (F1=0)", "False alarm (GT=0, pred>0)"])
    max_pred = int(cast(Any, metrics_df["n_pred"]).max()) if len(metrics_df) else 0
    n_pred_range = st.sidebar.slider("Range jumlah prediksi", 0, max(1, max_pred), (0, max(1, max_pred)))
    sort_by = st.sidebar.selectbox("Urutkan", ["Nama file", "F1 terendah", "F1 tertinggi",
                                              "GT terbanyak", "Prediksi terbanyak", "Recall terendah"])
else:
    sort_by = st.sidebar.selectbox("Urutkan", ["Nama file", "GT terbanyak"])

if st.sidebar.button("Reset filter"):
    st.session_state.pop("idx", None)
    st.session_state.pop("gallery_page", None)
    st.rerun()

# ---------------- Terapkan filter ----------------
view: Any = df.copy()
if gt_status == "Ber-GT saja":
    view = view[view["n_gt"] > 0]
elif gt_status == "Background saja":
    view = view[view["n_gt"] == 0]
view = view[(view["n_gt"] >= n_gt_range[0]) & (view["n_gt"] <= n_gt_range[1])]
if q.strip():
    view = view[view["filename"].str.contains(q.strip(), case=False, na=False)]
if sel_classes:
    if match_mode.startswith("Semua"):
        view = view[view["gt_classes"].apply(lambda gs: all(c in gs for c in sel_classes))]
    else:
        view = view[view["gt_classes"].apply(lambda gs: any(c in gs for c in sel_classes))]
if metrics_df is not None:
    view = view.merge(metrics_df, on="filename", how="left")
    view = view[(view["f1"] >= f1_range[0]) & (view["f1"] <= f1_range[1])]
    view = view[(view["precision"] >= prec_min) & (view["recall"] >= rec_min)]
    if n_pred_range is not None:
        view = view[(view["n_pred"] >= n_pred_range[0]) & (view["n_pred"] <= n_pred_range[1])]
    if pred_status == "Ada prediksi":
        view = view[view["n_pred"] > 0]
    elif pred_status == "Tanpa prediksi":
        view = view[view["n_pred"] == 0]
    elif pred_status == "Perfect (F1=1)":
        view = view[view["f1"] >= 0.999]
    elif pred_status == "Missed (F1=0)":
        view = view[(view["n_gt"] > 0) & (view["f1"] <= 0.001)]
    elif pred_status.startswith("False alarm"):
        view = view[(view["n_gt"] == 0) & (view["n_pred"] > 0)]

if sort_by == "GT terbanyak":
    view = view.sort_values(["n_gt", "filename"], ascending=[False, True])
elif metrics_df is not None and sort_by == "F1 terendah":
    view = view.sort_values(["f1", "filename"], ascending=[True, True])
elif metrics_df is not None and sort_by == "F1 tertinggi":
    view = view.sort_values(["f1", "filename"], ascending=[False, True])
elif metrics_df is not None and sort_by == "Prediksi terbanyak":
    view = view.sort_values(["n_pred", "filename"], ascending=[False, True])
elif metrics_df is not None and sort_by == "Recall terendah":
    view = view.sort_values(["recall", "filename"], ascending=[True, True])
else:
    view = view.sort_values("filename")
view = view.reset_index(drop=True)

if view.empty:
    st.warning("Tidak ada citra yang cocok dengan filter. Longgarkan filter atau klik Reset filter.")
    st.stop()

# ---------------- Ringkasan + grid hasil ----------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Citra cocok", f"{len(view)} / {len(df)}")
m2.metric("Total GT (cocok)", f"{int(view['n_gt'].sum())}")
if metrics_df is not None:
    m3.metric("Rata-rata F1", f"{view['f1'].mean():.3f}")
    m4.metric("Missed (F1=0, GT>0)", f"{int(((view['n_gt'] > 0) & (view['f1'] <= 0.001)).sum())}")
else:
    m3.metric("Kelas GT unik", f"{len({c for gs in view['gt_classes'] for c in gs})}")
    m4.metric("Background", f"{int((view['n_gt'] == 0).sum())}")
st.caption("Aktifkan 'Filter by skor per-citra' di sidebar untuk filter/sort by F1, precision, recall, dan status prediksi. Skor = matching greedy IoU≥0.5 per kelas pada threshold confidence aktif.")

st.subheader(f"Grid hasil pencarian ({len(view)} citra)")
page_size = st.selectbox("Thumbnail per halaman", [8, 12, 16, 24], index=1)
total_pages = max(1, (len(view) + page_size - 1) // page_size)
page = st.number_input("Halaman grid", 1, total_pages, st.session_state.get("gallery_page", 1))
st.session_state["gallery_page"] = page
start, end = (page - 1) * page_size, min(page * page_size, len(view))
page_view = view.iloc[start:end]
cols = st.columns(4)
for i, (_, r) in enumerate(page_view.iterrows()):
    with cols[i % 4]:
        if metrics_df is not None:
            cap = f"{r['filename']} | GT:{int(r['n_gt'])} pred:{int(r['n_pred'])} F1:{r['f1']:.2f}"
        else:
            cap = f"{r['filename']} | GT:{int(r['n_gt'])}"
        st.image(r["path"], width="stretch", caption=cap)
        if st.button("Buka", key=f"open_{start + i}_{r['filename']}", width="stretch"):
            st.session_state["idx"] = start + i
            st.rerun()

# ---------------- Detail GT vs prediksi ----------------
st.divider()
st.subheader("Detail GT vs prediksi")
if st.sidebar.button("Acak citra"):
    st.session_state["idx"] = random.randint(0, len(view) - 1)
    st.rerun()
if len(view) > 1:
    cur = int(st.session_state.get("idx", 0)) % len(view)
    c_prev, c_slider, c_next = st.columns([1, 8, 1])
    with c_prev:
        if st.button("◀", key="prev_img", help="Citra sebelumnya", width="stretch"):
            st.session_state["idx"] = (cur - 1) % len(view)
            st.rerun()
    with c_next:
        if st.button("▶", key="next_img", help="Citra berikutnya", width="stretch"):
            st.session_state["idx"] = (cur + 1) % len(view)
            st.rerun()
    with c_slider:
        idx = st.slider("Navigasi citra", 0, len(view) - 1, cur)
else:
    idx = 0
    st.caption("1 citra cocok dengan filter.")
st.session_state["idx"] = idx
row = view.iloc[idx]
if metrics_df is not None:
    st.caption(f"{row['filename']} — GT:{int(row['n_gt'])} pred:{int(row['n_pred'])} "
               f"TP:{int(row['tp'])} FP:{int(row['fp'])} FN:{int(row['fn'])} | "
               f"P:{row['precision']:.2f} R:{row['recall']:.2f} F1:{row['f1']:.2f} (IoU 0.5)")

m = load_model(model)
preds = list(m.predict(row["path"], imgsz=640, conf=conf_thr, iou=0.6, verbose=False, device=DEVICE) or [])
if not preds:
    st.warning("Prediksi gagal pada citra ini.")
    st.stop()
r = cast(Results, preds[0])
if r.boxes is None:
    st.warning("Tidak ada prediksi pada citra ini.")
    st.stop()
W, H = Image.open(row["path"]).size
pred_boxes = []
boxes: Any = r.boxes
for b in boxes:
    x1, y1, x2, y2 = (float(v) for v in b.xyxy[0].tolist())
    c, cf = int(b.cls), float(b.conf)
    pred_boxes.append({"class_id": c, "class_name": f"{NAMES[c]} {cf:.2f}",
                       "xc": ((x1 + x2) / 2) / W, "yc": ((y1 + y2) / 2) / H,
                       "w": (x2 - x1) / W, "h": (y2 - y1) / H, "conf": cf})

gt_boxes = read_gt_boxes(row["path"])
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"GT ({len(gt_boxes)})")
    st.image(draw_bounding_boxes(row["path"], gt_boxes, True, show_labels),
             width="stretch", caption=row["filename"])
with col2:
    st.subheader(f"Prediksi {model} conf>={conf_thr:.2f} ({len(pred_boxes)})")
    st.image(draw_bounding_boxes(row["path"], pred_boxes, True, show_labels),
             width="stretch", caption=row["filename"])

c1, c2 = st.columns(2)
with c1:
    if gt_boxes:
        st.dataframe(pd.DataFrame([{"kelas": b["class_name"], "box_px": b["px"]} for b in gt_boxes]),
                     hide_index=True, width="stretch")
    else:
        st.info("Tanpa GT (background).")
with c2:
    if pred_boxes:
        st.dataframe(pd.DataFrame([{"kelas": b["class_name"].rsplit(" ", 1)[0],
                                    "conf": b["conf"]} for b in pred_boxes]),
                     hide_index=True, width="stretch")
    else:
        st.info("Tidak ada prediksi di atas threshold.")

if __name__ == "__main__":
    pass
