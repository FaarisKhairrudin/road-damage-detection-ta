# Hasil Evaluasi Model — Rangkuman Tabel

Rangkuman rapih dari `RESULTS.md`. Nilai diambil persis dari log Ultralytics, tidak diubah.

## ***Ringkasan Model (Overall / Semua Kelas)***

Perbandingan metrik agregat (`all`) pada validasi (val) dan test, beserta estimasi kecepatan inferensi test.

| Model | val P | val R | val mAP50 | val mAP50-95 | test P | test R | test mAP50 | test mAP50-95 | FPS |
|---|---|---|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.684 | 0.598 | 0.657 | 0.365 | 0.643 | 0.599 | 0.648 | 0.364 | 219.7 |
| yolov12n_class_weight | 0.669 | 0.600 | 0.656 | 0.368 | 0.638 | 0.608 | 0.654 | 0.371 | 319.3 |
| yolov26n_class_weight | 0.681 | 0.572 | 0.633 | 0.360 | 0.642 | 0.580 | 0.625 | 0.358 | 293.3 |
| yolov8_pd_class_weight | 0.677 | 0.604 | 0.651 | 0.366 | 0.675 | 0.591 | 0.646 | 0.362 | 368.4 |
| yolo_rd_class_weight | 0.520 | 0.506 | 0.493 | 0.225 | 0.504 | 0.524 | 0.500 | 0.234 | 280.8 |

## ***Per-Kelas mAP50 — Val (Full 6 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | manhole | patchy_road | Overall (avg) |
|---|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.637 | 0.586 | 0.684 | 0.570 | 0.801 | 0.665 | 0.657 |
| yolov12n_class_weight | 0.656 | 0.595 | 0.672 | 0.568 | 0.791 | 0.654 | 0.656 |
| yolov26n_class_weight | 0.625 | 0.544 | 0.654 | 0.550 | 0.772 | 0.654 | 0.633 |
| yolov8_pd_class_weight | 0.656 | 0.593 | 0.663 | 0.555 | 0.785 | 0.655 | 0.651 |
| yolo_rd_class_weight | 0.460 | 0.405 | 0.403 | 0.539 | 0.769 | 0.383 | 0.493 |

## ***Per-Kelas mAP50 — Test (Full 6 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | manhole | patchy_road | Overall (avg) |
|---|---|---|---|---|---|---|---|
| yolov8n_class_weight | 0.664 | 0.599 | 0.700 | 0.526 | 0.825 | 0.571 | 0.648 |
| yolov12n_class_weight | 0.680 | 0.582 | 0.708 | 0.535 | 0.833 | 0.587 | 0.654 |
| yolov26n_class_weight | 0.639 | 0.567 | 0.675 | 0.538 | 0.820 | 0.512 | 0.625 |
| yolov8_pd_class_weight | 0.678 | 0.572 | 0.702 | 0.541 | 0.819 | 0.562 | 0.646 |
| yolo_rd_class_weight | 0.478 | 0.408 | 0.446 | 0.526 | 0.823 | 0.318 | 0.500 |

## ***Per-Kelas mAP50 — Val (4 Kelas Kerusakan Asli)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_class_weight | 0.637 | 0.586 | 0.684 | 0.570 | 0.619 |
| yolov12n_class_weight | 0.656 | 0.595 | 0.672 | 0.568 | 0.623 |
| yolov26n_class_weight | 0.625 | 0.544 | 0.654 | 0.550 | 0.593 |
| yolov8_pd_class_weight | 0.656 | 0.593 | 0.663 | 0.555 | 0.617 |
| yolo_rd_class_weight | 0.460 | 0.405 | 0.403 | 0.539 | 0.452 |

## ***Per-Kelas mAP50 — Test (4 Kelas Kerusakan Asli)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_class_weight | 0.664 | 0.599 | 0.700 | 0.526 | 0.622 |
| yolov12n_class_weight | 0.680 | 0.582 | 0.708 | 0.535 | 0.626 |
| yolov26n_class_weight | 0.639 | 0.567 | 0.675 | 0.538 | 0.605 |
| yolov8_pd_class_weight | 0.678 | 0.572 | 0.702 | 0.541 | 0.623 |
| yolo_rd_class_weight | 0.478 | 0.408 | 0.446 | 0.526 | 0.465 |

## ***Ringkasan F1 (Macro & Weighted)***

| Model | val macro F1 | val weighted F1 | test macro F1 | test weighted F1 |
|---|---|---|---|---|
| yolov8n_class_weight | 0.636 | 0.632 | 0.617 | 0.636 |
| yolov12n_class_weight | 0.631 | 0.631 | 0.619 | 0.637 |
| yolov26n_class_weight | 0.620 | 0.617 | 0.606 | 0.622 |
| yolov8_pd_class_weight | 0.638 | 0.633 | 0.627 | 0.640 |
| yolo_rd_class_weight | 0.510 | 0.501 | 0.512 | 0.523 |
