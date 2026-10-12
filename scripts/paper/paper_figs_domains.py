#!/usr/bin/env python3
"""Domain characteristic panels — compact, English, same style as G plots.

Two variants:
  paper_figD3_domains.png — 3 source domains only (China/Japan/India), 3x3
  paper_figD4_domains.png — 3 source + Indonesia V4 target, 4x3

Images: 3 per domain closest to the domain median (brightness/saturation/
contrast/sharpness), i.e. the most typical-looking frames, not random picks.

Usage:
  python3 scripts/paper/paper_figs_domains.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OUTDIR = REPO / "latex/IEEE-Conference/gambar"
SRC = REPO / "data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/test/images"
V4 = REPO / "data/RDD-indo-v4/valid/images"

DOMAINS_3: dict[str, list[str]] = {
    "China (n=180)": [
        "China_MotorBike_001779_jpg.rf.421b5ffe08eee44952dd87684b106455.jpg",
        "China_MotorBike_000863_jpg.rf.2d4381786ca69c456ccd1fa63e9ebebd.jpg",
        "China_MotorBike_001890_jpg.rf.7a773b1b80b72c526a32e5a503194dfb.jpg",
    ],
    "Japan (n=705)": [
        "Japan_011914_jpg.rf.21e45fabf45ae64ee7838da43ab7d916.jpg",
        "Japan_005925_jpg.rf.4bec0906a80834ca7a0fd39d413a3ba3.jpg",
        "Japan_008835_jpg.rf.086bc704787936df01e313c03df93d8a.jpg",
    ],
    "India (n=110)": [
        "India_004602_jpg.rf.bdf699274c5ba3ca4e98e3baef521881.jpg",
        "India_002009_jpg.rf.8f769ac005f920771fc22b0d2540bfff.jpg",
        "India_003007_jpg.rf.8847ec3bd891bb5a28cf9fc0f9f73c6c.jpg",
    ],
}
INDO_3 = [
    "Merge-1_mp4-0563_jpg.rf.dbaac59f981ff5e61a3abc7cdee91f1f.jpg",
    "Merge-1_mp4-0435_jpg.rf.b44c67ac846e08eeb9a6168ecf2d5089.jpg",
    "VID_20260520_092711_mp4-0221_jpg.rf.495ae6e6bfd9deb92d8cbf1cfe071457.jpg",
]

plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": 8, "axes.titlesize": 8, "figure.dpi": 300})


def panel(domains: dict[str, list[str]], fname: str) -> Path:
    nrows, ncols = len(domains), 3
    cell = 1.6
    fig = plt.figure(figsize=(cell * ncols, cell * nrows))
    gs = fig.add_gridspec(nrows, ncols, hspace=0.12, wspace=0.06,
                          left=0.15, right=0.99, top=0.99, bottom=0.01)
    for i, (dname, files) in enumerate(domains.items()):
        base = V4 if "Indonesia" in dname else SRC
        for j, f in enumerate(files):
            ax = fig.add_subplot(gs[i, j])
            ax.imshow(Image.open(base / f).convert("RGB"))
            ax.axis("off")
            if j == 0:
                ax.text(-0.06, 0.5, dname, fontsize=8, rotation=90,
                        va="center", ha="right", transform=ax.transAxes)
    out = OUTDIR / fname
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    return out


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    panel(dict(DOMAINS_3), "paper_figD3_domains.png")
    panel({**DOMAINS_3, "Indonesia V4 (n=307)": INDO_3}, "paper_figD4_domains.png")


if __name__ == "__main__":
    main()
