# Referensi Tambahan untuk TA / Paper IEEE: Deteksi Kerusakan Jalan YOLO Ringan + Zero-Shot Indonesia

## Executive summary

- Pertanyaan: paper apa yang layak ditambahkan ke daftar pustaka (saat ini 13 entri di `latex/IEEE-Conference/references.bib`, 11 PDF di `latex/refference/`) untuk memperkuat TA evaluasi komparatif 5 YOLO nano pada N-RDD2024 subset Asia + uji zero-shot Bandung.
- Temuan: 4 riset paralel (models, domain, loss, efficiency) menghasilkan ~36 kandidat; setelah deduplikasi terhadap 13 entri existing, **12 entri prioritas tambah** + **8 entri pelengkap opsional** + **5 merge/perbaikan key** direkomendasikan. Satu sitasi di glosarium proposal tidak boleh dipakai (YOLO-LWD / Shi 2026 — tidak ditemukan).
- Prioritas tertinggi: tutup kesenjangan bib IEEE (GhostNet, CBAM, REG, EfficientDet-Indonesia, lineage YOLOv3/v4) karena sudah disitasi di proposal tapi belum ada di `references.bib`.
- Semua angka di bawah berasal dari file riset `outputs/.drafts/yolo-road-damage-references-research-*.md`; klaim tanpa sumber primer ditandai. Tidak ada sumber, angka, atau URL yang diinventarisasi di laporan ini.

## Findings

### 1. Apa yang sudah dimiliki (13 entri — jangan diduplikasi)

`redmon2016you`, `arya2021deep`, `Arya2024846` (RDD2022 journal), `kaya2024nrdd2024` (N-RDD2024 Mendeley v3), `Zeng2024` (YOLOv8-PD), `Li2024` (RDD-YOLO), `Wang2025` (YOLO-RD Sensors — versi Wei Wang et al., bukan Neurocomputing), `Wu2023` (YOLO-LWNet), `matouq2024ai`, `tian2026yolov12`, `sapkota2025yolo26`, `cui2019class`, `dai2017deformable`.

Implikasi: kandidat T1 C1 (Zeng), C2 (Li), C3 (Wu), C8 (Arya RDD2022 journal), T3 C2 (Cui), T4 C2/C3/C5 (GhostNet/CBAM/DCNv1) adalah duplikat — perlakukan sebagai merge/perbaikan BibTeX, bukan entri baru.

### 2. Model YOLO ringan pembanding (menjawab Q1)

**ADD — Wu, Zhang & Fan (2025), RSDD tiny-damage, Scientific Reports 15:11032.** YOLO-adjacent komparator 2025 terkuat: backbone DSCD+MFE+SPPF, neck FSM+FFM, multi-scale decoupled head; 10.440 citra / 36.579 instance (D00/D10/D20/D40) + subset RDD2022 10.000 citra; mAP50 70,8% (self-set, 16,5M params, 30,9 GFLOPs, 4,5 ms) dan mAP50 61,2% pada subset RDD2022 — taksonomi 4 kelas sama dengan kelas inti TA. Cocok untuk Bab 2/4 sebagai pembanding tiny-damage 2025. URL: https://doi.org/10.1038/s41598-025-95502-z. Caveat: nama depan penulis hanya inisial di file riset — verifikasi sebelum BibTeX final.

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

**MERGE — Tian et al. YOLOv12 (arXiv:2502.12524, 2025; NeurIPS 2025).** Laporan resmi baseline YOLOv12n (R-ELAN + area attention) di balik model zero-shot terbaik TA (Indo-v3 0,309). Key existing `tian2026yolov12` hampir pasti karya yang sama dengan tahun salah — normalisasi ke 2025, jangan dihitung ganda. URL: https://arxiv.org/abs/2502.12524.

```bibtex
@article{tian2025yolov12,
  author  = {Tian, Yunjie and Ye, Qixiang and Doermann, David},
  title   = {{YOLOv12}: Attention-Centric Real-Time Object Detectors},
  journal = {arXiv preprint arXiv:2502.12524},
  year    = {2025}
}
```

**MERGE — Sapkota & Karkee YOLO26 (arXiv:2510.09653 overview + arXiv:2509.25164 benchmarking) + Ultralytics docs.** Dokumentasi resep DFL-free / NMS-free / MuSGD / ProgLoss / STAL yang membedakan model ke-5 TA; spesifikasi resmi YOLO26n 40,9 mAP, 1,7 ms T4, 2,4M params, 5,5B FLOPs dibaca langsung dari docs. Key existing `sapkota2025yolo26` sama — gabungkan, klarifikasi penamaan YOLO26 vs YOLOv26. URL: https://arxiv.org/abs/2510.09653 dan https://docs.ultralytics.com/models/yolo26/.

**OPTIONAL — Zhao et al. RT-DETR (arXiv:2304.08069, 2023).** Komparator non-YOLO (transformer, NMS-free end-to-end) untuk memposisikan pilihan attention YOLOv12 dan NMS-free YOLO26. Status: eksistensi terverifikasi, isi belum dibaca, daftar penulis belum terverifikasi — verifikasi atau buang. URL: https://arxiv.org/abs/2304.08069.

**CAUTION — Wang et al. YOLO-RD Neurocomputing 2025 (DOI 10.1016/j.neucom.2025.132000).** Ini karya BERBEDA dari `Wang2025` milik TA (Sensors 25(5), Wei Wang et al.). Snippet mengklaim −39,8% params dan evaluasi RM-RDD+RDD2022+N-RDD2024 plus deployment edge NT98525 — semuanya UNVERIFIED (paywall/403). Jangan merge dengan key existing; hanya jadikan komparator cadangan setelah full-text dibaca. URL: https://www.sciencedirect.com/science/article/pii/S0925231225026724.

**DO NOT CITE — YOLO-LWD / Shi 2026.** Pencarian paper-DB + web mengembalikan nol sumber cocok. Inferensi: nama salah atau karya tidak ada. Jangan jadikan referensi sampai nama yang benar ditemukan (kandidat yang mungkin tertukar: LL-YOLO, LTF-YOLO, RDL-YOLO — belum diverifikasi).

### 3. Dataset, benchmark, domain gap (menjawab Q2–Q3)

**ADD — Arya et al. CRDDC'2022 challenge report (arXiv:2211.11362).** Benchmark resmi yang memberi angka kemenangan F1 ≈0,76 (ensemble YOLO+Faster-RCNN, 60+ tim/19 negara, 5 leaderboard) dan disparitas antar-negara 16,2% (India) hingga 21,2% (Norwegia) pada versi journal — landasan utama narasi "variansi sumber" TA (China ≫ Japan > India). Berbeda dari paper dataset RDD2022 — keduanya perlu disitasi. URL: https://arxiv.org/abs/2211.11362.

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

**ADD — Arya et al. GRDDC'2020 (arXiv:2011.08740).** Baseline historis: 26.336 citra / 3 negara, ensemble YOLO terbaik F1 0,67/0,66 — menjangkar progres 0,67 (2020) → 0,76–0,77 (2022) dengan gap lintas-negara tetap ada. URL: https://arxiv.org/abs/2011.08740.

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

**ADD — Maeda et al. (2018), CACIE 33(12):1127–1141.** Studi fondasi crowdsensing smartphone: 9.053 citra / 15.435 instance, 7 kota Jepang, 8 kelas, deteksi on-server vs on-phone — metodologi yang direplikasi protokol akuisisi Bandung TA. URL: https://onlinelibrary.wiley.com/doi/10.1111/mice.12387 (preprint https://arxiv.org/abs/1801.09454).

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

**ADD — Lin et al. DA-RDD (IEEE T-ITS 24(3), 2023).** Satu-satunya framework unsupervised domain adaptation spesifik kerusakan jalan yang ditemukan: alignment adversarial level-citra + level-instance (importance weighting + RoI multi-scale context), plus RDD2021 100k citra sintetis dari RDD2020. Peran di TA: teori Bab 2 + future work Bab 5 atas drop zero-shot >50%. Status: snippet abstrak IEEE saja — baca full-text sebelum mengutip angka. Caveat: DOI 10.1109/TITS.2022.3226018 di file riset TIDAK terverifikasi di halaman; yang terverifikasi adalah nomor artikel Xplore 9954613. URL: https://ieeexplore.ieee.org/document/9954613.

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

**ADD — Munawir et al. (2025), Bandung YOLOv8+CNN, JAILCD.** Satu-satunya studi Bandung yang ditemukan: hybrid YOLOv8 (proposal) + CNN (klasifikasi) pada citra resolusi tinggi Bandung, akurasi rata-rata 93,06% — membuktikan relevansi lokal. Caveat besar: metrik akurasi (bukan mAP/F1) dan protokol tak dibaca — tidak dapat dibandingkan langsung dengan mAP50 zero-shot 0,23–0,31 TA; justru kontras supervised-lokal vs zero-shot-asing adalah bukti domain gap. URL: https://journal.moi.work/index.php/AILCD/article/view/418.

```bibtex
@article{munawir2025bandung,
  author = {Munawir, Munawir and Pararta, Muhammad Salam and Suteddy, Wirmanto and Putra, Muhammad Taufik Dwi and Koerniawan, Mochamad Donny and Dewancker, Bart Julien},
  title = {Enhancing Road Maintenance Strategies in {Bandung} City Through {YOLO} and {CNN}-Based Damage Detection},
  journal = {Journal of Asian Institute of Low Carbon Design},
  year = {2025},
  doi = {10.69368/jailcd.20250009}
}
```

**CLARIFY — Kaya & Codur N-RDD2024.** Key existing `kaya2024nrdd2024` menunjuk Mendeley v3 (DOI ...27c8pwsd6v.3); halaman dataset kini v5 (DOI 10.17632/27c8pwsd6v.5, CC BY 4.0, 10 kelas D00–D90) — update versi, bukan entri baru. Paper pendamping Measurement 2024 (YOLOv5 global 8 negara, DOI 10.1016/j.measurement.2024.116453) adalah sitasi BERBEDA yang layak ditambahkan sebagai baseline 10-kelas. Keduanya perlu disitasi distinctly. URL dataset: https://data.mendeley.com/datasets/27c8pwsd6v/5. URL paper: https://www.sciencedirect.com/science/article/abs/pii/S0263224124023388 (metrik belum terverifikasi — jangan kutip angka sebelum dibaca).

**CHECK — Arya et al. transfer-learning preprint (arXiv:2008.13101).** Preseden transfer Jepang→negara-lain + rekomendasi deployment bagi dinas — kemungkinan besar versi preprint dari `arya2021deep` (Automation in Construction) yang sudah dimiliki. Verifikasi sebelum menambah; bila sama, simpan versi journal saja. URL: https://arxiv.org/abs/2008.13101.

**BACKUP — Pham et al. YOLOv7 CRDDC'2022 3rd place (arXiv:2211.00091); Rachman et al. YOLOv7 CWD-NMS Indonesia (JOIN 2025); Arya RDD2020 Data in Brief 2021 (DOI 10.1016/j.dib.2021.107133).** Cadangan bila butuh exemplar metode YOLOv7 atau sitasi Indonesia kedua.

### 4. Imbalance, loss, distractor, objek kecil (menjawab Q4)

**ADD — Lin et al. Focal Loss (ICCV 2017).** Fondasi loss untuk foreground–background ~1:1000: faktor (1−pt)^γ, γ=2 terbaik, varian α-balanced, init prior π=0,01; RetinaNet-101-FPN 39,1 COCO AP. Dibaca langsung via HTML. Untuk subseksi imbalance/loss Bab 2 (9,67x patchy/longitudinal). URL: https://arxiv.org/abs/1708.02002.

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

**ADD — Li et al. Generalized Focal Loss (NeurIPS 2020).** Jembatan focal → quality-aware: joint classification–IoU + distribusi box diskrit umum; QFL (|y−σ|^β, β=2) + DFL; +0,6–0,8 AP tanpa overhead inferensi; 45,0% COCO AP (R-101), 48,2% single-scale terbaik. Dibaca langsung via HTML. Untuk subseksi perbandingan loss (GFL/VFL/REG) pada batas pothole/patch ambigu. URL: https://arxiv.org/abs/2006.04388.

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

**ADD — Zhang et al. VarifocalNet (CVPR 2021 oral).** Alternatif IoU-aware ranking (IACS + Varifocal Loss, ~2 AP gain, 55,1 AP terbaik — level abstrak). Untuk diskusi ablasi loss/head. URL: https://arxiv.org/abs/2008.13367.

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

**ADD (proposal→bib) — Panboonyuen REG (KST 2025).** Satu-satunya refinement focal spesifik domain jalan yang ditemukan; klaim self-reported mAP50 80,34 / F1 77,87 di jalan Thailand (dari README repo — perlakukan sebagai unverified sampai teks IEEE/arXiv dibaca). Sudah di proposal (`panboonyuen2025reg`), belum di bib IEEE — tambahkan sebagai metode, bukan sebagai angka. URL repo: https://github.com/kaopanboonyuen/REG; IEEE: https://ieeexplore.ieee.org/document/11003314/; arXiv: https://arxiv.org/abs/2409.09877.

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

**ADD — Bučko et al. (Sensors 2022, 22:8878).** Satu-satunya preseden eksplisit manhole-sebagai-distractor: kelas manhole ditambahkan karena bentuk bulat meniru pothole; manhole empiris lebih mudah daripada pothole — pola yang sama dengan TA (manhole 0,82–0,85 vs pothole 0,526–0,541). Untuk subseksi distractor + error analysis ablasi 6-vs-4 kelas. Level snippet/abstrak — baca full-text sebelum mengutip detail. URL: https://doi.org/10.3390/s22228878.

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

**ADD — Lin et al. COCO (ECCV 2014).** Jangkar metrik normatif untuk evaluasi multi-skala mAP-S/M/L mengingat median box TA 1,69% luas citra (rezim objek kecil); 328K citra / 2,5M instance / 91 kategori. Threshold piksel S/M/L perlu verifikasi ulang ke protokol evaluasi resmi saat penulisan. URL: https://arxiv.org/abs/1405.0312.

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

**ADD (proposal→bib) — Yang et al. SimAM (ICML 2021, PMLR 139:11863–11874).** Baseline atensi nol-parameter (bobot 3-D per feature map dari solusi closed-form fungsi energi, <10 baris kode) — pembanding CBAM berparameter dalam ablasi atensi neck. URL: https://proceedings.mlr.press/v139/yang21o.html.

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

**COMPLETE (proposal→bib) — Han et al. GhostNet (CVPR 2020).** Sitasi first-principles GhostConv (ghost feature maps dari transformasi linear murah; 75,7% top-1 ImageNet dengan biaya setara MobileNetV3) untuk cabang efisiensi YOLOv8-PD (2,46M/7,7 GFLOPs/368 FPS). URL: https://arxiv.org/abs/1911.11907.

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

**COMPLETE (proposal→bib) — Woo et al. CBAM (ECCV 2018).** Counterpart atensi berparameter (channel+spatial sekuensial, overhead negligible). Pasangkan dengan SimAM saat melaporkan delta Params/GFLOPs/FPS. URL: https://arxiv.org/abs/1807.06521.

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

**ADD — Wang et al. ECA-Net (CVPR 2020).** Preseden efisiensi atensi terkuat (interaksi cross-channel lokal via conv 1-D tanpa reduksi dimensi; +80 params, +4,7e-4 GFLOPs untuk gain Top-1 >2%) — layak disebut satu baris sebagai kandidat ablasi masa depan walau TA hanya memakai SimAM/CBAM. URL: https://arxiv.org/abs/1910.03151.

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

**ADD — Zhu et al. DCNv2 (CVPR 2019).** Pelengkap deformable-conv (modulasi offset+amplitudo, integrasi conv3–conv5, feature mimicking, klaim modul tetap ringan) untuk cabang akurasi YOLO-RD — pasangkan dengan `dai2017deformable` yang sudah ada. URL: https://arxiv.org/abs/1811.11168.

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

**ADD — Finder et al. WTConv (ECCV 2024).** Sitasi kanonis modul wavelet-refinement YOLO-RD (skala log-param terhadap receptive field, Haar WT, drop-in depth-wise conv) — argumen "receptive field besar untuk retak tipis dengan biaya rendah". URL: https://arxiv.org/abs/2407.05848.

**ADD — Tan et al. EfficientDet (CVPR 2020).** Referensi keluarga detector efisien (BiFPN + compound scaling; D7 55,1 AP / 77M / 410B FLOPs) sebagai konteks klaim efisiensi YOLOv8-PD. URL: https://arxiv.org/abs/1911.09070.

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

**ADD (proposal→bib) — Hugo et al. (2025) EfficientDet-D0 Indonesia.** Instansiasi Indonesia (F1 validasi 59,7% pada pothole/retak, mengalahkan prior work) — sitasi relevansi geografis, bukan angka SOTA. Caveat: outlet JMLDL visibilitas rendah — cek indeksasi sebelum bobot setara venue besar. URL PDF: https://www.academicedgepress.co.uk/publicresources/documents/JMLDL.1.1/JMLDL.2.1/EfficientDet%20Model%20for%20Accurate%20Detection%20and%20Classification%20of%20Road%20Damages%20in%20Indonesia.pdf.

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

**COMPLETE (proposal→bib) — Lineage YOLO + metodologi benchmark.** Redmon v1 (2016, sudah ada — gabungkan/rename key `redmon2017` yang salah tahun), Redmon & Farhadi YOLOv3 (arXiv:1804.02767), Bochkovskiy YOLOv4 (arXiv:2004.10934), Ge YOLOX anchor-free decoupled head + SimOTA (arXiv:2107.08430), panduan metrik Ultralytics (P/R/mAP50/mAP50-95 + rincian speed — cerminan protokol RTX 4070 SUPER bs=1 imgsz-640 TA). URL: https://arxiv.org/abs/1804.02767, https://arxiv.org/abs/2004.10934, https://arxiv.org/abs/2107.08430, https://docs.ultralytics.com/guides/yolo-performance-metrics/.

## Evidence-backed caveats and disagreements

- Tingkat bukti tidak seragam: hanya Zeng 2024, RSDD 2025, Focal Loss, GFL, docs YOLO26, halaman arXiv/Mendeley, dan PDF Hugo-2025 yang dibaca langsung; sisanya abstrak/metadata/snippet. Angka dari level snippet (YOLO-RD Neurocomputing, RDD-YOLO, YOLOv12 COCO, VarifocalNet, REG 80,34, Bandung 93,06%, Kaya Measurement) tidak boleh dikutip sebagai fakta sampai full-text dibaca.
- Duplikasi silang file riset: T1 mengklaim Arya RDD2022 sebagai NEW, T2 benar menandainya duplikat `Arya2024846` — versi T2 yang dipakai di laporan ini.
- Ketidaksepakatan tahun/key: `tian2026yolov12` (existing) vs arXiv 2025; `kaya2024nrdd2024` v3 vs dataset v5; `arya2021deep` vs preprint transfer-learning; `redmon2017` vs venue kanonis 2016. Semua dinormalisasi di rekomendasi merge di atas.
- Latar belakang non-teknis proposal (beban muatan, iklim tropis, keselamatan — `kusumah2023deep`, `hosseini2021prediction`, `mandal2020deep`, `suhartono2019estimated`, `radopoulou2015detection`) berada di luar cakupan 4 brief dan tidak diverifikasi di sini — pertahankan key proposal untuk skripsi, jangan harapkan dari laporan ini.
- Klaim dari outlet kecil (JMLDL Bandung/Indonesia, JAILCD) ditandai sesuai asalnya;570+ sitasi GhostNet/CBAM/ECA adalah metadata OpenAlex, bukan verifikasi isi.

## Open questions

1. Nama benar "YOLO-LWD / Shi 2026"? Nol hasil — butuh pencarian author/judul khusus sebelum disitasi.
2. Identitas `kaya2024nrdd2024`: dataset v3 vs paper Measurement — TA perlu mengutip keduanya secara distinct; konfirmasi key mana yang menunjuk ke mana.
3. Full-text yang masih perlu dibaca sebelum mengutip angka: YOLO-RD (kedua versi), RDD-YOLO, YOLOv12, REG, DA-RDD, Kaya Measurement, Bandung, Bučko, COCO thresholds.
4. Sitasi teori generalisasi domain kedua (di luar DA-RDD) bila Bab 2 butuh lebih dari satu — kandidat WACV'26 prompting / CNRDD hanya muncul sebagai snippet, belum terverifikasi.
5. DCNv3 / InternImage kanonis belum diamankan — butuh pencarian exact-title khusus.
6. Nama depan Wu/Zhang/Fan 2025 dan daftar penulis RT-DETR perlu verifikasi dari halaman artikel sebelum BibTeX final.
