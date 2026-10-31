"""Dataset label-inventory figure for the dataset paragraph (one column).

Panel A: stacked train/val/test instances per class (6 labels).
Panel B: test-domain composition shift, source test vs RDD-Indo.
Counts verified by direct label-file counting 2026-10-16:
  train 6778 lbl-files (1 empty) inst {0:4555,1:3219,2:4385,3:2192,4:2270,5:471}
  val   1899 lbl-files (1 empty) inst {0:1257,1:897,2:1245,3:597,4:645,5:132}
  test   996 lbl-files (1 empty) inst {0:635,1:446,2:642,3:312,4:321,5:69}
  indo   307 lbl-files (39 empty) inst {0:48,1:231,2:21,3:70,4:132}
  (image inventory in the paragraph: 6777/1898/995, one fewer per split
  because of the single empty label file without an image pair)
No main title (IEEE rule); sub-labels (a)/(b) only. Narrow bars so
stem text fits inside cells.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "latex/IEEE-Conference/gambar/paper_fig_dataset_inventory.png"

CLS = ["Long", "Trans", "Allig", "Poth", "Manh", "Patchy"]
COLORS = ["#2E7D32", "#1565C0", "#EF6C00", "#C62828", "#6A1B9A", "#C2185B"]
TRAIN = np.array([4555, 3219, 4385, 2192, 2270, 471])
VAL = np.array([1257, 897, 1245, 597, 645, 132])
TEST = np.array([635, 446, 642, 312, 321, 69])
# Target ids: 0=Allig 48, 1=Long 231, 2=Patchy 21, 3=Poth 70, 4=Trans 132.
# Reordered to CLS order [Long, Trans, Allig, Poth, Manh, Patchy]:
INDO = np.array([231, 132, 48, 70, 0, 21], dtype=float)

plt.rcParams.update(
    {"font.family": "serif", "font.size": 6, "axes.labelsize": 6,
     "xtick.labelsize": 5.5, "ytick.labelsize": 5.5}
)
fig, (axA, axB) = plt.subplots(2, 1, figsize=(3.5, 3.1), gridspec_kw={"hspace": 0.55})

# --- (a) stacked train / val / test ---
x = np.arange(6)
b1 = axA.bar(x, TRAIN, 0.52, color=COLORS, edgecolor="white", linewidth=0.5,
             label="Train (17092)")
b2 = axA.bar(x, VAL, 0.52, bottom=TRAIN, color=COLORS, alpha=0.55,
             edgecolor="white", linewidth=0.5, label="Val (4773)")
b3 = axA.bar(x, TEST, 0.52, bottom=TRAIN + VAL, color=COLORS, alpha=0.30,
             edgecolor="white", linewidth=0.5, label="Test (2425)")
for i, (t, v, te) in enumerate(zip(TRAIN, VAL, TEST, strict=True)):
    tot = t + v + te
    axA.text(i, tot + 120, f"{tot}", ha="center", va="bottom", fontsize=5.5)
axA.axhline(471, color="#C2185B", ls=":", lw=0.8)
axA.text(5.55, 471, "Patchy train 471", color="#C2185B", fontsize=5,
         va="bottom", ha="right")
axA.set_xticks(x, CLS, rotation=18, ha="right")
axA.set_ylabel("Instances")
axA.set_ylim(0, 7200)
axA.text(-0.09, 1.04, "(a) N-RDD train / val / test per class",
         transform=axA.transAxes, fontsize=6.5, fontweight="bold", va="top",
         ha="left")
axA.legend(frameon=True, fontsize=5, handlelength=1.4, loc="upper left",
           borderpad=0.4)

# --- (b) composition shift: source test vs target ---
src = np.array([TEST[:4].sum(), TEST[4], TEST[5]], dtype=float)
tgt = np.array([INDO[:4].sum(), INDO[4], INDO[5]], dtype=float)
assert src.sum() == 2425 and tgt.sum() == 502
src_pct = 100 * src / src.sum()
tgt_pct = 100 * tgt / tgt.sum()
COLS = ["#37474F", "#6A1B9A", "#C2185B"]


def stacked_100(ax, ypos, pct, hatch=None):
    left = np.concatenate([[0.0], np.cumsum(pct / 100)[:-1]])
    bars = ax.barh([ypos] * 3, pct / 100, 0.42, left=left, color=COLS,
                   edgecolor="white", hatch=hatch)
    for b, p in zip(bars, pct, strict=True):
        if p >= 4:
            ax.text(b.get_x() + b.get_width() / 2,
                    b.get_y() + b.get_height() / 2, f"{p:.1f}%", ha="center",
                    va="center", fontsize=5.5, color="white")
    return bars


stacked_100(axB, 1.35, src_pct)
stacked_100(axB, 0.65, tgt_pct, hatch="//")
axB.text(0.01, 1.35, "Source test (2425): Long 635 Trans 446 Allig 642 Poth 312",
         va="center", ha="left", fontsize=5)
axB.text(0.01, 0.65, "RDD-Indo (502): Long 231 Trans 132 Allig 48 Poth 70",
         va="center", ha="left", fontsize=5)
axB.text(0.99, 0.42, "no manholes, 39 empty imgs",
         va="center", ha="right", fontsize=5, style="italic")
axB.set_xlim(0, 1)
axB.set_ylim(0.2, 1.8)
axB.set_yticks([1.35, 0.65], ["Source test", "RDD-Indo"])
axB.set_xlabel("Share of split instances")
axB.text(-0.09, 1.10, "(b) Test composition shifts to target",
         transform=axB.transAxes, fontsize=6.5, fontweight="bold", va="top",
         ha="left")

fig.savefig(OUT, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", OUT, f"({OUT.stat().st_size/1024:.0f} KB)")
print("panel A totals:", (TRAIN + VAL + TEST).tolist())
print("panel B src%:", np.round(src_pct, 1).tolist())
print("panel B tgt%:", np.round(tgt_pct, 1).tolist())
