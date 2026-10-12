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
