# Current work state

## Goal
Complete the previously deferred domain analysis on Indonesia V4, integrate the
verified results into documentation, and push task-owned changes to main.

## Completed
- User resumed the V4 run after NVIDIA was enabled. Python 3.12 / torch CUDA
  detected the RTX 3050; no model training was performed.
- Extracted 1,302 × 256 embeddings for 995 source + 307 Indonesia V4 images;
  generated UMAP, t-SNE, image statistics and sample montage in a new bundle.
- Updated the final artifact map, index, 15-figure narrative and move/status report.
- Preserved the historical V2 bundle and all submitted manuscript/PDF artifacts.

## Checks actually run
- Verified complete status, all bundle output hashes, 1,302 image/label hashes,
  source checkpoint hash, manifest/domain ordering and finite projection shapes.
- Inspected all four V4 figures visually. No notebook or manuscript was executed.
- Independent detection/F1 results remain from the archived final CSVs; the
  domain projections describe features and are not evidence of causal effects.

## In progress
- Refresh report provenance after updating the artifact map; validate links.
- Stage task-owned documentation/figures and push main as previously authorized.

## Remaining
- Locate the missing PD four-class training results.csv if its source is available.
- Notebook edits remain out of scope; notebook07 had a pre-existing local edit.

## Key paths
- docs/INDEX.md; docs/draft-analisis-rapih.md; docs/figures/domain_v4/.
- runs/rdd_yolov8n_local/evaluation/domain_viz_v4/provenance.json.
- docs/FINAL_ARTIFACTS.json; docs/REORGANIZATION.md; docs/archive/MANIFEST.json.

## Next concrete action
Verify final report/input hashes and links, then commit and push task-owned files.
