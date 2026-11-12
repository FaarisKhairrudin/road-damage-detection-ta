# Penataan repo dan daftar revisi berikutnya

Pada tahap penataan awal, isi riset dipertahankan dan pembaruan analisis ditunda. Status terbaru setelah pengguna melanjutkan tercantum pada bagian berikut.

## Status terkini setelah pembaruan isi yang disetujui

Pengguna kemudian mengizinkan pembaruan isi dan meminta commit/push ke main. Restriksi struktur-only pada catatan awal di bawah sudah digantikan untuk dokumen dan script laporan; notebook serta source/PDF naskah tetap dipertahankan.

| Bagian | Status sekarang |
|---|---|
| `docs/RESULTS_TABLE.md` | Dihasilkan dari CSV/config/audit final: sumber enam kelas, transfer/ablasi/negara empat kelas, tambahan lima kelas terpisah. |
| `docs/draft-analisis-rapih.md` | Narasi dan 11 gambar diselaraskan dengan hasil final; klaim sebab-akibat/signifikansi yang tidak didukung dikoreksi. |
| README utama, data, model, ISRITI | Metadata/protokol/status diperbarui. Header model diubah hanya sebagai dokumentasi; executable AST tetap. |
| Script laporan | Generator tabel/narasi dapat dijalankan ulang. Generator grafik lama mengarah ke generator final; ekspor Word hardcoded lama dinonaktifkan dan versi aslinya diarsipkan. |
| Draf teknis Markdown | Menunjuk narasi dan tabel aktif; teks lama disimpan pada arsip sebelum pembaruan. |
| Domain V4: UMAP/t-SNE/embeddings/statistik | **Selesai** setelah pengguna melanjutkan dengan GPU. Bundle 995 sumber + 307 V4 diverifikasi dan hasilnya dimasukkan ke narasi. |
| Notebook | Tidak diubah/dieksekusi oleh pekerjaan ini. Perubahan notebook yang sudah ada sebelumnya tetap dipertahankan. |
| Naskah LaTeX/PDF submission | Tidak diubah dan tidak dikompilasi. |
| Kurva training PD empat kelas | `results.csv` tetap tidak ditemukan; tidak dibuat atau diganti dengan run lain. |

Salinan utuh sebelum perubahan isi tersimpan di [archive/content-before-update/](archive/content-before-update/). Rincian hash ada pada `authorized_content_updates` di manifest. Dataset, bobot, log mentah, CSV final asli dan arsip V2 dipertahankan. Tidak ada detector yang dilatih ulang atau DOCX yang dibuat ulang.

Script V4 telah dijalankan hingga selesai setelah pengguna melanjutkan. Narasi hanya menerima bundle dengan status complete, tanpa marker INCOMPLETE, dan hash output yang cocok. Bundle V2 terdahulu tetap berada di arsip.

## Penataan struktur awal — riwayat

- Versi dataset lama, keluaran evaluasi lama, smoke test, backup, dan dua rangkuman lama dipindahkan ke arsip dengan nama aslinya.
- `AGENTS.md` diperbarui mengikuti pola kontinuitas yang diberikan pengguna. `docs/INDEX.md` diringkas menjadi pintu masuk yang menunjuk artefak terkini.
- `.agents/STATE.md` dan `.agents/MEMORY.md` menyimpan status dan pengetahuan; tidak dibuat log sesi bertanggal baru.
- `docs/FINAL_ARTIFACTS.json` memetakan sepuluh eksperimen final, target V4, dan naskah aktif tanpa menghitung ulang metrik.
- Keadaan working tree `AGENTS.md` dan `docs/INDEX.md` sebelum penataan disalin utuh ke `docs/archive/navigation/`; perubahan yang sudah ada sebelumnya tidak hilang.

## Yang dipertahankan pada tahap struktur awal

- Seluruh 16 notebook tetap pada lokasi asal, tanpa edit sel/output/metadata maupun eksekusi ulang.
- Seluruh script, model/YAML, source naskah, referensi, gambar naskah, dataset final, bobot final dan CSV final dipertahankan isinya.
- `README.md`, `data/README.md`, `docs/RESULTS.md`, `docs/RESULTS_TABLE.md`, README model dan README ISRITI tidak ditulis ulang. Kekurangan isinya tercatat di bawah.
- Folder `runs/rdd_4class_local_pc_lab/` tetap tersedia: CSV final v8n/v12n/v26n tidak boleh hilang.
- `data/archive/` tetap berisi bahan mentah. Remapped views tetap direktori fisik. Folder LaTeX termasuk build/snapshot/QA dan PDF submission dipertahankan.
- Tidak ada penghapusan permanen, kompilasi LaTeX, training, inference, atau sinkronisasi/publikasi GitHub pada tahap ini.

## Cara membaca arsip dan alias

Lokasi tujuan pada tabel adalah lokasi fisik baru. Bila kolom alias berisi **ya**, nama pada lokasi asal sekarang adalah symlink relatif ke arsip, agar notebook/script/tautan lama tetap dapat menemukan inputnya. Alias tidak menandakan bahwa versi itu aktif atau final.

Alias masih dapat ditulis. Menjalankan ulang notebook lama dapat menimpa isi arsip melalui alias; jangan memakai alias sebagai tujuan run baru. Pembaruan analisis berikutnya perlu direktori output baru dan otorisasi perubahan isi.

Dua rangkuman lama masih dapat dibuka melalui alias lama untuk menjaga tautan README/progress yang isinya belum diubah. Pilihan konteks kerja yang berlaku ada di [INDEX.md](INDEX.md), bukan kata “final” yang tertulis dalam rangkuman historis.

## Daftar lengkap asal → tujuan

Terdapat **80 kelompok pemindahan** dan **46 alias kompatibilitas**. Folder dipindahkan beserta seluruh isi dan struktur internalnya. [Manifest mesin](archive/MANIFEST.json) memuat alasan, jumlah berkas, ukuran, dan hash pohon setiap kelompok.

| Asal | Tujuan fisik | Alias di asal |
|---|---|---|
| `data/RDD-Indonesia.v1i.yolov8` | `data/_archive/RDD-Indonesia.v1i.yolov8` | ya |
| `data/RDD-indo-v2` | `data/_archive/RDD-indo-v2` | ya |
| `data/RDD-indo-v3` | `data/_archive/RDD-indo-v3` | ya |
| `data/RDD-indo-v4-bak` | `data/_archive/RDD-indo-v4-bak` | ya |
| `docs/rangkuman-eksperimen-ta.md` | `docs/archive/summaries/rangkuman-eksperimen-ta.md` | ya |
| `docs/rangkuman-eksperimen-ta-v2.md` | `docs/archive/summaries/rangkuman-eksperimen-ta-v2.md` | ya |
| `docs/Salah prediksi Merge 1.txt` | `docs/archive/working-notes/Salah prediksi Merge 1.txt` | tidak |
| `runs/rdd_yolov8n_local_bak` | `runs/_archive/backup/rdd_yolov8n_local_bak` | tidak |
| `runs/detect` | `runs/_archive/ad_hoc/detect` | tidak |
| `code/runs/detect` | `runs/_archive/ad_hoc/code_detect` | tidak |
| `runs/proposal_text_mining_render` | `runs/_archive/unrelated/proposal_text_mining_render` | tidak |
| `runs/proposal_text_mining_flowchart.png` | `runs/_archive/unrelated/proposal_text_mining_flowchart.png` | tidak |
| `runs/rdd_yolov8n_local/evaluation/domain_viz` | `runs/_archive/indonesia_v2/domain_viz` | ya |
| `runs/rdd_yolov8n_local/evaluation/zero_shot_indonesia` | `runs/_archive/indonesia_history/zero_shot_indonesia` | ya |
| `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v2` | `runs/_archive/indonesia_history/zero_shot_indo_v2` | ya |
| `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v3` | `runs/_archive/indonesia_history/zero_shot_indo_v3` | ya |
| `runs/rdd_yolov8n_local/experiments/yolo_rd_focal_smoke` | `runs/_archive/experiments_history/rdd_yolov8n_local/experiments/yolo_rd_focal_smoke` | ya |
| `runs/rdd_yolov8n_local/experiments/yolov12n_focal` | `runs/_archive/experiments_history/rdd_yolov8n_local/experiments/yolov12n_focal` | ya |
| `runs/rdd_yolov8n_local/experiments/yolov12n_focal_smoke` | `runs/_archive/experiments_history/rdd_yolov8n_local/experiments/yolov12n_focal_smoke` | ya |
| `runs/rdd_yolov8n_local/experiments/yolov26n_focal` | `runs/_archive/experiments_history/rdd_yolov8n_local/experiments/yolov26n_focal` | ya |
| `runs/rdd_yolov8n_local/experiments/yolov26n_focal_smoke` | `runs/_archive/experiments_history/rdd_yolov8n_local/experiments/yolov26n_focal_smoke` | ya |
| `runs/rdd_yolov8n_local/experiments/yolov8_pd_focal_smoke` | `runs/_archive/experiments_history/rdd_yolov8n_local/experiments/yolov8_pd_focal_smoke` | ya |
| `runs/rdd_yolov8n_local/experiments/yolov8n_focal_smoke` | `runs/_archive/experiments_history/rdd_yolov8n_local/experiments/yolov8n_focal_smoke` | ya |
| `runs/rdd_yolov8n_local/evaluation/test_baseline` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/test_baseline` | ya |
| `runs/rdd_yolov8n_local/evaluation/val_baseline` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/val_baseline` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolo_rd_focal_test` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolo_rd_focal_test` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolo_rd_focal_val` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolo_rd_focal_val` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov12n_focal_test` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov12n_focal_test` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov12n_focal_val` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov12n_focal_val` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov26n_focal_test` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov26n_focal_test` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov26n_focal_val` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov26n_focal_val` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov8_pd_focal_test` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov8_pd_focal_test` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov8_pd_focal_val` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov8_pd_focal_val` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov8n_focal_test` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov8n_focal_test` | ya |
| `runs/rdd_yolov8n_local/evaluation/yolov8n_focal_val` | `runs/_archive/experiments_history/rdd_yolov8n_local/evaluation/yolov8n_focal_val` | ya |
| `runs/rdd_4class_local/experiments/yolo_rd_4cls_smoke` | `runs/_archive/experiments_history/rdd_4class_local/experiments/yolo_rd_4cls_smoke` | ya |
| `runs/rdd_4class_local/experiments/yolov8n_4cls_smoke` | `runs/_archive/experiments_history/rdd_4class_local/experiments/yolov8n_4cls_smoke` | ya |
| `runs/rdd_4class_local/evaluation/yolo_rd_4cls_smoke_test` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolo_rd_4cls_smoke_test` | ya |
| `runs/rdd_4class_local/evaluation/yolo_rd_4cls_smoke_val` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolo_rd_4cls_smoke_val` | ya |
| `runs/rdd_4class_local/evaluation/yolo_rd_4cls_test` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolo_rd_4cls_test` | ya |
| `runs/rdd_4class_local/evaluation/yolo_rd_4cls_val` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolo_rd_4cls_val` | ya |
| `runs/rdd_4class_local/evaluation/yolov8n_4cls_smoke_test` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolov8n_4cls_smoke_test` | ya |
| `runs/rdd_4class_local/evaluation/yolov8n_4cls_smoke_val` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolov8n_4cls_smoke_val` | ya |
| `runs/rdd_4class_local/evaluation/yolov8n_4cls_test` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolov8n_4cls_test` | ya |
| `runs/rdd_4class_local/evaluation/yolov8n_4cls_val` | `runs/_archive/experiments_history/rdd_4class_local/evaluation/yolov8n_4cls_val` | ya |
| `runs/rdd_4class_local_pc_lab/experiments/yolo_rd_4cls_smoke` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/experiments/yolo_rd_4cls_smoke` | ya |
| `runs/rdd_4class_local_pc_lab/experiments/yolov8_pd_4cls` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/experiments/yolov8_pd_4cls` | ya |
| `runs/rdd_4class_local_pc_lab/experiments/yolov8n_4cls_smoke` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/experiments/yolov8n_4cls_smoke` | ya |
| `runs/rdd_4class_local_pc_lab/evaluation/yolo_rd_4cls_test` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/evaluation/yolo_rd_4cls_test` | ya |
| `runs/rdd_4class_local_pc_lab/evaluation/yolo_rd_4cls_val` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/evaluation/yolo_rd_4cls_val` | ya |
| `runs/rdd_4class_local_pc_lab/evaluation/yolov8n_4cls_test` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/evaluation/yolov8n_4cls_test` | ya |
| `runs/rdd_4class_local_pc_lab/evaluation/yolov8n_4cls_val` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/evaluation/yolov8n_4cls_val` | ya |
| `runs/rdd_4class_local/yolo_rd_4cls_f1_summary.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_f1_summary.csv` | tidak |
| `runs/rdd_4class_local/yolo_rd_4cls_smoke_f1_summary.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_smoke_f1_summary.csv` | tidak |
| `runs/rdd_4class_local/yolo_rd_4cls_smoke_summary.json` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_smoke_summary.json` | tidak |
| `runs/rdd_4class_local/yolo_rd_4cls_smoke_test_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_smoke_test_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local/yolo_rd_4cls_smoke_val_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_smoke_val_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local/yolo_rd_4cls_summary.json` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_summary.json` | tidak |
| `runs/rdd_4class_local/yolo_rd_4cls_test_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_test_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local/yolo_rd_4cls_val_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolo_rd_4cls_val_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_f1_summary.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_f1_summary.csv` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_smoke_f1_summary.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_smoke_f1_summary.csv` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_smoke_summary.json` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_smoke_summary.json` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_smoke_test_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_smoke_test_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_smoke_val_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_smoke_val_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_summary.json` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_summary.json` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_test_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_test_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local/yolov8n_4cls_val_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local/metrics/yolov8n_4cls_val_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local_pc_lab/yolo_rd_4cls_f1_summary.csv` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolo_rd_4cls_f1_summary.csv` | tidak |
| `runs/rdd_4class_local_pc_lab/yolo_rd_4cls_summary.json` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolo_rd_4cls_summary.json` | tidak |
| `runs/rdd_4class_local_pc_lab/yolo_rd_4cls_test_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolo_rd_4cls_test_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local_pc_lab/yolo_rd_4cls_val_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolo_rd_4cls_val_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local_pc_lab/yolov8n_4cls_f1_summary.csv` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolov8n_4cls_f1_summary.csv` | tidak |
| `runs/rdd_4class_local_pc_lab/yolov8n_4cls_summary.json` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolov8n_4cls_summary.json` | tidak |
| `runs/rdd_4class_local_pc_lab/yolov8n_4cls_test_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolov8n_4cls_test_per_class_metrics.csv` | tidak |
| `runs/rdd_4class_local_pc_lab/yolov8n_4cls_val_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_4class_local_pc_lab/metrics/yolov8n_4cls_val_per_class_metrics.csv` | tidak |
| `runs/rdd_yolov8n_local/baseline_summary.json` | `runs/_archive/experiments_history/rdd_yolov8n_local/baseline_metrics/baseline_summary.json` | tidak |
| `runs/rdd_yolov8n_local/test_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_yolov8n_local/baseline_metrics/test_per_class_metrics.csv` | tidak |
| `runs/rdd_yolov8n_local/val_per_class_metrics.csv` | `runs/_archive/experiments_history/rdd_yolov8n_local/baseline_metrics/val_per_class_metrics.csv` | tidak |
| `runs/rdd_yolov8n_local/f1_summary.csv` | `runs/_archive/experiments_history/rdd_yolov8n_local/baseline_metrics/f1_summary.csv` | tidak |

### Salinan navigasi sebelum diganti

| Asal yang diperbarui | Salinan utuh sebelumnya |
|---|---|
| `AGENTS.md` | `docs/archive/navigation/AGENTS.pre-organization.md` |
| `docs/INDEX.md` | `docs/archive/navigation/INDEX.pre-organization.md` |

## Daftar koreksi awal — lihat status pembaruan di bagian atas

Prioritas ini memisahkan koreksi dokumentasi, penyesuaian cakupan metrik, dan analisis yang benar-benar perlu dijalankan ulang. Jangan menimpa hasil historis untuk membuatnya terlihat sebagai hasil data baru.

| Prioritas | File / analisis | Perubahan isi yang diperlukan |
|---|---|---|
| 1 | `README.md` | Perbarui cerita baseline-only, native loss/Focal Loss opsional, notebook utama, dan contoh patience 50 agar sesuai eksperimen final. |
| 1 | `data/README.md` | Tambahkan dataset target final V4, split valid sebagai test, versi ekspor dan mapping label. |
| 1 | `docs/RESULTS_TABLE.md` | Koreksi footer metadata Roboflow V3; pisahkan empat kelas utama vs lima kelas tambahan; arahkan perbandingan negara ke empat kelas bersama. Jangan mengganti angka 0.337 menjadi 0.413 tanpa mengubah label/cakupan tabel: keduanya mengukur himpunan kelas berbeda. |
| 1 | `docs/RESULTS_TABLE.md` bagian kompleksitas | Selaraskan dengan protokol fused `model_complexity.json` dan bukti `RESULTS.md`; jelaskan perbedaan protokol, jangan menghapus log mentah. |
| 1 | `latex/ISRITI-submission/README.md` | Ubah status draft arsitektur tujuh halaman menjadi dibatalkan/diarsipkan; hapus arahan seolah discussion/compile-discussion.sh masih aktif. Snapshot PDF terunggah tetap dipertahankan. |
| 2 | `code/07_domain_visualization.ipynb` dan arsip `domain_viz` | Notebook memakai V2. Ketika edit notebook diizinkan, regenerasi pada 995 source + 307 V4 = 1302 gambar: manifest, embeddings, domains, UMAP, t-SNE, statistik citra, dan sampel. Saat ini masih 995+308 V2. |
| 2 | `scripts/paper/paper_fig_umap.py` dan gambar domain pada naskah | Plotting script membaca embeddings lama; menggambar ulang saja tidak cukup. Setelah bundle V4 baru diverifikasi, perbarui rute input, figure turunan dan caption. Figur lama dibiarkan karena source naskah belum diubah. |
| 2 | `code/05_zero_shot_indo_v4.ipynb` | Header masih menyebut 308; output final mencatat 307/502. Agregasi utamanya masih lima kelas. Tambahkan pemisahan empat kelas utama vs lima tambahan ketika perubahan notebook diizinkan. |
| 2 | `code/06_per_country_analysis.ipynb` | Evaluasi agregat negara lama mengikuti kelas yang tersedia. Untuk perbandingan utama gunakan empat kelas kerusakan yang sama. Notebook belum disentuh. |
| 2 | `scripts/paper/paper_figs_summary.py` | Hardcoded kompleksitas dan agregat negara lama; kemudian baca artefak final/empat kelas bersama. |
| 2 | `scripts/paper/paper_figs_v4.py`, `scripts/run_zs_v4_finish.py`, dan gambar domain-gap yang ada | Tinjau label serta cakupan empat vs lima kelas. Angka V4 lima kelas masih valid sebagai suplemen; tidak otomatis merupakan hasil dataset lama. |
| 2 | `scripts/paper/make_docx_v4.py` dan ekspor Word turunannya | Metadata V3, 514 anotasi dan beberapa hitungan kelas masih lama. Audit sebelum membuat ekspor baru. |
| 3 | `code/models/README.md` | Bedakan tabel smoke test Focal Loss historis dari weighting BCE pada run final, dan verifikasi klaim versi dependensi. |
| 3 | Header `code/models/custom_modules.py` | Klaim torchvision 0.28.0 berbeda dengan README model; verifikasi environment dulu, jangan mengganti versinya berdasarkan dugaan. |
| 3 | `runs/rdd_4class_local/experiments/yolov8_pd_4cls_class_weights/results.csv` | File kurva ini tidak ditemukan. Registry menandainya null/unavailable; telusuri salinan asli sebelum menjanjikan kurva training PD empat kelas. Jangan mengarang atau mengganti dengan run lain. |
| Historis | `docs/archive/summaries/rangkuman-eksperimen-ta*.md` | Dipertahankan sebagai sejarah dan tidak perlu dibetulkan agar tampak mutakhir. Bila dibutuhkan narasi baru, tulis dari artefak final, bukan menimpa sejarahnya. |

## Hasil tetap aktif dan perannya

- `docs/RESULTS_TABLE.md`: tabel yang sudah ada, dipertahankan dengan caveat di INDEX; tidak menjadi bukti bahwa semua bagian telah mutakhir.
- `docs/RESULTS.md`: log mentah/bukti evaluasi, bukan versi ringkasan lain yang perlu dihapus.
- `docs/FINAL_ARTIFACTS.json`: pemilihan sumber data/angka terbaru. CSV source per kelas dan CSV V4 yang ditunjuk adalah acuan saat koreksi isi berikutnya.
- Primary transfer memakai empat damage classes; lima kelas termasuk patchy road tetap analisis tambahan. Tidak ada perhitungan ulang atau penggantian angka dalam penataan ini.

## Status naskah

PDF aktif submission tetap `latex/ISRITI-submission/hasil/ISRITI_Review_Anonymous_Layout_Revised.pdf` (enam halaman). Draft diskusi arsitektur sudah dibatalkan atas permintaan pengguna; manifest terdahulunya ada pada `latex/ISRITI-submission/build/archived-architecture-discussion-2026-11-13/manifest.json`. Penataan ini tidak memulihkan draft tersebut maupun menyentuh snapshot submission.

## Pemeriksaan

Validasi struktur dan preservasi dicatat pada `verification` di [MANIFEST.json](archive/MANIFEST.json). Penghitungan ulang ilmiah, eksekusi notebook, inference/training, dan kompilasi PDF tidak dijalankan karena di luar cakupan tahap ini.

- Preservasi inventaris awal: 60906 entri; 4352 berkas diverifikasi SHA-256.
- Seluruh 16 notebook tetap identik di lokasi asal.
- 80 kelompok arsip dan 46 alias terverifikasi; tidak ada symlink lama yang menjadi rusak.
- Lokasi artefak 10 eksperimen final dan SHA-256 PDF submission aktif terverifikasi.
- Pemeriksaan akhir navigasi: 37 tautan lokal valid; seluruh 80 baris pemindahan dan 46 penanda alias cocok dengan manifest; pemeriksaan whitespace Git lulus.


## Tindak lanjut yang diminta: pindahkan analisis bergambar ke docs

Penataan awal di atas dipertahankan sebagai bukti tahap sebelumnya. Setelah pengguna meminta pemindahan spesifik, dilakukan tindak lanjut berikut:

| Asal | Tujuan | Penyesuaian |
|---|---|---|
| `latex/IEEE-Conference/draft/draft-analisis-rapih.md` | [docs/draft-analisis-rapih.md](draft-analisis-rapih.md) | Hanya 15 jalur gambar relatif yang disesuaikan; narasi, angka, tabel dan gambar asli tetap. |

Input `scripts/paper/make_docx_rapih.py` diarahkan ke lokasi baru dan resolusi gambarnya mengikuti direktori Markdown. Output DOCX tidak dibuat ulang. Draft teknis `draft-analisis-hasil.md` tetap di lokasi semula. Peta artefak dan indeks turut diperbarui. Rekam hash dan pemeriksaan ada pada `authorized_followups` di manifest; hasil verifikasi penataan awal adalah rekam tahap sebelumnya, bukan klaim bahwa jalur Markdown ini belum dipindahkan.


## Tindak lanjut: analisis domain V4 selesai

Setelah NVIDIA aktif, pengguna mengizinkan melanjutkan. Ekstraksi memakai Python 3.12, RTX 3050 dan checkpoint YOLOv8n final, tanpa training ulang. Dihasilkan 1.302 embedding berdimensi 256, UMAP, t-SNE, statistik dan sampel. Hitungan tiap domain, urutan manifest, hash keluaran dan angka proyeksi terverifikasi; empat gambar diperiksa visual.

Keluaran fisik: `runs/rdd_yolov8n_local/evaluation/domain_viz_v4/`; gambar dan provenance yang dapat dibaca di dokumentasi: `docs/figures/domain_v4/`. Median statistik V4 Indonesia berbeda dari sebagian hasil V2 lama; gunakan narasi terkini, bukan tabel lama. Hasil ini deskriptif dan tidak menetapkan sebab-akibat. Notebook dan PDF submission tidak diubah.
