# 2026-10-08 — Zero-shot RDD-indo-v4 + metrik F1 (macro/weighted) + bug `class_result`

## Diskusi
- Diminta memindahkan target uji zero-shot dari `data/RDD-indo-v3` ke `data/RDD-indo-v4`
  dengan syarat **hanya mengganti nama/parameter**, tanpa menambah notebook atau script baru.
- Keputusan (konfirmasi user): **timpa file lama** (rename v3 → v4) dan **artefak ke folder V4 baru**
  supaya hasil V3 tetap utuh.
- Lanjutan: F1 zero-shot belum pernah dihitung (artefak V3/V4 hanya menyimpan P, R, mAP50, mAP50-95).
  Diminta menghitung F1 macro + weighted, ditaruh di notebook, sekaligus **run all** agar output terlihat.

## Yang dikerjakan
1. `code/05_zero_shot_indo_v3.ipynb` → `05_zero_shot_indo_v4.ipynb`; `scripts/zero_shot_viewer_v3.py` → `zero_shot_viewer_v4.py`
   (`git mv` gagal karena `.git/index.lock` stale sejak 22 Sep → dipakai `mv` biasa).
2. Repoint seluruh referensi v3 → v4: dataset `data/RDD-indo-v4`, remap `indo_v4_remapped`,
   evaluasi `evaluation/zero_shot_indo_v4`, kolom `indo_v4_zs`, caption 307 citra.
3. Artefak baru: `runs/rdd_yolov8n_local/indo_v4_remapped/` dan
   `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/`.
4. Sel baru di notebook: per-kelas P/R/F1/mAP + ringkasan F1 macro & weighted,
   tulis `zs_per_class_metrics.csv` dan `zs_f1_summary.csv`.
5. Helper: `scripts/run_zs_v4_finish.py` (finishing metrics+plot) dan `scripts/run_nb_zs_v4.py` (runner notebook kernel `python3_12`).

## Hasil zero-shot V4 (307 citra, 514 instans, 39 background)
| Model | P | R | mAP50 | mAP50-95 | F1 macro | F1 weighted |
|---|---|---|---|---|---|---|
| yolov12n | 0.424 | 0.352 | 0.332 | 0.141 | 0.378 | 0.464 |
| yolo_rd | 0.401 | 0.298 | 0.297 | 0.127 | 0.332 | 0.431 |
| yolov8_pd | 0.343 | 0.308 | 0.279 | 0.121 | 0.305 | 0.402 |
| yolov8n | 0.304 | 0.311 | 0.250 | 0.103 | 0.306 | 0.392 |
| yolov26n | 0.280 | 0.295 | 0.239 | 0.099 | 0.274 | 0.359 |

- Ranking mAP50 dan F1 weighted identik: **12n > RD > PD > 8n > 26n** (sama dengan v2 dan v3).
- F1 macro menukar 8n ↔ PD (0.306 vs 0.305, praktis seri) karena bobot tiap kelas sama.
- Domain gap vs test sumber: 12n −49.2%, RD −55.0%, PD −56.8%, 8n −61.5%, 26n −61.7%
  (v3: −52.8 s.d. −63.9%; v2: −73.7 s.d. −78.2%).
- V4 vs V3 naik tipis (+0.002 s.d. +0.025 mAP50) seiring berkurangnya 33 instans, dengan
  Pothole (kelas tersulit) turun paling banyak (−17 instans) → efek komposisi dataset, bukan model membaik.
- Per-kelas: tersulit Pothole (F1 0.148–0.324) dan patchy_road (0.075–0.109); termudah Longitudinal_Crack (0.513–0.603).

## Bug yang ditemukan & diperbaiki

### B1 — Edit notebook tidak tersimpan (script patch lupa `json.dump`)
- Gejala: run ke-1 gagal; `KeyError: 'macro_f1'` di sel domain gap, `NameError: ZS_PC`, `NameError: df`.
- Penyebab: script patch pertama menulis `cell['source']` ke dict in-memory **tanpa** `json.dump`,
  sementara sel berikutnya sudah memakai variabel baru.
- Perbaikan: tulis ulang sel `run_zs` dengan `json.dump` + verifikasi ulang isi file setelah menyimpan.

### B2 — `Metric.class_result(i)` bersifat POSISIONAL, bukan class-id
- Gejala: baris `patchy_road` (support 22, ada GT) bernilai `NaN`, sedangkan `manhole` (0 GT)
  justru punya angka.
- Investigasi: `len(box.p) = 5` dan `ap_class_index = [0, 1, 2, 3, 5]` →
  `class_result(4)` sebenarnya mengembalikan metrik **patchy_road**, dan `class_result(5)` → `IndexError`
  (tertelan `except Exception` sehingga muncul sebagai `NaN`).
- Akar masalah: kelas tanpa GT di split target (`manhole`) tidak masuk `ap_class_index`,
  sehingga posisi bergeser dari class-id.
- Perbaikan: petakan posisi → class-id lewat `ap_class_index`; kelas tanpa GT dilaporkan `NaN`
  dan **tidak** dihitung seperti 0. Macro/weighted dihitung atas kelas yang benar-benar dievaluasi (5 kelas).
- Untungnya angka macro/weighted **tidak berubah** (pandas mean sudah melewati `NaN`); hanya label
  per-kelas yang bergeser — tapi label salah tetap fatal kalau masuk skripsi.

### Cek dampak ke notebook lain
`02_modelling_baseline_local`, `03_*`, `04_*` juga memakai `class_result(class_id)`, tetapi **aman**:
dataset sumber (6 kelas) dan dataset 4-kelas punya GT untuk semua kelas di setiap split, jadi
`ap_class_index` lengkap dan posisi ≡ class-id. Bug ini hanya muncul saat ada kelas tanpa GT di split evaluasi
(hanya target V3/V4).

## Implikasi untuk TA
- Klaim "manhole dihitung 0 sehingga menekan mAP" **tidak berlaku** untuk split target: Ultralytics
  mengeluarkan kelas tanpa GT dari rata-rata. Semua angka zero-shot (v3 dan v4) sudah benar,
  tapi narasi yang menyebut penekanan oleh manhole harus dihapus.
- F1 weighted lebih cocok dibandingkan dengan mAP50 (urutan identik); F1 macro berguna untuk
  menyoroti performa kelas kecil (patchy_road). Laporkan keduanya dengan definisi eksplisit.
- `RESULTS.md` masih memuat angka YOLO-RD pra-fix dan belum disinkronkan (catatan lama, belum dikerjakan).

## Artefak
- `code/05_zero_shot_indo_v4.ipynb` (20 → 22 sel, semua ter-run, 0 error)
- `scripts/zero_shot_viewer_v4.py`, `scripts/run_zs_v4_finish.py`, `scripts/run_nb_zs_v4.py`
- `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/`: `domain_gap.csv/png`, `zs_f1_summary.csv`,
  `zs_per_class_metrics.csv`, `zs_samples_pred_only.png`, `zs_samples_gt_vs_pred.png`
- `runs/rdd_yolov8n_local/indo_v4_remapped/` (307 symlink + label remap + yaml)
