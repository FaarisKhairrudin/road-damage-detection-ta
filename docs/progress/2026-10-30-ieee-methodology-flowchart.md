# Flowchart metodologi pada paper IEEE

## Diskusi dan persetujuan

Pengguna meminta penempatan flowchart penelitian pada branch `exp/zero-shot-indonesia`, lalu menyetujui penerapan dengan pesan "terapkan". Rekomendasi: paragraf pengantar dan flowchart di awal Section III (Materials and Methods), sebelum subsection A (Source and Target Data).

## Masalah yang diperjelas

- Diagram awal dapat terbaca seolah Mosaic diterapkan ke seluruh split. Augmentasi harus ditandai khusus training; validation dan test hanya menerima pemrosesan input.
- Jalur target harus menghubungkan akuisisi, anotasi, dan evaluasi zero-shot secara berurutan. Evaluasi target juga membutuhkan checkpoint hasil pelatihan source, tanpa fine-tuning.

## Solusi diterapkan

- Menambahkan pengantar, referensi otomatis, dan caption pada `latex/IEEE-Conference/main.tex`. Pengguna kemudian meminta satu kolom; implementasi akhir menggunakan `figure` dengan `width=\columnwidth`.
- Versi awal sempat menggunakan diagram TikZ. Pengguna kemudian meminta memakai gambar miliknya langsung; versi TikZ dibatalkan dan dependensi TikZ dihapus.
- Menyalin `/home/varys/Downloads/Blank diagram - Page 1.png` tanpa perubahan ke `latex/IEEE-Conference/gambar/methodology_workflow.png`, lalu memasangnya pada lebar satu kolom sesuai permintaan terbaru. PNG berukuran 3229 x 1995 piksel dan berlatar transparan, sehingga area luar diagram mengikuti latar putih PDF.
- Struktur gambar pengguna dipertahankan. Penjelasan bahwa Mosaic hanya untuk training tetap dicantumkan pada caption; naskah menjelaskan evaluasi target tanpa fine-tuning dan status reimplementasi model custom.
- Tidak mengubah angka hasil, konfigurasi eksperimen, atau analisis lain.

## Pemadatan pengantar dan caption

Setelah meninjau hasil satu kolom, pengguna menilai pengantar redundan dan terlalu panjang, lalu menyetujui pemadatan. Pengantar menjadi satu kalimat yang merujuk gambar: "Fig. 1 summarizes the overall experimental workflow." Nomor gambar tetap memakai referensi LaTeX otomatis. Caption dipadatkan menjadi "Experimental workflow. Mosaic augmentation is applied only to the source training split." Penjelasan tanpa fine-tuning tetap tersedia pada subsection data target dan evaluasi.

## Validasi

Kompilasi dengan `bash compile.sh` berhasil setelah pemadatan. Pemeriksaan visual halaman 2 memastikan gambar asli berada dalam satu kolom, setelah pengantar Section III dan sebelum III-A; caption tidak terpotong dan tidak ada tumpang tindih. Log kompilasi tidak memuat warning, referensi undefined, atau overfull box. Teks internal gambar menjadi kecil pada lebar satu kolom, sesuai pilihan pengguna mempertahankan gambar asli. Seluruh artefak kompilasi disimpan di `latex/IEEE-Conference/build/`; PDF akhir di `latex/IEEE-Conference/hasil/`.
