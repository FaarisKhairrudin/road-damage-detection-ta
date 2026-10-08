# Draft Paper Notes

This note records items that are intentionally provisional in the current conference-paper draft. The paper is written in scientific English, but several experimental and metadata details still need to be validated before submission.

## Current draft status

- `main.tex` contains a complete interim paper draft.
- `references.bib` contains the references currently cited in the draft.
- The draft uses the current six-class source-domain results.
- The draft uses the latest available `RDD-indo-v2` zero-shot result artifact.
- The draft is written conservatively where the evidence is incomplete.
- The paper currently reports descriptive comparisons; it does not claim statistical significance for differences between model mAP values.

## Critical items to validate

### 1. Target-domain dataset provenance

The draft calls the target data `RDD-indo-v2` and describes it as an Indonesian target set. Before making a specific claim about Bandung, verify and document:

- geographic location of image acquisition;
- whether the images are original primary data or adapted from an existing dataset;
- camera and recording details;
- image extraction interval or scene-selection procedure;
- annotation tool and annotation protocol;
- annotator and quality-control procedure;
- final number of images and instances after the last data revision.

The current repository contains 308 test images and 585 annotated instances for `RDD-indo-v2`, with six validation images. The older `RDD-Indonesia.v1i.yolov8` set contains different counts. Only one target-data version should be used in the final paper.

### 2. Final source-domain hardware protocol

The repository contains different hardware descriptions. The final paper should state one authoritative protocol for the source-domain throughput measurement, including:

- GPU model;
- GPU memory;
- PyTorch and CUDA versions;
- Ultralytics version;
- batch size;
- image size;
- warm-up iterations;
- number of timed iterations;
- whether preprocessing and postprocessing are included;
- whether the reported value is FPS, inverse latency, or an estimate.

FPS is hardware-dependent and should not be presented as a universal deployment speed.

### 3. YOLO-RD profiling discrepancy

The current artifacts report different YOLO-RD values. The main result table currently uses:

- 7.09M parameters;
- 12.9 GFLOPs;
- 189.4 FPS.

Some JSON/log artifacts report slightly different parameter and GFLOP counts and a substantially different FPS estimate. Re-run or select one canonical profiling protocol, then update the paper, `docs/RESULTS_TABLE.md`, and this note consistently.

### 4. Target zero-shot result artifact

The paper currently uses the latest file:

```text
runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v2/domain_gap.csv
```

The older artifact under:

```text
runs/rdd_yolov8n_local/evaluation/zero_shot_indonesia/
```

uses a different target set and produces different values. Do not mix the two result versions in the final manuscript.

### 5. Model reconstruction statement

YOLOv8-PD and YOLO-RD are reconstructed implementations. Before submission, confirm that:

- the architecture descriptions in the paper match the actual implementation;
- the reconstruction differences from the original papers are documented;
- the model names clearly indicate that these are reproduced implementations when appropriate;
- the final results are not presented as exact replications of the original papers.

### 6. Statistical robustness

The current main experiments use a deterministic single seed. If computation allows, repeat the main training with multiple seeds and report mean plus standard deviation or confidence intervals. If this is not feasible, keep the current limitation statement and avoid significance claims for model-to-model mAP differences.

### 7. YOLOv26 training protocol

The current YOLOv26n experiment uses the shared comparison configuration, but the latest experiment review confirms several implementation details:

- `optimizer="auto"` selected MuSGD in the recorded runs;
- the end-to-end loss branch activates ProgLoss through `E2ELoss`;
- the default DFL weight is 1.5 rather than the reported value of 6.0;
- the batch size is 16 rather than 128;
- STAL was not available in the evaluated Ultralytics versions.

The shared protocol is a deliberate fairness choice for architecture comparison. The result should therefore be described as a result under the common protocol, not as evidence that YOLOv26 is intrinsically inferior. The complete architecture-specific recipe remains a limitation.

## Figures

The current draft uses `flafter` and `stfloats` for float control. The current placement choices are intentionally conservative: single-column figures use `!ht` or `!b`, the wide source-domain table uses `table*[!b]`, and the remaining tables use `!ht`. The current draft uses:

- `gambar/class_examples.png`: six source-domain classes;
- `gambar/country_heatmap.png`: source-domain mAP50 by country;
- `gambar/domain_gap.png`: source versus zero-shot target mAP50.

The figures were copied from existing project artifacts. Before submission:

- check that all labels and captions are readable at IEEE column width;
- replace Indonesian-language flowchart artwork if a methodology figure is added;
- confirm image licensing and dataset citation requirements;
- consider replacing the current country heatmap with a vector-quality export;
- consider adding a target-domain ground-truth/prediction figure if the target-data provenance is confirmed.

## Tables

The current draft includes:

1. source-domain class distribution;
2. source-domain model comparison;
3. zero-shot source-versus-target comparison.

The distractor-ablation values are currently reported in prose to save space. A compact table can be added if the conference format allows it.

## Writing and formatting checks before submission

- Replace the placeholder author email.
- Confirm the official affiliation and department name.
- Verify that the PDF citation links are active after compiling with `hyperref`.
- Confirm the final paper title.
- Check whether the venue requires a specific page limit including references.
- Remove the word `interim` and the pending-validation language only after all critical items are resolved.
- Check all citations against the final reference list.
- Verify that every numerical result in the manuscript matches one canonical result table.
- Compile with `bash compile.sh` and check the final PDF page count.
- Inspect the PDF for overfull boxes, unreadable tables, and figure placement.
- Check whether the venue permits or requires an acknowledgment section.
- Confirm that the venue accepts the `stfloats` package; it is used only to improve placement of the wide source-domain result table in the draft.

## Recommended final scientific claims

The current evidence supports the following claims:

- YOLO-RD obtains the highest source-domain mAP50 among the compared models.
- YOLOv8-PD has the lowest parameter count and the highest current measured throughput.
- YOLOv12n provides the strongest current balance and the highest zero-shot target mAP50.
- Explicit distractor labeling does not show a statistically significant reduction in pothole false positives in the current ablation.
- All models experience a substantial source-to-target performance decrease.

The current evidence does **not** support the following stronger claims without further experiments:

- that distractor classes universally reduce false positives;
- that one architecture is statistically superior to all others;
- that the reported FPS applies to edge devices;
- that the reconstructed models exactly reproduce the original papers;
- that the zero-shot target set is representative of all Indonesian roads.
