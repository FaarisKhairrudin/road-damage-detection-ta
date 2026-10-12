# 2026-10-09 — Hapus judul dalam gambar + rapatkan vertikal plot Indonesia

## Permintaan
- Semua gambar bukti tidak perlu judul di dalam gambar, cukup gambarnya saja.
- Karakter citra tiap domain (D3/D4) dan plot per negara sudah aman, tidak diubah.
- Yang diperbaiki: deretan Indonesia mulai studi kasus kilau pagi (G1, G2, G3, dummy Fig3). Jarak vertikal antar baris model terlalu renggang, jarak horizontal antar kolom sudah aman.

## Yang dikerjakan
1. `scripts/paper/paper_figs_final_G.py`: `panel_fig` diganti dari `plt.subplots` + `tight_layout` ke `gridspec` manual (hspace 0,06, wspace 0,04, margin 0,01-0,99). Semua `set_title` dan `suptitle` dihapus. `savefig` pakai `pad_inches=0,02`.
2. `scripts/paper/paper_fig3_qualitative_v4.py`: perlakuan sama untuk dummy 4x4 (gridspec hspace 0,06, tanpa judul panel maupun suptitle).
3. Regenerate via background task (python3.12, inferensi 3 model): G1 2,8 MB (1830x1394), G2 2,5 MB, G3 2,0 MB, dummy 4,1 MB. Terverifikasi visual: tanpa judul dalam, baris rapat, label box (Long/Trans/Poth + skor) tetap ada sebagai bukti.
4. D3/D4 dan country tidak disentuh. DOCX tidak diregenerate. Teks draf rapih tidak diubah karena narasi kolom sudah ada di caption MD.

## Artefak
- `latex/IEEE-Conference/gambar/paper_figG1_glare.png`, `paper_figG2_correct.png`, `paper_figG3_predonly.png`, `paper_fig3_qualitative_v4_dummy.png`
