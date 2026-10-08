# T2 — Datasets, benchmarks, domain gap: research-domain draft

## Search terms used (exact)
1. `RDD2022 road damage dataset CRDDC2022 challenge winning F1`
2. `N-RDD2024 normalized road damage detection dataset paper`
3. `road damage detection Indonesia dataset YOLO study`
4. `cross-country domain shift road damage detection generalization`
5. `Kaya Codur N-RDD2024 road damage defects journal paper YOLO`
6. `Maeda road damage detection classification smartphone images 2018 deep neural networks`
7. `Global Road Damage Detection Challenge GRDDC 2020 arXiv winning F1 score`
8. `pothole crack detection Indonesia Bandung road YOLO deep learning`
9. `unsupervised domain adaptive object detection Faster R-CNN Cityscapes Foggy review`

Paper-search backends (`feynman_science_database_search`, semanticscholar/openalex) returned fetch failures during this run, so paper discovery was done via `web_search` (parallel-mcp) + direct `fetch_content` on arXiv abs pages, Mendeley Data, and journal pages. Abstracts/HTML/metadata were preferred; no full PDF was parsed (PDF parsing blocked / not attempted beyond HTML/abs). All claims below come from read snippets/pages; full-text details not read are marked as such.

## Candidate list (9 candidates)

### C1 — RDD2022 multi-national dataset (dataset foundation)
- **Title:** RDD2022: A multi-national image dataset for automatic Road Damage Detection
- **Authors:** Deeksha Arya, Hiroya Maeda, Sanjay Kumar Ghosh, Durga Toshniwal, Yoshihide Sekimoto
- **Venue + year:** arXiv cs.CV preprint, 18 Sep 2022 (IEEE BigData Cup CRDDC'2022 data article; journal version: Geoscience Data Journal, Arya et al. 2024 [8])
- **DOI / arXiv ID + URL:** arXiv:2209.08538 — https://arxiv.org/abs/2209.08538 ; DOI 10.48550/arXiv.2209.08538
- **Findings (2–4 sentences):** RDD2022 comprises 47,420 road images from six countries (Japan, India, Czech Republic, Norway, US, China) with 55,000+ damage instances across four classes (longitudinal, transverse, alligator cracks, potholes) [1]. It extends RDD2018 (9,053 images / 15,435 instances) → RDD2019/2020 → RDD2022, was released as the CRDDC'2022 challenge dataset, and is explicitly framed for low-cost smartphone-based monitoring by municipalities plus benchmarking by ML researchers [1]. The journal version notes persistent challenges of data imbalance, data sparsity, and domain shift for global models [8].
- **Fits TA section:** Ch.2 dataset/background because it is the direct parent dataset of the TA's N-RDD2024 Asia subset and the source of the 4-class taxonomy.
- **BibTeX:**
```bibtex
@misc{arya2022rdd2022,
  author = {Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Sekimoto, Yoshihide},
  title = {{RDD2022}: A multi-national image dataset for automatic Road Damage Detection},
  year = {2022},
  eprint = {2209.08538},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV},
  doi = {10.48550/arXiv.2209.08538},
  url = {https://arxiv.org/abs/2209.08538}
}
```
- **Duplicate-vs-existing:** LIKELY DUPLICATE of existing `Arya2024846 (RDD2022)` cited in proposal — verify key/year before adding; keep journal version (Arya et al. 2024, doi:10.1002/gdj3.260) as the citable record if the existing key already covers the preprint.

### C2 — CRDDC'2022 challenge report (benchmark + winning F1 + cross-country variance)
- **Title:** Crowdsensing-based Road Damage Detection Challenge (CRDDC'2022)
- **Authors:** Deeksha Arya, Hiroya Maeda, Sanjay Kumar Ghosh, Durga Toshniwal, Hiroshi Omata, Takehiro Kashiyama, Yoshihide Sekimoto
- **Venue + year:** arXiv cs.CV preprint, 21 Nov 2022 (IEEE Big Data 2022 Big Data Cup; IEEE proceedings version doi:10.1109/BigData55660.2022.10021040); 9 pages
- **DOI / arXiv ID + URL:** arXiv:2211.11362 — https://arxiv.org/abs/2211.11362 ; proceedings: https://www.computer.org/csdl/proceedings-article/big-data/2022/10021040/1KfRDEJmQo0
- **Findings (2–4 sentences):** 47,420 images from six countries; 60+ teams from 19 countries; five leaderboards (overall + per-country); best model uses YOLO + Faster-RCNN ensemble learning with F1 ≈ 0.76 on combined six-country test data [2]. The journal companion reports the top model at F1 76.9% overall and notes per-country gaps between top/bottom teams of 16.2% (India) to 21.2% (Norway), i.e. documented cross-country performance disparity [8]. This is the primary benchmark justifying the TA's "source variance" discussion.
- **Fits TA section:** Ch.2 benchmark/SOTA + Ch.4 discussion because it gives the official winning F1 (0.76–0.77) and the per-country spread the TA mirrors (China ≫ Japan > India).
- **BibTeX:**
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
- **Duplicate-vs-existing:** NEW (challenge report; distinct from RDD2022 dataset paper) — recommend adding unless proposal already cites it implicitly via Arya2024846.

### C3 — GRDDC'2020 challenge report (predecessor benchmark, F1 0.67)
- **Title:** Global Road Damage Detection: State-of-the-art Solutions
- **Authors:** Deeksha Arya, Hiroya Maeda, Sanjay Kumar Ghosh, Durga Toshniwal, Hiroshi Omata, Takehiro Kashiyama, Yoshihide Sekimoto
- **Venue + year:** arXiv cs.CV preprint, 17 Nov 2020 (IEEE Big Data 2020 Big Data Cup)
- **DOI / arXiv ID + URL:** arXiv:2011.08740 — https://arxiv.org/abs/2011.08740 ; DOI 10.48550/arXiv.2011.08740
- **Findings (2–4 sentences):** 26,336 images from India, Japan, Czech Republic; 121 registered teams; test1 (2,631) / test2 (2,664 images); best model is YOLO-based ensemble with F1 0.67 (test1) / 0.66 (test2), top-3 teams >60% via ensembles + augmentation [3]. Provides the historical baseline showing progress 0.67 (2020, 3 countries) → 0.76–0.77 (2022, 6 countries).
- **Fits TA section:** Ch.2 benchmark evolution because it anchors the "challenge series improved but cross-country gap persists" narrative.
- **BibTeX:**
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
- **Duplicate-vs-existing:** NEW — recommend adding (predecessor benchmark not in existing-keys list).

### C4 — Transfer-learning / multi-country generalization study (direct domain-gap precedent)
- **Title:** Transfer Learning-based Road Damage Detection for Multiple Countries
- **Authors:** Deeksha Arya, Hiroya Maeda, Sanjay Kumar Ghosh, Durga Toshniwal, Alexander Mraz, Takehiro Kashiyama, Yoshihide Sekimoto
- **Venue + year:** arXiv cs.CV/cs.CY preprint, 30 Aug 2020; 16 pages
- **DOI / arXiv ID + URL:** arXiv:2008.13101 — https://arxiv.org/abs/2008.13101 ; DOI 10.48550/arXiv.2008.13101
- **Findings (2–4 sentences):** Assesses usability of the Japanese model in other countries; proposes a 26,620-image heterogeneous multi-country smartphone dataset; proposes generalized multi-country models and gives deployment recommendations for agencies reusing another country's data/model [4]. This is the closest published precedent for the TA's zero-shot question (train on foreign data, test locally).
- **Fits TA section:** Ch.2 domain-shift framing + Ch.5 recommendations because it directly tests Japanese→other-country transfer and advises municipalities.
- **BibTeX:**
```bibtex
@misc{arya2020transfer,
  author = {Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Mraz, Alexander and Kashiyama, Takehiro and Sekimoto, Yoshihide},
  title = {Transfer Learning-based Road Damage Detection for Multiple Countries},
  year = {2020},
  eprint = {2008.13101},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV},
  doi = {10.48550/arXiv.2008.13101},
  url = {https://arxiv.org/abs/2008.13101}
}
```
- **Duplicate-vs-existing:** POSSIBLE OVERLAP with existing `arya2021deep` — verify; if `arya2021deep` is the journal version of this preprint, cite the journal instead and drop this preprint.

### C5 — Smartphone-based foundation study (RDD2018 origin, crowdsensing method)
- **Title:** Road Damage Detection and Classification Using Deep Neural Networks with Smartphone Images
- **Authors:** Hiroya Maeda, Yoshihide Sekimoto, Toshikazu Seto, Takehiro Kashiyama, Hiroshi Omata
- **Venue + year:** Computer-Aided Civil and Infrastructure Engineering, vol. 33(12), pp. 1127–1141, Dec 2018 (preprint arXiv:1801.09454, Feb 2018)
- **DOI / arXiv ID + URL:** DOI 10.1111/mice.12387 — https://onlinelibrary.wiley.com/doi/10.1111/mice.12387 ; preprint https://arxiv.org/abs/1801.09454 ; code https://github.com/sekilab/RoadDamageDetector/
- **Findings (2–4 sentences):** First large-scale smartphone road-damage dataset: 9,053 images / 15,435 instances collected with 7 Japanese municipalities (>40 h driving, varied weather/illumination), 8 damage classes; SSD/MobileNet-style detectors run on GPU server and on-smartphone with accuracy-vs-speed comparison [5]. Establishes the crowdsensing-by-smartphone methodology every later RDD round reuses.
- **Fits TA section:** Ch.2/3 methods background because the TA's Bandung capture protocol is a smartphone-crowdsensing replication of this design.
- **BibTeX:**
```bibtex
@article{maeda2018road,
  author = {Maeda, Hiroya and Sekimoto, Yoshihide and Seto, Toshikazu and Kashiyama, Takehiro and Omata, Hiroshi},
  title = {Road Damage Detection and Classification Using Deep Neural Networks with Smartphone Images},
  journal = {Computer-Aided Civil and Infrastructure Engineering},
  volume = {33},
  number = {12},
  pages = {1127--1141},
  year = {2018},
  doi = {10.1111/mice.12387},
  url = {https://onlinelibrary.wiley.com/doi/10.1111/mice.12387}
}
```
- **Duplicate-vs-existing:** NEW (foundational; not in existing-keys list) — recommend adding.

### C6 — N-RDD2024 dataset record (TA's exact training source)
- **Title:** N-RDD2024: Road damage and defects (dataset)
- **Authors/Contributors:** Ömer Kaya, Muhammed Yasin Çodur
- **Venue + year:** Mendeley Data, v5 20 Nov 2024 (v3 Jan 2024; institution Erzurum Teknik Üniversitesi)
- **DOI + URL:** DOI 10.17632/27c8pwsd6v.5 — https://data.mendeley.com/datasets/27c8pwsd6v/5 ; licence CC BY 4.0
- **Findings (2–4 sentences):** Edited/updated RDD2022 relabelled to 10 defect classes D00–D90 (adds repaired cracks D30, pedestrian-crossing blur D50, lane-line blur D60, manhole D70, patchy section D80, rutting D90 beyond the RDD2022 four) [6]. Dataset page categories span image processing / object detection / road safety; this is the authoritative citation for the TA's 9,670-image Asia subset provenance.
- **Fits TA section:** Ch.3 data section because it is the citable source of the exact training distribution (must cite dataset DOI, not just the derived paper).
- **BibTeX:**
```bibtex
@misc{kaya2024nrdd2024data,
  author = {Kaya, {\"O}mer and {\c{C}}odur, Muhammed Yasin},
  title = {{N-RDD2024}: Road damage and defects},
  year = {2024},
  publisher = {Mendeley Data},
  version = {5},
  doi = {10.17632/27c8pwsd6v.5},
  url = {https://data.mendeley.com/datasets/27c8pwsd6v/5}
}
```
- **Duplicate-vs-existing:** LIKELY DUPLICATE of existing `kaya2024nrdd2024` — verify whether that key points to this dataset DOI or to the Measurement journal paper (C7); if the latter, keep both (dataset + paper are distinct citables).

### C7 — N-RDD2024 companion journal paper (10-class global YOLOv5 study)
- **Title:** Automatic detection and classification of road defects on a global-scale: Embedded system
- **Authors:** Ömer Kaya, Muhammed Yasin Çodur
- **Venue + year:** Measurement (Journal of the International Measurement Confederation), 2024
- **DOI + URL:** DOI 10.1016/j.measurement.2024.116453 — https://www.sciencedirect.com/science/article/abs/pii/S0263224124023388
- **Findings (2–4 sentences, from search-result snippet — full text NOT read):** Reports YOLOv5 detection/classification over 10 classes from eight countries as an embedded/real-time system; snippet claims global-scale framing beyond a single region [7]. Per-class numbers, split sizes, and mAP values were NOT verified (paywalled abstract page; full text not fetched) — do not quote metrics from this source until read.
- **Fits TA section:** Ch.2 related-work (10-class YOLO baseline) because it is the peer-reviewed companion to the TA's exact training dataset.
- **BibTeX (metadata-only; verify volume/pages on read):**
```bibtex
@article{kaya2024automatic,
  author = {Kaya, {\"O}mer and {\c{C}}odur, Muhammed Yasin},
  title = {Automatic detection and classification of road defects on a global-scale: Embedded system},
  journal = {Measurement},
  year = {2024},
  doi = {10.1016/j.measurement.2024.116453},
  url = {https://www.sciencedirect.com/science/article/abs/pii/S0263224124023388}
}
```
- **Duplicate-vs-existing:** POSSIBLE DUPLICATE of `kaya2024nrdd2024` — if that key is this paper, no new entry needed; confirm which of C6/C7 the existing key covers.

### C8 — DA-RDD domain-adaptive road damage detection (domain-shift theory + method)
- **Title:** DA-RDD: Toward Domain Adaptive Road Damage Detection Across Different Countries
- **Authors:** Chunmian Lin, Daxin Tian, Xuting Duan, Jianshan Zhou, Dezong Zhao, Dongpu Cao
- **Venue + year:** IEEE Transactions on Intelligent Transportation Systems, vol. 24(3), Mar 2023
- **DOI + URL:** IEEE Xplore 9954613 — https://ieeexplore.ieee.org/document/9954613
- **Findings (2–4 sentences, from IEEE abstract snippet — full text NOT read):** Proposes unsupervised domain adaptation combining image-level and instance-level adversarial alignment (importance weighting + RoI-wise multi-scale context aggregation); builds RDD2021 with 100k synthetic labeled distress images from RDD2020; claims first systematic study of domain-adaptive pavement-crack detection with cross-country experiments [9]. Gives the TA a principled "future work" method (UDA) rather than just reporting the gap.
- **Fits TA section:** Ch.2 theory + Ch.5 future work because it is the only road-damage-specific UDA framework found, directly addressing the TA's >50% zero-shot drop.
- **BibTeX (verify pages on read):**
```bibtex
@article{lin2023dardd,
  author = {Lin, Chunmian and Tian, Daxin and Duan, Xuting and Zhou, Jianshan and Zhao, Dezong and Cao, Dongpu},
  title = {{DA-RDD}: Toward Domain Adaptive Road Damage Detection Across Different Countries},
  journal = {IEEE Transactions on Intelligent Transportation Systems},
  volume = {24},
  number = {3},
  year = {2023},
  doi = {10.1109/TITS.2022.3226018},
  url = {https://ieeexplore.ieee.org/document/9954613}
}
```
  - NOTE: DOI above (10.1109/TITS.2022.3226018) was NOT verified in-page; Xplore article number 9954613 was verified [9]. Confirm DOI before compiling IEEE bib.
- **Duplicate-vs-existing:** NEW — recommend adding (only domain-adaptation-theory entry).

### C9 — Bandung City YOLOv8+CNN hybrid (in-domain Indonesian/Bandung comparator)
- **Title:** Enhancing Road Maintenance Strategies in Bandung City Through YOLO and CNN-Based Damage Detection
- **Authors:** Munawir Munawir, Muhammad Salam Pararta, Wirmanto Suteddy, Muhammad Taufik Dwi Putra, Mochamad Donny Koerniawan, Bart Julien Dewancker
- **Venue + year:** Journal of Asian Institute of Low Carbon Design (JAILCD), vol. 2025, published 5 Sep 2025
- **DOI + URL:** DOI 10.69368/jailcd.20250009 — https://journal.moi.work/index.php/AILCD/article/view/418
- **Findings (2–4 sentences, abstract read directly):** Hybrid YOLOv8 (rapid region proposal) + CNN (precise classification) trained on high-resolution Bandung road images covering cracks/potholes/other defects; reports 93.06% average accuracy, claimed consistent across datasets and better than traditional/standalone-AI methods, framed for Bandung maintenance prioritization [10]. Metric is accuracy (not mAP/F1) and the evaluation protocol was not read — not directly comparable to the TA's mAP50 numbers.
- **Fits TA section:** Ch.1/5 localization argument because it is the only Bandung-specific AI road-damage study found, proving local relevance while its accuracy-vs-mAP mismatch motivates the TA's stricter zero-shot protocol.
- **BibTeX:**
```bibtex
@article{munawir2025bandung,
  author = {Munawir, Munawir and Pararta, Muhammad Salam and Suteddy, Wirmanto and Putra, Muhammad Taufik Dwi and Koerniawan, Mochamad Donny and Dewancker, Bart Julien},
  title = {Enhancing Road Maintenance Strategies in {Bandung} City Through {YOLO} and {CNN}-Based Damage Detection},
  journal = {Journal of Asian Institute of Low Carbon Design},
  year = {2025},
  doi = {10.69368/jailcd.20250009},
  url = {https://journal.moi.work/index.php/AILCD/article/view/418}
}
```
- **Duplicate-vs-existing:** NEW — recommend adding (sole Bandung comparator).

## Supporting / rejected / duplicate notes
- **S1 — Pham et al. YOLOv7 + coordinate attention (CRDDC'2022 3rd place).** arXiv:2211.00091, https://arxiv.org/abs/2211.00091 : F1 81.7% on US Google-Street-View subset, 74.1% overall; ranked 3rd of 51 teams [3-refs]. REJECTED as standalone candidate (winner-report C2 already covers the benchmark; keep as backup if a per-method YOLOv7 exemplar is needed in Ch.2).
- **S2 — ITS Indonesia YOLOv7 + Cluster-Weighted DIoU-NMS (Rachman et al., JOIN 2025).** https://scholar.its.ac.id/en/publications/road-damage-detection-using-yolov7-with-cluster-weighted-distance , doi:10.15575/join.v10i1.1481 : Indonesian pothole study combining new local data with public sets; YOLOv7 beats Faster R-CNN; improved NMS for small/close potholes. REJECTED from top-9 on space (Bandung C9 prioritized as the in-country comparator); keep as second Indonesian citation if room.
- **S3 — Hendra et al. YOLOv5n pothole on Indonesian roadways (SENSI 2023).** https://ejournal.raharja.ac.id/sensi/article/download/2911/1711/6332 : YOLOv5nano (~3M params, 281 layers) for smartphone/Raspberry-Pi deployment. REJECTED (low-venue, nano-only pothole scope); useful only for an edge-deployment aside.
- **S4 — Arya et al. challenge-series retrospective (Nat. Mach. Intell. 2025).** https://doi.org/10.1038/s42256-025-01132-5 : organizers' 2018–2024 reflection. REJECTED (commentary, paywalled, adds no numbers beyond C2/C3).
- **Duplicates to verify before bib edit:** C1↔`Arya2024846`, C4↔`arya2021deep`, C6/C7↔`kaya2024nrdd2024`. `hugo2025efficientdet` and `matouq2024ai` were not encountered in this search and are unaffected.

## Open questions
1. Which existing bib key covers which N-RDD item — does `kaya2024nrdd2024` cite the Mendeley dataset DOI (C6) or the Measurement paper (C7)? TA needs both cited distinctly.
2. Unverified numbers: C7 per-class mAP/split sizes; C8 article DOI/pages and RDD2021 construction details; C9 accuracy protocol and dataset size — each needs 1 full-text read before quoting metrics.
3. Indonesia gap stands: no Indonesia-containing RDD round found (RDD2022 countries confirmed [1][2]); Bandung C9 is a local single-city study, not a multi-country benchmark — the "Indonesia absent from RDD2022" claim is supported by the country lists read.
4. Cross-device/cross-national generalization beyond DA-RDD (e.g., WACV'26 self-supervised prompting, CNRDD attention models) surfaced only as snippets and was not verified — candidate follow-up if Ch.2 theory needs a second domain-generalization citation.

## Evidence table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Arya et al., RDD2022 preprint (arXiv:2209.08538, 2022) | https://arxiv.org/abs/2209.08538 | 47,420 images / 55k+ instances, 6 countries, 4 classes; CRDDC'2022 dataset | primary (dataset paper) | high |
| 2 | Arya et al., CRDDC'2022 report (arXiv:2211.11362, 2022) + IEEE BigData proceedings | https://arxiv.org/abs/2211.11362 | 60+ teams/19 countries; YOLO+Faster-RCNN ensemble F1 ≈0.76 overall | primary (challenge report) | high |
| 3 | Arya et al., GRDDC'2020 report (arXiv:2011.08740, 2020) | https://arxiv.org/abs/2011.08740 | 26,336 images, 3 countries; winning YOLO ensemble F1 0.67/0.66 | primary (challenge report) | high |
| 4 | Arya et al., Transfer Learning multi-country (arXiv:2008.13101, 2020) | https://arxiv.org/abs/2008.13101 | Japanese-model transfer test; 26,620-image heterogeneous set; generalized models + agency guidance | primary (paper) | high (abstract-level; full text not parsed) |
| 5 | Maeda et al., Smartphone road damage (CACIE 2018; arXiv:1801.09454) | https://onlinelibrary.wiley.com/doi/10.1111/mice.12387 | 9,053 images / 15,435 instances, 8 classes, 7 municipalities; on-phone detection | primary (journal) | high |
| 6 | Kaya & Çodur, N-RDD2024 dataset (Mendeley Data v5, 2024) | https://data.mendeley.com/datasets/27c8pwsd6v/5 | RDD2022 relabelled to 10 classes D00–D90; CC BY 4.0 | primary (dataset record, read directly) | high |
| 7 | Kaya & Çodur, global-scale embedded system (Measurement, 2024) | https://www.sciencedirect.com/science/article/abs/pii/S0263224124023388 | YOLOv5, 10 classes, 8 countries, real-time/embedded framing | secondary (search snippet; full text not read) | medium |
| 8 | Arya et al., RDD2022 journal (Geosci. Data J., 2024) | https://rmets.onlinelibrary.wiley.com/doi/10.1002/gdj3.260 | Top F1 76.9–77%; per-country top–bottom gaps 16.2–21.2% | primary (journal data article) | high (snippet-level; page read via search excerpt) |
| 9 | Lin et al., DA-RDD (IEEE T-ITS 24(3), 2023) | https://ieeexplore.ieee.org/document/9954613 | Image+instance adversarial UDA; RDD2021 100k synthetic; first cross-country adaptive crack study | primary (journal; abstract snippet only) | medium |
| 10 | Munawir et al., Bandung YOLOv8+CNN (JAILCD 2025) | https://journal.moi.work/index.php/AILCD/article/view/418 | Bandung images; hybrid YOLOv8+CNN; 93.06% avg. accuracy | primary (journal abstract read directly) | medium-high (abstract only; protocol unread) |
| 11 | Pham et al., YOLOv7 road damage (arXiv:2211.00091, 2022) | https://arxiv.org/abs/2211.00091 | F1 81.7% US-GSV / 74.1% overall; CRDDC'2022 3rd of 51 | primary (preprint) | medium (snippet-level) |
| 12 | Rachman et al., YOLOv7 CWD-NMS Indonesia (JOIN 10(1), 2025) | https://scholar.its.ac.id/en/publications/road-damage-detection-using-yolov7-with-cluster-weighted-distance | Indonesian pothole set + public data; YOLOv7 > Faster R-CNN | primary (journal record) | medium (index page only) |

## Findings (with inline references)
- The RDD family grew from 9,053 smartphone images in 7 Japanese municipalities (8 classes) [5] to 26,336 images / 3 countries for GRDDC'2020 [3] and 47,420 images / 55k+ instances / 6 countries for RDD2022/CRDDC'2022 (4 classes) [1][2].
- Challenge performance progressed from winning F1 0.67/0.66 (GRDDC'2020, YOLO ensemble) [3] to ≈0.76 overall (CRDDC'2022, YOLO+Faster-RCNN ensemble) [2], with the journal record at 76.9–77% [8]; a contemporaneous YOLOv7 entry scored 74.1% overall (3rd place) with 81.7% on the US subset [11] — an inference from converging snippets is that per-country variance is structural, not method-specific.
- Cross-country disparity is documented twice: top–bottom team gaps of 16.2% (India) to 21.2% (Norway) in CRDDC'2022 [8], and an earlier explicit Japanese→other-country transfer test with a 26,620-image heterogeneous set plus agency reuse guidance [4] — together these license the TA's domain-gap framing and its >50% zero-shot drop as expected rather than anomalous.
- The TA's training source is precisely identified: N-RDD2024 relabels RDD2022 into 10 classes D00–D90 (adding D30/D50/D60/D70/D80/D90) under CC BY 4.0 [6], with a YOLOv5-based global 8-country companion paper [7] (metrics unverified — inference: the Asia subset used by the TA is a slice of this 10-class resource).
- Domain-shift theory specific to road damage exists: DA-RDD (IEEE T-ITS 2023) aligns image- and instance-level features adversarially and adds a 100k-image synthetic RDD2021 built from RDD2020 [9] — this is the natural Ch.5 future-work citation (full-text verification still needed).
- The Indonesian/Bandung context is covered but thin: one Bandung hybrid YOLOv8+CNN study reports 93.06% accuracy on local high-resolution images [10], and one ITS study tests YOLOv7+CWD-NMS on Indonesian potholes versus Faster R-CNN [12]; neither uses mAP/F1 zero-shot protocol, so neither contradicts the TA's 0.23–0.31 Bandung mAP50 (inference: local supervised accuracy ≫ foreign zero-shot mAP is itself evidence for the domain gap).
- Indonesia's absence from RDD2022 is confirmed by the enumerated country lists (Japan, India, Czech Republic, Norway, US, China) in both the dataset and challenge reports [1][2].

## Sources
1. Arya, Maeda, Ghosh, Toshniwal, Sekimoto — RDD2022 preprint — https://arxiv.org/abs/2209.08538
2. Arya, Maeda, Ghosh, Toshniwal, Omata, Kashiyama, Sekimoto — CRDDC'2022 report — https://arxiv.org/abs/2211.11362 (proceedings: https://www.computer.org/csdl/proceedings-article/big-data/2022/10021040/1KfRDEJmQo0)
3. Arya et al. — GRDDC State-of-the-art Solutions — https://arxiv.org/abs/2011.08740
4. Arya et al. — Transfer Learning-based Road Damage Detection for Multiple Countries — https://arxiv.org/abs/2008.13101
5. Maeda et al. — Road Damage Detection and Classification Using Deep Neural Networks with Smartphone Images — https://onlinelibrary.wiley.com/doi/10.1111/mice.12387 (preprint: https://arxiv.org/abs/1801.09454)
6. Kaya & Çodur — N-RDD2024: Road damage and defects (Mendeley Data v5) — https://data.mendeley.com/datasets/27c8pwsd6v/5
7. Kaya & Çodur — Automatic detection and classification of road defects on a global-scale: Embedded system (Measurement, 2024) — https://www.sciencedirect.com/science/article/abs/pii/S0263224124023388
8. Arya et al. — RDD2022 journal data article (Geosci. Data J., 2024) — https://rmets.onlinelibrary.wiley.com/doi/10.1002/gdj3.260
9. Lin et al. — DA-RDD (IEEE T-ITS 24(3), 2023) — https://ieeexplore.ieee.org/document/9954613
10. Munawir et al. — Bandung YOLO+CNN (JAILCD, 2025) — https://journal.moi.work/index.php/AILCD/article/view/418
11. Pham et al. — Road Damages Detection and Classification with YOLOv7 — https://arxiv.org/abs/2211.00091
12. Rachman et al. — Road Damage Detection Using YOLOv7 with Cluster Weighted Distance-IoU NMS (JOIN, 2025) — https://scholar.its.ac.id/en/publications/road-damage-detection-using-yolov7-with-cluster-weighted-distance

## Coverage status
- **Checked directly:** arXiv abs pages for C1–C4 (titles, authors, dates, abstracts, country/image counts, F1 numbers); Mendeley N-RDD2024 page (classes, DOI, licence, version); JAILCD Bandung abstract (authors, DOI, 93.06% claim); IEEE Xplore DA-RDD abstract snippet; Wiley/journal pages via search excerpts + DOI records.
- **Uncertain / snippet-only:** C7 full metrics and 8-country list; C8 DOI/pages and RDD2021 details; C9 evaluation protocol/dataset size; C5 on-phone latency figures; exact CRDDC winning-team method composition beyond "YOLO + Faster-RCNN ensemble".
- **Could not complete:** `feynman_science_database_search` backends failed (all 4 parallel queries); no PDF full-text parse (marked blocked per brief); citation-count / bib-key reconciliation against the proposal's `.bib` (no repo access in this run); second domain-generalization theory citation (WACV'26 prompting, CNRDD) left as follow-up.
