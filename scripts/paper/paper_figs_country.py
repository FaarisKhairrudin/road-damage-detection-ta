#!/usr/bin/env python3
"""Per-country GT vs 3 best models — 3 rows (China/Japan/India) x 4 cols (GT/v12n/RD/PD).

Random 1 image per country seeded 42 for repeatability.

Usage:
  python3.12 scripts/paper/paper_figs_country.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "code/models"))

OUTDIR = REPO / "latex/IEEE-Conference/gambar"
SRC = REPO / "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes"
SRC_NAMES = ["Long_Crack", "Trans_Crack", "Allig_Crack", "Pothole", "manhole", "patchy_road"]
SHORT = {0: "Long", 1: "Trans", 2: "Allig", 3: "Poth", 4: "Manh", 5: "Patchy"}
COLORS = {0: "#2E7D32", 1: "#1565C0", 2: "#EF6C00", 3: "#C62828", 4: "#6A1B9A", 5: "#C2185B"}

WEIGHTS = {
    "yolov12n": REPO / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/experiments/yolo_rd_class_weight/weights/best.pt",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/experiments/yolov8_pd_class_weight/weights/best.pt",
}

plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": 8, "axes.titlesize": 8, "figure.dpi": 300})


def draw_gt(ax, im: Image.Image, lbl_path: Path) -> int:
    ax.imshow(im)
    W, H = im.size
    n = 0
    if lbl_path.exists():
        for line in lbl_path.read_text().splitlines():
            p = line.split()
            if len(p) >= 5:
                cid = int(p[0])
                xc, yc, w, h = float(p[1]), float(p[2]), float(p[3]), float(p[4])
                x1, y1 = (xc - w / 2) * W, (yc - h / 2) * H
                ax.add_patch(Rectangle((x1, y1), w * W, h * H, fill=False,
                                       edgecolor=COLORS.get(cid, "lime"), lw=1.1))
                ax.text(x1, max(0, y1 - 3), SHORT.get(cid, ""), fontsize=5, color="white",
                        bbox={"facecolor": COLORS.get(cid, "lime"), "edgecolor": "none", "pad": 1})
                n += 1
    return n


def draw_pred(ax, im: Image.Image, r) -> int:
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


def draw_gt_thin(ax, im: Image.Image, lbl_path: Path) -> int:
    ax.imshow(im)
    W, H = im.size
    n = 0
    if lbl_path.exists():
        for line in lbl_path.read_text().splitlines():
            p = line.split()
            if len(p) >= 5:
                cid = int(p[0])
                xc, yc, w, h = float(p[1]), float(p[2]), float(p[3]), float(p[4])
                x1, y1 = (xc - w / 2) * W, (yc - h / 2) * H
                ax.add_patch(Rectangle((x1, y1), w * W, h * H, fill=False,
                                       edgecolor=COLORS.get(cid, "lime"), lw=0.7))
                ax.text(x1, max(0, y1 - 2), SHORT.get(cid, ""), fontsize=4.5, color="white",
                        bbox={"facecolor": COLORS.get(cid, "lime"), "edgecolor": "none",
                              "pad": 0.6, "linewidth": 0})
                n += 1
    return n


def country_gt_panel() -> Path:
    """3 typical frames per source domain, GT boxes drawn thin (D3 style + labels)."""
    domains = {
        "China (n=180)": [
            "China_MotorBike_001779_jpg.rf.421b5ffe08eee44952dd87684b106455",
            "China_MotorBike_000863_jpg.rf.2d4381786ca69c456ccd1fa63e9ebebd",
            "China_MotorBike_001890_jpg.rf.7a773b1b80b72c526a32e5a503194dfb",
        ],
        "Japan (n=705)": [
            "Japan_011914_jpg.rf.21e45fabf45ae64ee7838da43ab7d916",
            "Japan_005925_jpg.rf.4bec0906a80834ca7a0fd39d413a3ba3",
            "Japan_008835_jpg.rf.086bc704787936df01e313c03df93d8a",
        ],
        "India (n=110)": [
            "India_004602_jpg.rf.bdf699274c5ba3ca4e98e3baef521881",
            "India_002009_jpg.rf.8f769ac005f920771fc22b0d2540bfff",
            "India_003007_jpg.rf.8847ec3bd891bb5a28cf9fc0f9f73c6c",
        ],
    }
    nrows, ncols = len(domains), 3
    cell = 1.6
    fig = plt.figure(figsize=(cell * ncols, cell * nrows))
    gs = fig.add_gridspec(nrows, ncols, hspace=0.10, wspace=0.05,
                          left=0.15, right=0.99, top=0.99, bottom=0.01)
    for i, (dname, stems) in enumerate(domains.items()):
        for j, stem in enumerate(stems):
            ax = fig.add_subplot(gs[i, j])
            im = Image.open(SRC / "test/images" / f"{stem}.jpg").convert("RGB")
            draw_gt_thin(ax, im, SRC / "test/labels" / f"{stem}.txt")
            ax.axis("off")
            if j == 0:
                ax.text(-0.06, 0.5, dname, fontsize=8, rotation=90,
                        va="center", ha="right", transform=ax.transAxes)
    out = OUTDIR / "paper_fig_country_gt.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    return out


def main() -> None:
    if "--gt-only" in sys.argv:
        country_gt_panel()
        return
    from custom_modules import patch_ultralytics
    from ultralytics import YOLO

    # load models
    patch_ultralytics()
    models = {name: YOLO(str(w)) for name, w in WEIGHTS.items()}

    countries = ["China", "Japan", "India"]
    rng = random.Random(42)
    rows = []
    for c in countries:
        imgs = sorted((SRC / "test/images").glob(f"{c}_*"))
        chosen = rng.choice(imgs)
        lbl = SRC / "test/labels" / (chosen.stem + ".txt")
        rows.append((c, chosen, lbl))

    # batch predict
    img_paths = [r[1] for r in rows]
    preds = {name: list(m.predict([str(p) for p in img_paths], imgsz=640,
                                  conf=0.25, iou=0.6, verbose=False))
             for name, m in models.items()}

    cols = ["GT", "YOLOv12n", "YOLO-RD", "YOLOv8-PD"]
    nrows, ncols = 3, 4
    cell = 1.6
    fig = plt.figure(figsize=(cell * ncols, cell * nrows))
    gs = fig.add_gridspec(nrows, ncols, hspace=0.12, wspace=0.06,
                          left=0.02, right=0.99, top=0.90, bottom=0.02)
    for i, (cty, ip, lp) in enumerate(rows):
        im = Image.open(ip).convert("RGB")
        # GT col
        ax = fig.add_subplot(gs[i, 0])
        n_gt = draw_gt(ax, im, lp)
        ax.axis("off")
        ax.set_title(f"{cty} GT n={n_gt}", fontsize=8)
        # model cols
        for j, (mname, mid) in enumerate(
                zip(cols[1:], ["yolov12n", "yolo_rd", "yolov8_pd"], strict=True), start=1):
            ax = fig.add_subplot(gs[i, j])
            n_pred = draw_pred(ax, im, preds[mid][i])
            ax.axis("off")
            ax.set_title(f"{mname} n={n_pred}", fontsize=8)

    fig.suptitle("Source-domain detection: GT vs 3 models (display conf=0.25)", fontsize=9)
    out = OUTDIR / "paper_fig_country_examples.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    for c, p, _ in rows:
        print(f"  {c}: {p.name}")
    country_gt_panel()


if __name__ == "__main__":
    main()
