# Audit akhir kesiapan submit IEEE — 2026-10-30

## Cakupan dan keputusan
Pengguna meminta last check tiap bagian dan korelasi antarbab. Audit read-only terhadap main.tex, references.bib, suplemen, PDF final, CSV sumber/target, args.yaml final, serta kode ekspor F1 notebook (source cells, tanpa mengeksekusi). Tidak mengubah naskah atau angka dan tidak menjalankan inferensi/training.

Kesimpulan: alur dan klaim utama selaras, tetapi belum disarankan submit persis versi ini sebelum kejelasan F1 dan optimizer dilengkapi dan ketentuan venue dipastikan.

## Korelasi bagian
- Judul dan abstrak sesuai eksperimen perbandingan model compact dan transfer domain; tidak mengklaim model baru.
- Introduction memiliki tiga kontribusi yang dijawab oleh hasil sumber/throughput (IV-A), ablasi (IV-C), dan transfer (IV-D). IV-B merupakan subgroup source, bukan unseen-country transfer.
- Related Work memotivasi kelas pengecoh dan efisiensi. Sitasi Telkom digunakan terbatas pada klaim dari abstrak yang diberikan pengguna.
- Methods memisahkan 6 kelas training/source keseluruhan, 4 kelas evaluasi transfer, dan 4 kelas training ablasi. Semua citra dipertahankan. Adaptasi fusion RD dan partial pretraining diungkapkan.
- Results/Conclusion konsisten: RD source terbaik, v12 target terbaik, PD throughput tertinggi; pengaruh pengecoh tidak terbukti konsisten. Penjelasan attention dan tekstur bersifat hipotesis.
- Suplemen mempertahankan hasil lima kelas; jangan menyatakan provided supplementary analysis jika berkas tidak ikut didistribusikan.

## Temuan penting sebelum submit
1. Macro-F1 tidak menjelaskan aturan confidence operating point. Notebook mengambil class_result dan menghitung harmonic mean P/R lalu macro mean. Dokumentasi Ultralytics saat audit menyebut summary pada threshold yang memaksimalkan mean F1. Perlu konfirmasi implementasi versi runtime run dan jelaskan evaluasi-set optimized F1 bila memang demikian; jangan tulis threshold tetap 0.25/0.001 atau validation-selected jika tidak benar.
2. Lima args final class_weight menggunakan optimizer=auto, lr0 nominal 0.01, weight_decay 0.0005, batch16, seed42. Optimizer aktual dan lr0 dapat ditentukan otomatis sehingga nominal args tidak cukup. Output notebook menunjukkan MuSGD(lr0.01,momentum0.9) untuk RD yang ditampilkan; jangan generalisasi ke semua model tanpa log final. Methods perlu mengungkap auto dan pengaturan efektif jika tersedia.
3. Fig.1 flowchart label kecil dalam satu kolom (preferensi pengguna sebelumnya). Beberapa label panel prediksi juga kecil. Ini persoalan keterbacaan cetak, bukan error kompilasi.
4. Table I menebalkan RD mAP50:95=0.371 tetapi v12 juga tampil0.371 dan prosa menyebut tied to 3 decimals. Bold keduanya atau gunakan presisi lebih tinggi secara konsisten.
5. Metadata YOLOv12 di BibTeX adalah inproceedings dengan booktitle arXiv preprint sehingga daftar pustaka menampilkan "in arXiv preprint". Perbaiki jenis entri preprint; tidak perlu mengklaim venue yang belum diverifikasi. Metadata YOLO26 arxiv2509.25164 cocok judul/empat penulis saat dicek ulang.
6. Identitas/email, batas halaman, review anonymous/nonanonymous, dan mekanisme suplemen/PDF eXpress bergantung venue; belum ada ketentuan konferensi spesifik dalam permintaan ini, sehingga tidak dapat menyatakan administrasi submission sudah lolos.

## Minor / tindak lanjut
- "which preserves class proportions" lebih tepat "to maintain similar class proportions".
- Methods menyebut class weights beta0.999 tetapi belum merinci normalisasi; optimizer, class-weight recipe, dan konfigurasi final bisa dijelaskan pada suplemen reproduksibilitas.
- Potensi korelasi antar-frame dan uji multi-seed tidak diaudit empiris. Jangan menyatakan split bebas near-duplicate atau ranking signifikan. Tidak ada indikasi di audit ini bahwa target masuk training; bukan bukti audit kebocoran menyeluruh.
- catatan note.md dan rangkuman-v2 sebagian historis. Angka final mengikuti CSV dan progress terbaru, bukan ringkasan lama.

## Verifikasi
Rata-rata mAP50 source6 dan source4 dihitung dari lima CSV final. Semua pasangan source4/target4/drop TableIV cocok: v8 0.622/0.303/51.4; v12 0.626/0.413/34.1; v26 0.604/0.301/50.2; PD0.623/0.342/45.2; RD0.633/0.359/43.4. CSV final PD/RD empat kelas cocok0.6341/0.6511. CSV root lain bernama smoke/4cls lama bukan sumber final. Tidak semua angka GFLOPs/per-country/FP dihitung ulang; gunakan audit terdahulu, bukan klaim verifikasi ulang seluruh pipeline.

PDF: 6 halaman, 20 bibitem. Font PDF tertanam. Log kompilasi terbaru tidak memuat warning/overfull/undefined. Render enam halaman diperiksa; tidak ada objek terpotong/bertumpuk, tetapi label Fig1 kecil. TableII masih satu halaman dengan mention, TableIV berada atas halaman5 setelah pembahasan di halaman4. Render: build/final-audit-page-*.png dan final-audit-contact.png.

Sumber web: https://docs.ultralytics.com/reference/utils/metrics/ dan https://arxiv.org/abs/2509.25164. DOI dua paper Telkom tidak berhasil dibuka pada audit ini; klaim tetap berdasarkan abstrak/metadata dari pengguna.

## Implementasi dua tambahan wajib
Pengguna mengizinkan hanya dua tambahan wajib. III-B ditambah automatic optimizer selection (optimizer=auto) dan weight decay0.0005, mengikuti kelima args final. III-C ditambah definisi macro-F1 dari per-class precision/recall pada confidence yang memaksimalkan smoothed mean F1 di evaluated split. Notebook ekspor memakai class_result; sumber Ultralytics tag v8.4.108 diperiksa melalui https://raw.githubusercontent.com/ultralytics/ultralytics/v8.4.108/ultralytics/utils/metrics.py. Default Python lokal tidak menginstal Ultralytics sehingga verifikasi runtime dilakukan pada sumber version-tagged, bukan import executable lokal. Tidak mengubah nilai tabel, threshold inferensi, atau aturan pemilihan checkpoint. Perbaikan editorial lain dalam audit belum diterapkan.
