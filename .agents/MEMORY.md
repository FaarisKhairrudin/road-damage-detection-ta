# Project memory

## Working agreements (user-confirmed)
- This is the private research workspace. The curated public portfolio is a separate sibling repository.
- Earlier structural-only scope is superseded by explicit approval to synchronize research docs/tables/report scripts. Notebooks and submitted/manuscript LaTeX/PDFs remain protected.
- Keep superseded artifacts as archives and provide an original-path → destination report.
- User explicitly deferred GPU/domain processing until after restart. CPU extraction was stopped; no complete V4 bundle exists. Do not relabel V2 or partial outputs as V4 results.
- User-supplied continuity guidance supersedes adding per-session dated progress logs: use STATE for present work and MEMORY for durable lessons. Preserve existing docs/progress history.
- Ask for approval before new implementation scope; approval covers the agreed work without asking per file.

## Verified final-data and metric conventions
- Target data/RDD-indo-v4 is Roboflow rdd-indo-crop version 4: 307 images, 502 annotations, 39 empty labels. Its valid split is used as the target test.
- Target ID → source ID mapping: {0:2, 1:0, 2:5, 3:3, 4:1}. Target has no manhole GT.
- Primary source/target comparison uses the same four damage classes, retaining six-class checkpoints and all target images. Five-class V4 metrics remain valid supplementary results, not replacements for the primary four-class metric.
- Final weighting is effective-number class weighting on classification BCE (beta=0.999), not Focal Loss. Infer actual training settings from args.yaml, not names or stale notebook constants.
- The final four-class CSVs for v8n/v12n/v26n are in runs/rdd_4class_local_pc_lab; PD/RD CSVs are in runs/rdd_4class_local. Their final weights/args are in rdd_4class_local. Do not discard the lab folder as a duplicate.

## Verified preservation/dependency pitfalls
- Existing domain_viz uses Indo V2: 995 source + 308 target images. A V4 rerun would have 995+307=1302 images. Regenerate embeddings and input manifests as well as plots; plotting old embeddings again is insufficient.
- Old target exports have different labels; v4-bak is Roboflow V3 (514 annotations), not an identical copy of final V4.
- Existing remapped views contain absolute image symlinks. Historical dataset locations need aliases if the physical folders move.
- Keep remapped view directories physical: old notebooks call shutil.rmtree(REM), which rejects directory symlinks.
- Most Python scripts calculate repo root from __file__. Moving them, even behind symlinks, can break .resolve().parents[...] logic. Leave executable paths stable during a no-content-edit pass.
- LaTeX build folders include manually preserved sources/QA/snapshots; they are not entirely disposable cache. Protect submitted PDFs and those archives.

## Manuscript state (verified from local revert manifest)
- Active submitted ISRITI version is the six-page ISRITI_Review_Anonymous_Layout_Revised.pdf.
- Its recorded SHA-256 is 8e00e6dea660c80b9ef28d942d6b9a27358950e42c7cfce6e0ce8b7873f7a690.
- The seven-page architecture discussion was reverted at the user's request and archived under latex/ISRITI-submission/build/archived-architecture-discussion-2026-11-13/. Do not restore it from stale README/index instructions.
- latex/buku-ta-template is current book work; latex/skripsi-telkom still supplies older proposal identity/reference context. Keep both paths stable for now.

## Source of truth
Use docs/INDEX.md and docs/FINAL_ARTIFACTS.json for current routing. Old dataset/results/summary paths may be compatibility aliases to archives; they are not active selections and remain writable. Use new output locations for a future rerun to avoid overwriting history.
Use docs/REORGANIZATION.md for move details and the pending content-review list.
Historical summaries and progress notes explain prior decisions; verify them against current artifacts before relying on them.

## Confirmed missing artifact
- PD four-class final weights/args/metrics exist, but its run results.csv is absent. FINAL_ARTIFACTS.json records a null training_curve and the missing path; do not substitute another run or fabricate a curve.

## Illustrated analysis location
- User requested moving the 15-image narrative to docs/draft-analisis-rapih.md. The narrative is now synchronized to final CSVs with 11 figures and a deferred V4 section; the technical Markdown redirects to it. Original pre-update versions are archived. scripts/paper/make_docx_rapih.py resolves images relative to the Markdown.

## Content report and execution status
- scripts/build_final_results.py regenerates authoritative CSV aggregates, RESULTS_TABLE and docs/figures/final_results without model inference; scripts/build_analysis_narrative.py regenerates the narrative.
- Supplementary five-class v12n relative drop is 45.4% when derived from full precision; do not retain 45.5% from rounded inputs. Primary four-class drop remains 34.1%.
- Current-session Python was /usr/bin/python3.12 (3.12.16), torch2.6.0+cu124; GPU hardware RTX3050 is present but active nouveau driver exposed no CUDA device. Recheck after restart; this is an observation, not a permanent hardware limitation.
- User authorized committing task-owned changes and pushing main; unrelated notebook/manuscript edits must remain local.
