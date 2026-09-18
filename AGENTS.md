## Rules

- Always ask permission before implementing anything

## LaTeX conventions

- **Isolasi folder build & hasil**: Jangan mengotori root direktori dengan file perantara.
  - File perantara kompilasi wajib masuk ke `build/`.
  - File output PDF final wajib disimpan di `hasil/`.
- **Cara kompilasi**:
  ```bash
  cd latex_skripsi/skripsi-telkom && bash compile.sh
  ```
  *(Atau manual: `latexmk -pdf -outdir=build -interaction=nonstopmode main.tex && cp build/main.pdf hasil/`)*

## Notebook conventions

- **1 cell = 1 logical unit** (1 output or none). Never merge multiple independent outputs into one cell.
- **Markdown style**:
  - Centered title with `<div align="center">` for the project/notebook title.
  - Main sections: `## ***Section Name***` followed by `---`.
  - Subsections: `### ***Subsection Name***` (no horizontal rule).
  - No emoji, no decorative filler.
  - Short explanations scoped to the current group.
  - Write conclusions after running and inspecting the output, not before.

## Role

- you are a data science research expert.

