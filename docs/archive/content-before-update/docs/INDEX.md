# Peta kerja TA — mulai di sini

Navigasi ini memilih artefak final yang sudah diverifikasi. Penataan saat ini hanya mengarsipkan versi lama dan memperjelas rute; isi ilmiah notebook, hasil eksperimen, dan naskah tidak direvisi atau dihitung ulang. Penyesuaian jalur yang diperlukan oleh pemindahan dicatat pada laporan.

- [Aturan agen](../AGENTS.md), [status pekerjaan](../.agents/STATE.md), dan [pengetahuan proyek](../.agents/MEMORY.md).
- [Daftar artefak final](FINAL_ARTIFACTS.json): lokasi dataset, bobot, konfigurasi, CSV dan naskah.
- [Laporan pemindahan dan daftar isi yang perlu direvisi](REORGANIZATION.md).

## Hasil: pilih sesuai cakupannya

| Kebutuhan | Acuan |
|---|---|
| Analisis naratif dengan 15 gambar | [draft-analisis-rapih.md](draft-analisis-rapih.md); isi dipertahankan, pembaruan ilmiah masih ditunda |
| Tabel hasil yang sudah ada | [RESULTS_TABLE.md](RESULTS_TABLE.md), dipertahankan tanpa perubahan; perhatikan catatan cakupan di bawah |
| Bukti log evaluasi mentah | [RESULTS.md](RESULTS.md), bukan ringkasan final alternatif |
| Angka per kelas dari lima model enam kelas | `runs/rdd_yolov8n_local/*_class_weight_test_per_class_metrics.csv` |
| CSV ablasi empat kelas v8n/v12n/v26n | `runs/rdd_4class_local_pc_lab/*_4cls_class_weights_test_per_class_metrics.csv` |
| CSV ablasi empat kelas PD/RD | `runs/rdd_4class_local/*_4cls_class_weights_test_per_class_metrics.csv` |
| Zero-shot target final | [CSV per kelas V4](../runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/zs_per_class_metrics.csv) |
| Kompleksitas model | [Audit fused model](../runs/rdd_yolov8n_local/model_complexity.json), dengan protokol yang tercatat di dalamnya |
| Konfigurasi dan bobot tiap run | [Peta 10 eksperimen final](FINAL_ARTIFACTS.json); `args.yaml` mengungguli konstanta notebook |
| Pembahasan angka final untuk penulisan | [Paper sumber](../latex/IEEE-Conference/main.tex), [source ISRITI](../latex/ISRITI-submission/main.tex), dan artefak yang dirujuk |

**Cakupan utama:** source overall memakai enam kelas; perbandingan transfer dan antarnegara yang setara memakai empat kelas kerusakan yang sama. Ringkasan zero-shot lima kelas di tabel/CSV lama tetap merupakan analisis tambahan yang berbeda. Jangan mencampur kedua agregasi tersebut.

`RESULTS_TABLE.md` masih memiliki metadata V3 pada bagian akhir serta nilai kompleksitas lama. Keduanya belum disunting pada tahap ini. Dua rangkuman eksperimen bernomor versi sudah berada di [arsip ringkasan](archive/summaries/), sehingga tidak lagi menjadi konteks kerja default. Jalur lama rangkuman hanya alias kompatibilitas untuk tautan README/riwayat, bukan pilihan konteks final. Daftar koreksi lengkap ada di laporan penataan.

## Data aktif dan kompatibilitas

| Peran | Lokasi |
|---|---|
| Source enam kelas | `data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/` |
| Turunan source empat kelas | `data/NRDD-2024/RDD_4class/` |
| Target Indonesia final | [RDD-indo-v4](../data/RDD-indo-v4/) — Roboflow versi 4, 307 gambar, 502 anotasi, 39 label kosong; split `valid` dipakai sebagai uji target |
| Bahan mentah | `data/archive/` — data mentah yang dipertahankan, bukan folder sampah |
| Ekspor Indonesia sebelumnya | `data/_archive/`; nama folder lama di `data/` hanya alias kompatibilitas |
| Remapping target final | `runs/rdd_yolov8n_local/indo_v4_remapped/` |

Remapped views lama tetap berupa direktori fisik agar sel notebook yang memakai `shutil.rmtree(REM)` tidak rusak. Alias dataset mempertahankan target symlink gambar yang masih memakai jalur lama. Alias/arsip hanya untuk kompatibilitas pencarian/baca historis, bukan pilihan run final. Alias masih dapat ditulis: menjalankan ulang notebook lama dapat menimpa arsip. Jangan rerun lewat alias; pembaruan analisis berikutnya harus memakai direktori keluaran baru.

## Notebook dan script: lokasi tidak berubah

| Kebutuhan | Lokasi / status |
|---|---|
| EDA awal | [00_EDA.ipynb](../code/00_EDA.ipynb) |
| Training komparatif bertahap | `code/03_1_modelling_comparative_local.ipynb`, `03_2_...`, `03_3_...`; tahapan berbeda, bukan duplikat yang boleh dibuang |
| Training ablasi | `code/04_1_modelling_4class.ipynb` sampai `04_4_modelling_4class.ipynb`; daftar model nyata harus dibaca dari isinya |
| Zero-shot V4 | [05_zero_shot_indo_v4.ipynb](../code/05_zero_shot_indo_v4.ipynb); header/agregasi masih masuk daftar revisi berikutnya |
| Analisis negara | [06_per_country_analysis.ipynb](../code/06_per_country_analysis.ipynb); keluaran agregat lama tidak selalu memakai empat kelas bersama |
| Visualisasi domain | [07_domain_visualization.ipynb](../code/07_domain_visualization.ipynb); **masih memakai Indonesia V2**, belum diperbarui |
| Model rekonstruksi | [code/models/README.md](../code/models/README.md), YAML dan `custom_modules.py` di folder yang sama |
| Viewer aktif | `scripts/visualize_streamlit.py`, `scripts/zero_shot_viewer_v4.py` |
| Tabel dan kurva Bab IV | [thesis_bab4_assets.py](../scripts/paper/thesis_bab4_assets.py) |
| Notebook baseline/zero-shot lama dan script viewer lama | Tetap di lokasi semula sesuai permintaan; berstatus historis, bukan acuan final |
| Dependensi | [requirements_yolov8_local.txt](../code/requirements_yolov8_local.txt); baca catatan torch/torchvision di dalamnya |

Memindahkan script sekarang akan mengubah perhitungan root berbasis `__file__`. Karena isi source belum boleh diubah, script tidak ikut dipindahkan.

## UMAP dan analisis Indonesia yang belum mutakhir

Bundle UMAP/t-SNE lama disimpan bersama manifest, embeddings, statistik dan montage di [arsip domain V2](../runs/_archive/indonesia_v2/domain_viz/). Jalur `runs/rdd_yolov8n_local/evaluation/domain_viz` adalah alias historis agar script lama masih menemukan inputnya.

Manifest lama berisi 995 source + 308 Indonesia V2. Mengganti judul atau menggambar ulang embeddings tersebut tidak menghasilkan analisis V4. Pembaruan berikutnya harus memakai 995 source + 307 V4 serta meregenerasi manifest, embeddings dan keluaran turunannya. Figur lama dalam folder naskah dipertahankan; bagian feature-viz pada paper saat ini dinonaktifkan.

## Naskah dan kompilasi

| Peran | Acuan / perintah yang sudah ada |
|---|---|
| Buku TA aktif | [latex/buku-ta-template/](../latex/buku-ta-template/); `cd latex/buku-ta-template && bash compile.sh`; preview Bab I–III: `bash compile.sh bab123` |
| Source paper | [latex/IEEE-Conference/main.tex](../latex/IEEE-Conference/main.tex); `cd latex/IEEE-Conference && bash compile.sh` |
| Submission ISRITI | [main.tex](../latex/ISRITI-submission/main.tex); revisi review: `cd latex/ISRITI-submission && bash compile-review-revised.sh` |
| PDF submission aktif | [ISRITI_Review_Anonymous_Layout_Revised.pdf](../latex/ISRITI-submission/hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf), enam halaman; pertahankan snapshot terunggah |
| Review anonim awal | [ISRITI_Review_Anonymous.pdf](../latex/ISRITI-submission/hasil/ISRITI_Review_Anonymous.pdf), dipertahankan; `compile-review.sh` dapat menimpanya bila dijalankan |
| Draft diskusi arsitektur tujuh halaman | Sudah dibatalkan dan diarsipkan atas permintaan pengguna: [manifest pembatalan](../latex/ISRITI-submission/build/archived-architecture-discussion-2026-11-13/manifest.json). Jangan memulihkannya dari petunjuk lama |
| Naskah/proposal terdahulu | [latex/skripsi-telkom/](../latex/skripsi-telkom/) dan [PROPOSAL_TA.md](../latex/PROPOSAL_TA.md); tetap di lokasi yang sama |
| Referensi PDF dan hasil riset pustaka | `latex/refference/` dan [outputs/yolo-road-damage-references.md](../outputs/yolo-road-damage-references.md) |

README ISRITI lama masih mendeskripsikan draft arsitektur sebagai aktif. Catatan itu dipertahankan tanpa penyuntingan; status pembatalan di atas dan manifestnya adalah acuan terkini. Folder `build/` memuat snapshot/QA penting selain intermediates kompilasi: jangan dibersihkan secara menyeluruh.

## Arsip, riwayat dan repo portfolio

- [Manifest pemindahan](archive/MANIFEST.json) mencatat asal, tujuan, alasan, alias, jumlah berkas dan verifikasi hash setiap kelompok.
- [docs/progress/](progress/) tetap utuh sebagai sejarah. Ke depan, kontinuitas pekerjaan memakai `.agents/STATE.md` dan `.agents/MEMORY.md`, tanpa menambah log sesi bertanggal.
- [INDEX dan AGENTS sebelum penataan](archive/navigation/) menyimpan keadaan working tree semula, termasuk perubahan yang belum di-commit.
- README root masih menjelaskan baseline lama; isinya sengaja belum ditulis ulang. Gunakan halaman ini untuk navigasi kondisi sekarang.
- Portfolio berada di repository terpisah: [FaarisKhairrudin/road-damage-detection](https://github.com/FaarisKhairrudin/road-damage-detection). Penataan ini tidak mengubah atau memublikasikan ulang repo portfolio.
