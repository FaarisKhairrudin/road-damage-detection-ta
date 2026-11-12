# Peta kerja TA — mulai di sini

Dokumen hasil dan narasi telah diselaraskan dengan artefak final. Agregasi CSV dan grafik diperbarui tanpa training ulang. Regenerasi fitur/UMAP V4 **ditunda atas permintaan pengguna**; folder parsial tidak dipakai sebagai hasil final. Notebook dan naskah/PDF terunggah tetap dipertahankan.

- [Aturan agen](../AGENTS.md), [status pekerjaan](../.agents/STATE.md), [pengetahuan proyek](../.agents/MEMORY.md).
- [Peta artefak final](FINAL_ARTIFACTS.json): lokasi dataset, bobot, konfigurasi, CSV dan naskah.
- [Riwayat pemindahan dan status pembaruan isi](REORGANIZATION.md).

## Hasil dan analisis aktif

| Kebutuhan | Acuan |
|---|---|
| Analisis naratif bergambar | [draft-analisis-rapih.md](draft-analisis-rapih.md) |
| Tabel hasil final | [RESULTS_TABLE.md](RESULTS_TABLE.md), dihasilkan dari CSV/config/audit final |
| Log mentah historis | [RESULTS.md](RESULTS.md), dipertahankan sebagai bukti |
| Dataset/run/bobot/konfigurasi final | [FINAL_ARTIFACTS.json](FINAL_ARTIFACTS.json); `args.yaml` mengungguli konstanta notebook |
| CSV sumber per kelas | `runs/rdd_yolov8n_local/*_class_weight_test_per_class_metrics.csv` |
| CSV empat kelas v8n/v12n/v26n | `runs/rdd_4class_local_pc_lab/*_4cls_class_weights_test_per_class_metrics.csv` |
| CSV empat kelas PD/RD | `runs/rdd_4class_local/*_4cls_class_weights_test_per_class_metrics.csv` |
| Target V4 per kelas | [zs_per_class_metrics.csv](../runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/zs_per_class_metrics.csv) |
| Agregat laporan yang diregenerasi | `runs/rdd_yolov8n_local/evaluation/final_report/`; grafik di [docs/figures/final_results/](figures/final_results/) |
| Kompleksitas fused | [model_complexity.json](../runs/rdd_yolov8n_local/model_complexity.json), dengan protokol di dalamnya |

Overall sumber memakai enam kelas. Transfer utama, ablasi dan perbandingan negara memakai empat kelas kerusakan yang sama. Lima kelas bersama, termasuk patchy road tanpa manhole, tetap merupakan analisis tambahan yang diberi label terpisah. Perbandingan negara mengikuti presisi tiga desimal pada paper; tidak ditambah presisi rekaan.

Reproduksi laporan/narasi: `python3.12 scripts/build_final_results.py`, lalu `python3.12 scripts/build_analysis_narrative.py`. Ini tidak menjalankan model. Generator Word lama `make_docx_v4.py` sudah dinonaktifkan agar tidak menghasilkan klaim/metadata lama; gunakan arahan pada [make_docx_rapih.py](../scripts/paper/make_docx_rapih.py) bila ekspor Word memang diminta. Tidak ada DOCX yang diregenerasi pada pembaruan ini.

## Dataset dan arsip

| Peran | Lokasi |
|---|---|
| Source enam kelas | `data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/` |
| Turunan source empat kelas | `data/NRDD-2024/RDD_4class/` |
| Target final | [RDD-indo-v4](../data/RDD-indo-v4/): Roboflow versi 4, 307 gambar, 502 anotasi, 39 label kosong; split valid sebagai test |
| Bahan mentah | `data/archive/`, tetap dipertahankan |
| Ekspor target sebelumnya | `data/_archive/`; nama lama di `data/` hanya alias kompatibilitas |
| Remapping V4 | `runs/rdd_yolov8n_local/indo_v4_remapped/` |

Baca [data/README.md](../data/README.md) untuk mapping kelas dan protokol. Remapped views lama tetap berupa direktori fisik karena notebook lama memakai `shutil.rmtree(REM)`. Alias historis masih writable; jangan menulis run baru ke alias karena dapat menimpa arsip.

## Notebook dan analisis domain

Semua notebook tetap di lokasi dan pada isi awal tugas ini, termasuk perubahan pengguna yang sudah ada sebelumnya. Konfigurasi aktif harus diverifikasi dari run sebenarnya.

| Kebutuhan | Lokasi / status |
|---|---|
| Training komparatif bertahap | `code/03_1_modelling_comparative_local.ipynb`, `03_2_...`, `03_3_...` |
| Training ablasi | `code/04_1_modelling_4class.ipynb` sampai `04_4_modelling_4class.ipynb` |
| Zero-shot V4 | [05_zero_shot_indo_v4.ipynb](../code/05_zero_shot_indo_v4.ipynb); header/agregasi notebook belum diubah |
| Analisis negara | [06_per_country_analysis.ipynb](../code/06_per_country_analysis.ipynb); agregat notebook lama tidak selalu empat kelas bersama |
| Visualisasi domain historis | [07_domain_visualization.ipynb](../code/07_domain_visualization.ipynb), masih menunjuk V2 |
| Bundle V2 | [arsip domain_viz](../runs/_archive/indonesia_v2/domain_viz/), 995 sumber + 308 Indonesia V2; tidak ditimpa |
| Script V4 yang disiapkan | [domain_analysis_v4.py](../scripts/domain_analysis_v4.py), target 995+307=1302 gambar; eksekusi ditunda |
| Folder V4 parsial | `runs/rdd_yolov8n_local/evaluation/domain_viz_v4/`, ditandai `INCOMPLETE.md` dan `run_status.json`; tidak memiliki hasil akhir/provenance lengkap |
| Rekonstruksi PD/RD | [code/models/README.md](../code/models/README.md); model executable tidak diubah |
| Dependensi riset | [requirements_yolov8_local.txt](../code/requirements_yolov8_local.txt) |

Setelah GPU tersedia dan pengguna melanjutkan eksekusi, jalankan `python3.12 scripts/domain_analysis_v4.py --device 0 --resume`. Script memeriksa kecocokan input/cache dan tidak menulis ke alias V2. Setelah berhasil, figure dan provenance V4 dipublikasikan ke `docs/figures/domain_v4/`; barulah bangun ulang narasi. Menggambar ulang embeddings V2 tidak menghasilkan analisis V4.

## Naskah

| Peran | Acuan / kompilasi yang sudah ada |
|---|---|
| Buku TA aktif | [buku-ta-template/](../latex/buku-ta-template/); `cd latex/buku-ta-template && bash compile.sh`; preview: `bash compile.sh bab123` |
| Source paper | [IEEE-Conference/main.tex](../latex/IEEE-Conference/main.tex); `cd latex/IEEE-Conference && bash compile.sh` |
| Submission ISRITI | [README](../latex/ISRITI-submission/README.md); `cd latex/ISRITI-submission && bash compile-review-revised.sh` |
| PDF submission aktif | [ISRITI_Review_Anonymous_Layout_Revised.pdf](../latex/ISRITI-submission/hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf), enam halaman; snapshot dipertahankan |
| Draft arsitektur dibatalkan | [Manifest arsip](../latex/ISRITI-submission/build/archived-architecture-discussion-2026-11-13/manifest.json); jangan dipulihkan dari petunjuk lama |
| Proposal/naskah terdahulu | [skripsi-telkom/](../latex/skripsi-telkom/) dan [PROPOSAL_TA.md](../latex/PROPOSAL_TA.md) |
| Referensi | `latex/refference/` dan [hasil riset pustaka](../outputs/yolo-road-damage-references.md) |

Naskah LaTeX dan seluruh PDF tidak disunting/dikompilasi. Folder build memuat snapshot dan bukti QA selain intermediates; jangan dibersihkan menyeluruh.

## Kontinuitas dan preservasi

- [Manifest arsip](archive/MANIFEST.json) mencatat 80 pemindahan awal, relokasi Markdown, serta pembaruan isi yang diotorisasi berikutnya.
- Versi sebelum pembaruan isi disimpan di [archive/content-before-update/](archive/content-before-update/). Ringkasan lama dan log [progress/](progress/) tetap sebagai sejarah.
- Kontinuitas berikutnya memakai STATE/MEMORY, tanpa log sesi bertanggal baru.
- Portfolio adalah [repo terpisah](https://github.com/FaarisKhairrudin/road-damage-detection); pembaruan ini hanya untuk repo TA.
