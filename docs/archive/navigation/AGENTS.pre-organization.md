## Rules

- Always ask permission before implementing anything
- write every experiment bug discussion, and solution applied at docs/progress/date-problem

## Navigation — find the file before exploring

This repo has many layered files. Before opening files at random:

1. Read **`docs/INDEX.md`** — the full context map: "looking for X → open Y" routing (§3), the contents of every folder (§4–§6), and the list of pitfalls you must know (§7).
2. For result numbers, start with **`docs/RESULTS_TABLE.md`** (tidy tables) and **`docs/RESULTS.md`** (raw log). Do not infer numbers from constants left behind in notebook cells — the authoritative run configuration is in `runs/*/experiments/*/args.yaml`.
3. Final experiment context for writing: **`docs/rangkuman-eksperimen-ta-v2.md`** (not v1).
4. Decision/bug history: **`docs/progress/`** (chronological).
5. Token-efficient TA proposal index: **`latex/PROPOSAL_TA.md`**.
6. Deep-research reference output: **`outputs/yolo-road-damage-references.md`** (+ `.provenance.md`).

After adding/moving a notebook, script, or main results folder, **update `docs/INDEX.md`** (see §9 there).

## LaTeX conventions

- **Build & result folder isolation**: Do not clutter the root directory with intermediate files.
  - Compilation intermediates must go into `build/`.
  - Final PDF output must be stored in `hasil/`.
- **How to compile**:
  ```bash
  cd latex/skripsi-telkom && bash compile.sh
  ```
  \*(Or manually: \`latexmk -pdf -outdir=build -interaction=nonstopmode main.tex &amp;&amp; cp build/main.pdf hasil/\`)\*

## Notebook conventions

- **1 cell = 1 logical unit** (1 output or none). Never merge multiple independent outputs into one cell.
- **Markdown style**:
  - Centered title with `[[ORCA_RICH_MD:18706e15e9a8a180d366292ffc2ba9b3:inline-html:%3Cdiv%20align%3D%22center%22%3E]]` for the project/notebook title.
  - Main sections: `## ***Section Name***` followed by `---`.
  - Subsections: `### ***Subsection Name***` (no horizontal rule).
  - No emoji, no decorative filler.
  - Short explanations scoped to the current group.
  - Write conclusions after running and inspecting the output, not before.

## Role

- you are a data science research expert.
