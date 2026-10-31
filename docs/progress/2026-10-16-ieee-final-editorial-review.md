# 2026-10-16 — Final IEEE editorial review and revision

## Authorization and scope

The author requested a final writing and page-efficiency review of `latex/IEEE-Conference/main.tex`, then explicitly authorized the corrections with the instruction to avoid overclaiming. The review covered the complete active manuscript, all three active figures, and every rendered PDF page. No experiment code, notebooks, run configurations, or model artifacts were opened during this editorial batch. No experiments or metric computations were repeated.

This note consolidates the discussion, changes, and verification for this batch rather than creating a log for each individual wording change.

Pre-edit backup:

- `latex/IEEE-Conference/build/revision-backups/main-before-final-editorial-2026-10-16.tex`

## Problems discussed and changes applied

### 1. Standard metric formulas and class alignment

- Did not add textbook equations for precision, recall, F1, or mAP. Defined mAP and macro-F1 as unweighted class averages in concise prose.
- Preserved the relative-decrease equation verbatim, including the distinction between evaluated classes and training classes.
- Kept `K=4` for the main four-damage-class transfer table and `K=5` for the additional check, which remains reported in prose for YOLOv12n (source 0.618, target 0.337, relative decrease 45.5%).
- Clarified that the 0.001 minimum confidence concerns AP evaluation. Did not invent or change an F1 operating-point selection rule.
- Explained that relative performance decrease is not the magnitude of domain shift.

### 2. Redundant setup details and long captions

- Condensed the Table I caption and note. GPU, throughput software versions, training-time definition, and best-checkpoint selection now reside in Methods.
- Reduced active mentions of RTX 4070 SUPER from three to one. Kept the software versions scoped to throughput measurement rather than asserting that every experiment used the same environment.
- Restored an explanation for the previously dangling GFLOPs dagger marker. The note distinguishes a computational estimate from a timing measurement.
- Standardized the Table I heading to `mAP@0.5:0.95`.
- Shortened the Table II, Table III, and figure captions. Preserved the Table III overlap confidence and IoU thresholds, the 321 manhole plus 69 patchy-road annotations, and the distinction between prediction-box counts and unique-object false-positive rates.
- Removed repeated model lists, repeated label-removal descriptions, and redundant warnings within the main text. Necessary four-class-evaluation versus six-class-training distinctions remain.
- Kept AMP settings in Methods and did not add an AMP limitation or an unverified hardware-equivalence claim, following the author's earlier decision.

### 3. Fig. 2 visual discussion

The active numbering is Fig. 1 for source-country prediction panels, Fig. 2 for source/target image appearance, and Fig. 3 for Indonesian target prediction panels. Table III is the source training-label comparison, not a duplicate of Fig. 3.

- Replaced generic/representativeness-oriented wording such as “typical-looking” with selected-example wording.
- Described the displayed Chinese images as downward-looking pavement views, Japanese images as forward-looking street views, Indian images as containing more sky and distant scenery with a lower vehicle edge in some panels, and Indonesian images as showing light-colored, coarse-textured pavement with cracks, traffic, and shadows.
- Did not assert that a particular camera angle caused a country's AP ranking, that the examples characterize entire national datasets, or that a visible vehicle edge proves a dashboard or windshield-reflection mechanism.
- Positioned the Fig. 1 declaration after its first textual citation.

### 4. Fig. 3 interpretation

- Removed the caption's repeated row-by-row explanation and kept panel order and display confidence.
- Row 2 now explicitly distinguishes YOLOv12n's miss, YOLO-RD's small misplaced transverse-crack box, and YOLOv8-PD's pothole-class prediction.
- Row 3 notes that YOLOv8-PD returns multiple boxes for the annotated longitudinal crack.
- Row 4 is described as two annotated longitudinal cracks and one transverse crack, with additional transverse-crack predictions. It is not described as three longitudinal cracks or as an entirely clean success case.
- Retained pavement texture and sunlight reflections as possible contributors observed in inspected examples, not demonstrated causes or explanations of the overall performance gap.

### 5. Geographic scope, annotations, and recommendations

- Aligned Methods with the author's account: collection in both directions, mainly on Jalan Raya Bojongsoang with some nearby streets.
- Replaced strict one-corridor wording in the Introduction, Limitations, and Conclusion with local-area/pilot wording.
- Removed the unsupported suggestion that target images may contain similar nearby video frames. Did not replace it with an unperformed formal deduplication claim.
- Added the author-reported single-annotator limitation and the absence of an inter-annotator agreement assessment. Did not infer that no other informal review ever occurred.
- Preserved single-seed, reconstruction/pretraining, limited geographic coverage, illustrative-case, and non-edge-device throughput limitations.
- Kept model recommendations conditional on the tested data and hardware, and described the source/target ranking change as an observation rather than a general law.
- Softened claims of an entirely untested literature gap or a strictly identical architecture-only training comparison.

## Preservation checks

Programmatically compared the revised LaTeX against the pre-edit backup:

- All four `tabular` blocks have identical numerical cells and structure. The only header change is normalized mAP notation.
- The relative-decrease equation is identical.
- All figure filenames and display widths are identical. No image assets were regenerated.
- The entire preamble is identical, including IEEEtran class, title/author PDF metadata, font/margin-related setup, and float settings.
- Approximately 300 whitespace-delimited LaTeX words were removed overall, despite the expanded visual discussion. This is an approximate editorial size comparison, not a formal natural-language word count.
- No results tables elsewhere, bibliography records, experiments, datasets, or model files were changed.

## Build and visual verification

A review-only render of the starting manuscript already contained five pages, not the six pages recorded for earlier drafts. The final revision also contains five pages.

Build command:

```bash
bash latex/IEEE-Conference/compile.sh
```

Verification:

- 5 pages.
- 0 LaTeX errors.
- 0 overfull boxes.
- 0 undefined references/citations.
- 0 multiply defined labels.
- 3 underfull-box warnings remain. No font, margin, or column-width hacks were used to suppress them.
- All pages were visually inspected after the editorial build. The last page was inspected again after the final layout adjustment.
- A native `\newpage` before the bibliography starts References in the next column, avoiding a very short final column after the text reduction. A source comment instructs future editors to recheck this break after length changes. It does not add a page in this version.
- PDF text checks confirm the macro-F1 explanation, Fig. 2 framing discussion, Fig. 3 mixed-class scene, single-annotator limitation, and five-class additional result. Superseded nearby-frame/one-corridor/clean-success wording is absent.
- `hasil/main.pdf` and `hasil/Paper_IEEE_Conference.pdf` are byte-identical.

Outputs:

- `latex/IEEE-Conference/hasil/Paper_IEEE_Conference.pdf`
- `latex/IEEE-Conference/hasil/main.pdf`
- `latex/IEEE-Conference/build/final-editorial-2026-10-16/page-{1..5}.png`
- `latex/IEEE-Conference/build/final-editorial-2026-10-16-compile.log`

## Verification boundaries

This was a manuscript/figure/PDF editorial pass, not a fresh experiment audit, literature search, or acceptance guarantee. No new numerical results, causal findings, annotation-agreement scores, or F1 threshold details were fabricated. Figure assets and their existing small panel labels were retained rather than redesigned.

## Follow-up — Semantic audit and targeted restoration

### Author correction and authorization

The author questioned whether explanations and insights had been lost during compression, specifically the overlap diagnostic's inability to establish a causal benefit from adding D70/D80 labels. A comparison of the complete pre-editorial backup with the revised manuscript confirmed that numerical preservation did not guarantee preservation of every interpretive nuance. Some passages had been shortened too aggressively. The author explicitly approved a targeted restoration, not another broad paraphrase.

Pre-restoration backup:

- `latex/IEEE-Conference/build/revision-backups/main-before-insight-restoration-2026-10-16.tex`

### Restored information

Exactly ten text regions were changed relative to that backup:

1. Restored the rationale that the target crop size matches the model input size.
2. Made the 640-pixel input explicit in the throughput protocol, without repeating the GPU name.
3. Kept both distinct limits on relative decrease: it is neither domain-shift magnitude nor a causal effect of pavement texture, lighting, or location.
4. Restored that complexity summaries describe the evaluated models, retaining the GFLOPs computational-estimate distinction.
5. Restored the source-result qualification that rankings describe one run per model, not statistically resolved differences or intrinsic superiority.
6. Restored both the Fig. 2 image-selection method and the fact that its panels are not paired observations of the same scene. Documentation confirms the median-based selection: `docs/progress/2026-10-09-panel-domain-D3-D4.md`, item 1, records three images per domain nearest the median image statistics, including the Indonesian V4 selections. No experiment or figure-generation code was opened to establish this.
7. Restored the explicit limit that overlap-box counts do not establish a causal benefit from adding D70/D80 labels. The distinction from unique-object matches and formal false-positive rates remains.
8. Restored the specific hypothesis that appearance and annotation differences may make patch transfer harder, alongside the statement that these were not tested as causes.
9. Restored the observational link between some inspected false positives and coarse, pitted target pavement, retaining the restriction to inspected examples and the absence of a demonstrated cause.
10. Retained both throughput boundaries: the measurement is hardware-specific, not an edge-device benchmark or a universal real-time guarantee.

The restoration adds approximately 104 whitespace-delimited LaTeX words. It does not restore unsupported nearby-frame speculation, strict one-corridor geography, a wholly untested-literature claim, or the inaccurate clean-success interpretation of Fig. 3's lower rows. The existing positive insights, conditional model recommendations, local-area and single-annotator limitations, and corrected Fig. 3 class/box descriptions remain.

### Verification after restoration

- All four table bodies are byte-identical to the pre-restoration versions.
- The relative-decrease equation, figure filenames/display widths, and full preamble/metadata are identical to the pre-restoration versions.
- All ten restoration anchors and the previously retained substantive result interpretations passed source-text checks.
- Final compile: 5 pages, 0 LaTeX errors, 0 overfull boxes, 0 undefined references/citations, and 0 multiply defined labels. There are 2 nonfatal underfull-box warnings, superseding the earlier count of 3.
- PDF text checks confirm the causal overlap limit, patch-transfer explanation, ranking qualification, false-positive/texture link, median image-selection method, and universal-throughput qualification.
- All five final rendered pages were visually inspected. Fig. 3 now floats to the top of page 5 before the conclusion and bibliography. References remain in the right column of page 5. No font, margin, figure-size, or additional placement changes were made for this restoration.
- Both final PDFs remain byte-identical.

Latest verification artifacts:

- `latex/IEEE-Conference/build/insight-restoration-2026-10-16/page-{1..5}.png`
- `latex/IEEE-Conference/build/insight-restoration-2026-10-16-compile.log`

Final PDF paths are unchanged. These checks preserve manuscript meaning and build integrity, not a new empirical validation of the experiments.

## Follow-up — Bounded YOLOv12n transfer interpretation

The author asked whether the paper should state that YOLOv12n was less affected by source-to-target differences. Added a bounded interpretation in the `Zero-Shot Transfer and Domain Shift` Results paragraph: YOLOv12n had the highest target mAP@0.5 (0.413) and smallest relative decrease (34.1%) among the five models, described as the strongest **observed** zero-shot transfer on this specific Indonesian target set. The Conclusion now briefly includes the smallest relative decrease as well. No universal “most robust to domain shift” claim or architectural causal explanation was added. Table values and evaluation scope are unchanged.

Build and visual checks after this two-paragraph prose addition: 5 pages, 0 LaTeX errors, 0 overfull boxes, 0 undefined references/citations, 0 multiply defined labels, 2 nonfatal underfull warnings. Both output PDFs are identical. The changed Results and Conclusion placements were visually inspected on pages 4–5. Final PDF paths remain `latex/IEEE-Conference/hasil/Paper_IEEE_Conference.pdf` and `latex/IEEE-Conference/hasil/main.pdf`; build log: `latex/IEEE-Conference/build/yolov12n-transfer-interpretation-2026-10-16.log`.

## Follow-up — Abstract alignment and reimplementation terminology

After a title/abstract/conclusion alignment check, the author approved two changes:

1. Abstract now ends the YOLOv12n result sentence with "the smallest relative decrease among the five models (34.1%)", aligning the abstract with the Results and Conclusion transfer interpretation. Abstract length remains within the IEEE-typical range (~183 words).
2. Replaced the unusual term "local reconstruction(s)" with "reimplementation" consistently in the Abstract, Methods (three spots), Limitations, and Conclusion ("Our YOLO-RD reimplementation..."). Related Work's verb "we reconstruct" was intentionally left unchanged.

Pre-edit backup: `latex/IEEE-Conference/build/revision-backups/main-before-reimplementation-wording-2026-10-16.tex`.

Verification: 5 pages, 0 LaTeX errors, 0 overfull boxes, 0 undefined references/citations, 0 multiply defined labels, 1 nonfatal underfull warning. All eight source-text changes verified present; "local reconstruction" no longer appears in the PDF. One automated PDF-text assertion initially failed only because text extraction split "YOLO-RD" across a line break ("YOLO- RD"); a hyphen-tolerant recheck confirmed the phrase is present and rendered correctly. Both output PDFs remain byte-identical. Build log: `latex/IEEE-Conference/build/reimplementation-wording-2026-10-16.log`.

## Follow-up — Split ratio mention

The author noted the missing split ratio. Added "divided at an approximately 70:20:10 ratio" to the existing split sentence in Source and Target Data. Verified against the counts already in the manuscript: 6,777/1,898/995 of 9,670 images equals 70.1/19.6/10.3 percent, hence "approximately". The 307-image target set needs no split because all images are used for zero-shot evaluation, which the manuscript already states. Pre-edit backup: `latex/IEEE-Conference/build/revision-backups/main-before-split-ratio-2026-10-16.tex`. Build: 5 pages, 0 errors/overfull/undefined/multiply-defined, 1 nonfatal underfull, PDF copies identical. Build log: `latex/IEEE-Conference/build/split-ratio-wording-2026-10-16.log`.

## Follow-up — Split method wording (author-confirmed)

The author confirmed the configured split ratio is exactly 70:20:10 and that the split preserves class proportions, pointing to `/mnt/Data/01_Akademik/Proposal TA/code/P3_split_data_6_classes.py` for details. That script was read and confirms: ratios 0.7/0.2/0.1, `MultilabelStratifiedShuffleSplit` (iterative-stratification) over a per-image binary label matrix, two-stage split (train vs temp, then val/test), seed 42, and YOLO folder/classes.txt/data.yaml export.

The Methods sentence was revised to: "The train, validation, and test splits were formed by multilabel stratified sampling at a 70:20:10 ratio, which preserves class proportions across splits, and contained 6,777, 1,898, and 995 images...". The hedge "approximately" was removed because the ratio refers to the configured split parameters, while the realized image shares (70.1/19.6/10.3) remain consistent with stratified sampling. Optional, not applied: a citation for multilabel stratification (Sechidis et al., 2011) if the author wants formal attribution.

Pre-edit backup: `latex/IEEE-Conference/build/revision-backups/main-before-split-method-wording-2026-10-16.tex`. Build: 5 pages, 0 errors/overfull/undefined/multiply-defined, 1 nonfatal underfull, new wording present in PDF, old wording absent, PDF copies identical. Build log: `latex/IEEE-Conference/build/split-method-wording-2026-10-16.log`.

## Follow-up — Methods data paragraph explanation and duplicate-note removal

The author asked what the four-class inventory passage means and whether the duplicate-annotation sentence was necessary. Explained: "corresponding" refers to the same train/val/test splits in the four-class label-set version (17,092/4,773/2,425 minus removed D70+D80 gives 14,351/3,996/2,035; test difference of 390 equals the 321 manhole + 69 patchy distractor count used in Table III); "images were retained" means only labels were deleted, so images containing only distractors become background; the 471 vs 4,555 (9.7-fold) comparison substantiates the effective-number class weighting; the duplicate-annotation sentence was evaluator bookkeeping, not an insight.

Per the author's decision, the sentence "One duplicate validation annotation was removed by the Ultralytics evaluator; the instance counts above describe the dataset inventory rather than the post-scan evaluation count." was removed. The four-class inventory, images-retained, and class-imbalance sentences were retained. Pre-edit backup: `latex/IEEE-Conference/build/revision-backups/main-before-duplicate-note-removal-2026-10-16.tex`. Build: 5 pages, 0 errors/overfull/undefined/multiply-defined, 1 nonfatal underfull, duplicate sentence absent from PDF, retained sentences present, PDF copies identical. Build log: `latex/IEEE-Conference/build/duplicate-note-removal-2026-10-16.log`.

## Follow-up — Punctuation preference

Per the author's request, changed `source--target evaluation` to `source-to-target evaluation` in the Introduction. Recompiled successfully: 5 pages, 0 LaTeX errors, 0 overfull boxes, 0 undefined references/citations; the two PDF copies remain identical.
