# Brief T1 — YOLO lightweight road-damage models

## Task
Write `outputs/.drafts/yolo-road-damage-references-research-models.md`.

## Context
TA compares 5 nano-scale YOLO models on N-RDD2024 Asia subset (6 classes: D00/D10/D20/D40 + D70 manhole/D80 patchy): YOLOv8n (baseline), YOLOv8-PD (Zeng 2024 reconstruction), YOLO-RD (Wang 2025 reconstruction), YOLOv12n, YOLOv26n. Source test mAP50: RD 0.661, v12n 0.654, v8n 0.648, PD 0.646, v26n 0.625. Zero-shot Indo-v3: v12n 0.309 best. Already have: Zeng2024, Li2024 (RDD-YOLO), Wang2025 (YOLO-RD), Wu2023 (YOLO-LWNet), tian2026yolov12, sapkota2025yolo26, matouq2024ai, redmon2016you.

## Objective
Find 7-10 candidate papers: lightweight YOLO variants for road damage (YOLO-LWD/Shi 2026, YOLO-LWNet follow-ups, YOLOv8-PD/RDD-YOLO/YOLO-RD originals, YOLOv11/YOLO-NAS/RT-DETR as non-YOLO comparator, official YOLOv8/v12/v26 reports). Prioritize 2022-2026, RDD2022/N-RDD2024 evaluations with mAP/F1 numbers.

## Instructions
- Use paper search and web search with varied terms (min 3 distinct queries). Prefer abstracts, HTML, official docs, metadata. Full-text only for 1-2 key papers.
- If PDF parsing fails, continue from abstracts/metadata and mark PDF parsing as blocked.
- For each candidate record: title, authors, venue+year, DOI/arXiv ID + URL, 2-4 sentence findings with key numbers, 1 sentence "fits TA section X because Y", BibTeX entry, duplicate-vs-existing flag.
- Record exact search terms used at top of file.
- No invented sources, numbers, or URLs.

## Deliverable structure
Search terms, candidate list (with above fields each), rejected/duplicates, open questions.
