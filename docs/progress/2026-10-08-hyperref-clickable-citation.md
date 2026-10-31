# 2026-10-08 — hyperref clickable citations (IEEE-Conference)

## Problem
PDF citations/references (and fig/tab/equation cross-refs) were not clickable in `latex/IEEE-Conference/main.pdf`.

## Root cause
- `main.tex` loaded `cite`, `url`, etc. but never loaded `hyperref`, so pdfTeX wrote no `/Link` annotations.
- Two citation keys (`TODO_yolov12_primary`, `TODO_yolo26_primary`) had no `references.bib` records, so they rendered as `[?]` and could never link.

## Fix (no body-text wording changed)
- `latex/IEEE-Conference/main.tex`
  - Added `\usepackage[hidelinks]{hyperref}` after `\usepackage{url}` (after `cite`: correct load order) + explicit `\hypersetup{pdftitle/pdfauthor}`. (`pdfusetitle` was avoided: it expands IEEE's complex `\author` block and crashes with `TeX capacity exceeded`.)
  - Repointed `\cite{TODO_yolov12_primary,TODO_yolo26_primary}` to `\cite{tian2025yolov12_primary,sapkota2025yolo26_primary}`.
  - Marked the two stale bibliography TODO comments as DONE (comment-only change).
- `latex/IEEE-Conference/references.bib`
  - Replaced disputed `tian2026yolov12` (claimed NeurIPS 2026 — contradicts verified 2025 arXiv record) with `tian2025yolov12_primary` = Tian/Ye/Doermann, arXiv:2502.12524 (verified live via arXiv API, 2025-02-18, v1).
  - Replaced `sapkota2025yolo26` with `sapkota2025yolo26_primary` = Sapkota et al., arXiv:2509.25164 (verified live via arXiv API; dedicated YOLO26 architectural paper — better primary source than the retitled v4 YOLO27-overview record 2510.09653 flagged in outputs/yolo-road-damage-references.md).
  - Cross-checked against `latex/refference/` (no YOLOv12/YOLO26 PDFs there) and `outputs/yolo-road-damage-references*.md`.

## Verification
- `bash compile.sh` (latexmk -> build/, copy to hasil/): success, 4 pages, 682,782 bytes.
- `build/main.log`: zero undefined-citation warnings, no fatal errors.
- `hasil/main.pdf` via pypdf: 27 Link annotations (25 internal cite/ref links + 2 arXiv URI actions), 9 outline entries; `pdfinfo` shows Creator `LaTeX with hyperref`, correct Title/Author metadata.
- `hidelinks` = links work but print black, IEEE-submission safe.

## Note
The old wrong-year `tian2026yolov12` key is gone; any other file still citing it will need the same repoint (none found in main.tex).

## Update 19:55 — restore author block
- Working copy had dropped the 2nd author vs committed HEAD. Restored two-author block per user confirmation:
  Faaris Khairrudin (faariskhairrudin@student.telkomuniversity.ac.id) + Gamma Kosala (gammakosala@telkomuniversity.ac.id), School of Computing / Telkom University (italic, as in committed version).
- Title style: plain `Gamma Kosala` (no `Dr.`), per official IEEE conference template (`IEEE-conference-template-062824.tex`: `Nth Given Name Surname`; HOWTO examples all plain names — titles/degrees don't go in conference author blocks).
- Recompiled clean; PDF Author metadata now `Faaris Khairrudin and Gamma Kosala`; links intact.

## Update — float stacking fix (formatting only, no content changed)
- Symptom: page with Fig.1 + Tables II/III/IV back-to-back looked cramped (all floats `[t]`, long captions, no float separation).
- Changes (main.tex only):
  - All 6 tables `[t]` -> `[!htbp]` so LaTeX may place them here/bottom, not force all to column tops.
  - Both `figure*` `[t]` -> `[!t]`.
  - Preamble: `\floatsep 10pt`, `\textfloatsep 12pt`, `\intextsep 10pt` breathing room.
  - Shortened caption tails only (e.g. dropped repeated `Table~\ref` self-reference); body sentences untouched. One accidental mid-edit deletion of the ablation table was restored verbatim.
- Result: compiles clean (5 pages, no undefined refs), 26 link annots intact, Tables II+III now sit side-by-side with breathing room per visual render check.

## Update — IEEE template compliance (conference_101719.tex comparison)
Reference: `/home/varys/Downloads/conference-latex-template_10-17-19/Conference-LaTeX-template_10-17-19/conference_101719.tex`.
Already compliant: documentclass, author block, maketitle->abstract->keywords order, caption above tables / below figures, label-after-caption, BibTeX style, untouched margins/fonts.
Fixed (wording/numbers unchanged, notation only):
1. Abstract: `mAP@0.5` -> `mAP at IoU 0.5` + first-use definitions (mean average precision, intersection-over-union). No `@` symbols left in abstract.
2. `Figure~\ref{fig:qual-surface}` at sentence start -> `Fig.~\ref`.
3. Equation now referenced: `Equation~\eqref{eq:relative-drop}` with toggle-guarded `tab:core-transfer` mention.
4. First-use definitions: average precision (AP), non-maximum suppression (NMS), frames per second (FPS), giga floating-point operations (GFLOPs).
5. Table header `mAP@.5`/`mAP@.5:.95` -> `mAP@0.5`/`mAP@0.5:.95`.
Table format verdict: booktabs without vertical rules is IEEE-acceptable and better than the template's `|c|c|` example; footnotes with `*` + scriptsize explanation present on both marked tables.
Result: clean compile, 5 pages, 29 link annots, no undefined refs.

## Update 2026-10-12 — float distribution overhaul (formatting only)
- Symptom: pages 1-3 all-text while ALL floats piled onto pages 4-6 ("gambar/tabel nggak di tempatnya").
- Root cause: float declarations lived at their prose locations deep in section Results; LaTeX may never place a float before its declaration point, so pages 1-3 got pure text and the queue dumped onto the tail.
- Fixes (no wording changed):
  1. Preamble: relaxed float fractions (topfraction/dbltopfraction 0.9, textfraction 0.07, floatpagefraction 0.75) + counters topnumber 3 / dbltopnumber 2 / totalnumber 5.
  2. Single-column floats -> [!htbp] (merged ablation/overlap table, Fig 2 domains, UMAP).
  3. Declaration moves: Table I (table*) before \section{Results}; Fig 1 before \subsection{Country...}; Fig 3 before \subsection{Target Error...} — earliest legal points so they can top earlier pages.
- Result: 6 pages, 0 overfull boxes, 0 errors. Distribution: p3 = Table I+II; p4 = Fig1+Table III+IV; p5 = Fig2+Table V; p6 = Fig3. Mentions stay at/before their floats.

## Update 2026-10-15 — Params/GFLOPs audit & correction (Table I)
- User requested full number audit of main.tex tables vs repo sources. ALL mAP/F1/overlap/inventory/epochs/train-time/FPS numbers verified correct (see conversation audit vs runs/ CSVs, per_country_all.json, zs_per_class_metrics.csv, dataset_split_summary*.csv, experiments/*/results.csv).
- ONLY defect found: Params/GFLOPs column in Table I carried the disputed RESULTS_TABLE.md values, contradicted by fused logs (RESULTS.md) and by direct recomputation.
- Recomputed from final best.pt weights (fused summary, Ultralytics 8.4.177, 640px, sys.path including code/models for custom modules): v8n 3.007M/8.1, v12n 2.558M/7.3, v26n 2.376M/5.3, v8pd 2.468M/7.7, yolo_rd 7.086M/12.8. Archived: runs/rdd_yolov8n_local/model_complexity.json; script: scripts/audit_model_complexity.py (LSP-confirmed clean).
- main.tex changes: Table I Params/GFLOPs cells updated (2.57->2.56, 2.51->2.38, 2.46->2.47; GFLOPs 8.2->8.1, 7.5->7.3, 5.9->5.3, 12.9->12.8); dagger footnote now cites the recompute protocol + JSON artifact; prose IV-A updated (5.9->5.3 GFLOPs lowest, 2.46->2.47 M lowest params, 12.9->12.8 highest). Rankings in prose remain valid.
- note.md §3 marked RESOLVED with pointer to artifact; RESULTS_TABLE.md still carries old values (flagged for separate reconciliation).
- Cleanup: user's disk was full from audit installs; removed .venv-audit, system torch/torchvision/ultralytics + 16 nvidia-* packages, freeing ~3.2 GB (354 MB -> 3.5 GB free).
- Recompiled: 6 pages, 0 errors, Table I renders with corrected values.

## Update 2026-10-15 (2) — citation expansion review + first addition (Bučko)
- Reviewed outputs/yolo-road-damage-references.md + .provenance.md against current cite set (13 cited / 14 bib; dai2017deformable orphan).
- Wrote review proposal: latex/IEEE-Conference/draft/citation-addition-proposal.md — 15 ready BibTeX blocks in 4 tiers with exact insertion points.
- New papers verified today: finder2024wtconv (arXiv API, ECCV 2024), li2025dife (OpenAlex W4414432319, IEEE TCSVT 36(3):3466-3480), sapkota2025yoloreview (OpenAlex W4400266963, AI Review 58(9)).
- IMPLEMENTED (user go-ahead): added bucko2022computer to references.bib + new sentence in main.tex §II-A ("Bu{\v{c}}ko et al. \cite{bucko2022computer} likewise annotated manhole covers as a pothole-like class in urban pothole detection."). Compiles clean, 6 pages, ref renders as [8]; bbl has 14 bibitems.
- Still NOT added (awaiting decision): Tier 1 (yang2021simam, han2020ghostnet, wang2020eca, finder2024wtconv), Tier 2 (lin2023dardd, li2025dife), Tier 3 (maeda2018road, arya2020grddc, arya2022crddc2022), Tier 4 optional.
- PDF library downloads into latex/refference/: 12_GhostNet, 13_ECA-Net, 14_SimAM, 15_WTConv, 17_Maeda2018, 18_GRDDC2020, 19_CRDDC2022, 20_YOLO_review_AIReview (all valid sizes). 16_Pothole_Sensors_Bucko2022.pdf is BROKEN (1.8KB HTML, PMC/mirror blocked) — needs manual download or different mirror.

## Update 2026-10-15 (3) — REVERT §II-A/§II-B citation additions (author request)
- Author judged the added §II-A/§II-B citations ("aneh") and supplied the desired text verbatim; reverted both subsections exactly:
  - §II-A: first sentence back to \cite{Arya2024846} + \cite{arya2021deep}; restored the five separate sentences (Shi_2026 / Matouq / N-RDD2024 / open question); REMOVED the condensed "Manhole covers and road patches..." sentence and the "Bučko et al. further report..." sentence.
  - §II-B: \cite{Wu2023,Li2024,Shi_2026} (dropped han2020ghostnet/wang2020eca/yang2021simam); "Conversely, YOLO-RD \cite{Wang2025} prioritizes..." (dropped finder2024wtconv and restored cite to after YOLO-RD).
- Result: 6 pages, 0 errors, 14 bibitems.
- Bib entries now ORPHANED (present in references.bib, not cited => absent from PDF): maeda2018road, arya2020grddc, arya2022crddc2022, lin2023dardd, li2025dife, han2020ghostnet, wang2020eca, yang2021simam, finder2024wtconv (+ pre-existing dai2017deformable). Keep or prune pending author decision.
- Still cited/kept: bucko2022computer (Introduction \cite{matouq2024ai,bucko2022computer,Shi_2026}) and Shi_2026.
- PDF library additions in latex/refference/ (12–15, 17–20) retained; 16_Pothole_Sensors_Bucko2022.pdf still broken (1.8KB).

## Update 2026-10-15 (4) — Bučko placement decided (§II-A only, option B)
- Author reviewed my placement draft (recommended §IV-G for max scientific value; alternatives §II-A grouped or merged with Matouq sentence). Author chose the zero-word §II-A group option.
- Applied: §II-A sentence "However, prior image-based pothole detectors often suffer from false alarms caused by visually similar non-damage surface features." now ends with \cite{bucko2022computer}. No wording changed.
- Rationale recorded: Bučko's unique content (reflections, rain spots, low-visibility dark areas) also matches the §IV-G error-case paragraph, but §IV-G clause was declined to save space. Revisit if a line is available later.
- Rejected option (C): merging into the Matouq sentence would misattribute Matouq's claim to Bučko.
- Verified: 6 pages, 0 errors, 14 bibitems; Bučko renders as [4] in §II-A.
- Open: 9 orphan bib entries (maeda2018road, arya2020grddc, arya2022crddc2022, lin2023dardd, li2025dife, han2020ghostnet, wang2020eca, yang2021simam, finder2024wtconv) + dai2017deformable — keep or prune, still undecided.

## Update 2026-10-15 (5) — float placement fix: figure sizes + [!htbp]
- Symptom reported by author: figures/tables far from their mentions; one figure seemed to occupy a whole page.
- Diagnosis:
  1. `paper_figD4_domains.png` is PORTRAIT (1278x1849, aspect 0.69) placed at \columnwidth => ~5.1in tall, nearly two-thirds of a column; hard to place.
  2. `paper_figG_cases_4x4.png` square (1056x1053) at \columnwidth => ~3.5in.
  3. Two-column floats (`figure*`, `table*`) can ONLY be placed at a page top in LaTeX two-column mode (no h/b), so they always land at a page top, away from the mention. Official IEEE guidance also says: place figures/tables at top or bottom of columns, avoid the middle.
- Applied (formatting only, no wording changed):
  - class_examples 0.72 -> 0.62 \textwidth; country_examples 0.70 -> 0.58 \textwidth; domain 1.0 -> 0.75 \columnwidth; target-cases 1.0 -> 0.80 \columnwidth; umap 1.0 -> 0.85 \columnwidth.
  - target-cases figure, transfer table, umap figure: [!t] -> [!htbp] (allows mid-column placement).
- ATTEMPTED then REVERTED: `placeins`/\FloatBarrier barriers — aborted because `placeins.sty` is NOT installed in this TinyTeX and the compile died with "File `placeins.sty' not found" + Emergency stop (the hasil/ PDF was stale at that moment). All \FloatBarrier/placeins lines removed; verified clean.
- Verified after revert: clean compile (0 fatal, 0 overfull), 6 pages. Caption locations: Fig.1 + Fig.2 captions on p4 (mentions on p3), Fig.3 caption and mention both on p5. No stray \FloatBarrier left.
- Remaining option not taken (needs author decision): convert fig:country-examples from figure* to single-column [!htbp] for guaranteed proximity, or install the tiny placeins package for strict per-subsection barriers.

## Update 2026-10-15 (6) — placeins tested with A/B measurements; barriers rejected
- Author approved installing placeins. Installed via `tlmgr update --self` + `tlmgr install placeins` (kpsewhich confirms ~/.TinyTeX/texmf-dist/tex/latex/placeins/placeins.sty).
- A/B test results (same body text, only \FloatBarrier placement varied):
  | config | pages | float proximity | whitespace |
  |---|---|---|---|
  | no barriers | 6 | Fig1/Fig2 caption p4 (mention p3); Fig3 same page | p4=36 lines |
  | barriers on 9 headings | 7 | mentions reflowed onto p4 => same page as captions | p3=31, p6=38 |
  | barriers on 2 headings | 7 | mention p3, captions p4 | p4=24, p6=21 |
  | barriers removed again | 6 | Fig1/Fig2 caption p4 (mention p3); Fig3 same page as mention | p4=36 |
- Conclusion: \FloatBarrier did NOT move floats closer; it pushed TEXT down (page 3 emptied to 31 lines), i.e. it bought "same page" by adding a blank page and gaps. Rejected.
- Final state: placeins remains INSTALLED but the \usepackage and all \FloatBarrier calls are removed (verified 0 occurrences). Compile clean, 0 fatal, 0 overfull, 6 pages.
- Remaining real levers (author decision): (a) convert fig:country-examples from figure* to a single-column [!htbp] so it can sit mid-column; (b) regenerate paper_figD4_domains.png (portrait 0.69 aspect) as a landscape montage; (c) accept IEEE-standard <=1 page gap.

## Update 2026-10-15 (7) — FINAL float layout (fig:country-examples converted to single column)
- Author approved converting fig:country-examples from `figure*` (two-column, top-only) to `\begin{figure}[!htbp]` with `width=\columnwidth`. This is the only way a previously-top-only float can sit near its text.
- Final measured layout (6 pages, 0 fatal, 0 overfull, all \FloatBarrier removed):
  | float | first mention page | caption page | gap |
  |---|---|---|---|
  | Fig. 1 | 3 | 3 | 0 |
  | Fig. 2 | 3 | 4 | 1 |
  | Fig. 3 | 4 | 4 | 0 |
  | Table I | 2 | 3 | 1 |
  | Table II | 3 | 3 | 0 |
  | Table III | 3 | 4 | 1 |
  | Table IV | 2 (early forward-ref in Metrics) / 4 (main discussion) | 4 | 0 vs main discussion |
- Per-page density: p1 51, p2 60, p3 58, p4 49, p5 59 lines (p6 = references only). No orphan/empty float pages.
- Note: page-4 density improved from 36 -> 49 lines versus the pre-conversion state.
- Cosmetic leftovers (harmless, not removed): `\usepackage{float}`, `\usepackage{color}`, `\usepackage{soul}` are now unused (only referenced in a comment); placeins is installed but unused.

## Update 2026-10-15 (8) — references jumping to next page: root cause found and fixed
- Symptom (author): bibliography moved to a new page although a lot of space was still free, "like a forced page break".
- Root cause (measured, not guessed): the source contained BOTH
  1. a now-obsolete hack `\ifmaterialanalysis\newpage\fi` ("Start references in the next column so the queued target figure precedes them"), and
  2. `\IEEEtriggeratref{7}` ("Balance the bibliography columns on the final page").
  The real culprit was `\IEEEtriggeratref{7}`: it forces a column break at reference 7, which pushed refs [7]-[14] to page 6 while page 5 col 2 still had 508 pt of empty space.
- Pixel-level measurement (pdftoppm + PIL, so images count as content) confirmed: p5 col2 ended at y=244 (508 pt empty) and p6 col1 at y=273 (479 pt empty), p6 col2 fully empty.
- Fix: removed `\ifmaterialanalysis\newpage\fi` and `\IEEEtriggeratref{7}` (+ their comments).
- Result: pages 6 -> 5. Fill per column now: p1-p4 all ~full; p5 col1 full, col2 ends at y=467 (285 pt, normal end-of-document). 0 fatal, 0 overfull, 14 bibitems intact ([1]-[14], last = Cui 2019), all sections present.
- Float proximity unchanged and good: Fig.1 (mention 3 / caption 3), Fig.2 (3/4), Fig.3 (4/5), Table I (2/3), Table II (3/3), Table III (3/4), Table IV (early ref 2 / main discussion 4, caption 4).
- Note: removing only the \newpage had ZERO effect on layout (identical pixel fill) — that proved the triggeratref was the true cause.
