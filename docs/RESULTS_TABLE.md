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

Eksperimen terpisah: model dilatih langsung hanya pada 4 kelas kerusakan utama (tanpa manhole & patchy_road). Model non-modifikasi (nc=4, imgsz=640).

| Model | Params | GFLOPs | val P | val R | val mAP50 | val mAP50-95 | test P | test R | test mAP50 | test mAP50-95 | FPS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| yolov8n_4cls_class_weights | 3,006,428 | 8.1 | 0.646 | 0.557 | 0.612 | 0.310 | 0.644 | 0.566 | 0.631 | 0.314 | 329.4 |
| yolov12n_4cls_class_weights | 2,557,508 | 6.3 | 0.647 | 0.576 | 0.626 | 0.320 | 0.640 | 0.577 | 0.628 | 0.319 | 329.4 |
| yolov26n_4cls_class_weights | 2,375,616 | 5.2 | 0.674 | 0.528 | 0.587 | 0.303 | 0.654 | 0.549 | 0.604 | 0.313 | 263.1 |

## ***Per-Kelas mAP50 — Val (Training 4 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_4cls_class_weights | 0.644 | 0.591 | 0.664 | 0.548 | 0.612 |
| yolov12n_4cls_class_weights | 0.645 | 0.616 | 0.690 | 0.554 | 0.626 |
| yolov26n_4cls_class_weights | 0.617 | 0.551 | 0.655 | 0.523 | 0.587 |

## ***Per-Kelas mAP50 — Test (Training 4 Kelas)***

| Model | Longitudinal_Crack | Transverse_Crack | Alligator_Crack | Pothole | Overall (avg) |
|---|---|---|---|---|---|
| yolov8n_4cls_class_weights | 0.679 | 0.595 | 0.705 | 0.546 | 0.631 |
| yolov12n_4cls_class_weights | 0.680 | 0.593 | 0.703 | 0.536 | 0.628 |
| yolov26n_4cls_class_weights | 0.640 | 0.537 | 0.676 | 0.562 | 0.604 |

## ***Ringkasan F1 (Macro & Weighted) — Training 4 Kelas***

| Model | val macro F1 | val weighted F1 | test macro F1 | test weighted F1 |
|---|---|---|---|---|
| yolov8n_4cls_class_weights | 0.598 | 0.606 | 0.602 | 0.617 |
| yolov12n_4cls_class_weights | 0.608 | 0.618 | 0.606 | 0.620 |
| yolov26n_4cls_class_weights | 0.592 | 0.602 | 0.595 | 0.606 |
