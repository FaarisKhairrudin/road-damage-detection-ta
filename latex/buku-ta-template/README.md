# Template Buku TA FIF

Template LaTeX generik berdasarkan `TEMPLATE BUKU TA FIF.docx` yang diberikan pengguna pada 1 November 2026. Bab I–III telah diisi dengan draf penelitian Faaris Khairrudin pada 2 November 2026; Bab IV ditambahkan pada 4 November 2026. Kata pengantar dan ucapan terima kasih telah diisi. Abstrak, Bab V, dan lampiran belum disusun. Identitas, judul, pembimbing tunggal, kaprodi, dan tanggal draf mengikuti metadata aktif proposal di `latex/skripsi-telkom/main.tex`.

**Pedoman utama sebelum mengganti isi:** baca [PEDOMAN-PENULISAN.md](PEDOMAN-PENULISAN.md). Satu file ini menghimpun seluruh aturan penulisan, contoh LaTeX, checklist, dan arsip lengkap materi panduan sumber, sehingga petunjuk di dalam bab `.tex` dapat diganti tanpa kehilangan pedomannya.

## Pratinjau Bab I–III

Jalankan `bash compile.sh bab123` dari folder ini (atau `bash latex/buku-ta-template/compile.sh bab123` dari akar repositori). Keluaran khusus: `hasil/Bab_I-III_Buku_TA.pdf`. Berkas `bab123.tex` memakai tiga sumber bab yang sama beserta daftar otomatis dan bibliografi; bagian awal pribadi serta Bab IV–V tidak ikut dalam pratinjau.

Catatan penyesuaian dan sumber bukti: `../../docs/progress/2026-11-02-transformasi-bab-1-2-3-buku-ta.md`.

## Kompilasi

Dari akar repositori:

```bash
cd latex/buku-ta-template
bash compile.sh
```

Hasil: `hasil/Template_Buku_TA_FIF.pdf`. Semua berkas antara, log, dan render pemeriksaan disimpan di `build/`. Skrip dapat dipanggil dari direktori mana pun.

Gunakan **XeLaTeX**, `latexmk`, dan BibTeX. Font utama **Aptos**, heading **Aptos Display**, serta daftar pustaka **Times New Roman** (fallback TeX Gyre Termes). Pasang [Microsoft Aptos Fonts dari Microsoft](https://www.microsoft.com/en-us/download/details.aspx?id=106087), lalu jalankan `fc-cache` pada Linux. Font tidak dibundel dalam repositori. Font Aptos dan Aptos Display sengaja diwajibkan agar kompilasi tidak diam-diam menghasilkan tampilan berbeda.

Paket yang digunakan: `fontspec`, `babel`/`babel-indonesian`, `geometry`, `graphicx`, `amsmath`, `amssymb`, `array`, `tabularx`, `longtable`, `booktabs`, `xcolor`, `colortbl`, `float`, `ulem`, `enumitem`, `titlesec`/`titletoc`, `caption`, `fancyhdr`, `natbib`, `bibentry`, `hyperref`, dan `bookmark`. `IEEEtran.bst` disertakan dengan pemberitahuan lisensi aslinya.

Pemenggalan kata otomatis dimatikan agar mendekati Word dan menghindari pemakaian pola bahasa Inggris pada teks Indonesia. Bahasa/caption menggunakan locale Indonesia modern dari Babel. Karena itu template tidak memerlukan pola pemenggalan Indonesia tambahan. Line break tetap dapat sedikit berbeda antarversi font dan mesin tata letak.

## Berkas yang diedit

| Berkas | Fungsi |
| --- | --- |
| `main.tex` | Urutan halaman awal, bab, daftar pustaka, dan lampiran |
| `metadata.tex` | Semua identitas dan judul |
| `format.tex` | Margin, font, spasi, heading, caption, daftar otomatis, nomor halaman |
| `Cover.tex`, `Lembar-Pengesahan.tex`, `Lembar-Orisinalitas.tex` | Halaman identitas dan pengesahan |
| `Abstrak-Indo.tex`, `Abstract.tex`, `Kata-Pengantar.tex`, `Ucapan-Terima-Kasih.tex` | Halaman awal |
| `Pendahuluan.tex` sampai `Kesimpulan-dan-Saran.tex` | Bab I–IV berisi penelitian; Bab V masih panduan |
| `References.bib` | Pustaka penelitian yang digunakan pada Bab I–III |
| `Lampiran.tex` | Tempat lampiran |
| `gambar/` | Logo, contoh catatan kaki dari Word, serta tiga gambar yang digunakan kembali dari proposal |
| `PEDOMAN-PENULISAN.md` | Pegangan lengkap dalam satu file sebelum mengisi/mengganti naskah |
| `AUDIT-PANDUAN.md`, `PANDUAN-PENGISIAN.md` | Pemetaan aturan sumber, bukti penerapan, pemeriksaan isi yang masih diperlukan, dan panduan abstrak asli |
| `PERBANDINGAN-FORMAT.md` | Hasil perbandingan, pilihan format, dan batas kesamaan |

Gunakan `\chapter`, `\section`, dan `\subsection` untuk judul. Gunakan `\label`/`\ref` untuk rujukan, `\cite` untuk pustaka, `\caption` di atas tabel dan di bawah gambar. Jangan mengetik nomor bab atau nomor halaman daftar isi secara manual. Daftar pustaka hanya menampilkan sumber yang dipanggil oleh `\cite` atau contoh entri lengkap `\ContohPustaka`; tidak ada `\nocite{*}`. `\ContohPustaka{key}` memakai database `.bib` yang sama untuk menampilkan nomor dan entri lengkap di bagian panduan. Catatan kaki dibuat dengan `\footnote`, bukan superskrip manual. Label seperti `[Nomor kutipan]` di penjelasan format tetap merupakan placeholder, bukan penghitung.

Lembar orisinalitas memuat contoh redaksi dokumen sumber dengan identitas placeholder. Saat menulis naskah sebenarnya, pernyataan tersebut harus diperiksa dan disesuaikan oleh penulis. Kedua abstrak berisi placeholder empat bagian di bawah 200 kata. Petunjuk abstrak asli disimpan di `PANDUAN-PENGISIAN.md`; ganti placeholder dengan abstrak sebenarnya saat mengisi naskah.

`latex/skripsi-telkom/` tetap menjadi naskah lama dan tidak diubah. Template baru ini berdiri sendiri.

Rujukan gambar dan tabel menggunakan `Gambar~\ref{fig:...}` dan `Tabel~\ref{tab:...}`; persamaan menggunakan `\eqref{eq:...}`. Semua contoh gambar dan tabel memiliki rujukan di paragraf. Contoh bibliografi serta catatan kaki tetap berasal dari materi template, bukan hasil validasi sumber penelitian.

Caption tabel: hanya label yang bold, diikuti dua spasi, lalu judul sentence case bertitik. Setelah setiap tabel/gambar, sertakan paragraf arti dan tujuan objek seperti contoh yang tersedia. Lihat `AUDIT-PANDUAN.md` untuk batas penerapan aturan pada template.

## Bab IV dan keterlacakan hasil

`Hasil-Percobaan-dan-Analisis.tex` mengikuti struktur skenario, hasil, dan analisis. Sembilan tabel di `tabel/bab4-*.tex` serta kurva validasi dibangkitkan dengan `python3 scripts/paper/thesis_bab4_assets.py` dari akar repositori. Skrip hanya membaca artefak tersimpan, tanpa pelatihan/inferensi ulang. Perbandingan antarnegara menggunakan angka dibulatkan pada paper final yang telah dicocokkan dengan keluaran notebook. Sumber dan SHA-256 dicatat di `build/bab4-qa/evidence.json`. Gambar contoh target digunakan kembali dari paper tanpa perubahan.

Catatan audit Bab IV: `../../docs/progress/2026-11-04-penyusunan-bab-4-buku-ta.md`. Pratinjau `bab123` tetap hanya Bab I–III; baca hasil kompilasi penuh untuk Bab IV.
