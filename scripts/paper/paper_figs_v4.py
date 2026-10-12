#!/usr/bin/env python3
"""IEEE-ready figures (English) for the conference paper, sourced from V4 CSVs.

Reads numbers directly from result CSVs (no hard-coded metrics):
  - runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/domain_gap.csv
  - runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/zs_per_class_metrics.csv
  - runs/rdd_yolov8n_local/<model>_class_weight_test_per_class_metrics.csv

Outputs (300 dpi, ~7 in wide for IEEE figure*):
  - latex/IEEE-Conference/gambar/paper_fig1_domain_gap_v4.png
  - latex/IEEE-Conference/gambar/paper_fig2_perclass_collapse_v12n.png

Usage:
  python3 scripts/paper/paper_figs_v4.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
EV = REPO / "runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4"
OUT = REPO / "latex/IEEE-Conference/gambar"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.dpi": 300,
    }
)

SRC_PER_CLASS_FILES = {
    "yolov12n": REPO / "runs/rdd_yolov8n_local/yolov12n_class_weight_test_per_class_metrics.csv",
    "yolo_rd": REPO / "runs/rdd_yolov8n_local/yolo_rd_class_weight_test_per_class_metrics.csv",
    "yolov8_pd": REPO / "runs/rdd_yolov8n_local/yolov8_pd_class_weight_test_per_class_metrics.csv",
    "yolov8n": REPO / "runs/rdd_yolov8n_local/yolov8n_class_weight_test_per_class_metrics.csv",
    "yolov26n": REPO / "runs/rdd_yolov8n_local/yolov26n_class_weight_test_per_class_metrics.csv",
}

MODEL_LABEL = {
    "yolov12n": "YOLOv12n",
    "yolo_rd": "YOLO-RD",
    "yolov8_pd": "YOLOv8-PD",
    "yolov8n": "YOLOv8n",
    "yolov26n": "YOLOv26n",
}

CLASS_ORDER = [
    "Longitudinal_Crack",
    "Transverse_Crack",
    "Alligator_Crack",
    "Pothole",
    "patchy_road",
]
CLASS_SHORT = {
    "Longitudinal_Crack": "Long.",
    "Transverse_Crack": "Trans.",
    "Alligator_Crack": "Allig.",
    "Pothole": "Pothole",
    "patchy_road": "Patchy",
}

C_SRC = "#2E5A88"  # muted steel blue
C_TGT = "#C96A1B"  # muted dark orange


def read_domain_gap() -> list[dict]:
    with open(EV / "domain_gap.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    # order by target mAP descending (best target model first)
    rows.sort(key=lambda r: float(r["indo_v4_zs_5cls"]), reverse=True)
    return rows


def fig1_domain_gap(rows: list[dict]) -> Path:
    labels: list[str] = [str(MODEL_LABEL.get(r["model"], r["model"])) for r in rows]
    src = [float(r["src_test_5cls"]) for r in rows]
    tgt = [float(r["indo_v4_zs_5cls"]) for r in rows]
    drop = [float(r["drop_mAP50_pct"]) for r in rows]

    x = range(len(rows))
    w = 0.36
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    b1 = ax.bar([i - w / 2 for i in x], src, width=w, color=C_SRC, label="Source test (5 shared classes)")
    b2 = ax.bar([i + w / 2 for i in x], tgt, width=w, color=C_TGT, label="Target V4 zero-shot (5 classes)")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("mAP@0.5")
    ax.set_title("Source vs zero-shot target mAP@0.5 over five shared classes (V4, 307 images)")
    ax.set_ylim(0, 0.90)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    for i, (sv, tv) in enumerate(zip(src, tgt)):
        ax.text(i - w / 2, sv + 0.015, f"{sv:.3f}", ha="center", va="bottom", fontsize=8)
        ax.text(i + w / 2, tv + 0.015, f"{tv:.3f}", ha="center", va="bottom", fontsize=8)
    for i, d in enumerate(drop):
        ax.text(i, 0.76, f"{d:.1f}%", ha="center", va="bottom", fontsize=8, color="black")
    ax.legend(frameon=True, loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2)
    fig.tight_layout()
    out = OUT / "paper_fig1_domain_gap_v4.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def read_per_class(model: str) -> tuple[dict, dict]:
    """Return (source_mAP, target_mAP/support) for CLASS_ORDER."""
    with open(SRC_PER_CLASS_FILES[model], newline="") as f:
        srows = {r["class_name"]: float(r["mAP50"]) for r in csv.DictReader(f)}
    with open(EV / "zs_per_class_metrics.csv", newline="") as f:
        trows = {r["class_name"]: r for r in csv.DictReader(f) if r["model"] == model}
    src = {c: srows[c] for c in CLASS_ORDER}
    tgt = {c: (float(trows[c]["mAP50"]), int(trows[c]["support"])) for c in CLASS_ORDER}
    return src, tgt


def fig2_perclass_collapse(model: str = "yolov12n") -> Path:
    src, tgt = read_per_class(model)
    xlab = [f"{CLASS_SHORT[c]}\n(n={tgt[c][1]})" for c in CLASS_ORDER]
    s = [src[c] for c in CLASS_ORDER]
    t = [tgt[c][0] for c in CLASS_ORDER]
    n = [tgt[c][1] for c in CLASS_ORDER]

    x = range(len(CLASS_ORDER))
    w = 0.36
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    b1 = ax.bar([i - w / 2 for i in x], s, width=w, color=C_SRC, label="Source test")
    b2 = ax.bar([i + w / 2 for i in x], t, width=w, color=C_TGT, label="Target V4 zero-shot")
    ax.set_xticks(list(x), xlab)
    ax.set_ylabel("AP@0.5")
    ax.set_title(
        f"Per-class collapse on V4 for {MODEL_LABEL[model]} (target support n shown above orange bars)"
    )
    ax.set_ylim(0, 0.95)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    for i, (sv, tv) in enumerate(zip(s, t)):
        ax.text(i - w / 2, sv + 0.045, f"{sv:.3f}", ha="center", va="bottom", fontsize=7.5)
        ax.text(i + w / 2, tv + 0.015, f"{tv:.3f}", ha="center", va="bottom", fontsize=7.5)
    ax.legend(frameon=True, loc="upper right")
    ax.legend(frameon=True, loc="upper right")
    fig.tight_layout()
    out = OUT / "paper_fig2_perclass_collapse_v12n.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = read_domain_gap()
    p1 = fig1_domain_gap(rows)
    p2 = fig2_perclass_collapse("yolov12n")
    print(f"wrote {p1} ({p1.stat().st_size/1024:.0f} KB)")
    print(f"wrote {p2} ({p2.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
