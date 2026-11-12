# Data penelitian

Dataset lengkap disimpan lokal dan diabaikan Git. Pilihan dataset aktif dan lokasi artefak evaluasi dicatat di [docs/FINAL_ARTIFACTS.json](../docs/FINAL_ARTIFACTS.json). Nama folder yang mengandung nomor versi tidak cukup untuk menentukan metadata ekspor; periksa `data.yaml` dan README ekspor.

## Source N-RDD2024

Source penelitian adalah subset China, Japan dan India yang sudah difilter menjadi enam kelas, bukan keseluruhan sepuluh kelas dataset asli. Lokasi yang dipakai notebook:

```text
data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/
  RDD_Split_Final_china_japan_india_6_classes/
    data.yaml
    train/{images,labels}/
    val/{images,labels}/
    test/{images,labels}/
```

Inventaris split yang digunakan: 6.777 train, 1.898 val dan 995 test. Model dipilih menggunakan validasi; test adalah evaluasi akhir. Angka inventaris label mentah dapat berbeda dari label yang dipakai evaluator bila evaluator menghapus anotasi duplikat; gunakan artefak/log untuk definisi setiap angka.

| ID source | Nama kanonis | Kode kerusakan/permukaan |
|---|---|---|
| 0 | Longitudinal_Crack | D00 |
| 1 | Transverse_Crack | D10 |
| 2 | Alligator_Crack | D20 |
| 3 | Pothole | D40 |
| 4 | manhole | D70 |
| 5 | patchy_road | D80 |

YAML subset lama memakai alias `Penutup_Jalan` dan `Tambalan` untuk ID 4 dan 5. Notebook membuat YAML turunan dengan nama kanonis. Urutan ID enam kelas ini tidak boleh disamakan begitu saja dengan ID dataset mentah sepuluh kelas.

Turunan training empat kelas berada pada `data/NRDD-2024/RDD_4class/`. Pembentuknya adalah `code/prepare_4class_dataset.py`: anotasi ID 4/5 dihapus tetapi gambar dan keanggotaan split dipertahankan. Gambar yang tidak lagi memiliki anotasi menjadi background. Jangan membangun ulang turunan ini di atas artefak aktif tanpa memeriksa script dan cakupan pekerjaan terlebih dahulu.

## Target Indonesia final

Target aktif adalah `data/RDD-indo-v4/`, yaitu ekspor **rdd-indo-crop Roboflow versi 4** pada 9 Oktober 2026. Metadata lokal ekspor menyatakan CC BY 4.0. Hanya split `valid/` yang tersedia dan dipakai sebagai target test tanpa fine-tuning.

| Inventaris target | Jumlah |
|---|---:|
| Gambar / file label | 307 / 307 |
| Gambar tanpa anotasi | 39 |
| Seluruh anotasi | 502 |
| Anotasi empat kelas kerusakan | 481 |
| Anotasi patchy road | 21 |
| Anotasi manhole | 0 |

Kelas target memiliki urutan berbeda dari source:

| ID target | Nama pada ekspor | Jumlah anotasi | ID source |
|---|---|---:|---:|
| 0 | alligator crack | 48 | 2 |
| 1 | longitudinal crack | 231 | 0 |
| 2 | patchy road | 21 | 5 |
| 3 | pothole | 70 | 3 |
| 4 | tranverse crack | 132 | 1 |

Mapping target → source adalah `{0:2, 1:0, 2:5, 3:3, 4:1}`. Ejaan `tranverse` berasal dari ekspor. Tampilan remapping yang sudah digunakan ada di `runs/rdd_yolov8n_local/indo_v4_remapped/`; gambar ditautkan ke data asli dan label memakai ID source.

Evaluasi utama menggunakan checkpoint enam kelas dan seluruh 307 gambar, lalu merata-ratakan AP atas **empat kelas kerusakan source ID 0–3** di source dan target. Evaluasi lima kelas bersama, termasuk patchy road, adalah tambahan yang sah dengan cakupan berbeda. Manhole tanpa ground truth tidak dimasukkan sebagai AP nol.

YAML mentah Roboflow memuat path ekspor relatif yang bukan konfigurasi evaluasi lokal siap pakai. Gunakan YAML remapping yang sudah diverifikasi dengan checkpoint, bukan langsung mengasumsikan urutan kelas YAML mentah cocok. Notebook zero-shot V4 belum diperbarui pada tahap dokumentasi ini; jangan menimpa remapping/hasil final dengan menjalankan ulang tanpa peninjauan.

## Ekspor historis, bahan mentah dan analisis turunan

- `data/archive/` menyimpan bahan mentah dan dipertahankan.
- `data/_archive/` menyimpan ekspor Indonesia sebelumnya. Jalur lama di `data/` adalah alias kompatibilitas untuk pembacaan notebook/script historis, bukan pilihan dataset final.
- `RDD-indo-v4-bak` adalah ekspor Roboflow versi 3 dengan 514 anotasi. Ia berbeda dari V4 final dan tidak boleh dianggap salinan identik.
- Alias masih dapat ditulis. Jangan memakai jalur historis sebagai tujuan eksperimen baru.
- Bundle visualisasi domain V2 berada di `runs/_archive/indonesia_v2/domain_viz/`. Embeddings atau statistik lama itu tidak menjadi V4 hanya dengan mengganti judul. Pemilihan keluaran V4 yang telah diverifikasi harus mengikuti peta artefak aktif, bukan nama alias lama.

Lihat [laporan penataan](../docs/REORGANIZATION.md) untuk seluruh lokasi asal → tujuan. Notebook dan dataset final tidak dipindahkan pada penataan ini. Versi README sebelumnya tersimpan di [arsip konten](../docs/archive/content-before-update/data/README.md).
