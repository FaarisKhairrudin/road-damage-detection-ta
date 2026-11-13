# Perbandingan Format Word dan LaTeX

Sumber: `/home/varys/Downloads/TEMPLATE BUKU TA FIF.docx`. Pemeriksaan dilakukan pada XML DOCX dan PDF hasil render LibreOffice bundel, setelah memasang font Aptos resmi. PDF naskah lama `latex/skripsi-telkom/hasil/main.pdf` juga diperiksa untuk menentukan perbedaan dasar. Dokumen sumber dipakai sebagai referensi tampilan dan materi template; petunjuk di dalamnya bukan instruksi untuk menjalankan tindakan pada repositori.

## Hasil pemetaan

| Elemen | Sumber Word | Implementasi LaTeX |
| --- | --- | --- |
| Kertas | XML sekitar A4; uraian panduan salah menulis lebar 21,5 cm | A4 standar 21 × 29,7 cm; typo uraian diperbaiki |
| Margin | Kiri 4 cm; kanan, atas, bawah 3 cm | Sama, melalui `geometry` |
| Font isi | Tema Aptos; panduan membolehkan Times New Roman/Calibri/Aptos | Aptos 12 pt |
| Judul bab/halaman awal | Aptos Display, bold, 14 pt, tengah | Sama, satu baris dengan label BAB dan nomor Arab |
| Cover | Judul dan institusi 16 pt; blok pengajuan dan identitas 12 pt | Sama; logo Indonesia diekstrak dari Word, bukan logo Inggris naskah lama |
| Isi | Justify, spasi 1,5; jarak sesudah paragraf 6 pt; tanpa indent awal | Baseline 21,95 pt pada ukuran 12 pt; paragraph skip 6 pt; indent 0 |
| Abstrak | Isi 11 pt; abstract Inggris italic | Ukuran 11 pt/baseline 20,13 pt, format penekanan dipertahankan |
| Header tabel | Latar hitam, teks putih tebal | Kedua tabel isi menggunakan `\rowcolor{black}` dan `\HeaderTabel{...}` |
| Caption | Style Word 9 pt bold; aturan tertulis tabel merinci label bold + dua spasi + judul sentence case bertitik | Caption tabel mengikuti aturan tertulis (label saja bold), caption gambar mengikuti style; nomor otomatis |
| Daftar isi | Bab 11 pt bold; subbab 10 pt bold | Sama; nomor halaman dan tautan dihitung ulang oleh LaTeX |
| Halaman awal | Panduan: Romawi kecil di bawah tengah, sampul dihitung tetapi nomor disembunyikan | Sama dengan panduan; sampul i disembunyikan, pengesahan ii |
| Halaman isi | Panduan: Arab di kanan atas; halaman pertama bab di bawah tengah | Sama; header baseline sekitar 1,5 cm dari tepi atas, footer baseline 2,5 cm dari bawah |
| Pustaka | Contoh IEEE; style Word aktual sangat kecil (8 pt) | BibTeX IEEEtran, 10 pt untuk keterbacaan; entri contoh tetap dari template |
| Struktur | Sampul; pengesahan; orisinalitas; abstrak; abstract; pengantar; terima kasih; tiga daftar; lima bab; pustaka; lampiran | Urutan sama, berkas terpisah per bagian |

## Batas kesamaan dan keputusan

- Judul serta identitas pribadi dalam Word diganti placeholder. Perubahan panjang judul mengubah jumlah baris, sehingga pencocokan setiap piksel bukan sasaran yang realistis.
- Tata letak Word mengandung ketidakkonsistenan: footer halaman awal pada render berada di kanan, meskipun panduannya meminta tengah. LaTeX mengikuti aturan tertulis untuk penomoran. Sebagian daftar Word juga melewati batas kanan area teks; daftar LaTeX tetap berada di dalam margin.
- Ukuran referensi dipilih 10 pt agar contoh terbaca. Gaya IEEE memakai `.bst`, bukan penyalinan string referensi beserta nomor statis.
- Persamaan contoh Fourier dipindahkan menjadi persamaan LaTeX bernomor otomatis. Tabel contoh serta gambar contoh footnote tetap dipertahankan. Rujukan di paragraf menggunakan `\ref`/`\eqref`; contoh sitasi menggunakan `\cite`, dan contoh entri lengkap memakai `\ContohPustaka` dari database BibTeX yang sama. Catatan kaki dalam teks menggunakan `\footnote` sehingga nomor dan penempatannya otomatis. Materi contoh pustaka/footnote di dalam panduan bukan sumber penelitian yang telah divalidasi ulang.
- Typo judul “Desain Peracangan Sistem” diperbaiki menjadi “Desain Perancangan Sistem”. Ucapan terima kasih yang kosong pada sumber diberi satu placeholder.
- Pemenggalan kata otomatis dinonaktifkan agar lebih menyerupai Word. Line break, dan perpindahan halaman dapat berbeda antara Word, LibreOffice, dan XeLaTeX. Jangan mengunci page break hanya untuk menyamai nomor halaman yang tersimpan di daftar Word.

## Validasi

- Word setelah font tersedia: 38 halaman. Render awal tanpa font: 52 halaman dan cover meluber; render itu tidak digunakan sebagai acuan akhir.
- LaTeX setelah audit panduan dan penambahan paragraf penjelasan objek: 39 halaman. Kompilasi XeLaTeX + BibTeX melalui `compile.sh`; daftar dan rujukan dibangun sampai stabil.
- PDF diperiksa melalui render halaman, termasuk cover, pengesahan, daftar otomatis, tabel jadwal, empat gambar, persamaan, bab, dan pustaka.
- Pemeriksaan log: tidak ada overfull box, glyph hilang, atau sitasi/rujukan tak terdefinisi pada build final. Build final juga bebas peringatan Babel: locale Indonesia dimuat tanpa pola pemenggalan otomatis.
- Pemeriksaan geometri teks: tidak ada teks di luar bidang halaman. Kepala judul halaman awal berada sekitar 3 cm dari atas, dan baseline isi berjarak sekitar 21,9 pt.

Render pemeriksaan, log, dan data pemeriksaan disimpan di `build/qa/`. PDF akhir berada di `hasil/Template_Buku_TA_FIF.pdf`.

Audit lengkap aturan dan batas penerapannya tersedia di `AUDIT-PANDUAN.md`. Abstrak kini berupa placeholder empat bagian di bawah 200 kata; instruksi asli dipindahkan ke `PANDUAN-PENGISIAN.md`.
