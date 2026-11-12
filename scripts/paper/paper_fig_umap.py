#!/usr/bin/env python3
"""Plot the completed V4 projection for documentation, preserving submitted assets.

This entry point never plots archived V2 embeddings as V4 and never writes the
figure used in an already submitted manuscript. Domain inference is a separate,
currently deferred task: scripts/domain_analysis_v4.py.
"""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))


def main():
    source=ROOT/'runs/rdd_yolov8n_local/evaluation/domain_viz_v4'
    from scripts.domain_bundle import completed_bundle
    if completed_bundle(source) is None:
        raise SystemExit('V4 domain analysis is incomplete/deferred. Complete scripts/domain_analysis_v4.py before plotting; V2 outputs will not be substituted.')
    import numpy as np
    from scripts.domain_analysis_v4 import plot_projection
    output=ROOT/'docs/figures/domain_v4/umap.png'
    output.parent.mkdir(parents=True,exist_ok=True)
    plot_projection(np.load(source/'umap.npy'),np.load(source/'domains.npy'),'UMAP',output)
    print(output)


if __name__=='__main__':main()
