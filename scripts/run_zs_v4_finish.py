#!/usr/bin/env python3
"""Finishing zero-shot V4: val v8n/v12n (P/R/mAP), plot domain_gap.png,
sampel pred_only + gt_vs_pred. Output -> runs/.../evaluation/zero_shot_indo_v4/."""
import random
import sys
from pathlib import Path
from typing import cast

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as patches  # noqa: E402
import pandas as pd
import torch
from PIL import Image as PILImage
from ultralytics.engine.results import Results

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "code/models"))
from ultralytics import YOLO  # noqa: E402
from custom_modules import patch_ultralytics  # noqa: E402

patch_ultralytics()
print("patch custom aktif", flush=True)
DEVICE = 0 if torch.cuda.is_available() else "cpu"
print("device:", DEVICE, flush=True)

SRC_NAMES = ["Longitudinal_Crack", "Transverse_Crack", "Alligator_Crack",
             "Pothole", "manhole", "patchy_road"]
REM = REPO / "runs/rdd_yolov8n_local/indo_v4_remapped"
EV = REPO / "runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4"
EV.mkdir(parents=True, exist_ok=True)
DATA = str(REM / "indo_v4_remapped.yaml")

WEIGHTS = {
    "yolov8n": REPO / "runs/rdd_yolov8n_local/experiments/yolov8n_class_weight/weights/best.pt",
    "yolov12n": REPO / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt",
    "yolov26n": REPO / "runs/rdd_yolov8n_local/experiments/yolov26n_class_weight/weights/best.pt",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/experiments/yolov8_pd_class_weight/weights/best.pt",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/experiments/yolo_rd_class_weight/weights/best.pt",
}
SRC_TEST = {"yolov8n": 0.648, "yolov12n": 0.654, "yolov26n": 0.625,
            "yolov8_pd": 0.646, "yolo_rd": 0.661}

# 1) val v8n + v12n (3 model lain sudah ada di domain_gap.csv dari run sebelumnya)
zs: dict = {}
for name in ["yolov8n", "yolov12n"]:
    m = YOLO(str(WEIGHTS[name]))
    r = m.val(data=DATA, split="test", imgsz=640, conf=0.001, iou=0.6,
              verbose=False, device=DEVICE)
    zs[name] = {"P": float(r.box.p.mean()), "R": float(r.box.r.mean()),
                "mAP50": float(r.box.map50), "mAP50-95": float(r.box.map)}
    d = zs[name]
    print(f"{name}: P={d['P']:.3f} R={d['R']:.3f} mAP50={d['mAP50']:.3f} "
          f"mAP50-95={d['mAP50-95']:.3f}", flush=True)
    torch.cuda.empty_cache()

old = pd.read_csv(EV / "domain_gap.csv")
full = {row["model"]: {"P": None, "R": None, "mAP50": row["indo_v4_zs"],
                       "mAP50-95": None} for _, row in old.iterrows()}
full.update(zs)
detail = pd.DataFrame([{"model": k, **v} for k, v in full.items()])
detail.to_csv(EV / "zs_detail.csv", index=False)
print(detail.round(3).to_string(index=False), flush=True)

# 2) plot domain gap
df = old.sort_values("indo_v4_zs", ascending=False).reset_index(drop=True)
x = range(len(df))
w = 0.35
plt.figure(figsize=(8, 4))
plt.bar([i - w / 2 for i in x], df["src_test"], width=w, label="sumber (test)")
plt.bar([i + w / 2 for i in x], df["indo_v4_zs"], width=w,
        label="RDD-indo-v4 (zero-shot)")
plt.xticks(list(x), list(df["model"].astype(str)), rotation=20)
plt.ylabel("mAP50")
plt.title("Domain gap: sumber vs zero-shot RDD-indo-v4")
plt.legend()
plt.tight_layout()
plt.savefig(str(EV / "domain_gap.png"), dpi=120)
plt.close()
print("plot OK:", EV / "domain_gap.png", flush=True)

# 3) sampel visual model terbaik
best = df.iloc[0]["model"]
print("model visual:", best, flush=True)
bm = YOLO(str(WEIGHTS[best]))
all_imgs = sorted((REM / "test/images").glob("*"))

imgs = random.Random(42).sample(all_imgs, 6)
res = bm.predict([str(p) for p in imgs], imgsz=640, conf=0.25, iou=0.6,
                 verbose=False, device=DEVICE)
fig, ax = plt.subplots(2, 3, figsize=(12, 8))
for a, r, p in zip(ax.flat, res, imgs, strict=False):
    rr = cast(Results, r)
    boxes = rr.boxes
    n = len(boxes) if boxes is not None else 0
    a.imshow(rr.plot()[:, :, ::-1])
    a.set_title(f"{p.name[:28]}.. n={n}", fontsize=9)
    a.axis("off")
plt.suptitle(f"Prediksi zero-shot {best} pada RDD-indo-v4 (acak, conf=0.25)")
plt.tight_layout()
plt.savefig(str(EV / "zs_samples_pred_only.png"), dpi=120)
plt.close()

gt_imgs = random.Random(7).sample(all_imgs, 4)
res_g = bm.predict([str(p) for p in gt_imgs], imgsz=640, conf=0.25, iou=0.6,
                   verbose=False, device=DEVICE)
fig, axes = plt.subplots(4, 2, figsize=(12, 16))
for row, (p, r) in enumerate(zip(gt_imgs, res_g, strict=False)):
    rr = cast(Results, r)
    boxes = rr.boxes
    n_pred = len(boxes) if boxes is not None else 0
    im = PILImage.open(p).convert("RGB")
    W, H = im.size
    ax_gt, ax_pr = axes[row]
    ax_gt.imshow(im)
    n_gt = 0
    for line in (REM / "test/labels" / (p.stem + ".txt")).read_text().splitlines():
        if not line.strip():
            continue
        q = line.split()
        cid, xc, yc, ww, hh = int(q[0]), *map(float, q[1:5])
        x0, y0 = (xc - ww / 2) * W, (yc - hh / 2) * H
        ax_gt.add_patch(patches.Rectangle((x0, y0), ww * W, hh * H, linewidth=2,
                                          edgecolor="lime", facecolor="none"))
        ax_gt.text(x0, max(y0 - 4, 0), SRC_NAMES[cid], fontsize=7, color="black",
                   bbox={"facecolor": "lime", "alpha": 0.7, "pad": 1, "edgecolor": "none"})
        n_gt += 1
    ax_gt.set_title(f"GT: {p.name[:30]}.. n={n_gt}", fontsize=9)
    ax_gt.axis("off")
    ax_pr.imshow(rr.plot()[:, :, ::-1])
    ax_pr.set_title(f"Pred {best}: {p.name[:30]}.. n={n_pred}", fontsize=9)
    ax_pr.axis("off")
plt.tight_layout()
plt.savefig(str(EV / "zs_samples_gt_vs_pred.png"), dpi=120)
plt.close()
print("sampel OK", flush=True)
print("DONE", flush=True)
