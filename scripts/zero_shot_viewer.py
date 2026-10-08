#!/usr/bin/env python3
"""Zero-shot viewer: GT vs prediksi model N-RDD2024 pada data RDD-Indonesia.

Jalankan: streamlit run scripts/zero_shot_viewer.py
"""

from pathlib import Path
import json
import pickle
import random

import pandas as pd
import streamlit as st
from PIL import Image

from visualize_streamlit import draw_bounding_boxes, CLASS_INFO

REPO = Path(__file__).resolve().parent.parent
REM = REPO / "runs/rdd_yolov8n_local/indonesia_remapped"
EV = REPO / "runs/rdd_yolov8n_local/evaluation/zero_shot_indonesia"
SRC_TEST = {"yolov8n": 0.648, "yolov12n": 0.654, "yolov26n": 0.625, "yolov8_pd": 0.646, "yolo_rd": 0.661}
NAMES = ["Longitudinal_Crack", "Transverse_Crack", "Alligator_Crack", "Pothole", "manhole", "patchy_road"]

st.set_page_config(page_title="Zero-Shot Indonesia Viewer", page_icon="🛣️", layout="wide")

st.title("Zero-Shot ke RDD-Indonesia — GT vs Prediksi")
st.caption("Bobot N-RDD2024 (sumber) diuji langsung pada data Bandung tanpa fine-tuning. Label GT sudah di-remap ke urutan kelas sumber.")


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
def load_preds(model):
    with open(EV / f"{model}_preds.pkl", "rb") as f:
        return pickle.load(f)


@st.cache_data(show_spinner=False)
def load_metrics():
    with open(EV / "zs_results.json") as f:
        return json.load(f)


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
                      "px": [int((xc - w / 2) * W), int((yc - h / 2) * H), int((xc + w / 2) * W), int((yc + h / 2) * H)]})
    return boxes


df = load_index()
zs = load_metrics()

with st.expander("Ringkasan domain gap (mAP50 sumber vs zero-shot)", expanded=False):
    rows = [{"model": k, "sumber": SRC_TEST[k], "zero-shot": v["mAP50"],
             "drop": round(v["mAP50"] - SRC_TEST[k], 3)} for k, v in zs.items()]
    st.dataframe(pd.DataFrame(rows).sort_values("zero-shot", ascending=False),
                 hide_index=True, use_container_width=True)

st.sidebar.header("Pengaturan")
model = st.sidebar.selectbox("Model", options=sorted(zs.keys()), index=sorted(zs.keys()).index("yolov12n"))
conf_thr = st.sidebar.slider("Threshold confidence prediksi", 0.05, 0.9, 0.25, 0.05)
show_labels = st.sidebar.checkbox("Tampilkan label box", value=True)
only_gt = st.sidebar.checkbox("Hanya citra ber-GT", value=False)
q = st.sidebar.text_input("Cari file", placeholder="cth: 0328")

view = df[df["n_gt"] > 0] if only_gt else df
if q.strip():
    view = view[view["filename"].str.contains(q.strip(), case=False, na=False)]
if view.empty:
    st.warning("Tidak ada citra yang cocok.")
    st.stop()

if st.sidebar.button("Acak citra"):
    st.session_state["idx"] = random.randint(0, len(view) - 1)
idx = st.slider("Navigasi citra", 0, len(view) - 1, st.session_state.get("idx", 0) % len(view))
st.session_state["idx"] = idx
row = view.iloc[idx]

preds = load_preds(model)
pi = preds["images"].index(row["filename"])
raw = [b for b in preds["preds"][pi] if b[2] >= conf_thr]
W, H = Image.open(row["path"]).size
pred_boxes = [{"class_id": c, "class_name": f"{NAMES[c]} {cf:.2f}",
               "xc": ((x1 + x2) / 2) / W, "yc": ((y1 + y2) / 2) / H,
               "w": (x2 - x1) / W, "h": (y2 - y1) / H} for (x1, y1, x2, y2), c, cf in raw]

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
        st.dataframe(pd.DataFrame([{"kelas": b["class_name"],
                                    "conf": float(b["class_name"].split()[-1])} for b in pred_boxes]),
                     hide_index=True, use_container_width=True)
    else:
        st.info("Tidak ada prediksi di atas threshold.")


if __name__ == "__main__":
    pass
