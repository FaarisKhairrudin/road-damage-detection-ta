# Indeks & Ringkasan Proposal TA (untuk konteks LLM)

> **Fungsi file ini:** peta konten proposal TA dalam format hemat token. Gunakan ini sebagai referensi struktur/fakta sebelum membaca file LaTeX individual. Baca file `.tex` asli hanya jika butuh kalimat persisnya.
>
> **Catatan konteks:** Dokumen ini adalah **proposal** (format Telkom University). Saat menulis **skripsi**, struktur akan diperluas (mis. Bab kajian pustaka & metodologi dipecah lebih detail, ditambah Bab hasil & pembahasan, kesimpulan, dsb.).

## Identitas Proyek

| Item | Nilai |
|---|---|
| Judul (ID) | Evaluasi Komparatif dan Uji Generalisasi Arsitektur *Deep Learning* untuk Deteksi Kerusakan dan Cacat Permukaan Jalan di Indonesia |
| Judul (EN) | Comparative Evaluation and Generalization Testing of Deep Learning Architectures for Road Damage and Surface Defect Detection in Indonesia |
| Penulis | Faaris Khairrudin — NIM 103052300115 — Prodi Sains Data |
| Pembimbing | Dr. GAMMA KOSALA, S.Si (satu pembimbing) |
| KK / Gelar | Modelling Computational Experiment / Sains Komputasi |
| Tahun | 2026 (Pengesahan: 4 September) |
| Topik inti | Deteksi objek kerusakan jalan (YOLO), kelas pengecoh (*distractor*), *domain shift*, uji *zero-shot* di Indonesia |

**Alternatif judul (opsi cadangan di `main.tex`, belum dipakai):** (2) "…Analisis *Domain Gap*…", (3) "…Lintas Domain pada Perangkat Terbatas…".

## Peta File

| File | Isi | Bab skripsi |
|---|---|---|
| `main.tex` | Metadata judul/penulis/pembimbing, template, urutan include | — |
| `Cover.tex`, `Lembar-Persetujuan.tex`, `Abstrak-Indo.tex`* | Halaman muka & abstrak | — |
| `Pendahuluan.tex` | Latar belakang, rumusan masalah, tujuan, batasan, rencana & jadwal | BAB I |
| `Kajian-Pustaka.tex` | Landasan teori + tabel penelitian terkait | BAB II |
| `Metodologi.tex` | EDA/data, alur penelitian, arsitektur, metrik, 3 skenario | BAB III |
| `References.bib` | 26 entri pustaka (kunci: lihat glosarium bawah) | Daftar Pustaka |
| `Lampiran.tex` | Kosong (`\chapter*{Lampiran}` placeholder) | Lampiran |
| `gambar/` | 13 gambar (lihat daftar di bawah) | — |

\* `Abstrak-Indo.tex` hanya ada di `build/` (artifact kompilasi); `main.tex` meng-include-nya dari root. Jika re-kompilasi gagal, salin kembali dari `build/`.

---

## Ringkasan per Bagian

### Abstrak (`Abstrak-Indo.tex`)
- Masalah: inspeksi jalan manual tidak efisien; tantangan YOLO di dunia nyata = *false positive* (manhole/tambalan), *domain shift* ke jalan Indonesia, beban komputasi *real-time*.
- Solusi: evaluasi komparatif YOLO *baseline* vs YOLO modifikasi vs YOLO versi mutakhir, dilatih pada N-RDD2024 (subset Asia, memuat kelas pengecoh). Metrik: mAP50, F1 + *trade-off* (GFLOPs, Params, FPS).
- Puncak: model terbaik diuji *zero-shot* pada data primer jalan raya Bandung (tanpa *fine-tuning*) untuk mengukur generalisasi & *domain gap*.
- Kata kunci: Deteksi Kerusakan Jalan, YOLO, Domain Shift, Zero-Shot Inference, N-RDD2024, Lightweight Model.

### BAB I — Pendahuluan (`Pendahuluan.tex`)

**1.1 Latar Belakang** — alur argumen (5 tahap):
1. Jalan = fondasi ekonomi; kerusakan (retak/lubang) menaikkan risiko kecelakaan, kritis di Indonesia (beban muatan berlebih, iklim tropis, drainase buruk) → `hugo2025efficientdet`, `kusumah2023deep`.
2. Inspeksi manual: tidak efisien, subjektif, padat karya, tidak skalabel → `Li2024`, `hosseini2021prediction`.
3. *Deep learning* & YOLO unggul untuk otomasi deteksi (F1 0,5814/0,5751 mengalahkan CenterNet & EfficientDet) → `mandal2020deep`; banyak varian: RDD-YOLO, YOLOv8-PD, YOLO-RD, YOLO-LWD, YOLO-LWNet.
4. Benchmark umum = RDD2022 (47.420 citra, 6 negara, kelas D00/D10/D20/D40; F1 terbaik CRDDC2022 = 0,770) → `Arya2024846`.
5. **Dua research gap:**
   - *Domain shift*: model degradasi lintas negara; **Indonesia tidak terwakili di RDD2022**; EfficientDet-D0 pada data lokal hanya F1 59,7%.
   - *False positive* dari objek mirip visual (manhole, patch): akurasi D40 YOLOv8-PD hanya 53,1%; N-RDD2024 (`kaya2024nrdd2024`) menambah kelas D30/D50/D60/D70/D80/D90 — D70 (manhole) & D80 (patch) diadopsi sebagai **kelas pengecoh**.
- Celah riset final: belum ada studi komparatif sistematis pada N-RDD2024 dengan kelas pengecoh + pengukuran *domain gap* eksplisit *zero-shot* di Indonesia.

**1.2 Rumusan Masalah (3):**
1. Performa deteksi model DL dilatih dengan N-RDD2024 yang memuat kelas kerusakan + pengecoh?
2. Performa & kelayakan *real-time* pada perangkat terbatas ditinjau dari efisiensi komputasi?
3. Berapa *domain gap*/generalisasi model terbaik saat diuji *zero-shot* pada data primer jalan raya Indonesia?

**1.3 Tujuan Penelitian** — paralel dengan rumusan: (1) evaluasi & komparasi akurasi (mAP) YOLO baseline vs modifikasi vs terbaru + analisis penekanan FP dari pengecoh; (2) analisis *trade-off* akurasi vs efisiensi (FPS, Params, GFLOPs) → pilih model terbaik; (3) uji *zero-shot* model terbaik pada data Bandung tanpa *fine-tuning* → ukur *accuracy drop* = besaran *domain shift*.

**1.4 Batasan Masalah (5):**
1. Pelatihan hanya subset **Asia** N-RDD2024 (India, Tiongkok, Jepang) — domain sumber yang diasumsikan mirip Indonesia, bukan representasi langsung.
2. Deteksi hanya anomali aspal/beton: 4 kelas struktural + 2 kelas pengecoh (total **6 kelas**).
3. Hanya deteksi objek (lokalisasi + klasifikasi); **tanpa estimasi severity**.
4. Data primer: rute jalan raya/jalan besar Bandung, siang hari (isolasi variabel pencahayaan).
5. Uji efisiensi di NVIDIA RTX 4070 Ti 12GB; **tanpa deployment aplikasi**.

**1.5 Rencana Kegiatan (6 tahap):** studi literatur → pengumpulan & prapemrosesan data (sekunder + primer) → perancangan skenario evaluasi → pelatihan & implementasi model (termasuk Focal Loss untuk imbalance) → pengujian & analisis (Precision/Recall/mAP + FPS/Params/GFLOPs, *error analysis* pothole vs pengecoh) → penyusunan laporan.

**1.6 Jadwal Kegiatan** — Gantt 6 bulan (Tabel `tab:jadwal`): kajian pustaka (bln 1–4), data (1–2), skenario (2–3), pelatihan model (3–4), pengujian (4–5), laporan (2–6).

### BAB II — Kajian Pustaka (`Kajian-Pustaka.tex`)

**2.1 Kerusakan jalan & N-RDD2024:**
- 4 kelas kerusakan struktural standar: D00 (retak memanjang), D10 (retak melintang), D20 (retak buaya), D40 (lubang).
- RDD2022 = basis; N-RDD2024 = perluasan Kaya & Çodur jadi **10 kelas** (+D30 retak diperbaiki, D50 pejalan kaki, D60 marka, D70 manhole, D80 patchy road, D90 rutting).
- D70 & D80 = kelas pengecoh eksplisit untuk menekan FP (Matouq dkk., Shi).
- Masalah turunan: **class imbalance** (pothole langka) → perlu strategi khusus saat training.

**2.2 YOLO:**
- *One-stage detector*, regresi *end-to-end*, prediksi bbox+kelas dalam *single forward pass* (Redmon dkk.).
- Evolusi: YOLOv1→v2/YOLO9000→v3 (residual, SPP, CSPNet) → v4 (Mosaic, atensi spasial) → **YOLOv8** (Ultralytics 2023, anchorless head).
- YOLOv8 = Backbone / Neck / Head; varian n/s/m/l/x; **YOLOv8n/s = kandidat baseline ringan**.

**2.3 Modifikasi arsitektur untuk efisiensi:**
- **Mekanisme atensi** (SimAM tanpa parameter tambahan, CBAM) → fokus pada retakan tipis, tekan noise.
- **GhostConv** pada Neck → reduksi parameter & GFLOPs drastis.
- **Loss adaptif** (Focal Loss, REG-*Refined Generalized Focal Loss*) → bobot penalti kelas minoritas.

**2.4 Domain shift & zero-shot:**
- Domain shift = degradasi performa lintas wilayah; penuh risiko untuk Indonesia (F1 lokal bahkan dengan fine-tuning hanya 59,7%).
- Uji *zero-shot* = evaluasi langsung tanpa *fine-tuning*; justifikasi: anotasi ulang data lokal mahal waktu/tenaga → ukur generalisasi murni.

**2.5 Penelitian terkait (Tabel `tab:penelitian_terkait`)** — 5 SOTA + usulan:

| Ref | Metode/Dataset | Kekurangan kunci |
|---|---|---|
| Li2024 | RDD-YOLO (v8+SimAM+GhostConv), RDD2022 | Tanpa uji domain shift; tanpa kelas pengecoh |
| Zeng2024 | YOLOv8-PD (v8n+GhostNet), RDD2022 | D40 anjlok 53,1% (imbalance) |
| matouq2024ai | YOLOv8 segmentation, data Ohio custom | Data mandiri mahal; komputasi besar |
| hugo2025efficientdet | EfficientDet-D0, jalan Indonesia | F1 hanya 59,7% (generalisasi lokal sulit) |
| Shi_2026 | YOLO-LWD (GhostConv+ECA), Aug-RDD | *Single domain* (Tiongkok) saja |
| **Usulan** | Komparatif YOLO lightweight, N-RDD2024 + jalan Indonesia | — (gabungan kelas pengecoh + zero-shot Indonesia) |

### BAB III — Metodologi dan Desain Sistem (`Metodologi.tex`)

**3.1 Eksplorasi Data (EDA):**
- **Data sekunder (latihan):** N-RDD2024 subset Asia (India, China, Jepang) — awal **10.395 citra**, setelah penyaringan 6 kelas target → **9.670 citra**, resolusi asli 640×640, format anotasi YOLO.
- **Data primer (uji zero-shot):** jalan raya Bandung, target **≥500 citra** berlabel; rekam 1080p/30fps sudut pengendara roda dua, siang hari; frame diekstraksi per interval/*scene change*; dilabel manual via **CVAT/Roboflow**, validasi manual, standar bbox mengikuti N-RDD2024/RDD2022.
- **Visualisasi/statistik kunci (pakai angka ini saat menulis skripsi):**
  - Distribusi citra per negara: **Jepang 6.638 (68,6%)**, Tiongkok 1.977 (20,4%), India 1.055 (10,9%).
  - Total **24.290 objek**; retak memanjang 6.447 & retak buaya 6.272 (mayoritas); patchy road hanya **672** (paling langka); pothole 3.101; manhole 3.236.
  - Anomali lokal: 3.051/3.236 manhole eksklusif dari Jepang; 994 pothole di India.
  - Luas bbox: **right-skewed ekstrem**; median **1,69%** luas citra; P90 = 17,19% → dominasi objek kecil → justifikasi Focal Loss & atensi.
- Gambar terkait: distribusi_gambar, object_sample, object_per_country, distribusi_kelas, distribusi_kelas_country, distribusi_luas.

**3.2 Alur Penelitian (flowchart `fig:alur_penelitian`):**
Pengumpulan data (sekunder + primer + labeling) → EDA → **data splitting 70:20:10** (train/val/test) → preprocessing (resize 640×640, normalisasi, augmentasi **Mosaic**) → pemodelan 3 skenario → evaluasi (deteksi + efisiensi) → uji zero-shot model terbaik → analisis & kesimpulan.

**3.3 Rancangan Arsitektur Model (YOLO):**
- **Backbone:** Conv + C2f + SPPF; target penyisipan atensi (SimAM, SOM) untuk objek kecil.
- **Neck:** fusi multi-skala (Upsample + Concat); modifikasi lightweight = **GhostConv**.
- **Head:** *decoupled head* (klasifikasi & lokalisasi terpisah) + **NMS**.
- Gambar: rancangan_implementasi, arsitektur_yolov8_standar, arsitektur_yolov8_modifikasi.

**3.4 Evaluasi Performa Model:**
- Confusion matrix berbasis IoU threshold: TP / FP / FN (definisi standar, IoU > 0,5).
- Precision = TP/(TP+FP); Recall = TP/(TP+FN); F1 = harmonic mean.
- IoU = overlap/union; **mAP@0.5** utama; tambahan multi-skala **mAP_s (<32×32 px), mAP_m, mAP_l**.
- Efisiensi komputasi: **Params (M)**, **GFLOPs**, **FPS**.

**3.5 Skenario Penelitian (3, menjawab 3 rumusan masalah):**
1. **Skenario 1 — Evaluasi domain sumber + analisis pengecoh:** latih & bandingkan YOLOv8n (baseline), model modifikasi (modul atensi + konvolusi ringan, adaptasi YOLO-RD / RDD-YOLO / YOLOv8-PD), dan iterasi mutakhir (**YOLOv12, YOLOv26**) pada N-RDD2024. Keluaran: mAP, F1, Confusion Matrix (penekanan FP terhadap D70/D80), penanganan imbalance via Focal Loss/pembobotan kelas.
2. **Skenario 2 — Trade-off & kelayakan real-time:** bandingkan mAP vs FPS/Params/GFLOPs (benchmark di RTX 4070 Ti 12GB) → pilih 1 model terbaik.
3. **Skenario 3 — Uji zero-shot lintas domain:** bobot model terbaik diuji langsung pada dataset primer Bandung tanpa fine-tuning; selisih akurasi Skenario 1 vs 3 = **besaran domain gap**.

---

## Daftar Gambar (folder `gambar/`)

| File | Dipakai di | Label/isi |
|---|---|---|
| contoh_label_RDD.png | Kajian Pustaka | Contoh kelas D00/D10/D20/D40 RDD2022 |
| arsitektur_yolov8_standar.png | Kajian Pustaka | Arsitektur YOLOv8 (Li dkk. 2024) |
| arsitektur_yolov8_modifikasi.png | Kajian Pustaka | Contoh modifikasi YOLOv8 efisien |
| distribusi_gambar.png | Metodologi | Distribusi citra per negara |
| object_sample.png | Metodologi | Contoh bbox 6 kelas target |
| object_per_country.png | Metodologi | Karakteristik citra per negara |
| distribusi_kelas.png | Metodologi | Distribusi objek per kelas |
| distribusi_kelas_country.png | Metodologi | Sebaran objek per kelas per negara |
| distribusi_luas.png | Metodologi | Histogram luas bbox (% citra) |
| flowchart_penelitian.png / flowchart_penelitian_1.png | Metodologi | Flowchart alur penelitian |
| rancangan_implementasi.png | Metodologi | Ilustrasi alur kerja YOLO |

## Glosarium Kutipan (kunci BibTeX → topik)

- `Arya2024846` — RDD2022 & CRDDC2022 (dataset benchmark, domain shift lintas negara)
- `kaya2024nrdd2024` — N-RDD2024 (10 kelas, termasuk D70/D80)
- `hugo2025efficientdet` — EfficientDet-D0 di Indonesia (F1 59,7%)
- `matouq2024ai` — FP manhole vs pothole vs patch; anotasi pengecoh menekan FP
- `Shi_2026` — YOLO-LWD (GhostConv+ECA); manhole harus dianotasi terpisah
- `Li2024` — RDD-YOLO (v8+SimAM+GhostConv); arsitektur YOLOv8
- `Zeng2024` — YOLOv8-PD (ringan, D40 53,1%); Mosaic; Focal Loss
- `Wang2025` — YOLO-RD; modul SOM; mAP multi-skala
- `Wu2023` — YOLO-LWNet; metrik efisiensi (Params/GFLOPs/FPS)
- `mandal2020deep` — komparasi framework DL klasifikasi distres (F1 0,5814)
- `redmon2016you` / `redmon2017yolo9000` / `redmon2018yolov3` — YOLO v1/v2/v3
- `bochkovskiy2020yolov4` — YOLOv4 (Mosaic, atensi)
- `han2020ghostnet` — GhostConv/GhostNet
- `woo2018cbam` — CBAM
- `panboonyuen2025reg` — REG (Refined Generalized Focal Loss)
- `tian2026yolov12` / `sapkota2025yolo26` (juga `sapkota2025ultralytics`) — YOLOv12, YOLOv26
- `radopoulou2015detection`, `kusumah2023deep`, `hosseini2021prediction`, `suhartono2019estimated`, `arya2021deep` — pendukung latar belakang (kerusakan jalan, keselamatan, prediksi kondisi, transfer learning)

**Label silang LaTeX yang ada:** `tab:jadwal`, `tab:penelitian_terkait`, `fig:label_kerusakan_rdd`, `fig:yolov8_standar`, `fig:yolov8_modifikasi`, `fig:distribusi_negara`, `fig:contoh_kelas`, `fig:contoh_negara`, `fig:distribusi_kelas_global`, `fig:distribusi_objek_negara`, `fig:distribusi_luas_bbox`, `fig:alur_penelitian`, `fig:arsitektur_yolo`.
