# Deep Research Plan: yolo-road-damage-references

## Topic
Cari referensi paper tambahan yang cocok untuk daftar pustaka TA / paper IEEE: evaluasi komparatif YOLO lightweight untuk deteksi kerusakan jalan (N-RDD2024 subset Asia, 6 kelas + 2 distractor), trade-off akurasi-efisiensi, dan uji generalisasi zero-shot di Indonesia.

## What was read (source of truth)
- `latex/PROPOSAL_TA.md` — judul, 3 rumusan masalah, N-RDD2024 subset Asia 9.670 citra / 24.290 objek (6 kelas: D00/D10/D20/D40 + D70 manhole/D80 patchy), 5 model (YOLOv8n, YOLOv8-PD, YOLO-RD, YOLOv12n, YOLOv26n), skenario 1-3, glosarium 26 kunci BibTeX proposal.
- `latex/IEEE-Conference/draft/draft-analisis-hasil.md` — hasil test 5 model (RD mAP50 0.661 #1 sumber, v12n 0.654 #2 sumber tapi #1 zero-shot Indo 0.309), ablasi 6-vs-4 kelas (FP-rate + uji z), variasi per negara (China 0.88-0.90 >> Japan ~0.58 > India ~0.43), domain gap >50%, studi kilau pagi (N=42, caveat komposisi kelas).
- `latex/IEEE-Conference/references.bib` — 13 entri saat ini: redmon2016you, arya2021deep, Arya2024846 (RDD2022), kaya2024nrdd2024, Zeng2024 (YOLOv8-PD), Li2024 (RDD-YOLO), Wang2025 (YOLO-RD), Wu2023 (YOLO-LWNet), matouq2024ai, tian2026yolov12, sapkota2025yolo26, cui2019class, dai2017deformable.
- `latex/refference/` — 7 PDF terdaftar (01 RDD2022, 02 YOLOv8-PD, 03 RDD-YOLO, 04 YOLO-RD, 05 lightweight+KD, 06 YOLO-LWNet, 07 EfficientDet Indonesia) + 4 PDF tambahan (08 REG loss, 09 AI-Driven pothole, 10 Road Defect baseline, 11 Ultralytics YOLO Evolution).

## Gaps in current bibliography (why more refs needed)
1. Proposal mengutip tapi `references.bib` IEEE belum punya: `Shi_2026` (YOLO-LWD), `hugo2025efficientdet` (F1 59,7% Indonesia), `han2020ghostnet`, `woo2018cbam`, `panboonyuen2025reg`, `bochkovskiy2020yolov4`, `redmon2017/2018` (v2/v3), `mandal2020deep`, `hosseini2021`, `kusumah2023`, pendukung latar belakang.
2. Tidak ada referensi metodologi domain shift / domain generalization / zero-shot detection untuk jalan (klaim gap >50% butuh landasan teori, bukan hanya angka sendiri).
3. Tidak ada referensi CRDDC2022 challenge / cross-country benchmark selain Arya2024 (padahal F1 0,770 dan degradasi lintas negara disebut di proposal).
4. Tidak ada paper asli attention lightweight (SimAM, ECA) dan YOLOv8/v12/v26 resmi Ultralytics — padahal modifikasi RD/PD diklaim rekonstruksi tanpa kode resmi.
5. Tidak ada referensi small-object detection / multi-scale mAP (median bbox 1,69% citra) dan evaluasi real-time (FPS/Params/GFLOPs) sebagai trade-off metric.
6. Tidak ada pembanding detector non-YOLO terkini (EfficientDet, RT-DETR, YOLO-NAS/v11) untuk posisi "YOLO nano" di related work.

## Key questions
1. Paper YOLO lightweight road-damage apa (2022-2026) yang paling cocok disandingkan dengan 5 model TA (arsitektur, dataset RDD2022/N-RDD2024, angka mAP/F1, efisiensi)?
2. Paper dataset/benchmark apa (RDD2022, N-RDD2024, CRDDC2022, crowdsensing, Indonesia/Asia Tenggara) yang memperkuat urgensi domain gap?
3. Paper domain shift / domain generalization / zero-shot / cross-domain object detection apa yang memberi landasan teori untuk uji zero-shot Bandung?
4. Paper class-imbalance / loss (Focal, class-balanced, REG/GFL) + distractor/false-positive (manhole vs pothole vs patch) apa yang mendukung ablasi 6-vs-4 kelas?
5. Paper attention/efficiency (SimAM, CBAM, ECA, GhostNet/GhostConv, deformable conv, wavelet) + metrik real-time (mAP-small, FPS/Params/GFLOPs) apa yang mendukung klaim accuracy-first vs efficiency-first?
6. Setiap kandidat: metadata lengkap (venue/tahun/DOI), relevansi ke bab/section TA mana, dan entri BibTeX siap pakai?

## Evidence needed
- Minimal 20-30 kandidat paper, masing-masing: judul, penulis, venue + tahun, DOI/arXiv ID + URL terverifikasi, 2-4 kalimat ringkasan temuan/angka kunci, 1 kalimat "cocok untuk section X karena Y", BibTeX.
- Prioritas: open-access / arXiv / DOI resmi; hindari blog dan sumber tak terverifikasi.
- Tandai duplikat vs 13 entri yang sudah ada; tandai yang hanya dari abstrak/metadata vs full-text.
- Catat yang ditolak (dead link, tak terverifikasi, tidak relevan) untuk provenance.

## Scale decision
Topik ini survei multi-faset (komparasi model + dataset/domain + loss/imbalance + efisiensi), bukan explainer sempit "what is X". Direct search saja tidak cukup karena butuh 4 sudut literatur berbeda dengan istilah pencarian berbeda. Keputusan: pakai **4 `researcher` subagents paralel** (batas atas kategori broad survey), lalu verifikasi + review berlapis. Setiap researcher menulis 1 file riset; lead (saya) melakukan sintesis, sitasi, dan review akhir — tidak didelegasikan.

## Task ledger
| ID | Owner | Task | Output |
|---|---|---|---|
| T1 | researcher | Sudut 1: YOLO lightweight road-damage (RDD-YOLO, YOLOv8-PD, YOLO-RD, YOLO-LWD, YOLO-LWNet, YOLOv8/v12/v26 resmi, YOLOv11/NAS, RT-DETR sebagai pembanding). Baca brief `outputs/.plans/yolo-road-damage-references-T1.md`, tulis kandidat + BibTeX. | `outputs/.drafts/yolo-road-damage-references-research-models.md` |
| T2 | researcher | Sudut 2: dataset & domain (RDD2022, N-RDD2024, CRDDC2022, crowdsensing/smartphone, road Indonesia/Asia, cross-country degradation). | `outputs/.drafts/yolo-road-damage-references-research-domain.md` |
| T3 | researcher | Sudut 3: imbalance + distractor (Focal/class-balanced/REG-GFL, manhole-vs-pothole-vs-patch FP, small-object/multi-scale). | `outputs/.drafts/yolo-road-damage-references-research-loss.md` |
| T4 | researcher | Sudut 4: efficiency & attention (SimAM/CBAM/ECA, GhostNet/GhostConv, deformable conv/wavelet, Params/GFLOPs/FPS methodology, EfficientDet). | `outputs/.drafts/yolo-road-damage-references-research-efficiency.md` |
| S1 | lead (saya) | Sintesis: tulis `yolo-road-damage-references-draft.md`, sapu klaim tanpa sumber. | `outputs/.drafts/yolo-road-damage-references-draft.md` |
| S2 | verifier | Tambah sitasi inline + section Sources, verifikasi tiap URL. | `outputs/.drafts/yolo-road-damage-references-cited.md` |
| S3 | reviewer | Verifikasi klaim tak berdasar, gap logika, single-source critical claims. | `outputs/.drafts/yolo-road-damage-references-verification.md` |
| S4 | lead (saya) | Revisi (bila FATAL) + deliver final + provenance. | `outputs/yolo-road-damage-references.md` + `outputs/yolo-road-damage-references.provenance.md` |

## Verification log
- [ ] Setiap kandidat punya URL terverifikasi (fetch/search) sebelum masuk final.
- [ ] Tidak ada sumber/angka/tabel/figure inventasi di draft.
- [ ] Klaim kritis (angka mAP/F1, "terbaik", "pertama") didukung ≥1 sumber; single-source ditandai.
- [ ] Duplikat terhadap 13 entri existing ditandai, bukan diduplikasi diam-diam.
- [ ] Semua artefak required ada di disk sebelum respons final.

## Decision log
- 2026-10-02: slug `yolo-road-damage-references` (4 kata, lowercase-hyphen).
- 2026-10-02: skala = 4 researcher paralel (broad survey), bukan direct search — alasan: 4 sudut literatur berbeda, masing-masing butuh 3+ kueri.
- 2026-10-02: brief per-researcher ditulis dulu (`-T1.md` … `-T4.md`) + workflow `runs.all`, sesuai aturan subagent.
- 2026-10-02: menunggu persetujuan user sebelum gather evidence (belum ada search/fetch/subagent/draft).
