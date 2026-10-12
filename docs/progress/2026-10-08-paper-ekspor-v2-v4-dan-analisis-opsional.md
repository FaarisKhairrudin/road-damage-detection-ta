# 2026-10-08 — Ekspor V2/V4 dan analisis modular paper IEEE

## Diskusi / masalah
- Penulis meminta analisis tambahan yang dapat dimatikan secara terpisah dari draf paper, terutama per-negara sumber, empat-versus-lima kelas pada uji lintas domain, dan contoh visual permukaan jalan yang tampak berbeda.
- Penulis mengonfirmasi citra target diambil di Jl. Raya Bojongsoang, Kabupaten Bandung. Rincian kamera, waktu, ekstraksi frame, dan audit anotasi ekspor V4 tetap perlu didokumentasikan.
- Visualisasi embedding dan statistik citra sebelumnya memakai ekspor lokal `RDD-indo-v2` (308 gambar), sedangkan evaluasi final memakai `RDD-indo-v4` (307 gambar). Keduanya tidak boleh disebut sebagai split identik tanpa audit.

## Audit ekspor dan penyebab potensi salah tafsir
- Pencocokan berdasarkan ID frame sebelum sufiks Roboflow menemukan **301 gambar bersama** dari 308 gambar V2 test dan 307 gambar V4 valid; 7 ID hanya di V2 dan 6 hanya di V4. Ketiga-ratus-satu pasangan mempunyai byte gambar dan piksel terdekode yang sama walaupun sebagian nama file penuh berbeda.
- V2 test mempunyai 585 baris anotasi pada 308 gambar; V4 valid mempunyai 514 baris pada 307 gambar. Setelah ID kelas V2 `{0:0,1:1,3:2,4:3,5:4}` dipetakan ke V4 dan kelas manhole (ID 2) diabaikan, hanya **151/301** gambar bersama memiliki baris label sama persis; 101 mempunyai jumlah baris berbeda dan 49 mempunyai jumlah sama tetapi isi anotasi berbeda. Dengan demikian, pemakaian visualisasi V2 sebagai metrik V4 adalah kekeliruan metodologis.
- Agregat mAP per negara yang ada menggunakan dukungan kelas berbeda: India memiliki satu GT manhole dan nol GT patchy road. Solusi draf: bandingkan rata-rata AP empat kelas kerusakan yang sama dan beri batasan ukuran subset.
- Pembanding zero-shot lima kelas juga memberi bobot sama pada patchy road yang hanya memiliki 22 GT target. Solusi draf: sertakan analisis sensitivitas empat kelas inti untuk sumber dan target tanpa mengganti bobot model.

## Solusi yang diterapkan pada draf
- Sakelar LaTeX untuk analisis tambahan dibuat di preamble `latex/IEEE-Conference/main.tex`; abstrak, metode, dan kesimpulan mengondisikan pernyataan ablasi jika sakelar dimatikan.
- Modul negara memakai rata-rata dari tabel AP per kelas yang dibulatkan; angka ditandai perkiraan sampai ekspor CSV per-negara eksak tersedia.
- Modul visual hanya mendeskripsikan satu contoh GT/prediksi V4 dan contoh sumber, bukan mengklaim beton menyebabkan penurunan mAP. Prediksi ilustratif memakai conf 0.25, berbeda dari conf 0.001 evaluasi numerik.
- Plot UMAP V2 disediakan sebagai modul opsional yang **nonaktif secara default**, dengan versi ekspor dan overlap citra dijelaskan jelas.
- Pembuatan gambar komposit pertama gagal karena jalur font DejaVu yang tidak ada di mesin ini; jalur font diganti ke Noto Sans yang tersedia, dan file gambar berhasil dibuat.
- Layout awal menempatkan figur dua kolom sendirian setelah daftar pustaka; figur dipindahkan sebelum bagian hasil, dipotong agar fokus pada permukaan jalan, dan caption/paragraf diringkas. `bash compile.sh` kemudian berhasil menghasilkan PDF empat halaman tanpa overfull box. Peringatan dua sitasi `TODO` sengaja belum terselesaikan karena metadata referensi YOLOv12/YOLO26 perlu verifikasi.
- Uji dua konfigurasi sementara: semua analisis opsional nonaktif → PDF 3 halaman; semua analisis opsional nonaktif tetapi modul UMAP V2 aktif → PDF 3 halaman. Keduanya sukses kompilasi tanpa overfull box atau referensi silang hilang, selain dua placeholder sitasi yang memang disengaja. Berkas `.tex` sementara dihapus; PDF utama tetap empat halaman.

## Keputusan penamaan publik (permintaan lanjutan)
- Nomor folder lokal `RDD-indo-v2`/`RDD-indo-v4` tidak dipakai sebagai nama dataset pada naskah. Abstrak dan metode sekarang menyebut *Indonesian road image set* / target Indonesia, sambil tetap memberi 307 gambar, 514 anotasi, lima kelas, split ekspor `valid`, dan lokasi yang dikonfirmasi penulis (Jl. Raya Bojongsoang, Kabupaten Bandung).
- Caption figur memakai istilah target Indonesia; modul UMAP opsional menjelaskan hanya sebagai *earlier export*, 308 vs 307 gambar, overlap 301 gambar identik, tanpa menyamaratakan evaluasi dua anotasi. Rilis anotasi yang tepat masih harus diarsipkan/dikutip untuk reprodusibilitas.
- `bash compile.sh` berhasil setelah revisi nama; kompilasi terbaru berjumlah lima halaman karena daftar pustaka juga diperbarui oleh proses lain (dua entri primer YOLO ditambahkan secara terpisah), tanpa sitasi tak-terdefinisi/overfull. Halaman terakhir hanya memuat akhir daftar pustaka; penyusunan akhir masih perlu perapian.

## Batasan berikutnya
- Konfirmasi metode akuisisi dan anotasi target; audit kemungkinan frame berdekatan dari video yang sama dan kebocoran identitas terhadap data sumber.
- Jangan menyebut perbedaan permukaan sebagai sebab kausal tanpa label material yang diverifikasi dan evaluasi per-subset dengan dukungan kelas memadai.
- Parameter/GFLOPs dan protokol FPS tetap belum direkonsiliasi; metadata dua sitasi YOLO masih TODO pada bibliografi paper.
