# Citation Addition Proposal — READY TO PASTE BibTeX

> Source: `outputs/yolo-road-damage-references.md` (verified 2026-10-02, W1–W8 fixed)
> + new finds verified today via OpenAlex/arXiv API (li2025dife, sapkota2025yoloreview, finder2024wtconv).
> Current state: 13 cited keys / 14 bib entries / `dai2017deformable` orphaned.

---

## Tier 1 — Module names already in the text, citations missing (STRONGLY RECOMMENDED)

**Insertion point A** (`main.tex` line 86):
`...lightweight convolutions, attention modules, or feature-fusion blocks... \cite{Wu2023,Li2024,Shi_2026}`
→ append: `,han2020ghostnet,wang2020eca,yang2021simam`

**Insertion point B** (line 86): `...a wavelet-convolution head \cite{Wang2025}`
→ append: `,finder2024wtconv`

```bibtex
@inproceedings{yang2021simam,
  author    = {Yang, Lingxiao and Zhang, Ru-Yuan and Li, Lida and Xie, Xiaohua},
  title     = {{SimAM}: A Simple, Parameter-Free Attention Module for Convolutional Neural Networks},
  booktitle = {Proceedings of the 38th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {139},
  pages     = {11863--11874},
  year      = {2021},
  url       = {https://proceedings.mlr.press/v139/yang21o.html}
}

@inproceedings{han2020ghostnet,
  author    = {Han, Kai and Wang, Yunhe and Tian, Qi and Guo, Jianyuan and Xu, Chunjing and Xu, Chang},
  title     = {{GhostNet}: More Features From Cheap Operations},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages     = {1577--1586},
  year      = {2020},
  doi       = {10.1109/CVPR42600.2020.00165}
}

@inproceedings{wang2020eca,
  author    = {Wang, Qilong and Wu, Banggu and Zhu, Pengfei and Li, Peihua and Zuo, Wangmeng and Hu, Qinghua},
  title     = {{ECA-Net}: Efficient Channel Attention for Deep Convolutional Neural Networks},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages     = {11531--11539},
  year      = {2020},
  doi       = {10.1109/CVPR42600.2020.01155}
}

@inproceedings{finder2024wtconv,
  author    = {Finder, Shahaf E. and Amoyal, Roy and Treister, Eran and Freifeld, Oren},
  title     = {Wavelet Convolutions for Large Receptive Fields},
  booktitle = {Proceedings of the European Conference on Computer Vision (ECCV)},
  year      = {2024},
  eprint    = {2407.05848},
  archivePrefix = {arXiv},
  note      = {ECCV 2024}
}
```

## Tier 2 — Core argument support (distractor hypothesis + domain gap)

**Insertion point C** (line 83, after Matouq sentence): append
`Bu{\v{c}}ko et al. similarly treated manholes as a pothole-like distractor class in urban pothole detection~\cite{bucko2022computer}.`
(or simply add `,bucko2022computer` to the Matouq `\cite`)

**Insertion point D** (line 83, cross-country sentence): `...beyond their training distribution \cite{arya2021deep}`
→ append: `,lin2023dardd,li2025dife` (domain-adaptation line of work)

```bibtex
@article{bucko2022computer,
  author  = {Bu{\v{c}}ko, Boris and Lieskovsk{\'a}, Eva and Z{\'a}bovsk{\'a}, Katar{\'\i}na and Z{\'a}bovsk{\'y}, Michal},
  title   = {Computer Vision Based Pothole Detection under Challenging Conditions},
  journal = {Sensors},
  volume  = {22},
  number  = {22},
  pages   = {8878},
  year    = {2022},
  doi     = {10.3390/s22228878}
}

@article{lin2023dardd,
  author  = {Lin, Chunmian and Tian, Daxin and Duan, Xuting and Zhou, Jianshan and Zhao, Dezong and Cao, Dongpu},
  title   = {{DA-RDD}: Toward Domain Adaptive Road Damage Detection Across Different Countries},
  journal = {IEEE Transactions on Intelligent Transportation Systems},
  volume  = {24},
  number  = {3},
  pages   = {3091--3103},
  year    = {2023},
  doi     = {10.1109/TITS.2022.3221067}
}

@article{li2025dife,
  author  = {Li, Jie and Qu, Zhong and Yin, Xuehui},
  title   = {Domain-Invariant Feature Enhancement Domain Adaptation for Cross-Scene Road Damage Detection},
  journal = {IEEE Transactions on Circuits and Systems for Video Technology},
  volume  = {36},
  number  = {3},
  pages   = {3466--3480},
  year    = {2025},
  doi     = {10.1109/TCSVT.2025.3613484}
}
```

## Tier 3 — Multi-country benchmark lineage (datasets section)

**Insertion point E** (line 83, RDD2022 sentence): `\cite{Arya2024846}` →
`\cite{Arya2024846,maeda2018road,arya2020grddc,arya2022crddc2022}`

```bibtex
@article{maeda2018road,
  author  = {Maeda, Hiroya and Sekimoto, Yoshihide and Seto, Toshikazu and Kashiyama, Takehiro and Omata, Hiroshi},
  title   = {Road Damage Detection and Classification Using Deep Neural Networks with Smartphone Images},
  journal = {Computer-Aided Civil and Infrastructure Engineering},
  volume  = {33},
  number  = {12},
  pages   = {1127--1141},
  year    = {2018},
  doi     = {10.1111/mice.12387}
}

@misc{arya2020grddc,
  author = {Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Omata, Hiroshi and Kashiyama, Takehiro and Sekimoto, Yoshihide},
  title  = {Global Road Damage Detection: State-of-the-art Solutions},
  year   = {2020},
  eprint = {2011.08740},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV},
  doi    = {10.48550/arXiv.2011.08740}
}

@misc{arya2022crddc2022,
  author = {Arya, Deeksha and Maeda, Hiroya and Ghosh, Sanjay Kumar and Toshniwal, Durga and Omata, Hiroshi and Kashiyama, Takehiro and Sekimoto, Yoshihide},
  title  = {Crowdsensing-based Road Damage Detection Challenge ({CRDDC}'2022)},
  year   = {2022},
  eprint = {2211.11362},
  archivePrefix = {arXiv},
  primaryClass = {cs.CV},
  doi    = {10.48550/arXiv.2211.11362}
}
```

## Tier 4 — Optional extras

**Insertion points:** `sapkota2025yoloreview` → line 86 `single-stage framework \cite{redmon2016you}` +review;
`munawir2025bandung` → Target-Data subsection (Indonesian precedent);
`wu2025rsdd` → compact-variants sentence; `lin2014coco` → Metrics subsection.

```bibtex
@article{sapkota2025yoloreview,
  author  = {Sapkota, Ranjan and Flores-Calero, Marco and Qureshi, Rizwan and Badjugar, Chetan and Nepal, Upesh and Poulose, Alwin and Zeno, Peter J. and Vaddevolu, Uday Bhanu Prakash and Khan, Sheheryar and Shoman, Maged and Yan, Hong and Karkee, Manoj},
  title   = {{YOLO} Advances to Its Genesis: A Decadal and Comprehensive Review of the You Only Look Once ({YOLO}) Series},
  journal = {Artificial Intelligence Review},
  volume  = {58},
  number  = {9},
  year    = {2025},
  doi     = {10.1007/s10462-025-11253-3}
}

@article{munawir2025bandung,
  author  = {Munawir, Munawir and Pararta, Muhammad Salam and Suteddy, Wirmanto and Putra, Muhammad Taufik Dwi and Koerniawan, Mochamad Donny and Dewancker, Bart Julien},
  title   = {Enhancing Road Maintenance Strategies in {Bandung} City Through {YOLO} and {CNN}-Based Damage Detection},
  journal = {Journal of Asian Institute of Low Carbon Design},
  year    = {2025},
  doi     = {10.69368/jailcd.20250009},
  note    = {Accuracy-based (not mAP); relevance-only citation}
}

@article{wu2025rsdd,
  author  = {Wu, C. and Zhang, L. and Fan, X.},
  title   = {Object Detection Model Design for Tiny Road Surface Damage},
  journal = {Scientific Reports},
  volume  = {15},
  pages   = {11032},
  year    = {2025},
  doi     = {10.1038/s41598-025-95502-z},
  note    = {Author given names unverified (initials in source)}
}

@inproceedings{lin2014coco,
  author    = {Lin, Tsung-Yi and Maire, Michael and Belongie, Serge and Hays, James and Perona, Pietro and Ramanan, Deva and Doll{\'a}r, Piotr and Zitnick, C. Lawrence},
  title     = {{Microsoft COCO}: Common Objects in Context},
  booktitle = {Proceedings of the European Conference on Computer Vision},
  pages     = {740--755},
  year      = {2014},
  doi       = {10.1007/978-3-319-10602-1_48}
}
```

## Housekeeping
- `dai2017deformable` in references.bib is never cited → safe to delete (BibTeX only emits cited entries; harmless but dead weight).

## Verification summary
| Key | Verified via |
|---|---|
| yang2021simam, han2020ghostnet, wang2020eca, lin2023dardd, bucko2022computer, maeda2018road, arya2020grddc, arya2022crddc2022, lin2014coco, munawir2025bandung, wu2025rsdd | outputs/yolo-road-damage-references.md (fetched live / index-matched, W1–W8 reviewed) |
| finder2024wtconv | arXiv API today (ECCV 2024, 4 authors confirmed) |
| li2025dife | OpenAlex W4414432319 today (TCSVT 36(3):3466–3480) |
| sapkota2025yoloreview | OpenAlex W4400266963 today (AIR 58(9), 308 citations) |
