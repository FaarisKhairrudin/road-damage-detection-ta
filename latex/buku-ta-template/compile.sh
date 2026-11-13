#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
mkdir -p build hasil
if [[ "${1:-}" == "bab123" ]]; then
  latexmk -xelatex -outdir=build/bab123-output -interaction=nonstopmode -halt-on-error -file-line-error bab123.tex
  cp build/bab123-output/bab123.pdf hasil/Bab_I-III_Buku_TA.pdf
  printf 'PDF: %s/hasil/Bab_I-III_Buku_TA.pdf\n' "$DIR"
  exit 0
fi
latexmk -xelatex -outdir=build -interaction=nonstopmode -halt-on-error -file-line-error main.tex
cp build/main.pdf hasil/Template_Buku_TA_FIF.pdf
printf 'PDF: %s/hasil/Template_Buku_TA_FIF.pdf\n' "$DIR"
