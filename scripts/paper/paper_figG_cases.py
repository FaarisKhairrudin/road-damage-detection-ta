#!/usr/bin/env python3
"""Fig 3 versi 4x4 untuk 1 kolom IEEE: 4 kasus x 4 kolom (GT + 3 model).

Baris (2 gagal + 2 benar):
  1. mp4-0036  G1 baris 1  gagal  (pori beton ditembak Patchy/Pothole)
  2. mp4-0015  G1 baris 2  gagal  (retak melintang, model gagal)
  3. mp4-0436  G2 baris 1  benar  (retak memanjang, ketiga model benar)
  4. mp4-0727  G2 baris 3  benar  (tiga anotasi, ketiga model menembak)

Kolom: GT / YOLOv12n / YOLO-RD / YOLOv8-PD.

Gaya mengikuti paper_figs_final_G.py: tanpa judul utama, header kolom hanya di
baris pertama, jarak rapat. Ukuran sel dibuat kecil supaya saat diperkecil ke
lebar 1 kolom IEEE (~3,5 inci) label box tetap terbaca.

Output: latex/IEEE-Conference/gambar/paper_figG_cases_4x4.png

Usage:
  python3.12 scripts/paper/paper_figG_cases.py
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
OUTDIR = REPO / "latex/IEEE-Conference/gambar"

WEIGHTS = {
    "yolov12n": REPO / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/experiments/yolo_rd_class_weight/weights/best.pt",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/experiments/yolov8_pd_class_weight/weights/best.pt",
}
REMAP = {0: 2, 1: 0, 2: 5, 3: 3, 4: 1}
SHORT = {0: "Long", 1: "Trans", 2: "Allig", 3: "Poth", 4: "Manh", 5: "Patchy"}
COLORS = {0: "#2E7D32", 1: "#1565C0", 2: "#EF6C00", 3: "#C62828", 4: "#6A1B9A", 5: "#C2185B"}

# 2 gagal (G1 baris 1-2) + 2 benar (G2 baris 1 dan 3)
STEMS = ["mp4-0036", "mp4-0015", "mp4-0436", "mp4-0727"]
COLS = ["GT", "YOLOv12n", "YOLO-RD", "YOLOv8-PD"]
KEY = {"YOLOv12n": "yolov12n", "YOLO-RD": "yolo_rd", "YOLOv8-PD": "yolov8_pd"}

CONF, IOU = 0.25, 0.6
# Figure dibuat ~3,5 inci (lebar 1 kolom IEEE) supaya saat masuk PDF hampir tidak
# diperkecil, sehingga label box tetap terbaca. 4 kolom x 0,88 inci = 3,52 inci.
CELL = 0.88
FS_BOX = 5   # font label box (kecil, digambar di dalam kotak)
FS_HEAD = 8  # font header kolom

plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": FS_BOX, "figure.dpi": 300})


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
    from custom_modules import patch_ultralytics
    from ultralytics import YOLO

    patch_ultralytics()
    return {name: YOLO(str(w)) for name, w in WEIGHTS.items()}


def put_label(ax: Any, x1: float, y1: float, text: str, facecolor: str,
              img_h: int) -> None:
    """Gambar label di DALAM kotak, tepat di bawah tepi atas.

    Kalau label ditaruh di atas kotak, box yang menempel tepi atas gambar akan
    meluber ke sel baris sebelumnya. Menaruhnya di dalam membuat label selalu
    terkurung di selnya sendiri.
    """
    off = 0.013 * img_h
    ax.text(x1 + off, y1 + off, text, fontsize=FS_BOX, color="white",
            va="top", ha="left",
            bbox={"facecolor": facecolor, "edgecolor": "none", "pad": 0.4})


def draw_gt(ax: Any, im: Any, gt: list) -> None:
    W, H = im.size
    ax.imshow(im)
    for cid, xc, yc, w, h in gt:
        x1, y1 = (xc - w / 2) * W, (yc - h / 2) * H
        ax.add_patch(Rectangle((x1, y1), w * W, h * H, fill=False,
                               edgecolor=COLORS[cid], lw=1.0))
        put_label(ax, x1, y1, SHORT[cid], COLORS[cid], H)


def draw_pred(ax: Any, im: Image.Image, r: Any) -> None:
    ax.imshow(im)
    _, H = im.size
    boxes = getattr(r, "boxes", None)
    if boxes is not None and len(boxes) > 0:
        for b in boxes:
            cid = int(b.cls)
            conf = float(b.conf)
            x1, y1, x2, y2 = (float(v) for v in b.xyxy[0].tolist())
            ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False,
                                   edgecolor=COLORS.get(cid, "yellow"), lw=1.0))
            put_label(ax, x1, y1, f"{SHORT.get(cid, cid)} {conf:.2f}",
                      COLORS.get(cid, "black"), H)


def main() -> None:
    models = load_models()
    paths = [find_image(s) for s in STEMS]
    ims = [Image.open(p).convert("RGB") for p in paths]
    gts = [read_gt(p) for p in paths]
    preds = {name: m.predict([str(p) for p in paths], imgsz=640, conf=CONF,
                             iou=IOU, verbose=False) for name, m in models.items()}

    nrows, ncols = len(STEMS), len(COLS)
    fig = plt.figure(figsize=(CELL * ncols, CELL * nrows))
    gs = fig.add_gridspec(nrows, ncols, hspace=0.05, wspace=0.04,
                          left=0.01, right=0.99, top=0.955, bottom=0.005)
    for i in range(nrows):
        for j, c in enumerate(COLS):
            ax = fig.add_subplot(gs[i, j])
            ax.axis("off")
            if c == "GT":
                draw_gt(ax, ims[i], gts[i])
            else:
                draw_pred(ax, ims[i], preds[KEY[c]][i])
            if i == 0:
                ax.set_title(c, fontsize=FS_HEAD, pad=3)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / "paper_figG_cases_4x4.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    for s, p in zip(STEMS, paths, strict=True):
        print(f"  {s}: {p.name}")


if __name__ == "__main__":
    main()
