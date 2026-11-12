# Salinan submission ISRITI

**Versi terunggah dan bahan bimbingan dibedakan:**

- `hasil/ISRITI_Review_Anonymous.pdf`: versi anonim yang sudah berhasil diunggah pengguna ke EDAS; file ini dipertahankan tanpa perubahan.
- `hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf`: versi 6 halaman dengan revisi posisi gambar/tabel; pengguna melaporkan sudah mengunggah ulang versi ini. Dibangun dengan `bash compile-review-revised.sh`.
- `hasil/ISRITI_Architecture_Discussion_Draft.pdf`: versi bahan bimbingan 7 halaman dengan diagram ringkas dan tabel implementasi tambahan. Disimpan terpisah dan tidak diunggah oleh agen.
- `hasil/ISRITI_Submission_A4.pdf`: versi dengan nama, afiliasi dan email author; dipertahankan terpisah.

EDAS konferensi ini menerapkan double-blind. Versi review dan bahan bimbingan sama-sama mempertahankan anonimitas author.

Salinan mandiri paper dari `../IEEE-Conference/`, dibuat pada 12 November 2026 atas persetujuan pengguna untuk persiapan submission ISRITI. Isi naskah, identitas penulis, angka dan isi tabel, sitasi, gambar, dan sakelar analisis dipertahankan, dengan satu pembaruan keyword yang disetujui pengguna dan dijelaskan di bawah.

Satu-satunya perbedaan pada `main.tex` saat penyalinan adalah opsi ukuran kertas:

```diff
-\documentclass[conference]{IEEEtran}
+\documentclass[conference,a4paper]{IEEEtran}
```

`IEEEtran.cls`, `IEEEtran.bst`, kedua berkas `.bib`, seluruh isi `gambar/`, serta source suplemen disalin tanpa perubahan byte. Source suplemen disimpan sebagai pendamping; script kompilasi hanya menghasilkan PDF paper utama.

## Bahan bimbingan dengan diagram dan tabel implementasi

Pengguna meminta salinan tambahan untuk dibandingkan dengan versi yang sudah disubmit saat bimbingan pada 13 November 2026. Versi diskusi berada di `discussion/main.tex`, yaitu snapshot source revisi layout dengan tambahan package `array` dan satu input `discussion/architecture-addition.tex`. Isi naskah lama dapat dipulihkan identik byte demi byte dengan menghapus dua tambahan itu. Penambahan ini memang menambah teks: pengantar singkat, caption diagram dan tabel, serta isi tabel implementasi; hasil eksperimen lama tidak disunting. Nomor gambar/tabel sesudahnya menyesuaikan otomatis.

Halaman 3 memuat satu figure dua panel tentang implementasi lokal YOLOv8-PD dan YOLO-RD serta satu tabel empat aspek yang membedakan desain referensi dengan pilihan implementasi. Diagram dibuat sendiri dari rute YAML lokal dan memakai label minimal 8.3 pt pada ukuran cetak. Repeats, channel count dan operasi internal modul sengaja diringkas. Tidak ada figure dari paper referensi yang disalin sebagai gambaran model yang diuji.

Asset baru `gambar/architecture_compact_discussion.pdf` dibuat dengan `scripts/paper/paper_fig_architectures_compact.py`. Perbedaan penting yang dijelaskan adalah MAF berbobot pada paper YOLO-RD versus Upsample--Concat--Conv 1x1 pada implementasi lokal. Diagram lengkap per layer yang sudah ada tetap cocok untuk diskusi detail, skripsi atau materi pendamping; tidak dikecilkan menjadi label yang sulit dibaca dalam paper.

Kompilasi:

```bash
cd latex/ISRITI-submission
bash compile-discussion.sh
```

Output bahan bimbingan tetap 7 halaman A4, seluruh 16 font tertanam, tanpa bookmark/link aktif maupun metadata identitas author. Ketujuh halaman sudah diperiksa visual; log final bersih. Bibliography 20 entri tetap identik. Seluruh 61 file sebelum penambahan, termasuk semua PDF yang sudah diunggah, tetap cocok SHA-256. Bukti di `build/architecture-discussion-verification.json`; catatan lengkap di `../../docs/progress/2026-11-12-isriti-architecture-discussion.md`.

## Revisi posisi gambar dan tabel

Pengguna meminta versi layout yang terpisah dari PDF terunggah, lalu menunjukkan contoh Fig. 1 tepat setelah judul Materials and Methods dan kalimat pengantarnya. Revisi mengikuti susunan itu dengan penempatan `[H]` hanya untuk Fig. 1. Ini merupakan pilihan lokal sesuai contoh pengguna; template konferensi secara umum menganjurkan float di atas/bawah kolom, sehingga revisi ini tidak diklaim mengikuti anjuran posisi tersebut pada Fig. 1.

Table I ditempatkan di bawah halaman 3 melintasi dua kolom menggunakan `stfloats`, sehingga berada pada halaman yang sama dengan pembahasan hasil source dan tidak lagi menumpuk di halaman 4. Table IV ditempatkan di bawah kolom kanan halaman 4 setelah rujukan dan pembahasan utama zero-shot-nya. Figure 2–4 serta Table II–III tetap berupa float atas/bawah, semua setelah penyebutan pertamanya dalam urutan baca dua kolom. Beberapa float tetap terpisah dari paragraf pengantarnya; tidak dipaksa semuanya menempel pada teks.

Script `compile-review-revised.sh` menurunkan source dari `main.tex` ke `build/review-revised.tex` pada setiap kompilasi. Selain anonimisasi yang sama dengan versi terunggah, perbedaannya hanya package `stfloats` dan tiga opsi penempatan float. Seluruh source ilmiah identik setelah opsi penempatan diabaikan. Font, margin, ukuran gambar, desain/isi tabel, caption, urutan referensi dan isi naskah tidak diubah.

Revisi tetap 6 halaman A4, tanpa bookmark/link aktif dan tanpa identitas author. Semua font tertanam, bibliography identik 20 entri, inventaris karakter PDF sama setelah whitespace/ligatur/hyphen pemenggalan baris dinormalisasi, dan semua halaman dirender serta diperiksa visual. SHA-256 PDF terunggah dan file lama lain tetap sama. Bukti: `build/review-revised-verification.json`, `build/review-revised-vs-submitted-source.diff`, dan `build/render-review-revised/`. Catatan lengkap: `../../docs/progress/2026-11-12-isriti-layout-revision.md`.

## Review anonim awal untuk EDAS

Pengguna menyetujui pembuatan versi review anonim setelah EDAS menolak upload karena nama author dalam metadata (`authormeta`) dan mendeteksi blok identitas pada halaman pertama (`authorname`). EDAS juga memperingatkan bookmark dan tautan PDF yang aktif.

Jalankan `bash compile-review.sh` untuk menghasilkan `hasil/ISRITI_Review_Anonymous.pdf`. Script membaca `main.tex` terkini, menghasilkan source turunan di `build/review-anonymous.tex`, menghapus pemakaian `hyperref`, mengosongkan metadata author sambil mempertahankan judul, dan mengganti blok identitas dengan `Anonymous Authors`. Semua source setelah `\maketitle` tetap identik byte demi byte. Intermediates berada di `build/review-anonymous/`. Script dan PDF dengan identitas tidak ditimpa.

PDF anonim tetap 6 halaman A4 dengan font tertanam, tanpa bookmark, annotation/link, maupun lampiran. Bibliography tetap 20 entri yang identik; nama `G. Kosala` pada dua referensi karya terdahulu dipertahankan sebagai sitasi, bukan blok identitas penulis paper ini. Penghapusan blok afiliasi mengubah aliran halaman secara normal; referensi pada halaman terakhir tetap mengisi kiri dahulu. Semua halaman sudah dirender dan diperiksa visual.

Bukti lokal: `build/review-anonymous-verification.json`, `build/review-anonymous-source.diff`, dan `build/render-review-anonymous/`. Pengguna kemudian mengirim bukti upload berhasil dan status `Active (has manuscript)` untuk versi awal ini. Sertifikasi IEEE PDF eXpress belum dilakukan. Data author pada record EDAS tetap berisi Faaris Khairrudin dan Gamma Kosala. Catatan perbaikan: `../../docs/progress/2026-11-12-isriti-double-blind-review.md`.

## Format submission yang ditetapkan

Setelah pengguna menyetujui mengikuti contoh konferensi, empat tabel utama memakai gaya kotak dari `conference_101719.tex`: kolom dengan garis vertikal, `\hline`/`\cline`, serta header tebal dan subheader bertingkat tebal miring. Ukuran teks dan catatan tabel memakai `\footnotesize` IEEEtran (8 pt). Isi setiap sel, caption, catatan dan label tabel dipertahankan.

Pada versi awal, tabel dan gambar memakai penempatan atas/bawah kolom; perubahan pada revisi layout dijelaskan di atas. Deklarasi Tabel I dipindahkan ke setelah penyebutan pertamanya pada teks. `\raggedbottom` mencegah ruang kosong kolom meregangkan jarak paragraf; font, baseline teks, margin, lebar kolom, dan ukuran gambar tidak diubah. Sesuai permintaan pengguna terakhir, referensi mengisi kolom kiri terlebih dahulu mengikuti alur LaTeX normal; pemisahan manual `\IEEEtriggeratref{16}` telah dihapus.

PDF tetap A4, 6 halaman. Pemeriksaan source memastikan seluruh teks di luar float tetap sama setelah perintah format diabaikan, seluruh isi tabel sama setelah markup tampilan diabaikan, dan seluruh blok gambar sama selain opsi penempatan. Seluruh file pada folder naskah asal tidak berubah.

Versi A4 sebelum penyesuaian tabel diarsipkan di `build/before-conference-table-format/`; versi sebelum pengembalian alur referensi di `build/before-natural-references/`. Diff lengkap terhadap naskah asal berada di `build/source-vs-original.diff`; pemeriksaan format di `build/conference-format-verification.json` dan perubahan referensi terakhir di `build/natural-references-verification.json`.

## Penyesuaian keyword

Atas permintaan pengguna, keyword keenam pada salinan submission diubah dari `class-label ablation` menjadi `label-set ablation`. Istilah baru menjelaskan perbandingan himpunan label training enam kelas dan empat kelas; pemilihan ini berdasarkan ketepatan deskripsi, bukan klaim bahwa istilah lama tidak lazim. Lima keyword pertama dan seluruh source lainnya tidak berubah dibandingkan versi sebelum penyesuaian ini. Folder IEEE asal tetap tidak diubah.

Versi sebelumnya disimpan di `build/before-keyword-label-set/`. PDF hasil kompilasi tetap 6 halaman A4; teks hanya berubah pada keyword tersebut dan content stream halaman 2–6 identik. Halaman 1 dirender ulang dan diperiksa visual. Bukti terkini: `build/keyword-update-verification.json` dan `build/keyword-update.diff`. Laporan format sebelumnya merekam keadaan sebelum pembaruan keyword ini.

## Kompilasi

```bash
cd latex/ISRITI-submission
bash compile-review-revised.sh
```

Perintah di atas hanya menghasilkan PDF revisi layout yang namanya terpisah. `bash compile-review.sh` membangun ulang versi anonim awal dan akan menimpa file anonim awal tersebut, sehingga hindari menjalankannya bila ingin mempertahankan snapshot PDF yang sudah terunggah. Untuk membangun versi dengan identitas, gunakan `bash compile.sh` yang menghasilkan `hasil/ISRITI_Submission_A4.pdf`. Semua berkas sementara dan pemeriksaan berada di `build/`. Ketiga script hanya bekerja di folder salinan ini.

## Acuan

- Situs konferensi: https://isriti.utdi.ac.id/
- Paket LaTeX yang ditautkan pada bagian Submission: https://isriti.utdi.ac.id/template/conference-latex-template_IEEE.zip
- Template Word A4: https://isriti.utdi.ac.id/template/Conference-template-A4-IEEE.doc

Kelas IEEE pada paket LaTeX konferensi sama dengan kelas naskah asal setelah normalisasi akhir baris. Opsi `a4paper` dinyatakan eksplisit karena contoh LaTeX yang diunduh masih memakai default Letter, sedangkan ketentuan konferensi meminta A4.

Pemeriksaan lokal tidak menggantikan pemeriksaan EDAS atau proses IEEE PDF eXpress untuk camera-ready. Pengguna melakukan upload sendiri; agen hanya menyiapkan dan memeriksa file lokal. Pengguna melaporkan sudah mengunggah ulang revisi layout 6 halaman. Versi diskusi 7 halaman disiapkan terpisah untuk bimbingan, dengan hasil eksperimen yang sama dan penjelasan implementasi tambahan.

Catatan pemeriksaan format final: `../../docs/progress/2026-11-12-isriti-conference-format-audit.md`. Catatan penyalinan A4 tahap awal: `../../docs/progress/2026-11-12-isriti-submission-a4.md`.
