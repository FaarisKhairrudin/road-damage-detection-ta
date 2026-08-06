"""
prepare_4class_dataset.py
=========================
Membuat dataset 4-kelas dari dataset 6-kelas yang sudah ada.

Yang dilakukan:
- Label : copy + filter, hapus baris dengan class ID >= 4 (manhole & patchy_road)
- Gambar : symlink ke folder asli di Linux/Mac; copy di Windows
           (Windows memerlukan Developer Mode untuk symlink — fallback ke copy otomatis)

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

IS_WINDOWS = platform.system() == "Windows"


def make_image_link(src_img_dir: Path, dst_img_dir: Path) -> str:
    """
    Buat symlink (Linux/Mac) atau copy folder gambar (Windows fallback).
    Mengembalikan string keterangan metode yang dipakai.
    """
    # Hapus target lama jika ada
    if dst_img_dir.is_symlink():
        dst_img_dir.unlink()
    elif dst_img_dir.exists():
        if not any(dst_img_dir.iterdir()):
            dst_img_dir.rmdir()
        else:
            return "already exists (skipped)"

    if IS_WINDOWS:
        # Coba symlink dulu (perlu Developer Mode); fallback ke copy
        try:
            dst_img_dir.symlink_to(src_img_dir.resolve())
            return "symlink (Windows Developer Mode)"
        except (OSError, NotImplementedError):
            print(f"  [!] Symlink gagal di Windows — copy gambar (ini bisa memakan waktu)...")
            shutil.copytree(str(src_img_dir), str(dst_img_dir))
            return "copy (Windows fallback)"
    else:
        dst_img_dir.symlink_to(src_img_dir.resolve())
        return "symlink"


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
        img_method = make_image_link(src_img_dir, dst_img_dir)

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
