#!/usr/bin/env python3
"""Compact summary figures as table replacements (source 6-class + per-country).

Four standalone options, pick whichever fits the paper:
  paper_figX1_dashboard.png  — 4-panel combo (distribution / trade-off / radar / per-country)
  paper_figX2_radar.png      — radar: 5 models x 6 classes
  paper_figX3_bubble.png     — bubble trade-off: mAP50 vs FPS, size=params, color=GFLOPs
  paper_figX4_heatmap.png    — heatmap: model x class + model x country

All values are taken from docs/RESULTS_TABLE.md (test split, nc=6) and
runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/domain_gap.csv.

Usage:
  python3 scripts/paper/paper_figs_summary.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

REPO = Path(__file__).resolve().parents[2]
OUTDIR = REPO / "latex/IEEE-Conference/gambar"
DOMAIN_GAP = REPO / "runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/domain_gap.csv"

MODELS = ["YOLOv8n", "YOLOv12n", "YOLOv26n", "YOLOv8-PD", "YOLO-RD"]
COLORS = {"YOLOv8n": "#4C72B0", "YOLOv12n": "#DD8452", "YOLOv26n": "#55A868",
          "YOLOv8-PD": "#C44E52", "YOLO-RD": "#8172B3"}

CLASSES = ["Long", "Trans", "Allig", "Poth", "Manh", "Patchy"]

# test mAP50 per class (6 cls), from RESULTS_TABLE.md
PER_CLASS = {
    "YOLOv8n":  [0.664, 0.599, 0.700, 0.526, 0.825, 0.571],
    "YOLOv12n": [0.680, 0.582, 0.708, 0.535, 0.833, 0.587],
    "YOLOv26n": [0.639, 0.567, 0.675, 0.538, 0.820, 0.512],
    "YOLOv8-PD": [0.678, 0.572, 0.702, 0.541, 0.819, 0.562],
    "YOLO-RD":  [0.696, 0.608, 0.701, 0.527, 0.845, 0.587],
}
OVERALL = {"YOLOv8n": 0.648, "YOLOv12n": 0.654, "YOLOv26n": 0.625,
           "YOLOv8-PD": 0.646, "YOLO-RD": 0.661}
PARAMS = {"YOLOv8n": 3.01, "YOLOv12n": 2.57, "YOLOv26n": 2.51,
          "YOLOv8-PD": 2.46, "YOLO-RD": 7.09}  # millions
GFLOPS = {"YOLOv8n": 8.2, "YOLOv12n": 7.5, "YOLOv26n": 5.9,
          "YOLOv8-PD": 7.7, "YOLO-RD": 12.9}
FPS = {"YOLOv8n": 219.7, "YOLOv12n": 319.3, "YOLOv26n": 293.3,
       "YOLOv8-PD": 368.4, "YOLO-RD": 189.4}

COUNTRY = {
    "China": {"YOLOv8n": 0.883, "YOLOv12n": 0.890, "YOLOv26n": 0.869,
              "YOLOv8-PD": 0.907, "YOLO-RD": 0.892},
    "Japan": {"YOLOv8n": 0.581, "YOLOv12n": 0.587, "YOLOv26n": 0.546,
              "YOLOv8-PD": 0.570, "YOLO-RD": 0.594},
    "India": {"YOLOv8n": 0.426, "YOLOv12n": 0.433, "YOLOv26n": 0.443,
              "YOLOv8-PD": 0.438, "YOLO-RD": 0.442},
}
N_IMG = {"China": 180, "Japan": 705, "India": 110}

# source train/test instances per class
TRAIN_N = [4555, 3219, 4385, 2192, 2270, 471]
TEST_N = [635, 446, 642, 312, 321, 69]

plt.rcParams.update({"font.family": "serif",
                     "font.serif": ["Times New Roman", "DejaVu Serif"],
                     "font.size": 7, "axes.titlesize": 8, "figure.dpi": 300})


def load_domain_gap() -> dict[str, float]:
    out: dict[str, float] = {}
    if DOMAIN_GAP.exists():
        with DOMAIN_GAP.open() as fh:
            for row in csv.DictReader(fh):
                key = row.get("model") or row.get("Model") or ""
                key = key.replace("_class_weight", "")
                for name in MODELS:
                    if name.replace("-", "").lower() in key.replace("_", "").lower():
                        for col in ("drop_mAP50_pct", "drop_map50_pct"):
                            if col in row and row[col]:
                                out[name] = abs(float(row[col]))
                        break
    return out


# ---------------------------------------------------------------- option 1
def fig_dashboard() -> Path:
    fig = plt.figure(figsize=(7.1, 5.2))
    gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.28,
                          left=0.08, right=0.98, top=0.93, bottom=0.09)

    # (a) class distribution
    ax = fig.add_subplot(gs[0, 0])
    y = np.arange(len(CLASSES))[::-1]
    ax.barh(y + 0.18, TRAIN_N, height=0.34, color="#4C72B0", label="Train")
    ax.barh(y - 0.18, TEST_N, height=0.34, color="#DD8452", label="Test")
    for yi, (tr, te) in zip(y, zip(TRAIN_N, TEST_N), strict=True):
        ax.text(tr + 60, yi + 0.18, f"{tr:,}".replace(",", " "), va="center", fontsize=6)
        ax.text(te + 60, yi - 0.18, f"{te}", va="center", fontsize=6)
    ax.set_yticks(y, CLASSES, fontsize=7)
    ax.set_xlim(0, 5400)
    ax.set_xlabel("instances")
    ax.set_title("(a) Class distribution (source)", loc="left")
    ax.legend(fontsize=6, frameon=False, loc="lower right")
    ax.grid(axis="x", alpha=0.25, lw=0.5)
    ax.set_axisbelow(True)

    # (b) bubble trade-off
    ax = fig.add_subplot(gs[0, 1])
    cmap = plt.get_cmap("viridis")
    norm = plt.Normalize(min(GFLOPS.values()), max(GFLOPS.values()))
    for m in MODELS:
        ax.scatter(FPS[m], OVERALL[m], s=PARAMS[m] * 34, color=COLORS[m],
                   alpha=0.82, edgecolor="black", lw=0.5, zorder=3)
        ax.annotate(m, (FPS[m], OVERALL[m]), textcoords="offset points",
                    xytext=(0, 11), ha="center", fontsize=6)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, ax=ax, pad=0.02, fraction=0.05)
    cb.set_label("GFLOPs", fontsize=6)
    cb.ax.tick_params(labelsize=5)
    ax.set_xlabel("FPS")
    ax.set_ylabel("test mAP50 (6 cls)")
    ax.set_title("(b) Accuracy vs speed (size = params)", loc="left")
    ax.grid(alpha=0.25, lw=0.5)
    ax.set_axisbelow(True)
    ax.margins(x=0.16, y=0.22)

    # (c) radar
    ax = fig.add_subplot(gs[1, 0], projection="polar")
    angles = np.linspace(0, 2 * np.pi, len(CLASSES), endpoint=False).tolist()
    angles += angles[:1]
    for m in MODELS:
        vals = PER_CLASS[m] + PER_CLASS[m][:1]
        ax.plot(angles, vals, color=COLORS[m], lw=1.1, label=m)
        ax.fill(angles, vals, color=COLORS[m], alpha=0.06)
    ax.set_xticks(angles[:-1], CLASSES, fontsize=6)
    ax.set_ylim(0.4, 0.95)
    ax.set_yticks([0.5, 0.7, 0.9], ["0.5", "0.7", "0.9"], fontsize=5)
    ax.tick_params(pad=1)
    ax.set_title("(c) Per-class mAP50 (source)", loc="left", pad=14)
    ax.legend(fontsize=5, frameon=False, loc="upper right",
              bbox_to_anchor=(1.28, 1.12))

    # (d) per-country grouped bars
    ax = fig.add_subplot(gs[1, 1])
    x = np.arange(len(MODELS))
    width = 0.26
    ccol = {"China": "#2E7D32", "Japan": "#1565C0", "India": "#C62828"}
    for k, cty in enumerate(["China", "Japan", "India"]):
        vals = [COUNTRY[cty][m] for m in MODELS]
        ax.bar(x + (k - 1) * width, vals, width, color=ccol[cty],
               label=f"{cty} (n={N_IMG[cty]})")
    ax.set_xticks(x, [m.replace("YOLO", "") for m in MODELS], fontsize=6)
    ax.set_ylabel("test mAP50 (6 cls)")
    ax.set_ylim(0, 1.0)
    ax.set_title("(d) Per-country performance", loc="left")
    ax.legend(fontsize=6, frameon=False, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, -0.13))
    ax.grid(axis="y", alpha=0.25, lw=0.5)
    ax.set_axisbelow(True)

    out = OUTDIR / "paper_figX1_dashboard.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    return out


# ---------------------------------------------------------------- option 2
def fig_radar() -> Path:
    fig, ax = plt.subplots(figsize=(3.4, 3.2), subplot_kw={"projection": "polar"})
    angles = np.linspace(0, 2 * np.pi, len(CLASSES), endpoint=False).tolist()
    angles += angles[:1]
    for m in MODELS:
        vals = PER_CLASS[m] + PER_CLASS[m][:1]
        ax.plot(angles, vals, color=COLORS[m], lw=1.2, marker="o", ms=2.2, label=m)
        ax.fill(angles, vals, color=COLORS[m], alpha=0.05)
    ax.set_xticks(angles[:-1], CLASSES, fontsize=7)
    ax.set_ylim(0.4, 0.95)
    ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9], ["0.5", "0.6", "0.7", "0.8", "0.9"], fontsize=5.5)
    ax.tick_params(pad=2)
    ax.legend(fontsize=6, frameon=False, loc="upper center",
              bbox_to_anchor=(0.5, -0.06), ncol=3)
    fig.suptitle("Per-class mAP50 by model (source, 6 classes)", fontsize=8, y=0.98)
    out = OUTDIR / "paper_figX2_radar.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    return out


# ---------------------------------------------------------------- option 3
def fig_bubble() -> Path:
    fig, ax = plt.subplots(figsize=(3.6, 2.9))
    cmap = plt.get_cmap("viridis")
    norm = plt.Normalize(min(GFLOPS.values()), max(GFLOPS.values()))
    for m in MODELS:
        ax.scatter(FPS[m], OVERALL[m], s=PARAMS[m] * 55, color=cmap(norm(GFLOPS[m])),
                   alpha=0.85, edgecolor="black", lw=0.6, zorder=3)
        ax.annotate(m, (FPS[m], OVERALL[m]), textcoords="offset points",
                    xytext=(0, 14), ha="center", fontsize=7)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, ax=ax, pad=0.02, fraction=0.045)
    cb.set_label("GFLOPs", fontsize=6.5)
    cb.ax.tick_params(labelsize=5.5)
    ax.set_xlabel("FPS (higher is better)")
    ax.set_ylabel("test mAP50, 6 classes")
    ax.set_title("Accuracy vs speed vs size", fontsize=8)
    ax.grid(alpha=0.25, lw=0.5)
    ax.set_axisbelow(True)
    ax.margins(x=0.18, y=0.24)
    out = OUTDIR / "paper_figX3_bubble.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    return out


# ---------------------------------------------------------------- option 4
def fig_heatmap() -> Path:
    cols = ["China", "Japan", "India", "Overall"]
    n_lbl = {"China": 180, "Japan": 705, "India": 110, "Overall": 995}
    mat = np.array([[COUNTRY[c][m] for c in ("China", "Japan", "India")] + [OVERALL[m]]
                    for m in MODELS])
    fig, ax = plt.subplots(figsize=(3.7, 2.7))
    im = ax.imshow(mat, cmap="YlOrRd", vmin=0.4, vmax=0.95, aspect="auto")
    ax.set_xticks(range(len(cols)), [f"{c}\n(n={n_lbl[c]})" for c in cols], fontsize=6.5)
    ax.set_yticks(range(len(MODELS)), MODELS, fontsize=7)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            ax.text(j, i, f"{v:.2f}".replace(".", ","), ha="center", va="center",
                    fontsize=6.5, color="white" if v > 0.72 else "black")
    cb = fig.colorbar(im, ax=ax, pad=0.02, fraction=0.07)
    cb.ax.tick_params(labelsize=6)

    out = OUTDIR / "paper_figX4_heatmap.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
    return out


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    dg = load_domain_gap()
    if dg:
        print("domain_gap drop (mAP50 pct):", {k: round(v, 1) for k, v in dg.items()})
    fig_dashboard()
    fig_radar()
    fig_bubble()
    fig_heatmap()


if __name__ == "__main__":
    main()
