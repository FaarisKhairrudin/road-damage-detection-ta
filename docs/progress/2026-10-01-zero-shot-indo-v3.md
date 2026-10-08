# 2026-10-01 — Zero-shot ke RDD-indo-v3 (adaptasi notebook v2)

## Diskusi
Diminta adaptasi `code/05_zero_shot_indo_v2.ipynb` agar menunjuk ke `data/RDD-indo-v3`.
Pemeriksaan struktur: v3 hanya punya split `valid/` (308 citra, 308 label) dan 5 kelas
tanpa manhole (`['alligator crack', 'longitudinal crack', 'patchy road', 'pothole', 'tranverse crack']`),
berbeda dari v2 (valid 6 + test 308 citra, 6 kelas dengan manhole). Diputuskan (konfirmasi user):
file baru `05_zero_shot_indo_v3.ipynb`, evaluasi langsung 5 bobot, pakai isi `valid/` sebagai split test remap.

## Eksperimen (`code/05_zero_shot_indo_v3.ipynb`, 20 sel, 1 cell = 1 logical unit)
- EDA: valid 308 images / 308 label / 33 empty, 547 instans
  (longitudinal 238, tranverse 140, pothole 92, alligator 52, patchy road 25).
- Remap target->sumber baru (cocok via nama kelas, assert diverifikasi):
  `{0: 2, 1: 0, 2: 5, 3: 3, 4: 1}` — v2 memakai `{0: 2, 1: 0, 2: 4, 3: 5, 4: 3, 5: 1}`.
  Isi `valid/` disymlink ke `indo_v3_remapped/test/`, yaml `nc: 6, names: SRC_NAMES`,
  val dengan `split='test'` supaya identik protokol v2 (conf=0.001, iou=0.6).
- Setup bobot sama seperti v2 (yolov8n/yolov12n/yolov26n/yolov8_pd/yolo_rd `*_class_weight`),
  patch custom hanya untuk PD/RD. SRC_TEST tetap (8n 0.648, 12n 0.654, 26n 0.625, PD 0.646, RD 0.661).
- Runner: nbclient cell-by-cell kernel `python3_12` (torch 2.6.0+cu124, GPU RTX 3050),
  notebook ditulis balik tiap run termasuk output parsial (perbaikan runner: `create_kernel_manager()` dulu,
  sebelumnya `AssertionError: km is None` karena `start_new_kernel()` langsung).

## Hasil (zero-shot RDD-indo-v3, conf=0.001, iou=0.6)
- yolov12n: P=0.418 R=0.326 mAP50=0.309 mAP50-95=0.130 (terbaik)
- yolo_rd: P=0.386 R=0.270 mAP50=0.272 mAP50-95=0.115
- yolov8_pd: P=0.343 R=0.295 mAP50=0.269 mAP50-95=0.114
- yolov8n: P=0.306 R=0.299 mAP50=0.248 mAP50-95=0.102
- yolov26n: P=0.283 R=0.278 mAP50=0.225 mAP50-95=0.093
- Domain gap vs test sumber: 12n -0.345 (-52.8%), RD -0.389 (-58.8%), PD -0.377 (-58.3%),
  8n -0.400 (-61.7%), 26n -0.400 (-63.9%).
- Ranking sama persis dengan zero-shot v2 (12n > RD > PD > 8n > 26n), tapi gap absolut
  lebih kecil dari v2 (-0.48 s.d. -0.51, -74 s.d. -78%).

## Solusi / implikasi
- Gap v3 < v2 konsisten dengan hilangnya kelas manhole (di v2 n=4, AP ~0 menyeret
  rata-rata mAP) plus komposisi split berbeda — bukan bukti model membaik, melainkan
  efek penghapusan kelas tersulit. Untuk klaim skripsi, bandingkan v2↔v3 hanya dengan
  catatan caveat ini; atau hitung ulang mAP atas 5 kelas bersama agar apel-ke-apel.
- Artefak: `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v3/`
  (domain_gap.csv/png, zs_samples_pred_only.png, zs_samples_gt_vs_pred.png);
  label remap di `runs/rdd_yolov8n_local/indo_v3_remapped/`;
  sel Kesimpulan Sementara di notebook sudah diisi pasca-run.

## 2026-10-02 — Streamlit viewer
- Dibuat `scripts/zero_shot_viewer_v3.py` dari pola viewer v2, diarahkan ke remap + domain gap v3.
  Viewer memuat 308 citra, menampilkan GT vs prediksi on-demand untuk 5 bobot, serta tabel domain gap.
- Smoke test dengan `streamlit.testing.v1.AppTest`: tampilan awal berhasil dan inferensi GPU yolov12n tampil (GT 2 box, prediksi 4 box).
- Bug ditemukan saat pencarian menghasilkan tepat satu citra: slider `0..0` ditolak Streamlit. Solusi: bila hanya satu hasil, lewati slider dan tampilkan caption; kasus 1 dan 0 hasil sudah diuji ulang.
- Perbarui `use_container_width` menjadi `width="stretch"` agar tidak memakai parameter deprecated. Rapikan tipe dinamis pandas/Ultralytics. Pyright/LSP terkonfirmasi clean.
- Perintah: `streamlit run scripts/zero_shot_viewer_v3.py` dari root repo.
