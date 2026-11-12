# Ringkasan Eksperimen TA — Konteks Final untuk LLM Penulis

> **Versi konteks kerja, bukan naskah paper.** File ini dibuat sebagai versi baru sesuai permintaan; `docs/rangkuman-eksperimen-ta.md` sengaja tidak ditimpa. Gunakan file ini sebagai ringkasan eksperimen terkini. Hasil lama yang metriknya keliru ditandai sebagai superseded dan tidak boleh dipakai sebagai temuan final.

## 1. Tujuan dan posisi eksperimen

TA membandingkan lima detektor YOLO skala nano pada subset Asia N-RDD2024, lalu mengamati generalisasi zero-shot ke beberapa ekspor dataset jalan Indonesia. Pertanyaan tambahan adalah apakah pelabelan `manhole` dan `patchy_road` sebagai kelas eksplisit membantu deteksi empat kelas kerusakan utama.

**Narasi hasil yang didukung data:** YOLO-RD memberi mAP tertinggi pada sumber; YOLOv8-PD paling cepat menurut hasil runtime yang tercatat; YOLOv12n memberi kompromi performa yang baik. Pada ablation jumlah kelas, hasil 4-kelas cenderung setara atau sedikit lebih baik pada empat kelas inti, tetapi selisih kecil dan belum diuji signifikansi. Pada target RDD-indo, semua model mengalami domain shift besar; YOLOv12n konsisten menjadi yang terbaik di antara lima model pada eksperimen zero-shot yang tercatat.

Eksperimen distractor/FP adalah **analisis sekunder opsional**, bukan dasar klaim utama. Jangan klaim bahwa kelas pengecoh terbukti meningkatkan atau menurunkan performa secara signifikan.

## 2. Dataset, label, dan protokol

### Dataset sumber
N-RDD2024 subset Asia menggunakan enam kelas:

1. `Longitudinal_Crack` (D00)
2. `Transverse_Crack` (D10)
3. `Alligator_Crack` (D20)
4. `Pothole` (D40)
5. `manhole` (D70; distractor)
6. `patchy_road` (D80; distractor)

Empat kelas pertama adalah kelas kerusakan inti; dua kelas terakhir adalah objek permukaan jalan yang dipilih untuk menguji hipotesis kemiripan visual dengan Pothole. Kelas N-RDD2024 lain tidak termasuk eksperimen ini.

| Split | Gambar | Instance 6 kelas | Instance setelah filter 4 kelas |
|---|---:|---:|---:|
| Train | 6.777 | 17.092 | 14.351 |
| Val | 1.898 | 4.773 | 3.996 |
| Test | 995 | 2.425 | 2.035 |

Distribusi per kelas (train/val/test): Longitudinal 4.555/1.257/635; Transverse 3.219/897/446; Alligator 4.385/1.245/642; Pothole 2.192/597/312; manhole 2.270/645/321; patchy road 471/132/69. `patchy_road` adalah kelas paling langka; rasio kelas terbesar/terkecil 6-kelas sekitar 9,67×, sedangkan rasio empat kelas inti sekitar 2,08×.

Sumber audit: `runs/rdd_yolov8n_local/dataset_split_summary.csv`, distribusi kelas di `runs/rdd_yolov8n_local/`; untuk label empat kelas lihat `runs/rdd_4class_local/dataset_split_summary_4cls.csv` dan `code/prepare_4class_dataset.py`.

### Konfigurasi training umum
Seed 42; imgsz 640; maksimal 300 epoch dengan early stopping patience 40; batch dan argumen lain harus dibaca dari `args.yaml` run masing-masing. Augmentasi utama: mosaic 1.0, mixup 0.05, fliplr 0.5, translate 0.10, scale 0.50, degrees 0.0. Penanganan imbalance yang aktif pada run final adalah class-balanced weighting berbasis Effective Number, β=0.999 (Cui et al., CVPR 2019), dengan patch `DetectionModel.init_criterion`; variabel atau sel Focal Loss lama dalam notebook tidak berarti Focal Loss aktif.

Evaluasi sumber utama: test set N-RDD2024, mAP50/mAP50-95, P/R, dan F1. Parameter evaluasi ada di notebook/run; konfigurasi yang tercatat memakai imgsz=640, conf=0.001, IoU NMS=0.6. Detail aktual per run di `runs/rdd_yolov8n_local/experiments/*/args.yaml` dan log di `docs/RESULTS.md`.

## 3. Hasil utama — model 6-kelas pada test sumber

| Model | Test mAP50 (6 kelas) | Test mAP50-95 | Macro-F1 (6 kelas) | FPS tercatat* |
|---|---:|---:|---:|---:|
| YOLOv8n | 0.648 | 0.364 | 0.617 | 219.7 |
| YOLOv12n | 0.654 | 0.371 | 0.619 | 319.3 |
| YOLOv26n | 0.625 | 0.358 | 0.606 | 293.3 |
| YOLOv8-PD | 0.646 | 0.362 | 0.627 | 368.4 |
| YOLO-RD | **0.661** | **0.371** | **0.633** | 189.4 |

*FPS adalah hasil pengukuran yang dicatat proyek pada perangkat/harness yang dilaporkan, bukan jaminan kecepatan deployment di hardware lain. YOLO-RD tertinggi pada mAP50 dan seri tertinggi pada mAP50-95 bersama YOLOv12n; YOLOv8-PD tercepat menurut angka FPS yang dicatat; YOLOv26n terendah dalam mAP50 pada resep bersama. Pothole adalah salah satu kelas inti dengan mAP50 relatif rendah (sekitar 0.526–0.541 pada model 6-kelas), tetapi jangan menyebutnya “paling sering tertukar dengan distractor” tanpa bukti tambahan.

**Peringatan kompleksitas:** angka parameter/GFLOPs di `docs/RESULTS_TABLE.md` tidak cocok dengan ringkasan model fused di `docs/RESULTS.md` (contoh YOLOv26n tercatat 2.506M/5.9 di tabel vs 2.376M/5.2 di log; YOLOv12n 2.569M/7.5 vs 2.558M/6.3). Jangan menyalin parameter/GFLOPs untuk paper sebelum dihitung/ditetapkan ulang dengan versi runtime dan bobot yang sama. FPS di atas juga perlu dicantumkan bersama hardware/protokol pengukurannya.

Hasil terperinci: `docs/RESULTS_TABLE.md`, `docs/RESULTS.md`, serta file per-kelas `runs/rdd_yolov8n_local/*_test_per_class_metrics.csv` dan direktori `runs/rdd_yolov8n_local/evaluation/`.

## 4. Ablation 6-kelas vs 4-kelas — perbandingan empat kelas inti

Perbandingan yang tepat adalah pada empat kelas yang sama, bukan membandingkan langsung mAP/F1 agregat 6 kelas dengan agregat 4 kelas. Nilai berikut adalah rata-rata mAP50 dari empat kelas inti; macro-F1 6-kelas dihitung ulang hanya pada empat kelas inti. Untuk tiga model 4-kelas non-PD, nilai hasil evaluasi dirujuk dari `docs/RESULTS_TABLE.md`; untuk YOLOv8-PD 4-kelas dipakai CSV per-kelas lokal.

| Arsitektur | 6-kelas: mAP50 4 inti | 4-kelas: mAP50 4 inti | Δ (4−6) | 6-kelas: macro-F1 4 inti | 4-kelas: macro-F1 | Δ F1 |
|---|---:|---:|---:|---:|---:|---:|
| YOLOv8n | 0.6224 | 0.6313 | +0.0089 | 0.602 | 0.602 | ~0.000 |
| YOLOv12n | 0.6264 | 0.6280 | +0.0016 | 0.602 | 0.606 | +0.004 |
| YOLOv26n | 0.6044 | 0.6038 | −0.0007 | 0.588 | 0.595 | +0.007 |
| YOLOv8-PD | 0.6233 | 0.6341 | +0.0108 | 0.6057 | 0.6167 | +0.011 |

mAP50 Pothole sendiri lebih tinggi pada model 4-kelas untuk keempat pasangan: v8n +0.020, v12n +0.001, v26n +0.024, v8-PD +0.011. Kesimpulan yang aman: pada satu seed/run, menghapus dua label distractor tidak menurunkan performa empat kelas inti; sebagian besar pasangan menunjukkan kenaikan kecil. Efek belum diuji dengan bootstrap, multi-seed, atau uji inferensial; jangan menyebutnya signifikan atau kausal. Sebagian hasil v8n/v12n/v26n 4-kelas berasal dari bobot PC lab yang dipindahkan ke `runs/rdd_4class_local/experiments/`; cek file run sebelum klaim kesetaraan lingkungan perangkat lunak.

Hasil tabel inti empat kelas: `docs/RESULTS_TABLE.md`. CSV 4-kelas YOLOv8-PD: `runs/rdd_4class_local/yolov8_pd_4cls_class_weights_test_per_class_metrics.csv`. Bobot/run: `runs/rdd_4class_local/experiments/<run>/`.

## 5. Generalisasi zero-shot ke RDD-indo

Lima bobot yang dilatih pada N-RDD2024 diuji tanpa fine-tuning dengan conf=0.001, IoU NMS=0.6, imgsz=640. Hasil mAP50 yang tercatat:

| Model | RDD-indo-v2 | RDD-indo-v3 | Folder RDD-indo-v4* |
|---|---:|---:|---:|
| YOLOv8n | 0.145 | 0.248 | 0.250 |
| YOLOv12n | **0.172** | **0.309** | **0.332** |
| YOLOv26n | 0.136 | 0.225 | 0.239 |
| YOLOv8-PD | 0.149 | 0.269 | 0.279 |
| YOLO-RD | 0.149 | 0.272 | 0.297 |

*Path lokal `data/RDD-indo-v4/` berisi Roboflow `rdd-indo-crop` version 3 menurut `data.yaml`/README. Hanya ada split valid berisi 307 gambar, 514 instance, lima kelas, tanpa manhole; split valid dipakai sebagai test karena tidak ada folder test. Remap target→kelas sumber: `{0:2, 1:0, 2:5, 3:3, 4:1}`. Jangan menyebut ini data yang diambil sendiri di Bandung tanpa konfirmasi provenance.

**Interpretasi:** mAP50 zero-shot target jauh di bawah sumber; YOLOv12n tertinggi di tiap ekspor yang tercatat. V2 mencakup 6 kelas termasuk hanya 4 GT manhole; v3/v4 mencakup 5 kelas dan tidak punya manhole, serta ukuran/split ekspor berbeda. Jadi angka antarexpors tidak apple-to-apple dan kenaikan v2→v3→v4 bukan bukti model membaik.

Untuk V3/V4, domain-gap CSV lama membandingkan mAP sumber 6 kelas dengan target yang tidak punya kelas manhole. Domain gap V4 yang sudah diperbarui (`domain_gap.csv`) kini menyertakan kolom mAP50 5 kelas bersama, macro-F1, dan weighted-F1 untuk sumber dan target:

| Model | Source mAP50 (5 kelas) | Target V4 mAP50 | Penurunan | Source macro-F1 | Target V4 macro-F1 | Penurunan macro | Source weighted-F1 | Target V4 weighted-F1 | Penurunan weighted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| YOLOv12n | 0.618 | **0.332** | 46.3% | 0.584 | **0.378** | 35.3% | 0.613 | **0.464** | 24.2% |
| YOLO-RD | 0.624 | 0.297 | 52.3% | 0.596 | 0.332 | 44.4% | 0.625 | 0.431 | 31.0% |
| YOLOv8-PD | 0.611 | 0.279 | 54.3% | 0.594 | 0.305 | 48.7% | 0.617 | 0.402 | 34.9% |
| YOLOv8n | 0.612 | 0.250 | 59.2% | 0.581 | 0.306 | 47.3% | 0.612 | 0.392 | 36.0% |
| YOLOv26n | 0.586 | 0.239 | 59.1% | 0.570 | 0.274 | 52.0% | 0.598 | 0.359 | 40.0% |

Catatan F1: weighted-F1 memberi bobot tiap kelas sesuai jumlah instance-nya (support), menghasilkan urutan identik dengan mAP50 (12n > RD > PD > 8n > 26n), karena volume Pothole dan patchy_road kecil sehingga efeknya minor. Macro-F1 agak berbeda (8n 0.306 vs PD 0.305 — praktis seri) karena macro memberi bobot sama pada patchy_road (support 22). Domain gap weighted-F1 (−24 s.d. −40%) lebih kecil dari macro-F1 (−35 s.d. −52%), yang berarti model kurang parah pada kelas dominan (Longitudinal) namun lebih parah pada kelas langka.

Nilai source 5-kelas dihitung sebagai rata-rata per kelas bersama dari `runs/rdd_yolov8n_local/*_test_per_class_metrics.csv`; target dari `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/zs_per_class_metrics.csv`. Ringkasan F1 di `zs_f1_summary.csv`. `domain_gap.csv` juga sudah diperbarui dengan kolom 5 kelas bersama dan F1 — lihat file langsung untuk angka eksak (3 desimal).

Untuk V4, metrik machine-readable lengkap ada di `domain_gap.csv`, `zs_f1_summary.csv`, `zs_per_class_metrics.csv` (P/R/F1/mAP50/mAP50-95 per kelas + evaluated boolean). File `zs_detail.csv` sudah dihapus karena duplikat parsial. Artefak visual target: `domain_gap.png`, `zs_samples_pred_only.png`, `zs_samples_gt_vs_pred.png`. Progres V3: `docs/progress/2026-10-01-zero-shot-indo-v3.md`. Catatan teknis: `Metric.class_result(i)` bersifat posisional terhadap `ap_class_index` (bukan class-id) — kelas tanpa GT dievaluasi sebagai `NaN` dan tidak dimasukkan rata-rata, konsisten dengan perilaku Ultralytics `all` mAP.

Prototipe zero-shot lebih lama ada di `code/05_zero_shot_indonesia.ipynb` dan `evaluation/zero_shot_indonesia/`; jangan campur dengan V2–V4. V2/V4 notebook tersedia di `code/05_zero_shot_indo_v2.ipynb` dan `code/05_zero_shot_indo_v4.ipynb`.

## 6. Analisis domain negara dan visualisasi fitur

- Per-country source evaluation: `code/06_per_country_analysis.ipynb`; output di `runs/rdd_yolov8n_local/per_country/` dan tabel `docs/RESULTS_TABLE.md`. Hasil mAP50 gabungan negara yang tercatat: China sekitar 0.869–0.907, Japan 0.546–0.594, India 0.426–0.443. Domain memiliki ukuran dan komposisi kelas berbeda; interpretasikan deskriptif, bukan efek kausal negara.
- Embedding/domain visualization: `code/07_domain_visualization.ipynb`, output `runs/rdd_yolov8n_local/evaluation/domain_viz/`, progres `docs/progress/2026-10-01-domain-viz.md`. Visualisasi t-SNE/UMAP dan statistik visual membantu mendeskripsikan perbedaan domain, tetapi tidak membuktikan sebab-akibat atau menyediakan jarak antardomain yang dapat dibaca langsung. Dataset Indo pada visualisasi memiliki 308 gambar; belum tentu persis ekspor V4 307 gambar.

## 7. FP proxy vs overlap — tambahan opsional

Notebook lama menghitung semua prediksi Pothole di gambar yang mengandung distractor; metrik tersebut adalah **proxy per gambar**, bukan salah-label objek. Tabel/p-value two-proportion z-test lama di `docs/rangkuman-eksperimen-ta.md` §3a tidak valid untuk klaim “manhole/patchy salah diprediksi sebagai Pothole” dan tidak dimasukkan sebagai hasil utama.

Analisis ulang test-only menggunakan conf=0.25, NMS IoU=0.6, syarat overlap IoU≥0.5; pada 272 gambar terdapat 321 GT manhole dan 69 GT patchy. Jumlah prediksi Pothole yang overlap salah satu GT distractor adalah 1–3 dari 8 model; rate TRUE gabungan 0.0026–0.0077 per 390 GT distractor. TRUE patchy = 0 pada seluruh model. Numerator adalah jumlah box prediksi yang overlap, bukan matching unik satu-ke-satu dengan GT; sebut metrik sebagai hitungan/rate overlap diagnostik, bukan recall unik objek.

Jika halaman terbatas, cukup satu catatan metode/hasil singkat atau pindahkan ke lampiran. Detail dan seluruh tabel: `docs/progress/2026-09-29-fp-proxy-vs-fp-overlap.md`; skrip `scripts/fp_overlap_table.py`; CSV `runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv`; visual contoh `runs/rdd_yolov8n_local/viz_fp_overlap_yolov8n_test.png` dari `scripts/viz_fp_overlap.py`.

## 8. Implementasi model dan sumber rujukan

- YOLOv8n, YOLOv12n, YOLOv26n: model Ultralytics nano/pretrained; untuk resep aktual cek `args.yaml` dan bobot `best.pt`.
- YOLOv8-PD: rekonstruksi lokal dari paper Zeng & Zhong; `code/models/yolov8-pd.yaml`, `code/models/custom_modules.py`; PDF `latex/refference/02_YOLOv8‑PD an improved road.pdf`; key BibTeX `Zeng2024`.
- YOLO-RD: rekonstruksi lokal dari Wang et al.; `code/models/yolo-rd.yaml`, `custom_modules.py`; PDF `latex/refference/04_YOLO RD A Road Damage Detection Method for Effective.pdf`; key `Wang2025`. MAF diimplementasikan sebagai pola Upsample–Concat–Conv1×1 sesuai catatan metodologi proyek.
- N-RDD2024: key `kaya2024nrdd2024`; RDD2022: `Arya2024846`; class-balanced loss: `cui2019class`; DCN: `dai2017deformable` di `latex/skripsi-telkom/References.bib`.
- Literatur manhole vs Pothole: Shi 2026 PDF lokal `latex/refference/05_A Lightweight Road Damage Detection Model based on Structural Improvement and Knowledge Distillation.pdf`, key `Shi_2026`; hasil audit klaim: `docs/progress/2026-10-02-cek-klaim-shi-2026.md`.
- PD/RD adalah rekonstruksi paper di Ultralytics, bukan reproduksi bit-exact kode penulis. Gunakan frasa “implementasi/rekonstruksi dalam penelitian ini” dan jangan mengklaim hasil mengonfirmasi mekanisme arsitektur secara kausal. Audit literatur/provenance: `outputs/yolo-road-damage-references.md` dan `outputs/yolo-road-damage-references.provenance.md`. Metadata/versi BibTeX YOLOv12/YOLO26 perlu diverifikasi sebelum naskah final.

## 9. Batas klaim dan pekerjaan yang belum selesai

1. Semua perbandingan performa adalah satu run/seed yang terdokumentasi; belum ada multi-seed, CI, bootstrap, atau uji signifikansi untuk beda mAP/F1.
2. Parameter/GFLOPs yang dilaporkan `RESULTS_TABLE.md` vs `RESULTS.md` perlu direkonsiliasi; FPS harus selalu disertai hardware dan protokol.
3. Perbedaan empat-vs-enam kelas hanya tren deskriptif; jangan menyebut 4 kelas unggul signifikan atau menyimpulkan mekanisme hard-negative secara kausal.
4. Proxy FP dan p-value lama bukan metrik salah-label; jangan tampilkan sebagai hasil utama.
5. Provenance target bernama RDD-indo-v4 harus ditulis sesuai metadata aktual (Roboflow `rdd-indo-crop` v3) dan dibedakan dari data Bandung yang direncanakan/disebut di sebagian file LaTeX.
6. Belum ada bukti bahwa ekspor Indo V2/V3/V4 merupakan benchmark yang sama; jangan mengadu nilai agregat antarekspor.
7. Pemeriksaan BibTeX/tahun YOLOv12 dan YOLO26 masih diperlukan sebelum sitasi final.

## 10. Peta file utama

| Tujuan | File/folder |
|---|---|
| Ringkasan sumber hasil utama | `docs/RESULTS_TABLE.md`, `docs/RESULTS.md` |
| Notebook komparasi 6-kelas | `code/03_3_modelling_comparative_local.ipynb` |
| Notebook/modeling 4-kelas | `code/04_1_modelling_4class.ipynb`–`code/04_4_modelling_4class.ipynb` |
| Bobot final 4-kelas | `runs/rdd_4class_local/experiments/*_4cls_class_weights/weights/best.pt` |
| Source per-class test metrics | `runs/rdd_yolov8n_local/*_test_per_class_metrics.csv` |
| 4-class PD per-class metrics | `runs/rdd_4class_local/yolov8_pd_4cls_class_weights_test_per_class_metrics.csv` |
| V2/V4 zero-shot code | `code/05_zero_shot_indo_v2.ipynb`, `code/05_zero_shot_indo_v4.ipynb` |
| V4 zero-shot results | `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/` (`domain_gap.csv`, `zs_f1_summary.csv`, `zs_per_class_metrics.csv`) |
| Country and feature analysis | `code/06_per_country_analysis.ipynb`, `code/07_domain_visualization.ipynb` |
| Progress logs | `docs/progress/2026-09-29-fp-proxy-vs-fp-overlap.md`, `2026-10-01-zero-shot-indo-v3.md`, `2026-10-01-domain-viz.md`, `2026-10-02-cek-klaim-shi-2026.md`, `2026-10-02-mcp-migrasi-bawaan.md`, `docx` 2026-10-08-zero-shot-v4-dan-f1-per-kelas.md |

**Instruksi untuk LLM penulis:** perlakukan angka dan file sumber di atas sebagai konteks proyek, bukan sitasi eksternal; gunakan test sebagai hasil final, val hanya untuk validasi/early stopping. Jika angka bertentangan, jangan memilih diam-diam—ikuti peringatan audit dan minta rekonsiliasi. Jangan memasukkan seluruh analisis proxy FP kecuali diperlukan dan halaman tersedia.
