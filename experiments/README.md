# Experiment Registry

Folder ini berisi catatan eksperimen yang ringan dan aman untuk GitHub.

Yang boleh masuk GitHub:

- konfigurasi eksperimen
- ringkasan metrik
- tabel metrik per kelas
- link bobot model
- link paket artefak evaluasi
- catatan eksperimen

Yang tidak dimasukkan ke GitHub:

- dataset
- folder `runs/`
- bobot model `.pt`
- export model `.onnx`, `.engine`, dan sejenisnya
- paket artefak `.zip`

## Alur yang Disarankan

1. Jalankan training dari notebook.
2. Cek hasil di `runs/rdd_yolov8n_local/`.
3. Buat paket artefak lokal:

```bash
python scripts/package_experiment.py --run-dir runs/rdd_yolov8n_local/experiments/yolov8n_baseline_native_loss --run-id yolov8n_baseline_native_loss_v1
```

4. Upload `best.pt` dan paket evaluasi dari folder `artifacts/` ke GitHub Releases, Hugging Face, Google Drive, atau Kaggle Dataset/Model.
5. Catat link dan metrik utama ke `experiments/registry.csv`.

Dengan cara ini repository tetap ringan, tetapi setiap eksperimen tetap bisa dilacak dan dibuka lagi dari mana pun.
