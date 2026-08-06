"""
prepare_4class_dataset.py
=========================
Membuat dataset 4-kelas dari dataset 6-kelas yang sudah ada.

Yang dilakukan:
- Label : copy + filter, hapus baris dengan class ID >= 4 (manhole & patchy_road)
- Gambar : hard link per-file (tidak copy, hemat disk, path tidak di-resolve YOLO)
           Fallback: symlink per-file → copy jika beda filesystem atau Windows tanpa dev mode

Jalankan sekali sebelum notebook 04_modelling_4class.ipynb:
    python code/prepare_4class_dataset.py

Tidak ada yang diubah pada dataset asli.
"""

import os
import platform
import shutil
import yaml
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────
ROOT_CANDIDATES = [
    Path.cwd().resolve(),
    Path.cwd().resolve().parent,
    Path("D:/01_Akademik/TA-Project"),
    Path("C:/01_Akademik/TA-Project"),
]
REPO_ROOT = next(
    (p for p in ROOT_CANDIDATES if (p / "data").exists()),
    Path.cwd().resolve(),
)

SRC_DIR = (
    REPO_ROOT
    / "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes"
    / "RDD_Split_Final_china_japan_india_6_classes"
)
DST_DIR = REPO_ROOT / "data/NRDD-2024/RDD_4class"

CLASS_NAMES_4 = [
    "Longitudinal_Crack",
    "Transverse_Crack",
    "Alligator_Crack",
    "Pothole",
]
MAX_VALID_ID = len(CLASS_NAMES_4) - 1  # 3

SPLITS = ["train", "val", "test"]
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

IS_WINDOWS = platform.system() == "Windows"


def make_image_links(src_img_dir: Path, dst_img_dir: Path) -> str:
    """
    Buat hard link per-file gambar (bukan symlink folder).

    Mengapa per-file, bukan symlink folder?
    YOLO me-resolve symlink folder ke path asli saat scan, lalu mencari label
    di path asli juga — menyebabkan label yang belum difilter terbaca.
    Hard link per-file tidak punya masalah ini karena path-nya tetap
    terbaca sebagai RDD_4class/.../images/filename.jpg.

    Fallback priority:
      1. os.link (hardlink)  — cross-platform, filesystem sama, tidak di-resolve
      2. symlink per-file    — fallback jika beda filesystem
      3. shutil.copy2        — fallback terakhir (Windows tanpa dev mode / NFS)
    """
    dst_img_dir.mkdir(parents=True, exist_ok=True)

    images = [p for p in src_img_dir.iterdir() if p.suffix.lower() in IMG_EXTS]

    # Jika sudah ada dan jumlah file sama → skip
    dst_count = sum(1 for p in dst_img_dir.iterdir() if p.suffix.lower() in IMG_EXTS)
    if dst_count == len(images):
        return f"already exists ({dst_count} files, skipped)"

    # Bersihkan isi lama jika ada
    for f in dst_img_dir.iterdir():
        f.unlink()

    method = None
    for src_file in images:
        dst_file = dst_img_dir / src_file.name
        if dst_file.exists() or dst_file.is_symlink():
            dst_file.unlink()

        if method in (None, "hardlink"):
            try:
                os.link(src_file, dst_file)
                method = "hardlink"
                continue
            except OSError:
                method = "symlink"

        if method == "symlink":
            try:
                dst_file.symlink_to(src_file.resolve())
                continue
            except (OSError, NotImplementedError):
                method = "copy"

        shutil.copy2(str(src_file), str(dst_file))
        method = "copy"

    return f"{method} per-file ({len(images)} gambar)"


def filter_labels(src_label_dir: Path, dst_label_dir: Path):
    """Filter label files: hapus baris dengan class ID > MAX_VALID_ID."""
    dst_label_dir.mkdir(parents=True, exist_ok=True)
    label_files = sorted(
        [p for p in src_label_dir.glob("*.txt") if p.name.lower() != "classes.txt"]
    )

    n_kept = 0
    n_removed = 0
    n_empty = 0

    for src_lp in label_files:
        lines = src_lp.read_text(encoding="utf-8", errors="ignore").splitlines()
        kept = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            try:
                cid = int(parts[0])
            except ValueError:
                kept.append(line)
                continue
            if cid <= MAX_VALID_ID:
                kept.append(line)
                n_kept += 1
            else:
                n_removed += 1

        dst_lp = dst_label_dir / src_lp.name
        dst_lp.write_text(
            "\n".join(kept) + ("\n" if kept else ""), encoding="utf-8"
        )
        if not kept:
            n_empty += 1

    return n_kept, n_removed, n_empty, len(label_files)


def main():
    print(f"Repo root  : {REPO_ROOT}")
    print(f"Source     : {SRC_DIR}")
    print(f"Dest       : {DST_DIR}")
    print(f"Platform   : {platform.system()}")
    print()

    assert SRC_DIR.exists(), (
        f"\nDataset sumber tidak ditemukan:\n  {SRC_DIR}\n"
        "Pastikan dataset sudah di-download dan path sudah benar."
    )

    DST_DIR.mkdir(parents=True, exist_ok=True)

    total_removed = 0
    for split in SPLITS:
        src_img_dir   = SRC_DIR   / split / "images"
        src_label_dir = SRC_DIR   / split / "labels"
        dst_img_dir   = DST_DIR   / split / "images"
        dst_label_dir = DST_DIR   / split / "labels"

        dst_img_dir.parent.mkdir(parents=True, exist_ok=True)

        # Gambar
        img_method = make_image_links(src_img_dir, dst_img_dir)

        # Label
        kept, removed, empty, n_files = filter_labels(src_label_dir, dst_label_dir)
        total_removed += removed

        print(
            f"[{split:5s}] images: {img_method} | "
            f"{n_files} label files | "
            f"kept {kept} | removed {removed} (ID>=4) | "
            f"{empty} background files"
        )

    # data.yaml
    yaml_cfg = {
        "path":  str(DST_DIR.resolve()).replace("\\", "/"),
        "train": "train/images",
        "val":   "val/images",
        "test":  "test/images",
        "nc":    len(CLASS_NAMES_4),
        "names": CLASS_NAMES_4,
    }
    dst_yaml = DST_DIR / "data.yaml"
    with dst_yaml.open("w", encoding="utf-8") as f:
        yaml.safe_dump(yaml_cfg, f, sort_keys=False, allow_unicode=False)

    print(f"\ndata.yaml tersimpan : {dst_yaml}")
    print(f"Total box dihapus   : {total_removed}")
    print("\nDataset 4-kelas siap. Notebook 04_modelling_4class.ipynb bisa dijalankan.")


if __name__ == "__main__":
    main()
