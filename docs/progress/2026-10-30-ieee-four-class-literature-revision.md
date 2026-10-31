# Fokus empat kelas dan dukungan literatur paper IEEE

## Persetujuan dan cakupan
Pengguna menyetujui paket revisi dengan "gas coba terapin": dua sitasi Telkom, fokus zero-shot pada empat kelas utama, pemindahan pembahasan patchy road ke analisis tambahan, dan interpretasi hasil dengan literatur.

## Keputusan metodologis
- Evaluasi utama tetap empat kelas D00/D10/D20/D40 pada source dan target. Model tetap dilatih enam kelas; seluruh citra target dipertahankan. Tidak ada training atau inferensi baru.
- Hasil patchy road tidak dibuang karena skor rendah. Paragraf asli dipindahkan ke supplementary-zero-shot.tex, disertai protokol dan keterbatasan. Supplement dikompilasi sebagai PDF terpisah untuk menyertai paper.
- Review sebelumnya menemukan hitungan overlap pengecoh valid sebagai diagnostik jumlah kotak prediksi, bukan formal false-positive rate atau persentase objek unik. Narasi paper yang sudah membatasi interpretasi ini dipertahankan; perhitungan tidak diubah.

## Perubahan
- Sitasi Tilmisani & Kosala pada Introduction; Rianto & Kosala pada Related Work. Masing-masing satu lokasi, tanpa paragraf khusus. Metadata dan dukungan klaim berasal dari abstrak/BibTeX yang diberikan pengguna; tidak mengklaim telah membaca full text.
- Methods menjelaskan empat kategori RDD2022, model enam kelas, semua citra target, dan lokasi analisis lima kelas.
- Results menambahkan konteks DA-RDD dan DIFEDA serta hipotesis Area Attention YOLOv12 dengan batas eksplisit bahwa kontribusi modul tidak diisolasi.
- Pembahasan efisiensi YOLOv8-PD disambungkan ke paper asal. Klaim lama "lowest parameter count" dikoreksi menjadi lebih sedikit parameter daripada YOLOv8n karena tabel sendiri mencantumkan YOLO26n 2.38 M, lebih kecil daripada PD 2.47 M.
- Tahun entri DIFEDA diselaraskan ke volume 36(3), 2026 (terbit daring 2025); key tetap li2025dife agar referensi tidak putus.
- INDEX ditambah lokasi sumber suplemen.

## Landasan yang diperiksa
- YOLOv12: https://arxiv.org/html/2502.12524v1 — desain Area Attention; bukan bukti sebab keunggulan transfer Indonesia.
- DA-RDD: https://eprints.gla.ac.uk/285896/1/285896.pdf — konteks adaptasi lintas negara.
- DIFEDA: https://ieeexplore.ieee.org/abstract/document/11176940 — abstrak dan metadata; mencakup baseline YOLOv12, tanpa klaim ranking dari tabel yang belum diperiksa.
- YOLOv8-PD: https://www.nature.com/articles/s41598-024-62933-z — desain efisiensi.
- RDD2022: https://arxiv.org/abs/2209.08538 — empat kategori kerusakan.

## Validasi
Kompilasi paper dan suplemen berhasil. Render seluruh halaman diperiksa; tidak ditemukan teks terpotong atau overlap. Page break manual sebelum daftar pustaka dihapus agar referensi mengikuti kesimpulan tanpa ruang kosong yang tidak perlu. Paper tetap 6 halaman; suplemen 1 halaman. Sitasi Telkom muncul sebagai [9] dan [13], DA-RDD/DIFEDA sebagai [17]/[18]. Log awal revisi tidak memuat warning, overfull, atau undefined references.

## Penambahan dua referensi komponen model
Pengguna menyetujui dengan "gas" penambahan GhostNet (Han et al., CVPR 2020) dan WTConv (Finder et al., ECCV 2024). Kedua entri sudah tersedia dalam references.bib. Sitasi ditambahkan pada frasa Ghost-based blocks dan wavelet-convolution head di Related Work II-B, tanpa paragraf baru atau klaim tambahan tentang domain shift. Target daftar pustaka: 20 referensi.

Validasi tambahan: kompilasi berhasil tanpa warning/undefined/overfull; main.bbl berisi tepat 20 bibitem. GhostNet [14] dan WTConv [15] tampil pada II-B; render halaman 2 dan 6 diperiksa. Paper tetap 6 halaman.
