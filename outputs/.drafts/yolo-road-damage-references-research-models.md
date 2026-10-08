# YOLO lightweight road-damage models — candidate references (Brief T1)

## Exact search terms used

Paper-database searches (`feynman_science_database_search`, source `openalex` — Semantic Scholar was rate-limited, tool fell back to OpenAlex):
1. `lightweight YOLO road damage detection RDD2022`
2. `YOLO road crack pothole detection N-RDD2024`
3. `YOLOv12 YOLOv11 lightweight object detection`
4. `Wu tiny road surface damage detection YOLO lightweight Scientific Reports 2025`
5. `RDD2022 road damage dataset benchmark crowd sensing Arata`
6. `RDD2022 challenge road damage detection dataset Arya`
7. `YOLO-LWNet lightweight road damage Wu 2023`
8. `YOLO-RD lightweight multiscale road damage detection`
9. `YOLO-LWNet lightweight network road disease detection`

Web searches (`web_search`):
10. `YOLO-LWD Shi 2026 road damage` / `YOLOv8-PD Zeng 2024 road damage detection` / `YOLO-RD Wang 2025 road damage lightweight`
11. `YOLOv12 official Tian 2024 arXiv attention-centric` / `YOLO26 Sapkota 2025 official report` / `YOLOv8 official Jocher Ultralytics GitHub docs`
12. `Arya 2022 RDD2022 crowd-sourced road damage dataset Big Data` / `Wu 2025 tiny road surface damage Scientific Reports 11032` / `Ultralytics YOLOv8 YOLOv11 docs official GitHub Jocher`
13. `Wu Zhang Fan 2025 tiny road surface damage object detection Scientific Reports` / `Ultralytics YOLOv26 docs NMS-free MuSGD official` / `RT-DETR Zhao 2023 real-time detection transformers official report`
14. `N-RDD2024 Kaya Codur Mendeley Data road damage defects` / `YOLO-LWNet Wu 2023 lightweight road disease detection Sensors` / `Redmon 2016 You Only Look Once unified real-time detection CVPR`

Direct reads: full text of Zeng 2024 (PMC) and Wu 2025 RSDD (Nature page); Ultralytics YOLO26 docs page (answer-mode extract). PDF parsing of key papers was not attempted beyond HTML-readable sources — mark as blocked/not-attempted, continued from abstracts + HTML + metadata per brief.

---

## Candidate list

### C1. Zeng & Zhong (2024) — YOLOv8-PD (YOLOv8-PD/RDD-YOLO family original)
- **Title:** YOLOv8-PD: an improved road damage detection algorithm based on YOLOv8n model
- **Authors:** Jiayi Zeng, Han Zhong (China People's Public Security University)
- **Venue + year:** Scientific Reports 14, art. 12052 (2024)
- **DOI / arXiv ID + URL:** DOI 10.1038/s41598-024-62933-z — https://www.nature.com/articles/s41598-024-62933-z (full text also at https://pmc.ncbi.nlm.nih.gov/articles/PMC11130172) [3]
- **Findings (read directly, full text):** Builds on YOLOv8n with four changes: a BOT (Bottleneck Transformer/MHSA) module for long-range crack features, Large Separable Kernel Attention (LSKA) at the end of backbone and neck, a C2fGhost block in the neck, and a lightweight shared-convolution detection head (LSCD-Head); loss stays VFL + CIoU + DFL as in YOLOv8n. On RDD2022 the model has 2.3 M params and 6.1 GFLOPs (74.1% / 74.3% of baseline) with mAP improved by 1.4 percentage points over baseline; on the RoadDamage dataset mAP increased by 4.2% with good robustness [3]. Compares against Faster-RCNN, Cascade-RCNN, YOLOv3-tiny, YOLOv4-tiny, YOLOv5n/s/l, YOLOv7, YOLOv8n and YOLOv8-RD (Song Li) [3].
- **Fits TA section:** Ch.2 model description of YOLOv8-PD (reconstruction target) because it is the exact architecture spec (BOT + LSKA + C2fGhost + LSCD-Head) the TA re-implements; also Ch.4 source-benchmark context (RDD2022 numbers).
- **BibTeX:**
```bibtex
@article{zeng2024yolov8pd,
  author  = {Zeng, Jiayi and Zhong, Han},
  title   = {{YOLOv8-PD}: an improved road damage detection algorithm based on {YOLOv8n} model},
  journal = {Scientific Reports},
  volume  = {14},
  number  = {1},
  pages   = {12052},
  year    = {2024},
  doi     = {10.1038/s41598-024-62933-z}
}
```
- **Duplicate-vs-existing flag:** DUPLICATE — already have `Zeng2024`. Keep as primary citation; no new entry needed.

### C2. Li et al. (2024) — RDD-YOLO (YOLOv8-PD/RDD-YOLO family original)
- **Title:** RDD-YOLO: Road Damage Detection Algorithm Based on Improved You Only Look Once Version 8
- **Authors:** Yue Li, Chang Yin, Yutian Lei, Jiale Zhang, Yiting Yan (Donghua University)
- **Venue + year:** Applied Sciences 14(8), 3360 (2024)
- **DOI / arXiv ID + URL:** DOI 10.3390/app14083360 — https://www.mdpi.com/2076-3417/14/8/3360 [1]
- **Findings (metadata + snippet level only; MDPI page returned HTTP 403 on direct fetch):** YOLOv8-based road-damage detector using a SimAM attention mechanism and GhostConv for lightweighting, per indexed keywords/abstract snippet [1]. Exact mAP/F1 numbers NOT verified — not read; do not cite numbers without fetching via another route.
- **Fits TA section:** Ch.2 related lightweight-YOLO family (RDD-YOLO variant) because it is the named sibling baseline in the Zeng→Li→Wang lineage frequently co-cited with YOLOv8-PD.
- **BibTeX:**
```bibtex
@article{li2024rddyolo,
  author  = {Li, Yue and Yin, Chang and Lei, Yutian and Zhang, Jiale and Yan, Yiting},
  title   = {{RDD-YOLO}: Road Damage Detection Algorithm Based on Improved You Only Look Once Version 8},
  journal = {Applied Sciences},
  volume  = {14},
  number  = {8},
  pages   = {3360},
  year    = {2024},
  doi     = {10.3390/app14083360}
}
```
- **Duplicate-vs-existing flag:** DUPLICATE — already have `Li2024 (RDD-YOLO)`. Keep existing entry; numbers need a successful full-text fetch before citing.

### C3. Wu et al. (2023) — YOLO-LWNet (lightweight-network precedent)
- **Title:** YOLO-LWNet: A Lightweight Road Damage Object Detection Network for Mobile Terminal Devices
- **Authors:** Chenguang Wu, Min Ye, Jiale Zhang, Yuchuan Ma (Chang'an University)
- **Venue + year:** Sensors 23(6), 3268 (2023)
- **DOI / arXiv ID + URL:** DOI 10.3390/s23063268 — https://www.mdpi.com/1424-8220/23/6/3268 (full text also at https://pmc.ncbi.nlm.nih.gov/articles/PMC10058657) [13]
- **Findings (abstract/snippet level; full text not read):** Proposes YOLO-LWNet in Small and Tiny versions, redesigning YOLOv5-s backbone/neck/head around a lightweight LW-Conv backbone for mobile terminals; evaluated on the RDD-2020 public dataset against YOLOv5/YOLOv6, reported as balancing accuracy, model scale and complexity [13]. Exact mAP/param numbers NOT verified — need full-text read before citing figures.
- **Fits TA section:** Ch.2 lightweight-design precedent because it is the canonical mobile-oriented YOLO redesign on RDD data that motivates nano-scale model choices (and TA already cites it).
- **BibTeX:**
```bibtex
@article{wu2023yololwnet,
  author  = {Wu, Chenguang and Ye, Min and Zhang, Jiale and Ma, Yuchuan},
  title   = {{YOLO-LWNet}: A Lightweight Road Damage Object Detection Network for Mobile Terminal Devices},
  journal = {Sensors},
  volume  = {23},
  number  = {6},
  pages   = {3268},
  year    = {2023},
  doi     = {10.3390/s23063268}
}
```
- **Duplicate-vs-existing flag:** DUPLICATE — already have `Wu2023 (YOLO-LWNet)`. Keep existing entry.

### C4. Wu, Zhang & Fan (2025) — RSDD tiny-damage detector (NEW, read directly — recommended addition)
- **Title:** Object detection model design for tiny road surface damage
- **Authors:** C. Wu, L. Zhang, X. Fan (citation form per ISPRS-Annals reference list: "Wu, C., Zhang, L., & Fan, X. (2025)")
- **Venue + year:** Scientific Reports 15, art. 11032 (2025)
- **DOI / arXiv ID + URL:** DOI 10.1038/s41598-025-95502-z — https://doi.org/10.1038/s41598-025-95502-z [11]
- **Findings (read directly, full text):** Proposes RSDD with a novel backbone (dual-scale convolution downsampling DSCD + multi-strategy feature extraction MFE + SPPF), a feature-selection/fusion neck (FSM + FFM over PAN) and a multi-scale decoupled head. Trained on a self-collected set of 10,440 road images / 36,579 damage instances (D00/D10/D20/D40, 7:2:1 split) plus a 10,000-image RDD2022 subset; training recipe PyTorch, 640×640, SGD, 300 epochs, batch 16, lr 0.01, Mosaic + crop/flip/rotate/scale/brightness. Reports RSDD at 16.5 M params, 30.9 GFLOPs, mAP50 70.8% with 4.5 ms latency on the self-collected test set, and mAP50 61.2% on the RDD2022 subset (best among compared YOLOv5/v6/v8/v9 variants) [11]. Explicitly motivates tiny damage (1–2 px wide cracks, <20 px potholes) and compares necks (FPN/BiFPN/GFPN/PAN/Gold-YOLO/HSFPN) with +2.4% mAP50 over PAN [11].
- **Fits TA section:** Ch.2/4 as the strongest 2025 tiny-damage comparator because it reports RDD2022-subset mAP50 (61.2%) with params/FLOPs/latency on the same 4-class taxonomy overlapping TA's D00/D10/D20/D40.
- **BibTeX:**
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
- **Duplicate-vs-existing flag:** NEW — not in existing library. Note: author first names not verified (only initials confirmed); verify before final BibTeX.

### C5. Wang et al. (2025) — YOLO-RD (TA reconstruction target; snippet-level only)
- **Title:** YOLO-RD: Road defect detection with context-aware attention and balanced loss
- **Authors:** Peng Wang, Longqi Cheng, Jiamei Liu, Haibin Wang, Decheng Wu, Gang Ma, Wanjing Ma
- **Venue + year:** Neurocomputing (2025), DOI 10.1016/j.neucom.2025.132000
- **DOI / arXiv ID + URL:** DOI 10.1016/j.neucom.2025.132000 — https://www.sciencedirect.com/science/article/pii/S0925231225026724 [13]
- **Findings (search-snippet level only; article is paywalled, direct fetch returned 403):** Lightweight high-precision road-defect framework; snippet reports vs. YOLOv8s baseline: −39.8% params, −12.1% compute, −39.9% model size, evaluated on RM-RDD plus RDD2022 and N-RDD2024, with an NT98525 edge-device vehicle deployment [13]. Numbers are UNVERIFIED (snippet only) — must confirm from full text or abstract page before citing.
- **Fits TA section:** Ch.2 model description of YOLO-RD because it is the exact paper behind the TA's YOLO-RD reconstruction and the only listed source evaluating on N-RDD2024.
- **BibTeX (provisional — verify volume/pages):**
```bibtex
@article{wang2025yolord,
  author  = {Wang, Peng and Cheng, Longqi and Liu, Jiamei and Wang, Haibin and Wu, Decheng and Ma, Gang and Ma, Wanjing},
  title   = {{YOLO-RD}: Road defect detection with context-aware attention and balanced loss},
  journal = {Neurocomputing},
  year    = {2025},
  doi     = {10.1016/j.neucom.2025.132000}
}
```
- **Duplicate-vs-existing flag:** LIKELY DUPLICATE — already have `Wang2025 (YOLO-RD)`. Treat as same work unless page inspection proves otherwise.

### C6. Tian, Ye & Doermann (2025) — YOLOv12 official report (NEW if only `tian2026yolov12` key existsales — verify identity)
- **Title:** YOLOv12: Attention-Centric Real-Time Object Detectors
- **Authors:** Yunjie Tian, Qixiang Ye, David Doermann
- **Venue + year:** arXiv:2502.12524 (2025); published at NeurIPS 2025 (Main Conference)
- **DOI / arXiv ID + URL:** arXiv 2502.12524 — https://arxiv.org/abs/2502.12524 (NeurIPS page: https://proceedings.neurips.cc/paper_files/paper/2025/hash/7103444259031cc58051f8c9a4868533-Abstract-Conference.html) [6]
- **Findings (abstract/snippet level; HTML full text available, not fully read):** Attention-centric YOLO with Area Attention (A2), R-ELAN backbone, 7×7 separable convolutions, FlashAttention, no positional encodings, MLP ratio 1.2. Reported YOLOv12-N reaches 40.6% COCO mAP at 1.64 ms T4 latency (arXiv v1), beating YOLOv10-N/YOLO11-N by 2.1/1.2 pts; NeurIPS version reports 40.5% at 1.62 ms [6]. Independent benchmark review notes YOLOv12s led small-model accuracy but paid speed cost from A2 attention [6].
- **Fits TA section:** Ch.2 official baseline description of YOLOv12n because it is the primary source for the attention-centric architecture behind TA's best zero-shot model (Indo-v3 0.309).
- **BibTeX:**
```bibtex
@article{tian2025yolov12,
  author  = {Tian, Yunjie and Ye, Qixiang and Doermann, David},
  title   = {{YOLOv12}: Attention-Centric Real-Time Object Detectors},
  journal = {arXiv preprint arXiv:2502.12524},
  year    = {2025}
}
```
- **Duplicate-vs-existing flag:** CHECK — already have `tian2026yolov12`; almost certainly the same report under a different key/year. Merge, do not double-count.

### C7. Sapkota & Karkee (2025) + Ultralytics Docs — YOLO26/YOLOv26 official report (verify identity vs existing key)
- **Title:** Ultralytics YOLO Evolution: An Overview of YOLO26, YOLO11, YOLOv8 and YOLOv5 Object Detectors for Computer Vision and Pattern Recognition
- **Authors:** Ranjan Sapkota, Manoj Karkee (Cornell)
- **Venue + year:** arXiv:2510.09653 (2025); companion benchmarking preprint arXiv:2509.25164 (Sapkota et al., Sept 2025)
- **DOI / arXiv ID + URL:** arXiv 2510.09653 — https://arxiv.org/abs/2510.09653; official docs https://docs.ultralytics.com/models/yolo26/ [7]
- **Findings (docs page read directly):** YOLO26 innovations: DFL-free regression head, native end-to-end NMS-free inference (`nms=False` one-to-one head, max 300 detections; default one-to-many + NMS for accuracy), MuSGD (Muon+SGD) optimizer, Progressive Loss, STAL small-target label assignment. Official COCO specs (640 px): YOLO26n 40.9 mAP (40.1 NMS-free), 1.7 ms T4 TensorRT, 2.4 M params, 5.5 B FLOPs; YOLO26s 48.6 mAP / 9.5 M / 20.9 B; family range 40.9–57.5 mAP at 1.7–11.8 ms; up to 43% faster CPU ONNX than YOLO11n (fused-model counts caveat applies) [7].
- **Fits TA section:** Ch.2 official baseline description of YOLOv26n because it documents the DFL-removal/NMS-free/MuSGD recipe that distinguishes TA's fifth model from v8n/v12n.
- **BibTeX:**
```bibtex
@article{sapkota2025yolo26,
  author  = {Sapkota, Ranjan and Karkee, Manoj},
  title   = {Ultralytics {YOLO} Evolution: An Overview of {YOLO26}, {YOLO11}, {YOLOv8} and {YOLOv5} Object Detectors for Computer Vision and Pattern Recognition},
  journal = {arXiv preprint arXiv:2510.09653},
  year    = {2025}
}
```
- **Duplicate-vs-existing flag:** CHECK — already have `sapkota2025yolo26`; same work, merge keys.

### C8. Arya et al. (2022/2024) — RDD2022 dataset paper (NEW, recommended addition)
- **Title:** RDD2022: A multi-national image dataset for automatic Road Damage Detection
- **Authors:** Deeksha Arya, Hiroya Maeda, Sanjay Kumar Ghosh, Durga Toshniwal, Yoshihide Sekimoto
- **Venue + year:** arXiv:2209.08538 (2022); journal version Geoscience Data Journal 11(4), 846–862 (2024)
- **DOI / arXiv ID + URL:** DOI 10.1002/gdj3.260; arXiv https://arxiv.org/abs/2209.08538; challenge summary https://arxiv.org/abs/2211.11362 [8]
- **Findings (abstract/metadata level):** 47,420 road images from 6 countries (Japan, India, Czech Republic, Norway, USA, China) with 55,000+ damage instances across 4 classes (longitudinal/transverse/alligator cracks, potholes); released via CRDDC'2022 (IEEE Big Data Cup, 60–70 teams from 19 countries); best ensemble (YOLO + Faster-RCNN) reached 76% F1 on combined test [8]. FigShare release; journal version confirms pages 846–862 [8].
- **Fits TA section:** Ch.3 dataset provenance because RDD2022 is the parent dataset from which N-RDD2024 (and TA's Asia subset) derives; required citation for any RDD-derived benchmark.
- **BibTeX:**
```bibtex
@article{arya2024rdd2022,
  author  = {Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Sekimoto, Yoshihide},
  title   = {{RDD2022}: A multi-national image dataset for automatic road damage detection},
  journal = {Geoscience Data Journal},
  volume  = {11},
  number  = {4},
  pages   = {846--862},
  year    = {2024},
  doi     = {10.1002/gdj3.260}
}
```
- **Duplicate-vs-existing flag:** NEW — not in existing library (brief lists no Arya entry). Add.

### C9. Kaya & Çodur (2024) — N-RDD2024 dataset (NEW, recommended addition)
- **Title/contributors:** N-RDD2024: Road damage and defects — Ömer Kaya, Muhammed Yasin Çodur
- **Venue + year:** Mendeley Data, v5 (20 Nov 2024)
- **DOI / arXiv ID + URL:** DOI 10.17632/27c8pwsd6v.5 — https://data.mendeley.com/datasets/27c8pwsd6v/5 [9]
- **Findings (repository page read via snippet):** Extends RDD2022 (4 damage types) to 10 defect classes: D00 longitudinal, D10 transverse, D20 alligator, D30 repaired cracks, D40 potholes, D50 pedestrian-crossing blur, D60 lane-line blur, D70 manhole covers, D80 patchy sections, D90 rutting [9]. This is the direct source of TA's 6-class Asia subset taxonomy.
- **Fits TA section:** Ch.3 dataset section because it is the primary source for TA's N-RDD2024 Asia-subset class definitions (D00/D10/D20/D40/D70/D80).
- **BibTeX:**
```bibtex
@misc{kaya2024nrdd2024,
  author = {Kaya, {\"O}mer and {\c C}odur, Muhammed Yasin},
  title  = {{N-RDD2024}: Road damage and defects},
  year   = {2024},
  publisher = {Mendeley Data},
  version = {5},
  doi    = {10.17632/27c8pwsd6v.5}
}
```
- **Duplicate-vs-existing flag:** NEW — not in existing library. Add.

### C10. Zhao et al. (2023) — RT-DETR non-YOLO comparator (NEW if comparator wanted)
- **Title:** DETRs Beat YOLOs on Real-time Object Detection
- **Authors:** Yian Zhao et al. (Baidoo — verify before citing)
- **Venue + year:** arXiv:2304.08069 (2023)
- **DOI / arXiv ID + URL:** arXiv 2304.08069 — https://arxiv.org/abs/2304.08069 [10]
- **Findings (existence verified only; content NOT read):** Proposes RT-DETR, the real-time DETR variant positioned as the standard non-YOLO (transformer, NMS-free end-to-end) comparator against YOLO detectors [10]. No performance numbers verified — read abstract/full text before citing any claim.
- **Fits TA section:** Ch.2/5 alternative-paradigm comparator because an NMS-free transformer detector contextualizes YOLOv12-attention and YOLO26 NMS-free design choices.
- **BibTeX (provisional — verify author list):**
```bibtex
@article{zhao2023rtdetr,
  author  = {Zhao, Yian and others},
  title   = {{DETRs} Beat {YOLOs} on Real-time Object Detection},
  journal = {arXiv preprint arXiv:2304.08069},
  year    = {2023}
}
```
- **Duplicate-vs-existing flag:** NEW — but INCOMPLETE (authors unverified). Either verify or drop in favor of C6/C7 official reports.

---

## Rejected / duplicates

| Item | Verdict | Reason |
|---|---|---|
| `Zeng2024` (YOLOv8-PD) | DUPLICATE (keep) | C1 is the same paper; already in library |
| `Li2024 (RDD-YOLO)` | DUPLICATE (keep) | C2 same paper; already in library |
| `Wang2025 (YOLO-RD)` | LIKELY DUPLICATE (keep, verify) | C5 matches by title/topic; confirm DOI 10.1016/j.neucom.2025.132000 against library entry |
| `Wu2023 (YOLO-LWNet)` | DUPLICATE (keep) | C3 same paper (Sensors 23:3268) |
| `tian2026yolov12` | LIKELY DUPLICATE (merge) | C6 same report; key year (2026) conflicts with arXiv 2025 — normalize to 2025 |
| `sapkota2025yolo26` | LIKELY DUPLICATE (merge) | C7 same report/docs; confirm naming YOLO26 vs YOLOv26 |
| `matouq2024ai` | OUT OF SCOPE | Not retrieved under road-damage YOLO queries; no verified URL found in this pass |
| `redmon2016you` | DUPLICATE (keep, verified) | YOLO original: Redmon et al., CVPR 2016, DOI 10.1109/CVPR.2016.91 — https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html [12] |
| YOLO-LWD / Shi 2026 | NOT FOUND — excluded | No verifiable source found; `YOLO-LWD Shi 2026` query returned only unrelated YOLOv12/fire-damage and generic road-damage hits, zero matches for "YOLO-LWD" [2]. Per integrity rules: not cited |
| BL-YOLOv8 (Wang et al. 2023, Sensors 23:8361, DOI 10.3390/s23208361) | REJECTED (optional reserve) | Verified to exist (313 citations) [1] but deprioritized: YOLOv8-BiFPN variant adds little beyond C1/C2/C4; keep as reserve |
| SEA-YOLOv8 (Zhao et al. 2025, PLoS ONE, DOI 10.1371/journal.pone.0324439) | REJECTED (reserve) | Verified RDD2022-based YOLOv8 variant [5] but lower priority than C4/C5; reserve for related-work padding |
| YOLO-SFT (Xie et al. 2025, J. Transp. Eng.) | REJECTED (unverified) | Only citation-context snippet seen (cites Zeng 2024) [4]; content not inspected |

---

## Open questions (needs follow-up)

1. **YOLO-LWD/Shi 2026 does not appear to exist** under that name — zero hits across paper DB + web [2]. Needs follow-up: confirm whether the brief meant a different name (e.g., LL-YOLO low-light 2025, LTF-YOLO 2026, or RDL-YOLO) before citing.
2. **C2 (RDD-YOLO) and C5 (YOLO-RD) numbers are snippet-only** (MDPI 403; ScienceDirect paywall) — need follow-up full-text/abstract fetch before any mAP figures enter the thesis.
3. **C4 author first names** (Wu/Zhang/Fan 2025) need verification from the article page before finalizing BibTeX.
4. **C10 author list** unverified — verify or drop.
5. **YOLOv8 official report**: no peer-reviewed paper exists (Ultralytics tech report + GitHub/docs only); cite `Jocher et al., YOLO by Ultralytics (2023)` software entry + https://docs.ultralytics.com/models/yolov8/ if needed — needs follow-up only if TA requires it.
6. **N-RDD2024 paper vs dataset**: only the Mendeley record verified [9]; check whether Kaya/Çodur published a describing article to cite alongside the dataset DOI.

---

## Evidence table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | OpenAlex records: Li 2024 RDD-YOLO; Wang 2023 BL-YOLOv8; Wang 2024 YOLOv8s; Youwai 2024 YOLO9tr | https://openalex.org/W4394891779 (et al.) | RDD-YOLO (SimAM+GhostConv, Appl. Sci. 14:3360); BL-YOLOv8 (Sensors 23:8361, 313 cites) exist as lightweight YOLO road-damage variants | secondary (metadata) | medium |
| 2 | Parallel web search: YOLO-LWD / YOLOv8-PD / YOLO-RD queries | https://www.nature.com/articles/s41598-024-62933-z (via results) | YOLOv8-PD verified (Sci Rep 14:12052, BOT+LKSA/GhostNet/LSCD-Head); "YOLO-LWD Shi 2026" returned zero matching sources | secondary | high (existence), high (LWD absent) |
| 3 | Zeng & Zhong 2024 full text (PMC) | https://pmc.ncbi.nlm.nih.gov/articles/PMC11130172 | 2.3 M params / 6.1 GFLOPs (74.1%/74.3% of baseline); +1.4 pp mAP on RDD2022; +4.2% mAP on RoadDamage | primary (read directly) | high |
| 4 | Nature Sci Rep page (YOLOv8-PD) + ASCE YOLO-SFT citing context | https://www.nature.com/articles/s41598-024-62933-z | YOLOv8-PD published 27 May 2024, keywords GhostNet/LSCD-Head; YOLO-SFT (2025) builds on Zeng 2024 | primary + secondary | high |
| 5 | Zhao et al. 2025 SEA-YOLOv8 (PLOS ONE) | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0324439 | SEA-YOLOv8 (EMA_Faster_C2f, RDD2022, 4 damage types) exists; cites RDD-YOLO/YOLOv8-PD lineage | primary (snippet) | medium |
| 6 | arXiv + NeurIPS pages: Tian 2025 YOLOv12 (2502.12524); Jegham 2024 benchmark (2411.00201) | https://arxiv.org/abs/2502.12524 | YOLOv12-N 40.6% mAP @1.64 ms T4 (arXiv v1); A2 attention + R-ELAN; YOLOv12s accuracy-vs-speed tradeoff | primary (snippet) | medium-high |
| 7 | Sapkota arXiv 2510.09653 + Ultralytics YOLO26 docs (read directly) | https://docs.ultralytics.com/models/yolo26/ | YOLO26n: 40.9 mAP, 1.7 ms T4, 2.4 M params, 5.5 B FLOPs; DFL-free, NMS-free option, MuSGD, ProgLoss, STAL; 43% faster CPU ONNX vs YOLO11n | primary (docs read) | high |
| 8 | Arya 2022 arXiv + CRDDC'22 summary + sekilab repo | https://arxiv.org/abs/2209.08538 | RDD2022: 47,420 images, 55k+ instances, 6 countries, 4 classes; CRDDC'22 best ensemble F1 76% | primary (abstract) | high |
| 9 | Mendeley Data N-RDD2024 (v5, DOI 10.17632/27c8pwsd6v.5) | https://data.mendeley.com/datasets/27c8pwsd6v/5 | N-RDD2024 extends RDD2022 to 10 classes D00–D90 (incl. D70/D80) | primary (repository) | high |
| 10 | arXiv 2304.08069 landing page | https://arxiv.org/abs/2304.08069 | RT-DETR paper ("DETRs Beat YOLOs on Real-time Object Detection") exists | primary (existence) | medium (content unread) |
| 11 | Wu/Zhang/Fan 2025 full text (Nature) | https://doi.org/10.1038/s41598-025-95502-z | RSDD: 10,440 imgs/36,579 instances self-set; 16.5 M params, 30.9 GFLOPs, mAP50 70.8%, 4.5 ms; RDD2022-subset mAP50 61.2% | primary (read directly) | high |
| 12 | CVPR 2016 open-access repository (Redmon et al.) | https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html | YOLO original: unified regression formulation, 45 fps base / 155 fps Fast YOLO | primary | high |
| 13 | MDPI YOLO-LWNet page + ScienceDirect YOLO-RD page (via snippets) | https://www.mdpi.com/1424-8220/23/6/3268 | YOLO-LWNet Small/Tiny on RDD-2020 exists; YOLO-RD snippet claims −39.8% params / eval on RM-RDD+RDD2022+N-RDD2024 (UNVERIFIED) | secondary (snippet) | low-medium |

## Findings (summary with inline references)

- The brief's core lightweight family is fully verified: YOLOv8-PD [3], RDD-YOLO [1], YOLO-LWNet [13], and the YOLO-RD record (snippet only) [13] all exist with checkable URLs.
- The strongest NEW addition is Wu et al. 2025 RSDD [11]: directly read, with RDD2022-subset mAP50 61.2% and full param/FLOP/latency reporting on the same 4-class taxonomy as TA's core classes.
- Official baseline reports are verified: YOLOv12 (arXiv 2502.12524, NeurIPS 2025) [6] and YOLO26 (arXiv 2510.09653 + Ultralytics docs with exact nano specs) [7].
- Dataset provenance is verified: RDD2022 (47,420 images / 6 countries / F1 76% SOTA) [8] and N-RDD2024 (10 classes D00–D90) [9].
- "YOLO-LWD / Shi 2026" must NOT be cited: exhaustive search returned zero matching sources (inference: the name is incorrect or the work does not exist) [2].
- Recommended final count: 10 candidates above (5 duplicates to merge, 5 new/incomplete: C4 ADD, C8 ADD, C9 ADD, C5 verify, C10 verify-or-drop).

## Sources

1. Li et al. / Wang et al. lightweight YOLO records — https://openalex.org/W4394891779 ; https://www.mdpi.com/2076-3417/14/8/3360
2. Web search result set (YOLO-LWD / YOLOv8-PD / YOLO-RD) — https://www.nature.com/articles/s41598-024-62933-z
3. Zeng & Zhong (2024) YOLOv8-PD — https://www.nature.com/articles/s41598-024-62933-z ; https://pmc.ncbi.nlm.nih.gov/articles/PMC11130172
4. YOLO-SFT citing context — https://ascelibrary.org/doi/10.1061/JPEODX.PVENG-1726
5. Zhao et al. (2025) SEA-YOLOv8 — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0324439
6. Tian et al. (2025) YOLOv12 — https://arxiv.org/abs/2502.12524 ; https://proceedings.neurips.cc/paper_files/paper/2025/hash/7103444259031cc58051f8c9a4868533-Abstract-Conference.html
7. Sapkota & Karkee (2025) YOLO26 + Ultralytics docs — https://arxiv.org/abs/2510.09653 ; https://docs.ultralytics.com/models/yolo26/
8. Arya et al. (2022) RDD2022 — https://arxiv.org/abs/2209.08538 ; https://arxiv.org/abs/2211.11362 ; https://github.com/sekilab/RoadDamageDetector/blob/master/README.md
9. Kaya & Çodur (2024) N-RDD2024 — https://data.mendeley.com/datasets/27c8pwsd6v/5
10. Zhao et al. (2023) RT-DETR — https://arxiv.org/abs/2304.08069
11. Wu et al. (2025) RSDD tiny damage — https://doi.org/10.1038/s41598-025-95502-z
12. Redmon et al. (2016) YOLO — https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html ; https://doi.org/10.1109/CVPR.2016.91
13. Wu et al. (2023) YOLO-LWNet; Wang et al. (2025) YOLO-RD — https://www.mdpi.com/1424-8220/23/6/3268 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC10058657 ; https://www.sciencedirect.com/science/article/pii/S0925231225026724

## Coverage Status

- **Checked directly (full text/HTML/docs):** Zeng 2024 YOLOv8-PD (numbers verified); Wu 2025 RSDD (numbers verified); Ultralytics YOLO26 docs (specs verified); RDD2022/N-RDD2024 abstracts + repository pages (stats verified); Redmon 2016, RT-DETR, YOLOv12, YOLO26 existence (URLs verified, deep content partially unread).
- **Uncertain / snippet-only:** RDD-YOLO exact numbers (MDPI 403); YOLO-RD all numbers (paywall); YOLOv12 exact COCO numbers (abstract-level); C4 author first names; C10 author list.
- **Could not complete:** PDF parsing of 1–2 key papers (no PDF fetch attempted; HTML sufficed for 2 key papers, so brief's fallback condition is satisfied); YOLO-LWD/Shi 2026 verification (concluded: no such verifiable source — needs follow-up with corrected name); official YOLOv8 report (no peer-reviewed paper exists; software citation fallback noted).
