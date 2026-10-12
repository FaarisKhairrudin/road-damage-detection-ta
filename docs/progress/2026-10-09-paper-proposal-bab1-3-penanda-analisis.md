# 2026-10-09 — Tinjauan proposal Bab I–III dan penanda analisis paper IEEE

## Permintaan dan prinsip editorial
- Meninjau `docs/proposal.pdf` Bab I (halaman PDF 6–12), Bab II (13–19), dan Bab III (20–30), serta naskah `latex/IEEE-Conference/main.tex`.
- Pembahasan latar belakang/literatur tetap ringkas; ruang lebih banyak untuk metode, hasil, dan analisis. Pengguna memilih penanda berupa komentar LaTeX (`% REVIEW-ANALYSIS` dan `% REVIEW-METHOD`) sehingga tidak terlihat pada PDF.

## Temuan dan kehati-hatian metodologis
- Bab I §1.1 dan Bab II §2.1 memotivasi anotasi manhole dan tambalan jalan yang mirip pothole. Matouq dkk., `latex/refference/09_AI-Driven Approach for Automated Real-Time Pothole Detection, Localization, and Area Estimation.pdf`, secara eksplisit menyebut kemiripan ini serta melatih tiga kelas. Itu mendukung motivasi, **bukan** bukti kausal bahwa kelas tambahan menurunkan false positive pada dataset dan model penelitian ini. Naskah sudah tepat menyebut manfaatnya sebagai pertanyaan empiris.
- Bab II §2.3 dan Bab III §3.3 menjelaskan modul arsitektur; sumber primer YOLOv8-PD pada `latex/refference/02_YOLOv8‑PD an improved road.pdf` (abstrak dan gambar modul) menyebut BoT, LSKA, C2fGhost, LSCD-Head. YOLO-RD pada `latex/refference/04_YOLO RD A Road Damage Detection Method for Effective.pdf` (bagian 3.1) menyebut SOM, MAF/ARM, dan WTC. Kode rekonstruksi lokal `code/models/yolov8-pd.yaml` serta `code/models/yolo-rd.yaml` memuat adaptasi ide itu, tetapi bukan reproduksi identik kode penulis. Ringkasan per model cukup satu kalimat, tanpa uraian evolusi YOLOv1–v4 dari proposal.
- Bab III mengandung rencana Focal Loss, klaim real-time/edge, pemilihan satu model akhir, dan domain shift yang mungkin terkesan kausal. Paper melaporkan hasil yang benar-benar ada: effective-number-derived BCE weights, semua model pada zero-shot target, FPS sebagai proxy belum direkonsiliasi, dan kontras antarset bukan identifikasi sebab material/lokasi. Jangan mentransfer rencana proposal sebagai hasil.
- Kalimat pertanyaan “We also ask what changes when manhole and patchy-road labels are removed ...” **sudah** dijawab oleh bagian Four- versus Six-Class Training dan Table ablation dalam draft; penanda diberi status `covered`/`conditional`, bukan `pending`.
- Analisis country masih berupa mean dari angka pembulatan (perlu ekspor AP tepat atau hilangkan bagian opsional); FPS masih memerlukan satu protokol timing standar. Penanda `pending` ditambahkan untuk dua hal ini.

## Perubahan yang disetujui dan diterapkan
- `latex/IEEE-Conference/main.tex`: satu kalimat motivasi visual yang berhati-hati dengan `\cite{matouq2024ai}` pada Introduction; dua kalimat sangat ringkas tentang modul YOLOv8-PD/YOLO-RD pada Compact Detection Architectures; komentar sumber pada RQ/ablation/zero-shot dan dua item tertunda (FPS, country). Tidak ada highlight yang akan terbawa ke PDF.
- `latex/IEEE-Conference/references.bib`: DOI Matouq dikoreksi dari `10.1177/0361198124656269` ke `10.1177/03611981241246993`, sesuai header PDF lokal (halaman artikel 2018). Perubahan ini menghindari sitasi DOI salah ketika referensi tersebut dipakai di Introduction.
- Cek kompilasi IEEE dilakukan setelah perubahan untuk memastikan sitasi dan tata letak tetap valid.

## Penyempurnaan alur Related Work / Methods
- Diskusi lanjutan: frasa tentang model yang dievaluasi dan status rekonstruksi pada `Compact Detection Architectures` mengulang isi `Compared Models and Training`.
- Solusi disetujui: Related Work mempertahankan hanya desain/modul karya terdahulu; Methods menyebut kelima model yang benar-benar dievaluasi, sumber arsitektur YOLOv12/YOLO26, dan status rekonstruksi lokal yang tidak bit-exact. Ini tidak mengubah eksperimen maupun klaim hasil.

## Klarifikasi pemilihan enam dari sepuluh kelas
- Masalah: Introduction sudah menyebut kemiripan potensial manhole/patches dengan pothole menurut Matouq dkk., tetapi Methods belum menyatakan secara eksplisit bahwa D70 dan D80 dipilih dari sepuluh kategori N-RDD2024, bukan digunakan seluruhnya.
- Solusi disetujui: mengganti satu kalimat di Source and Target Data untuk menegaskan empat kelas kerusakan inti ditambah D70 (manhole) dan D80 (patchy road), dipilih karena kemiripan visual potensial dengan pothole; mengutip dataset N-RDD2024 dan Matouq dkk. Ini motivasi seleksi label, bukan klaim bahwa penambahan label terbukti menurunkan false positive pada eksperimen ini.

## Pembaruan setelah konfirmasi penulis (2026-10-09)
- Penulis mengonfirmasi metode target: video ponsel menghadap jalan, resolusi 1080p, sampling 1 frame/detik, anotasi melalui Roboflow. Sekitar 1.000 frame kandidat dikurasi; ekspor yang dievaluasi memiliki 307 gambar 640×640, 514 instance, dan 39 label kosong/background. Naskah menyatakan hanya split Roboflow `valid` tersedia dan dipakai untuk zero-shot. Kriteria seleksi, kualitas label, ketergantungan frame video, dan kemungkinan overlap sumber tetap ditandai untuk dokumentasi.
- Penulis meminta semua analisis, termasuk komparasi 4-vs-6 kelas, tetap tampak di draft saat ini; komentar LaTeX sumber menandai analisis tersebut masih provisional, bukan menyembunyikannya.
- Tabel hasil utama ditambah Params dan GFLOPs untuk lima model enam-kelas, memakai satu basis konsisten dari ringkasan evaluasi Ultralytics 8.4.108 pada imgsz 640 (`docs/RESULTS.md`): YOLOv8n 3.01M/8.1; YOLOv12n 2.56M/6.3; YOLO26n 2.38M/5.2; YOLOv8-PD 2.47M/7.6; YOLO-RD 7.09M/12.8. Catatan tabel membedakan kompleksitas ringkasan dari latency; FPS tetap estimate dengan timing belum diseragamkan. Tabel dijadikan dua kolom agar kolom tujuh metrik tetap terbaca.
- Mengganti frasa audit-style “The recorded training configuration” dengan “We trained all five six-class models...” yang didukung args lima run; keterbatasan tetap menyatakan satu seed dan variasi batch/AMP. Related Work juga diringkas dengan satu kalimat tentang tema modifikasi YOLO-road lainnya (attention, lightweight convolution, feature fusion), lalu detail pada dua arsitektur yang dibandingkan.
- Nilai penurunan target tetap dilaporkan sebagai hasil deskriptif; komentar review menyatakan sebabnya masih dianalisis dan tidak boleh diklaim dari eksperimen ini sebelum ada bukti.
