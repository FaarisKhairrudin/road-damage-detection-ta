# 2026-10-02 — Halaman prediksi pada test set N-RDD2024

## Diskusi
Awalnya halaman prediksi baru diarahkan ke RDD-indo-v3 berdasarkan konteks percakapan. Pengguna mengoreksi bahwa yang dimaksud adalah prediksi pada split `test` dataset sumber yang sedang diinspeksi di `visualize_streamlit.py` (N-RDD2024), bukan dataset Indo. Halaman direvisi sesuai klarifikasi itu; halaman Inspect Dataset yang lama tetap dipertahankan.

## Implementasi (`scripts/visualize_streamlit.py`)
- Tambah navigasi sidebar: `Inspect Dataset` dan `Prediksi pada Test Set N-RDD2024`.
- Halaman baru menggunakan data test yang diindeks oleh `scan_dataset` dari `data/NRDD-2024/.../data.yaml`; bukan remap Indo.
- Ringkasan berisi jumlah citra test, model terbaik berdasarkan mAP50, dan tabel lima model.
- Hasil inferensi per citra ditampilkan berdampingan dengan GT; model, confidence, filter hanya-GT, dan pencarian nama citra dapat diatur.
- Bobot yang digunakan: `*_class_weight`; custom patch dipasang untuk YOLOv8-PD dan YOLO-RD.
- mAP50 test sumber yang ditampilkan: yolov8n 0.648, yolov12n 0.654, yolov26n 0.625, yolov8_pd 0.646, yolo_rd 0.661. Nilai ini berasal dari hasil eksperimen sumber yang sudah tercatat; inferensi per citra tetap dijalankan on-demand.
- Scanner menemukan 995 citra di split test; model terbaik pada metrik tersimpan adalah yolo_rd (mAP50 0.661).

## Verifikasi
- `python3.12 -m py_compile scripts/visualize_streamlit.py`: lulus.
- Streamlit `AppTest`: halaman Inspect Dataset tetap render; halaman prediksi N-RDD2024 tidak exception, inferensi YOLO-RD berjalan, dan panel GT/prediksi tampil (contoh test image: 1 GT box dan 1 pred box).
- Pyright/LSP diagnostics: confirmed clean.

## Cara menjalankan
Dari root repository: `streamlit run scripts/visualize_streamlit.py`
