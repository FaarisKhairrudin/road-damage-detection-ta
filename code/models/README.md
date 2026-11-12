# Rekonstruksi YOLOv8-PD dan YOLO-RD

Folder ini berisi dua reimplementasi lokal untuk perbandingan dengan YOLOv8n, YOLOv12n dan YOLO26n pada penelitian TA. Rujukan desain:

1. Zeng dan Zhong, *YOLOv8-PD: an improved road damage detection algorithm based on YOLOv8n model*, Scientific Reports 14, 12052 (2024), [DOI](https://doi.org/10.1038/s41598-024-62933-z).
2. Wang et al., *YOLO-RD: A Road Damage Detection Method for Effective Pavement Maintenance*, Sensors 25, 1442 (2025), [DOI](https://doi.org/10.3390/s25051442).

Ini adalah kode penelitian lokal yang merekonstruksi pilihan desain dari paper, bukan kode resmi penulis atau reproduksi identik. Status publikasi kode upstream terbaru tidak diaudit kembali pada pembaruan dokumentasi ini. Hasil dan kompleksitas implementasi lokal tidak boleh dianggap sama dengan angka paper referensi.

## Berkas dan penggunaan

| Berkas | Peran |
|---|---|
| `custom_modules.py` | Modul kedua model serta patch parser Ultralytics |
| `yolov8-pd.yaml` | Arsitektur lokal PD: BoT, LSKA, C2fGhost dan LSCDHead |
| `yolo-rd.yaml` | Arsitektur lokal RD: SOM, ARM dengan deformable convolution, dan wavelet head |
| `train_example.py` | Contoh konstruksi/training; bukan resep lengkap run final |

Panggil `patch_ultralytics()` sebelum membangun model YAML atau memuat checkpoint custom. Checkpoint penelitian menyimpan nama modul Python `custom_modules`, sehingga path modul perlu tetap tersedia.

Contoh konstruksi berikut dijalankan dari `code/models/`, bukan contoh training final:

```python
from custom_modules import patch_ultralytics
patch_ultralytics()

from ultralytics import YOLO
model = YOLO("yolo-rd.yaml", task="detect")
```

Untuk training final, ikuti notebook bertahap dan `args.yaml` yang ditunjuk [peta artefak](../../docs/FINAL_ARTIFACTS.json). `train_example.py` tidak memasang seluruh mekanisme weighting/resep aktual dan tidak boleh menggantikan konfigurasi eksperimen final.

## Pilihan implementasi yang perlu dinyatakan

- Kedua model menggunakan skala kedalaman/lebar nano pada perbandingan ini.
- PD memakai blok Ghost, perhatian BoT/LSKA dan head shared-convolution lokal.
- RD memakai star-operation blocks, attention refinement dengan `torchvision.ops.DeformConv2d`, dan transformasi wavelet Haar pada head lokal.
- Auxiliary fusion RD direalisasikan sebagai **Upsample → Concat → Conv 1×1**, bukan weighted-sum eksplisit pada desain referensi. Ini perbedaan implementasi yang perlu dijelaskan; kesetaraan hasil atau mekanisme tidak diasumsikan.
- Native models memulai dari checkpoint pretrained masing-masing. Model custom hanya memuat bobot YOLOv8n yang bentuknya kompatibel. Inisialisasi dan konfigurasi presisi yang berbeda membatasi kesimpulan tentang arsitektur saja.

## Loss dan artefak final

Run final memakai **effective-number class weighting (beta 0.999) pada classification BCE**, bukan Focal Loss. Patch criterion dilakukan di tingkat kelas `DetectionModel` karena Ultralytics Trainer membangun ulang model ketika training. Notebook lama masih menyimpan variabel atau cell Focal Loss; nama variabel itu tidak menentukan loss yang aktif pada run final.

Bobot dan args enam kelas ada di `runs/rdd_yolov8n_local/experiments/*_class_weight/`. Bobot dan args empat kelas ada di `runs/rdd_4class_local/experiments/*_4cls_class_weights/`. Untuk CSV empat kelas, v8n/v12n/v26n memakai ekspor final di `runs/rdd_4class_local_pc_lab/`, sedangkan PD/RD memakai `runs/rdd_4class_local/`. Daftar lengkap beserta artefak yang tidak tersedia dicatat di [FINAL_ARTIFACTS.json](../../docs/FINAL_ARTIFACTS.json).

Kompleksitas yang dibahas pada hasil utama menggunakan audit **fused model pada input 640** dari [model_complexity.json](../../runs/rdd_yolov8n_local/model_complexity.json). Jangan mencampur angka model unfused, head empat kelas/enam kelas, atau ukuran referensi paper tanpa menyebut protokolnya.

## Dependensi dan catatan validasi

[requirements_yolov8_local.txt](../requirements_yolov8_local.txt) menyatakan `ultralytics>=8.4.108,<9` dan tidak memasang torch/torchvision. Rentang itu bukan jaminan bahwa seluruh versi Ultralytics di dalamnya kompatibel dengan parser internal yang disalin. Fungsi `_patched_parse_model` berbasis parser Ultralytics 8.4.108; perubahan API internal perlu diaudit sebelum upgrade.

Bukti environment yang tersedia dibedakan sebagai berikut:

- Log evaluasi source di [RESULTS.md](../../docs/RESULTS.md) mencatat Ultralytics 8.4.108, Python 3.12.3, torch 2.5.1+cu121 dan RTX 4070 SUPER. Log ini tidak cukup untuk mengklaim versi torchvision suatu run bila versinya tidak tercatat.
- Pemeriksaan packaging portfolio terdahulu mencatat Ultralytics 8.4.108, torch 2.5.1+cpu dan torchvision 0.20.1+cpu; kedua model custom lolos build, finite weighted-loss/backward, serta satu epoch smoke test. Itu pemeriksaan pipeline pada data sintetis, bukan pengulangan eksperimen penuh. Bukti historis: [catatan packaging](../../docs/progress/2026-11-06-portfolio-curation.md).
- README lama menyebut environment 8.4.114 / torch 2.6.0+cu124 / torchvision 0.21.0+cu124, sedangkan header lama menyebut torchvision 0.28.0. Klaim yang berbeda itu tidak menetapkan satu environment final yang terverifikasi; versi lama disimpan di [arsip README](../../docs/archive/content-before-update/code/models/README.md).

Pembaruan dokumentasi ini tidak menginstal environment atau menjalankan ulang model. Gunakan pasangan torch/torchvision yang kompatibel dengan lingkungan yang dituju, lalu verifikasi build/forward/loss bila environment berubah.

## Guard dan riwayat perbaikan yang dipertahankan

- ARM mempertahankan sanitasi/clamp offset sebelum deformable convolution, mengikuti perbaikan crash yang dicatat dalam riwayat implementasi.
- WTConv memiliki guard untuk dimensi feature map ganjil pada dekomposisi/rekonstruksi wavelet.
- MHSA membuat parameter positional embedding dengan batas ukuran saat inisialisasi dan mengambil slice saat forward, sehingga bentuk parameter tidak berubah di tengah training/EMA.

Implementasi guard tersebut tidak diubah pada pembaruan ini. Tabel smoke test Focal Loss pada README lama adalah catatan percobaan awal, bukan konfigurasi loss run final. Bukti historis tetap tersedia di arsip; klaim validasi baru harus disertai pemeriksaan yang benar-benar dijalankan.
