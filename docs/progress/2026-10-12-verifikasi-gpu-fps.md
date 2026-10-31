# 2026-10-12 — Verifikasi GPU: mAP identik 4070 vs 3050, FPS beda

## Pertanyaan user
Boleh nulis "RTX 4070" saja di paper? Apakah hasil di GPU lain pasti sama?

## Eksperimen langsung (bg task bb9f5b3db, RTX 3050 Laptop 6GB, exit 0)
Re-run `model.val()` test N-RDD2024 6-kelas, bobot `yolov8n_class_weight/best.pt`,
imgsz 640, conf=0.001, iou=0.6, Ultralytics 8.4.115, torch 2.6.0+cu124:

| Metrik | RTX 3050 (re-run) | RTX 4070 SUPER (tercatat) |
|---|---|---|
| mAP50 | **0.6476** | 0.648 (0.6476 penuh) |
| mAP50-95 | **0.3643** | 0.364 |
| Speed end-to-end | 168.8 FPS | **219.7 FPS** |

## Kesimpulan (terbukti, bukan asumsi)
1. **mAP identik antar GPU** → angka akurasi (sumber maupun zero-shot V4 yang dievaluasi
   di 3050) valid apa pun GPU-nya. Tidak perlu re-run apa pun.
2. **FPS hardware-dependent** → hanya FPS yang wajib ditarik ke 4070 SUPER, dan memang
   seluruh kolom FPS tabel sumber berasal dari log `docs/RESULTS.md` (RTX 4070 SUPER
   12282MiB, Ultralytics 8.4.108, torch 2.5.1+cu121, Python 3.12.3).

## Aturan penulisan yang aman untuk user (mau nulis "4070" saja)
- BOLEH: "Throughput was measured on an NVIDIA RTX 4070 SUPER 12 GB" (untuk kolom FPS).
- JANGAN: "All experiments were run on an RTX 4070" → salah, zero-shot V4 + run overlap
  jalan di RTX 3050 laptop (Ultralytics 8.4.115, torch 2.6.0+cu124, notebook cell 6-10).
- Angka zero-shot V4 tidak perlu disentuh.

## Rekomendasi edit main.tex (menunggu persetujuan user)
1. Footnote `tab:source` versi yakin: end-to-end (pre+inf+post) di RTX 4070 SUPER 12GB,
   Ultralytics 8.4.108, PyTorch 2.5.1, CUDA 12.1, imgsz 640, 995 citra test.
2. III-B: satu kalimat "Throughput was measured on an RTX 4070 SUPER 12 GB GPU"
   (tanpa klaim semua eksperimen di GPU yang sama).
3. Limitations: hapus "need a canonical timed re-evaluation" →
   "not a standalone benchmark with dedicated warm-up or batch-size sweeps".
