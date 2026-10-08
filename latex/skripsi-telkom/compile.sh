#!/usr/bin/env bash
set -e

# Pastikan berada di direktori skripsi-telkom
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

mkdir -p build hasil

echo "==> Mengompilasi naskah LaTeX (seluruh artefak sementara masuk ke build/)..."
latexmk -pdf -outdir=build -interaction=nonstopmode main.tex

echo "==> Menyalin hasil PDF ke folder hasil/..."
cp build/main.pdf hasil/main.pdf
cp build/main.pdf hasil/Draf_Skripsi_TA.pdf

echo "==> Kompilasi sukses! PDF tersimpan rapi di folder hasil/:"
echo "    [1] hasil/main.pdf"
echo "    [2] hasil/Draf_Skripsi_TA.pdf"
