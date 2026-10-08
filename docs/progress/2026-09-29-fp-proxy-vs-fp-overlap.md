# 2026-09-29 — FP "rate" notebook 04_* adalah proxy, bukan false positive IoU-based

## Masalah / Diskusi

Angka FP Pothole di notebook `04_1/04_2/04_3` (dan `confusion_6cls_vs_4cls.py`) didefinisikan sebagai:

```text
fp_rate = jumlah SEMUA prediksi Pothole pada gambar yang memuat GT manhole/patchy_road
          ─────────────────────────────────────────────────────────────────────
          jumlah GT objek manhole/patchy_road pada gambar tersebut
```

Definisi ini **tidak mengecek tumpang tindih box**. Akibatnya prediksi Pothole yang BENAR
(atau FP di lokasi lain) di gambar yang kebetulan memuat pengecoh ikut terhitung.
Ini proxy per-gambar, bukan FP box-level.

## Bukti (yolov8n 6-kelas, split test, conf=0.25, iou=0.6)

Dihitung ulang dengan IoU-match (pred Pothole dihitung "FP beneran" hanya jika
IoU ≥ 0.5 terhadap box GT pengecoh) — `scripts/viz_fp_overlap.py`:

| Metrik | Nilai |
|---|---|
| Proxy FP (metode lama) | 53 / 390 = **0.1359** |
| TRUE overlap FP (IoU ≥ 0.5) | 3 / 390 = **0.0077** |
| Gambar proxy-FP > 0 | 41 dari 272 |
| Gambar dengan FP beneran | hanya 3 (semua Japan_00xxxx) |

Kesimpulan: ~94% dari angka "FP" metode lama BUKAN salah label objek pengecoh;
mayoritas prediksi Pothole tidak menyentuh GT pengecoh sama sekali (IoU ~0.00–0.35).

Perbedaan angka docs vs notebook tetap karena beda split: `SPLITS=["val","test"]`
(`confusion_6cls_vs_4cls.py`, GT 966/201) vs test-only notebook (GT 321/69).
CSV sumber: `runs/rdd_yolov8n_local/confusion_6cls_vs_4cls{,_val_test}.csv`.

## Solusi yang diterapkan

1. `scripts/viz_fp_overlap.py` — skrip baru: hitung proxy FP vs TRUE overlap FP,
   pilih 4 contoh kasus (FP beneran / proxy-saja / penanganan benar / kasus kedua),
   render PNG 2×2 (`runs/rdd_yolov8n_local/viz_fp_overlap_yolov8n_test.png`)
   + CSV detail per gambar (`viz_fp_overlap_detail.csv`).
2. Bug yang ditemui & diperbaiki saat pembuatan:
   - **OOM CUDA** saat predict 272 gambar sekaligus (GPU dipakai proses lain) →
     predict per batch-8 + `torch.cuda.empty_cache()` antar batch (konsisten dengan notebook).
   - **`np.concatenate` ValueError** saat gambar hanya punya GT manhole *atau* patchy
     (array kosong berdimensi 1) → `arr.reshape(-1, 4)`.
   - **Label IoU salah petakan** di panel contoh: `best_iou` sejajar urutan prediksi
     Pothole, bukan urutan semua prediksi → index khusus `pot_j`.
   - **Panel B/C memilih gambar sama** → pengecualian `stem` yang sudah dipakai.

## Implikasi untuk TA

- Jika metrik ini masuk skripsi, **wajib ditulis eksplisit** definisinya
  ("false-positive *proxy* per-gambar"), atau ganti/added-angle dengan FP overlap IoU-based.
- Angka 0.1359 vs 0.0077 menunjukkan klaim "model sering keliru label manhole sebagai
  Pothole" TIDAK didukung metode proxy; klaim yang benar: "model masih menghasilkan
  prediksi Pothole di gambar berpengecoh, tetapi hampir tidak pernah tepat di atas objek pengecoh".
- Rekomendasi: laporkan kedua metrik (proxy untuk konsistensi dengan eksperimen
  sebelumnya + overlap IoU≥0.5 untuk klaim salah-label), atau diskusikan k bersama dospem.

## Lanjutan — tabel FP/GT semua model (skrip `scripts/fp_overlap_table.py`)

Split test, conf=0.25, IoU(NMS)=0.60, IoU match TRUE=0.5. GT: manhole=321, patchy=69, gabungan=390.
Gabungan proxy = union (pred Pothole dihitung 1× per gambar, definisi notebook).

| Model | nc | proxy M | proxy P | proxy Gab | TRUE M | TRUE P | TRUE Gab | det M | det P |
|---|---|---|---|---|---|---|---|---|---|
| yolov8n_6cls | 6 | 0.1402 | 0.2174 | 0.1359 | 0.0093 | 0.0000 | 0.0077 | 0.8224 | 0.5507 |
| yolov12n_6cls | 6 | 0.1620 | 0.1739 | 0.1462 | 0.0062 | 0.0000 | 0.0051 | 0.8100 | 0.6087 |
| yolov26n_6cls | 6 | 0.1620 | 0.2029 | 0.1513 | 0.0031 | 0.0000 | 0.0026 | 0.9159 | 0.5507 |
| yolov8_pd_6cls | 6 | 0.1464 | 0.1594 | 0.1333 | 0.0062 | 0.0000 | 0.0051 | 0.8224 | 0.5507 |
| yolov8n_4cls † | 4 | 0.1651 | 0.2029 | 0.1513 | — | — | — | — | — |
| yolov12n_4cls † | 4 | 0.1371 | 0.1304 | 0.1231 | — | — | — | — | — |
| yolov26n_4cls † | 4 | 0.1589 | 0.1884 | 0.1487 | — | — | — | — | — |
| yolov8_pd_4cls | 4 | 0.1433 | 0.1594 | 0.1308 | 0.0062 | 0.0000 | 0.0051 | — | — |

† bobot final `yolov8n/v12n/v26n_4cls_class_weights/weights/best.pt` TIDAK ada di repo
(hanya versi smoke 2-epoch); angka proxy-nya dari run 2025-08-07
(`confusion_6cls_vs_4cls.csv`), TRUE overlap tidak bisa dihitung ulang sampai bobot dipulihkan.

Validasi silang: proxy 6cls & PD-4cls cocok persis dengan CSV/notebook lama → pipeline benar.

Temuan:
1. TRUE Gab semua model 0.0026–0.0077 (1–3 prediksi dari 390 GT) — salah-label pengecoh sebagai Pothole hampir tidak pernah terjadi.
2. TRUE P = 0.0000 di SEMUA model — tidak ada satu pun pred Pothole menimpa GT patchy_road (IoU≥0.5).
3. Pasangan 6cls vs 4cls yang bisa dibanding TRUE hanya v8_pd: 0.0051 vs 0.0051 (identik, 2/390).
4. Perbedaan proxy antar model (mis. v12n 0.1231 vs 0.1462) berasal dari prediksi Pothole di lokasi lain dalam gambar, bukan dari pengecoh → metrik proxy rawan salah tafsir antar model.
5. det rate 6cls: manhole terserap baik (0.81–0.92), patchy lebih sulit (0.55–0.61).
6. Bug fix: bobot v8_pd butuh `patch_ultralytics()` (custom_modules) sebelum `YOLO(bobot)` dipanggil — sama seperti guard notebook 04_3.

## Update — bobot final 4-kelas dipulihkan dari PC lab (2026-10-01)

Folder `runs/rdd_4class_local_pc_lab/` (hasil copy dari PC lab) berisi training final 4-kelas.
Yang dipindah (mv) ke `runs/rdd_4class_local/experiments/`:
- `yolov8n_4cls_class_weights` (full: best/last/epoch*.pt 6.3MB, results.csv 170 epoch)
- `yolov12n_4cls_class_weights` (full: best 5.5MB, 135 epoch)
- `yolov26n_4cls_class_weights` (full: best 5.4MB, 164 epoch)
args.yaml ketiganya: nc final (eksperimen 300 epoch, batch 16, imgsz 640, data.yaml = 4cls).

Yang TIDAK dipindah (ramping / duplikat / sudah ada versi final lokal):
- `yolov8_pd_4cls/`, `yolo_rd_4cls_class_weights/` (hanya args.yaml+jpg, tanpa .pt)
- `yolov8n_4cls_smoke`, `yolo_rd_4cls_smoke` (smoke 2-epoch; lokal sudah punya)
- `evaluation/{yolov8n,yolo_rd}_4cls_{test,val}` + `predictions/*_test_samples` (hasil evaluasi PC lab; lokal sudah punya versi sendiri)
- `yolov8_pd_4cls_class_weights` sudah final di lokal (tidak disentuh).

Folder `rdd_4class_local_pc_lab/` dibiarkan apa adanya sebagai arsip (tidak dihapus).
Skrip `scripts/fp_overlap_table.py` di-run ulang → kolom TRUE 4-kelas terisi untuk v8/v12/v26.

## Update 2026-10-01 — tabel lengkap 8 model (bobot 4-kelas dipulihkan)

Setelah 3 bobot final 4-kelas dipindah dari PC lab, `fp_overlap_table.py` di-run ulang (8 model,
test, conf=0.25). Semua baris sekarang dari inferensi langsung — tidak ada lagi `†`.

| Model | nc | proxy M | proxy P | proxy Gab | TRUE M | TRUE P | TRUE Gab | det M | det P |
|---|---|---|---|---|---|---|---|---|---|
| yolov8n_6cls | 6 | 0.1402 | 0.2174 | 0.1359 | 0.0093 | 0.0 | 0.0077 | 0.8224 | 0.5507 |
| yolov12n_6cls | 6 | 0.1620 | 0.1739 | 0.1462 | 0.0062 | 0.0 | 0.0051 | 0.8100 | 0.6087 |
| yolov26n_6cls | 6 | 0.1620 | 0.2029 | 0.1513 | 0.0031 | 0.0 | 0.0026 | 0.9159 | 0.5507 |
| yolov8_pd_6cls | 6 | 0.1464 | 0.1594 | 0.1333 | 0.0062 | 0.0 | 0.0051 | 0.8224 | 0.5507 |
| yolov8n_4cls | 4 | 0.1682 | 0.2029 | 0.1538 | 0.0093 | 0.0 | 0.0077 | — | — |
| yolov12n_4cls | 4 | 0.1371 | 0.1304 | 0.1231 | 0.0093 | 0.0 | 0.0077 | — | — |
| yolov26n_4cls | 4 | 0.1589 | 0.1884 | 0.1487 | 0.0062 | 0.0 | 0.0051 | — | — |
| yolov8_pd_4cls | 4 | 0.1433 | 0.1594 | 0.1308 | 0.0062 | 0.0 | 0.0051 | — | — |

Catatan penting: proxy Gab 4-kelas hasil inferensi ulang sedikit beda dari referensi run 2025-08-07
(v8n: 0.1538 vs 0.1513; v26n: 0.1487 vs 0.1513? cocok). Perbedaan ±1–2 prediksi Pothole pada gambar
union — kemungkinan versi ultralytics/seed NMS berbeda; per-kelas M/P cocok persis → pipeline valid.
TRUE Gab: pasangan se-arsitektur 6cls vs 4cls identik atau beda ≤1 prediksi (v8: 0.0077=0.0077;
v12: 0.0051 vs 0.0077 = beda 1 prediksi; v26: 0.0026 vs 0.0051 = beda 1; PD: 0.0051=0.0051).
→ Tidak ada bukti efek distractor pada FP beneran di semua arsitektur.
