# T3 — Imbalance, loss, distractor FPs, small objects: candidate references

## Search terms used (exact)
1. `Focal Loss dense object detection RetinaNet` (semanticscholar)
2. `Class-Balanced Loss Effective Number of Samples Cui` (semanticscholar — 0 hits) + `Class-Balanced Loss Based on Effective Number of Samples CVPR 2019` (crossref) + `Class-Balanced Loss Effective Number Samples arXiv 1901.05555 Cui` (web)
3. `Generalized Focal Loss GFL object detection quality focal loss` (semanticscholar)
4. `road damage detection pothole crack YOLO class imbalance` (semanticscholar)
5. `small object detection COCO mAP small multiscale feature pyramid` (openalex fallback)
6. `manhole pothole detection false positive road damage` (openalex fallback)
7. `Varifocal loss dense object detection Zhang` (openalex) + `VarifocalNet rank dense object detectors CVPR 2021` (crossref) + `VarifocalNet IoU-aware dense object detector arXiv Zhang Wang Dayoub` (web)
8. `Refined Generalized Focal Loss REG road damage detection` (web)
9. `Global Road Damage Detection Challenge GRDDC dataset manhole class` (web) + `Global Road Damage Detection Challenge dataset smartphone images Arya` (openalex)
10. `COCO small object AP definition area thresholds small medium large` (web)
11. `Microsoft COCO Common Objects Context Lin ECCV 2014` (crossref) + `Microsoft COCO Common Objects Context arXiv 1405.0312` (web)
12. `manhole pothole misclassification false positive road damage detection` (web)
13. `YOLOv8-PD improved road damage detection small objects LSKA 2024 Scientific Reports` (web)

Note: Semantic Scholar rate-limited (HTTP 429) partway; fell back to OpenAlex/Crossref/web per routing rules. Full text read directly for 2 key papers via arXiv HTML: Lin et al. 1708.02002 (Focal Loss) and Li et al. 2006.04388 (GFL). REG repo README fetched directly. All other claims from abstracts/metadata/official pages — marked accordingly. PDF parsing NOT attempted beyond HTML; mark as not-blocked (HTML sufficed).

---

## Candidate list

### C1. Focal Loss for Dense Object Detection — Lin et al., ICCV 2017 (TPAMI 2020 journal version)
- Title: Focal Loss for Dense Object Detection
- Authors: Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, Piotr Dollár
- Venue + year: Proc. IEEE Int. Conf. on Computer Vision (ICCV) 2017; journal version IEEE TPAMI 2020
- DOI / arXiv + URL: DOI 10.1109/ICCV.2017.324 — https://doi.org/10.1109/ICCV.2017.324 ; arXiv 1708.02002 — https://arxiv.org/abs/1708.02002 ; HTML read: https://arxiv.org/html/1708.02002
- Findings (read directly, HTML): Diagnoses extreme foreground–background imbalance (~1:1000) as the central cause of one-stage detector lag; proposes modulating factor (1−pt)^γ on cross-entropy with γ=2 best, plus α-balanced variant and foreground prior π=0.01 init for stability [1][2]. RetinaNet with ResNet-101-FPN reaches 39.1 COCO test-dev AP at ~5 fps, surpassing prior one-/two-stage results; γ=2 makes a pt=0.9 example ~100× lower loss than CE and pt≈0.968 ~1000× lower (verified from §3.2 text) [1][2].
- Fits TA section: Ch.2 loss-function foundation + justifying focal-family choice for 9.67× patchy_road/longitudinal imbalance and dense small-box sampling — cite in imbalance/loss subsection.
- BibTeX:
```bibtex
@inproceedings{lin2017focal,
  title={Focal Loss for Dense Object Detection},
  author={Lin, Tsung-Yi and Goyal, Priya and Girshick, Ross and He, Kaiming and Doll{\'a}r, Piotr},
  booktitle={Proc. IEEE Int. Conf. Comput. Vis. (ICCV)},
  pages={2980--2988},
  year={2017},
  doi={10.1109/ICCV.2017.324}
}
```
- Duplicate vs existing: NEW (foundational; not in existing TA bib per brief).

### C2. Class-Balanced Loss Based on Effective Number of Samples — Cui et al., CVPR 2019
- Title: Class-Balanced Loss Based on Effective Number of Samples
- Authors: Yin Cui, Menglin Jia, Tsung-Yi Lin, Yang Song, Serge Belongie
- Venue + year: Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) 2019
- DOI / arXiv + URL: DOI 10.1109/CVPR.2019.00949 — https://doi.org/10.1109/CVPR.2019.00949 ; arXiv 1901.05555 — https://arxiv.org/abs/1901.05555 ; IEEE page: https://ieeexplore.ieee.org/document/8953804
- Findings (abstract/metadata + search-verified abstract text): Defines effective number En=(1−β^n)/(1−β) to model diminishing marginal benefit of extra samples via data overlap; re-weighting factor (1−β)/(1−β^ny) applied to softmax/sigmoid/focal losses [3][4]. Validated on artificially long-tailed CIFAR plus ImageNet and iNaturalist with significant gains on long-tailed splits (exact per-dataset deltas not extracted — only abstract-level claim verified) [3][4].
- Fits TA section: Direct theoretical grounding for the TA's own β=0.999 class-balanced weighting (patchy_road 672 vs longitudinal 6447) — cite in methods/imbalance handling.
- BibTeX:
```bibtex
@inproceedings{cui2019class,
  title={Class-Balanced Loss Based on Effective Number of Samples},
  author={Cui, Yin and Jia, Menglin and Lin, Tsung-Yi and Song, Yang and Belongie, Serge},
  booktitle={Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)},
  pages={9268--9277},
  year={2019},
  doi={10.1109/CVPR.2019.00949}
}
```
- Duplicate vs existing: DUPLICATE — already have `cui2019class` per brief; keep existing key, use this entry only to verify DOI/arXiv metadata.

### C3. Generalized Focal Loss — Li et al., NeurIPS 2020
- Title: Generalized Focal Loss: Learning Qualified and Distributed Bounding Boxes for Dense Object Detection
- Authors: Xiang Li, Wenhai Wang, Lijun Wu, Shuo Chen, Xiaolin Hu, Jun Li, Jin-Hui Tang, Jian Yang
- Venue + year: Adv. Neural Inf. Process. Syst. (NeurIPS) 2020, pp. 21002–21012
- DOI / arXiv + URL: arXiv 2006.04388 — https://arxiv.org/abs/2006.04388 ; HTML read: https://arxiv.org/html/2006.04388 ; ACM proceedings page: https://dl.acm.org/doi/10.5555/3495724.3497487
- Findings (read directly, HTML): Merges classification + IoU quality into a joint "classification–IoU" vector supervised with continuous 0–1 labels, and models box edges as a learned general discrete distribution instead of Dirac delta; both need continuous-label loss [5][6]. Proposes QFL (modulator |y−σ|^β, β=2 best) and DFL (cross-entropy on nearest bins yi, yi+1), unified as GFL; QFL gives +0.6–0.8 AP on several one-stage detectors at zero inference overhead; GFL/ATSS-ResNet-101 reaches 45.0% COCO AP, best single-scale single-model 48.2% at 10 fps on 2080Ti (verified from abstract + §3–4 text) [5][6].
- Fits TA section: Bridges focal loss → quality-aware losses (QFL/DFL) motivating REG and Varifocal alternatives for ambiguous pothole/patch boundaries — cite in loss-function comparison subsection.
- BibTeX:
```bibtex
@inproceedings{li2020generalized,
  title={Generalized Focal Loss: Learning Qualified and Distributed Bounding Boxes for Dense Object Detection},
  author={Li, Xiang and Wang, Wenhai and Wu, Lijun and Chen, Shuo and Hu, Xiaolin and Li, Jun and Tang, Jin-Hui and Yang, Jian},
  booktitle={Adv. Neural Inf. Process. Syst. (NeurIPS)},
  volume={33},
  pages={21002--21012},
  year={2020},
  eprint={2006.04388},
  archiveprefix={arXiv}
}
```
- Duplicate vs existing: NEW.

### C4. VarifocalNet — Zhang et al., CVPR 2021 (oral)
- Title: VarifocalNet: An IoU-aware Dense Object Detector
- Authors: Haoyang Zhang, Ying Wang, Feras Dayoub, Niko Sünderhauf
- Venue + year: Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) 2021 (oral)
- DOI / arXiv + URL: DOI 10.1109/CVPR46437.2021.00841 — https://doi.org/10.1109/CVPR46437.2021.00841 ; arXiv 2008.13367 — https://arxiv.org/abs/2008.13367 ; CVF open access PDF: https://openaccess.thecvf.com/content/CVPR2021/papers/Zhang_VarifocalNet_An_IoU-Aware_Dense_Object_Detector_CVPR_2021_paper.pdf
- Findings (abstract/metadata level; full text not fetched): Learns IoU-aware Classification Score (IACS) merging object presence + localization accuracy to fix candidate-ranking misalignment in dense detectors; new Varifocal Loss + star-shaped box feature + refinement branch on FCOS+ATSS [7][8]. Reported ~2.0 AP gain over strong baseline across backbones; best VFNet-X-1200/Res2Net-101-DCN 55.1 single-model single-scale AP on COCO test-dev (abstract-level numbers, not independently re-verified) [7][8].
- Fits TA section: Alternative quality-aware loss head for hard pothole-vs-background ranking and small-object NMS ordering — cite alongside GFL/REG in loss ablation discussion.
- BibTeX:
```bibtex
@inproceedings{zhang2021varifocalnet,
  title={VarifocalNet: An IoU-aware Dense Object Detector},
  author={Zhang, Haoyang and Wang, Ying and Dayoub, Feras and S{\"u}nderhauf, Niko},
  booktitle={Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)},
  pages={8516--8525},
  year={2021},
  doi={10.1109/CVPR46437.2021.00841}
}
```
- Duplicate vs existing: NEW.

### C5. REG: Refined Generalized Focal Loss — Panboonyuen, IEEE KST 2025
- Title: REG: Refined Generalized Focal Loss for Road Asset Detection on Thai Highways Using Vision-Based Detection and Segmentation Models (repo title variant: "…Using Vision Models")
- Authors: Teerapong Panboonyuen
- Venue + year: 17th Int. Conf. on Knowledge and Smart Technology (KST) 2025, pp. 324–329, IEEE
- DOI / arXiv + URL: IEEE https://ieeexplore.ieee.org/document/11003314/ ; arXiv 2409.09877 — https://arxiv.org/abs/2409.09877 ; code https://github.com/kaopanboonyuen/REG ; project page https://kaopanboonyuen.github.io/REG ; explainer https://kaopanboonyuen.github.io/blog/2024-09-07-refined-generalized-focal-loss-for-road-asset-detection-on-thai-highways-using-vision-models/
- Findings (repo README read directly; paper full text NOT read): Self-reported mAP@50 = 80.34, F1 = 77.87 on Thai highway data; combines focal loss + spatial refinement + probabilistic uncertainty in a multi-task detection+segmentation PyTorch codebase (Dockerized; train `python src/train.py --data-path ./data/ --batch 8 --epochs 50 --lr 1e-4`), claimed to beat focal baselines under glare/occlusion/rare classes [9]. Treat all performance numbers as self-reported/unverified until the IEEE/arXiv paper text is read.
- Fits TA section: Only road-domain focal-loss refinement found; directly relevant to rare-asset road damage loss choice and Thai-highway domain transfer — cite in domain-specific loss subsection; ADD TO IEEE BIB (missing per brief).
- BibTeX (repo-given; normalize title casing when inserting):
```bibtex
@inproceedings{panboonyuen2025reg,
  title={{REG: Refined Generalized Focal Loss for Road Asset Detection on Thai Highways Using Vision Models}},
  author={Panboonyuen, Teerapong},
  booktitle={Proc. 17th Int. Conf. Knowl. Smart Technol. (KST)},
  pages={324--329},
  year={2025},
  organization={IEEE}
}
```
- Duplicate vs existing: DUPLICATE (cited in proposal, missing from IEEE bib) — action is to ADD, not re-discover.

### C6. Microsoft COCO — Lin et al., ECCV 2014 (mAP-s/m/l metric definitions)
- Title: Microsoft COCO: Common Objects in Context
- Authors: Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, C. Lawrence Zitnick
- Venue + year: Proc. Eur. Conf. Comput. Vis. (ECCV) 2014
- DOI / arXiv + URL: DOI 10.1007/978-3-319-10602-1_48 — https://doi.org/10.1007/978-3-319-10602-1_48 ; arXiv 1405.0312 — https://arxiv.org/abs/1405.0312
- Findings (metadata level; thresholds are community-standard, re-verify from COCO eval docs before citing numbers): 328K images / 2.5M instances / 91 categories with 82 having >5,000 instances; 7.7 instances per image vs 3.0 ImageNet / 2.3 PASCAL (verified from arXiv page text) [10][11]. Standard scale split used for mAP-S/M/L (small: area < 32², medium: 32²–96², large: > 96²) — well-known but NOT re-verified from the official eval protocol in this pass, so confirm at write-up time.
- Fits TA section: Normative citation for multi-scale mAP evaluation (mAP-S/M/L) given TA median box 1.69% image area (small-object regime) — cite in metrics/evaluation subsection.
- BibTeX:
```bibtex
@inproceedings{lin2014microsoft,
  title={{Microsoft COCO: Common Objects in Context}},
  author={Lin, Tsung-Yi and Maire, Michael and Belongie, Serge and Hays, James and Perona, Pietro and Ramanan, Deva and Doll{\'a}r, Piotr and Zitnick, C. Lawrence},
  booktitle={Proc. Eur. Conf. Comput. Vis. (ECCV)},
  pages={740--755},
  year={2014},
  doi={10.1007/978-3-319-10602-1_48}
}
```
- Duplicate vs existing: NEW (likely; metric-definition citation).

### C7. RDD2020 / RDD2022 — Arya et al., Data in Brief 2021 / arXiv 2022 (GRDDC dataset + imbalance context)
- Title: RDD2020: An annotated image dataset for automatic road damage detection using deep learning (2021); RDD2022: A multi-national image dataset for automatic Road Damage Detection (2022)
- Authors: Deeksha Arya, Hiroya Maeda, Sanjay Kumar Ghosh, Durga Toshniwal, Yoshihide Sekimoto (+ CRDDC collaborators on RDD2022)
- Venue + year: Data in Brief, vol. 36, 107133, 2021; arXiv preprint 2022 (RDD2022)
- DOI / arXiv + URL: DOI 10.1016/j.dib.2021.107133 — https://doi.org/10.1016/j.dib.2021.107133 ; arXiv 2209.08538 — https://arxiv.org/abs/2209.08538 ; RDD2022 OA PDF: https://arxiv.org/pdf/2209.08538
- Findings (metadata level): RDD2020 multi-country smartphone-image road-damage dataset underlying the Global Road Damage Detection Challenge (GRDDC 2020); RDD2022 extends to multiple nations; cited 241× (RDD2020) / 86× (RDD2022) per OpenAlex [12]. Label taxonomy and per-class counts NOT extracted — check dataset paper/card before citing crack/pothole/manhole distributions.
- Fits TA section: Dataset lineage + challenge benchmark context for class-imbalance and cross-country generalization discussion — cite in dataset subsection.
- BibTeX:
```bibtex
@article{arya2021rdd2020,
  title={{RDD2020: An annotated image dataset for automatic road damage detection using deep learning}},
  author={Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Sekimoto, Yoshihide},
  journal={Data in Brief},
  volume={36},
  pages={107133},
  year={2021},
  doi={10.1016/j.dib.2021.107133}
}
@misc{arya2022rdd2022,
  title={{RDD2022: A multi-national image dataset for automatic Road Damage Detection}},
  author={Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Sekimoto, Yoshihide},
  year={2022},
  eprint={2209.08538},
  archiveprefix={arXiv},
  url={https://arxiv.org/abs/2209.08538}
}
```
- Duplicate vs existing: NEW (dataset; complements Zeng2024-style YOLO road papers).

### C8. YOLOv8-PD — Zeng & Zhong (Han), Scientific Reports 2024 (small-object road damage recipe)
- Title: YOLOv8-PD: an improved road damage detection algorithm based on YOLOv8n model
- Authors: Jiayi Zeng, Han Zhong
- Venue + year: Scientific Reports, vol. 14, art. 12052, 2024
- DOI / URL: DOI 10.1038/s41598-024-62933-z — https://doi.org/10.1038/s41598-024-62933-z ; PubMed: https://pubmed.ncbi.nlm.nih.gov/38802524 ; PDF: https://www.nature.com/articles/s41598-024-62933-z.pdf
- Findings (abstract + secondary-report level; full text NOT read): YOLOv8n-based lightweight detector adding BOT global-context module for long-span cracks, Large Separable Kernel Attention (LSKA) for accuracy, C2fGhost neck for efficiency, and LSCD-Head retaining small-object detection; compares vs Faster/Cascade R-CNN, YOLOv3-tiny/v4-tiny/v5n/s/l, YOLOv7, YOLOv8n, YOLOv8-RD [13][14]. A related low-compute YOLOv8 pavement-distress variant reports pothole AP@0.5 53.4%→75.5% and strip-patch 52.1%→69.8% via LSKA+DIoU+Soft-NMS — DIFFERENT paper (Sensors 2025), do not conflate with YOLOv8-PD numbers [14].
- Fits TA section: Applied recipe for the TA's exact pain points (multi-scale cracks + small potholes + lightweight deployment) — cite in small-object/architecture subsection.
- BibTeX:
```bibtex
@article{zeng2024yolov8pd,
  title={{YOLOv8-PD: an improved road damage detection algorithm based on YOLOv8n model}},
  author={Zeng, Jiayi and Zhong, Han},
  journal={Sci. Rep.},
  volume={14},
  pages={12052},
  year={2024},
  doi={10.1038/s41598-024-62933-z}
}
```
- Duplicate vs existing: POSSIBLE DUPLICATE of brief's "Zeng2024 (Focal/Mosaic)" — verify whether brief's Zeng2024 is this paper or a different Zeng; if same, keep one key.

### C9. Pothole detection under challenging conditions — Bučko et al., Sensors 2022 (manhole-vs-pothole FP evidence)
- Title: Computer Vision Based Pothole Detection under Challenging Conditions
- Authors: Boris Bučko, Eva Lieskovská, Katarína Zábovská, Michal Zábovský
- Venue + year: Sensors, vol. 22, no. 22, 8878, 2022
- DOI / URL: DOI 10.3390/s22228878 — https://doi.org/10.3390/s22228878 ; PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9694379
- Findings (search-snippet + abstract level; full text NOT read): Explicitly added a manhole-cover class because "round nature of manhole covers may be somewhat similar to the shape of potholes and therefore misclassification can occur"; 1,052 clear-weather images; YOLOv3-SPP (1080×1080) mAP@0.5 up to 0.791 multi-class; manhole "more easily recognized compared to potholes"; rain spots/wet-road reflections, car-hood reflections, small cracks/dark spots falsely detected as potholes; night worst, larger input helps [15].
- Fits TA section: Only explicit manhole-as-distractor FP study found — directly supports the TA 6-class vs 4-class ablation and explains manhole-easy (0.82–0.85) vs pothole-hard (0.526–0.541) pattern — cite in distractor/negative-class + error-analysis subsection.
- BibTeX:
```bibtex
@article{bucko2022computer,
  title={{Computer Vision Based Pothole Detection under Challenging Conditions}},
  author={Bu{\v{c}}ko, Boris and Lieskovsk{\'a}, Eva and Z{\'a}bovsk{\'a}, Katar{\'\i}na and Z{\'a}bovsk{\'y}, Michal},
  journal={Sensors},
  volume={22},
  number={22},
  pages={8878},
  year={2022},
  doi={10.3390/s22228878}
}
```
- Duplicate vs existing: NEW.

---

## Evidence table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Lin et al., Focal Loss (ICCV 2017; arXiv HTML) | https://arxiv.org/html/1708.02002 | γ=2 focal loss + α-balance + prior init; RetinaNet-101-FPN 39.1 COCO AP | primary (read directly) | high |
| 2 | Lin et al., Focal Loss (S2 metadata: DOI, venue, citations) | https://doi.org/10.1109/ICCV.2017.324 | Venue/year/DOI/citation count triangulation | secondary (metadata) | high |
| 3 | Cui et al., Class-Balanced Loss (Crossref + arXiv abstract) | https://doi.org/10.1109/CVPR.2019.00949 / https://arxiv.org/abs/1901.05555 | En=(1−β^n)/(1−β); loss-agnostic re-weighting; gains on long-tailed CIFAR/ImageNet/iNat | secondary (abstract/metadata) | medium |
| 4 | IEEE Xplore page for Cui et al. 2019 | https://ieeexplore.ieee.org/document/8953804 | Confirms CVPR 2019 venue, authors, DOI | secondary (metadata) | high |
| 5 | Li et al., GFL (NeurIPS 2020; arXiv HTML) | https://arxiv.org/html/2006.04388 | QFL/DFL formulation; β=2; 45.0% AP R-101, 48.2% best single-scale | primary (read directly) | high |
| 6 | Li et al., GFL (ACM proceedings page) | https://dl.acm.org/doi/10.5555/3495724.3497487 | Confirms NeurIPS'20 pp. 21002–21012 | secondary (metadata) | high |
| 7 | Zhang et al., VarifocalNet (arXiv abs + CVF PDF) | https://arxiv.org/abs/2008.13367 / https://openaccess.thecvf.com/content/CVPR2021/papers/Zhang_VarifocalNet_An_IoU-Aware_Dense_Object_Detector_CVPR_2021_paper.pdf | IACS + Varifocal Loss; ~2.0 AP gain; 55.1 best COCO AP | secondary (abstract) | medium |
| 8 | Zhang et al., VarifocalNet (Crossref) | https://doi.org/10.1109/CVPR46437.2021.00841 | Confirms CVPR 2021 venue/authors/DOI | secondary (metadata) | high |
| 9 | Panboonyuen REG repo README (read directly) | https://github.com/kaopanboonyuen/REG | mAP50 80.34 / F1 77.87 (self-reported); focal+spatial+uncertainty; train command | self-reported (primary for code, unverified for metrics) | low–medium |
| 10 | Lin et al., COCO (Crossref + arXiv) | https://doi.org/10.1007/978-3-319-10602-1_48 / https://arxiv.org/abs/1405.0312 | ECCV 2014; 328K imgs / 2.5M instances / 91 cats; 7.7 inst/img | secondary (metadata) | medium–high |
| 11 | Arya et al., RDD2020 (OpenAlex/Data in Brief) | https://doi.org/10.1016/j.dib.2021.107133 | Multi-country smartphone road-damage dataset; GRDDC basis; 241 cites | secondary (metadata) | medium |
| 12 | Arya et al., RDD2022 (arXiv) | https://arxiv.org/abs/2209.08538 | Multi-national extension; OA PDF available | secondary (metadata) | medium |
| 13 | Zeng & Zhong, YOLOv8-PD (Sci Rep 2024) | https://www.nature.com/articles/s41598-024-62933-z | YOLOv8n + BOT + LSKA + C2fGhost + LSCD-Head for multi-scale distress | secondary (abstract) | medium |
| 14 | YOLOv8 pavement-distress low-compute variant (Sensors) | https://www.mdpi.com/1424-8220/26/11/3373 | LSKA+DIoU+Soft-NMS pothole AP 53.4→75.5 (DIFFERENT paper — do not conflate) | secondary (snippet) | low–medium |
| 15 | Bučko et al., pothole under challenging conditions (Sensors/PMC) | https://doi.org/10.3390/s22228878 / https://pmc.ncbi.nlm.nih.gov/articles/PMC9694379 | Manhole class added as pothole distractor; YOLOv3-SPP mAP@0.5 ≤0.791; manhole easier than pothole | secondary (snippet/abstract) | medium |

## Findings (with inline refs)

- Focal loss is the established fix for dense-detector foreground–background imbalance, with the exact γ=2 / α-balance / prior-init recipe verified from the source text [1][2].
- Class-balanced re-weighting by inverse effective number of samples is loss-agnostic (softmax/sigmoid/focal) and is the direct theory behind the TA's β=0.999 weighting [3][4].
- GFL generalizes focal loss to continuous quality labels via QFL (|y−σ|^β) and flexible box distributions via DFL, with verified COCO gains at no inference cost [5][6] — inference: this makes GFL/VFL/REG the natural loss-ablation family for ambiguous pothole/patch edges.
- VarifocalNet offers a parallel IoU-aware ranking fix (IACS + Varifocal Loss, ~2 AP gain, abstract-level) [7][8] — inference: candidate head/loss alternative if REG underperforms.
- REG is the only road-domain focal refinement found, but its headline numbers are self-reported from the repo page, not the peer-reviewed text [9] — inference: cite as method, do not lean on 80.34/F1 numbers without reading the KST paper.
- COCO scale-split evaluation (mAP-S/M/L) is the right instrument for the TA's 1.69%-area small-box regime, but the exact pixel thresholds need re-verification against the eval protocol [10][11].
- RDD2020/2022 grounds the GRDDC dataset lineage behind road-damage class-imbalance discussion [12]; YOLOv8-PD gives a small-object road-damage recipe (BOT+LSKA+LSCD-Head) at abstract level [13], kept distinct from a similarly-named Sensors variant [14].
- Manhole-as-distractor has direct published precedent: round manholes mimic potholes, motivating an explicit manhole class, with manholes empirically easier than potholes — matching the TA's 0.82–0.85 vs 0.526–0.541 pattern [15].

## Rejected / duplicates
- Cui et al. 2019 (`cui2019class`): DUPLICATE — already in TA bib; retained only for metadata verification.
- Panboonyuen 2025 REG (`panboonyuen2025reg`): DUPLICATE-in-proposal, MISSING-from-bib — action: insert BibTeX above.
- Brief's "Zeng2024 (Focal/Mosaic)": POSSIBLE DUPLICATE of C8 YOLOv8-PD — verify identity before adding; if same, keep single key.
- Brief's "Shi_2026 / mandals manhole annotation claims": NOT FOUND in this pass — no verifiable URL located; excluded per no-URL rule; needs dedicated follow-up search.
- Lettuce-seedling Faster R-CNN, UAV detection, X-ray baggage papers from the focal-loss S2 query: REJECTED as off-topic (returned only as citation neighbors).
- Generic YOLO surveys / Faster R-CNN / FPN / OHEM / M2Det from the small-object OpenAlex fallback: REJECTED as too generic; COCO (C6) kept as the metric anchor instead.
- FHWA distress manual, YOLO pothole comparative study (IOP), Dhaka polygonal-annotation preprint (arXiv 2510.03797): SEEN but REJECTED for the candidate list (manual = taxonomy not loss; IOP = weak venue; Dhaka preprint = unverified 2025 preprint with anomalous 18.2% manhole F1) — may revisit for error-analysis color only.

## Open questions
1. Is brief's "Zeng2024" identical to YOLOv8-PD (C8)? Needs key reconciliation against the TA .bib.
2. Shi_2026 / mandals manhole-annotation sources: no URL found — needs a dedicated author/title search before any citation.
3. REG paper text (IEEE pp. 324–329 / arXiv 2409.09877) not yet read — loss formula and ablations unverified; claims rest on repo README.
4. COCO mAP-S/M/L pixel thresholds and VarifocalNet/GFL exact numbers rest on abstract-level evidence — re-verify from primary text at write-up time.
5. No dedicated "explicit distractor/negative-class labeling" study beyond Bučko et al. found — consider widening to open-set/background-class detection literature if the TA needs more.

## Sources
1. T.-Y. Lin et al., Focal Loss for Dense Object Detection — https://arxiv.org/html/1708.02002
2. T.-Y. Lin et al., ICCV 2017 (DOI) — https://doi.org/10.1109/ICCV.2017.324
3. Y. Cui et al., Class-Balanced Loss (arXiv) — https://arxiv.org/abs/1901.05555
4. Y. Cui et al., CVPR 2019 (DOI/IEEE) — https://doi.org/10.1109/CVPR.2019.00949 / https://ieeexplore.ieee.org/document/8953804
5. X. Li et al., Generalized Focal Loss (arXiv HTML) — https://arxiv.org/html/2006.04388
6. X. Li et al., NeurIPS'20 proceedings — https://dl.acm.org/doi/10.5555/3495724.3497487
7. H. Zhang et al., VarifocalNet (arXiv) — https://arxiv.org/abs/2008.13367
8. H. Zhang et al., CVPR 2021 (DOI/CVF PDF) — https://doi.org/10.1109/CVPR46437.2021.00841 / https://openaccess.thecvf.com/content/CVPR2021/papers/Zhang_VarifocalNet_An_IoU-Aware_Dense_Object_Detector_CVPR_2021_paper.pdf
9. T. Panboonyuen, REG repo — https://github.com/kaopanboonyuen/REG ; project — https://kaopanboonyuen.github.io/REG ; IEEE — https://ieeexplore.ieee.org/document/11003314/ ; arXiv — https://arxiv.org/abs/2409.09877
10. T.-Y. Lin et al., Microsoft COCO (DOI) — https://doi.org/10.1007/978-3-319-10602-1_48
11. T.-Y. Lin et al., COCO (arXiv) — https://arxiv.org/abs/1405.0312
12. D. Arya et al., RDD2020 / RDD2022 — https://doi.org/10.1016/j.dib.2021.107133 / https://arxiv.org/abs/2209.08538
13. J. Zeng & H. Zhong, YOLOv8-PD, Sci. Rep. 2024 — https://www.nature.com/articles/s41598-024-62933-z
14. Improved YOLOv8 pavement-distress variant, Sensors — https://www.mdpi.com/1424-8220/26/11/3373
15. B. Bučko et al., Sensors 2022 — https://doi.org/10.3390/s22228878 / https://pmc.ncbi.nlm.nih.gov/articles/PMC9694379

## Coverage status
- Checked directly: Focal Loss HTML, GFL HTML, REG repo README, plus metadata for all 9 candidates (each has a checkable URL).
- Uncertain / abstract-level only: VarifocalNet numbers, YOLOv8-PD details, RDD taxonomy/counts, COCO S/M/L thresholds, Bučko details (snippet-level).
- Not completed: Shi_2026/mandals lookup; Zeng2024 identity reconciliation; REG/IEEE full-text read; COCO eval-protocol threshold confirmation. Recommended as follow-ups, not blockers.
