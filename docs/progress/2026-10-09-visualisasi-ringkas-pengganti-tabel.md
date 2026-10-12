# 2026-10-09 — Visualisasi ringkas pengganti tabel (4 opsi)

## Permintaan
Buat visualisasi seperti distribusi/tabel gabungan yang lebih menarik dan hemat tempat di paper, merangkum beberapa variabel sekaligus. Buat dulu semua opsi, nanti user pilih. Ukuran compact tapi tetap enak dibaca. Cakupan data: sumber 6 kelas + per negara.

## Yang dikerjakan
Script baru `scripts/paper/paper_figs_summary.py` (murni matplotlib, tanpa inferensi, jalan di python3 biasa). Empat opsi berdiri sendiri:

1. `paper_figX1_dashboard.png` (300 KB) — dashboard 4 panel: (a) distribusi kelas train/test batang horizontal, (b) trade-off mAP50 vs FPS bubble (ukuran = params, warna = GFLOPs), (c) radar per-kelas 5 model, (d) batang per negara China/Jepang/India.
2. `paper_figX2_radar.png` (186 KB) — radar 5 model x 6 kelas, legend di bawah.
3. `paper_figX3_bubble.png` (82 KB) — bubble trade-off 4 variabel (mAP50, FPS, params, GFLOPs).
4. `paper_figX4_heatmap.png` (180 KB) — heatmap dua panel: (a) 5 model x 6 kelas mAP50, (b) 5 model x 3 negara, angka koma Indonesia.

Sumber angka: `docs/RESULTS_TABLE.md` test nc=6 + `domain_gap.csv` (fungsi `load_domain_gap` sudah tersedia untuk panel gap bila perlu).

## Perbaikan layout
- Dashboard panel (d): legend dipindah ke bawah (`bbox_to_anchor=(0.5,-0.13)`) supaya tidak menabrak judul.
- Radar: legend pindah ke bawah, `suptitle` turun ke y=0,98.
- Heatmap: `wspace` dinaikkan 0,34 ke 0,62 supaya colorbar panel (a) tidak menabrak label panel (b).
- Verifikasi visual keempatnya bersih.

## Status
Belum dimasukkan ke draf rapih (user mau pilih dulu). DOCX tidak disentuh.
