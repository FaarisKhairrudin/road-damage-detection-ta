# Project memory

## Project objective and stage (user-confirmed)
- The enduring goal is completing the Data Science final research and thesis book at Telkom University as part of graduation requirements.
- The conference paper has been submitted. Acceptance, publication, review status and graduation have not been established; do not infer them.
- The user is now beginning/continuing the thesis-book writing stage in `latex/buku-ta-template/`; check actual chapter content and the writing guide for each task.
- Keep this larger objective in STATE across sessions; update recent progress in place and change the objective only on explicit user direction (ask if ambiguous).

## Working agreements (user-confirmed)
- This is the private research workspace. The curated public portfolio is a separate sibling repository.
- The earlier structural-only scope was superseded for the approved research-docs/analysis update. Submitted PDF snapshots remain protected; the active thesis-book source may be edited when the user authorizes that writing scope. Preserve unrelated notebook edits.
- Keep superseded artifacts as archives and provide an original-path → destination report.
- GPU/domain processing was initially deferred; after the user resumed, V4 completed with 1302×256 embeddings and verified output hashes. V2 remains a separate archive; do not relabel it as V4.
- User-supplied continuity guidance supersedes adding per-session dated progress logs: use STATE for present work and MEMORY for durable lessons. Preserve existing docs/progress history.
- Ask for approval before new implementation scope; approval covers the agreed work without asking per file.

## Verified final-data and metric conventions
- Target data/RDD-indo-v4 is Roboflow rdd-indo-crop version 4: 307 images, 502 annotations, 39 empty labels. Its valid split is used as the target test.
- Target ID → source ID mapping: {0:2, 1:0, 2:5, 3:3, 4:1}. Target has no manhole GT.
- Primary source/target comparison uses the same four damage classes, retaining six-class checkpoints and all target images. Five-class V4 metrics remain valid supplementary results, not replacements for the primary four-class metric.
- Final weighting is effective-number class weighting on classification BCE (beta=0.999), not Focal Loss. Infer actual training settings from args.yaml, not names or stale notebook constants.
- The final four-class CSVs for v8n/v12n/v26n are in runs/rdd_4class_local_pc_lab; PD/RD CSVs are in runs/rdd_4class_local. Their final weights/args are in rdd_4class_local. Do not discard the lab folder as a duplicate.

## Verified preservation/dependency pitfalls
- Legacy domain_viz uses Indo V2 (995 source + 308 target). The distinct domain_viz_v4 bundle uses 995+307=1302 images and has freshly computed embeddings, projections and manifests. Projections are descriptive, not causal evidence.
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
- User explicitly authorized publishing the existing thesis-book source, required assets/bibliography/guides and its asset-generation helper on main. These are draft sources; build/hasil outputs remain local under the existing ignore rules.

## Source of truth
Use docs/INDEX.md and docs/FINAL_ARTIFACTS.json for current routing. Old dataset/results/summary paths may be compatibility aliases to archives; they are not active selections and remain writable. Use new output locations for a future rerun to avoid overwriting history.
Use docs/REORGANIZATION.md for move details and the pending content-review list.
Historical summaries and progress notes explain prior decisions; verify them against current artifacts before relying on them.

## Confirmed missing artifact
- PD four-class final weights/args/metrics exist, but its run results.csv is absent. FINAL_ARTIFACTS.json records a null training_curve and the missing path; do not substitute another run or fabricate a curve.

## Illustrated analysis location
- User requested moving the 15-image narrative to docs/draft-analisis-rapih.md. The narrative is synchronized to final CSVs and the verified V4 domain bundle with 15 figures; the technical Markdown redirects to it. Original pre-update versions are archived. scripts/paper/make_docx_rapih.py resolves images relative to the Markdown.

## Content report and execution status
- scripts/build_final_results.py regenerates authoritative CSV aggregates, RESULTS_TABLE and docs/figures/final_results without model inference; scripts/build_analysis_narrative.py regenerates the narrative.
- Supplementary five-class v12n relative drop is 45.4% when derived from full precision; do not retain 45.5% from rounded inputs. Primary four-class drop remains 34.1%.
- The user resumed after restarting NVIDIA; Python 3.12.16 / torch 2.6.0+cu124 detected the RTX 3050 and produced the V4 domain bundle on GPU.
- User authorized committing task-owned changes and pushing main; unrelated notebook/manuscript edits must remain local.
