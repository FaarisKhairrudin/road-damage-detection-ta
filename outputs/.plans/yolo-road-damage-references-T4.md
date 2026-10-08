# Brief T4 — Attention, lightweight conv, real-time efficiency

## Task
Write `outputs/.drafts/yolo-road-damage-references-research-efficiency.md`.

## Context
TA narrative: accuracy-first YOLO-RD (7.09M params, 12.9 GFLOPs, 189 FPS, deformable-conv + wavelet refinement) vs efficiency-first YOLOv8-PD (2.46M, 7.7 GFLOPs, 368 FPS, GhostNet + shared head) vs balanced YOLOv12n (2.57M, 7.5 GFLOPs, 319 FPS, R-ELAN + area attention). Modifications insert SimAM/CBAM attention and GhostConv in neck. Benchmarked on RTX 4070 SUPER 12GB, bs=1, imgsz 640. Already have: han2020ghostnet and woo2018cbam cited in proposal but missing from IEEE bib, dai2017deformable, Wu2023 (efficiency metrics), redmon2017/2018 and bochkovskiy2020yolov4 cited in proposal but missing.

## Objective
Find 7-10 candidate papers: SimAM, CBAM, ECA-Net attention originals; GhostNet/GhostConv; deformable convolutions/DCNv2/DCNv3; wavelet-based vision modules; YOLO evolution history (v1-v4, anchor-free decoupled head); EfficientDet family incl. Indonesian road study (hugo2025efficientdet); Params/GFLOPs/FPS benchmarking methodology for real-time detectors.

## Instructions
- Use paper search and web search with varied terms (min 3 distinct queries). Prefer abstracts, HTML, official docs, metadata. Full-text only for 1-2 key papers.
- If PDF parsing fails, continue from abstracts/metadata and mark PDF parsing as blocked.
- For each candidate record: title, authors, venue+year, DOI/arXiv ID + URL, 2-4 sentence findings with key numbers, 1 sentence "fits TA section X because Y", BibTeX entry, duplicate-vs-existing flag.
- Record exact search terms used at top of file.
- No invented sources, numbers, or URLs.

## Deliverable structure
Search terms, candidate list (with above fields each), rejected/duplicates, open questions.
