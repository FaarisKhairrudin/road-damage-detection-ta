# 2026-10-15 — Zero-shot core classes, visual examples, and model selection

## Authorization and scope

The author explicitly requested an audit and immediate revision of the IEEE paper's zero-shot results and visual discussion. Requested goals were simple English, compact presentation, no detailed morning-time subgroup discussion, appropriate limits on claims, and recommendations for accuracy, balance, or speed. The author also asked whether the main comparison should focus on the four core damage classes instead of five labels.

Edited manuscript: `latex/IEEE-Conference/main.tex`. Raw results, datasets, prediction figures, and draft analysis documents are unchanged. A pre-edit copy is stored at `latex/IEEE-Conference/build/revision-backups/main-before-zero-shot-2026-10-15.tex`.

## Audit findings

- The existing paper already contained both five-class transfer and four-damage-class sensitivity tables. Promoting the four-class comparison does not require new training or inference.
- Six-class trained weights remain the weights used for zero-shot evaluation. Four-class AP aggregation is not the separate four-class-training ablation.
- All 307 target images remain included. There are 502 annotations in total, of which 481 belong to D00/D10/D20/D40 and 21 are patchy road. Manhole has no target annotations.
- Recomputed means and relative decreases from full-precision source and target per-class CSVs before rounding. Authoritative paths:
  - `runs/rdd_yolov8n_local/<model>_class_weight_test_per_class_metrics.csv`
  - `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/zs_per_class_metrics.csv`
- The previous target F1 sentence attached an equal-class-weight explanation ambiguously to support-weighted F1. That sentence and the five-class F1 column are removed rather than reused with a four-class label.
- Inspected `paper_figG_error_success_cases.png`: upper row is background-annotated porous-looking pavement with YOLOv12n patchy 0.78, YOLOv8-PD pothole 0.69, and no displayed YOLO-RD box. Lower row has an annotated longitudinal crack identified by all three displayed models with different boxes.
- Figure provenance: `docs/progress/2026-10-09-plot-final-G1-G2-G3.md` and `2026-10-09-paper-full-analysis-first-pass.md`. These are curated examples, not an exhaustive or frequency-estimating error sample.
- The author reported that inspected target repairs may be worn, irregular, partly missing, or light-colored/cement-like, unlike clearer and darker source patches. These observations are treated as annotation/appearance context, not a measured material identification or causal explanation of AP.
- A separate consistency issue affects training-cost interpretation: all five `args.yaml` files specify batch 16, seed 42, and patience 40. AMP is true for YOLOv8n/YOLOv12n/YOLO26n and false for the two custom reconstructions. Corrected the manuscript's contradictory claim that batch sizes varied.

## Verified four-class transfer values

| Model | Source mean AP@0.5 | Target mean AP@0.5 | Relative decrease (%) |
| --- | ---: | ---: | ---: |
| YOLOv8n | 0.622 | 0.303 | 51.4 |
| YOLOv12n | 0.626 | 0.413 | 34.1 |
| YOLO26n | 0.604 | 0.301 | 50.2 |
| YOLOv8-PD | 0.623 | 0.342 | 45.2 |
| YOLO-RD | 0.633 | 0.359 | 43.4 |

For YOLOv12n the unrounded means are 0.626359217 on source and 0.412604173 on target, giving a 34.126590% relative decrease. The existing five-class result remains 0.618 source and 0.337 target, with a 45.5% relative decrease. Target patchy-road AP spans 0.036–0.075 across the five models.

## Revisions applied

1. Made four-damage-class transfer the main zero-shot table, using the existing `tab:transfer` label. Removed the duplicate sensitivity subsection/table and unused `coretransferanalysis` toggle. Table count decreases by one without changing evaluation artifacts.
2. Kept a compact five-class check in the results, including very low patchy-road AP and its 21-instance support. The choice is justified by the core detection task, not by hiding low patch performance. This editorial change is a reanalysis of existing results, not a preregistered choice or a new experiment.
3. Synchronized the abstract, target-data description, metric definition, equation, and conclusion with four-class primary reporting. The abstract no longer presents the five-class result as the headline result. The full five-class annotation inventory remains explicit in Methods.
4. Replaced morning-subgroup counts and detailed proxy explanations with a short upper-row false-alarm/lower-row crack-detection explanation. Ground-truth annotations and display/evaluation confidence thresholds remain defined.
5. Kept porous-looking texture and reflected light as possible sources of visual confusion. Did not claim that most errors are caused by texture, that morning light caused the AP drop, or that this corridor represents Indonesian roads generally.
6. Added `Model Selection by Priority`: source-like accuracy candidate YOLO-RD, observed accuracy/transfer/throughput balance YOLOv12n, measured-throughput candidate YOLOv8-PD, lower estimated GFLOPs YOLO26n, and shorter observed training YOLOv8n. Recommendations require validation on intended road data and hardware and do not imply deployment readiness.
7. Preserved IEEEtran layout, fonts, column widths, existing image assets, and bibliography. No new figure or table is added.

## Verification

- Static check: every source reference resolves to an existing label after removing the sensitivity table.
- All five main transfer-table rows match recomputation from full-precision CSVs.
- Removed the old subgroup-count text, five-class target F1 column, and obsolete sensitivity references.
- `git diff --check` is clean for the manuscript.
- First compile completed successfully: `pdfinfo` confirms 6 letter-size pages. The build has 0 overfull boxes, 0 undefined or multiply defined references, and 0 LaTeX errors. Underfull-box warnings remain.
- PDF text confirms 0.413, 34.1%, the secondary 45.5% decrease, the 481/502 annotation distinction, and the new section headings. The old target-F1 header and morning-subgroup count discussion are absent.
- Visual inspection of rendered pages found the target figure deferred until after References. Moved its float declaration immediately after its first citation in the zero-shot subsection while retaining the detailed discussion in Section IV-E. Caption now explicitly describes false alarms relative to the reference annotations. No image, margin, font, or column-width changes were made.
- Removed an inherited semicolon from the edited Limitations paragraph. Added-line checks now find 0 semicolons and 0 em dashes, and the source has exactly one target-figure declaration.
- Moving the float declaration earlier alone did not resolve the placement: the tall single-column domain figure still occupied page 5, leaving the two-column target figure queued for page 6. Added a conditional native `\newpage` before the bibliography to move References to the next column, allowing the target figure to precede the reference list. This does not change fonts, margins, column widths, or image scale. It is a placement choice that needs rechecking if subsequent text edits change pagination.
- Final compile is successful and remains 6 pages, verified with `pdfinfo` rather than a trailing-form-feed count. There are 0 overfull boxes, 0 LaTeX errors, 0 undefined references/citations, and 0 multiply defined labels.
- Rendered and inspected the final page: the target panel and its caption appear at the top of page 6, before the References heading and bibliography below them. PDF bounding-box checks confirm the caption starts at y=244.93 pt and References at y=293.72 pt. The two-column panel retains readable labels, and there is no content overlap.
- Final PDF: `latex/IEEE-Conference/hasil/Paper_IEEE_Conference.pdf`, also copied to `hasil/main.pdf` within that paper folder. No new inference or training was performed.

## Remaining limits

No new target annotation-quality audit, matched-object error analysis, material test, lighting-stratified evaluation, multi-seed training, or hardware benchmark was run. Target patch descriptions are author-reported visual observations. The selection recommendations remain descriptive for these runs, and the original five-class/F1 artifacts remain available for fuller reporting.
