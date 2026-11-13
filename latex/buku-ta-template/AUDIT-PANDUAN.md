# Audit penerapan panduan buku TA FIF

Audit ulang 1 November 2026 mencakup seluruh paragraf panduan pada `TEMPLATE BUKU TA FIF.docx`, termasuk aturan format umum, gambar, tabel, persamaan, kutipan, catatan kaki, abstrak, dan isi tiap bab. Dokumen Word diperlakukan sebagai sumber rujukan format dan materi contoh. Aturan isi penelitian dibedakan dari aturan tata letak yang dapat diterapkan pada template.

## Aturan yang sudah diterapkan pada template

| Kelompok | Aturan sumber | Penerapan dan bukti |
| --- | --- | --- |
| Kertas dan margin | A4, satu sisi, kiri 4 cm, lainnya 3 cm | `oneside`, `openany`, dan `geometry` dalam `main.tex`/`format.tex` |
| Font dan paragraf | TNR/Calibri/Aptos 12 pt; justify; spasi 1,5; teks hitam | Aptos, baseline 21,95 TeX pt (sekitar 21,87 PDF pt), paragraf justify dan hitam. Selisih kecil akibat konversi satuan dicatat, tidak diklaim identik per piksel |
| Sampul | Simetris di tengah; judul bukan pertanyaan dan tanpa titik akhir | `Cover.tex` dan placeholder judul di `metadata.tex`; logo asli Word |
| Halaman awal | Romawi kecil bawah tengah; sampul tanpa nomor tercetak tetapi dihitung | `pagenumbering{roman}`, page style `awal`, sampul `empty` |
| Isi | Arab kanan atas; awal bab bawah tengah | Page style `isi`/`plain`; baseline header sekitar 1,49 cm dari atas, footer sekitar 2,5 cm dari bawah |
| Tabel: posisi | Caption di atas; nomor bab dan urutan | `caption` sebelum `tabularx`; `thetable` dan `label` otomatis |
| Tabel: nomenklatur | “Tabel 2.1” bold, dua spasi, judul sentence case, titik akhir | `labelfont=bf`, `textfont=normalfont`, separator `duaspasi`; kedua judul diperiksa. Nomenklatur tidak ditambah titik sebelum dua spasi |
| Tabel: header | Header hitam, huruf putih seperti sumber/screenshot | `rowcolor{black}` dan `HeaderTabel` pada kedua tabel isi |
| Tabel: pembahasan | Dirujuk sebelum/sesudah; setelah tabel menjelaskan arti dan tujuannya | Dua tabel memiliki rujukan sebelum tabel dan paragraf sesudah tabel yang menjelaskan isi serta kegunaannya |
| Gambar: posisi | Nomor dan caption di bawah, mengikuti bab | Empat gambar isi menggunakan `caption` di bawah objek, dengan `label` dan `ref` |
| Gambar: pembahasan | Dirujuk dekat objek; setelah gambar menjelaskan arti dan tujuan | Empat gambar memiliki rujukan serta paragraf penjelasan sesudah objek |
| Persamaan | Nomor bab/urutan; arti dan tujuan dijelaskan | `equation`, `label`, dan `eqref`; konstanta dijelaskan dan tujuan contoh deret Fourier diterangkan |
| Kutipan | Sitasi numerik; kutipan langsung bertanda petik; bahasa asing italic | `natbib`/`cite`; contoh kutipan langsung berupa placeholder bertanda petik dan miring, tanpa mengarang kutipan sumber |
| Pustaka | Format IEEE | BibTeX dengan `IEEEtran.bst`; nomor mengikuti urutan sitasi; contoh entri memakai database yang sama |
| Catatan kaki | Nomor superskrip; font lebih kecil (contoh 10 pt); baris pertama menjorok dan lanjutan dari kiri; judul miring | `footnote`, `footnotesize` 10/12 pt, `@makefntext` dengan indent 1,8 em, judul contoh dicetak italic |
| Abstrak | Maksimum 200 kata; font 11 pt; empat bagian; tanpa sitasi; maksimal enam kata kunci | Kedua halaman kini berupa empat bagian placeholder pendek, tanpa sitasi; empat item kata kunci huruf kecil. English abstract italic |
| Struktur | Halaman awal, lima bab, pustaka, lampiran | Berkas terpisah per bagian; tiga daftar dihasilkan otomatis |

## Hal yang harus diperiksa saat menjadi naskah penelitian

- Masalah, latar belakang, tujuan yang terukur, batasan beralasan, serta keselarasan pengujian dan kesimpulan baru dapat dinilai setelah isi penelitian ditulis. Template menyimpan panduan dan placeholder, bukan klaim bahwa penelitian telah memenuhi semuanya.
- Minimal lima sumber ber-ISBN/ISSN harus dipenuhi oleh pustaka penelitian yang benar-benar dibaca. Contoh sumber dari Word belum diverifikasi ulang dan tidak dianggap sebagai pemenuhan persyaratan penelitian mahasiswa.
- Batas 200 kata, jumlah kata kunci, kebenaran kutipan, dan penulisan asing perlu dicek kembali setelah placeholder diganti.
- Panduan sumber memuat kalimat panjang, salah ketik, serta contoh yang tidak selalu mengikuti nasihatnya sendiri. Materi panduan bab sebagian besar tetap dipertahankan; aturan bahasa seperti panjang kalimat maksimum tiga baris belum menjadi jaminan untuk seluruh teks panduan tersebut maupun naskah final.
- Teks orisinalitas merupakan contoh formulir beridentitas placeholder, bukan pernyataan faktual atas karya pengguna.
- Berat/jenis kertas, pencetakan satu sisi, dan kualitas cetakan harus dipastikan saat mencetak; berkas PDF tidak dapat menguji bahan kertas.

## Perbaikan yang dilakukan setelah audit ini

Versi sebelumnya belum memenuhi seluruh aturan: caption tabel masih seluruhnya bold, separator masih titik, judul jadwal masih title case, penjelasan setelah tabel/gambar belum lengkap, dan abstrak Indonesia berisi panduan panjang. Masalah tersebut diperbaiki. Panduan abstrak asli dipindahkan ke `PANDUAN-PENGISIAN.md` agar tetap tersedia tanpa melanggar bentuk contoh abstrak.

Keluaran setelah penambahan penjelasan menjadi 39 halaman. Jumlah halaman tidak dipaksakan sama dengan Word, karena penerapan panduan dan paragraf penjelasan lebih penting daripada mempertahankan page break contoh.

## Verifikasi

Kompilasi XeLaTeX/BibTeX sampai stabil; pemeriksaan log; pemeriksaan caption di PDF (label Aptos Bold, judul Aptos Regular, separator dua spasi); rujukan tujuh objek; tautan sitasi menuju daftar pustaka; hitung kata abstrak; render kedua tabel, empat gambar, abstrak, dan halaman yang berubah. Hasil teknis di `build/qa/validation.json`. Penilaian isi penelitian tetap berada pada daftar pemeriksaan di atas.
