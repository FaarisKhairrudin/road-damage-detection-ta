#!/usr/bin/env python3
"""Plot final kurasi G1/G2/G3 — compact untuk paper, hemat tempat.

Pilihan user:
  G1 (GT + 3 model, pantulan + tekstur pori): mp4-0036, mp4-0015, mp4-0041
  G2 (GT + 3 model, prediksi benar): mp4-0436, mp4-0441, mp4-0727
  G3 (pred 3 model saja, tanpa GT): mp4-0716, mp4-0734, mp4-0768

Model: yolov12n / yolo_rd / yolov8_pd (display conf=0.25, NMS 0.6).
GT dari label V4 diremap target->sumber {0:2, 1:0, 2:5, 3:3, 4:1}.

Output:
  latex/IEEE-Conference/gambar/paper_figG1_glare.png   (3x4)
  latex/IEEE-Conference/gambar/paper_figG2_correct.png  (3x4)
  latex/IEEE-Conference/gambar/paper_figG3_predonly.png (3x3)

Usage:
  python3.12 scripts/paper/paper_figs_final_G.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "code/models"))

V4IMG = REPO / "data/RDD-indo-v4/valid/images"
V4LBL = REPO / "data/RDD-indo-v4/valid/labels"
OUTDIR = REPO / "latex/IEEE-Conference/gambar"

WEIGHTS = {
    "yolov12n": REPO / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/experiments/yolo_rd_class_weight/weights/best.pt",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/experiments/yolov8_pd_class_weight/weights/best.pt",
}
REMAP = {0: 2, 1: 0, 2: 5, 3: 3, 4: 1}
SRC_NAMES = ["Longitudinal_Crack", "Transverse_Crack", "Alligator_Crack",
             "Pothole", "manhole", "patchy_road"]
SHORT = {0: "Long", 1: "Trans", 2: "Allig", 3: "Poth", 4: "Manh", 5: "Patchy"}
COLORS = {0: "#2E7D32", 1: "#1565C0", 2: "#EF6C00", 3: "#C62828", 4: "#6A1B9A", 5: "#C2185B"}

G1 = ["mp4-0036", "mp4-0015", "mp4-0041"]
G2 = ["mp4-0436", "mp4-0441", "mp4-0727"]
G3 = ["mp4-0716", "mp4-0734", "mp4-0768"]

CONF, IOU = 0.25, 0.6

plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": 8, "axes.titlesize": 8, "figure.dpi": 300})


def find_image(stem_part: str) -> Path:
    hits = sorted(V4IMG.glob(f"*{stem_part}*.jpg"))
    if not hits:
        raise FileNotFoundError(stem_part)
    return hits[0]


def read_gt(img: Path) -> list:
    lbl = V4LBL / (img.stem + ".txt")
    if not lbl.exists():
        cands = sorted(V4LBL.glob(img.stem.split("_jpg")[0] + "*.txt"))
        lbl = cands[0] if cands else lbl
    boxes = []
    if lbl.exists():
        for line in lbl.read_text().splitlines():
            p = line.split()
            if len(p) >= 5:
                boxes.append((REMAP[int(float(p[0]))], float(p[1]), float(p[2]),
                              float(p[3]), float(p[4])))
    return boxes


def load_models() -> dict:
    from ultralytics import YOLO

    models = {}
    for name, w in WEIGHTS.items():
        if name in ("yolov8_pd", "yolo_rd"):
            from custom_modules import patch_ultralytics

            patch_ultralytics()
        models[name] = YOLO(str(w))
    return models


def draw_gt(ax: Any, im: Any, gt: list) -> None:
    W, H = im.size
    ax.imshow(im)
    for cid, xc, yc, w, h in gt:
        x1, y1 = (xc - w / 2) * W, (yc - h / 2) * H
        ax.add_patch(Rectangle((x1, y1), w * W, h * H, fill=False,
                               edgecolor=COLORS[cid], lw=1.1))
        ax.text(x1, max(0, y1 - 3), SHORT[cid], fontsize=5, color="white",
                bbox={"facecolor": COLORS[cid], "edgecolor": "none", "pad": 1})


def draw_pred(ax: Any, im: Image.Image, r: Any) -> int:
    ax.imshow(im)
    n = 0
    boxes = getattr(r, "boxes", None)
    if boxes is not None and len(boxes) > 0:
        for b in boxes:
            cid = int(b.cls)
            conf = float(b.conf)
            x1, y1, x2, y2 = (float(v) for v in b.xyxy[0].tolist())
            ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False,
                                   edgecolor=COLORS.get(cid, "yellow"), lw=1.1))
            ax.text(x1, max(0, y1 - 3), f"{SHORT.get(cid, cid)} {conf:.2f}",
                    fontsize=5, color="white",
                    bbox={"facecolor": COLORS.get(cid, "black"), "edgecolor": "none", "pad": 1})
            n += 1
    return n


def panel_fig(stems: list, cols: list, fname: str) -> Path:
    models = load_models()
    paths = [find_image(s) for s in stems]
    ims = [Image.open(p).convert("RGB") for p in paths]
    gts = [read_gt(p) for p in paths]
    preds = {name: m.predict([str(p) for p in paths], imgsz=640, conf=CONF,
                             iou=IOU, verbose=False) for name, m in models.items()}
    nrows, ncols = len(stems), len(cols)
    cell = 1.55
    fig = plt.figure(figsize=(cell * ncols, cell * nrows))
    gs = fig.add_gridspec(nrows, ncols, hspace=0.06, wspace=0.04,
                          left=0.01, right=0.99, top=0.93, bottom=0.01)
    for i in range(nrows):
        for j, c in enumerate(cols):
            ax = fig.add_subplot(gs[i, j])
            ax.axis("off")
            if c == "GT":
                draw_gt(ax, ims[i], gts[i])
            else:
                key = {"YOLOv12n": "yolov12n", "YOLO-RD": "yolo_rd",
                       "YOLOv8-PD": "yolov8_pd"}[c]
                draw_pred(ax, ims[i], preds[key][i])
            if i == 0:
                ax.set_title(c, fontsize=8, pad=3)
    out = OUTDIR / fname
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    return out


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    panel_fig(G1, ["GT", "YOLOv12n", "YOLO-RD", "YOLOv8-PD"],
              "paper_figG1_glare.png")
    panel_fig(G2, ["GT", "YOLOv12n", "YOLO-RD", "YOLOv8-PD"],
              "paper_figG2_correct.png")
    panel_fig(G3, ["YOLOv12n", "YOLO-RD", "YOLOv8-PD"],
              "paper_figG3_predonly.png")


if __name__ == "__main__":
    main()
