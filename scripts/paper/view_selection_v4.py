#!/usr/bin/env python3
"""Contact sheet seleksi gambar V4 (3 grup) — bantu user memilih citra final.

Windows GUI tidak bisa dibuka dari environment ini, jadi figur matplotlib
di-render ke PNG dan ditampilkan di chat. Untuk window interaktif lokal,
jalankan dengan --show di mesin yang ada display-nya:
  python3 scripts/paper/view_selection_v4.py --show

Tanpa flag: simpan 3 PNG ke /tmp/select_v4/.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IMGDIR = REPO / "data/RDD-indo-v4/valid/images"
OUTDIR = Path("/tmp/select_v4")

GROUPS: dict[str, list[str]] = {
    "G1_pantulan_cahaya": [
        "VID_20260520_092711_mp4-0036_jpg.rf.7a7e5b3526ce4960b882afbb9d2553f6.jpg",
        "VID_20260520_092711_mp4-0023_jpg.rf.5c5e2a77af3dc09a74953358c19b2f4c.jpg",
        "VID_20260520_092711_mp4-0004_jpg.rf.d7238bec30ec2cc79e9cc58d04fa4d0b.jpg",
        "VID_20260520_092711_mp4-0007_jpg.rf.2e583f4356da1dd6d244c49bdbdb90df.jpg",
        "VID_20260520_092711_mp4-0008_jpg.rf.98ec29919ec3aab88d4eb7c1a38ad959.jpg",
        "VID_20260520_092711_mp4-0010_jpg.rf.7c003778665332f21afa453ad0c165f8.jpg",
        "VID_20260520_092711_mp4-0058_jpg.rf.bea523a7a34b396969808b82fe3f4fcf.jpg",
        "VID_20260520_092711_mp4-0009_jpg.rf.846b13e85ae58f71de958677b575d1b6.jpg",
        # hash lama bd83... tidak ada di dataset baru -> ganti hash baru, stem sama
        "VID_20260520_092711_mp4-0015_jpg.rf.5662d053e1bd0b02b59ee8e06cc761b8.jpg",
        "VID_20260520_092711_mp4-0035_jpg.rf.9088971cda70b1603b7b3401724b8026.jpg",
        "VID_20260520_092711_mp4-0041_jpg.rf.fc496120f0a27907702260474d3e6114.jpg",
    ],
    "G2_benar_prediksi_dengan_gt": [
        "VID_20260520_092711_mp4-0018_jpg.rf.eca099ddfec331f1b7e2dd90cdf8f883.jpg",
        "Merge-1_mp4-0436_jpg.rf.42bc2b4480c6cf4ab83870300ac06ca6.jpg",
        "Merge-1_mp4-0441_jpg.rf.f4eed802f07e91d3125e2abb5009fadd.jpg",
        "Merge-1_mp4-0713_jpg.rf.1f7f41a50ec57a14b7069ff77677d9cb.jpg",
        "Merge-1_mp4-0727_jpg.rf.e75e41563597aca0ab4ec7ddc5d30523.jpg",
    ],
    "G3_benar_prediksi_tanpa_gt": [
        "Merge-1_mp4-0703_jpg.rf.ed4f025f83e959dfd6c787300629a889.jpg",
        "Merge-1_mp4-0706_jpg.rf.a8507c635d208c82126f924c46205fd4.jpg",
        "Merge-1_mp4-0708_jpg.rf.adfd6a67b6b779b4a2548674d71cd0d9.jpg",
        "Merge-1_mp4-0716_jpg.rf.d3cfb99d6a6c7182ba5d02603b9a9b27.jpg",
        "Merge-1_mp4-0734_jpg.rf.8ad7ae9ed88206af6e63d5c305f13820.jpg",
        "Merge-1_mp4-0765_jpg.rf.ad5eab77613776d7bf7d32fab0cf0c76.jpg",
        # hash lama e099... tidak ada di dataset baru -> ganti hash baru, stem sama
        "Merge-1_mp4-0767_jpg.rf.a99f57798536721f3dadc8a8a9855e05.jpg",
        "Merge-1_mp4-0768_jpg.rf.4b505bd448e403095eefc00368974cf8.jpg",
    ],
}


def short_name(fname: str) -> str:
    m = re.search(r"(mp4-\d+)", fname)
    return m.group(1) if m else fname[:20]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true", help="tampilkan window interaktif (mesin lokal ber-display)")
    ap.add_argument("--ncols", type=int, default=4)
    args = ap.parse_args()

    import matplotlib

    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for gname, files in GROUPS.items():
        missing = [f for f in files if not (IMGDIR / f).exists()]
        if missing:
            print(f"[{gname}] MISSING: {missing}")
            files = [f for f in files if (IMGDIR / f).exists()]
        n = len(files)
        ncols = min(args.ncols, n)
        nrows = (n + ncols - 1) // ncols
        fig, _axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 3.0 * nrows))
        flat = list(fig.get_axes())
        for ax in flat:
            ax.axis("off")
        for idx, (fname, ax) in enumerate(zip(files, flat, strict=False), start=1):
            ax.imshow(Image.open(IMGDIR / fname).convert("RGB"))
            ax.axis("off")
            ax.set_title(f"{gname[:2]}-{idx:02d} {short_name(fname)}", fontsize=9)
            print(f"{gname[:2]}-{idx:02d} = {fname}")
        fig.suptitle(f"{gname} ({n} citra) — pilih nomornya", fontsize=12)
        fig.tight_layout()
        out = OUTDIR / f"{gname}.png"
        if args.show:
            plt.show()
        else:
            fig.savefig(out, dpi=150, bbox_inches="tight")
            print(f"saved {out} ({out.stat().st_size/1024:.0f} KB)")
        plt.close(fig)


if __name__ == "__main__":
    main()
