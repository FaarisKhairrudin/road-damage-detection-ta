"""Sweep conf & IoU-match untuk tabel FP/GT Pothole vs pengecoh (manhole, patchy_road).

Satu kali inferensi di conf sangat rendah (0,001), lalu tabel dihitung ulang
untuk banyak threshold dari data mentah yang sama.

Definisi TRUE overlap (FP beneran): prediksi Pothole dengan IoU >= IOU_MATCH
terhadap >=1 box GT pengecoh. Penyebut tetap jumlah GT pengecoh:
manhole 321, patchy_road 69, gabungan 390.

Sweep:
  conf      : 0,001 / 0,010 / 0,050 / 0,100 / 0,250 / 0,500
  IoU match : 0,3 / 0,5 / 0,7

Model: 5 arsitektur 6-kelas. Split TEST, iou(NMS)=0.60, imgsz=640.

Output:
  runs/rdd_yolov8n_local/fp_overlap_conf_sweep_raw.csv   (prediksi mentah)
  docs/analisis-threshold-fp-overlap.md                  (tabel markdown)

Usage:
  python3.12 scripts/fp_overlap_threshold_sweep.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2  # type: ignore[import-unresolved, import-not-found]
import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import torch  # type: ignore[import-unresolved, import-not-found]

REPO = Path("/mnt/Data/01_Akademik/TA-Project")

CUSTOM_DIR = REPO / "code/models"
if str(CUSTOM_DIR) not in sys.path:
    sys.path.insert(0, str(CUSTOM_DIR))
from custom_modules import patch_ultralytics  # type: ignore[import-unresolved, import-not-found]

patch_ultralytics()
from ultralytics import YOLO  # type: ignore[import-unresolved, import-not-found]

SRC = (
    REPO
    / "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes"
    / "RDD_Split_Final_china_japan_india_6_classes"
    / "test"
)
IMGDIR, LBDIR = SRC / "images", SRC / "labels"

OUT_RAW = REPO / "runs/rdd_yolov8n_local/fp_overlap_conf_sweep_raw.csv"
OUT_MD = REPO / "docs/analisis-threshold-fp-overlap.md"

CONF_MIN, IOU_NMS, IMGSZ = 0.001, 0.60, 640
POTHOLE = 3
DISTR = {4: "manhole", 5: "patchy_road"}
N_GT = {4: 321, 5: 69}
N_GT_TOTAL = 390
BATCH = 8

CONF_SWEEP = [0.001, 0.010, 0.050, 0.100, 0.250, 0.500]
IOU_SWEEP = [0.3, 0.5, 0.7]

E6 = REPO / "runs/rdd_yolov8n_local/experiments"
MODELS = [
    ("yolov8n_6cls", E6 / "yolov8n_class_weight/weights/best.pt"),
    ("yolov12n_6cls", E6 / "yolov12n_class_weight/weights/best.pt"),
    ("yolov26n_6cls", E6 / "yolov26n_class_weight/weights/best.pt"),
    ("yolov8_pd_6cls", E6 / "yolov8_pd_class_weight/weights/best.pt"),
    ("yolo_rd_6cls", E6 / "yolo_rd_class_weight/weights/best.pt"),
]


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


# ── 1. Kumpulkan citra test berpengecoh + GT ────────────────────────────────
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
    per_cls: dict[int, list] = {c: [] for c in DISTR}
    for ln in lp.read_text(errors="ignore").splitlines():
        p = ln.strip().split()
        if p and int(p[0]) in DISTR:
            cid, box = xywhn_to_xyxy(p, w, h)
            per_cls[cid].append(box)
    if any(per_cls.values()):
        items.append((lp.stem, img_path,
                      {c: np.array(v) if v else np.zeros((0, 4))
                       for c, v in per_cls.items()}))

print(f"Citra test berpengecoh: {len(items)}")

paths = [str(p) for _, p, _ in items]

# ── 2. Inferensi sekali di conf minimal, simpan tiap prediksi Pothole ───────
records = []
for label, weights in MODELS:
    if not weights.exists():
        print(f"[-] {label}: bobot tidak ada, lewati")
        continue
    model = YOLO(str(weights))
    preds_all = []
    for i in range(0, len(paths), BATCH):
        out = model.predict(paths[i:i + BATCH], imgsz=IMGSZ, conf=CONF_MIN,
                            iou=IOU_NMS, device=0, verbose=False)
        for r in out:
            bx = r.boxes
            if bx is not None and len(bx):
                xy = bx.xyxy.cpu().numpy().reshape(-1, 4)
                cl = bx.cls.cpu().numpy()
                cf = bx.conf.cpu().numpy()
                preds_all.append((xy, cl, cf))
            else:
                preds_all.append((np.zeros((0, 4)), np.zeros(0), np.zeros(0)))
    del model
    torch.cuda.empty_cache()

    n_pot_total = 0
    for (stem, _, gt), (xy, cl, cf) in zip(items, preds_all, strict=True):
        keep = cl == POTHOLE
        pot = xy[keep]
        pconf = cf[keep]
        n_pot_total += len(pot)
        if not len(pot):
            continue
        iou_m = iou_matrix(pot, gt[4]).max(axis=1) if len(gt[4]) else np.zeros(len(pot))
        iou_p = iou_matrix(pot, gt[5]).max(axis=1) if len(gt[5]) else np.zeros(len(pot))
        iou_any = np.maximum(iou_m, iou_p)
        for c, im, ip, ia in zip(pconf, iou_m, iou_p, iou_any, strict=True):
            records.append((label, stem, float(c), float(im), float(ip), float(ia)))
    print(f"[+] {label}: prediksi Pothole (conf>=0,001) = {n_pot_total}")

raw = pd.DataFrame(records, columns=["model", "stem", "conf",
                                     "iou_manhole", "iou_patchy", "iou_any"])
OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
raw.to_csv(OUT_RAW, index=False)
print(f"\nRAW: {OUT_RAW}  ({len(raw)} baris prediksi Pothole)")

# ── 3. Sweep conf x IoU-match ───────────────────────────────────────────────
MODEL_ORDER = [m for m, _ in MODELS if (raw["model"] == m).any()]


def count_table(col: str, denom: int) -> pd.DataFrame:
    """Tabel: baris=conf, kolom=model, isi=jumlah pred Pothole IoU>=t (per t)."""
    out = {}
    for iou_t in IOU_SWEEP:
        sub = raw[raw[col] >= iou_t]
        tab = []
        for conf_t in CONF_SWEEP:
            row = {}
            for m in MODEL_ORDER:
                row[m] = int(((sub["model"] == m) & (sub["conf"] >= conf_t)).sum())
            tab.append({"conf": conf_t, **row})
        out[iou_t] = pd.DataFrame(tab)
    return out


tab_total = count_table("iou_any", N_GT_TOTAL)
tab_manh = count_table("iou_manhole", N_GT[4])
tab_patchy = count_table("iou_patchy", N_GT[5])

# ── 4. Tulis markdown ───────────────────────────────────────────────────────
lines: list[str] = []
lines.append("# Analisis Threshold Tabel FP/GT Pothole vs Pengecoh")
lines.append("")
lines.append("Tanggal: 2026-10-09")
lines.append("")
lines.append("Catatan: dokumen ini hanya catatan eksplorasi. Tabel dan angka di draf "
             "belum diubah.")
lines.append("")
lines.append("## Latar Belakang")
lines.append("")
lines.append("Tabel FP/GT pothole yang dipakai di draf memakai conf=0,25 dan IoU match 0,5. "
             "Pertanyaannya apakah angka berubah bila threshold diturunkan atau dinaikkan.")
lines.append("")
lines.append(f"Metode: satu kali inferensi pada conf=0,001 (iou NMS 0,60, imgsz 640) "
             f"untuk {len(MODEL_ORDER)} model 6-kelas pada {len(items)} citra test "
             f"berpengecoh. Semua prediksi Pothole disimpan bersama IoU maksimumnya "
             f"terhadap GT manhole dan patchy_road, lalu tabel dihitung ulang untuk "
             f"tiap kombinasi threshold.")
lines.append("")
lines.append("Penyebut tetap jumlah GT pengecoh: manhole 321, patchy_road 69, "
             "gabungan 390. Nilai di tabel adalah jumlah prediksi Pothole yang "
             "menimpa pengecoh (bukan rate).")
lines.append("")
lines.append(f"Jumlah prediksi Pothole mentah (conf>=0,001) per model:")
lines.append("")
lines.append("| Model | Prediksi Pothole |")
lines.append("|---|---|")
for m in MODEL_ORDER:
    lines.append(f"| {m} | {int((raw['model'] == m).sum())} |")
lines.append("")


def emit_section(title: str, tables: dict, denom: int) -> None:
    lines.append(f"## {title} (penyebut {denom})")
    lines.append("")
    for iou_t in IOU_SWEEP:
        lines.append(f"### IoU match >= {str(iou_t).replace('.', ',')}")
        lines.append("")
        df = tables[iou_t]
        cols = ["conf", *MODEL_ORDER]
        lines.append("| conf | " + " | ".join(MODEL_ORDER) + " |")
        lines.append("|---|" + "---|" * len(MODEL_ORDER))
        for _, r in df.iterrows():
            vals = " | ".join(str(int(r[m])) for m in MODEL_ORDER)
            lines.append(f"| {str(r['conf']).replace('.', ',')} | {vals} |")
        lines.append("")


emit_section("Gabungan (manhole + patchy)", tab_total, N_GT_TOTAL)
emit_section("Manhole", tab_manh, N_GT[4])
emit_section("Patchy road", tab_patchy, N_GT[5])

lines.append("## Cara Baca")
lines.append("")
lines.append("Baris conf adalah ambang keyakinan minimum yang dipertahankan. "
             "Kolom adalah model. Nilai adalah jumlah prediksi pothole yang "
             "menumpuk pada pengecoh pada IoU match yang tercantum.")
lines.append("")
lines.append("Makin kecil conf makin banyak prediksi yang ikut dihitung sehingga "
             "jumlah tumpang tindih hampir pasti naik. Makin besar IoU match makin "
             "ketat definisi tumpang tindih sehingga jumlahnya turun.")
lines.append("")

OUT_MD.write_text("\n".join(lines), encoding="utf-8")
print(f"MD : {OUT_MD}")

# ringkas ke stdout
print("\n===== RINGKAS: gabungan (dari 390 GT) =====")
for iou_t in IOU_SWEEP:
    print(f"\nIoU match >= {iou_t}")
    print("  conf  | " + " | ".join(f"{m:>14}" for m in MODEL_ORDER))
    for _, r in tab_total[iou_t].iterrows():
        print(f"  {r['conf']:.3f} | " +
              " | ".join(f"{int(r[m]):>14}" for m in MODEL_ORDER))
