# 2026-11-02 — Transformasi proposal menjadi Bab I–III buku TA

## Otorisasi dan lingkup
Pengguna menyetujui penerapan pada `latex/buku-ta-template/` setelah rancangan disampaikan. Pengguna meminta membaca setiap bagian template/pedoman, mempertahankan format, dan melakukan penyesuaian minimal. Pengguna juga mengarahkan penggunaan LaTeX di `latex/skripsi-telkom/` untuk sitasi dan gambar.

Isi Bab I–III menggantikan teks petunjuk pada tiga berkas bab. Judul dan enam bagian Bab I dipertahankan; Bab II diisi lima kelompok teori; empat bagian awal Bab III dipertahankan lalu dilengkapi data, implementasi, dan protokol. Font, margin, spasi, gaya heading/caption, halaman awal, metadata, Bab IV–V, serta lampiran tidak diubah. Semua pedoman asal tetap tersedia dalam `PEDOMAN-PENULISAN.md`.

## Sumber dan pemeriksaan
- Proposal bertanda tangan: `latex/refference/103052300115_FAARIS_KHAIRRUDIN_signed.pdf`; indeks `latex/PROPOSAL_TA.md`.
- Sumber LaTeX proposal/pekerjaan sebelumnya: `latex/skripsi-telkom/` (beberapa isinya sudah berbeda dari PDF bertanda tangan; tidak disalin mentah).
- `latex/buku-ta-template/PEDOMAN-PENULISAN.md`, seluruh komponen `.tex`, `format.tex`, dan `compile.sh`.
- `docs/RESULTS_TABLE.md`, `docs/RESULTS.md`, `docs/rangkuman-eksperimen-ta-v2.md`, audit terbaru paper 2026-10-30, catatan editorial 2026-10-16, serta catatan GPU/provenance Oktober.
- PDF dan sumber paper IEEE; argumen sepuluh run final enam/empat kelas; notebook komparasi dan zero-shot; YAML arsitektur; inventaris split dan `model_complexity.json`.
- Hitungan ulang label target lokal: 307 berkas, 39 kosong, 502 anotasi. Pemetaan jumlah: D00 231, D10 132, D20 48, D40 70, D80 21; empat kerusakan 481.
- Tidak menjalankan ulang training/inferensi atau mengubah angka eksperimen.

## Rekonsiliasi dan batas klaim
1. **Data target:** catatan 8 Oktober dan INDEX lama merujuk ekspor v3/514 anotasi. `data/RDD-indo-v4/data.yaml` saat ini menyebut versi 4; README menyebut ekspor 9 Oktober 2026; hitungan aktual 502 cocok dengan paper dan audit terbaru. Bab III memakai metadata saat ini, bukan mengasumsikan versi dari nama folder. Rangkuman lama tidak ditimpa.
2. **GPU:** RTX 4070 SUPER pada log evaluasi menjadi dasar lingkungan FPS. Tidak mengklaim semua eksperimen berlangsung pada perangkat tersebut.
3. **Pembobotan:** effective-number beta 0,999; bobot dinormalisasi rata-rata satu dan diterapkan pada BCE klasifikasi. Tidak menyatakan Focal Loss aktif.
4. **Model:** PD/RD adalah rekonstruksi, transfer pralatih parsial; fusi RD menggunakan Upsample–Concat–Conv1×1. Skala nano tidak menyamakan kapasitas.
5. **AMP:** args enam kelas native=true, PD/RD=false; args empat kelas kelima model=true. Bab III mencatatnya agar perbandingan tidak disebut identik seluruh konfigurasinya.
6. **Validasi sumber:** 4.773 baris inventaris berbeda dari 4.772 anotasi validator akibat satu duplikat manhole. Keduanya dijelaskan, tidak dipilih diam-diam.
7. **Generalisasi:** seluruh lima model diuji tanpa fine-tuning; penurunan dihitung pada empat kelas yang sama. Selisih metrik bukan jarak distribusi atau ukuran kausal domain shift.
8. **Efisiensi:** GFLOPs adalah operasi per forward, bukan per detik. FPS berasal dari pre+inference+post validator, bukan benchmark perangkat edge.
9. **F1:** menggunakan P/R pada operating point yang memaksimalkan smoothed mean F1 di evaluated split, mengikuti audit version-tagged 2026-10-30. Tidak disebut threshold tetap/validation-selected.
10. **Ablasi:** lima arsitektur empat kelas tersedia pada args final. Analisis deskriptif single seed; tidak membawa p-value proxy lama. Overlap dihitung per kotak prediksi, bukan FP unik objek.
11. **Jadwal:** enam bulan dipertahankan sebagai rencana proposal, bukan tanggal realisasi buatan. Target awal ≥500 citra dibedakan dari 307 citra aktual.
12. Tidak memasukkan skor model ke Bab I–III; pembahasan hasil tetap untuk Bab IV.

## Sitasi dan gambar
- Pustaka disusun dari proposal dan bibliografi IEEE; narasi proposal digunakan ulang dengan batas klaim yang sama atau lebih sempit.
- Metadata tambahan dicek: https://arxiv.org/abs/1901.05555, https://arxiv.org/abs/2502.12524, https://arxiv.org/abs/2509.25164.
- YOLOv12 dicatat sebagai preprint, bukan `inproceedings` dengan venue arXiv. Tanggal akses sumber online dicantumkan.
- Halaman GhostNet mengikuti versi CVF 1580–1589 (https://openaccess.thecvf.com/content_CVPR_2020/html/Han_GhostNet_More_Features_From_Cheap_Operations_CVPR_2020_paper.html); tidak dicampur dengan penomoran penerbit lain.
- Gambar `arsitektur_yolov8_standar.png`, `distribusi_gambar.png`, dan `object_sample.png` disalin byte-identik dari folder gambar proposal, setelah inspeksi visual. Atribusi Li dkk. tetap pada gambar arsitektur. Diagram alur ditulis langsung di LaTeX sesuai pelaksanaan aktual.
- Caption daftar gambar arsitektur memakai versi pendek agar sitasi pada daftar gambar tidak mendahului sitasi teks utama.

## Masalah kompilasi dan solusi
- `\nobibliography*` untuk contoh bibliografi template berkonflik dengan entri IEEEtran yang memakai `BIBentryALTinterwordspacing`; muncul `Paragraph ended before \BR@c@bibitem was complete`. Pemanggilan itu dihapus dari main dan pratinjau karena tidak ada lagi contoh `\ContohPustaka` yang digunakan. Daftar pustaka biasa tetap melalui BibTeX/IEEEtran. Tidak mengubah format.tex.
- URL panjang Hugo diganti tautan DOI dari metadata yang sama. Judul pustaka dilindungi kapitalisasinya agar akronim tidak berubah.
- Artefak sementara yang sempat muncul akibat salah opsi `-outdir` pada pemanggilan langsung XeLaTeX dipindahkan ke build. Kompilasi akhir memakai compile.sh/latexmk dan tidak meninggalkan intermediate pada folder sumber.
- Float awal dapat menempatkan paragraf interpretasi sebelum gambar/tabel. Posisi `[H]` mengikuti contoh template agar penjelasan tetap sesudah objek.
- Paragraf batas interpretasi dipadatkan tanpa kehilangan batas klaim untuk menghindari halaman dengan satu baris sisa.

## Berkas keluaran dan reproduksi
- `Pendahuluan.tex`, `Tinjauan-Pustaka.tex`, `Perancangan-Sistem.tex`, `References.bib` pada folder buku.
- `bab123.tex` memuat tiga bab dari sumber yang sama, daftar isi/gambar/tabel, dan daftar pustaka. Tidak menduplikasi isi bab.
- `bash latex/buku-ta-template/compile.sh bab123` → `hasil/Bab_I-III_Buku_TA.pdf`.
- `bash latex/buku-ta-template/compile.sh` → PDF susunan buku lengkap; bagian di luar Bab I–III masih template.
- Cadangan tiga bab dan bibliografi sebelum perubahan: `build/sebelum-bab123-2026-11-02/`.
- Log dan render QA: `build/compile-bab123*.log`, `build/qa-bab123/`.

## Validasi
Pemeriksaan awal: 26 label, 52 pemanggilan ref/eqref, 15 sumber tersitasi, tidak ada label/sitasi hilang. Kompilasi serta pemeriksaan visual akhir dicatat setelah perbaikan tata letak.

### Hasil validasi akhir
- Kedua perintah `compile.sh` dan `compile.sh bab123` berhasil.
- PDF khusus Bab I–III: **34 halaman** (4 halaman daftar otomatis, 29 halaman bab, 1 halaman pustaka).
- **15 sumber tersitasi**, 9 tabel, 4 gambar, dan 10 persamaan bernomor; seluruh label dan sitasi terdefinisi.
- Log final: 0 error, 0 undefined citation/reference, 0 overfull box. Masih terdapat 189 pemberitahuan underfull pada pratinjau terkait perataan tanpa pemenggalan kata template; pengaturan format tidak diubah untuk menyembunyikannya. Teks diperiksa secara visual dan tidak terpotong/bertumpuk.
- Seluruh halaman diperiksa melalui render kontak; halaman akhir setelah pemadatan diperiksa kembali pada resolusi lebih besar. Halaman sisa satu baris telah hilang. Posisi penjelasan kini mengikuti gambar/tabel.
- Nomor bab/bagian, tabel, gambar, persamaan, daftar otomatis, serta bibliografi memakai penghitung LaTeX. Tidak ditemukan `??` pada teks PDF.
- Tidak ada intermediate `.aux/.log/.xdv/.toc/.lof/.lot/.bbl/.blg` tersisa pada akar folder sumber buku.
- Metadata Matouq dari bibliografi paper juga cocok dengan laman penerbit: https://journals.sagepub.com/doi/abs/10.1177/03611981241246993. DOI yang berbeda pada bibliografi lama tidak dibawa ke draf baru.
- Scope final tetap draf Bab I–III. Halaman identitas/abstrak/pengesahan dan Bab IV–V belum diisi; PDF pratinjau tidak menyatakan buku lengkap siap diserahkan.

## Tindak lanjut — diagram metodologi pengguna
Pengguna memilih `latex/IEEE-Conference/gambar/methodology_workflow.png` dan mengizinkan pemasangan melalui pesan “gas masukin”. Diagram disalin tanpa perubahan ke `latex/buku-ta-template/gambar/` dan menggantikan diagram linear LaTeX pada bagian 3.2. Berkas gambar sumber IEEE tetap utuh.

Paragraf sesudah gambar menjelaskan urutan akuisisi–anotasi–evaluasi, bobot terbaik berdasarkan validasi sumber, makna rekonstruksi pada kelompok custom/modified, dan sifat perkiraan rasio 70:20:10. Efisiensi, ablasi empat/enam kelas, serta pembandingan empat kelas sumber–target dijelaskan dalam teks pendamping. Label/caption tetap Gambar 3.1; desain dan label bahasa Inggris pada PNG asli dipertahankan.

Kedua PDF berhasil dikompilasi; pratinjau terbaru 35 halaman. Log akhir tidak memuat error, overfull, atau rujukan tak terdefinisi. Halaman gambar (halaman PDF 23/nomor isi 19) dirender dan diperiksa: seluruh diagram tampil di dalam margin, tanpa pemotongan atau tumpang tindih. Render: `build/qa-bab123/diagram-pengguna.png`.

## Tindak lanjut — identitas mengikuti proposal LaTeX
Pengguna meminta menyamakan judul, penulis, serta pembimbing dengan `latex/skripsi-telkom/`. `metadata.tex` kini mengikuti definisi aktif di `skripsi-telkom/main.tex`: judul Indonesia/Inggris, Faaris Khairrudin, NIM 103052300115, Sains Data, tahun 2026, Dr. GAMMA KOSALA, S.Si (NIP 26920005), serta Kaprodi sesuai sumber tersebut. Tanggal 4 September 2026 disalin dari metadata LaTeX yang diminta pengguna; ini isian draf, bukan verifikasi bahwa pengesahan buku telah terjadi. PDF proposal bertanda tangan memakai tanggal berbeda (4 Mei 2026); tidak direkonsiliasi dengan mengubah sumber proposal.

Lembar pengesahan menggunakan satu pembimbing sesuai flag aktif proposal. Identitas pembimbing kedua yang masih contoh tidak dibawa ke buku. Judul/penulis metadata PDF juga diperbarui. Berkas halaman orisinalitas tidak diubah redaksinya; identitas otomatis mengikuti macro yang sama.

Kompilasi susunan buku dan pratinjau Bab I–III berhasil. Sampul dan lembar pengesahan dirender serta diperiksa: teks utuh, satu pembimbing, tidak bertumpuk, tidak meluber. Log tidak memuat error, overfull, atau rujukan tak terdefinisi. Render: `build/qa-bab123/identitas-{1,2}.png`.

## Tindak lanjut — kata pengantar dan ucapan terima kasih
Atas permintaan pengguna, placeholder `Kata-Pengantar.tex` dan `Ucapan-Terima-Kasih.tex` diganti narasi singkat. Kata pengantar memuat syukur, tujuan penyusunan, topik, terima kasih, harapan manfaat, dan keterbukaan terhadap perbaikan sesuai panduan. Ucapan terima kasih menyebut pembimbing, rekan diskusi Big Data Lab, serta fasilitas GPU RTX 4070 SUPER 12 GB sesuai perangkat eksperimen yang tercatat. Tidak menambahkan nama individu atau pihak lain yang belum diberikan pengguna.

PDF susunan buku berhasil dikompilasi; kedua halaman (vi dan vii) dirender dan diperiksa. Tidak ada teks bertumpuk/terpotong, error, overfull, atau rujukan tak terdefinisi. Render: `build/qa-bab123/pengantar-{6,7}.png`. PDF pratinjau Bab I–III memang tidak memuat halaman awal tersebut; perubahan terlihat pada `hasil/Template_Buku_TA_FIF.pdf`.

### Revisi kata pengantar — terima kasih umum
Pengguna meminta kata pengantar yang umum. Penyebutan pembimbing, rekan Big Data Lab, diskusi, dan fasilitas pada paragraf terima kasih kata pengantar diganti satu kalimat terima kasih kepada seluruh pihak atas bimbingan, bantuan, dan dukungan. Ucapan terima kasih khusus tetap pada halaman tersendiri. PDF dikompilasi dan halaman kata pengantar diperiksa kembali; tidak ada error, overfull, atau rujukan tak terdefinisi.
