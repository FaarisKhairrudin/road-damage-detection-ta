# X4 Per-Negara + Overall, Sampel GT Per-Negara, Kolom Tabel Utama

Tanggal: 2026-10-09

## Permintaan user
1. X4 heatmap: panel per-negara ditambah kolom **Overall**, panel per-kelas dibuang
   (user sudah hapus bagian bawahnya di draf), jadi X4 kini satu heatmap per-negara saja.
2. Sampel contoh per-negara: tambah gaya **Karakter Citra Tiap Domain** (3 citra per negara)
   dengan **label GT tipis** plus keterangan kelas.
3. Tabel **Hasil Utama di Data Sumber**: tambah kolom **Params (M)**, **GFLOPs**, **FPS**.

## Keputusan yang dikonfirmasi user
- X4: per-negara saja + kolom Overall (panel per-kelas dihapus dari gambar).
- Per-negara: **tambah file baru** `paper_fig_country_gt.png`, gambar lama
  `paper_fig_country_examples.png` tetap dipertahankan.
- Tabel: Params + GFLOPs + FPS.

## Perubahan kode
### `scripts/paper/paper_figs_summary.py`
- `fig_heatmap()` ditulis ulang: satu heatmap 5 model x 4 kolom
  (China n=180 / Japan n=705 / India n=110 / Overall n=995), cmap YlOrRd.
- Kolom Overall memakai `OVERALL[m]` (mAP50 test 6 kelas).

### `scripts/paper/paper_figs_country.py`
- Tambah `draw_gt_thin()` (lw=0.7, fontsize 4.5, pad 0.6) dan `country_gt_panel()`:
  3 citra tipikal per negara dari stem yang sama dengan D3, label baris vertikal.
- `main()` dapat flag `--gt-only` supaya panel GT bisa jalan tanpa ultralytics.
- Rapikan blocker lama: `patch_ultralytics()` tanpa loop, `list(m.predict(...))`,
  `zip(..., strict=True)`, urutkan import.

## Output
- `paper_figX4_heatmap.png` 81 KB (sebelumnya 180 KB, 2 panel)
- `paper_fig_country_gt.png` 1926 KB (baru)
- `paper_fig_country_examples.png` 2356 KB (regenerate, tetap)

## Draf `draft-analisis-rapih.md`
- Tabel Hasil Utama: header + 5 baris ditambah Params/GFLOPs/FPS, narasi diperluas
  (YOLO RD terbaik tapi terberat, YOLOv12n separuh parameter, PD paling ringan 2,46 M / 368,4 FPS).
- Bagian Perbedaan Antar Negara: gambar jadi `paper_figX4_heatmap.png` dengan narasi baru
  (kolom Overall di antara China dan Jepang), header tabel `Gabungan` -> `Overall`.
- Bagian Perbandingan Langsung: tambah gambar `paper_fig_country_gt.png` + narasi 3 baris.
- Daftar Gambar/Tabel dirapikan: nomor disusun ulang sesuai urutan kemunculan di badan draf,
  `fig_percountry.png` (sudah tidak dipakai) dikeluarkan dari daftar.

## Catatan
- `fig_percountry.png` masih ada di folder tapi tidak lagi dirujuk di draf. Bisa dihapus
  atau disimpan sebagai arsip.
- X1 dashboard dan X2 radar tetap tidak dipakai, file tetap ada.
