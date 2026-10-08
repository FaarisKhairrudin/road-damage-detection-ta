#!/usr/bin/env python3
"""Zero-shot viewer v2: GT vs prediksi model N-RDD2024 pada data RDD-indo-v2.

Jalankan: streamlit run scripts/zero_shot_viewer_v2.py
Inferensi berjalan on-demand di GPU (model di-cache per pilihan).
"""

from pathlib import Path
import random
import sys

import pandas as pd
import streamlit as st
import torch
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "code/models"))
sys.path.insert(0, str(REPO / "scripts"))
from visualize_streamlit import draw_bounding_boxes  # noqa: E402

REM = REPO / "runs/rdd_yolov8n_local/indo_v2_remapped"
EV = REPO / "runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v2"
WEIGHTS = {
    "yolov8n": REPO / "runs/rdd_yolov8n_local/experiments/yolov8n_class_weight/weights/best.pt",
    "yolov12n": REPO / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt",
    "yolov26n": REPO / "runs/rdd_yolov8n_local/experiments/yolov26n_class_weight/weights/best.pt",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/experiments/yolov8_pd_class_weight/weights/best.pt",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/experiments/yolo_rd_class_weight/weights/best.pt",
}
NAMES = ["Longitudinal_Crack", "Transverse_Crack", "Alligator_Crack", "Pothole", "manhole", "patchy_road"]
DEVICE = 0 if torch.cuda.is_available() else "cpu"

st.set_page_config(page_title="Zero-Shot RDD-indo-v2 Viewer", page_icon="🛣️", layout="wide")
st.title("Zero-Shot ke RDD-indo-v2 — GT vs Prediksi")
st.caption("Bobot N-RDD2024 (sumber) diuji langsung pada RDD-indo-v2 (308 citra test) tanpa fine-tuning. Label GT sudah di-remap ke urutan kelas sumber.")


@st.cache_data(show_spinner=False)
def load_index():
    imgs = sorted((REM / "test/images").glob("*"))
    rows = []
    for p in imgs:
        lf = REM / "test/labels" / (p.stem + ".txt")
        n = sum(1 for l in lf.read_text().splitlines() if l.strip()) if lf.exists() else 0
        rows.append({"filename": p.name, "path": str(p), "n_gt": n})
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def load_gap():
    csv = EV / "domain_gap.csv"
    if csv.exists():
        return pd.read_csv(csv)
    return pd.DataFrame([
        {"model": "yolov12n", "src_test": 0.654, "indo_v2_zs": 0.172},
        {"model": "yolo_rd", "src_test": 0.661, "indo_v2_zs": 0.149},
        {"model": "yolov8_pd", "src_test": 0.646, "indo_v2_zs": 0.149},
        {"model": "yolov8n", "src_test": 0.648, "indo_v2_zs": 0.145},
        {"model": "yolov26n", "src_test": 0.625, "indo_v2_zs": 0.136},
    ])


@st.cache_resource(show_spinner="Memuat bobot model...")
def load_model(name):
    if name in ("yolov8_pd", "yolo_rd"):
        from custom_modules import patch_ultralytics
        patch_ultralytics()
    from ultralytics import YOLO
    return YOLO(str(WEIGHTS[name]))


def read_gt_boxes(img_path):
    lf = REM / "test/labels" / (Path(img_path).stem + ".txt")
    boxes = []
    if not lf.exists():
        return boxes
    W, H = Image.open(img_path).size
    for l in lf.read_text().splitlines():
        p = l.split()
        if len(p) < 5:
            continue
        c, xc, yc, w, h = int(p[0]), float(p[1]), float(p[2]), float(p[3]), float(p[4])
        boxes.append({"class_id": c, "class_name": NAMES[c], "xc": xc, "yc": yc, "w": w, "h": h,
                      "px": [int((xc - w / 2) * W), int((yc - h / 2) * H),
                             int((xc + w / 2) * W), int((yc + h / 2) * H)]})
    return boxes


df = load_index()
if df.empty:
    st.error(f"Tidak ada citra di {REM / 'test/images'}. Pastikan notebook 05_zero_shot_indo_v2.ipynb sel remap sudah dijalankan.")
    st.stop()

with st.expander("Ringkasan domain gap (mAP50 sumber vs zero-shot v2)", expanded=False):
    gap = load_gap()
    st.dataframe(gap, hide_index=True, use_container_width=True)

st.sidebar.header("Pengaturan")
model = st.sidebar.selectbox("Model", options=sorted(WEIGHTS.keys()),
                             index=sorted(WEIGHTS.keys()).index("yolov12n"))
conf_thr = st.sidebar.slider("Threshold confidence prediksi", 0.05, 0.9, 0.25, 0.05)
show_labels = st.sidebar.checkbox("Tampilkan label box", value=True)
only_gt = st.sidebar.checkbox("Hanya citra ber-GT", value=False)
q = st.sidebar.text_input("Cari file", placeholder="cth: 0440")

view = df[df["n_gt"] > 0] if only_gt else df
if q.strip():
    view = view[view["filename"].str.contains(q.strip(), case=False, na=False)]
if view.empty:
    st.warning("Tidak ada citra yang cocok.")
    st.stop()
view = view.reset_index(drop=True)

if st.sidebar.button("Acak citra"):
    st.session_state["idx"] = random.randint(0, len(view) - 1)
idx = st.slider("Navigasi citra", 0, len(view) - 1, st.session_state.get("idx", 0) % len(view))
st.session_state["idx"] = idx
row = view.iloc[idx]

m = load_model(model)
r = m.predict(row["path"], imgsz=640, conf=conf_thr, iou=0.6, verbose=False, device=DEVICE)[0]
W, H = Image.open(row["path"]).size
pred_boxes = []
for b in r.boxes:
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
             use_container_width=True, caption=row["filename"])
with col2:
    st.subheader(f"Prediksi {model} conf>={conf_thr:.2f} ({len(pred_boxes)})")
    st.image(draw_bounding_boxes(row["path"], pred_boxes, True, show_labels),
             use_container_width=True, caption=row["filename"])

c1, c2 = st.columns(2)
with c1:
    if gt_boxes:
        st.dataframe(pd.DataFrame([{"kelas": b["class_name"], "box_px": b["px"]} for b in gt_boxes]),
                     hide_index=True, use_container_width=True)
    else:
        st.info("Tanpa GT (background).")
with c2:
    if pred_boxes:
        st.dataframe(pd.DataFrame([{"kelas": b["class_name"].rsplit(" ", 1)[0],
                                    "conf": b["conf"]} for b in pred_boxes]),
                     hide_index=True, use_container_width=True)
    else:
        st.info("Tidak ada prediksi di atas threshold.")

if __name__ == "__main__":
    pass
