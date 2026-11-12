#!/usr/bin/env python3
"""UMAP per-domain figure for the paper, without a main title.

Reproduces code/07_domain_visualization.ipynb (cell 6) exactly:
same embeddings, same UMAP parameters, same seed. Only difference is that the
centred main title is omitted, because IEEE figures carry the title in the
LaTeX caption instead.

Reads : runs/rdd_yolov8n_local/evaluation/domain_viz/{embeddings.npy,domains.npy}
Writes: latex/IEEE-Conference/gambar/draft_umap_per_domain.png

Usage:
  python3.12 scripts/paper/paper_fig_umap.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import umap
from sklearn.preprocessing import normalize

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "runs/rdd_yolov8n_local/evaluation/domain_viz"
OUT = REPO / "latex/IEEE-Conference/gambar/draft_umap_per_domain.png"

plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": 8, "figure.dpi": 300})


def main() -> None:
    X = np.load(SRC / "embeddings.npy")
    dom = np.load(SRC / "domains.npy", allow_pickle=True)
    order = ["China", "Japan", "India", "Indo"]
    cmap = {"China": "#1f77b4", "Japan": "#ff7f0e",
            "India": "#2ca02c", "Indo": "#000000ff"}
    U = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42).fit_transform(normalize(X))

    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    for d in order:
        pts = U[dom == d]
        ax.scatter(pts[:, 0], pts[:, 1], s=8, alpha=0.75, c=cmap[d],
                   label=f"{d} (n={(dom == d).sum()})")
    ax.legend(markerscale=2, fontsize=6.5, loc="upper right", frameon=True)
    ax.set_xlabel("UMAP 1", fontsize=7)
    ax.set_ylabel("UMAP 2", fontsize=7)
    ax.tick_params(labelsize=6.5)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote {OUT} ({OUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
