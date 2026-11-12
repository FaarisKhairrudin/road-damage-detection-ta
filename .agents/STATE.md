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

## Publication completed
- Main implementation commit 9074582 was pushed to origin/main.
- 172 protected files (including 16 notebooks) remain unchanged.
- 111 active local links and 35 report-input hashes verified.
- Task-owned staged-file and whitespace checks passed; unrelated edits excluded.
- This continuity update records the published outcome.

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
No further non-GPU work remains for this request. When the user resumes GPU
work after restart, recheck CUDA and run the V4 script with explicit device; only
a fully validated bundle may update domain figures/narrative. Do not auto-resume.
