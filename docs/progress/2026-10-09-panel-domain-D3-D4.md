# 2026-10-09 — Panel domain compact D3/D4 + update draf rapih

## Diskusi
- Gambar karakter per domain lama (4x4 acak, Bahasa Indonesia, banyak gap) diminta dibaguskan ala plot G: compact hemat tempat, judul simple Bahasa Inggris, dua varian 3x3 (3 domain sumber) dan 4x3 (tambah Indonesia).
- DOCX tidak diregenerate (instruksi hemat: MD dulu sampai final).

## Yang dikerjakan
1. Sampel baru bukan acak: 3 citra per domain paling dekat median statistik (brightness/saturasi/kontras/ketajaman). China 001779/000863/001890, Japan 011914/005925/008835, India 004602/002009/003007, Indo V4 0563/0435/0221 (dihitung python3.12 + cv2 karena python3 biasa tanpa cv2).
2. `scripts/paper/paper_figs_domains.py` (baru): `paper_figD3_domains.png` 3x3 (1,9 MB), `paper_figD4_domains.png` 4x3 (2,5 MB). Label domain vertikal kiri, judul simple. Fix layout: gridspec manual hspace 0.12 (tight_layout konflik), judul dipendekkan.
3. `draft-analisis-rapih.md`: bagian karakter citra diganti dua figur D3/D4 + analisis (China close up tajam, Japan wide gelap ramai, India buram berdebu, Indonesia beton terang berpori kontras). Daftar gambar diupdate (6a/6b). `fig_samples.png` lama tidak dipakai lagi di narasi.
4. Checker bersih (py_compile OK). DOCX tidak disentuh sesuai instruksi.

## Artefak
- `scripts/paper/paper_figs_domains.py`
- `latex/IEEE-Conference/gambar/paper_figD3_domains.png`, `paper_figD4_domains.png`
- `latex/IEEE-Conference/draft/draft-analisis-rapih.md`

## Catatan
- Citra kanan Indonesia V4 ada traffic cone merah yang mengganggu. Pengganti siap (peringkat 4-6: 0436/0437/0433) bila diminta steril.
- Sampel Indo V4 median-baru; sampel sumber dari manifest/image_stats lama (masih valid karena data sumber tidak berubah).
