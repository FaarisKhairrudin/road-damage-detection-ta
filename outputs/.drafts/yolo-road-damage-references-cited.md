# Referensi Tambahan untuk TA / Paper IEEE: Deteksi Kerusakan Jalan YOLO Ringan + Zero-Shot Indonesia (Cited Brief)

> Catatan verifikasi: setiap klaim faktual eksternal di bawah ini diberi sitasi inline `[N]` yang merujuk pada daftar Sources terverifikasi di akhir. URL yang gagal di-fetch langsung ditandai eksplisit (fetch-blocked / tidak terbaca) dan klaim yang hanya bersumber dari snippet ditandai UNVERIFIED. Angka-angka internal TA (hasil eksperimen sendiri, hitungan inventaris) dipertahankan sebagai konteks proyek dan diberi label `internal` — bukan klaim literatur. Klaim tanpa dukungan apa pun yang tidak bisa dilabeli telah dihapus (lihat `Removed Unsupported Claims`).

## Executive summary

- Pertanyaan: paper apa yang layak ditambahkan ke daftar pustaka (saat ini 13 entri di `latex/IEEE-Conference/references.bib` — hitungan internal, belum diaudit ulang di pass ini) untuk memperkuat TA evaluasi komparatif 5 YOLO nano pada N-RDD2024 subset Asia + uji zero-shot Bandung.
- Temuan: 4 riset paralel (models, domain, loss, efficiency) menghasilkan ~36 kandidat (hitungan kerja internal dari keempat file riset); setelah deduplikasi terhadap entri existing, **12 entri prioritas tambah** + **8 entri pelengkap opsional** + **5 merge/perbaikan key** direkomendasikan (rekomendasi penulis draf, dipertahankan sebagaimana adanya). Satu sitasi di glosarium proposal tidak boleh dipakai (YOLO-LWD / Shi 2026 — pencarian mengembalikan nol sumber cocok, temuan proses tanpa URL pendukung).
- Prioritas tertinggi: tutup kesenjangan bib IEEE (GhostNet [25], CBAM [26], REG [21], EfficientDet-Indonesia [32], lineage YOLOv3/v4 [34][35]) karena sudah disitasi di proposal tapi belum ada di `references.bib` (status bib internal TA).
- Status bukti tidak seragam: angka dari level snippet (YOLO-RD Neurocomputing [6], RDD-YOLO [40], VarifocalNet [20], Bandung 93,06% [15], Kaya Measurement [12]) tidak boleh dikutip sebagai fakta final sampai full-text dibaca — masing-masing ditandai di bawah.

## Findings

### 1. Apa yang sudah dimiliki (13 entri — jangan diduplikasi; daftar internal TA)

`redmon2016you`, `arya2021deep`, `Arya2024846` (RDD2022 journal), `kaya2024nrdd2024` (N-RDD2024 Mendeley v3), `Zeng2024` (YOLOv8-PD [38]), `Li2024` (RDD-YOLO [40]), `Wang2025` (YOLO-RD Sensors — versi Wei Wang et al., bukan Neurocomputing [6]), `Wu2023` (YOLO-LWNet [39]), `matouq2024ai`, `tian2026yolov12` (kemungkinan besar karya yang sama dengan [2], tahun perlu dinormalisasi), `sapkota2025yolo26` (karya yang sama dengan [3], penamaan perlu diklarifikasi), `cui2019class` (karya yang sama dengan [18]), `dai2017deformable` (karya yang sama dengan [28]).

Implikasi: kandidat C1 (Zeng [38]), C2 (Li [40]), C3 (Wu [39]), T2 C1 (RDD2022 [10] vs `Arya2024846` — perlu verifikasi key/tahun), T3 C2 (Cui [18]), T4 C2/C3/C5 (GhostNet [25] / CBAM [26] / DCNv1 [28]) adalah duplikat — perlakukan sebagai merge/perbaikan BibTeX, bukan entri baru.

### 2. Model YOLO ringan pembanding (menjawab Q1)

**ADD — Wu, Zhang & Fan (2025), RSDD tiny-damage, Scientific Reports 15:11032 [1].** YOLO-adjacent komparator 2025: halaman artikel terverifikasi live dan teks yang di-fetch mengonfirmasi studi mengakuisisi 10.440 citra jalan dengan 36.579 area kerusakan teranotasi, backbone berbasis modul DSCD + MFE + SPPF, serta fokus pada kerusakan tiny (retak selebar 1–2 piksel, pothole <20 piksel) [1]. Klaim angka mAP50 70,8% (self-set, 16,5M params, 30,9 GFLOPs, 4,5 ms) dan mAP50 61,2% pada subset RDD2022 berasal dari pembacaan full-text file riset dan belum dire-verifikasi pada potongan yang diambil di pass ini — perlakukan sebagai perlu-konfirmasi-satu-kali sebelum dikutip sebagai fakta [1]. Taksonomi 4 kelas (D00/D10/D20/D40) tumpang tindih dengan kelas inti TA. Cocok untuk Bab 2/4 sebagai pembanding tiny-damage 2025.

```bibtex
@article{wu2025rsdd,
  author  = {Wu, C. and Zhang, L. and Fan, X.},
  title   = {Object detection model design for tiny road surface damage},
  journal = {Scientific Reports},
  volume  = {15},
  pages   = {11032},
  year    = {2025},
  doi     = {10.1038/s41598-025-95502-z}
}
```
Caveat: nama depan penulis hanya inisial di file riset — verifikasi sebelum BibTeX final.

**MERGE — Tian et al. YOLOv12 (arXiv:2502.12524, 2025) [2].** Laporan resmi baseline YOLOv12n (attention-centric dengan Area Attention; abstrak arXiv yang terverifikasi melaporkan YOLOv12-N 40,6% mAP dengan latensi 1,64 ms pada GPU T4, mengungguli YOLOv10-N/YOLO11-N sebesar 2,1/1,2 poin mAP pada kecepatan sebanding) [2]. Identitas penulis (Yunjie Tian, Qixiang Ye, David Doermann), judul, dan tahun 2025 terkonfirmasi cocok pada indeks arXiv dan catatan OpenAlex [2]. Key existing `tian2026yolov12` hampir pasti karya yang sama dengan tahun salah — normalisasi ke 2025, jangan dihitung ganda. Klaim venue NeurIPS 2025 hanya sebagian terverifikasi (catatan OpenAlex mencatatnya sebagai conference-paper 2025) — konfirmasi halaman venue sebelum dikutip [2].

```bibtex
@article{tian2025yolov12,
  author  = {Tian, Yunjie and Ye, Qixiang and Doermann, David},
  title   = {{YOLOv12}: Attention-Centric Real-Time Object Detectors},
  journal = {arXiv preprint arXiv:2502.12524},
  year    = {2025}
}
```

**MERGE — Sapkota & Karkee YOLO26 (arXiv:2510.09653) + Ultralytics docs [3][4].** Dokumentasi resep DFL-free / NMS-free / MuSGD / Progressive Loss / STAL yang membedakan model ke-5 TA; spesifikasi resmi YOLO26n yang terverifikasi langsung dari docs: 40,9 mAP (40,1 NMS-free), 1,7 ms T4 TensorRT, 2,4M params, 5,5B FLOPs, rentang family 40,9–57,5 mAP pada 1,7–11,8 ms, dan hingga 43% lebih cepat pada CPU ONNX vs YOLO11n [4]. Key existing `sapkota2025yolo26` sama — gabungkan, klarifikasi penamaan YOLO26 vs YOLOv26. FLAG: record arXiv yang sama kini berversi v4 (diperbarui Sep 2026) dengan judul diperluas mencakup YOLO27 ("...YOLO27, YOLO26, YOLO11, YOLOv8, and YOLOv5...") oleh penulis yang sama [3] — sitasi arXiv harus mencantumkan versi yang dibaca.

**OPTIONAL — Zhao et al. RT-DETR (arXiv:2304.08069, 2023) [5].** Komparator non-YOLO (transformer, NMS-free end-to-end dengan hybrid encoder dan uncertainty-minimal query selection; RT-DETR-R50/R101 dilaporkan 53,1%/54,3% AP COCO pada 108/74 FPS T4) [5]. Daftar penulis kini terverifikasi dari indeks arXiv: Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei, Guanzhong Wang, Qingqing Dang, Yi Liu, Jie Chen [5] — BibTeX provisional pada draf kini dapat dilengkapi. Isi paper belum dibaca penuh — verifikasi sebelum mengutip angka performa [5].

**CAUTION — Wang et al. YOLO-RD Neurocomputing 2025 (DOI 10.1016/j.neucom.2025.132000) [6].** Ini karya BERBEDA dari `Wang2025` milik TA (Sensors 25(5), Wei Wang et al.) (pembedaan internal TA). Halaman ScienceDirect fetch-blocked (HTTP 403) di pass ini — klaim snippet (−39,8% params, evaluasi RM-RDD+RDD2022+N-RDD2024, deployment edge NT98525) semuanya UNVERIFIED [6]. Jangan merge dengan key existing; hanya jadikan komparator cadangan setelah full-text dibaca.

**DO NOT CITE — YOLO-LWD / Shi 2026.** Pencarian paper-DB + web mengembalikan nol sumber cocok (temuan proses dari file riset T1, tanpa URL pendukung). Inferensi: nama salah atau karya tidak ada. Jangan jadikan referensi sampai nama yang benar ditemukan (kandidat yang mungkin tertukar: LL-YOLO, LTF-YOLO, RDL-YOLO — belum diverifikasi, tanpa sumber).

### 3. Dataset, benchmark, domain gap (menjawab Q2–Q3)

**ADD — Arya et al. CRDDC'2022 challenge report (arXiv:2211.11362) [7].** Benchmark resmi yang terverifikasi: 47.420 citra jalan dari 6 negara (India, Jepang, Ceko, Norwegia, AS, China), 60+ tim dari 19 negara, evaluasi lima leaderboard; model terbaik (ensemble YOLO + Faster-RCNN) mencapai F1 76% pada data uji gabungan enam negara [7]. Angka journal 76,9% dan disparitas antar-negara 16,2% (India) hingga 21,2% (Norwegia) hanya level snippet (halaman journal tidak di-fetch di pass ini) — UNVERIFIED sampai dibaca [43]. Berbeda dari paper dataset RDD2022 [10] — keduanya perlu disitasi.

```bibtex
@misc{arya2022crddc2022,
  author = {Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Omata, Hiroshi and Kashiyama, Takehiro and Sekimoto, Yoshihide},
  title = {Crowdsensing-based Road Damage Detection Challenge ({CRDDC}'2022)},
  year = {2022},
  eprint = {2211.11362},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV},
  doi = {10.48550/arXiv.2211.11362},
  url = {https://arxiv.org/abs/2211.11362}
}
```

**ADD — Arya et al. GRDDC'2020 (arXiv:2011.08740) [8].** Baseline historis yang terverifikasi: 26.336 citra dari India, Jepang, Ceko; 121 tim terdaftar; set uji test1 (2.631) / test2 (2.664); model terbaik (ensemble berbasis YOLO) F1 0,67 (test1) / 0,66 (test2) [8] — menjangkar progres 0,67 (2020) → 0,76 (2022) [7][8].

```bibtex
@misc{arya2020grddc,
  author = {Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Omata, Hiroshi and Kashiyama, Takehiro and Sekimoto, Yoshihide},
  title = {Global Road Damage Detection: State-of-the-art Solutions},
  year = {2020},
  eprint = {2011.08740},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV},
  doi = {10.48550/arXiv.2011.08740},
  url = {https://arxiv.org/abs/2011.08740}
}
```

**ADD — Maeda et al. (2018), CACIE 33(12):1127–1141 [9].** Studi fondasi crowdsensing smartphone (9.053 citra / 15.435 instance, 7 kota Jepang, 8 kelas, deteksi on-server vs on-phone — angka dari file riset, level abstrak) — metodologi yang direplikasi protokol akuisisi Bandung TA (klaim replikasi internal TA). Halaman Wiley fetch-blocked (HTTP 403); preprint arXiv terverifikasi live dengan judul yang cocok [9]. Sitasi memakai DOI journal; gunakan preprint sebagai akses baca.

```bibtex
@article{maeda2018road,
  author = {Maeda, Hiroya and Sekimoto, Yoshihide and Seto, Toshikazu and Kashiyama, Takehiro and Omata, Hiroshi},
  title = {Road Damage Detection and Classification Using Deep Neural Networks with Smartphone Images},
  journal = {Computer-Aided Civil and Infrastructure Engineering},
  volume = {33},
  number = {12},
  pages = {1127--1141},
  year = {2018},
  doi = {10.1111/mice.12387}
}
```

**ADD — Lin et al. DA-RDD (IEEE T-ITS 24(3), 2023) [14].** Satu-satunya framework unsupervised domain adaptation spesifik kerusakan jalan yang ditemukan (file riset): alignment adversarial level-citra + level-instance (importance weighting + RoI multi-scale context), plus RDD2021 100k citra sintetis dari RDD2020. Halaman IEEE Xplore tidak terbaca via fetch di pass ini dan DOI 10.1109/TITS.2022.3226018 TIDAK terverifikasi — seluruh detail UNVERIFIED sampai full-text dibaca [14]. Peran di TA: teori Bab 2 + future work Bab 5 atas drop zero-shot (besaran drop internal TA). Baca full-text sebelum mengutip angka apa pun [14].

```bibtex
@article{lin2023dardd,
  author = {Lin, Chunmian and Tian, Daxin and Duan, Xuting and Zhou, Jianshan and Zhao, Dezong and Cao, Dongpu},
  title = {{DA-RDD}: Toward Domain Adaptive Road Damage Detection Across Different Countries},
  journal = {IEEE Transactions on Intelligent Transportation Systems},
  volume = {24},
  number = {3},
  year = {2023},
  url = {https://ieeexplore.ieee.org/document/9954613}
}
```

**ADD — Munawir et al. (2025), Bandung YOLOv8+CNN, JAILCD [15].** Satu-satunya studi Bandung yang ditemukan: halaman journal terverifikasi live; klaim file riset (hybrid YOLOv8 proposal + CNN klasifikasi pada citra resolusi tinggi Bandung, akurasi rata-rata 93,06%) level abstrak — protokol tak dibaca [15]. Caveat besar: metrik akurasi (bukan mAP/F1) dan protokol tak dibaca — tidak dapat dibandingkan langsung dengan angka zero-shot internal TA; justru kontras supervised-lokal vs zero-shot-asing adalah bukti domain gap (interpretasi penulis, bukan klaim sumber) [15].

```bibtex
@article{munawir2025bandung,
  author = {Munawir, Munawir and Pararta, Muhammad Salam and Suteddy, Wirmanto and Putra, Muhammad Taufik Dwi and Koerniawan, Mochamad Donny and Dewancker, Bart Julien},
  title = {Enhancing Road Maintenance Strategies in {Bandung} City Through {YOLO} and {CNN}-Based Damage Detection},
  journal = {Journal of Asian Institute of Low Carbon Design},
  year = {2025},
  doi = {10.69368/jailcd.20250009}
}
```

**CLARIFY — Kaya & Codur N-RDD2024 [11][12].** Key existing `kaya2024nrdd2024` menunjuk Mendeley v3; halaman dataset kini v5 (DOI 10.17632/27c8pwsd6v.5, CC BY 4.0, 10 kelas D00–D90 — halaman terverifikasi live, detail kelas dari file riset level record) — update versi, bukan entri baru [11]. Paper pendamping Measurement 2024 (YOLOv5 global 8 negara, DOI 10.1016/j.measurement.2024.116453) adalah sitasi BERBEDA yang layak ditambahkan sebagai baseline 10-kelas; halaman ScienceDirect gagal di-fetch (HTTP 400) — metrik belum terverifikasi, jangan kutip angka sebelum dibaca [12]. Keduanya perlu disitasi distinctly.

**CHECK — Arya et al. transfer-learning preprint (arXiv:2008.13101) [13].** Preseden transfer Jepang→negara-lain + rekomendasi deployment bagi dinas (halaman arXiv terverifikasi live; detail 26.620 citra dari file riset level abstrak) — kemungkinan besar versi preprint dari `arya2021deep` (Automation in Construction) yang sudah dimiliki (dugaan internal). Verifikasi sebelum menambah; bila sama, simpan versi journal saja.

**BACKUP — Pham et al. YOLOv7 CRDDC'2022 3rd place (arXiv:2211.00091) [16]; Rachman et al. YOLOv7 CWD-NMS Indonesia (JOIN 2025) [42]; Arya RDD2020 Data in Brief 2021 (DOI 10.1016/j.dib.2021.107133) [41].** Halaman Pham terverifikasi live (detail F1 81,7% US-GSV / 74,1% overall, peringkat 3 dari 51 — level snippet, UNVERIFIED) [16]. Rachman [42] dan RDD2020 [41] tidak di-fetch di pass ini — URL dari file riset, UNVERIFIED. Cadangan bila butuh exemplar metode YOLOv7 atau sitasi Indonesia kedua.

### 4. Imbalance, loss, distractor, objek kecil (menjawab Q4)

**ADD — Lin et al. Focal Loss (ICCV 2017) [17].** Fondasi loss untuk foreground–background imbalance ekstrem pada detektor padat: merombak cross-entropy dengan faktor modulasi yang menurunkan bobot contoh mudah, plus varian α-balanced dan inisialisasi prior (detail γ=2/π=0,01/RetinaNet-101-FPN 39,1 COCO AP dari pembacaan HTML file riset, level primer) [17]. Venue/tahun/penulis terkonfirmasi cocok pada indeks arXiv dan OpenAlex (catatan OpenAlex: conference-paper 2017, DOI 10.1109/iccv.2017.324) [17]. Untuk subseksi imbalance/loss Bab 2 (rasio imbalance internal TA).

```bibtex
@inproceedings{lin2017focal,
  title = {Focal Loss for Dense Object Detection},
  author = {Lin, Tsung-Yi and Goyal, Priya and Girshick, Ross and He, Kaiming and Doll{\'a}r, Piotr},
  booktitle = {Proc. IEEE Int. Conf. Comput. Vis. (ICCV)},
  pages = {2980--2988},
  year = {2017},
  doi = {10.1109/ICCV.2017.324}
}
```

**ADD — Li et al. Generalized Focal Loss (NeurIPS 2020) [19].** Jembatan focal → quality-aware: menggabungkan estimasi kualitas lokalisasi ke dalam vektor prediksi kelas dan memodelkan lokasi box sebagai distribusi diskrit umum; GFL menggeneralisasi Focal Loss ke label kontinu; abstrak terverifikasi melaporkan 45,0% COCO AP (ResNet-101, melampaui SAPD 43,5% dan ATSS 43,6%) dan model terbaik 48,2% single-scale pada 10 FPS (2080Ti) [19]. Untuk subseksi perbandingan loss (GFL/VFL/REG) pada batas pothole/patch ambigu (framing penulis).

```bibtex
@inproceedings{li2020generalized,
  title = {Generalized Focal Loss: Learning Qualified and Distributed Bounding Boxes for Dense Object Detection},
  author = {Li, Xiang and Wang, Wenhai and Wu, Lijun and Chen, Shuo and Hu, Xiaolin and Li, Jun and Tang, Jin-Hui and Yang, Jian},
  booktitle = {Adv. Neural Inf. Process. Syst. (NeurIPS)},
  volume = {33},
  pages = {21002--21012},
  year = {2020},
  eprint = {2006.04388},
  archiveprefix = {arXiv}
}
```

**ADD — Zhang et al. VarifocalNet (CVPR 2021 oral) [20].** Alternatif IoU-aware ranking (IACS + Varifocal Loss + representasi box star-shaped di atas FCOS+ATSS; abstrak terverifikasi melaporkan konsisten ~2,0 AP di atas baseline kuat dan model terbaik 55,1 AP COCO test-dev) [20]. Untuk diskusi ablasi loss/head. Status: level abstrak — baca full-text sebelum mengutip angka [20].

```bibtex
@inproceedings{zhang2021varifocalnet,
  title = {VarifocalNet: An IoU-aware Dense Object Detector},
  author = {Zhang, Haoyang and Wang, Ying and Dayoub, Feras and S{\"u}nderhauf, Niko},
  booktitle = {Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)},
  pages = {8516--8525},
  year = {2021},
  doi = {10.1109/CVPR46437.2021.00841}
}
```

**ADD (proposal→bib) — Panboonyuen REG (KST 2025) [21].** Satu-satunya refinement focal spesifik domain jalan yang ditemukan; angka mAP50 80,34 / F1 77,87 kini terkonfirmasi tercantum pada abstrak preprint arXiv (14 halaman) yang merumuskan REG dengan spatial-contextual adjustment dan probabilistic refinement untuk aset jalan Thailand [21]. Repo GitHub terverifikasi live [21]; halaman IEEE (doc 11003314) tidak terbaca via fetch — detail venue KST (pp. 324–329) UNVERIFIED sampai teks dibaca [21]. Tambahkan sebagai metode; perlakukan angka sebagai preprint-level sampai teks KST/IEEE dibaca [21].

```bibtex
@inproceedings{panboonyuen2025reg,
  title = {{REG: Refined Generalized Focal Loss for Road Asset Detection on Thai Highways Using Vision Models}},
  author = {Panboonyuen, Teerapong},
  booktitle = {Proc. 17th Int. Conf. Knowl. Smart Technol. (KST)},
  pages = {324--329},
  year = {2025},
  organization = {IEEE}
}
```

**ADD — Bučko et al. (Sensors 2022, 22:8878) [22].** Satu-satunya preseden eksplisit manhole-sebagai-distractor (file riset, level snippet/abstrak): kelas manhole ditambahkan karena bentuk bulat meniru pothole; manhole empiris lebih mudah daripada pothole — pola yang sama dengan angka internal TA (bandingan internal, bukan klaim sumber). Cermin PMC terverifikasi live dan dapat dibaca penuh (79.712 chars) [22]; link DOI/MDPI fetch-blocked (HTTP 403, kemungkinan bot-block — bukan bukti mati) [22]. Baca full-text PMC sebelum mengutip detail [22].

```bibtex
@article{bucko2022computer,
  title = {{Computer Vision Based Pothole Detection under Challenging Conditions}},
  author = {Bu{\v{c}}ko, Boris and Lieskovsk{\'a}, Eva and Z{\'a}bovsk{\'a}, Katar{\'\i}na and Z{\'a}bovsk{\'y}, Michal},
  journal = {Sensors},
  volume = {22},
  number = {22},
  pages = {8878},
  year = {2022},
  doi = {10.3390/s22228878}
}
```

**ADD — Lin et al. COCO (ECCV 2014) [23].** Jangkar metrik normatif untuk evaluasi multi-skala mAP-S/M/L mengingat rezim objek kecil internal TA; abstrak terverifikasi: 2,5 juta instance terlabel pada 328 ribu citra, 91 tipe objek [23]. FLAG: daftar penulis arXiv (Lin, Maire, Belongie, Bourdev, Girshick, Hays, Perona, Ramanan, ...) berbeda dari versi prosiding ECCV pada draf (mencantumkan Ramanan, Dollár, Zitnick) — gunakan daftar penulis venue kanonis saat BibTeX final [23]. Threshold piksel S/M/L perlu verifikasi ulang ke protokol evaluasi resmi saat penulisan (TODO).

```bibtex
@inproceedings{lin2014microsoft,
  title = {{Microsoft COCO: Common Objects in Context}},
  author = {Lin, Tsung-Yi and Maire, Michael and Belongie, Serge and Hays, James and Perona, Pietro and Ramanan, Deva and Doll{\'a}r, Piotr and Zitnick, C. Lawrence},
  booktitle = {Proc. Eur. Conf. Comput. Vis. (ECCV)},
  pages = {740--755},
  year = {2014},
  doi = {10.1007/978-3-319-10602-1_48}
}
```

### 5. Atensi, konvolusi ringan, efisiensi real-time (menjawab Q5)

**ADD (proposal→bib) — Yang et al. SimAM (ICML 2021, PMLR 139:11863–11874) [24].** Baseline atensi nol-parameter (bobot 3-D per feature map dari solusi closed-form fungsi energi, <10 baris kode — halaman PMLR terverifikasi live dengan halaman dan PDF yang cocok) [24] — pembanding CBAM berparameter dalam ablasi atensi neck (framing internal TA).

```bibtex
@inproceedings{yang2021simam,
  author = {Yang, Lingxiao and Zhang, Ru-Yuan and Li, Lida and Xie, Xiaohua},
  title = {SimAM: A Simple, Parameter-Free Attention Module for Convolutional Neural Networks},
  booktitle = {Proceedings of the 38th International Conference on Machine Learning},
  series = {Proceedings of Machine Learning Research},
  volume = {139},
  pages = {11863--11874},
  year = {2021},
  url = {https://proceedings.mlr.press/v139/yang21o.html}
}
```

**COMPLETE (proposal→bib) — Han et al. GhostNet (CVPR 2020) [25].** Sitasi first-principles GhostConv: modul Ghost menghasilkan ghost feature maps dari transformasi linear murah atas intrinsic maps dan bersifat plug-and-play; abstrak terverifikasi melaporkan GhostNet 75,7% top-1 ImageNet dengan biaya komputasi setara MobileNetV3 [25]. Untuk cabang efisiensi YOLOv8-PD (angka Params/GFLOPs/FPS internal TA — TODO verifikasi, bukan klaim sumber) [25].

```bibtex
@inproceedings{han2020ghostnet,
  author = {Han, Kai and Wang, Yunhe and Tian, Qi and Guo, Jianyuan and Xu, Chunjing and Xu, Chang},
  title = {GhostNet: More Features From Cheap Operations},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages = {1577--1586},
  year = {2020},
  doi = {10.1109/CVPR42600.2020.00165}
}
```

**COMPLETE (proposal→bib) — Woo et al. CBAM (ECCV 2018) [26].** Counterpart atensi berparameter (channel+spatial sekuensial, overhead negligible, end-to-end trainable; validasi pada ImageNet-1K, MS-COCO, VOC 2007 — abstrak terverifikasi) [26]. Pasangkan dengan SimAM saat melaporkan delta Params/GFLOPs/FPS (protokol internal TA) [24][26].

```bibtex
@inproceedings{woo2018cbam,
  author = {Woo, Sanghyun and Park, Jongchan and Lee, Joon-Young and Kweon, In So},
  title = {{CBAM}: Convolutional Block Attention Module},
  booktitle = {Proceedings of the European Conference on Computer Vision (ECCV)},
  pages = {3--19},
  year = {2018},
  doi = {10.1007/978-3-030-01234-2_1}
}
```

**ADD — Wang et al. ECA-Net (CVPR 2020) [27].** Preseden efisiensi atensi (interaksi cross-channel lokal via conv 1-D tanpa reduksi dimensi, kernel adaptif; abstrak terverifikasi: modul hanya ~80 params dan ~4,7e-4 GFLOPs terhadap backbone ResNet-50 24,37M/3,86 GFLOPs dengan gain Top-1 >2%) [27] — layak disebut satu baris sebagai kandidat ablasi masa depan walau TA hanya memakai SimAM/CBAM (framing internal TA) [27].

```bibtex
@inproceedings{wang2020eca,
  author = {Wang, Qilong and Wu, Banggu and Zhu, Pengfei and Li, Peihua and Zuo, Wangmeng and Hu, Qinghua},
  title = {{ECA-Net}: Efficient Channel Attention for Deep Convolutional Neural Networks},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages = {11531--11539},
  year = {2020},
  doi = {10.1109/CVPR42600.2020.01155}
}
```

**ADD — Zhu et al. DCNv2 (CVPR 2019) [29].** Pelengkap deformable-conv (modulasi offset+amplitudo, integrasi conv3–conv5, feature mimicking; modul digambarkan tetap ringan dan drop-in — abstrak terverifikasi; angka AP eksak hanya snippet — UNVERIFIED) [29] — pasangkan dengan `dai2017deformable` (DCNv1, arXiv terverifikasi: modul deformable conv + deformable RoI pooling dengan offset 2-D yang dipelajari tugas, drop-in end-to-end) yang sudah ada [28][29].

```bibtex
@inproceedings{zhu2019dcnv2,
  author = {Zhu, Xizhou and Hu, Han and Lin, Stephen and Dai, Jifeng},
  title = {Deformable {ConvNets} v2: More Deformable, Better Results},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2019},
  eprint = {1811.11168},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/1811.11168}
}
```

**ADD — Finder et al. WTConv (ECCV 2024) [30].** Sitasi kanonis modul wavelet-refinement YOLO-RD (halaman arXiv terverifikasi live; klaim log-param scaling, Haar WT, drop-in depth-wise conv dari file riset level abstrak/HTML — UNVERIFIED sampai dibaca) [30] — argumen "receptive field besar untuk retak tipis dengan biaya rendah" (framing penulis).

**ADD — Tan et al. EfficientDet (CVPR 2020) [31].** Referensi keluarga detector efisien (BiFPN + compound scaling; abstrak terverifikasi: D7 55,1 AP COCO test-dev, 77M params, 410B FLOPs, 4–9× lebih kecil dan 13–42× lebih sedikit FLOPs dari detektor prior; jadwal training SGD momentum 0,9, warmup LR 0,16, cosine decay, 300 epoch) [31] sebagai konteks klaim efisiensi YOLOv8-PD (angka internal TA — TODO verifikasi) [31].

```bibtex
@inproceedings{tan2020efficientdet,
  author = {Tan, Mingxing and Pang, Ruoming and Le, Quoc V.},
  title = {{EfficientDet}: Scalable and Efficient Object Detection},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages = {10781--10790},
  year = {2020},
  eprint = {1911.09070},
  archiveprefix = {arXiv}
}
```

**ADD (proposal→bib) — Hugo et al. (2025) EfficientDet-D0 Indonesia [32].** Instansiasi Indonesia (klaim file riset dari skim PDF langsung: EfficientDet-D0 pretrained pada citra jalan Indonesia, F1 validasi 59,7%, mengalahkan prior work) — sitasi relevansi geografis, bukan angka SOTA [32]. Caveat: fetch PDF di pass ini hanya mengembalikan konten minimal (175 chars) dan kredibilitas outlet JMLDL belum dicek — angka 59,7% UNVERIFIED sampai PDF dibaca ulang dan indeksasi dicek [32].

```bibtex
@article{hugo2025efficientdet,
  author = {Hugo, Bernard and Zakiyyah, Alfi Yusrotis and Minor, Kelvin Asclepius},
  title = {EfficientDet Model for Accurate Detection and Classification of Road Damages in Indonesia},
  journal = {Journal of Machine Learning and Deep Learning (JMLDL)},
  volume = {2},
  number = {1},
  year = {2025},
  doi = {10.64820/AEPJMLDL.21.11.17.62025}
}
```

**COMPLETE (proposal→bib) — Lineage YOLO + metodologi benchmark [33][34][35][36][37].** Redmon v1 (2016 — halaman arXiv terverifikasi; gabungkan/rename key `redmon2017` yang salah tahun) [33], Redmon & Farhadi YOLOv3 (arXiv:1804.02767 — halaman terverifikasi) [34], Bochkovskiy YOLOv4 (arXiv:2004.10934 — halaman terverifikasi; angka 43,5% AP @ ~65 FPS hanya snippet — UNVERIFIED) [35], Ge YOLOX anchor-free decoupled head + SimOTA (arXiv:2107.08430 — halaman terverifikasi) [36], panduan metrik Ultralytics (P/R/mAP50/mAP50-95 + rincian speed — halaman docs terverifikasi live; cerminan protokol GPU/bs/imgsz internal TA) [37].

## Evidence-backed caveats and disagreements

- Tingkat bukti tidak seragam: hanya YOLOv8-PD [38], RSDD 2025 [1], Focal Loss [17], GFL [19], docs YOLO26 [4], halaman arXiv/Mendeley/PMLR/PMC yang berhasil di-fetch yang terbaca langsung; sisanya abstrak/metadata/snippet. Angka dari level snippet (YOLO-RD Neurocomputing [6], RDD-YOLO [40], VarifocalNet [20], REG pra-verifikasi-arXiv [21], Bandung 93,06% [15], Kaya Measurement [12]) tidak boleh dikutip sebagai fakta sampai full-text dibaca.
- Duplikasi silang file riset: T1 mengklaim Arya RDD2022 sebagai NEW, T2 benar menandainya duplikat `Arya2024846` — versi T2 yang dipakai di laporan ini (keputusan penulis draf; verifikasi key tetap TODO).
- Ketidaksepakatan tahun/key: `tian2026yolov12` (existing) vs arXiv 2025 [2]; `kaya2024nrdd2024` v3 vs dataset v5 [11]; `arya2021deep` vs preprint transfer-learning [13]; `redmon2017` vs venue kanonis 2016 [33]. Semua dinormalisasi di rekomendasi merge di atas.
- Latar belakang non-teknis proposal (`kusumah2023deep`, `hosseini2021prediction`, `mandal2020deep`, `suhartono2019estimated`, `radopoulou2015detection`) berada di luar cakupan 4 brief dan tidak diverifikasi di sini — pertahankan key proposal untuk skripsi, jangan harapkan dari laporan ini (tanpa sumber pendukung).
- Klaim sitasi-ke venue kecil dan hitungan sitasi OpenAlex pada draf awal tidak didukung file riset — dihapus (lihat Removed Unsupported Claims).

## Open questions

1. Nama benar "YOLO-LWD / Shi 2026"? Nol hasil — butuh pencarian author/judul khusus sebelum disitasi.
2. Identitas `kaya2024nrdd2024`: dataset v3 [11] vs paper Measurement [12] — TA perlu mengutip keduanya secara distinct; konfirmasi key mana yang menunjuk ke mana.
3. Full-text yang masih perlu dibaca sebelum mengutip angka: YOLO-RD (kedua versi) [6], RDD-YOLO [40], REG teks KST/IEEE [21], DA-RDD [14], Kaya Measurement [12], Bandung [15], Bučko (baca via PMC [22]), COCO thresholds [23].
4. Sitasi teori generalisasi domain kedua (di luar DA-RDD [14]) bila Bab 2 butuh lebih dari satu — kandidat WACV'26 prompting / CNRDD hanya muncul sebagai snippet, belum terverifikasi (tanpa sumber).
5. DCNv3 / InternImage kanonis belum diamankan — butuh pencarian exact-title khusus (tanpa sumber, tidak disitasi).
6. Nama depan Wu/Zhang/Fan 2025 [1] dan detail VarifocalNet/GFL [19][20] perlu verifikasi dari halaman artikel sebelum BibTeX final.

## Removed Unsupported Claims

- Dihapus: "570+ sitasi GhostNet/CBAM/ECA adalah metadata OpenAlex" — tidak ada bukti OpenAlex semacam itu di file riset.
- Dihapus: perbandingan outlet kecil "visibilitas rendah" sebagai fakta — dipertahankan hanya sebagai caveat yang diberi label (outlet credibility belum dicek) [32].
- Dilunakkan menjadi TODO: angka efisiensi internal TA (2,46M/7,7 GFLOPs/368 FPS; 7,09M/12,9 GFLOPs/189 FPS; Indo-v3 0,309; 0,23–0,31; 9,67x; 1,69%; protokol RTX 4070 SUPER) — data eksperimen TA sendiri, bukan klaim literatur; tidak diberi sitasi palsu.
- Dilunakkan menjadi UNVERIFIED: 76,9% / 16,2–21,2% (journal CRDDC, halaman tidak di-fetch) [43]; −39,8% params YOLO-RD [6]; 81,7%/74,1% Pham [16]; 59,7% Hugo [32]; 43,5%@65FPS YOLOv4 [35].

## Sources

[1] Wu, Zhang & Fan (2025), Object detection model design for tiny road surface damage, Sci. Rep. 15:11032 — https://doi.org/10.1038/s41598-025-95502-z — LIVE (full text fetched; dataset size, DSCD/MFE/SPPF modules, tiny-damage focus confirmed; headline mAP/latency figures per research-file read, re-confirm before citing as fact).
[2] Tian, Ye & Doermann (2025), YOLOv12: Attention-Centric Real-Time Object Detectors, arXiv:2502.12524 — https://arxiv.org/abs/2502.12524 — LIVE (arXiv index + OpenAlex record matched: title, year 2025, first author Yunjie Tian; abstract confirms 40.6% mAP @ 1.64 ms T4; NeurIPS-2025 venue only partially verified).
[3] Sapkota & Karkee (2025), Ultralytics YOLO Evolution (YOLO26...), arXiv:2510.09653 — https://arxiv.org/abs/2510.09653 — LIVE with FLAG (same ID now v4, Sep 2026, retitled to include YOLO27, same authors; cite the version read).
[4] Ultralytics YOLO26 documentation — https://docs.ultralytics.com/models/yolo26/ — LIVE (YOLO26n 40.9/40.1 mAP, 1.7 ms T4, 2.4M params, 5.5B FLOPs; DFL-free, NMS-free option, MuSGD, Progressive Loss, STAL confirmed).
[5] Zhao et al. (2023), DETRs Beat YOLOs on Real-time Object Detection, arXiv:2304.08069 — https://arxiv.org/abs/2304.08069 — LIVE (arXiv index matched: title, 2023, first author Yian Zhao; full 8-author list verified; content not fully read).
[6] Wang et al. (2025), YOLO-RD, Neurocomputing, DOI 10.1016/j.neucom.2025.132000 — https://www.sciencedirect.com/science/article/pii/S0925231225026724 — FETCH-BLOCKED (HTTP 403; all performance/deployment claims UNVERIFIED).
[7] Arya et al. (2022), Crowdsensing-based Road Damage Detection Challenge (CRDDC-2022), arXiv:2211.11362 — https://arxiv.org/abs/2211.11362 — LIVE (arXiv index matched: 47,420 images, 6 countries, 60+ teams/19 countries, five leaderboards, YOLO+Faster-RCNN ensemble F1 76%).
[8] Arya et al. (2020), Global Road Damage Detection: State-of-the-art Solutions, arXiv:2011.08740 — https://arxiv.org/abs/2011.08740 — LIVE (arXiv index matched: 26,336 images, 3 countries, 121 teams, test1/test2 2,631/2,664, YOLO-ensemble F1 0.67/0.66).
[9] Maeda et al. (2018), Road Damage Detection and Classification Using Deep Neural Networks with Smartphone Images — preprint https://arxiv.org/abs/1801.09454 — LIVE (title matched; counts 9,053/15,435 abstract-level per research file). Journal DOI 10.1111/mice.12387 (Wiley page fetch-blocked HTTP 403, not dead).
[10] Arya et al. (2022), RDD2022: A multi-national image dataset for automatic Road Damage Detection, arXiv:2209.08538 — https://arxiv.org/abs/2209.08538 — LIVE (arXiv index matched: 47,420 images, 55,000+ instances, 6 countries, 4 damage classes).
[11] Kaya & Çodur (2024), N-RDD2024: Road damage and defects, Mendeley Data v5, DOI 10.17632/27c8pwsd6v.5 — https://data.mendeley.com/datasets/27c8pwsd6v/5 — LIVE (record page fetched; 10-class D00–D90 taxonomy per research-file read).
[12] Kaya & Çodur (2024), Automatic detection and classification of road defects on a global-scale: Embedded system, Measurement, DOI 10.1016/j.measurement.2024.116453 — https://www.sciencedirect.com/science/article/abs/pii/S0263224124023388 — FETCH FAILED (HTTP 400; metrics UNVERIFIED).
[13] Arya et al. (2020), Transfer Learning-based Road Damage Detection for Multiple Countries, arXiv:2008.13101 — https://arxiv.org/abs/2008.13101 — LIVE (page fetched; transfer/detail claims abstract-level per research file).
[14] Lin et al. (2023), DA-RDD: Toward Domain Adaptive Road Damage Detection Across Different Countries, IEEE T-ITS 24(3) — https://ieeexplore.ieee.org/document/9954613 — UNREADABLE via fetch (metadata only; DOI 10.1109/TITS.2022.3226018 NOT verified; all method claims UNVERIFIED).
[15] Munawir et al. (2025), Enhancing Road Maintenance Strategies in Bandung City Through YOLO and CNN-Based Damage Detection, JAILCD, DOI 10.69368/jailcd.20250009 — https://journal.moi.work/index.php/AILCD/article/view/418 — LIVE (abstract page fetched; 93.06% accuracy claim abstract-level per research file, protocol unread).
[16] Pham et al. (2022), Road Damages Detection and Classification with YOLOv7, arXiv:2211.00091 — https://arxiv.org/abs/2211.00091 — LIVE (page fetched; F1/placement figures snippet-level, UNVERIFIED).
[17] Lin et al. (2017), Focal Loss for Dense Object Detection, arXiv:1708.02002 — https://arxiv.org/abs/1708.02002 — LIVE (arXiv index + OpenAlex record matched: title, 2017, first author Tsung-Yi Lin, DOI 10.1109/iccv.2017.324; γ=2/α-balance/prior-init/RetinaNet recipe per research-file HTML read).
[18] Cui et al. (2019), Class-Balanced Loss Based on Effective Number of Samples, arXiv:1901.05555 — https://arxiv.org/abs/1901.05555 — LIVE (arXiv index matched: title, 2019, first author Yin Cui; effective-number formula and loss-agnostic re-weighting per abstract).
[19] Li et al. (2020), Generalized Focal Loss, arXiv:2006.04388 — https://arxiv.org/abs/2006.04388 — LIVE (arXiv index matched: title, 2020, first author Xiang Li; abstract confirms QFL/DFL design, 45.0% AP R-101, 48.2% best single-scale).
[20] Zhang et al. (2021), VarifocalNet: An IoU-aware Dense Object Detector, arXiv:2008.13367 — https://arxiv.org/abs/2008.13367 — LIVE (arXiv index matched: title, authors, CVPR-2021-oral comment; abstract confirms IACS + Varifocal Loss, ~2.0 AP gain, 55.1 best AP; abstract-level).
[21] Panboonyuen (2024/2025), REG: Refined Generalized Focal Loss for Road Asset Detection on Thai Highways — arXiv https://arxiv.org/abs/2409.09877 (LIVE; index matched title/author; abstract confirms mAP50 80.34 / F1 77.87, spatial-contextual + probabilistic refinement) + code https://github.com/kaopanboonyuen/REG (LIVE) + IEEE https://ieeexplore.ieee.org/document/11003314/ (UNREADABLE via fetch; KST pp. 324–329 UNVERIFIED).
[22] Bučko et al. (2022), Computer Vision Based Pothole Detection under Challenging Conditions, Sensors 22:8878 — PMC mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC9694379 — LIVE (full text readable; manhole-as-distractor details per research-file snippet, re-confirm in PMC text). DOI/MDPI links fetch-blocked HTTP 403 (bot-block, not evidence of death).
[23] Lin et al. (2014), Microsoft COCO: Common Objects in Context, arXiv:1405.0312 — https://arxiv.org/abs/1405.0312 — LIVE with FLAG (arXiv index matched title/year; arXiv author list includes Bourdev/Girshick and omits Ramanan/Dollár/Zitnick vs ECCV proceedings version in draft BibTeX — use canonical venue author list for final BibTeX; abstract confirms 2.5M instances / 328k images / 91 types; S/M/L pixel thresholds TODO).
[24] Yang et al. (2021), SimAM, PMLR 139:11863–11874 — https://proceedings.mlr.press/v139/yang21o.html — LIVE (proceedings page fetched; parameter-free 3-D attention, energy-function closed form confirmed).
[25] Han et al. (2020), GhostNet: More Features from Cheap Operations, arXiv:1911.11907 — https://arxiv.org/abs/1911.11907 — LIVE (arXiv index matched: title, authors, CVPR-2020 comment; abstract confirms Ghost module/cheap linear transforms, 75.7% ImageNet top-1 at MobileNetV3-like cost).
[26] Woo et al. (2018), CBAM: Convolutional Block Attention Module, arXiv:1807.06521 — https://arxiv.org/abs/1807.06521 — LIVE (arXiv index matched: title, authors, ECCV-2018 comment; abstract confirms sequential channel+spatial attention, negligible overhead).
[27] Wang et al. (2020), ECA-Net, arXiv:1910.03151 — https://arxiv.org/abs/1910.03151 — LIVE (arXiv index matched: title, authors, CVPR-2020 comment; abstract confirms 1-D conv without dimensionality reduction, 80 params / 4.7e-4 GFLOPs vs ResNet-50, >2% Top-1 gain).
[28] Dai et al. (2017), Deformable Convolutional Networks, arXiv:1703.06211 — https://arxiv.org/abs/1703.06211 — LIVE (page fetched; deformable conv + deformable RoI pooling with learned offsets, drop-in end-to-end).
[29] Zhu et al. (2019), Deformable ConvNets v2, arXiv:1811.11168 — https://arxiv.org/abs/1811.11168 — LIVE (page fetched; modulation + wider deformable integration + feature mimicking; exact AP numbers UNVERIFIED).
[30] Finder et al. (2024), Wavelet Convolutions for Large Receptive Fields, arXiv:2407.05848 — https://arxiv.org/abs/2407.05848 — LIVE (page fetched; log-param scaling/Haar/drop-in claims abstract-level per research file, UNVERIFIED).
[31] Tan, Pang & Le (2020), EfficientDet, arXiv:1911.09070 — https://arxiv.org/abs/1911.09070 — LIVE (page fetched; abstract confirms BiFPN + compound scaling, D7 55.1 AP / 77M / 410B FLOPs, training schedule).
[32] Hugo, Zakiyyah & Minor (2025), EfficientDet Model for Accurate Detection and Classification of Road Damages in Indonesia, JMLDL 2(1) — PDF https://www.academicedgepress.co.uk/publicresources/documents/JMLDL.1.1/JMLDL.2.1/EfficientDet%20Model%20for%20Accurate%20Detection%20and%20Classification%20of%20Road%20Damages%20in%20Indonesia.pdf — PARTIALLY VERIFIED (fetch returned minimal content; 59.7% F1 figure per research-file PDF skim, UNVERIFIED; outlet indexing unchecked).
[33] Redmon et al. (2016), You Only Look Once: Unified, Real-Time Object Detection, arXiv:1506.02640 — https://arxiv.org/abs/1506.02640 — LIVE (page fetched; canonical 2016 venue — use to rename/merge `redmon2017`).
[34] Redmon & Farhadi (2018), YOLOv3: An Incremental Improvement, arXiv:1804.02767 — https://arxiv.org/abs/1804.02767 — LIVE (page fetched).
[35] Bochkovskiy, Wang & Liao (2020), YOLOv4: Optimal Speed and Accuracy of Object Detection, arXiv:2004.10934 — https://arxiv.org/abs/2004.10934 — LIVE (page fetched; 43.5% AP @ ~65 FPS figures snippet-level, UNVERIFIED).
[36] Ge et al. (2021), YOLOX: Exceeding YOLO Series in 2021, arXiv:2107.08430 — https://arxiv.org/abs/2107.08430 — LIVE (page fetched; anchor-free + decoupled head + SimOTA).
[37] Ultralytics, YOLO Performance Metrics guide — https://docs.ultralytics.com/guides/yolo-performance-metrics/ — LIVE (P/R/mAP50/mAP50-95 + speed-breakdown reporting convention confirmed).
[38] Zeng & Zhong (2024), YOLOv8-PD, Sci. Rep. 14:12052 — https://www.nature.com/articles/s41598-024-62933-z (LIVE, full text fetched; PMC mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC11130172) — duplicate of existing `Zeng2024`; keep as primary citation.
[39] Wu et al. (2023), YOLO-LWNet, Sensors 23:3268 — PMC mirror https://pmc.ncbi.nlm.nih.gov/articles/PMC10058657 — LIVE (full text readable; MDPI page https://www.mdpi.com/1424-8220/23/6/3268 fetch-blocked HTTP 403) — duplicate of existing `Wu2023`.
[40] Li et al. (2024), RDD-YOLO, Appl. Sci. 14:3360 — https://www.mdpi.com/2076-3417/14/8/3360 — FETCH-BLOCKED (HTTP 403; SimAM+GhostConv description and all numbers UNVERIFIED) — duplicate of existing `Li2024`.
[41] Arya et al. (2021), RDD2020, Data in Brief 36:107133, DOI 10.1016/j.dib.2021.107133 — https://doi.org/10.1016/j.dib.2021.107133 — NOT FETCHED in this pass (URL from research file; backup citation only, UNVERIFIED).
[42] Rachman et al. (2025), Road Damage Detection Using YOLOv7 with Cluster Weighted Distance-IoU NMS, JOIN — https://scholar.its.ac.id/en/publications/road-damage-detection-using-yolov7-with-cluster-weighted-distance — NOT FETCHED in this pass (URL from research file; backup citation only, UNVERIFIED).
[43] Arya et al. (2024), RDD2022 journal data article, Geosci. Data J. — https://rmets.onlinelibrary.wiley.com/doi/10.1002/gdj3.260 — NOT FETCHED in this pass (76.9% F1 and 16.2–21.2% per-country gaps UNVERIFIED; verify before citing figures).

## Source verification log (fetch + index cross-check)

- Live on direct fetch: [1][2][3][4][5][7][8][9-preprint][10][11][13][15][16][17][18][19][20][21-arXiv+repo][22-PMC][23][24][25][26][27][28][29][30][31][33][34][35][36][37][38][39-PMC].
- Fetch-blocked (HTTP 403, likely bot-block — not proof of death, no replacement invented): [6], [9-Wiley], [12 companion note: HTTP 400], [22-DOI/MDPI], [39-MDPI], [40].
- Unreadable/empty via fetch: [14] (IEEE Xplore structure), [21-IEEE], [32] (minimal content).
- Not fetched (from research files, flagged UNVERIFIED): [41][42][43].
- Index cross-checks (arXiv API + arXiv abs fetch; OpenAlex for [2] and [17]): all matched title/year/first-author except flags noted at [3] (v4 retitle to include YOLO27 — same ID/authors, record which version was read) and [23] (arXiv vs ECCV-proceedings author-list difference).
- No orphan citations; no orphan sources (each [N] is cited at least once above).
