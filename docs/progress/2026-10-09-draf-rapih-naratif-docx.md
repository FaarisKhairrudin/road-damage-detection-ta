# 2026-10-09 — Draf analisis rapih naratif + DOCX + Fig3 dummy

## Diskusi
- Draft lama terlalu teknis (penuh path file dan kode) sehingga sulit dibaca. Diminta tulis ulang sebagai narasi halus laporan akhir tanpa em dash dan tanpa titik koma, tetap lengkap dengan tabel gambar analisis dan concern.
- Setelah draf jadi diminta format angka Indonesia (koma desimal) karena versi pertama menulis 0661 dan minus 463 persen.
- Laporan DOCX dipindah ke folder yang sama dengan MD yaitu `latex/IEEE-Conference/draft/`.
- Fig3 memakai 7 nama Merge-1 dummy dari user. Ketujuh file dan label ketemu di V4.

## Yang dikerjakan
1. `latex/IEEE-Conference/draft/draft-analisis-rapih.md` (baru): narasi 11 bagian dari ringkasan sampai kesimpulan, 11 tabel, 8 gambar yang masing-masing dianalisis (gap domain, collapse per kelas, kualitatif dummy, bukti proxy vs overlap, heatmap negara, contoh citra, statistik, UMAP). Tanpa em dash dan tanpa titik koma. Angka format koma Indonesia.
2. Gambar disalin ke `latex/IEEE-Conference/gambar/`: `fig_fp_overlap.png`, `fig_percountry.png`, `fig_samples.png`, `fig_stats.png`, `fig_umap.png` plus 3 paper fig yang sudah ada. Link markdown relatif `gambar/nama.png` karena MD dan gambar beda folder (draft vs gambar).
3. `scripts/paper/paper_fig3_qualitative_v4.py` (baru): GT vs v12n/RD/PD untuk 4 citra dummy default (0453/0497/0566/0572), argv 6 untuk tambah 0571/0554. Harus run dengan `python3.12` karena ultralytics hanya ada di situ. Output `paper_fig3_qualitative_v4_dummy.png` 3,7 MB.
4. `scripts/paper/make_docx_rapih.py` (baru): konversi MD rapih ke `latex/IEEE-Conference/draft/laporan-analisis-rapih.docx` (TNR, spasi 1,5, justify, heading hitam). Hasil 7,6 MB dan 15 halaman, render LibreOffice diverifikasi per halaman.
5. `scripts/paper/make_docx_v4.py`: OUT dipindah ke folder draft, rewrite dengan type Any agar lolos pyright, regenerate terverifikasi 41 paragraf dan 4 tabel dan 12 heading hitam.

## Artefak
- `latex/IEEE-Conference/draft/draft-analisis-rapih.md`, `laporan-analisis-rapih.docx`, `laporan-analisis-v4.docx`, `draft-analisis-hasil.md` (teknis, tetap ada)
- `latex/IEEE-Conference/gambar/paper_fig1-3*.png`, `fig_*.png`
- `scripts/paper/paper_figs_v4.py`, `paper_fig3_qualitative_v4.py`, `make_docx_v4.py`, `make_docx_rapih.py`

## Tindak lanjut
- Kurasi kilau final tiba lalu ganti DUMMY_STEMS dan hapus label DUMMY.
- Sinkron `main.tex` ke angka V4.
- Opsional evaluasi subset pagi vs sisa V4 yang terkontrol.
