# Submission ISRITI — source dan snapshot review

Folder ini menyimpan salinan A4 paper beserta versi review anonim. **Versi aktif yang dilaporkan sudah diunggah ulang adalah PDF enam halaman `hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf`.** Source penelitian tidak diganti dengan draft diskusi arsitektur tujuh halaman.

## Versi yang dipertahankan

| Peran | Lokasi |
|---|---|
| Snapshot review revisi layout yang disubmit | [hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf](hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf) |
| Snapshot review anonim awal yang sebelumnya berhasil diunggah | [hasil/ISRITI_Review_Anonymous.pdf](hasil/ISRITI_Review_Anonymous.pdf) |
| PDF A4 dengan nama, afiliasi dan email author | [hasil/ISRITI_Submission_A4.pdf](hasil/ISRITI_Submission_A4.pdf) |
| Source dasar salinan ISRITI | [main.tex](main.tex) |
| Sumber paper sebelum penyesuaian submission | [../IEEE-Conference/main.tex](../IEEE-Conference/main.tex) |

Hash SHA-256 snapshot review revisi layout yang dicatat pada peta artefak:

```text
8e00e6dea660c80b9ef28d942d6b9a27358950e42c7cfce6e0ce8b7873f7a690
```

Lihat [peta artefak aktif](../../docs/FINAL_ARTIFACTS.json). Kedua PDF review adalah bukti versi yang sudah diunggah, sehingga tidak boleh ditimpa hanya untuk menyegarkan build. Tidak ada upload ulang konferensi atau kompilasi PDF pada pembaruan dokumentasi ini.

## Draft arsitektur sudah dibatalkan

Draft diskusi tujuh halaman dibuat sebagai bahan bimbingan, kemudian **dibatalkan atas permintaan pengguna pada 13 November 2026**. Source `discussion/`, `compile-discussion.sh`, generator diagram ringkas, PDF dan bukti QA-nya dipindahkan bersama ke:

[build/archived-architecture-discussion-2026-11-13/](build/archived-architecture-discussion-2026-11-13/)

[manifest.json](build/archived-architecture-discussion-2026-11-13/manifest.json) mencatat alasan pembatalan, path asli dan hash arsip, serta snapshot review aktif yang dipertahankan. Perintah `bash compile-discussion.sh` bukan perintah aktif pada folder ini. Jangan memulihkan draft tersebut berdasarkan petunjuk historis.

## Kompilasi yang sudah tersedia

Jalankan dari folder ini hanya ketika memang diperlukan. **Skrip-skrip berikut menyalin hasil build ke `hasil/` dan dapat menimpa PDF dengan nama yang sama.** Amankan snapshot terunggah lebih dahulu dan verifikasi hasil baru sebagai versi terpisah.

| Perintah | Keluaran | Peran |
|---|---|---|
| `bash compile-review-revised.sh` | `hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf` | Review anonim dengan revisi layout |
| `bash compile-review.sh` | `hasil/ISRITI_Review_Anonymous.pdf` | Review anonim awal |
| `bash compile.sh` | `hasil/ISRITI_Submission_A4.pdf` | Versi dengan identitas author |

Skrip anonim membaca `main.tex` dan membuat source turunan dalam `build/`; blok author dan metadata author dihapus, bookmark/link PDF dimatikan. Revisi layout menambahkan `stfloats`, membuat workflow inline sesuai contoh pengguna, serta menempatkan tabel source lebar dan tabel transfer di bawah halaman/kolom yang ditetapkan. Skrip memiliki assertion untuk memastikan teks ilmiah sesudah `\maketitle` tetap sama setelah opsi float diabaikan.

Review dan versi beridentitas harus dibedakan untuk proses double-blind. Pemeriksaan lokal tidak menggantikan pemeriksaan EDAS atau proses PDF eXpress bila diminta pada tahap berikutnya.

## Cakupan ilmiah dan rujukan hasil

Hasil pada paper mengacu target final **RDD-Indo-Crop versi 4: 307 gambar, 502 anotasi dan 39 gambar tanpa anotasi**. Empat kelas kerusakan memiliki 481 anotasi; 21 anotasi patchy road menjadi kategori tambahan. Perbandingan transfer utama memakai empat kelas yang sama di source dan target; hasil lima kelas bersama adalah analisis tambahan.

[docs/RESULTS_TABLE.md](../../docs/RESULTS_TABLE.md), [narasi analisis](../../docs/draft-analisis-rapih.md), dan [peta artefak](../../docs/FINAL_ARTIFACTS.json) membantu menelusuri angka. Pembaruan dokumentasi/analisis tidak otomatis mengubah `main.tex`, asset gambar paper atau PDF snapshot yang sudah disubmit.

Bagian feature-viz pada source paper dinonaktifkan. Gambar UMAP/statistik dari ekspor Indonesia 308 gambar yang lebih lama tidak boleh dilabeli ulang sebagai bukti V4. Gunakan status bundle analisis terbaru pada peta artefak sebelum mempertimbangkan perubahan naskah yang terpisah.

## Bukti historis dan file build

Catatan awal A4, audit format, anonimisasi dan revisi layout tetap tersedia di [docs/progress/](../../docs/progress/). Petunjuk historis yang menyebut draft arsitektur aktif telah digantikan oleh status pembatalan di atas.

Folder `build/` juga menyimpan snapshot sebelum perubahan format/keyword dan bukti pemeriksaan. Ia bukan seluruhnya cache yang boleh dibersihkan. `IEEEtran.cls`, style bibliografi, kedua database `.bib`, source suplemen dan gambar tetap dipertahankan pada lokasi yang dipakai source.

README sebelum pembaruan disimpan byte-identik di [arsip konten](../../docs/archive/content-before-update/latex/ISRITI-submission/README.md). Dokumentasi terkini tidak menyatakan bahwa naskah sudah diterima atau dipublikasikan.
