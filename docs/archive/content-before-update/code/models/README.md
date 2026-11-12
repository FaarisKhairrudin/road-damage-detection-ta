# YOLOv8-PD & YOLO-RD (reconstructions)

Reimplementasi arsitektur dari dua paper:

1. Zeng, J. & Zhong, H. **"YOLOv8-PD: an improved road damage detection algorithm
   based on YOLOv8n model."** *Scientific Reports* 14, 12052 (2024).
   https://doi.org/10.1038/s41598-024-62933-z
2. Wang, W. et al. **"YOLO-RD: A Road Damage Detection Method for Effective
   Pavement Maintenance."** *Sensors* 25, 1442 (2025).
   https://doi.org/10.3390/s25051442

## Status kode resmi

**Tidak ada satu pun dari kedua paper ini yang merilis kode arsitekturnya.**

- YOLOv8-PD: *Data availability* cuma menunjuk ke `github.com/sekilab/RoadDamageDetector`
  (repo **dataset** RDD2022, bukan kode). Kontak resmi: `z.h0912@163.com`.
- YOLO-RD: *Data Availability* juga cuma menunjuk ke repo dataset yang sama.
  Implementation Details di paper malah bilang mereka pakai **MMYOLO/MMDetection**
  untuk training (bukan Ultralytics resmi), jadi arsitekturnya "terinspirasi
  YOLOv8" tapi tidak 1:1 dengan struktur internal Ultralytics. Kontak resmi:
  `wangwei@ccu.edu.cn`.

Kedua model di folder ini direkonstruksi dari figure + persamaan matematis di
masing-masing paper, di atas framework Ultralytics (bukan MMYOLO), supaya
satu pipeline training/eval bisa dipakai untuk semua model pembanding kamu.

## Isi folder ini

- `custom_modules.py` — **satu file untuk kedua model** (sesuai permintaan):
  - YOLOv8-PD: **BoT**, **LSKA**, **C2fGhost**, **LSCDHead**
  - YOLO-RD: **SOM** (Star Operation Module), **ARM** (Attention Refinement
    Module, pakai deformable conv dari torchvision), **WTConv**/**WTHead**
    (Wavelet Transform Convolution, dekomposisi Haar wavelet asli, bukan
    aproksimasi)
  - `patch_ultralytics()` — satu fungsi yang mendaftarkan SEMUA modul di atas
    (dari kedua paper) ke parser YAML Ultralytics. Panggil sekali di awal,
    dipakai untuk kedua yaml.
- `yolov8-pd.yaml` — arsitektur YOLOv8-PD (Figure 2 paper 1).
- `yolo-rd.yaml` — arsitektur YOLO-RD (Figure 2 paper 2).
- `train_example.py` — contoh training (tinggal ganti path yaml-nya).

## Cara pakai

```bash
pip install ultralytics torchvision
```

```python
from custom_modules import patch_ultralytics
patch_ultralytics()          # WAJIB sebelum YOLO(...) dipanggil, untuk KEDUA model

from ultralytics import YOLO
model = YOLO("yolo-rd.yaml", task="detect")       # atau "yolov8-pd.yaml"
model.train(data="data.yaml", epochs=200, imgsz=640)
```

Ganti `nc:` di masing-masing yaml sesuai jumlah kelas dataset kamu.

## Validasi yang sudah saya lakukan (kedua model)

| | YOLOv8-PD | YOLO-RD |
|---|---|---|
| Build dari yaml | ✅ | ✅ |
| Forward pass (train & eval mode) | ✅ | ✅ |
| `v8DetectionLoss` + backward pass | ✅ | ✅ (gradient sampai ke ARM & WTHead) |
| Params/GFLOPs (`n` scale, 4 kelas) | ~2.46M / ~7.7 GFLOPs | ~7.09M / ~12.9 GFLOPs |
| Params/GFLOPs dilaporkan paper (`n` utk PD, `s` utk RD, 4 kelas) | 2.3M / 6.1 GFLOPs | 20.89M / 20.28 GFLOPs |

YOLO-RD jauh lebih besar dari basis `n`-nya dibanding YOLOv8-PD relatif ke
basisnya — ini konsisten dengan naratif kita sebelumnya: YOLO-RD memang
didesain "akurasi-first" (menambah beban komputasi), jadi walau di-rescale
ke `n`, dia tetap proporsional lebih berat dibanding modul-modul YOLOv8-PD
yang memang didesain untuk seringan mungkin.

### Bug yang ditemukan & diperbaiki: segfault di ARM

Saat testing, `model.info()` (yang menghitung GFLOPs pakai library `thop`)
**crash (segfault)** — bukan error Python biasa, tapi C-level crash yang
mematikan seluruh proses. Setelah ditelusuri pakai `faulthandler`, penyebabnya:
Ultralytics menghitung GFLOPs dengan `torch.empty(...)` (memori yang **belum
diinisialisasi**, bisa berisi angka acak ekstrem/`NaN`/`Inf`), dan kernel
CPU `deform_conv2d` milik torchvision ternyata tidak aman terhadap nilai
offset yang ekstrem — dia crash alih-alih menangani secara graceful. Ini bug
di torchvision, bukan di desain ARM itu sendiri. Sudah saya perbaiki dengan
`torch.clamp()` + `nan_to_num()` di dalam `ARM.forward()` sebelum masuk ke
`deform_conv2d`, dan sudah diverifikasi tidak crash lagi (termasuk dites
eksplisit dengan input `NaN`). Poin ini saya sebutkan supaya kalau kamu nanti
memodifikasi ARM, jangan hapus clamp-nya — itu bukan sekadar precaution,
tapi fix untuk crash yang benar-benar terjadi.

## Batasan penting & keputusan interpretasi — baca sebelum dipakai

Sama seperti YOLOv8-PD, ini **rekonstruksi dari gambar & rumus paper, bukan
kode asli**. Untuk YOLO-RD, karena papernya justru cukup eksplisit memberi
persamaan (Eq 1-10), sebagian besar bisa direkonstruksi cukup presisi:

- **SOM** (Eq 1-3): diimplementasikan mengikuti alur matematis persis
  (DWConv→BN→dua cabang 1×1 (satu digerbang ReLU6)→perkalian elemen→1×1→BN→
  DWConv→residual→1×1 akhir).
- **ARM** (Eq 5-7): pakai deformable convolution asli (`torchvision.ops.DeformConv2d`),
  bukan aproksimasi.
- **WTC** (Eq 8-10): pakai **transformasi wavelet Haar asli** (matematika
  eksak, bukan aproksimasi), dengan konvolusi kecil per sub-band frekuensi
  dan rekonstruksi invers, sesuai Fig 5.
- **Satu penyimpangan yang perlu kamu tahu**: modul "MAF" di paper (Eq 4) itu
  weighted-sum eksplisit (`Σαᵢ·F_stagei`, dengan `Σαᵢ=1`) antar level fitur.
  Saya realisasikan bagian ini dengan pola **Upsample→Concat→Conv1×1** standar
  (sudah dipakai di semua neck YOLOv8) alih-alih modul khusus dengan softmax
  weight — karena secara matematis Concat+Conv1×1 itu strictly lebih umum
  (bisa merepresentasikan kombinasi linear per-channel apa pun, termasuk
  convex combination), dan ini menjaga arsitektur tetap sederhana & konsisten
  dengan seluruh neck lain di studi kamu. Ini pilihan desain yang saya buat
  sadar, bukan kelalaian — tapi tetap sebutkan di metodologi kalau reviewer/
  dosen bertanya soal fidelity terhadap Eq 4.
- Detail lain yang tidak dijelaskan lengkap di paper (lebar channel persis di
  ARM/WTC, jumlah level dekomposisi wavelet — saya set 2 sesuai Fig 5, dll)
  saya isi dengan pilihan yang masuk akal dan konsisten dengan teks + gambar.

Angka mAP yang kamu dapat dari kedua model ini **kemungkinan besar tidak
akan persis sama** dengan yang dilaporkan di paper, meskipun arsitekturnya
setara secara struktural. Untuk metodologi TA, sebutkan eksplisit bahwa
kedua model adalah "reimplementasi berdasarkan arsitektur yang dipublikasikan
(kode tidak tersedia)".

## Kompatibilitas versi

Ditest dan berhasil dengan `ultralytics==8.4.114`, `torch==2.6.0+cu124`,
`torchvision==0.21.0+cu124`, Python 3.12. Versi minimum yang didukung adalah
`8.4.108` (karena `parse_model` versi ini yang menjadi basis
`_patched_parse_model`). Requirements di `code/requirements_yolov8_local.txt`
sudah dipin ke `ultralytics>=8.4.108`.

Fungsi `_patched_parse_model` di `custom_modules.py` adalah salinan dimodifikasi
dari `ultralytics.nn.tasks.parse_model` — kalau kamu pakai versi ultralytics
lain dan dapat error saat `patch_ultralytics()` / build model, kemungkinan
besar karena `parse_model` di versi itu sudah berubah strukturnya. Lihat
catatan di akhir `custom_modules.py` untuk cara memperbaikinya.

### Perbaikan yang sudah diverifikasi (smoke test 2 epoch, mini dataset)

| Model | Training | Validation |
|---|---|---|
| YOLOv8n + focal loss | OK | OK |
| YOLOv8-PD + pretrained + focal loss | OK | OK |
| YOLO-RD + pretrained + focal loss | OK | OK |

Dua bug yang ditemukan dan diperbaiki:

1. **`WTConv` gagal pada feature map ganjil.** Wavelet Haar stride-2 hanya
   lossless untuk dimensi genap. Saat `imgsz` menghasilkan feature map ganjil
   (misal 10x10 -> 5x5 -> 2x2), inverse wavelet tidak bisa merekonstruksi
   ukuran asli. Guard di `WTConv.forward` sekarang memerlukan dimensi genap
   sebelum dekomposisi.
2. **`MHSA` lazy position embedding merusak EMA.** Posisi embedding di-build
   ulang saat ukuran feature map berubah, sehingga parameter berubah bentuk di
   tengah training dan memutus optimizer/EMA Ultralytics. Sekarang embedding
   dibuat sekali di `__init__` berukuran `max_hw=64` lalu di-slice saat forward.

