# Brief T3 — Imbalance, loss, distractor false positives, small objects

## Task
Write `outputs/.drafts/yolo-road-damage-references-research-loss.md`.

## Context
TA data: patchy_road only 672 instances vs 6.447 longitudinal (9.67x imbalance); pothole hardest class (mAP50 0.526-0.541); manhole easiest (0.82-0.85). Uses class-balanced weighting via Effective Number of Samples (Cui et al. 2019, beta=0.999). Ablation 6-class vs 4-class: no significant FP-rate reduction (z-test p>0.05), small pothole mAP cost. Bboxes predominantly small (median 1.69% image area). Already have: cui2019class, Zeng2024 (Focal/Mosaic), panboonyuen2025reg cited in proposal but missing from IEEE bib, Shi_2026/mandals claims about manhole annotation cited in proposal but missing.

## Objective
Find 7-10 candidate papers: Focal Loss, class-balanced loss, Generalized/Refined-GFL/REG, manhole-vs-pothole-vs-patch false-positive studies, explicit distractor/negative-class labeling studies, small-object detection and multi-scale mAP evaluation (mAP-s/m/l).

## Instructions
- Use paper search and web search with varied terms (min 3 distinct queries). Prefer abstracts, HTML, official docs, metadata. Full-text only for 1-2 key papers.
- If PDF parsing fails, continue from abstracts/metadata and mark PDF parsing as blocked.
- For each candidate record: title, authors, venue+year, DOI/arXiv ID + URL, 2-4 sentence findings with key numbers, 1 sentence "fits TA section X because Y", BibTeX entry, duplicate-vs-existing flag.
- Record exact search terms used at top of file.
- No invented sources, numbers, or URLs.

## Deliverable structure
Search terms, candidate list (with above fields each), rejected/duplicates, open questions.
