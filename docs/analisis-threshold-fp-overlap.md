# Analisis Threshold Tabel FP/GT Pothole vs Pengecoh

Tanggal: 2026-10-09

Catatan: dokumen ini hanya catatan eksplorasi. Tabel dan angka di draf belum diubah.

## Latar Belakang

Tabel FP/GT pothole yang dipakai di draf memakai conf=0,25 dan IoU match 0,5. Pertanyaannya apakah angka berubah bila threshold diturunkan atau dinaikkan.

Metode: satu kali inferensi pada conf=0,001 (iou NMS 0,60, imgsz 640) untuk 5 model 6-kelas pada 272 citra test berpengecoh. Semua prediksi Pothole disimpan bersama IoU maksimumnya terhadap GT manhole dan patchy_road, lalu tabel dihitung ulang untuk tiap kombinasi threshold.

Penyebut tetap jumlah GT pengecoh: manhole 321, patchy_road 69, gabungan 390. Nilai di tabel adalah jumlah prediksi Pothole yang menimpa pengecoh (bukan rate).

Jumlah prediksi Pothole mentah (conf>=0,001) per model:

| Model | Prediksi Pothole |
|---|---|
| yolov8n_6cls | 1420 |
| yolov12n_6cls | 1321 |
| yolov26n_6cls | 1198 |
| yolov8_pd_6cls | 1244 |
| yolo_rd_6cls | 878 |

## Gabungan (manhole + patchy) (penyebut 390)

### IoU match >= 0,3

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 34 | 39 | 39 | 20 | 27 |
| 0,01 | 12 | 11 | 5 | 5 | 13 |
| 0,05 | 6 | 6 | 5 | 5 | 9 |
| 0,1 | 5 | 5 | 2 | 4 | 7 |
| 0,25 | 4 | 4 | 2 | 3 | 3 |
| 0,5 | 1 | 1 | 0 | 1 | 2 |

### IoU match >= 0,5

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 21 | 24 | 30 | 8 | 18 |
| 0,01 | 8 | 7 | 4 | 3 | 9 |
| 0,05 | 4 | 4 | 4 | 3 | 6 |
| 0,1 | 3 | 3 | 1 | 3 | 5 |
| 0,25 | 3 | 2 | 1 | 2 | 3 |
| 0,5 | 1 | 1 | 0 | 1 | 2 |

### IoU match >= 0,7

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 5 | 7 | 24 | 3 | 10 |
| 0,01 | 2 | 3 | 4 | 2 | 4 |
| 0,05 | 1 | 2 | 4 | 2 | 3 |
| 0,1 | 0 | 2 | 1 | 2 | 2 |
| 0,25 | 0 | 2 | 1 | 1 | 1 |
| 0,5 | 0 | 1 | 0 | 1 | 0 |

## Manhole (penyebut 321)

### IoU match >= 0,3

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 29 | 35 | 30 | 19 | 24 |
| 0,01 | 11 | 9 | 5 | 5 | 11 |
| 0,05 | 5 | 6 | 5 | 5 | 8 |
| 0,1 | 5 | 5 | 2 | 4 | 6 |
| 0,25 | 4 | 4 | 2 | 3 | 3 |
| 0,5 | 1 | 1 | 0 | 1 | 2 |

### IoU match >= 0,5

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 18 | 23 | 21 | 8 | 16 |
| 0,01 | 7 | 6 | 4 | 3 | 7 |
| 0,05 | 3 | 4 | 4 | 3 | 5 |
| 0,1 | 3 | 3 | 1 | 3 | 4 |
| 0,25 | 3 | 2 | 1 | 2 | 3 |
| 0,5 | 1 | 1 | 0 | 1 | 2 |

### IoU match >= 0,7

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 4 | 6 | 16 | 3 | 9 |
| 0,01 | 1 | 2 | 4 | 2 | 3 |
| 0,05 | 0 | 2 | 4 | 2 | 2 |
| 0,1 | 0 | 2 | 1 | 2 | 1 |
| 0,25 | 0 | 2 | 1 | 1 | 1 |
| 0,5 | 0 | 1 | 0 | 1 | 0 |

## Patchy road (penyebut 69)

### IoU match >= 0,3

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 5 | 4 | 9 | 1 | 3 |
| 0,01 | 1 | 2 | 0 | 0 | 2 |
| 0,05 | 1 | 0 | 0 | 0 | 1 |
| 0,1 | 0 | 0 | 0 | 0 | 1 |
| 0,25 | 0 | 0 | 0 | 0 | 0 |
| 0,5 | 0 | 0 | 0 | 0 | 0 |

### IoU match >= 0,5

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 3 | 1 | 9 | 0 | 2 |
| 0,01 | 1 | 1 | 0 | 0 | 2 |
| 0,05 | 1 | 0 | 0 | 0 | 1 |
| 0,1 | 0 | 0 | 0 | 0 | 1 |
| 0,25 | 0 | 0 | 0 | 0 | 0 |
| 0,5 | 0 | 0 | 0 | 0 | 0 |

### IoU match >= 0,7

| conf | yolov8n_6cls | yolov12n_6cls | yolov26n_6cls | yolov8_pd_6cls | yolo_rd_6cls |
|---|---|---|---|---|---|
| 0,001 | 1 | 1 | 8 | 0 | 1 |
| 0,01 | 1 | 1 | 0 | 0 | 1 |
| 0,05 | 1 | 0 | 0 | 0 | 1 |
| 0,1 | 0 | 0 | 0 | 0 | 1 |
| 0,25 | 0 | 0 | 0 | 0 | 0 |
| 0,5 | 0 | 0 | 0 | 0 | 0 |

## Cara Baca

Baris conf adalah ambang keyakinan minimum yang dipertahankan. Kolom adalah model. Nilai adalah jumlah prediksi pothole yang menumpuk pada pengecoh pada IoU match yang tercantum.

Makin kecil conf makin banyak prediksi yang ikut dihitung sehingga jumlah tumpang tindih hampir pasti naik. Makin besar IoU match makin ketat definisi tumpang tindih sehingga jumlahnya turun.
