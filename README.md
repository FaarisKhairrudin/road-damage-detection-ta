# Road Damage Detection — TA Research Workspace

Workspace penelitian Tugas Akhir untuk membandingkan lima detektor YOLO pada kerusakan jalan, mengevaluasi generalisasi tanpa fine-tuning ke Indonesia, dan menyiapkan buku TA serta paper. Repository portfolio publik berada terpisah di [road-damage-detection](https://github.com/FaarisKhairrudin/road-damage-detection).

## Mulai dari sini

| Kebutuhan | Buka |
|---|---|
| Peta kerja dan status artefak | [docs/INDEX.md](docs/INDEX.md) |
| Lokasi dataset, sepuluh run final, bobot, args dan CSV | [docs/FINAL_ARTIFACTS.json](docs/FINAL_ARTIFACTS.json) |
| Hasil dalam tabel | [docs/RESULTS_TABLE.md](docs/RESULTS_TABLE.md) |
| Pembahasan naratif dan gambar | [docs/draft-analisis-rapih.md](docs/draft-analisis-rapih.md) |
| Log evaluasi asli | [docs/RESULTS.md](docs/RESULTS.md) |
| Riwayat pemindahan dan arsip | [docs/REORGANIZATION.md](docs/REORGANIZATION.md) |
| Aturan kerja agen | [AGENTS.md](AGENTS.md), [.agents/STATE.md](.agents/STATE.md), [.agents/MEMORY.md](.agents/MEMORY.md) |

Rangkuman bernomor versi dan dataset lama sudah diarsipkan. Alias pada nama lama hanya mempertahankan akses historis; pilih data dan hasil aktif dari peta artefak di atas. Jangan menjalankan ulang eksperimen melalui alias arsip karena alias tersebut tetap dapat ditulis.

## Ruang lingkup eksperimen final

- Model pembanding: **YOLOv8n, YOLOv12n, YOLO26n, YOLOv8-PD, dan YOLO-RD**. Dua model terakhir merupakan reimplementasi lokal dari desain paper; perbedaan implementasi dijelaskan di [code/models/README.md](code/models/README.md).
- Source: subset Asia N-RDD2024 dari China, Japan dan India, dengan enam kelas: `Longitudinal_Crack`, `Transverse_Crack`, `Alligator_Crack`, `Pothole`, `manhole`, dan `patchy_road`.
- Penanganan imbalance pada run final: **effective-number class weighting, beta 0.999, pada komponen classification BCE**. Variabel/nama Focal Loss pada eksperimen lama tidak menunjukkan bahwa Focal Loss aktif pada run final.
- Target final: **RDD-Indo-Crop Roboflow versi 4**, `data/RDD-indo-v4/valid/`: **307 gambar, 502 anotasi, dan 39 gambar tanpa anotasi**. Sebanyak 481 anotasi adalah empat kelas kerusakan; sisanya 21 patchy road. Tidak ada manhole ground truth.
- Evaluasi source overall memakai enam kelas. Perbandingan transfer dan antarnegara utama memakai **empat kelas kerusakan yang sama**. Agregat lima kelas V4 merupakan analisis tambahan, sehingga tidak boleh disamakan dengan skor empat kelas.
- Perbandingan empat versus enam kelas adalah dua rezim training terpisah dengan split gambar sumber yang sama. Hasil berasal dari satu seed/run per model dan rezim, bukan pengujian multi-seed.

Konfigurasi aktual ada pada `args.yaml` tiap run. Kelima run enam kelas mencatat seed 42, input 640, batch 16, maksimal 300 epoch, patience 40 dan optimizer auto. AMP aktif pada model native dan nonaktif pada dua model custom enam kelas; konfigurasi empat kelas perlu dibaca terpisah. Nilai yang tertinggal dalam cell konfigurasi notebook tidak selalu sama dengan argumen run yang sudah selesai.

## Data dan hasil lokal

Dataset lengkap, bobot dan keluaran run tidak masuk Git. Setelah clone, siapkan sumber lokal sesuai [data/README.md](data/README.md). Path utama dipertahankan agar notebook dan script lama tetap menemukan berkasnya.

```text
code/                  notebook penelitian dan rekonstruksi model
scripts/               viewer, evaluasi tambahan dan pembangkit aset
data/                  source, target V4, bahan mentah dan _archive/
runs/                  hasil final dan _archive/ hasil historis
latex/                 buku TA, sumber paper dan submission ISRITI
docs/                  navigasi, tabel, narasi, bukti dan daftar arsip
.agents/               status pekerjaan serta pengetahuan proyek
```

CSV final empat kelas untuk v8n/v12n/v26n berada pada `runs/rdd_4class_local_pc_lab/`; CSV PD/RD berada pada `runs/rdd_4class_local/`. Bobot dan args empat kelas tersedia di `runs/rdd_4class_local/experiments/`. Folder lab masih merupakan sumber hasil final, bukan duplikat yang boleh dihapus. Detail setiap model ada pada [FINAL_ARTIFACTS.json](docs/FINAL_ARTIFACTS.json).

`docs/RESULTS.md` dipertahankan sebagai log mentah. Pembaruan tabel atau pembahasan tidak menulis ulang log tersebut.

## Setup dan notebook

Gunakan environment yang sesuai dengan artefak run. Log source mencatat Python 3.12.3, Ultralytics 8.4.108, torch 2.5.1+cu121 dan RTX 4070 SUPER 12 GB. Requirements proyek masih berupa rentang versi, bukan lockfile reproduksi seluruh run.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Pasang pasangan torch/torchvision yang sesuai CPU/CUDA terlebih dahulu.
python -m pip install -r code/requirements_yolov8_local.txt
```

[requirements_yolov8_local.txt](code/requirements_yolov8_local.txt) sengaja tidak memasang torch/torchvision. [Catatan model](code/models/README.md) membedakan environment run, pemeriksaan historis, dan ketergantungan parser internal.

Notebook tetap di lokasi semula dan belum dirapikan isinya:

| Kelompok | Peran |
|---|---|
| `code/03_1` sampai `03_3_modelling_comparative_local.ipynb` | Training komparatif bertahap; daftar model aktif berbeda per tahap |
| `code/04_1` sampai `04_4_modelling_4class.ipynb` | Training ablasi empat kelas |
| `code/05_zero_shot_indo_v4.ipynb` | Evaluasi target V4; header dan agregasi notebook masih perlu diselaraskan dengan empat kelas utama |
| `code/06_per_country_analysis.ipynb` | Evaluasi negara; agregat kelas yang tersedia perlu dibedakan dari perbandingan empat kelas utama |
| `code/07_domain_visualization.ipynb` | Notebook historis yang masih mengarah ke Indonesia V2; jangan menganggap outputnya sebagai V4 |
| Notebook baseline dan zero-shot V1/V2 | Riwayat eksperimen, bukan resep final default |

Sebelum training atau rerun, cocokkan argumen, dataset, mapping label dan direktori output dengan artefak final. Hindari menjalankan seluruh notebook lama langsung ke lokasi hasil final/arsip.

## Viewer dan naskah

```bash
streamlit run scripts/visualize_streamlit.py
streamlit run scripts/zero_shot_viewer_v4.py
```

| Naskah | Perintah yang sudah tersedia |
|---|---|
| Buku TA aktif | `cd latex/buku-ta-template && bash compile.sh` |
| Pratinjau Bab I–III | `cd latex/buku-ta-template && bash compile.sh bab123` |
| Sumber paper | `cd latex/IEEE-Conference && bash compile.sh` |
| Review ISRITI revisi layout | `cd latex/ISRITI-submission && bash compile-review-revised.sh` |

PDF review ISRITI enam halaman yang telah disubmit adalah snapshot yang dilindungi. Skrip kompilasi dapat menimpa PDF keluaran; baca [README submission](latex/ISRITI-submission/README.md) sebelum membangun ulang. Draft arsitektur tujuh halaman sudah dibatalkan dan diarsipkan, bukan versi submission aktif.

Versi README sebelum pembaruan disimpan utuh di [arsip konten](docs/archive/content-before-update/README.md). Riwayat lama di `docs/progress/` tetap ada; kontinuitas kerja berikutnya menggunakan `.agents/STATE.md` dan `.agents/MEMORY.md`.
