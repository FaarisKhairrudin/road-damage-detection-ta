"""Visualisasi: FP-proxy (per-gambar, dipakai di notebook 04_*) vs FP beneran (IoU-match).

- FP-proxy : semua prediksi Pothole pada gambar yang memuat GT manhole/patchy,
             dibagi GT pengecoh. TIDAK dicek tumpang tindihnya.
- FP beneran: prediksi Pothole dengan IoU >= IOU_MATCH terhadap box GT
              manhole/patchy (model beneran salah label objek pengecoh).

Model : yolov8n 6-kelas (baseline), split TEST saja, conf=0.25, iou=0.6.
Output: PNG 2x2 + CSV detail per-gambar.
"""

from pathlib import Path

import cv2  # type: ignore[import-unresolved, import-not-found]
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from ultralytics import YOLO  # type: ignore[import-unresolved, import-not-found]

REPO = Path("/mnt/Data/01_Akademik/TA-Project")
SRC = (
    REPO
    / "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes"
    / "RDD_Split_Final_china_japan_india_6_classes"
    / "test"
)
IMGDIR, LBDIR = SRC / "images", SRC / "labels"
WEIGHTS = REPO / "runs/rdd_yolov8n_local/experiments/yolov8n_class_weight/weights/best.pt"
OUT_PNG = REPO / "runs/rdd_yolov8n_local/viz_fp_overlap_yolov8n_test.png"
OUT_CSV = REPO / "runs/rdd_yolov8n_local/viz_fp_overlap_detail.csv"

CONF, IOU_NMS, IMGSZ = 0.25, 0.60, 640
IOU_MATCH = 0.5
POTHOLE = 3
DISTR = {4: "manhole", 5: "patchy_road"}
CLS_NAME = {0: "Longitudinal", 1: "Transverse", 2: "Alligator", 3: "Pothole",
            4: "manhole", 5: "patchy_road"}
BOX_COLOR = {0: "gray", 1: "gray", 2: "gray", 3: "red", 4: "cyan", 5: "orange"}


def xywhn_to_xyxy(line, w, h):
    cid, xc, yc, bw, bh = int(line[0]), *map(float, line[1:6])
    x1, y1 = (xc - bw / 2) * w, (yc - bh / 2) * h
    x2, y2 = (xc + bw / 2) * w, (yc + bh / 2) * h
    return cid, np.array([x1, y1, x2, y2])


def iou_matrix(a, b):
    """a: (N,4), b: (M,4) -> (N,M)."""
    if len(a) == 0 or len(b) == 0:
        return np.zeros((len(a), len(b)))
    inter_x1 = np.maximum(a[:, None, 0], b[None, :, 0])
    inter_y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    inter_x2 = np.minimum(a[:, None, 2], b[None, :, 2])
    inter_y2 = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.clip(inter_x2 - inter_x1, 0, None) * np.clip(inter_y2 - inter_y1, 0, None)
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    return inter / (area_a[:, None] + area_b[None, :] - inter + 1e-9)


# ── 1. Kumpulkan gambar test berpengecoh + GT ──
items = []  # (stem, img_path, gt_list[(cid, box)])
for lp in sorted(LBDIR.glob("*.txt")):
    if lp.name.lower() == "classes.txt":
        continue
    img_path = next((IMGDIR / f"{lp.stem}{e}" for e in
                     [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
                     if (IMGDIR / f"{lp.stem}{e}").exists()), None)
    if img_path is None:
        continue
    img = cv2.imread(str(img_path))
    if img is None:
        continue
    h, w = img.shape[:2]
    gts = []
    for ln in lp.read_text(errors="ignore").splitlines():
        p = ln.strip().split()
        if p:
            gts.append(xywhn_to_xyxy(p, w, h))
    if any(c in DISTR for c, _ in gts):
        items.append((lp.stem, img_path, gts))
print(f"Gambar test berpengecoh: {len(items)}")

# ── 2. Prediksi ──
model = YOLO(str(WEIGHTS))
print("names model:", model.names)
res = []
BATCH = 8
paths = [str(p) for _, p, _ in items]
for i in range(0, len(paths), BATCH):
    res.extend(model.predict(paths[i:i + BATCH], imgsz=IMGSZ,
                             conf=CONF, iou=IOU_NMS, device=0, verbose=False))
    import torch as _t  # type: ignore[import-unresolved, import-not-found]
    if _t.cuda.is_available():
        _t.cuda.empty_cache()
assert len(res) == len(items)

# ── 3. IoU-match + statistik proxy vs beneran ──
rows, proxy_fp, true_fp, n_gt = [], 0, 0, {4: 0, 5: 0}
for (stem, img_path, gts), r in zip(items, res):
    gt_boxes = {}
    for c in DISTR:
        arr = np.array([b for cc, b in gts if cc == c], dtype=float)
        gt_boxes[c] = arr.reshape(-1, 4) if arr.size else np.zeros((0, 4))
    for c in DISTR:
        n_gt[c] += len(gt_boxes[c])
    if r.boxes is None:
        preds = np.zeros((0, 6))
    else:
        preds = np.concatenate([r.boxes.xyxy.cpu().numpy(),
                                r.boxes.cls.cpu().numpy()[:, None],
                                r.boxes.conf.cpu().numpy()[:, None]], axis=1)
    pot = preds[preds[:, 4] == POTHOLE][:, [0, 1, 2, 3, 5]] if len(preds) else np.zeros((0, 5))
    dbox = np.concatenate([gt_boxes[4], gt_boxes[5]], axis=0) if (
        len(gt_boxes[4]) + len(gt_boxes[5])) else np.zeros((0, 4))
    ious = iou_matrix(pot[:, :4], dbox) if len(pot) and len(dbox) else np.zeros((len(pot), 0))
    best = ious.max(axis=1) if ious.size else np.zeros(len(pot))
    proxy_fp += len(pot)
    true_fp += int((best >= IOU_MATCH).sum())
    rows.append({"stem": stem, "img": str(img_path), "gts": gts, "preds": preds,
                 "n_pot": len(pot), "best_iou": best,
                 "n_true_fp": int((best >= IOU_MATCH).sum())})
print(f"GT manhole={n_gt[4]} patchy={n_gt[5]} | proxy FP={proxy_fp} "
      f"-> rate={proxy_fp / sum(n_gt.values()):.4f} | TRUE overlap FP={true_fp} "
      f"-> rate={true_fp / sum(n_gt.values()):.4f}")

# ── 4. Pilih 4 contoh ──
def first(cond):
    return next((r for r in rows if cond(r)), None)

# A: FP beneran — pred Pothole IoU tertinggi vs GT manhole
cand_a = [r for r in rows if r["n_true_fp"] > 0 and any(
    c == 4 for c, _ in r["gts"])]
ex_a = max(cand_a, key=lambda r: r["best_iou"].max()) if cand_a else None
picked = {ex_a["stem"]} if ex_a else set()
# B: proxy saja — ada pred Pothole tapi IoU vs pengecoh < 0.1, gambar beda dari A
ex_b = first(lambda r: r["stem"] not in picked and r["n_pot"] > 0 and r["n_true_fp"] == 0
             and (r["best_iou"].max() if len(r["best_iou"]) else 0) < 0.1)
picked.add(ex_b["stem"]) if ex_b else None
# C: penanganan benar — GT manhole diprediksi manhole (IoU>=0.5), tanpa FP overlap
def is_correct(r):
    if r["n_true_fp"] > 0:
        return False
    gb = np.array([b for c, b in r["gts"] if c == 4])
    pb = r["preds"][(r["preds"][:, 4] == 4)][:, :4] if len(r["preds"]) else np.zeros((0, 4))
    return len(gb) and len(pb) and (iou_matrix(pb, gb).max(axis=1) >= 0.5).any()
def is_correct_fresh(r):
    return r["stem"] not in picked and is_correct(r)
ex_c = first(is_correct_fresh)
picked.add(ex_c["stem"]) if ex_c else None
# D: FP beneran vs patchy_road (fallback: FP beneran lain)
cand_all = [r for r in rows if r["n_true_fp"] > 0 and r["stem"] not in picked]
ex_d = max(cand_all, key=lambda r: r["best_iou"].max()) if cand_all else None

examples = [
    (ex_a, "A. FP BENERAN: prediksi Pothole tepat di atas GT manhole\n(model salah label objek pengecoh)"),
    (ex_b, "B. DIHITUNG PROXY tapi BUKAN FP beneran\n(prediksi Pothole tidak menyentuh GT pengecoh)"),
    (ex_c, "C. PENANGANAN BENAR: GT manhole diprediksi manhole\n(objek pengecoh terserap ke kelas yang benar)"),
    (ex_d, "D. FP BENERAN lain (vs patchy_road / manhole kedua)\n(kasus salah label tambahan)"),
]
assert all(e for e, _ in examples), "contoh tidak lengkap, cek kandidat"

# ── 5. Plot ──
fig, axes = plt.subplots(2, 2, figsize=(20, 14))
for ax, (ex, title) in zip(axes.flat, examples, strict=True):
    assert ex is not None, "contoh kosong — cek kandidat di atas"
    img = cv2.cvtColor(cv2.imread(ex["img"]), cv2.COLOR_BGR2RGB)
    ax.imshow(img)
    for c, b in ex["gts"]:
        x1, y1, x2, y2 = b
        edge = "lime" if c in DISTR else "white"
        ax.add_patch(patches.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False,
                                   edgecolor=edge, linewidth=3))
        ax.text(x1, max(y1 - 8, 0), f"GT {CLS_NAME[c]}", color="black",
                fontsize=11, weight="bold",
                bbox={"facecolor": "lime" if c in DISTR else "white",
                          "alpha": 0.9, "pad": 2, "edgecolor": "none"})
    pot_j = 0  # index khusus urutan prediksi Pothole (best_iou sejajar ini, bukan i global)
    for (x1, y1, x2, y2, c, cf) in ex["preds"]:

        style = "--" if int(c) == POTHOLE else "-"
        lw = 3 if int(c) in (POTHOLE, 4, 5) else 1.5
        ax.add_patch(patches.Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False,
                                   edgecolor=BOX_COLOR[int(c)], linewidth=lw,
                                   linestyle=style))
        tag = f"pred {CLS_NAME[int(c)]} {cf:.2f}"
        if int(c) == POTHOLE:
            if pot_j < len(ex["best_iou"]):
                tag += f" | IoU-vs-pengecoh={ex['best_iou'][pot_j]:.2f}"
            pot_j += 1
        ax.text(x2 + 4, y1, tag, color="white", fontsize=10, weight="bold",
                bbox={"facecolor": BOX_COLOR[int(c)], "alpha": 0.9, "pad": 2, "edgecolor": "none"})
    ax.set_title(f"{title}\n[{ex['stem']}]", fontsize=13, weight="bold", loc="left")
    ax.axis("off")

fig.suptitle(
    f"yolov8n 6-kelas @ test — proxy FP={proxy_fp}/{sum(n_gt.values())} "
    f"({proxy_fp / sum(n_gt.values()):.4f}) vs TRUE overlap FP (IoU\u22650.5)="
    f"{true_fp}/{sum(n_gt.values())} ({true_fp / sum(n_gt.values()):.4f})  "
    "| hijau solid=GT pengecoh, merah putus-putus=pred Pothole",
    fontsize=14, weight="bold", y=0.99)
fig.tight_layout()
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT_PNG, dpi=110, bbox_inches="tight")
print("PNG:", OUT_PNG)

pd.DataFrame([{"stem": r["stem"], "n_pred_pothole": r["n_pot"],
               "n_true_overlap_fp": r["n_true_fp"],
               "max_iou_vs_distractor": (r["best_iou"].max()
                                         if len(r["best_iou"]) else 0)}
              for r in rows]).to_csv(OUT_CSV, index=False)
print("CSV:", OUT_CSV)
