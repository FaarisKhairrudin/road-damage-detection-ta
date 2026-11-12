# Current work state

## Goal
Synchronize final documentation/tables, then commit task-owned work and push main.
GPU-dependent domain processing is deferred by the user's latest instruction.

## Completed
- Final CSV generator rebuilt source6/common4/ablation/country/supplementary5
  tables and eight documentation figures without retraining detectors.
- Narrative updated with 11 figures and correct metric scopes/limitations.
- Root/data/model/ISRITI readmes updated; old technical Markdown redirects.
- Misleading hardcoded Word generator deprecated; no DOCX regenerated.
- Original affected files archived byte-exact under docs/archive/content-before-update.
- New V4 runner/completion validation prepared; old V2 bundle untouched.
- Switched to main at the same source tree, retaining unrelated working edits.

## Checks actually run
- Metric rounding, current report provenance, syntax and active links: passed.
- Completion-gate fixtures reject incomplete/corrupt bundles: passed.
- Custom model executable AST unchanged; only module docstring changed.
- CPU feature extraction was attempted and stopped at user request; no final
  embeddings/projections/statistics were produced. No detector training ran.

## In progress
- Final protected hashes, active links and staged-file review.
- Commit and push main (authorized, not yet completed).

## Deferred / unresolved
- UMAP/t-SNE V4 and feature/statistics execution until user resumes after restart.
- Notebook edits remain outside scope; notebook07 already had a pre-existing edit.
- PD four-class training results.csv remains unavailable; no substitute fabricated.
- No LaTeX/PDF rebuild or DOCX export requested/performed.

## Key paths
- docs/INDEX.md; docs/FINAL_ARTIFACTS.json; docs/draft-analisis-rapih.md.
- docs/RESULTS_TABLE.md; docs/REORGANIZATION.md; docs/archive/MANIFEST.json.
- Final report: runs/rdd_yolov8n_local/evaluation/final_report/.
- Deferred inputs: runs/rdd_yolov8n_local/evaluation/domain_viz_v4/ (INCOMPLETE).
- Temporary checks: /tmp/ta-content-update/.

## Next concrete action
Verify preservation/links, stage only task-owned paths, commit and push main;
report the published commit and explicit GPU deferral.
