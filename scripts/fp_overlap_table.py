"""Tabel FP/GT Pothole per model — proxy (metode lama) vs TRUE overlap (IoU-based).

Dua definisi yang dibandingkan, split TEST, conf=0.25, iou(NMS)=0.60, imgsz=640:

- PROXY (metode notebook 04_* / confusion_6cls_vs_4cls.py):
    jumlah SEMUA prediksi Pothole pada gambar yang memuat GT pengecoh
    -------------------------------------------------------------- x GT kelas tsb.
- TRUE overlap (FP beneran):
    jumlah prediksi Pothole yang IoU >= 0.5 dengan >=1 box GT pengecoh,
    dibagi jumlah GT pengecoh.

Model 6-kelas: v8n, v12n, v26n, v8pd. Model 4-kelas: hanya v8pd yang bobot
finalnya ada di repo; v8n/v12n/v26n 4-kelas hanya tersedia angka proxy
referensi dari run 2025-08-07 (runs/rdd_yolov8n_local/confusion_6cls_vs_4cls.csv).

Output:
    runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv
    + tabel markdown ke stdout.
"""

from pathlib import Path
from typing import Any

import cv2  # type: ignore[import-unresolved, import-not-found]
import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import torch  # type: ignore[import-unresolved, import-not-found]
from ultralytics import YOLO  # type: ignore[import-unresolved, import-not-found]

REPO = Path("/mnt/Data/01_Akademik/TA-Project")

# ── 0. Patch ultralytics utk bobot arsitektur custom (v8_pd / yolo_rd) ──────
# Sama dengan guard di notebook 04_3: daftarkan class custom (PAFPD, WTConv, dll)
# SEBELUM YOLO(bobot custom) dipanggil, kalau tidak ModuleNotFoundError: custom_modules.
import sys

CUSTOM_DIR = REPO / "code/models"
if str(CUSTOM_DIR) not in sys.path:
    sys.path.insert(0, str(CUSTOM_DIR))
from custom_modules import patch_ultralytics  # type: ignore[import-unresolved, import-not-found]

patch_ultralytics()
from ultralytics.nn import tasks as _tasks  # type: ignore[import-unresolved, import-not-found]

assert hasattr(_tasks, "PAFPD") or hasattr(_tasks, "BoT"), (
    "patch_ultralytics() belum aktif — class custom tidak terdaftar")
print("patch_ultralytics() aktif — bobot custom (v8_pd) bisa dimuat")

SRC = (
    REPO
    / "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes"
    / "RDD_Split_Final_china_japan_india_6_classes"
    / "test"
)
IMGDIR, LBDIR = SRC / "images", SRC / "labels"
OUT_CSV = REPO / "runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv"

CONF, IOU_NMS, IMGSZ = 0.25, 0.60, 640
IOU_MATCH = 0.5
POTHOLE = 3
DISTR = {4: "manhole", 5: "patchy_road"}
BATCH = 8

E6 = REPO / "runs/rdd_yolov8n_local/experiments"
E4 = REPO / "runs/rdd_4class_local/experiments"
MODELS = [
    ("yolov8n_6cls", E6 / "yolov8n_class_weight/weights/best.pt", 6),
    ("yolov12n_6cls", E6 / "yolov12n_class_weight/weights/best.pt", 6),
    ("yolov26n_6cls", E6 / "yolov26n_class_weight/weights/best.pt", 6),
    ("yolov8_pd_6cls", E6 / "yolov8_pd_class_weight/weights/best.pt", 6),
    ("yolov8n_4cls", E4 / "yolov8n_4cls_class_weights/weights/best.pt", 4),
    ("yolov12n_4cls", E4 / "yolov12n_4cls_class_weights/weights/best.pt", 4),
    ("yolov26n_4cls", E4 / "yolov26n_4cls_class_weights/weights/best.pt", 4),
    ("yolov8_pd_4cls", E4 / "yolov8_pd_4cls_class_weights/weights/best.pt", 4),
]
# Proxy referensi utk bobot 4-kelas yang tidak ada di repo (run 2025-08-07, test-only)
PROXY_REF = {
    "yolov8n_4cls": (0.1651, 0.2029, 0.1513),
    "yolov12n_4cls": (0.1371, 0.1304, 0.1231),
    "yolov26n_4cls": (0.1589, 0.1884, 0.1487),
}


def xywhn_to_xyxy(line, w, h):
    cid, xc, yc, bw, bh = int(line[0]), *map(float, line[1:6])
    return cid, np.array([(xc - bw / 2) * w, (yc - bh / 2) * h,
                          (xc + bw / 2) * w, (yc + bh / 2) * h])


def iou_matrix(a, b):
    if len(a) == 0 or len(b) == 0:
        return np.zeros((len(a), len(b)))
    ix1 = np.maximum(a[:, None, 0], b[None, :, 0])
    iy1 = np.maximum(a[:, None, 1], b[None, :, 1])
    ix2 = np.minimum(a[:, None, 2], b[None, :, 2])
    iy2 = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.clip(ix2 - ix1, 0, None) * np.clip(iy2 - iy1, 0, None)
    area_a = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1])
    area_b = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    return inter / (area_a[:, None] + area_b[None, :] - inter + 1e-9)


# ── 1. Kumpulkan gambar test berpengecoh + GT per kelas ──────────────────────
items = []  # (stem, img_path, {cid: array GT (n,4)})
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
    per_cls = {c: [] for c in DISTR}
    for ln in lp.read_text(errors="ignore").splitlines():
        p = ln.strip().split()
        if p and int(p[0]) in DISTR:
            cid, box = xywhn_to_xyxy(p, w, h)
            per_cls[cid].append(box)
    if any(per_cls.values()):
        items.append((lp.stem, img_path,
                      {c: np.array(v) if v else np.zeros((0, 4))
                       for c, v in per_cls.items()}))

n_gt = {c: sum(int(len(g[c])) for _, _, g in items) for c in DISTR}
n_gt_total = sum(n_gt.values())
n_img_m = sum(1 for _, _, g in items if len(g[4]))
n_img_p = sum(1 for _, _, g in items if len(g[5]))
print(f"Gambar test berpengecoh: {len(items)} (manhole {n_img_m}, patchy {n_img_p})")
print(f"GT: manhole={n_gt[4]}  patchy={n_gt[5]}  total={n_gt_total}\n")

paths = [str(p) for _, p, _ in items]

# ── 2. Evaluasi per model ────────────────────────────────────────────────────
rows = []
for label, weights, nc in MODELS:
    row = {"model": label, "nc": nc, "weights_found": weights.exists()}
    if not weights.exists():
        print(f"[-] {label}: bobot tidak ada, lewati ({weights})")
        rows.append(row)
        continue

    model = YOLO(str(weights))
    preds_all = []
    for i in range(0, len(paths), BATCH):
        out: Any = model.predict(paths[i:i + BATCH], imgsz=IMGSZ, conf=CONF,  # type: ignore[no-untyped-call]
                                iou=IOU_NMS, device=0, verbose=False)
        for r in out:
            bx = r.boxes  # type: ignore[attr-defined]
            if bx is not None and len(bx):
                xy = bx.xyxy.cpu().numpy().reshape(-1, 4)  # type: ignore[attr-defined]
                cl = bx.cls.cpu().numpy()[:, None]  # type: ignore[attr-defined]
                cf = bx.conf.cpu().numpy()[:, None]  # type: ignore[attr-defined]
                preds_all.append(np.concatenate([xy, cl, cf], axis=1))
            else:
                preds_all.append(np.zeros((0, 6)))
    assert len(preds_all) == len(items)
    del model
    torch.cuda.empty_cache()

    proxy = dict.fromkeys(DISTR, 0)
    proxy_union = 0  # pred Pothole dihitung 1x per gambar (definisi notebook 04_*)
    true = dict.fromkeys(DISTR, 0)
    true_any = 0
    det = dict.fromkeys(DISTR, 0)
    for (_, _, gt), pr in zip(items, preds_all, strict=True):
        pot = pr[pr[:, 4] == POTHOLE][:, :4]
        proxy_union += len(pot)
        # proxy: semua pred Pothole di gambar berpengecoh kelas c
        for c in DISTR:
            if len(gt[c]):
                proxy[c] += len(pot)
        # true: IoU >= 0.5 vs GT kelas c
        hit_any = np.zeros(len(pot), dtype=bool)
        for c in DISTR:
            if len(pot) and len(gt[c]):
                hit = iou_matrix(pot, gt[c]).max(axis=1) >= IOU_MATCH
                true[c] += int(hit.sum())
                hit_any |= hit
            # det rate (6cls): pred kelas c vs GT kelas c
            if nc == 6 and len(gt[c]):
                d = pr[pr[:, 4] == c][:, :4]
                if len(d):
                    det[c] += int((iou_matrix(d, gt[c]).max(axis=1) >= IOU_MATCH).sum())
        true_any += int(hit_any.sum())

    def rate(n, d):
        return round(n / d, 4) if d else float("nan")

    row.update({
        "proxy_manhole": rate(proxy[4], n_gt[4]),
        "proxy_patchy": rate(proxy[5], n_gt[5]),
        "proxy_total": rate(proxy_union, n_gt_total),
        "true_manhole": rate(true[4], n_gt[4]),
        "true_patchy": rate(true[5], n_gt[5]),
        "true_total": rate(true_any, n_gt_total),
        "n_proxy": proxy[4] + proxy[5], "n_true": true_any,
        "det_manhole": rate(det[4], n_gt[4]) if nc == 6 else float("nan"),
        "det_patchy": rate(det[5], n_gt[5]) if nc == 6 else float("nan"),
    })
    rows.append(row)
    print(f"[+] {label}: proxy={row['proxy_total']} true={row['true_total']} "
          f"(M {row['true_manhole']} / P {row['true_patchy']})")

df = pd.DataFrame(rows)
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_CSV, index=False)
print(f"\nCSV: {OUT_CSV}")

# ── 3. Tabel markdown gabungan (computed + referensi proxy) ──────────────────
print("\n===== TABEL FP/GT POTHOLE — TEST (conf=0.25, IoU match 0.5) =====\n")
hdr = ("| Model | nc | proxy M | proxy P | proxy Gab | TRUE M | TRUE P | TRUE Gab |"
       " det M | det P |")
print(hdr)
print("|---|---|---|---|---|---|---|---|---|---|")
for _, r in df.iterrows():
    if bool(r["weights_found"]):
        print(f"| {r['model']} | {r['nc']} | {r['proxy_manhole']} | {r['proxy_patchy']} "
              f"| {r['proxy_total']} | {r['true_manhole']} | {r['true_patchy']} "
              f"| {r['true_total']} | {r['det_manhole']} | {r['det_patchy']} |")
    else:
        pm, pp, pt = PROXY_REF.get(str(r["model"]), (float("nan"),) * 3)
        print(f"| {r['model']} † | {r['nc']} | {pm} | {pp} | {pt} "
              f"| — | — | — | — | — |")
if not bool(df["weights_found"].all()):
    print("\n† bobot final tidak ada di repo; angka proxy dari run 2025-08-07 "
          "(confusion_6cls_vs_4cls.csv), TRUE overlap tidak bisa dihitung ulang.")
print("M=manhole(321 GT), P=patchy_road(69 GT), Gab=390 GT; TRUE = IoU>=0.5.")
