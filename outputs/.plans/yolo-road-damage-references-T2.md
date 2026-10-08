# Brief T2 — Datasets, benchmarks, domain gap

## Task
Write `outputs/.drafts/yolo-road-damage-references-research-domain.md`.

## Context
TA trains on N-RDD2024 Asia subset (India/China/Japan, 9.670 images, 24.290 instances) and zero-shot tests on primary Bandung data (RDD-indo-v3, 308 images). Measured gap: source mAP50 ~0.65 drops to ~0.23-0.31 (>50% relative drop). Per-country source variance: China ~0.89 >> Japan ~0.58 > India ~0.43. Indonesia absent from RDD2022. Already have: Arya2024846 (RDD2022), kaya2024nrdd2024, arya2021deep, hugo2025efficientdet cited in proposal but missing from IEEE bib, matouq2024ai.

## Objective
Find 7-10 candidate papers: RDD2022/CRDDC2022 challenge reports (incl. winning F1 0.770), N-RDD2024, crowdsensing/smartphone road datasets, Indonesian/Southeast-Asia road studies, cross-country degradation studies, domain shift / domain generalization / zero-shot / cross-domain object detection theory applicable to road damage.

## Instructions
- Use paper search and web search with varied terms (min 3 distinct queries). Prefer abstracts, HTML, official docs, metadata. Full-text only for 1-2 key papers.
- If PDF parsing fails, continue from abstracts/metadata and mark PDF parsing as blocked.
- For each candidate record: title, authors, venue+year, DOI/arXiv ID + URL, 2-4 sentence findings with key numbers, 1 sentence "fits TA section X because Y", BibTeX entry, duplicate-vs-existing flag.
- Record exact search terms used at top of file.
- No invented sources, numbers, or URLs.

## Deliverable structure
Search terms, candidate list (with above fields each), rejected/duplicates, open questions.
