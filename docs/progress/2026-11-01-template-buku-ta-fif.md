# Konversi template buku TA FIF dari Word ke LaTeX

## Permintaan dan izin

Pengguna meminta template LaTeX yang menyerupai `TEMPLATE BUKU TA FIF.docx`, memakai isi panduan/placeholder dan struktur berkas yang rapi seperti `latex/skripsi-telkom/`. Analisis dilakukan terlebih dahulu. Pengguna memberi izin implementasi dengan “gass” pada 1 November 2026, setelah usulan membuat folder terpisah `latex/buku-ta-template/` dijelaskan.

## Temuan

- Naskah lama menggunakan Computer Modern, lembar persetujuan dengan calon pembimbing, dan belum memiliki beberapa halaman awal buku TA.
- Word memakai tema Aptos/Aptos Display; margin 4/3/3/3 cm; isi 12 pt spasi 1,5; judul 14 pt; abstrak 11 pt; caption 9 pt.
- Panduan nomor halaman meminta Romawi kecil bawah tengah untuk bagian awal serta Arab kanan atas untuk isi, kecuali halaman pembuka bab.
- Render pertama memakai substitusi font dan menghasilkan 52 halaman, termasuk cover yang meluber. Aptos resmi diunduh dari Microsoft dan dipasang sebagai font pengguna; render ulang menjadi 38 halaman. Berkas Word tidak diubah.
- Template sumber mencampur data pribadi nyata, isi panduan, dan contoh. Identitas nyata diganti placeholder; isi panduan dan contoh tetap dipertahankan.

## Implementasi

- Membuat template mandiri `latex/buku-ta-template/`; naskah `latex/skripsi-telkom/` tidak diubah.
- Memusatkan metadata di `metadata.tex`, format di `format.tex`, dan urutan bagian di `main.tex`.
- Menyediakan sampul, pengesahan dua pembimbing dan kaprodi, orisinalitas, abstrak Indonesia/Inggris, pengantar, terima kasih, tiga daftar otomatis, lima bab, pustaka IEEE, dan lampiran.
- Mengekstrak logo serta tiga gambar contoh dari DOCX. Mengubah tabel contoh dan persamaan Fourier menjadi LaTeX asli dengan penomoran otomatis.
- Menyertakan `IEEEtran.bst` beserta lisensi aslinya. Font Aptos tidak dimasukkan ke Git; README menunjuk unduhan resmi.
- Menyediakan `compile.sh` dengan XeLaTeX, build di `build/`, dan keluaran final di `hasil/`.
- Mencatat perbedaan yang disengaja dan batas kesamaan di `PERBANDINGAN-FORMAT.md`.

## Masalah yang ditemukan dan perbaikan

1. `tocloft.sty` tidak tersedia. Upaya memasangnya ditolak oleh `tlmgr` karena pengelola paket perlu diperbarui. Implementasi diganti ke `titletoc` yang sudah tersedia; tidak memperbarui instalasi TeX global.
2. Konversi paragraf awal menambahkan blank line di lingkungan persamaan, menyebabkan `Missing $ inserted`. Blank line pada lingkungan persamaan dan tabel dibersihkan.
3. Gaya `IEEEtran.bst` tidak ditemukan oleh BibTeX di folder baru. Berkas gaya disertakan secara lokal dari distribusi CTAN dengan lisensinya.
4. NIP kaprodi sempat pindah ke halaman tambahan. Leading/jarak paragraf halaman pengesahan disesuaikan dan posisi heading diperbaiki; seluruh pengesahan kembali dalam satu halaman.
5. Daftar isi awal terlalu renggang dan berjumlah tiga halaman. Font/baseline disesuaikan dengan gaya daftar Word sehingga kembali dua halaman.
6. Daftar panduan yang terputus paragraf sempat mengulang huruf a. Menggunakan `enumitem` series/resume; bullet bertingkat untuk rincian masalah dan komponen sistem juga dipulihkan.
7. Beberapa overfull box kecil pada teks dan tabel jadwal diatasi melalui emergency stretch dan lebar kolom yang sesuai. Build final bebas overfull box.
8. Lingkungan TeX belum memuat pola pemenggalan Indonesia. Konfigurasi awal Babel memakai pola bawaan dan memberi peringatan. Solusi final memakai locale Indonesia modern dengan `hyphenrules=nohyphenation`, mendekati Word yang tidak memenggal kata otomatis. Toleransi paragraf disesuaikan agar justify tetap berada dalam margin. Build final bebas peringatan Babel.
9. Posisi heading dan nomor halaman diperiksa melalui koordinat PDF. Heading halaman awal berada pada y≈85 pt (3 cm); baseline header isi y≈42,2 pt (1,49 cm).

## Verifikasi

Kompilasi melalui `bash latex/buku-ta-template/compile.sh`, render PDF per halaman, inspeksi visual, pemeriksaan log, nomor halaman, daftar otomatis, placeholder identitas, dan batas bidang halaman. PDF final berjumlah 38 halaman, sama dengan jumlah halaman render Word setelah font tersedia; kesamaan jumlah halaman bukan jaminan identik per piksel. Tidak ditemukan overfull box, glyph hilang, atau rujukan tak terdefinisi. Hasil serta temuan terperinci ada di `latex/buku-ta-template/PERBANDINGAN-FORMAT.md`; intermediate pemeriksaan ada di `latex/buku-ta-template/build/qa/`.


## Penyempurnaan sitasi dan rujukan LaTeX

Pengguna menegaskan bahwa template harus memakai fitur LaTeX asli untuk sitasi dan rujukan objek. Audit menemukan versi pertama masih memiliki nomor gambar/tabel/persamaan dan contoh sitasi yang diketik manual di paragraf. Caption dan label sudah otomatis, tetapi itu belum mencukupi kebutuhan penyuntingan naskah.

Perbaikan:

- Mengganti nomor objek di paragraf dengan `\ref` dan `\eqref`; seluruh empat gambar, dua tabel, dan persamaan memiliki rujukan teks. Rujukan Tabel 2.1 yang tidak mempunyai objek di sumber diperbaiki agar menunjuk tabel keterkaitan yang benar.
- Mengganti contoh sitasi numerik manual dengan `\cite` serta contoh sitasi gabungan. Menghapus contoh klaim sel surya/LDR yang tidak mempunyai sumber sesuai database; menggantinya dengan demonstrasi sintaks dan placeholder kutipan.
- Menghapus sitasi Eason pada pernyataan format karena artikel tersebut bukan sumber aturan format. Contoh pustaka tidak diperlakukan sebagai bukti klaim penelitian.
- Menambahkan entri contoh dari bagian panduan Word ke `References.bib`. Contoh entri lengkap memakai `bibentry` melalui `\ContohPustaka` agar teks bibliografi dan nomor berasal dari database yang sama. Menghapus `\nocite{*}` agar daftar pustaka hanya berisi sumber yang dipanggil.
- Mengubah nomor superskrip contoh catatan kaki menjadi `\footnote` asli dengan ukuran isi 10 pt. Teks skematis “Nomor kutipan” tetap dipertahankan sebagai panduan.
- Build awal dengan `bibentry` menghasilkan anchor sitasi ganda pada xdvipdfmx. Anchor lokal contoh entri dinonaktifkan melalui macro `\ContohPustaka`; anchor tujuan sitasi hanya dibuat di daftar pustaka.

Verifikasi dilakukan melalui kompilasi ulang, pemeriksaan log, pemeriksaan label/sitasi, tautan PDF, dan render halaman yang berubah. Isi tetap berupa template, tanpa memasukkan hasil penelitian mahasiswa.

Hasil pemeriksaan penyempurnaan: PDF tetap 38 halaman; tujuh objek (empat gambar, dua tabel, satu persamaan) memiliki rujukan otomatis; sepuluh entri pustaka digunakan; empat belas tautan sitasi menuju halaman daftar pustaka yang benar; dua puluh satu catatan kaki asli. Kompilasi final tanpa warning, anchor ganda, overfull box, atau rujukan tak terdefinisi.


## Koreksi warna header tabel

Pengguna menunjukkan screenshot Word dengan latar header kolom hitam dan teks putih. Versi LaTeX sebelumnya masih memakai header putih dengan teks hitam; ekstraksi struktur tabel belum mempertahankan shading sel.

Perbaikan: kedua tabel isi di `Pendahuluan.tex` (keterkaitan tujuan dan jadwal) menggunakan `\rowcolor{black}`. Teks header dipusatkan pengaturan warnanya melalui macro `\HeaderTabel` di `format.tex` (putih dan tebal). Area tanda tangan pengesahan bukan tabel data berheader dan tidak diberi shading.

Verifikasi: kompilasi ulang serta render kedua tabel untuk memeriksa warna, keterbacaan, dan batas sel. Penomoran, caption, dan rujukan tetap otomatis.


## Audit ulang seluruh panduan dan koreksi caption/pembahasan objek

Pengguna menanyakan apakah semua aturan tertulis sudah diterapkan, khususnya label tabel bold, dua spasi, judul sentence case bertitik, dan penjelasan setelah tabel. Pemeriksaan mengonfirmasi versi sebelumnya belum sepenuhnya sesuai. Membaca dan menyalin materi sumber belum sama dengan memeriksa penerapan setiap aturan.

Seluruh paragraf panduan DOCX diperiksa ulang. Pemetaan aturan beserta status dan batas pengujiannya ditulis di `latex/buku-ta-template/AUDIT-PANDUAN.md`.

Perbaikan:

- Caption tabel kini hanya labelnya yang bold; judul regular, sentence case, bertitik. Separator dua spasi memakai lebar dua spasi font; tidak lagi label diikuti titik. PDF menunjukkan label `Aptos-Bold` dan judul `Aptos`.
- Kedua tabel dan keempat gambar isi diberi paragraf sesudah objek yang menjelaskan arti serta tujuan penggunaannya. Rujukan sebelum objek tetap memakai `ref` otomatis.
- Persamaan contoh diberi penjelasan bentuk dan tujuan selain definisi konstantanya.
- Kedua abstrak diubah dari dinding panduan menjadi placeholder empat bagian, font 11 pt, tanpa sitasi, di bawah 200 kata dan empat item kata kunci. Instruksi abstrak asli dipindahkan ke `PANDUAN-PENGISIAN.md`.
- Footnote diperiksa terhadap panduan: font 10 pt, nomor otomatis, indent baris pertama 1,8 em, lanjutan rata kiri, serta judul sumber contoh miring.
- README, perbandingan, dan INDEX diperbarui. PDF menjadi 39 halaman karena penjelasan objek; jumlah halaman tidak dipaksakan menyamai sumber.

Tidak mengklaim seluruh syarat isi penelitian telah terpenuhi: keselarasan tujuan-pengujian-kesimpulan, mutu bahasa naskah final, validitas kutipan, dan minimal lima sumber ber-ISBN/ISSN harus dinilai setelah placeholder diganti. Sejumlah materi panduan sumber masih berupa kalimat panjang; aturan bahasa tiga baris tidak dijamin untuk seluruh materi contoh.

Hasil verifikasi audit: kedua abstrak masing-masing 59 dan 61 kata termasuk heading/kata kunci; kedua label tabel bertipe Aptos Bold dan judul Aptos Regular; celah label-judul terukur 3,658 PDF pt, sesuai dua spasi font caption. Enam objek tabel/gambar memiliki rujukan sebelum dan penjelasan setelah. Empat belas tautan sitasi tetap menuju daftar pustaka. PDF final 39 halaman, tanpa overfull box, rujukan tak terdefinisi, peringatan pada pass kompilasi akhir, atau teks di luar halaman. Render akhir diperiksa termasuk tabel, abstrak, gambar, footnote, dan halaman lanjutannya.
