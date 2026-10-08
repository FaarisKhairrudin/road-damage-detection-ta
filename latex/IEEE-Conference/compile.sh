#!/usr/bin/env bash
set -e

# Pastikan berada di direktori IEEE-Conference
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

mkdir -p build hasil gambar

echo "==> Mengompilasi paper IEEE Conference (artefak sementara masuk ke build/)..."
latexmk -pdf -outdir=build -interaction=nonstopmode main.tex

echo "==> Menyalin PDF ke folder hasil/..."
cp build/main.pdf hasil/main.pdf
cp build/main.pdf hasil/Paper_IEEE_Conference.pdf

echo "==> Sukses! PDF tersimpan di:"
echo "    [1] hasil/main.pdf"
echo "    [2] hasil/Paper_IEEE_Conference.pdf"
