# IEEE Conference Paper — Formatting Rules (Must Remember)

> Distilled from the official IEEE template
> (`conference_101719.tex`, Conference-LaTeX-template 10-17-19).
> This file is a checklist for our paper (`main.tex`). When in doubt, the template wins.

## 1. Document Setup (Do Not Alter the Design)

- Use `\documentclass[conference]{IEEEtran}`.
- **Never alter** margins, column widths, line spaces, or text fonts
  (no `geometry`, `fullpage`, `savetrees`, font-size hacks).
  The odd-looking head margin is deliberate — the paper is one part of
  the proceedings, not a standalone document.
- Extra packages are allowed **only if they do not change the layout**.
  Safe in our paper: `cite`, `amsmath`, `booktabs`, `graphicx`, `url`,
  `hyperref` with `hidelinks`, `float` (for `[H]`).
- Funding footnote (if any) needs `\IEEEoverridecommandlockouts` + `\thanks{}`.
  If there is no funding, comment that line out.

## 2. Title

- **No symbols, special characters, footnotes, or math** in the title
  (critical: they break IEEE Xplore metadata).
- Do not use sub-titles — Xplore does not capture them.
- Capitalize normally, except short words (a, an, and, as, at, but, by,
  for, in, nor, of, on, or, the, to, up) unless first/last word.
- "using" rule: if "that uses" can replace "using", capitalize the U.
- Line breaks (`\\`) may balance long title lines.

## 3. Authors and Affiliations

- Minimum **one** author; the class is designed for **up to six**.
- Order: **left to right, then down** — this is the citation/indexing order.
- Never list names in columns or group them by affiliation.
- **Plain names only**: no `Dr.`, no degrees, no `1st/2nd/3rd` prefixes
  (those in the template are placeholders, not formatting).
- Keep affiliations succinct — do not split departments of the same
  organization.
- Format: `\IEEEauthorblockN{Name}` + `\IEEEauthorblockA{affiliation}`,
  authors separated by `\and`.

## 4. Abstract and Keywords

- **No symbols, special characters, footnotes, or math** in the abstract.
  In practice: write `mAP at IoU 0.5`, not `mAP@0.5`.
- Define abbreviations in the abstract, then define them **again** at
  first use in the body text.
- Keywords go in the `IEEEkeywords` environment.

## 5. Sectioning and Headings

- Do not number headings manually — LaTeX does it.
- Two head types: **component heads** (Acknowledgment, References —
  not topically subordinate) and **text heads** (hierarchical I, II, A, B…).
- Only introduce subheads if there are **at least two** sub-topics.
- Spelling: **"Acknowledgment"** (American, no `e` after `g`).
- Put sponsor acknowledgments in the unnumbered first-page footnote.
- **Remove all template guidance text** before submission, or the paper
  may not be published.

## 6. Abbreviations and Acronyms

- Define each abbreviation **at first use in the text**, even if defined
  in the abstract.
- Never define: IEEE, SI, MKS, CGS, ac, dc, rms.
- No abbreviations in the title or headings unless unavoidable.

## 7. Units

- SI (MKS) primary; English units only as secondary in parentheses.
- Never combine SI and CGS (e.g. amperes + oersteds).
- Spell out units in text ("a few henries", not "a few H").
- Zero before decimals: `0.25`, not `.25`. Use `cm³`, not `cc`.

## 8. Equations

- Number consecutively; keep compact (solidus `/`, `exp`, exponents).
- Italicize Roman symbols, **not** Greek. Long dash for minus.
- **Punctuate equations** as part of the sentence (comma/period).
- Define every symbol before or immediately after the equation.
- Reference with `\eqref{eq}`, never `Eq. (1)` or hard-coded `(1)`.
  Only at sentence start: `Equation (1) is …`.
- Use `align` or `IEEEeqnarray` — **never `eqnarray`**.
- `subequations` increments the main counter even with no numbers shown.
- No `\nonumber` inside `array`.

## 9. Figures and Tables

- Place at the **top or bottom** of columns — never in the middle.
  Large items may span both columns (`figure*`, `table*`).
- **Figure captions below** the figure; **table heads above** the table.
- Insert each float **after** it is cited in the text.
- Always write **`Fig.`**, even at the start of a sentence
  (never `Figure` in running text).
- Use soft references (`\ref`, `\eqref`) — never hard-coded numbers.
- `\label` must come **after** `\caption` (a `\label` before the caption
  picks up the wrong counter).
- Figure labels: 8 pt Times. Axis labels use words ("Magnetization"),
  units in parentheses ("Temperature (K)"), never bare units or ratios.
- Our tables use `booktabs` (`\toprule/\midrule/\bottomrule`, no vertical
  rules) — cleaner than the template's `|c|c|` example and fully
  IEEE-acceptable. Keep one consistent style across all tables.
- Table footnotes use letters/symbols with a `\scriptsize` explanation
  under the table.

## 10. Citations and References

- Number citations **consecutively** in brackets: `[1]`, `[2]`.
- Sentence punctuation **follows** the bracket: `…systems [1], [2].`
- In-text: `as in [3]` — not `Ref. [3]` or `reference [3]`.
  Only at sentence start: `Reference [3] was the first …`.
- List **all authors** unless six or more — never truncate with `et al.`
  (there is no period after `et`).
- Unpublished work → `unpublished`; accepted work → `in press`.
- Capitalize only the first word of a paper title (plus proper nouns).
- Translation journals: English citation first, then the original.
- If BibTeX is used, the `.bib` files must be submitted with the paper.
- `i.e.` = "that is"; `e.g.` = "for example".

## 11. Footnotes

- Numbered separately, superscript.
- Placed at the bottom of the column where cited.
- Never in the abstract or reference list.

## 12. Common Language Mistakes (from the template)

- `data` is plural. `non` is a prefix, join it (`nonlinear`).
- Vacuum permeability subscript is **zero**: $\mu_{0}$, not letter `o`.
- US punctuation: commas/periods go **inside** quotation marks only for
  complete thoughts/titles; otherwise outside.
- A graph inside a graph is an **`inset`**, not "insert".
- `affect`/`effect`, `complement`/`compliment`, `discreet`/`discrete`,
  `principal`/`principle`, `imply`/`infer` — do not confuse.
- Never use `essentially` for `approximately`.

## 13. Pre-Submission Checklist for Our Paper

- [ ] Title/abstract free of symbols, math, footnotes.
- [ ] No `Figure` in running text (only `Fig.`); no hard-coded numbers.
- [ ] Every equation referenced at least once via `\eqref`.
- [ ] Every abbreviation defined at first body-text use.
- [ ] Every `\label` placed after its `\caption`.
- [ ] All authors listed (no `et al.`), first words of titles capitalized.
- [ ] All template guidance text removed.
- [ ] `.bib` files included with submission.
- [ ] PDF links work (we use `hyperref[hidelinks]` — invisible, IEEE-safe).
