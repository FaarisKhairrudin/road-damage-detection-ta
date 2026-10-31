# 2026-10-12 — Opsi B: YOLO-RD 4-kelas masuk ablasi + overlap GPU run

## Temuan awal
- "YOLO-RD 5-kelas" tidak ada konsepnya; yang dimaksud user = run 4-kelas RD.
- Artefak RD 4-kelas ternyata SUDAH ada lengkap: `runs/rdd_4class_local/experiments/yolo_rd_4cls_class_weights/` (best.pt 14.6MB 9 Okt, args seed 42 / 300 epoch / batch 16, CSV test+val, summary.json, kurva, confusion matrix).
- Yang kosong: baris RD di `tab:ablation` + `tab:overlap` paper, dan baris overlap di CSV (8 baris, RD absen).

## Run overlap GPU (RTX 3050 6GB, python3.12, bg task b5377033e, exit 0)
- Skrip: inline turunan `scripts/fp_overlap_table.py` (conf=0.25, NMS 0.6, IoU match ≥0.5, 272 gambar, GT 321+69=390).
- Hasil: RD 6cls TRUE 3/390 (M 3/321, P 0/69, proxy 58, det M 0.8287 / P 0.5942); RD 4cls TRUE 2/390 (M 2/321, P 0/69, proxy 49).
- CSV `fp_overlap_6cls_vs_4cls_test.csv` kini 10 baris (runs/ gitignored — catat bila fresh clone).

## Angka ablasi RD (presisi penuh → tampil)
- RD 4cls test: Long 0.6989, Trans 0.6081, Allig 0.7149, Pothole 0.5824 → avg4 0.6511; macro-F1 0.6174, weighted 0.6289.
- RD 6cls 4-inti: 0.6331 (macro-F1 0.6129) → Δ avg4 **+0.0180** (terbesar), pothole +0.055 (0.527→0.582).
- Narasi "4 dari 4" → "5 dari 5"; "largest observed" v8-PD +0.0108 → RD +0.0180.

## Perubahan file
1. `main.tex`: Methods "five separate four-class models ... YOLO-RD" (hapus "no corresponding run"); prosa 0.0017–0.0180 + RD largest; `tab:ablation` +1 baris RD 0.6331/0.6511/+0.0180; `tab:overlap` +1 baris RD 3/2 + "five paired"; Limitations hapus "did not include YOLO-RD".
2. `draft-analisis-hasil.md` §4.3: tabel TRUE +2 baris RD; tabel pothole +RD +0.055; tabel agregat +RD 0.6331/0.6511/+0.0180 (macro 0.6129/0.6174/+0.005); bacaan "5/5, RD terbesar"; hapus "(YOLO-RD tidak punya run 4-kelas)".
3. `docs/RESULTS_TABLE.md`: tabel ringkasan/val/test/F1 4-kelas +baris PD + RD (Params/GFLOPs PD–RD = — tidak tercatat; FPS 130.4/94.3 estimate + footnote).
4. CSV overlap: +2 baris RD (verified GPU run 2026-10-12).

## Verifikasi PDF
- Compile sukses; cek isi: 0.6511=1, +0.0180=2, "five separate four-class"=1, "no corresponding four-class"=0, "0.0017–0.0180" render en-dash benar.
