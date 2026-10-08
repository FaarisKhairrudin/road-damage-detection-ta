# T4 — Attention, lightweight conv, real-time efficiency: candidate references

## Search terms used (paper + web, >3 distinct queries)
1. `SimAM simple parameter-free attention module convolutional neural networks` (OpenAlex work-search)
2. `GhostNet cheap operations efficient neural network GhostConv` (OpenAlex work-search)
3. `Deformable Convolutional Networks DCNv2 DCNv3` (OpenAlex work-search)
4. `CBAM convolutional block attention module ECA-Net efficient channel attention` (Semantic Scholar)
5. `openalex_search_works:GhostNet more features from cheap operations` / `:CBAM convolutional block attention module` / `:ECA-Net efficient channel attention deep learning` / `:Deformable convolutional networks Dai` (OpenAlex exact-title mode)
6. Web: `Dai 2017 Deformable Convolutional Networks ICCV arXiv`; `DCNv2 Zhu 2019 deformable convnets v2 arXiv`; `EfficientDet Tan 2020 scalable object detection arXiv`; `YOLOv4 Bochkovskiy 2020 optimal speed accuracy arXiv`
7. Web: `SimAM Yang 2021 parameter-free attention ICML arXiv`; `Redmon 2016 You Only Look Once YOLO arXiv unified real-time detection`; `wavelet convolution object detection YOLO remote sensing`
8. Web: `Bochkovskiy YOLOv4 optimal speed accuracy arXiv 2004.10934`; `YOLOX Ge 2021 anchor-free decoupled head arXiv`; `WTConv wavelet transform convolution Finder ICCV 2024 arXiv`
9. Web: `EfficientDet road damage pothole detection Indonesia study`; `Ultralytics YOLOv8 documentation GFLOPs FPS benchmark methodology`; `YOLOv3 Redmon 2018 incremental improvement arXiv`
10. arXiv abstract pages fetched directly for 1911.11907 (GhostNet), 1807.06521 (CBAM), 1910.03151 (ECA-Net), 1911.09070 (EfficientDet), 2407.05848 (WTConv); Ultralytics performance-metrics guide fetched; Hugo-2025 Indonesia EfficientDet PDF fetched and skimmed. PDF parsing of full papers not attempted beyond abstracts/metadata — marked as blocked/not-done below.

## Candidate list

### C1. SimAM — Yang et al., ICML 2021 (original SimAM paper)
- Title: SimAM: A Simple, Parameter-Free Attention Module for Convolutional Neural Networks
- Authors: Lingxiao Yang, Ru-Yuan Zhang, Lida Li, Xiaohua Xie
- Venue + year: Proc. 38th International Conference on Machine Learning (ICML), PMLR 139, pp. 11863–11874, 2021 [1]
- DOI/arXiv + URL: no arXiv ID (ICML proceedings paper); canonical URL https://proceedings.mlr.press/v139/yang21o.html ; PDF https://proceedings.mlr.press/v139/yang21o/yang21o.pdf [1]
- Findings (3 sents): In contrast to channel-wise/spatial-wise attention, SimAM infers 3-D attention weights per feature map with zero added parameters, deriving a fast closed-form solution from a neuroscience-inspired energy function implementable in under ten lines of code [1]. The module is positioned as plug-and-play and structure-tuning-free, with most operators determined by the energy-function solution rather than manual design [1]. Quantitative evaluations on various visual tasks are reported to show flexible, effective gains in representation ability across many ConvNets (exact per-task numbers not extracted — abstract only) [1].
- Fits TA Section: neck-attention modifications (SimAM insertion adds no Params/GFLOPs) — cite in the attention-mechanism subsection and in the Params/GFLOPs/FPS cost discussion because it is the zero-parameter attention baseline vs CBAM.
- BibTeX:
```bibtex
@inproceedings{yang2021simam,
  author    = {Yang, Lingxiao and Zhang, Ru-Yuan and Li, Lida and Xie, Xiaohua},
  title     = {SimAM: A Simple, Parameter-Free Attention Module for Convolutional Neural Networks},
  booktitle = {Proceedings of the 38th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {139},
  pages     = {11863--11874},
  year      = {2021},
  url       = {https://proceedings.mlr.press/v139/yang21o.html}
}
```
- Duplicate-vs-existing: NEW (not in existing bib; complements han2020ghostnet/woo2018cbam already cited in proposal).

### C2. GhostNet — Han et al., CVPR 2020 (GhostConv original)
- Title: GhostNet: More Features From Cheap Operations
- Authors: Kai Han, Yunhe Wang, Qi Tian, Jianyuan Guo, Chunjing Xu, Chang Xu
- Venue + year: IEEE/CVF CVPR 2020, pp. 1577–1586; preprint arXiv:1911.11907 [2][3]
- DOI/arXiv + URL: DOI 10.1109/CVPR42600.2020.00165; arXiv https://arxiv.org/abs/1911.11907 ; code https://github.com/huawei-noah/ghostnet [2][3]
- Findings (3 sents): The Ghost module generates extra "ghost" feature maps from cheap linear transforms of a small set of intrinsic maps and is presented as a plug-and-play replacement for standard convolution layers, with stacked Ghost bottlenecks forming GhostNet [3]. On ImageNet ILSVRC-2012 the authors report GhostNet reaching 75.7% top-1 accuracy at a computational cost similar to MobileNetV3 [3]. OpenAlex records ~4,778 citations to the CVPR version, marking it the canonical lightweight-conv reference [2].
- Fits TA Section: YOLOv8-PD efficiency branch (GhostConv in neck/backbone, 2.46M params / 7.7 GFLOPs / 368 FPS narrative) — the first-principles citation for why GhostConv cuts FLOPs.
- BibTeX:
```bibtex
@inproceedings{han2020ghostnet,
  author    = {Han, Kai and Wang, Yunhe and Tian, Qi and Guo, Jianyuan and Xu, Chunjing and Xu, Chang},
  title     = {GhostNet: More Features From Cheap Operations},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {1577--1586},
  year      = {2020},
  doi       = {10.1109/CVPR42600.2020.00165},
  eprint    = {1911.11907},
  archiveprefix = {arXiv}
}
```
- Duplicate-vs-existing: LIKELY DUPLICATE — han2020ghostnet is already cited in the proposal but missing from the IEEE bib; use this entry to complete that bib record.

### C3. CBAM — Woo et al., ECCV 2018 (CBAM original)
- Title: CBAM: Convolutional Block Attention Module
- Authors: Sanghyun Woo, Jongchan Park, Joon-Young Lee, In So Kweon
- Venue + year: ECCV 2018 (LNCS); preprint arXiv:1807.06521 [4][5]
- DOI/arXiv + URL: DOI 10.1007/978-3-030-01234-2_1; arXiv https://arxiv.org/abs/1807.06521 [4][5]
- Findings (3 sents): CBAM sequentially infers channel and spatial attention maps from an intermediate feature map and multiplies them back for adaptive refinement, designed as a lightweight general module integrable into any CNN with negligible overhead and end-to-end training [5]. Validation is reported on ImageNet-1K, MS-COCO detection, and VOC 2007 detection with consistent classification/detection gains across backbone models (exact deltas not extracted — abstract only) [5]. OpenAlex records ~23,794 citations, making it the standard channel+spatial attention citation [4].
- Fits TA Section: neck-attention modifications (CBAM insertion) — the parameterized-attention counterpart to SimAM; pair C1+C3 when reporting the attention ablation's Params/GFLOPs/FPS delta.
- BibTeX:
```bibtex
@inproceedings{woo2018cbam,
  author    = {Woo, Sanghyun and Park, Jongchan and Lee, Joon-Young and Kweon, In So},
  title     = {{CBAM}: Convolutional Block Attention Module},
  booktitle = {Proceedings of the European Conference on Computer Vision (ECCV)},
  pages     = {3--19},
  year      = {2018},
  doi       = {10.1007/978-3-030-01234-2_1},
  eprint    = {1807.06521},
  archiveprefix = {arXiv}
}
```
- Duplicate-vs-existing: LIKELY DUPLICATE — woo2018cbam already cited in proposal but missing from IEEE bib; use this entry to complete that record.

### C4. ECA-Net — Wang et al., CVPR 2020 (efficient channel attention)
- Title: ECA-Net: Efficient Channel Attention for Deep Convolutional Neural Networks
- Authors: Qilong Wang, Banggu Wu, Pengfei Zhu, Peihua Li, Wangmeng Zuo, Qinghua Hu
- Venue + year: IEEE/CVF CVPR 2020, pp. 11531–11539; preprint arXiv:1910.03151 [6][7]
- DOI/arXiv + URL: DOI 10.1109/CVPR42600.2020.01155; arXiv https://arxiv.org/abs/1910.03151 ; project https://github.com/BangguWu/ECANet [6][7]
- Findings (4 sents): ECA avoids the dimensionality-reduction side effect of SE-style channel attention and instead uses local cross-channel interaction implemented efficiently via 1-D convolution with an adaptively selected kernel size [7]. The efficiency claim is explicit: the ECA module adds only ~80 parameters and ~4.7e-4 GFLOPs against a ResNet-50 backbone (24.37M params, 3.86 GFLOPs) while boosting Top-1 accuracy by more than 2% [7]. Evaluation spans image classification, object detection, and instance segmentation on ResNets and MobileNetV2, reported as favorable vs counterparts at lower complexity [7]. OpenAlex records ~8,787 citations to the CVPR version [6].
- Fits TA Section: attention-mechanism background and efficiency framing — ECA is the "avoid dimensionality reduction + 1-D conv" design precedent that motivates cheap attention in a real-time detector neck.
- BibTeX:
```bibtex
@inproceedings{wang2020eca,
  author    = {Wang, Qilong and Wu, Banggu and Zhu, Pengfei and Li, Peihua and Zuo, Wangmeng and Hu, Qinghua},
  title     = {{ECA-Net}: Efficient Channel Attention for Deep Convolutional Neural Networks},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {11531--11539},
  year      = {2020},
  doi       = {10.1109/CVPR42600.2020.01155},
  eprint    = {1910.03151},
  archiveprefix = {arXiv}
}
```
- Duplicate-vs-existing: NEW.

### C5. Deformable ConvNets v1 — Dai et al., ICCV 2017 (deformable convolution original)
- Title: Deformable Convolutional Networks
- Authors: Jifeng Dai, Haozhi Qi, Yuwen Xiong, Yi Li, Guodong Zhang, Han Hu, Yichen Wei
- Venue + year: IEEE ICCV 2017, pp. 764–773; preprint arXiv:1703.06211 [8][9]
- DOI/arXiv + URL: DOI 10.1109/ICCV.2017.89; arXiv https://arxiv.org/abs/1703.06211 ; proceedings page https://openaccess.thecvf.com/content_iccv_2017/html/Dai_Deformable_Convolutional_Networks_ICCV_2017_paper.html [8][9]
- Findings (3 sents): Two new modules — deformable convolution and deformable RoI pooling — augment fixed-grid sampling locations with task-learned 2-D offsets without extra supervision, remaining drop-in replacements trainable end-to-end by standard back-propagation [8][9]. The paper frames this as fixing CNNs' inherent limitation in modeling geometric transformations due to fixed geometric structures [9]. Effectiveness is validated on object detection and semantic segmentation (exact numbers not extracted — abstract/metadata only) and code was released via the Deformable-ConvNets repository [9].
- Fits TA Section: YOLO-RD accuracy branch (deformable-conv insertion, 7.09M / 12.9 GFLOPs / 189 FPS narrative) — the original citation for adaptive receptive fields on irregular crack/pothole geometry.
- BibTeX:
```bibtex
@inproceedings{dai2017deformable,
  author    = {Dai, Jifeng and Qi, Haozhi and Xiong, Yuwen and Li, Yi and Zhang, Guodong and Hu, Han and Wei, Yichen},
  title     = {Deformable Convolutional Networks},
  booktitle = {Proceedings of the IEEE International Conference on Computer Vision (ICCV)},
  pages     = {764--773},
  year      = {2017},
  doi       = {10.1109/ICCV.2017.89},
  eprint    = {1703.06211},
  archiveprefix = {arXiv}
}
```
- Duplicate-vs-existing: LIKELY DUPLICATE — dai2017deformable already in TA narrative; confirm/complete the existing bib entry with this record.

### C6. DCNv2 — Zhu et al., CVPR 2019 (modulated deformable convolution + feature mimicking)
- Title: Deformable ConvNets v2: More Deformable, Better Results
- Authors: Xizhou Zhu, Han Hu, Stephen Lin, Jifeng Dai
- Venue + year: IEEE/CVF CVPR 2019; preprint arXiv:1811.11168 [10][11]
- DOI/arXiv + URL: arXiv https://arxiv.org/abs/1811.11168 ; CVPR open-access PDF https://openaccess.thecvf.com/content_CVPR_2019/papers/Zhu_Deformable_ConvNets_V2_More_Deformable_Better_Results_CVPR_2019_paper.pdf [10][11]
- Findings (4 sents): DCNv2 increases deformation-modeling power in two ways: (i) deformable convolution applied across more network stages (conv3–conv5 in the Faster/Mask R-CNN experiments) and (ii) a modulation mechanism where each sampled point gets both a learned offset and a learned amplitude, plus R-CNN feature-mimicking loss to keep spatial support focused on the region of interest [11]. The added modules are described as remaining lightweight and drop-in compatible with existing detectors [11]. COCO object-detection/instance-segmentation experiments are reported as significantly above both regular ConvNets and DCNv1 on all tested backbones (exact AP numbers seen only in a truncated snippet — NOT verified, so no number is quoted here) [11].
- Fits TA Section: YOLO-RD deformable-conv discussion — cite alongside C5 to justify the modulation/offset mechanism behind the wavelet-refinement + deformable-conv accuracy claim; also the "lightweight module" phrasing supports the accuracy-vs-cost trade-off narrative.
- BibTeX:
```bibtex
@inproceedings{zhu2019dcnv2,
  author    = {Zhu, Xizhou and Hu, Han and Lin, Stephen and Dai, Jifeng},
  title     = {Deformable {ConvNets} v2: More Deformable, Better Results},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2019},
  eprint    = {1811.11168},
  archiveprefix = {arXiv},
  url       = {https://arxiv.org/abs/1811.11168}
}
```
- Duplicate-vs-existing: NEW (DCNv3 mentioned in brief scope but no verified DCNv3 record was found in this pass — see open questions).

### C7. WTConv — Finder et al., ECCV 2024 (wavelet convolution, large receptive fields)
- Title: Wavelet Convolutions for Large Receptive Fields
- Authors: Shahaf E. Finder, Roy Amoyal, Eran Treister, Oren Freifeld
- Venue + year: ECCV 2024 (accepted); preprint arXiv:2407.05848 [12]
- DOI/arXiv + URL: https://arxiv.org/abs/2407.05848 ; HTML https://arxiv.org/html/2407.05848v2 ; code https://github.com/BGU-CS-VIL/WTConv [12]
- Findings (4 sents): WTConv cascades wavelet-transform decomposition with small-kernel convolutions per frequency band so that trainable parameter count grows only logarithmically with receptive-field size k×k, addressing the saturation seen when naively enlarging CNN kernels toward ViT-like global fields [12]. It is designed as a drop-in replacement for depth-wise convolutions, retaining spatial resolution (unlike Fourier-based mixing) so wavelet-domain convolution stays meaningful [12]. Validation covers ConvNeXt/MobileNetV2 image classification and downstream-task backbones, with reported extra properties of corruption robustness and stronger shape-over-texture response (exact numbers not extracted — abstract/HTML skim only) [12]. Wavelet choice in the paper is the efficient Haar WT [12].
- Fits TA Section: YOLO-RD wavelet-refinement module — the canonical "why wavelets inside a conv detector" citation; supports the claim that wavelet-domain conv expands receptive field cheaply for thin cracks.
- BibTeX:
```bibtex
@misc{finder2024wtconv,
  author    = {Finder, Shahaf E. and Amoyal, Roy and Treister, Eran and Freifeld, Oren},
  title     = {Wavelet Convolutions for Large Receptive Fields},
  year      = {2024},
  eprint    = {2407.05848},
  archiveprefix = {arXiv},
  url       = {https://arxiv.org/abs/2407.05848},
  note      = {Accepted to ECCV 2024}
}
```
- Duplicate-vs-existing: NEW.

### C8. EfficientDet — Tan, Pang & Le, CVPR 2020 (efficient detector family + BiFPN + compound scaling)
- Title: EfficientDet: Scalable and Efficient Object Detection
- Authors: Mingxing Tan, Ruoming Pang, Quoc V. Le
- Venue + year: IEEE/CVF CVPR 2020; preprint arXiv:1911.09070 [13]
- DOI/arXiv + URL: arXiv https://arxiv.org/abs/1911.09070 ; code https://github.com/google/automl/tree/master/efficientdet [13]
- Findings (4 sents): Two efficiency optimizations are introduced: a weighted bi-directional feature pyramid network (BiFPN) for fast multi-scale fusion and a compound scaling rule that jointly scales backbone/BiFPN/box-class-network resolution-depth-width with one coefficient [13]. The headline result (single model, single scale) is EfficientDet-D7 at 55.1 AP on COCO test-dev with 77M parameters and 410B FLOPs, described as 4–9× smaller and using 13–42× fewer FLOPs than prior detectors [13]. Training follows SGD with momentum 0.9, weight decay 4e-5, linear warmup to LR 0.16 then cosine decay, 300 epochs for D0–D6 (batch 128 on 32 TPUv3) [13]. The family spans the full resource spectrum, which is exactly the accuracy-vs-cost framing the TA needs [13].
- Fits TA Section: efficiency-baseline / related-work section and the Params-GFLOPs-FPS methodology discussion — EfficientDet is the canonical "compound-scaled efficient detector" against which YOLOv8-PD's 2.46M/7.7 GFLOPs/368 FPS efficiency claim is contextualized.
- BibTeX:
```bibtex
@inproceedings{tan2020efficientdet,
  author    = {Tan, Mingxing and Pang, Ruoming and Le, Quoc V.},
  title     = {{EfficientDet}: Scalable and Efficient Object Detection},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages     = {10781--10790},
  year      = {2020},
  eprint    = {1911.09070},
  archiveprefix = {arXiv},
  url       = {https://arxiv.org/abs/1911.09070}
}
```
- Duplicate-vs-existing: NEW (distinct from C9, which is the Indonesian road-damage application of EfficientDet).

### C9. Hugo et al. 2025 — EfficientDet-D0 for road damage in Indonesia (hugo2025efficientdet)
- Title: EfficientDet Model for Accurate Detection and Classification of Road Damages in Indonesia
- Authors: Bernard Hugo, Alfi Yusrotis Zakiyyah, Kelvin Asclepius Minor (Mathematics Dept., School of Computer Science, Bina Nusantara University, Jakarta)
- Venue + year: Journal of Machine Learning and Deep Learning (JMLDL), Vol. 2 No. 1, 30 June 2025, DOI 10.64820/AEPJMLDL.21.11.17.62025 [14]
- URL: https://www.academicedgepress.co.uk/publicresources/documents/JMLDL.1.1/JMLDL.2.1/EfficientDet%20Model%20for%20Accurate%20Detection%20and%20Classification%20of%20Road%20Damages%20in%20Indonesia.pdf [14]
- Findings (4 sents, PDF skimmed directly): The study adapts a pre-trained EfficientDet-D0 (following Naddaf-Sh et al.) to Indonesian road images (pothole, alligator/longitudinal/lateral cracks) with built-in data augmentation, using validation F1-score as the dependent variable [14]. Best reported result is a 59.7% validation F1, stated to surpass the previous work's performance, with moderate performance attributed to feature complexity and generalization difficulty on unseen data [14]. The paper explicitly positions CNN/Faster R-CNN/YOLO as the common alternatives and EfficientDet-D0 as the assessed efficient option [14]. Caveat: JMLDL is a low-visibility outlet (verify indexing before giving it equal weight to CVPR/ECCV venues) [14 — inference from outlet, flagged as inference].
- Fits TA Section: related-work Indonesian-context paragraph — the only Indonesia-specific EfficientDet road-damage study found; cite for geographic/task relevance, not for SOTA numbers.
- BibTeX:
```bibtex
@article{hugo2025efficientdet,
  author  = {Hugo, Bernard and Zakiyyah, Alfi Yusrotis and Minor, Kelvin Asclepius},
  title   = {EfficientDet Model for Accurate Detection and Classification of Road Damages in Indonesia},
  journal = {Journal of Machine Learning and Deep Learning (JMLDL)},
  volume  = {2},
  number  = {1},
  year    = {2025},
  doi     = {10.64820/AEPJMLDL.21.11.17.62025},
  url     = {https://www.academicedgepress.co.uk/publicresources/documents/JMLDL.1.1/JMLDL.2.1/EfficientDet%20Model%20for%20Accurate%20Detection%20and%20Classification%20of%20Road%20Damages%20in%20Indonesia.pdf}
}
```
- Duplicate-vs-existing: NEW (this is the hugo2025efficientdet item requested in the brief).

### C10. YOLO lineage + benchmarking methodology (grouped: Redmon 2016 / Redmon&Farhadi 2018 / Bochkovskiy 2020 / Ge 2021 / Ultralytics docs)
- C10a. Redmon et al., CVPR 2016 — You Only Look Once: Unified, Real-Time Object Detection. DOI 10.1109/CVPR.2016.91; arXiv https://arxiv.org/abs/1506.02640. Single-network regression from pixels to boxes+class probabilities; base YOLO 45 FPS, Fast YOLO 155 FPS with ~2× mAP of other real-time detectors of the era [15].
- C10b. Redmon & Farhadi 2018 — YOLOv3: An Incremental Improvement. Tech report arXiv https://arxiv.org/abs/1804.02767. At 320×320 runs 22 ms / 28.2 mAP (SSD-level accuracy, ~3× faster); 57.9 mAP@50 in 51 ms on Titan X vs RetinaNet's 57.5 in 198 ms (~3.8× faster) [16].
- C10c. Bochkovskiy, Wang & Liao 2020 — YOLOv4: Optimal Speed and Accuracy of Object Detection. arXiv https://arxiv.org/abs/2004.10934. Reported 43.5% AP on COCO at ~65 FPS on Tesla V100 with WRC/CSP/CmBN/SAT/Mish/Mosaic/DropBlock/CIoU bag-of-specials (numbers from secondary snippet — medium confidence) [17].
- C10d. Ge et al. 2021 — YOLOX: Exceeding YOLO Series in 2021. arXiv https://arxiv.org/abs/2107.08430. Switches YOLO to anchor-free with a decoupled head and SimOTA label assignment; YOLO-Nano 0.91M params / 1.08G FLOPs / 25.3% COCO AP; YOLOX-L 50.0% AP at 68.9 FPS on Tesla V100 [18].
- C10e. Ultralytics YOLO Performance Metrics guide — https://docs.ultralytics.com/guides/yolo-performance-metrics/. Defines the exact metric stack the TA's RTX 4070 SUPER bs=1 imgsz-640 benchmark should mirror: per-class P/R/mAP50/mAP50-95, speed (preprocess/inference/postprocess) breakdown, F1 and PR curves, plus COCO-script metrics at multiple IoU thresholds and object sizes [19]. Ultralytics model tables also give the reporting convention (YOLOv8n: 37.3 mAP, 3.2M params, 8.7 GFLOPs) used to justify Params/GFLOPs/FPS side-by-side reporting [20].
- Fits TA Section: YOLO evolution history (v1→v3→v4→anchor-free decoupled head → v8/v12) in Chapter 2 background AND the benchmarking-methodology subsection (why Params/GFLOPs/FPS at fixed imgsz/bs/GPU is the real-time-detector reporting standard).
- BibTeX:
```bibtex
@inproceedings{redmon2016yolo,
  author    = {Redmon, Joseph and Divvala, Santosh and Girshick, Ross and Farhadi, Ali},
  title     = {You Only Look Once: Unified, Real-Time Object Detection},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2016},
  doi       = {10.1109/CVPR.2016.91},
  eprint    = {1506.02640},
  archiveprefix = {arXiv}
}
@misc{redmon2018yolov3,
  author = {Redmon, Joseph and Farhadi, Ali},
  title  = {{YOLOv3}: An Incremental Improvement},
  year   = {2018},
  eprint = {1804.02767},
  archiveprefix = {arXiv},
  url    = {https://arxiv.org/abs/1804.02767}
}
@misc{bochkovskiy2020yolov4,
  author = {Bochkovskiy, Alexey and Wang, Chien-Yao and Liao, Hong-Yuan Mark},
  title  = {{YOLOv4}: Optimal Speed and Accuracy of Object Detection},
  year   = {2020},
  eprint = {2004.10934},
  archiveprefix = {arXiv},
  url    = {https://arxiv.org/abs/2004.10934}
}
@misc{ge2021yolox,
  author = {Ge, Zheng and Liu, Songtao and Wang, Feng and Li, Zeming and Sun, Jian},
  title  = {{YOLOX}: Exceeding {YOLO} Series in 2021},
  year   = {2021},
  eprint = {2107.08430},
  archiveprefix = {arXiv},
  url    = {https://arxiv.org/abs/2107.08430}
}
@misc{ultralytics2024metrics,
  author = {{Ultralytics}},
  title  = {YOLO Performance Metrics},
  year   = {2024},
  url    = {https://docs.ultralytics.com/guides/yolo-performance-metrics/},
  note   = {Accessed Oct 2026}
}
```
- Duplicate-vs-existing: PARTIAL OVERLAP — redmon2017/redmon2018/bochkovskiy2020yolov4 are already cited in the proposal but missing from the IEEE bib; note the canonical YOLOv1 venue key is redmon2016 (CVPR 2016), so rename/merge redmon2017→redmon2016 on bib completion. YOLOX + Ultralytics-docs are NEW.

## Rejected / duplicates
- R1. GCL-YOLO (Cao et al., Remote Sensing 2023), YOLO-SE (Wu & Dong 2023), MGA-YOLO (Frontiers 2022), RepVGG-SimAM, DSAN/TechRxiv deformable-attention preprints — application papers that *use* GhostConv/SimAM/DCN rather than originating them. Rejected as primary citations; may serve as secondary "attention+Ghost in YOLO works" mentions only.
- R2. Guo et al. attention survey (Comp. Visual Media 2022) — useful background survey but not required given the 7–10 candidate cap and the brief's emphasis on originals.
- R3. DCNv3 / InternImage (Wang et al. 2022/2023) — in scope per brief ("DCNv3") but no verified DCNv3 record with URL was secured in this pass; NOT cited (no invented reference). Left as open question.
- R4. Wu2023 (efficiency metrics, per brief context) — not searched/verified in this pass; left as open question for the metrics-focused sibling brief or a follow-up.
- R5. YOLOv12n (R-ELAN + area attention, per TA narrative) — no verified YOLOv12 record secured in this pass; do not cite from memory. Left as open question.

## Open questions
1. DCNv3 canonical citation (Woo? Wang et al. 2023 "DCNv3" / InternImage CAA?) — needs a dedicated exact-title search; unresolved.
2. YOLOv12n original reference (R-ELAN + area attention) — unresolved; needed to ground the 2.57M/7.5 GFLOPs/319 FPS balanced-baseline claim.
3. Wu2023 efficiency-metrics source identity — unresolved in this pass.
4. JMLDL indexing/credibility check for hugo2025efficientdet (Scopus/Sinta/Google Scholar?) — unresolved; recommend a quick outlet check before leaning on its 59.7% F1 number.
5. Full-text PDF parsing done for 0 key papers (only abstracts/metadata/HTML skim + 1 PDF skim for C9) — brief allows abstract-level; flagging that exact AP deltas for C1/C3/C5/C6/C7 come from abstracts only.

## Evidence table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | PMLR — Yang et al., SimAM (ICML 2021 proceedings page + PDF) | https://proceedings.mlr.press/v139/yang21o.html | SimAM: parameter-free 3-D attention via energy-function closed-form solution, <10 lines of code; pp. 11863–11874 | primary | high |
| 2 | OpenAlex — Han et al., GhostNet CVPR 2020 record (DOI, venue, 4778 cites) | https://openalex.org/W3035414587 | GhostNet CVPR 2020, pp. 1577–1586, DOI 10.1109/CVPR42600.2020.00165 | secondary (metadata) | high |
| 3 | arXiv abs — GhostNet 1911.11907 (abstract read) | https://arxiv.org/abs/1911.11907 | Ghost module/cheap linear transforms; 75.7% top-1 ImageNet at MobileNetV3-like cost; code link | primary | high |
| 4 | OpenAlex — Woo et al., CBAM ECCV 2018 record (DOI, ~23,794 cites) | https://openalex.org/W2884585870 | CBAM ECCV 2018 (LNCS), DOI 10.1007/978-3-030-01234-2_1 | secondary (metadata) | high |
| 5 | arXiv abs — CBAM 1807.06521 (abstract read) | https://arxiv.org/abs/1807.06521 | Sequential channel+spatial attention, negligible overhead, gains on ImageNet/COCO/VOC | primary | high |
| 6 | OpenAlex — Wang et al., ECA-Net CVPR 2020 record (DOI, ~8787 cites) | https://openalex.org/W3034552520 | ECA-Net CVPR 2020, pp. 11531–11539, DOI 10.1109/CVPR42600.2020.01155 | secondary (metadata) | high |
| 7 | arXiv abs — ECA-Net 1910.03151 (abstract read) | https://arxiv.org/abs/1910.03151 | 80 params / 4.7e-4 GFLOPs vs ResNet-50 24.37M/3.86 GFLOPs; >2% Top-1 gain; 1-D conv, no dimensionality reduction | primary | high |
| 8 | CVF open access — Dai et al., Deformable ConvNets ICCV 2017 page | https://openaccess.thecvf.com/content_iccv_2017/html/Dai_Deformable_Convolutional_Networks_ICCV_2017_paper.html | ICCV 2017 pp. 764–773; deformable conv + deformable RoI pooling with learned offsets | primary | high |
| 9 | arXiv abs — Deformable ConvNets 1703.06211 (abstract read via search) | https://arxiv.org/abs/1703.06211 | Drop-in deformable modules, end-to-end backprop, detection+segmentation validation | primary | medium |
| 10 | arXiv abs — DCNv2 1811.11168 (abstract read) | https://arxiv.org/abs/1811.11168 | Modulation mechanism + broader deformable integration + R-CNN feature mimicking; COCO gains over DCNv1/regular | primary | high |
| 11 | CVF open access — Zhu et al., DCNv2 CVPR 2019 PDF | https://openaccess.thecvf.com/content_CVPR_2019/papers/Zhu_Deformable_ConvNets_V2_More_Deformable_Better_Results_CVPR_2019_paper.pdf | conv3–conv5 modulated deformable conv; RoIpooling modulation; lightweight claim | primary | medium (truncated fetch) |
| 12 | arXiv abs+HTML — WTConv 2407.05848 (ECCV 2024) | https://arxiv.org/abs/2407.05848 | Log-param scaling w/ receptive field; drop-in for depth-wise conv; Haar WT; code link | primary | high |
| 13 | arXiv abs — EfficientDet 1911.09070 (abstract read) | https://arxiv.org/abs/1911.09070 | BiFPN + compound scaling; D7 55.1 AP, 77M params, 410B FLOPs, 4–9× smaller, 13–42× fewer FLOPs; training schedule | primary | high |
| 14 | Hugo et al. 2025 PDF (skimmed directly) | https://www.academicedgepress.co.uk/publicresources/documents/JMLDL.1.1/JMLDL.2.1/EfficientDet%20Model%20for%20Accurate%20Detection%20and%20Classification%20of%20Road%20Damages%20in%20Indonesia.pdf | EfficientDet-D0 on Indonesian roads; best val F1 59.7%, beats prior work; JMLDL v2(1) 2025 | primary | medium (outlet visibility unverified) |
| 15 | arXiv abs — YOLOv1 1506.02640 | https://arxiv.org/abs/1506.02640 | Unified single-network detection; 45 FPS base / 155 FPS Fast YOLO; 2× mAP of contemporary real-time detectors | primary | high |
| 16 | arXiv abs — YOLOv3 1804.02767 | https://arxiv.org/abs/1804.02767 | 320×320: 22 ms / 28.2 mAP; 57.9 mAP@50 in 51 ms Titan X, ~3.8× faster than RetinaNet | primary | high |
| 17 | arXiv abs — YOLOv4 2004.10934 (via search snippets) | https://arxiv.org/abs/2004.10934 | 43.5% COCO AP at ~65 FPS Tesla V100; WRC/CSP/CmBN/SAT/Mish/Mosaic/DropBlock/CIoU | primary | medium (numbers from secondary snippet) |
| 18 | arXiv abs — YOLOX 2107.08430 | https://arxiv.org/abs/2107.08430 | Anchor-free + decoupled head + SimOTA; Nano 0.91M/1.08GFLOPs/25.3% AP; L 50.0% AP @68.9 FPS V100 | primary | high |
| 19 | Ultralytics docs — YOLO Performance Metrics guide (fetched) | https://docs.ultralytics.com/guides/yolo-performance-metrics/ | P/R/mAP50/mAP50-95 per class; speed breakdown; F1/PR curves; COCO-script evaluation | primary (vendor docs) | high |
| 20 | Ultralytics/Ultralytics YOLOv8 model table (via search snippets) | https://github.com/ultralytics/ultralytics/blob/main/docs/en/models/yolov8.md | YOLOv8n: 37.3 mAP, 3.2M params, 8.7 GFLOPs reporting convention | primary (vendor docs) | medium (snippet only) |

## Findings
- The zero-parameter attention baseline (SimAM, ICML 2021) [1] and the parameterized channel+spatial baseline (CBAM, ECCV 2018) [4][5] are both verified originals; together they frame the TA's SimAM/CBAM neck ablation, where only CBAM should move the Params/GFLOPs/FPS needle.
- The cheap-convolution baseline (GhostNet, CVPR 2020) [2][3] gives the TA's YOLOv8-PD branch its founding citation: 75.7% ImageNet top-1 at MobileNetV3-like cost via ghost feature maps [3] directly motivates GhostConv-in-neck for the 2.46M/7.7 GFLOPs/368 FPS efficiency point.
- Among attention options, ECA-Net [6][7] is the strongest efficiency-precedent citation (80 extra params, ~4.7e-4 GFLOPs, >2% Top-1 gain [7]) — worth a one-line related-work mention even though the TA only inserts SimAM/CBAM (inference: ECA is a candidate future ablation).
- Deformable convolution is grounded in two verified originals: v1 (ICCV 2017) [8][9] for the offset-sampling mechanism and v2 (CVPR 2019) [10][11] for modulation + feature mimicking and the explicit "modules remain lightweight" claim [11] — both support the YOLO-RD accuracy branch (7.09M/12.9 GFLOPs/189 FPS narrative).
- The wavelet-refinement module traces to WTConv (ECCV 2024) [12]: logarithmic parameter scaling with receptive-field size and Haar-wavelet drop-in design for depth-wise convolutions — the "large receptive field for thin cracks at low cost" argument.
- The efficiency-detector family reference is EfficientDet (CVPR 2020) [13] with its BiFPN + compound-scaling recipe and D7 headline (55.1 AP / 77M / 410B FLOPs) [13]; the Indonesia-specific instantiation is Hugo et al. 2025 (EfficientDet-D0, 59.7% val F1 on Indonesian pothole/crack classes) [14], the geographic-relevance citation (outlet credibility still to check — inference).
- YOLO history + benchmarking methodology rest on verified anchors: unified real-time detection at 45/155 FPS (v1, 2016) [15], incremental multi-scale/speed gains (v3, 2018) [16], bag-of-specials SOTA-efficiency point (v4, 2020) [17], anchor-free decoupled-head switch (YOLOX, 2021) [18], and the Ultralytics P/R/mAP50/mAP50-95 + speed-breakdown reporting convention [19][20] that the TA's RTX 4070 SUPER bs=1 imgsz-640 protocol should mirror.
- PDF full-text parsing: blocked/not-done for all papers except a direct skim of the Hugo-2025 PDF [14]; all mechanism/number claims above come from abstracts, HTML, official docs, or metadata as flagged per-row. No source, number, or URL was invented.

## Sources
1. Yang et al., SimAM — http://proceedings.mlr.press/v139/yang21o.html (PDF: http://proceedings.mlr.press/v139/yang21o/yang21o.pdf)
2. OpenAlex record, Han et al., GhostNet CVPR 2020 — https://openalex.org/W3035414587
3. Han et al., GhostNet arXiv — https://arxiv.org/abs/1911.11907 (code: https://github.com/huawei-noah/ghostnet)
4. OpenAlex record, Woo et al., CBAM ECCV 2018 — https://openalex.org/W2884585870
5. Woo et al., CBAM arXiv — https://arxiv.org/abs/1807.06521
6. OpenAlex record, Wang et al., ECA-Net CVPR 2020 — https://openalex.org/W3034552520
7. Wang et al., ECA-Net arXiv — https://arxiv.org/abs/1910.03151 (project: https://github.com/BangguWu/ECANet)
8. CVF, Dai et al., Deformable ConvNets ICCV 2017 — https://openaccess.thecvf.com/content_iccv_2017/html/Dai_Deformable_Convolutional_Networks_ICCV_2017_paper.html
9. Dai et al., Deformable ConvNets arXiv — https://arxiv.org/abs/1703.06211
10. Zhu et al., DCNv2 arXiv — https://arxiv.org/abs/1811.11168
11. CVF, Zhu et al., DCNv2 CVPR 2019 PDF — https://openaccess.thecvf.com/content_CVPR_2019/papers/Zhu_Deformable_ConvNets_V2_More_Deformable_Better_Results_CVPR_2019_paper.pdf
12. Finder et al., WTConv arXiv — https://arxiv.org/abs/2407.05848 (HTML: https://arxiv.org/html/2407.05848v2; code: https://github.com/BGU-CS-VIL/WTConv)
13. Tan et al., EfficientDet arXiv — https://arxiv.org/abs/1911.09070 (code: https://github.com/google/automl/tree/master/efficientdet)
14. Hugo et al. 2025, EfficientDet Indonesia roads PDF — https://www.academicedgepress.co.uk/publicresources/documents/JMLDL.1.1/JMLDL.2.1/EfficientDet%20Model%20for%20Accurate%20Detection%20and%20Classification%20of%20Road%20Damages%20in%20Indonesia.pdf
15. Redmon et al., YOLOv1 arXiv — https://arxiv.org/abs/1506.02640 (DOI: https://doi.org/10.1109/CVPR.2016.91)
16. Redmon & Farhadi, YOLOv3 arXiv — https://arxiv.org/abs/1804.02767
17. Bochkovskiy et al., YOLOv4 arXiv — https://arxiv.org/abs/2004.10934
18. Ge et al., YOLOX arXiv — https://arxiv.org/abs/2107.08430
19. Ultralytics YOLO Performance Metrics guide — https://docs.ultralytics.com/guides/yolo-performance-metrics/
20. Ultralytics YOLOv8 docs model table — https://github.com/ultralytics/ultralytics/blob/main/docs/en/models/yolov8.md

## Coverage status
- Checked directly: arXiv abstracts for GhostNet/CBAM/ECA-Net/EfficientDet/WTConv/DCNv2/YOLOv1/YOLOv3/YOLOX; PMLR page+PDF existence for SimAM; CVF pages for Dai-2017/DCNv2; OpenAlex metadata (venue/year/DOI/citations) for GhostNet/CBAM/ECA-Net/SimAM; Ultralytics metrics guide content; Hugo-2025 PDF skim (pp. 1–7 extracted).
- Uncertain: exact AP-delta numbers for SimAM/CBAM/DCN/WTConv (abstracts only); YOLOv4 43.5%@65FPS (secondary snippet); YOLOv8n table numbers (snippet only); JMLDL outlet credibility.
- Could not complete: full-text PDF parsing (marked blocked per brief permission); DCNv3 canonical record; YOLOv12n record; Wu2023 identity.
