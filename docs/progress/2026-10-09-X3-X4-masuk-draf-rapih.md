# 2026-10-09 — X3 dan X4 masuk draf rapih

## Permintaan
User memilih dua dari empat opsi visualisasi ringkas: X3 (bubble trade-off) dan X4 (heatmap gabungan). Keduanya dimasukkan ke draf rapih sebagai pengganti/pendamping tabel.

## Yang dikerjakan
1. `draft-analisis-rapih.md` bagian Hasil Utama di Data Sumber: sisipkan `paper_figX3_bubble.png` + paragraf narasi empat variabel (FPS mendatar, mAP50 tegak, ukuran gelembung params, warna GFLOPs, RD kiri atas, PD kanan tercepat, 12n tengah seimbang).
2. Bagian Perbedaan Antar Negara Sumber: sisipkan `paper_figX4_heatmap.png` + paragraf narasi dua panel (kiri per kelas, kanan per negara, koma Indonesia, pola identik semua arsitektur berarti karakter data bukan model).
3. Daftar gambar diupdate: Gambar 9 = X3 bubble, Gambar 10 = X4 heatmap. Daftar tabel diberi catatan bahwa Tabel 4 diringkas Gambar 10 panel kiri dan Tabel 7 diringkas Gambar 10 panel kanan.

## Keputusan
- Tabel 4 (per kelas sumber) dan Tabel 7 (per negara) **dipertahankan** sebagai rujukan angka presisi, gambar berfungsi sebagai ringkasan visual. Tidak ada tabel dihapus.
- Tabel 3 (P/R/mAP50/F1 lima model) tetap sebagai tabel karena memuat presisi recall dan F1 yang tidak ada di gambar X3.
- X1 dashboard dan X2 radar tidak dipakai, file tetap ada bila sewaktu waktu dibutuhkan.
- DOCX tidak diregenerate.

## Artefak
- `latex/IEEE-Conference/draft/draft-analisis-rapih.md`
- `latex/IEEE-Conference/gambar/paper_figX3_bubble.png`, `paper_figX4_heatmap.png`
