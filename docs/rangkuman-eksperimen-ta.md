# Rangkuman & Analisis Eksperimen Sementara
## Deteksi Kerusakan Jalan — Perbandingan Model YOLO

*Dokumen ini merangkum hasil eksperimen dan keputusan metodologis sampai titik ini. Disusun sebagai catatan kerja, bukan draf bab TA.*

---

## 1. Desain Eksperimen

### Dataset
- **N-RDD2024** (pengembangan dari RDD2022) — total 10 kelas tersedia, **6 kelas dipakai**:
  - 4 kelas kerusakan inti: `Longitudinal_Crack` (D00), `Transverse_Crack` (D10), `Alligator_Crack` (D20), `Pothole` (D40)
  - 2 kelas pengecoh (*distractor*): `manhole` (D70), `patchy_road` (D80) — dipilih karena literatur melaporkan kemiripan visual keduanya terhadap Pothole
- Kelas lain (D30 repaired cracks, D50/D60 blur, D90 rutting) **tidak dipakai** — di luar scope pertanyaan riset (bukan soal kemiripan dengan Pothole)

### Distribusi Data (instance)

| Kelas | Train | Val | Test | Total | % |
|---|---|---|---|---|---|
| Longitudinal_Crack | 4555 | 1257 | 635 | 6447 | 26.54 |
| Transverse_Crack | 3219 | 897 | 446 | 4562 | 18.78 |
| Alligator_Crack | 4385 | 1245 | 642 | 6272 | 25.82 |
| Pothole | 2192 | 597 | 312 | 3101 | 12.77 |
| manhole | 2270 | 645 | 321 | 3236 | 13.32 |
| patchy_road | 471 | 132 | 69 | 672 | 2.77 |

**Catatan penting:**
- Split **stratified dengan rapi** (~70/20/10% konsisten di semua kelas) → kekuatan metodologis, sebut di bab metodologi
- Rasio imbalance: **9.67×** untuk 6 kelas (didorong `patchy_road`), tapi hanya **2.08×** untuk 4 kelas inti → imbalance sebenarnya **ringan** di eksperimen utama
- `manhole` (3236) sebenarnya **bukan kelas langka** — sebanding dengan Pothole (3101)
- `patchy_road` (471 train) **genuinely langka** → sumber utama keterbatasan statistik di eksperimen distractor

### Konfigurasi Training
- Skala **nano (`n`) untuk semua model** — keputusan sadar agar perbandingan apple-to-apple (mencegah confounding antara desain arsitektur vs kapasitas model)
- 300 epoch, imgsz 640, `optimizer="auto"`, `cos_lr=True`, `amp=True`, `deterministic=True`
- Augmentasi: mosaic 1.0, mixup 0.05, fliplr 0.5, translate 0.10, scale 0.50, **degrees 0.0** (tanpa rotasi, sesuai arahan dospem)
- **Loss**: class-balanced weighting via *Effective Number of Samples* — Cui et al., CVPR 2019 ([arXiv:1901.05555](https://arxiv.org/abs/1901.05555)), β=0.999

---

## 2. Hasil Utama — Perbandingan 5 Model (nc=6)

| Model | Params | GFLOPs | test mAP50 | test mAP50-95 | macro F1 | FPS |
|---|---|---|---|---|---|---|
| **YOLO-RD** | 7.09M | 12.9 | **0.661** 🥇 | **0.371** 🥇 | **0.633** 🥇 | 189.4 (terlambat) |
| YOLOv12n | 2.57M | 7.5 | 0.654 | 0.371 | 0.619 | 319.3 |
| YOLOv8n *(baseline)* | 3.01M | 8.2 | 0.648 | 0.364 | 0.617 | 219.7 |
| YOLOv8-PD | **2.46M** | 7.7 | 0.646 | 0.362 | 0.627 | **368.4** 🥇 |
| YOLOv26n | 2.51M | 5.9 | 0.625 ⬇ | 0.358 ⬇ | 0.606 ⬇ | 293.3 |

### Analisis Trade-off — narasi utama TA

Kedua model modifikasi **membuktikan filosofi desain paper aslinya masing-masing**:

- **YOLO-RD** (desain *akurasi-first*, sengaja menambah beban komputasi) → akurasi terbaik di semua metrik, tapi terberat (7.09M params) & terlambat (189 FPS). Sesuai klaim paper.
- **YOLOv8-PD** (desain *efisiensi-first*) → **teringan (2.46M) dan tercepat (368 FPS, 68% lebih cepat dari baseline)** dengan akurasi praktis setara baseline (0.646 vs 0.648). Sesuai klaim paper.
- **YOLOv26n** konsisten **terjelek di semua metrik**. Hipotesis: resep training generik (`optimizer="auto"`) tidak cocok — YOLO26 didesain untuk dipasangkan dengan MuSGD + ProgLoss + STAL. Plus arsitekturnya DFL-free (regresi box pakai L1 polos), butuh adaptasi hyperparameter berbeda. → laporkan sebagai **limitasi eksperimen**, bukan kegagalan model.

### Insight per-kelas: Pothole adalah kelas tersulit
mAP50 Pothole konsisten ~0.53 di semua model — **lebih rendah** dari Longitudinal (0.64–0.70) dan Alligator (0.68–0.71), bahkan sering di bawah `patchy_road`. Konsisten dengan temuan paper YOLOv8-PD asli ("D40/potholes akurasi terendah karena objek kecil & sampel sedikit"). Pothole **sulit dua kali lipat**: sulit dideteksi sendiri + paling sering tertukar dengan distractor.

---

## 3. Eksperimen Sekunder — Efek Kelas Pengecoh (4-kelas vs 6-kelas)

**Pertanyaan**: apakah melabeli objek pengecoh secara eksplisit mengurangi false-positive Pothole terhadap objek tersebut?
**Scope**: 3 model (YOLOv8n, YOLOv12n, YOLOv26n) — PD & RD tidak dijalankan karena keterbatasan waktu (4–6 jam/model)

### 3a. False-positive rate (evaluasi val+test gabungan)

| Model | Kelas | 6cls rate | 4cls rate | p-value | Signifikan? |
|---|---|---|---|---|---|
| yolov8n | manhole | 18.3% | 21.4% | 0.087 | tidak (*mendekati*) |
| yolov8n | patchy_road | 36.3% | 37.3% | 0.836 | tidak |
| yolov12n | manhole | 19.7% | 17.7% | 0.267 | tidak |
| yolov12n | patchy_road | 34.8% | 31.3% | 0.458 | tidak |
| yolov26n | manhole | 19.9% | 20.7% | 0.651 | tidak |
| yolov26n | patchy_road | 40.3% | 41.3% | 0.839 | tidak |

*Uji: two-proportion z-test. N: manhole=966, patchy_road=201 (val+test gabungan).*

**Kesimpulan**: tidak ada perbedaan signifikan (p>0.05) di seluruh kombinasi. Hanya `yolov8n`/`manhole` yang mendekati ambang (p=0.087) — sinyal lemah bahwa efeknya (jika ada) kecil dan mungkin arsitektur-spesifik.

**Catatan metodologis**: val dipakai untuk early stopping (`patience`), jadi penggabungan val+test berpotensi sedikit optimistis. Namun karena early stopping memilih berdasarkan mAP keseluruhan (bukan metrik confusion spesifik ini), dan ini analisis diagnostik sekunder (bukan klaim utama), risikonya minor. Hasil test-only sebelumnya juga sama-sama tidak signifikan → kesimpulan robust.

### 3b. Biaya terhadap mAP kelas inti (temuan tandingan)

Selisih mAP50 test, 6cls-dilatih (dievaluasi subset 4 kelas) vs 4cls-dilatih-langsung:

| Model | Longitudinal | Transverse | Alligator | **Pothole** |
|---|---|---|---|---|
| yolov8n | −0.015 | +0.004 | −0.005 | **−0.020** |
| yolov12n | 0.000 | −0.011 | +0.005 | **−0.001** |
| yolov26n | −0.001 | +0.030 | −0.001 | **−0.024** |

**Pola**: mAP Pothole **turun konsisten arah** pada 2 dari 3 model (−0.020, −0.024).

**Penjelasan mekanisme**: `manhole` & `patchy_road` dipilih justru karena mirip Pothole. Menambahkannya sebagai kelas eksplisit memaksa TAL assigner membedakan Pothole dari dua tetangga visualnya — batas keputusan Pothole jadi lebih ketat, yang bisa sedikit mengorbankan metrik Pothole itu sendiri.

**⚠️ Kejujuran statistik**: selisih mAP ini **tidak diuji signifikansinya** (butuh bootstrap per-gambar atau multi-seed untuk confidence interval). Laporkan sebagai *tren yang diamati*, bukan klaim terbukti.

### 3c. Gambaran lengkap eksperimen distractor

> **Belum terbukti untung** (penurunan FP tidak signifikan) **+ ada indikasi rugi kecil** (mAP Pothole turun, 2/3 model) — dengan catatan keduanya berada dalam rentang efek yang kecil.

Ini narasi dua sisi yang jauh lebih kaya daripada sekadar "tidak ada efek", dan didapat **tanpa training tambahan** — murni dari analisis lebih dalam terhadap data yang sudah ada.

---

## 4. Bug yang Ditemukan & Diperbaiki (penting untuk bab metodologi)

Karena YOLOv8-PD & YOLO-RD **direkonstruksi dari paper tanpa kode resmi**, ada beberapa bug yang ditemukan lewat proses validasi:

| # | Bug | Dampak | Fix |
|---|---|---|---|
| 1 | **Segfault di `deform_conv2d`** saat hitung GFLOPs | Proses training mati total (C-level crash, bukan exception Python) | `clamp()` + `nan_to_num()` pada offset sebelum masuk kernel torchvision |
| 2 | **`init_criterion` di-patch level instance** | Focal Loss / class_weights **tidak pernah aktif** saat training (Trainer membangun ulang objek model) | Patch di level **class** `DetectionModel`, bukan instance |
| 3 | **`FocalLoss` bawaan Ultralytics mereduksi ke scalar** | Normalisasi `/target_scores_sum` rusak → cls_loss collapse ke ~1e-6 | (Tidak dipakai — beralih ke class_weights) |
| 4 | **`E2ELoss` vs `v8DetectionLoss`** | YOLOv26 (`end2end=True`) error `KeyError: 'boxes'` | Pertahankan branching asli: `E2ELoss` jika `end2end`, else `v8DetectionLoss` |
| 5 | **ARM: `offset_conv` tidak di-zero-init** | YOLO-RD anjlok ke mAP50 ~0.50 (terjelek) — sampling spasial acak sejak step 0 | `nn.init.zeros_()` pada weight & bias (praktik standar DCN/DCNv2) |
| 6 | **WTConv: ukuran ganjil** | `RuntimeError` size mismatch saat Haar wavelet decompose/recompose | Pad ke genap sebelum tiap level, crop balik persis setelah inverse |

**Dampak fix #5 + #6**: YOLO-RD naik dari **terjelek (~0.50 mAP50)** → **terbaik (0.661 mAP50)**. Ini bukti proses validasi kode yang ketat — worth ditulis eksplisit di TA.

---

## 5. Keputusan Metodologis & Alasannya

| Keputusan | Alasan |
|---|---|
| Semua model di skala **nano** | Mencegah confounding desain arsitektur vs kapasitas model |
| **5 model** (bukan 3 atau 6) | Cakupan: baseline + 2 modifikasi domain-spesifik (kutub efisiensi & akurasi) + 2 SOTA umum |
| **Class weights**, bukan Focal Loss | Lebih tepat sasaran untuk imbalance antar-kelas; Focal Loss didesain untuk masalah background-vs-foreground ala RetinaNet yang sudah banyak teratasi oleh TAL di YOLOv8+ |
| **Effective Number**, bukan inverse-frequency mentah | Inverse-frequency bisa meledak (73× pada contoh literatur) → tidak stabil dengan AMP. Effective Number ~3.16× untuk rasio serupa |
| **Tidak** menjalankan eksperimen 5-kelas terpisah | Bottleneck-nya ukuran test set, bukan konfigurasi training — memecah eksperimen tidak menambah N |
| **Tidak** menyitir paper REG | Preprint tanpa peer-review, tabel hasil tanpa baseline pembanding, salah label "GFL", matematika berat yang tak pernah dipakai di eksperimennya sendiri |

---

## 6. Limitasi yang Perlu Ditulis

1. **Rekonstruksi, bukan kode resmi** — YOLOv8-PD & YOLO-RD dibangun dari figure/persamaan paper; angka mAP tidak akan persis sama dengan yang dipublikasikan
2. **MAF disederhanakan** — Eq.4 (weighted sum dengan Σα=1) direalisasikan sebagai Upsample→Concat→Conv1×1
3. **Reproducibility YOLO-RD tidak bit-exact** — backward `deform_conv2d` tidak deterministik di PyTorch (limitasi library)
4. **YOLOv26n tidak pakai resep training aslinya** (MuSGD/ProgLoss/STAL)
5. **Eksperimen distractor kurang statistical power** — `patchy_road` hanya 201 instance evaluasi
6. **Eksperimen distractor hanya 3 model** — PD & RD tidak dijalankan (keterbatasan waktu 4–6 jam/model)
7. **Single-seed** — tidak ada confidence interval untuk selisih mAP antar model

---

## 7. Langkah Berikutnya

- [ ] **Uji domain shift zero-shot ke data Indonesia** ← fokus utama TA, prioritas tertinggi untuk sisa compute
- [ ] Ukur **latency/FPS aktual** di hardware yang sama untuk semua model (batch=1, imgsz=640) — idealnya juga di perangkat edge jika ada akses
- [ ] (Opsional, jika data per-instance tersedia) Uji **McNemar** untuk eksperimen distractor — lebih tepat untuk desain berpasangan, power lebih tinggi
- [ ] (Future work, bukan sekarang) Desain faktorial penuh distractor: tanpa / manhole-saja / patchy-saja / keduanya

---

## 8. Referensi Kunci

- Zeng, J. & Zhong, H. (2024). *YOLOv8-PD: an improved road damage detection algorithm based on YOLOv8n model.* **Scientific Reports** 14, 12052. https://doi.org/10.1038/s41598-024-62933-z
- Wang, W. et al. (2025). *YOLO-RD: A Road Damage Detection Method for Effective Pavement Maintenance.* **Sensors** 25, 1442. https://doi.org/10.3390/s25051442
- Cui, Y., Jia, M., Lin, T-Y., Song, Y., & Belongie, S. (2019). *Class-Balanced Loss Based on Effective Number of Samples.* **CVPR 2019**. https://arxiv.org/abs/1901.05555
- Dai, J. et al. (2017). *Deformable Convolutional Networks.* **ICCV 2017** — dasar praktik zero-init offset
- Arya, D. et al. (2024). *RDD2022: A multi-national image dataset for automatic road damage detection.* **Geoscience Data Journal** 11, 846–862
