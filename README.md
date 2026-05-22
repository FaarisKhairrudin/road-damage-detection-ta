# Road Damage Detection TA

Kode penelitian Tugas Akhir untuk baseline deteksi kerusakan dan cacat permukaan jalan menggunakan YOLOv8n pada subset Asia N-RDD2024 6 kelas.

## Fokus Eksperimen

- Dataset sekunder: N-RDD2024 subset China, Japan, India.
- Kelas: `Longitudinal_Crack`, `Transverse_Crack`, `Alligator_Crack`, `Pothole`, `manhole`, `patchy_road`.
- Baseline utama: YOLOv8n pretrained COCO dengan native Ultralytics loss.
- Evaluasi: mAP50, mAP50-95, precision, recall, F1 per kelas, confusion matrix, PR/F1 curve, dan estimasi FPS.
- Focal loss disiapkan sebagai ablation opsional, bukan baseline utama.

## Struktur Data yang Diharapkan

Data tidak disimpan di GitHub. Setelah clone repo, salin dataset dari SSD ke lokasi berikut:

```text
data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/
  data.yaml
  train/
    images/
    labels/
  val/
    images/
    labels/
  test/
    images/
    labels/
```

Notebook lokal sudah memakai path ini secara otomatis.

## Setup Lokal atau GPU Server

```bash
git clone https://github.com/FaarisKhairrudin/road-damage-detection-ta.git
cd road-damage-detection-ta
python -m venv .venv
```

Aktifkan environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

Install dependency:

```bash
pip install -U pip
pip install -r code/requirements_yolov8_local.txt
```

Jika GPU NVIDIA tersedia, pastikan PyTorch CUDA sudah terpasang sesuai versi CUDA server. Jika `torch.cuda.is_available()` masih `False`, install PyTorch CUDA dari instruksi resmi PyTorch terlebih dahulu, lalu install requirements di atas.

## Notebook Utama

- `code/01_modelling_baseline.ipynb`: versi Kaggle.
- `code/02_modelling_baseline_local.ipynb`: versi lokal/GPU server.

Untuk menjalankan baseline lokal:

1. Buka `code/02_modelling_baseline_local.ipynb`.
2. Jalankan cell install dependency jika environment belum lengkap.
3. Restart kernel.
4. Jalankan cell dari atas.
5. Untuk smoke test, ubah sementara `EPOCHS = 5` dan `RUN_NAME = "yolov8n_smoke_test"`.
6. Untuk eksperimen final, gunakan `EPOCHS = 300`, `PATIENCE = 50`, dan `RUN_NAME = "yolov8n_baseline_native_loss"`.

## Catatan Augmentasi Baseline

Baseline tidak menggunakan rotasi:

```python
degrees = 0.0
```

Augmentasi yang digunakan:

- Mosaic
- MixUp ringan
- horizontal flip
- translate
- scale
- close mosaic pada 10 epoch terakhir

## Output

Output training dan evaluasi akan muncul di:

```text
runs/rdd_yolov8n_local/
```

Folder `runs/`, dataset, dokumen proposal, dan bobot model diabaikan oleh Git agar repository tetap ringan.
