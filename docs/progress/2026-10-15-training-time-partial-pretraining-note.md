# 2026-10-15 — Compact explanation of custom-model training time

## Request

The author authorized a small addition explaining why YOLO-RD trained longest and whether limited pretraining in the custom architectures could be relevant. Keep the addition short and avoid implying that slow training proves slow or poor generalization.

## Evidence

Parsed the training cell (cell index 19) in the saved comparative notebooks, mapping transfer messages to the subsequent completion message and checkpoint run name:

| Notebook | Run | Transfer messages | Completed epochs | Hours |
| --- | --- | --- | ---: | ---: |
| 03_1 | yolov8n_class_weight | 319/355 items | 148 | 4.356 |
| 03_1 | yolov12n_class_weight | 640/691 items | 150 | 4.661 |
| 03_2 | yolov26n_class_weight | 606/708 items | 171 | 5.278 |
| 03_2 | yolov8_pd_class_weight | 164/541, followed by 541/541 items | 190 | 6.323 |
| 03_2 | yolo_rd_class_weight, earlier output | 84/519, followed by 519/519 items | 174 | 7.323 |
| 03_3 | yolo_rd_class_weight, final artifact-matching output | 84/519, followed by 519/519 items | 278 | 11.701 |

The custom initialization branch constructs the model from its YAML and calls `model.load(code/yolov8n.pt)`. The native branch starts from the model's corresponding pretrained checkpoint. These facts support partial pretrained transfer for the custom models, not training entirely from scratch.

Important interpretation: the initial custom transfer is 164/541 for PD and 84/519 for RD. The subsequent 541/541 and 519/519 messages reflect the trainer loading the already initialized custom model, not additional full COCO pretraining. Item counts are state-dictionary entries, not proportions of scalar parameters or of pretrained layers. Notebook model-list constants include stale batch sizes, so they are not used to revise run settings. Existing final `args.yaml` checks remain authoritative.

The final RD result matches the 278-epoch/11.701-hour CSV, not the earlier 174-epoch notebook output. No new experiment is run.

## Revisions

File: `latex/IEEE-Conference/main.tex`.

1. Added one Methods sentence:

   > Native models used pretrained checkpoints, while custom reconstructions loaded only compatible YOLOv8n weights.

2. Replaced the previous training-time sentence in Section IV-A with:

   > Training time ranged from 4.4 to 11.7 h, with YOLO-RD completing the most epochs (278). Limited pretrained-weight transfer may also have slowed training in the custom models, alongside computation and mixed-precision settings.

The two changes add roughly 30 words overall. There are no new tables, columns, footnotes, or metrics. Initialization is a possible contributor, not an isolated causal finding. The text concerns training cost and optimization, not inference throughput or a demonstrated generalization mechanism. Mixed-precision differences remain acknowledged because the native models use AMP and custom models do not.

Pre-edit copy: `latex/IEEE-Conference/build/revision-backups/main-before-initialization-note-2026-10-15.tex`.

## Verification

Compile completed successfully. `pdfinfo` confirms 6 pages, with 0 LaTeX errors, 0 overfull boxes, 0 undefined references/citations, and 0 multiply defined labels. PDF text confirms the initialization sentence, RD's 278 completed epochs, and the qualified partial-transfer explanation. The target figure remains on page 6 before References (caption y=244.93 pt, reference heading y=293.72 pt). Static comparison confirms both main tables are unchanged, exactly 27 net words were added, and no new em dashes or semicolons were introduced. `git diff --check` is clean.

Final PDF: `latex/IEEE-Conference/hasil/Paper_IEEE_Conference.pdf`.

## Follow-up: explicit custom-layer explanation

The author approved replacing the qualified transfer sentence with a more direct explanation of why custom layers reduce compatible pretrained-weight reuse:

> Custom layers allowed less pretrained-weight reuse than in the native models, which may partly explain the longer training of YOLOv8-PD and YOLO-RD.

This replaces one sentence in Section IV-A without adding a paragraph. The Methods initialization sentence and the 278-epoch observation are unchanged. Computation and AMP differences remain documented in Methods and Limitations. The wording does not claim that limited pretraining was an experimentally isolated cause of longer training, and does not attribute inference FPS to pretraining. Recompile succeeded. The PDF remains 6 pages, with 0 overfull boxes, 0 LaTeX errors, 0 undefined references/citations, and 0 multiply defined labels. PDF text confirms the approved replacement sentence is present and the old sentence is absent.
