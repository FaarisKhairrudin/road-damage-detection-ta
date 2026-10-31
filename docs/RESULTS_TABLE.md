# Hasil Evaluasi Model — Rangkuman Tabel

Rangkuman rapih dari `RESULTS.md`. Nilai diambil persis dari log Ultralytics, tidak diubah.

## ***Ringkasan Model (Overall / Semua Kelas)***

Perbandingan metrik agregat (`all`) pada validasi (val) dan test, beserta estimasi kecepatan inferensi test, jumlah parameter, dan GFLOPs (nc=6, imgsz=640).

| Model | Params | GFLOPs | val P | val R | val mAP50 | val mAP50-95 | test P | test R | test mAP50 | test mAP50-95 | FPS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| yolov8n_class_weight | 3,012,018 | 8.2 | 0.684 | 0.598 | 0.657 | 0.365 | 0.643 | 0.599 | 0.648 | 0.364 | 219.7 |
| yolov12n_class_weight | 2,569,218 | 7.5 | 0.669 | 0.600 | 0.656 | 0.368 | 0.638 | 0.608 | 0.654 | 0.371 | 319.3 |
| yolov26n_class_weight | 2,506,140 | 5.9 | 0.681 | 0.572 | 0.633 | 0.360 | 0.642 | 0.580 | 0.625 | 0.358 | 293.3 |
| yolov8_pd_class_weight | 2,459,509 | 7.7 | 0.677 | 0.604 | 0.651 | 0.366 | 0.675 | 0.591 | 0.646 | 0.362 | 368.4 |
| yolo_rd_class_weight | 7,092,392 | 12.9 | 0.679 | 0.614 | 0.663 | 0.374 | 0.655 | 0.618 | 0.661 | 0.371 | 189.4 |

Catatan: YOLO-RD (7.09M params / 12.9 GFLOPs) lebih berat dari YOLOv8n (3.01M / 8.2) namun lebih ringan dari YOLOv8s (11.14M / 28.7) — berada di antara keduanya. YOLOv8-PD (2.46M / 7.7) bahkan lebih ringan dari YOLOv8n.

## ***Per-Kelas mAP50 — Val (Full 6 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | manhole | patchy_road | Overall (avg) |
|---|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.637 | 0.586 | 0.684 | 0.570 | 0.801 | 0.665 | 0.657 |
| yolov12n_class_weight | 0.656 | 0.595 | 0.672 | 0.568 | 0.791 | 0.654 | 0.656 |
| yolov26n_class_weight | 0.625 | 0.544 | 0.654 | 0.550 | 0.772 | 0.654 | 0.633 |
| yolov8_pd_class_weight | 0.656 | 0.593 | 0.663 | 0.555 | 0.785 | 0.655 | 0.651 |
| yolo_rd_class_weight | 0.658 | 0.620 | 0.670 | 0.561 | 0.793 | 0.675 | 0.663 |

## ***Per-Kelas mAP50 — Test (Full 6 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | manhole | patchy_road | Overall (avg) |
|---|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.664 | 0.599 | 0.700 | 0.526 | 0.825 | 0.571 | 0.648 |
| yolov12n_class_weight | 0.680 | 0.582 | 0.708 | 0.535 | 0.833 | 0.587 | 0.654 |
| yolov26n_class_weight | 0.639 | 0.567 | 0.675 | 0.538 | 0.820 | 0.512 | 0.625 |
| yolov8_pd_class_weight | 0.678 | 0.572 | 0.702 | 0.541 | 0.819 | 0.562 | 0.646 |
| yolo_rd_class_weight | 0.696 | 0.608 | 0.701 | 0.527 | 0.845 | 0.587 | 0.661 |

## ***Per-Kelas mAP50 — Val (4 Kelas Kerusakan Asli)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_class_weight | 0.637 | 0.586 | 0.684 | 0.570 | 0.619 |
| yolov12n_class_weight | 0.656 | 0.595 | 0.672 | 0.568 | 0.623 |
| yolov26n_class_weight | 0.625 | 0.544 | 0.654 | 0.550 | 0.593 |
| yolov8_pd_class_weight | 0.656 | 0.593 | 0.663 | 0.555 | 0.617 |
| yolo_rd_class_weight | 0.658 | 0.620 | 0.670 | 0.561 | 0.627 |

## ***Per-Kelas mAP50 — Test (4 Kelas Kerusakan Asli)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_class_weight | 0.664 | 0.599 | 0.700 | 0.526 | 0.622 |
| yolov12n_class_weight | 0.680 | 0.582 | 0.708 | 0.535 | 0.626 |
| yolov26n_class_weight | 0.639 | 0.567 | 0.675 | 0.538 | 0.605 |
| yolov8_pd_class_weight | 0.678 | 0.572 | 0.702 | 0.541 | 0.623 |
| yolo_rd_class_weight | 0.696 | 0.608 | 0.701 | 0.527 | 0.633 |

## ***Ringkasan F1 (Macro & Weighted)***

| Model | val macro F1 | val weighted F1 | test macro F1 | test weighted F1 |
|---|---|---|---|---|
| yolov8n_class_weight | 0.636 | 0.632 | 0.617 | 0.636 |
| yolov12n_class_weight | 0.631 | 0.631 | 0.619 | 0.637 |
| yolov26n_class_weight | 0.620 | 0.617 | 0.606 | 0.622 |
| yolov8_pd_class_weight | 0.638 | 0.633 | 0.627 | 0.640 |
| yolo_rd_class_weight | 0.644 | 0.640 | 0.633 | 0.650 |

## ***Ringkasan Model — Training 4 Kelas (nc=4)***

Eksperimen terpisah: model dilatih langsung hanya pada 4 kelas kerusakan utama (tanpa manhole & patchy_road). Model non-modifikasi (nc=4, imgsz=640). YOLO-RD 4-kelas tersedia sebagai artefak final (`runs/rdd_4class_local/experiments/yolo_rd_4cls_class_weights/`, best.pt 9 Okt 2026, protokol sama: seed 42, 300 epoch, batch 16).

| Model | Params | GFLOPs | val P | val R | val mAP50 | val mAP50-95 | test P | test R | test mAP50 | test mAP50-95 | FPS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| yolov8n_4cls_class_weights | 3,006,428 | 8.1 | 0.646 | 0.557 | 0.612 | 0.310 | 0.644 | 0.566 | 0.631 | 0.314 | 329.4 |
| yolov12n_4cls_class_weights | 2,557,508 | 6.3 | 0.647 | 0.576 | 0.626 | 0.320 | 0.640 | 0.577 | 0.628 | 0.319 | 329.4 |
| yolov26n_4cls_class_weights | 2,375,616 | 5.2 | 0.674 | 0.528 | 0.587 | 0.303 | 0.654 | 0.549 | 0.604 | 0.313 | 263.1 |
| yolov8_pd_4cls_class_weights | — | — | 0.650 | 0.560 | 0.613 | 0.307 | 0.661 | 0.580 | 0.634 | 0.319 | 130.4† |
| yolo_rd_4cls_class_weights | — | — | 0.653 | 0.574 | 0.626 | 0.318 | 0.659 | 0.584 | 0.651 | 0.331 | 94.3† |

†Params/GFLOPs tidak tercatat di artefak run; FPS = project-recorded estimate (bukan edge benchmark), protokol timing belum kanonis — sama seperti run 6-kelas.

## ***Per-Kelas mAP50 — Val (Training 4 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_4cls_class_weights | 0.644 | 0.591 | 0.664 | 0.548 | 0.612 |
| yolov12n_4cls_class_weights | 0.645 | 0.616 | 0.690 | 0.554 | 0.626 |
| yolov26n_4cls_class_weights | 0.617 | 0.551 | 0.655 | 0.523 | 0.587 |
| yolov8_pd_4cls_class_weights | 0.651 | 0.600 | 0.662 | 0.540 | 0.613 |
| yolo_rd_4cls_class_weights | 0.666 | 0.606 | 0.681 | 0.552 | 0.626 |

## ***Per-Kelas mAP50 — Test (Training 4 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_4cls_class_weights | 0.679 | 0.595 | 0.705 | 0.546 | 0.631 |
| yolov12n_4cls_class_weights | 0.680 | 0.593 | 0.703 | 0.536 | 0.628 |
| yolov26n_4cls_class_weights | 0.640 | 0.537 | 0.676 | 0.562 | 0.604 |
| yolov8_pd_4cls_class_weights | 0.676 | 0.598 | 0.711 | 0.552 | 0.634 |
| yolo_rd_4cls_class_weights | 0.699 | 0.608 | 0.715 | 0.582 | 0.651 |

## ***Ringkasan F1 (Macro & Weighted) — Training 4 Kelas***

| Model | val macro F1 | val weighted F1 | test macro F1 | test weighted F1 |
|---|---|---|---|---|
| yolov8n_4cls_class_weights | 0.598 | 0.606 | 0.602 | 0.617 |
| yolov12n_4cls_class_weights | 0.608 | 0.618 | 0.606 | 0.620 |
| yolov26n_4cls_class_weights | 0.592 | 0.602 | 0.595 | 0.606 |
| yolov8_pd_4cls_class_weights | 0.601 | 0.611 | 0.617 | 0.630 |
| yolo_rd_4cls_class_weights | 0.610 | 0.620 | 0.617 | 0.629 |

## ***Per-Negara mAP50 — Test (Semua Model)***

Test N-RDD2024 dipecah per negara via prefix nama file (`China_*` 180 citra, `Japan_*` 705 citra, `India_*` 110 citra), dievaluasi tiap bobot (conf=0.001, iou=0.6, imgsz=640). Dihasilkan oleh `code/06_per_country_analysis.ipynb`; heatmap di `runs/rdd_yolov8n_local/per_country/per_country_heatmap.png`. Kolom Indonesia V4\* berasal dari uji zero-shot tanpa fine-tuning (lihat bagian ***Hasil Zero-Shot RDD-indo-v4*** di bawah).

| Model | China | Japan | India | Indonesia V4* | Gabungan |
|---|---|---:|---:|---:|
| yolov8n_class_weight | 0.883 | 0.581 | 0.426 | 0.253 | 0.648 |
| yolov12n_class_weight | 0.890 | 0.587 | 0.433 | **0.337** | 0.654 |
| yolov26n_class_weight | 0.869 | 0.546 | 0.443 | 0.249 | 0.625 |
| yolov8_pd_class_weight | 0.907 | 0.570 | 0.438 | 0.286 | 0.646 |
| yolo_rd_class_weight | 0.892 | 0.594 | 0.442 | 0.302 | 0.661 |

\*Indonesia V4: 5 kelas bersama (tanpa manhole), 307 citra, 502 instance (V4 FINAL); angka China/Japan/Gabungan = agregat Ultralytics 6 kelas, India = 5 kelas (manhole n=1, patchy n=0). Perbandingan bersifat indikatif; untuk antar-negara yang apple-to-apple pakai agregat 4 kelas inti (`main.tex` Tabel country-four / draft §4.4).

### ***Per-Kelas per Negara — China***

| Model | Longitudinal | Transverse | Alligator | Pothole | manhole | patchy_road |
|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.875 | 0.918 | 0.946 | 0.984 | 0.581 | 0.995 |
| yolov12n_class_weight | 0.900 | 0.911 | 0.959 | 0.962 | 0.616 | 0.995 |
| yolov26n_class_weight | 0.879 | 0.913 | 0.953 | 0.986 | 0.486 | 0.995 |
| yolov8_pd_class_weight | 0.918 | 0.925 | 0.975 | 0.995 | 0.634 | 0.995 |
| yolo_rd_class_weight | 0.903 | 0.934 | 0.947 | 0.995 | 0.581 | 0.995 |

### ***Per-Kelas per Negara — Japan***

| Model | Longitudinal | Transverse | Alligator | Pothole | manhole | patchy_road |
|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.545 | 0.494 | 0.689 | 0.582 | 0.843 | 0.331 |
| yolov12n_class_weight | 0.559 | 0.471 | 0.690 | 0.595 | 0.850 | 0.359 |
| yolov26n_class_weight | 0.488 | 0.456 | 0.654 | 0.573 | 0.832 | 0.272 |
| yolov8_pd_class_weight | 0.517 | 0.451 | 0.684 | 0.615 | 0.845 | 0.306 |
| yolo_rd_class_weight | 0.579 | 0.489 | 0.690 | 0.589 | 0.874 | 0.344 |

### ***Per-Kelas per Negara — India***

| Model | Longitudinal | Transverse | Alligator | Pothole | manhole (n=1) | patchy_road (n=0) |
|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.273 | 0.038 | 0.501 | 0.323 | 0.995 | — |
| yolov12n_class_weight | 0.234 | 0.056 | 0.539 | 0.341 | 0.995 | — |
| yolov26n_class_weight | 0.282 | 0.002 | 0.526 | 0.408 | 0.995 | — |
| yolov8_pd_class_weight | 0.244 | 0.129 | 0.507 | 0.314 | 0.995 | — |
| yolo_rd_class_weight | 0.184 | 0.214 | 0.494 | 0.325 | 0.995 | — |

## ***Distribusi Train per Negara vs Akurasi***

| Negara | Train citra | Longitudinal | Transverse | Alligator | Pothole | manhole | patchy_road | Total instance | Test mAP50 (v8n ultra) |
|---|---|---|---|---|---|---|---|---|---|
| Japan | 4624 | 2250 | 2385 | 3449 | 1270 | 2139 | 260 | 11753 | 0.581 |
| China | 1423 | 1942 | 815 | 460 | 191 | 123 | 208 | 3739 | 0.883 |
| India | 730 | 363 | 19 | 476 | 731 | 8 | 3 | 1600 | 0.426 |

Catatan: volume train tidak menjelaskan peringkat (Japan 3x China tapi kalah jauh) — kesulitan domain yang menjelaskan. Tautan representasi terbersih: Transverse India (19 instance train → 0.038 test). Sel India manhole (n=1) dan patchy_road (n=0) tidak bisa diklaim. Kolom Test mAP50 di atas = agregat Ultralytics bobot v8n (India 0.426 = 5 kelas, terdongkrak 1 GT manhole 0.995); agregat 4-kelas inti India = 0.284 — lihat draft §4.4 / `main.tex` Tabel country-four.

## ***Hasil Zero-Shot RDD-indo-v4***

Uji tanpa fine-tuning (conf=0.001, iou=0.6, imgsz=640) pada RDD-indo-v4 (307 citra, 502 instance, 5 kelas tanpa manhole — V4 FINAL). Sumber perbandingan: rata-rata mAP50 5 kelas bersama dari dataset sumber. Sumber angka: `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/domain_gap.csv` (`zs_per_class_metrics.csv`, `zs_f1_summary.csv`).

### ***Ringkasan (mAP50 + F1)***

| Model | Source mAP50 (6 cls) | Source mAP50 (5 cls) | Target V4 mAP50 | Penurunan | Source macro-F1 | Target V4 macro-F1 | Penurunan macro | Source weighted-F1 | Target V4 weighted-F1 | Penurunan weighted |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| yolov12n_class_weight | 0.654 | 0.618 | **0.337** | 45.5% | 0.584 | **0.383** | 34.5% | 0.613 | **0.471** | 23.1% |
| yolo_rd_class_weight | 0.661 | 0.624 | 0.302 | 51.6% | 0.596 | 0.336 | 43.6% | 0.625 | 0.440 | 29.6% |
| yolov8_pd_class_weight | 0.646 | 0.611 | 0.286 | 53.3% | 0.594 | 0.312 | 47.4% | 0.640 | 0.412 | 35.6% |
| yolov8n_class_weight | 0.648 | 0.612 | 0.253 | 58.6% | 0.581 | 0.308 | 46.9% | 0.612 | 0.397 | 35.1% |
| yolov26n_class_weight | 0.625 | 0.586 | 0.249 | 57.5% | 0.571 | 0.281 | 50.8% | 0.598 | 0.370 | 38.1% |

### ***Per-Kelas mAP50 — Target V4***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | patchy_road |
|---|---:|---:|---:|---:|---:|
| yolov12n_class_weight | **0.629** | **0.256** | **0.506** | **0.260** | 0.036 |
| yolo_rd_class_weight | 0.585 | 0.275 | 0.468 | 0.107 | **0.075** |
| yolov8_pd_class_weight | 0.558 | 0.217 | 0.442 | 0.149 | 0.062 |
| yolov8n_class_weight | 0.525 | 0.214 | 0.352 | 0.119 | 0.057 |
| yolov26n_class_weight | 0.534 | 0.157 | 0.296 | 0.218 | 0.039 |

Catatan: `manhole` tidak dievaluasi (0 GT di target). Angka sumber 5-kelas dihitung dari file per-class CSV source; target dari `zs_per_class_metrics.csv` (V4 FINAL, 502 instance). Dataset: `data/RDD-indo-v4` (Roboflow `rdd-indo-crop` v3, hanya split valid). Lihat `docs/progress/2026-10-08-zero-shot-v4-dan-f1-per-kelas.md` untuk detail metodologis dan bug `class_result` posisional.
