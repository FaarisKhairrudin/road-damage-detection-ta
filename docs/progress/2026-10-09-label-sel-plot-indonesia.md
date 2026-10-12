# 2026-10-09 — Kembalikan label sel singkat plot Indonesia (judul besar tetap dibuang)

## Permintaan
- Jarak sudah pas dan rapat, jangan diubah.
- Judul besar di dalam gambar tetap dibuang.
- Tambahkan kembali penjelasan indeks singkat tiap baris dan kolom seperti sebelumnya (label sel).

## Yang dikerjakan
1. `scripts/paper/paper_figs_final_G.py` `panel_fig`: kembalikan `ax.set_title` per sel, format `GT {stem} n={jumlah}` untuk kolom GT dan `{Model} n={jumlah}` untuk kolom model. hspace dinaikkan sedikit dari 0,06 ke 0,18 supaya label tidak menempel gambar, top 0,96. Suptitle tetap tidak ada.
2. `scripts/paper/paper_fig3_qualitative_v4.py`: perlakuan sama untuk dummy, label `GT {stem} n={n}` dan `{title} n={n}`, hspace 0,18.
3. Regenerate background (python3.12, inferensi 3 model): G1 2,4 MB, G2 2,2 MB, G3 1,8 MB, dummy 3,5 MB. Terverifikasi visual keempatnya: label baris/kolom kembali, jarak tetap rapat, label box deteksi tetap ada.

## Catatan
- Judul besar seperti "Glare + porous texture..." dan "V4 failure cases (DUMMY ...)" tidak dikembalikan sesuai instruksi. Penanda DUMMY hanya tersisa di teks narasi draf.
- D3/D4 dan country tidak disentuh. DOCX tidak diregenerate.
