#!/usr/bin/env python3
"""Fig3 (DUMMY): qualitative GT vs 3-model predictions on V4 failure cases.

Dummy image list (user-provided, "Salah prediksi" set):
  Merge-1_mp4-0453, 0497, 0566, 0572, 0571, 0554, 0570
Uses the first 4 by default; extend to 6 by setting N_ROWS=6.

Models: yolov12n / yolo_rd / yolov8_pd (display conf=0.25, NMS IoU=0.6).
GT drawn from data/RDD-indo-v4/valid/labels (target ids 0..4) remapped to
source ids via {0:2, 1:0, 2:5, 3:3, 4:1}.

Output:
  latex/IEEE-Conference/gambar/paper_fig3_qualitative_v4_dummy.png

Usage:
  python3 scripts/paper/paper_fig3_qualitative_v4.py [4|6]
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "code/models"))

V4IMG = REPO / "data/RDD-indo-v4/valid/images"
V4LBL = REPO / "data/RDD-indo-v4/valid/labels"
OUT = REPO / "latex/IEEE-Conference/gambar/paper_fig3_qualitative_v4_dummy.png"

WEIGHTS = {
    "yolov12n": REPO / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/experiments/yolo_rd_class_weight/weights/best.pt",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/experiments/yolov8_pd_class_weight/weights/best.pt",
}

# target-id -> source-id, target names, source names
REMAP = {0: 2, 1: 0, 2: 5, 3: 3, 4: 1}
SRC_NAMES = [
    "Longitudinal_Crack",
    "Transverse_Crack",
    "Alligator_Crack",
    "Pothole",
    "manhole",
    "patchy_road",
]
COLORS = {
    0: "#2E7D32",  # Long green
    1: "#1565C0",  # Trans blue
    2: "#EF6C00",  # Allig orange
    3: "#C62828",  # Pothole red
    4: "#6A1B9A",  # manhole purple
    5: "#C2185B",  # patchy pink
}

DUMMY_STEMS = [
    "Merge-1_mp4-0453",
    "Merge-1_mp4-0497",
    "Merge-1_mp4-0566",
    "Merge-1_mp4-0572",
    "Merge-1_mp4-0571",
    "Merge-1_mp4-0554",
]

CONF, IOU = 0.25, 0.6

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 9,
        "axes.titlesize": 9,
        "figure.dpi": 300,
    }
)


def find_image(stem: str) -> Path:
    hits = sorted(V4IMG.glob(stem + "*.jpg"))
    if not hits:
        raise FileNotFoundError(f"no image for {stem}")
    return hits[0]


def read_gt(img: Path) -> list[tuple[int, float, float, float, float]]:
    """Return list of (source_id, xc, yc, w, h) in YOLO normalized coords."""
    lbl = V4LBL / (img.name.replace(".jpg", ".txt"))
    # labels use full rf filename; fall back to stem glob
    if not lbl.exists():
        cands = sorted(V4LBL.glob(img.stem.split("_jpg")[0] + "*.txt"))
        lbl = cands[0] if cands else lbl
    boxes = []
    if lbl.exists():
        for line in lbl.read_text().splitlines():
            p = line.split()
            if len(p) >= 5:
                boxes.append((REMAP[int(float(p[0]))], float(p[1]), float(p[2]), float(p[3]), float(p[4])))
    return boxes


def load_models():
    from ultralytics import YOLO

    models = {}
    for name, w in WEIGHTS.items():
        if name in ("yolov8_pd", "yolo_rd"):
            from custom_modules import patch_ultralytics

            patch_ultralytics()
        models[name] = YOLO(str(w))
    return models


def main() -> None:
    n_rows = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    stems = DUMMY_STEMS[:n_rows]
    models = load_models()
    paths = [find_image(s) for s in stems]

    # batch inference per model
    preds: dict[str, list] = {}
    for name, m in models.items():
        res = m.predict([str(p) for p in paths], imgsz=640, conf=CONF, iou=IOU, verbose=False)
        preds[name] = res

    cell = 1.55
    fig = plt.figure(figsize=(cell * 4, cell * n_rows))
    gs = fig.add_gridspec(n_rows, 4, hspace=0.06, wspace=0.04,
                          left=0.01, right=0.99, top=0.93, bottom=0.01)
    for i, img_path in enumerate(paths):
        im = Image.open(img_path).convert("RGB")
        W, H = im.size
        gt = read_gt(img_path)

        panels: list[tuple[str, Any]] = [("GT", None)] + [
            ("YOLOv12n", preds["yolov12n"][i]),
            ("YOLO-RD", preds["yolo_rd"][i]),
            ("YOLOv8-PD", preds["yolov8_pd"][i]),
        ]
        for j, (title, r) in enumerate(panels):
            ax = fig.add_subplot(gs[i, j])
            ax.imshow(im)
            ax.axis("off")
            if r is None:  # GT
                for cid, xc, yc, w, h in gt:
                    x1, y1 = (xc - w / 2) * W, (yc - h / 2) * H
                    ax.add_patch(Rectangle((x1, y1), w * W, h * H, fill=False, edgecolor=COLORS[cid], lw=1.2))
                    ax.text(x1, max(0, y1 - 4), SRC_NAMES[cid], fontsize=5, color="white",
                            bbox={"facecolor": COLORS[cid], "edgecolor": "none", "pad": 1})
            else:
                if r.boxes is not None and len(r.boxes) > 0:
                    for b in r.boxes:
                        cid = int(b.cls)
                        conf = float(b.conf)
                        x1, y1, x2, y2 = (float(v) for v in b.xyxy[0].tolist())
                        # rescale 640-letterboxed xyxy back to original: ultralytics returns orig coords
                        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False,
                                               edgecolor=COLORS.get(cid, "yellow"), lw=1.2))
                        ax.text(x1, max(0, y1 - 4), f"{SRC_NAMES[cid]} {conf:.2f}", fontsize=5,
                                color="white", bbox={"facecolor": COLORS.get(cid, "black"),
                                                     "edgecolor": "none", "pad": 1})
            if i == 0:
                ax.set_title(title, fontsize=8, pad=3)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote {OUT} ({OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
