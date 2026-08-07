"""
confusion_6cls_vs_4cls.py
=========================
Analisis false positive Pothole pada gambar test yang berisi kelas pengecoh
(manhole & patchy_road), untuk membandingkan model 6-kelas vs model 4-kelas
(ablasi negative anchor).

Latar belakang:
- Model 6-kelas dilatih dengan kelas manhole & patchy_road tetap ada.
- Model 4-kelas menghapus kedua kelas tersebut (negative anchor dihilangkan).
- Script ini mengecek apakah ablasi 4-kelas benar-benar menekan prediksi
  Pothole yang salah pada objek pengecoh.

Metrik per kelas pengecoh (metode subset gambar, konsisten dengan notebook):
- n_gt_<class>             : jumlah objek GT kelas tersebut pada subset gambarnya
- n_pred_pothole_<class>   : jumlah prediksi Pothole (ID 3) pada subset gambar itu
- fp_pothole_rate_<class>  : n_pred_pothole_<class> / n_gt_<class>
- det_rate_<class>         : (khusus 6-kelas) prediksi kelas manhole/patchy dibagi
                             GT kelas tersebut — seberapa baik model menyerap objek
                             pengecoh ke kelas yang benar.

Gambar yang memuat manhole DAN patchy_road dihitung pada kedua subset.

Hasil disimpan ke:
    runs/rdd_yolov8n_local/confusion_6cls_vs_4cls_<splits>.csv
    (nama file mengikuti SPLITS yang dipakai, mis. ..._test.csv atau ..._val_test.csv)

Jalankan:
    python code/confusion_6cls_vs_4cls.py
"""

import gc
from pathlib import Path

import pandas as pd
import torch
from ultralytics import YOLO

# ── Config ───────────────────────────────────────────────────────────────────
ROOT_CANDIDATES = [
    Path.cwd().resolve(),
    Path.cwd().resolve().parent,
    Path("D:/01_Akademik/TA-Project"),
]
REPO_ROOT = next(
    (p for p in ROOT_CANDIDATES if (p / "data").exists()),
    Path.cwd().resolve(),
)

# Dataset 6-kelas asli (sumber label GT manhole & patchy_road)
SRC_DATASET_DIR = (
    REPO_ROOT
    / "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes"
    / "RDD_Split_Final_china_japan_india_6_classes"
)
# Dataset 4-kelas — gambar hardlink ke asli, label manhole/patchy sudah difilter
DATASET_DIR = REPO_ROOT / "data/NRDD-2024/RDD_4class"

# ID kelas pengecoh di dataset original (6-kelas) dan Pothole di model
CONFUSION_CLASSES = {4: "manhole", 5: "patchy_road"}
POTHOLE_ID = 3

IMGSZ = 640
PRED_CONF = 0.25
PRED_IOU = 0.60
BATCH_SIZE_ANALYSIS = 8

# Split yang dipakai untuk analisis:
#   ["test"]        → primary (held-out), sesuai laporan utama.
#   ["val", "test"] → diagnostik tambahan (lebih banyak data).
#                     Catatan penelitian: best.pt dipilih berdasarkan val
#                     (early stopping), sehingga angka pada val sedikit
#                     optimistik — jangan dipakai sebagai metrik utama.
SPLITS = ["val", "test"]

# Model yang dibandingkan: (label, path best.pt, jumlah kelas)
MODELS = [
    ("yolov8n_6cls_class_weight",
     REPO_ROOT / "runs/rdd_yolov8n_local/experiments/yolov8n_class_weight/weights/best.pt", 6),
    ("yolov12n_6cls_class_weight",
     REPO_ROOT / "runs/rdd_yolov8n_local/experiments/yolov12n_class_weight/weights/best.pt", 6),
    ("yolov26n_6cls_class_weight",
     REPO_ROOT / "runs/rdd_yolov8n_local/experiments/yolov26n_class_weight/weights/best.pt", 6),
    ("yolov8n_4cls_class_weights",
     REPO_ROOT / "runs/rdd_4class_local/experiments/yolov8n_4cls_class_weights/weights/best.pt", 4),
    ("yolov12n_4cls_class_weights",
     REPO_ROOT / "runs/rdd_4class_local/experiments/yolov12n_4cls_class_weights/weights/best.pt", 4),
    ("yolov26n_4cls_class_weights",
     REPO_ROOT / "runs/rdd_4class_local/experiments/yolov26n_4cls_class_weights/weights/best.pt", 4),
]

OUT_CSV = REPO_ROOT / f"runs/rdd_yolov8n_local/confusion_6cls_vs_4cls_{'_'.join(SPLITS)}.csv"


def collect_confusion_images():
    """Bangun subset gambar per kelas pengecoh + hitung GT objek per kelas.

    Iterasi atas setiap split di SPLITS (label GT diambil dari dataset 6-kelas
    asli, gambar dari dataset 4-kelas yang isinya hardlink ke gambar asli).
    """
    confusion_images_by_class = {cid: [] for cid in CONFUSION_CLASSES}
    n_gt_by_class = {cid: 0 for cid in CONFUSION_CLASSES}
    confusion_images = []

    for split in SPLITS:
        src_label_dir = SRC_DATASET_DIR / split / "labels"
        dst_img_dir = DATASET_DIR / split / "images"

        for lp in sorted(src_label_dir.glob("*.txt")):
            if lp.name.lower() == "classes.txt":
                continue
            lines = lp.read_text(encoding="utf-8", errors="ignore").splitlines()
            classes_in_img = set()
            gt_counts = {cid: 0 for cid in CONFUSION_CLASSES}
            for parts in (ln.strip().split() for ln in lines if ln.strip()):
                if not parts:
                    continue
                cid = int(parts[0])
                if cid in CONFUSION_CLASSES:
                    classes_in_img.add(cid)
                    gt_counts[cid] += 1
            if not classes_in_img:
                continue
            img_path = None
            for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
                cand = dst_img_dir / (lp.stem + ext)
                if cand.exists():
                    img_path = cand
                    break
            if img_path is None:
                continue
            for cid in classes_in_img:
                confusion_images_by_class[cid].append(img_path)
                n_gt_by_class[cid] += gt_counts[cid]
            confusion_images.append(img_path)

    confusion_images = list(dict.fromkeys(confusion_images))
    for cid in CONFUSION_CLASSES:
        confusion_images_by_class[cid] = list(dict.fromkeys(confusion_images_by_class[cid]))

    return confusion_images, confusion_images_by_class, n_gt_by_class


def predict_pothole_counts(best_model, confusion_images):
    """Predict per batch, kembalikan dict {stem: {"pothole": n, "manhole": n, "patchy": n}}.

    Catatan: r.path tidak bisa dipakai (ultralytics menamai ulang jadi image0..N),
    jadi hasil dipasangkan ke gambar input berdasarkan urutan (zip).
    """
    all_preds = []
    for i in range(0, len(confusion_images), BATCH_SIZE_ANALYSIS):
        batch = [str(p) for p in confusion_images[i:i + BATCH_SIZE_ANALYSIS]]
        batch_preds = best_model.predict(
            source=batch,
            imgsz=IMGSZ,
            conf=PRED_CONF,
            iou=PRED_IOU,
            device=ANALYSIS_DEVICE,
            verbose=False,
        )
        all_preds.extend(batch_preds)

    assert len(all_preds) == len(confusion_images), (
        f"hasil prediksi {len(all_preds)} != gambar input {len(confusion_images)}"
    )

    per_stem = {}
    for r, img_path in zip(all_preds, confusion_images):
        per_stem[img_path.stem] = {"pothole": 0, "manhole": 0, "patchy": 0}
        if r.boxes is None:
            continue
        cls = r.boxes.cls.long()
        per_stem[img_path.stem]["pothole"] = int((cls == POTHOLE_ID).sum())
        per_stem[img_path.stem]["manhole"] = int((cls == 4).sum())
        per_stem[img_path.stem]["patchy"] = int((cls == 5).sum())
    return per_stem


def rate(n_pred: int, n_gt: int) -> float:
    return round(n_pred / n_gt, 4) if n_gt > 0 else float("nan")


# ── Jalankan analisis ────────────────────────────────────────────────────────
confusion_images, confusion_images_by_class, n_gt_by_class = collect_confusion_images()

for cid, name in CONFUSION_CLASSES.items():
    print(f"Gambar dengan GT {name:<12s}: {len(confusion_images_by_class[cid])}  |  GT objek: {n_gt_by_class[cid]}")
print(f"Gambar gabungan (union)  : {len(confusion_images)}  |  GT objek: {sum(n_gt_by_class.values())}")

free_vram_gb = torch.cuda.mem_get_info()[0] / 1024**3 if torch.cuda.is_available() else 0
ANALYSIS_DEVICE = 0 if free_vram_gb > 2.0 else "cpu"
print(f"VRAM bebas: {free_vram_gb:.2f} GB → device: {ANALYSIS_DEVICE}\n")

rows = []
for model_label, weights, nc in MODELS:
    assert weights.exists(), f"weights tidak ditemukan: {weights}"
    best_model = YOLO(str(weights))

    per_stem = predict_pothole_counts(best_model, confusion_images)

    def agg(subset_stems, cid):
        n_pred = sum(per_stem[s]["pothole"] for s in subset_stems)
        return n_pred, rate(n_pred, n_gt_by_class[cid])

    row = {"model": model_label, "nc": nc}
    n_pred_manhole, row["fp_rate_manhole"] = agg(
        [p.stem for p in confusion_images_by_class[4]], 4)
    n_pred_patchy, row["fp_rate_patchy"] = agg(
        [p.stem for p in confusion_images_by_class[5]], 5)

    n_gt_total = sum(n_gt_by_class.values())
    n_pred_total = sum(per_stem[p.stem]["pothole"] for p in confusion_images)
    row["fp_rate_total"] = rate(n_pred_total, n_gt_total)

    if nc == 6:
        n_det_manhole = sum(per_stem[p.stem]["manhole"] for p in confusion_images_by_class[4])
        n_det_patchy = sum(per_stem[p.stem]["patchy"] for p in confusion_images_by_class[5])
        row["det_rate_manhole"] = rate(n_det_manhole, n_gt_by_class[4])
        row["det_rate_patchy"] = rate(n_det_patchy, n_gt_by_class[5])
    else:
        row["det_rate_manhole"] = float("nan")
        row["det_rate_patchy"] = float("nan")

    rows.append(row)

    print(f"{'-'*52}")
    print(f"Model: {model_label}  ({nc}-kelas)")
    print(f"  {CONFUSION_CLASSES[4]:<12s}: Pothole FP={n_pred_manhole}, GT={n_gt_by_class[4]}, rate={row['fp_rate_manhole']}")
    print(f"  {CONFUSION_CLASSES[5]:<12s}: Pothole FP={n_pred_patchy}, GT={n_gt_by_class[5]}, rate={row['fp_rate_patchy']}")
    print(f"  Gabungan    : Pothole FP={n_pred_total}, GT={n_gt_total}, rate={row['fp_rate_total']}")
    if nc == 6:
        print(f"  Deteksi {CONFUSION_CLASSES[4]:<12s}: {n_det_manhole} / {n_gt_by_class[4]} ({row['det_rate_manhole']})")
        print(f"  Deteksi {CONFUSION_CLASSES[5]:<12s}: {n_det_patchy} / {n_gt_by_class[5]} ({row['det_rate_patchy']})")

    del best_model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

df = pd.DataFrame(rows)
print("\n===== RINGKASAN =====")
print(df[["model", "nc", "fp_rate_manhole", "fp_rate_patchy", "fp_rate_total",
          "det_rate_manhole", "det_rate_patchy"]].to_string(index=False))

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_CSV, index=False)
print(f"\nDisimpan ke {OUT_CSV}")
