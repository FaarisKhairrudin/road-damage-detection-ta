# 2026-10-08 — Audit eksperimen RDD-indo-v4 dan penyusunan konteks final

## Diskusi / tujuan
Pengguna meminta ringkasan eksperimen final yang rapi sebagai konteks untuk LLM penulis paper, bukan draf paper. Permintaan eksplisit: buat sebagai `docs/rangkuman-eksperimen-ta-v2.md`, jangan menimpa `docs/rangkuman-eksperimen-ta.md`; hasil proxy FP menjadi catatan tambahan opsional karena batas halaman; sertakan file sumber kode, hasil, log progress, dan referensi.

## Audit sumber kode, hasil, dan dataset
- Model utama: training/evaluasi dirujuk oleh `code/03_3_modelling_comparative_local.ipynb`, `code/04_1_modelling_4class.ipynb` s.d. `code/04_4_modelling_4class.ipynb`, `code/prepare_4class_dataset.py`, dan `code/models/{yolov8-pd.yaml,yolo-rd.yaml,custom_modules.py}`.
- Konfigurasi run tersimpan per eksperimen pada `runs/rdd_yolov8n_local/experiments/*/args.yaml` dan `runs/rdd_4class_local/experiments/*/args.yaml`; args aktual lebih otoritatif daripada konstanta/daftar model yang tertinggal di beberapa sel notebook. Umumnya seed 42, imgsz 640, maksimal 300 epoch, patience 40; lihat args setiap run.
- Loss aktif: class-balanced weighting berdasarkan Effective Number, beta=0.999 (Cui et al. CVPR 2019), diverifikasi lewat patch `DetectionModel.init_criterion`. Variabel/sel Focal Loss lama di notebook bukan bukti Focal Loss dipakai pada run final.
- Dataset sumber statistik: `runs/rdd_yolov8n_local/dataset_split_summary.csv` (6.777/1.898/995 gambar train/val/test; 17.092/4.773/2.425 objek) dan distribusi kelas. 4-kelas dihasilkan dengan menyaring label `manhole` dan `patchy_road`; split gambar tetap sama, lihat `runs/rdd_4class_local/dataset_split_summary_4cls.csv` dan `code/prepare_4class_dataset.py`.
- RDD-indo-v4 lokal berisi **307** citra dan 307 label di `valid/`, 39 label kosong, 514 instance; lima kelas, tanpa manhole. Hitungan diverifikasi dari filesystem. Penting: path repo bernama `data/RDD-indo-v4/`, tetapi `data.yaml` dan `README.roboflow.txt` menyatakan proyek Roboflow `rdd-indo-crop`, version **3**, diekspor 2026-10-07; jangan menyebutnya versi dataset ke-4 atau dataset Bandung yang dikumpulkan sendiri tanpa provenance tambahan. Tidak ada folder test fisik; notebook menggunakan valid sebagai test zero-shot.

## Hasil RDD-indo-v4
Kode: `code/05_zero_shot_indo_v4.ipynb`; finishing/recompute parsial: `scripts/run_zs_v4_finish.py`. Model sumber diuji tanpa fine-tuning pada isi valid RDD-indo-v4 setelah remap nama kelas ke indeks sumber; conf=0.001, NMS IoU=0.6, imgsz=640.

mAP50 target yang tercatat di `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/domain_gap.csv`:

| Model | mAP50 RDD-indo-v4 |
|---|---:|
| yolov12n | 0.3323 |
| yolo_rd | 0.2975 |
| yolov8_pd | 0.2790 |
| yolov8n | 0.2497 |
| yolov26n | 0.2395 |

v12n tertinggi pada semua eksperimen target v2/v3/v4 yang tercatat. Namun v2 (308 citra, 6 kelas, hanya 4 GT manhole di test), v3 (308, 5 kelas, tanpa manhole), dan v4 (307, 5 kelas, tanpa manhole) berbeda pada versi, label, ukuran/split; **jangan menyimpulkan tren peningkatan antar-versi dataset dari mAP agregatnya**. V3 didokumentasikan di `docs/progress/2026-10-01-zero-shot-indo-v3.md`; notebook v3 tidak ditemukan di workspace saat audit ini, jadi rujukan hasil v3 yang tersedia adalah log dan artefak.

### Koreksi perbandingan domain yang harus dipertahankan
`domain_gap.csv` lama membandingkan mAP sumber 6 kelas dengan target v3/v4 yang tidak memiliki manhole (Ultralytics menghitung kelas target yang berlabel); ini bukan perbandingan kelas yang sepenuhnya sepadan. Untuk V4, mAP sumber dihitung ulang sebagai rata-rata mAP50 **lima kelas bersama** dari `runs/rdd_yolov8n_local/*_class_weight_test_per_class_metrics.csv`, lalu dibandingkan dengan mAP50 target:

| Model | Source mAP50, 5 kelas bersama | Target V4 | Δ target−source | Δ relatif |
|---|---:|---:|---:|---:|
| yolov8n | 0.6121 | 0.2497 | −0.3625 | −59.2% |
| yolov12n | 0.6184 | 0.3323 | −0.2861 | −46.3% |
| yolov26n | 0.5860 | 0.2395 | −0.3465 | −59.1% |
| yolov8_pd | 0.6110 | 0.2790 | −0.3320 | −54.3% |
| yolo_rd | 0.6238 | 0.2975 | −0.3264 | −52.3% |

Ini derived calculation dari per-class source CSV + `domain_gap.csv`, bukan kolom yang ada dalam CSV domain gap sekarang. Jangan salin gap lama sebagai head-to-head 5 kelas tanpa menjelaskan denominator/kelas berbeda.

`zs_detail.csv` menyimpan P/R/mAP untuk yolov8n dan yolov12n; untuk yolo_rd, yolov8_pd, yolov26n hanya mAP50 tersimpan karena `run_zs_v4_finish.py` mengimpor mAP terdahulu dari CSV. Jangan laporkan P/R atau mAP50-95 untuk ketiga model tersebut dari file ini tanpa memeriksa output notebook/log lain.

## Konteks domain shift / negara
- `code/07_domain_visualization.ipynb`, artefak `runs/rdd_yolov8n_local/evaluation/domain_viz/`; eksperimen menggunakan embedding YOLOv8n, t-SNE/UMAP, statistik citra, dan grid contoh domain. Log: `docs/progress/2026-10-01-domain-viz.md`.
- Hasil visual/fitur bersifat eksploratif, bukan bukti kausal atau ukuran jarak yang dapat ditafsirkan langsung. Set Indo di visualisasi berjumlah 308, sehingga jangan otomatis menyamakannya dengan ekspor V4 307 gambar.
- Analisis mAP per negara: `code/06_per_country_analysis.ipynb`, tabel di `docs/RESULTS_TABLE.md` dan hasil `runs/rdd_yolov8n_local/per_country/`. Perbedaan komposisi kelas dan ukuran domain membatasi interpretasi kausal.

## Hasil perbandingan kelas 4 vs 6
- Ringkasan agregat final 6 kelas: `docs/RESULTS_TABLE.md`, log rinci `docs/RESULTS.md`. 6-kelas: YOLO-RD tertinggi mAP50=0.661 dan mAP50-95=0.371; YOLOv8-PD paling ringan/tercepat pada pengukuran terlapor (2.46M, 368.4 FPS); YOLOv12n mAP50=0.654, mAP50-95=0.371; YOLOv26n terendah pada resep bersama (mAP50=0.625). Catatan custom PD/RD direkonstruksi dari paper, bukan replikasi dengan kode resmi; MAF pada RD disederhanakan; jangan menyatakan metrik membuktikan teori arsitektur secara kausal.
- Perbandingan yang adil untuk efek jumlah kelas adalah empat kelas kerusakan bersama, bukan mAP aggregate 6 kelas vs 4 kelas. Nilai mAP50 rata-rata empat kelas inti (sumber: `RESULTS_TABLE.md` per-kelas 6cls/4cls; PD-4cls: `runs/rdd_4class_local/yolov8_pd_4cls_class_weights_test_per_class_metrics.csv`):

| Arsitektur | 6cls, mAP50-4 inti | 4cls, mAP50-4 inti | Δ 4cls−6cls | Macro-F1 6cls-4 inti | Macro-F1 4cls | Δ F1 |
|---|---:|---:|---:|---:|---:|---:|
| v8n | 0.6224 | 0.6313 | +0.0089 | 0.602 | 0.602 | ~0.000 |
| v12n | 0.6264 | 0.6280 | +0.0016 | 0.602 | 0.606 | +0.004 |
| v26n | 0.6044 | 0.6038 | −0.0007 | 0.588 | 0.595 | +0.007 |
| v8-PD | 0.6233 | 0.6341 | +0.0108 | 0.6057 | 0.6167 | +0.011 |

Pothole mAP50 4cls lebih tinggi pada keempat pasangan (+0.020, +0.001, +0.024, +0.011); efeknya kecil dan belum diuji inferensial. Deskripsikan sebagai tren pada satu seed, bukan bukti signifikan bahwa kelas pengecoh merugikan. 4-class final weights v8n/v12n/v26n dipindahkan dari `runs/rdd_4class_local_pc_lab/` ke local pada 2026-10-01; model final sekarang ada.

## Tambahan FP proxy — non-utama, opsional
- Investigasi + bug/solusi sudah terdokumentasi di `docs/progress/2026-09-29-fp-proxy-vs-fp-overlap.md`; skrip `scripts/fp_overlap_table.py`, data `runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv`; visual yolov8n `scripts/viz_fp_overlap.py` dan `viz_fp_overlap_yolov8n_test.png`.
- Metrik notebook lama adalah proxy per-gambar, bukan salah-label box. Two-proportion z-test lama pada proxy **tidak boleh digunakan untuk klaim salah-label**.
- Test-only, conf=0.25, NMS IoU=0.6, true-overlap IoU≥0.5; 272 citra mengandung distractor, GT manhole=321, patchy=69. TRUE Gab per model berjangkau 0.0026–0.0077 (1–3 prediksi Pothole overlap / 390 GT distractor); TRUE Patchy=0 seluruh model. Hasil ini diagnostik sekunder saja; hitungan overlap bukan matching satu-ke-satu unik per GT.

## Referensi primer / kode yang relevan untuk penulis
- Dataset N-RDD2024: `latex/skripsi-telkom/References.bib` key `kaya2024nrdd2024`; data lokal `data/NRDD-2024/`.
- RDD2022: key `Arya2024846`; PDF `latex/refference/01_RDD2022 A multi‐national image dataset.pdf`.
- YOLOv8-PD: key `Zeng2024`; PDF `latex/refference/02_YOLOv8‑PD an improved road.pdf`; implementasi lokal `code/models/yolov8-pd.yaml` + `custom_modules.py`.
- YOLO-RD: key `Wang2025`; PDF `latex/refference/04_YOLO RD A Road Damage Detection Method for Effective.pdf`; implementasi lokal `code/models/yolo-rd.yaml` + `custom_modules.py`.
- Class-Balanced Effective Number: key `cui2019class` (Cui et al., CVPR 2019); DCN dasar custom RD: `dai2017deformable`.
- Motivasi manhole-vs-pothole: key `Shi_2026`, PDF lokal `latex/refference/05_A Lightweight Road Damage Detection Model based on Structural Improvement and Knowledge Distillation.pdf`; verifikasi/corrections dicatat di `docs/progress/2026-10-02-cek-klaim-shi-2026.md`.
- YOLOv12/YOLO26 keys saat ini `tian2026yolov12` / `sapkota2025yolo26`; audit referensi di `outputs/yolo-road-damage-references.md` mencatat bahwa metadata/versi sitasi perlu diperiksa sebelum paper final.

## Solusi / status dokumentasi
- Eksperimen FP proxy/overlap **sudah** punya progress log (tidak perlu diduplikasi).
- Audit ini menambahkan log V4 dan koreksi perbandingan kelas bersama; rangkuman konteks final dibuat sebagai file baru `docs/rangkuman-eksperimen-ta-v2.md`. File lama `docs/rangkuman-eksperimen-ta.md` tidak ditimpa.
