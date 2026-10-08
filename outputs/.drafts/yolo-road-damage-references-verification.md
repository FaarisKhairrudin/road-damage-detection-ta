## Summary
Verification pass over `yolo-road-damage-references-cited.md` (43 sources, claimed 12 ADD + 8 OPTIONAL/BACKUP + 5 MERGE). The draft's hedging discipline is good: it explicitly labels snippet-level numbers as UNVERIFIED, marks fetch-blocked pages, and refuses to cite YOLO-LWD. Spot re-fetch of [1][2][3][4][5][7][8][9][14][15][20][21][23] plus OpenAlex cross-checks confirms most "LIVE" labels and most abstract-level performance figures. The material blockers are narrow but real: a wrong DOI for DA-RDD [14], an unsupported "NeurIPS 2025" venue tag for YOLOv12 [2], year/version ambiguity for REG [21], and several unprovable exclusivity claims ("satu-satunya ... yang ditemukan"). Internal-project counts and duplicate-key decisions cannot be verified from this draft alone and must stay labeled as internal/process findings, not literature facts.

## Strengths
- [S1] Explicit evidence tiers (LIVE / FETCH-BLOCKED / UNVERIFIED / NOT FETCHED) are applied consistently; high-risk numbers (YOLO-RD [6], RDD-YOLO [40], Bandung 93.06% [15], Hugo 59.7% [32], Kaya Measurement [12], Pham [16], YOLOv4 43.5%@65FPS [35]) are correctly withheld from final citation.
- [S2] CRDDC [7] and GRDDC [8] figures re-verified verbatim against arXiv abstracts in this pass (47,420 / 6 countries / 60+ teams / F1 76%; 26,336 / 121 teams / test1 2,631 / test2 2,664 / F1 0.67/0.66).
- [S3] YOLO26 docs figures [4] re-verified verbatim (40.9/40.1 mAP, 1.7 ms T4, 2.4M params, 5.5B FLOPs, family 40.9–57.5 @ 1.7–11.8 ms, 43% CPU-ONNX claim) and the v4-retitle FLAG on arXiv:2510.09653 [3] is confirmed real.
- [S4] RSDD [1] dataset/module/tiny-focus description re-verified in full text; REG abstract figures [21] (mAP50 80.34 / F1 77.87, spatial-contextual + probabilistic refinement) re-verified; RT-DETR [5], VarifocalNet [20], COCO totals [23], Maeda counts [9] all match abstracts.
- [S5] DO NOT CITE on YOLO-LWD/Shi 2026 is the correct call given zero retrievable source; no replacement is invented.

## Weaknesses
- [W1] **FATAL:** DA-RDD [14] cites an unverified/wrong DOI (`10.1109/TITS.2022.3226018`) and an IEEE document URL (`document/9954613`) with no verified mapping. OpenAlex returns DOI `10.1109/tits.2022.3221067`, vol.24 no.3 pp.3091–3103, first-published 2022-11-18 (print 2023). BibTeX without DOI/pages as drafted will fail IEEE verification. Passage: §3 `ADD — Lin et al. DA-RDD` + Sources [14].
- [W2] **MAJOR:** YOLOv12 venue claim overstates evidence. Draft says "Klaim venue NeurIPS 2025 hanya sebagian terverifikasi (catatan OpenAlex mencatatnya sebagai conference-paper 2025)". OpenAlex record checked in this pass (W4407759488) says `type: conference-paper`, year 2025, pp.87151–87175, DOI `10.52202/085713-2627` — it does **not** name NeurIPS. "NeurIPS 2025" must be removed until a venue page is produced. Passage: §2 `MERGE — Tian et al. YOLOv12` + Sources [2].
- [W3] **MAJOR:** Unprovable exclusivity claims presented as literature facts. Four instances use "satu-satunya ... yang ditemukan" (REG §4 [21]; DA-RDD §3 [14]; Bandung §3 [15]; manhole-distractor §4 [22]) based on four internal briefs, not an exhaustive search. Each is single-source-critical if a reader relies on it for novelty. Reword to "satu preseden yang diidentifikasi dalam cakupan brief ini". Passages: §§3–4 as listed.
- [W4] **MAJOR:** REG [21] year/venue ambiguity. Draft BibTeX claims `@inproceedings KST 2025 pp.324–329 IEEE` while the only verified artifact is arXiv:2409.09877 (v1 Sep 2024, v2 Sep 2024, 14 pp. confirmed) plus an UNREADABLE IEEE link. Citing the KST proceedings version without a readable proceedings page risks a wrong-venue citation. Cite the arXiv version read, or hold the KST entry until the IEEE page is readable. Passage: §4 `ADD (proposal→bib) — Panboonyuen REG` + Sources [21].
- [W5] **MAJOR:** Single-source-critical performance/geo claims carried at abstract/snippet level without second-source check: Bandung 93.06% accuracy [15] (metric mismatch accuracy-vs-mAP correctly noted but protocol still unread); Hugo F1 59.7% [32] (minimal-content fetch + unchecked outlet); Bučko manhole-easier-than-pothole pattern [22] (PMC readable but detail still "per research-file snippet, re-confirm"). Draft correctly flags each UNVERIFIED, but §4 still uses the Bučko pattern as corroboration for internal TA numbers ("pola yang sama dengan angka internal TA"). Remove the corroboration use until the PMC passage is quoted. Passages: §3 [15][32]; §4 [22].
- [W6] **MINOR:** RT-DETR 8-author list [5] claimed "kini terverifikasi dari indeks arXiv" — the arXiv abs page fetched in this pass confirms title/numbers but the abs-page render used here surfaces only the submitter, not the full ordered author list. Confirm author order/spelling from PDF or arXiv API before final BibTeX. Passage: §2 `OPTIONAL — Zhao et al. RT-DETR` + Sources [5].
- [W7] **MINOR:** Internal counts and duplicate-key resolutions are unverifiable from this draft alone: "saat ini 13 entri", "~36 kandidat", "12 + 8 + 5", and each MERGE/DUPLICATE verdict (Tian [2], Sapkota [3], Cui [18], GhostNet/CBAM/DCNv1, Zeng [38]/Li [40]/Wu [39], `arya2021deep` vs [13], `redmon2017` vs [33]). They are correctly labeled internal/draft-decision in most places, but any reuse outside the TA must keep that label; do not promote them to literature facts. Passages: Executive summary; §1; Evidence-backed caveats.
- [W8] **MINOR:** COCO author-list FLAG [23] is correct but the draft BibTeX still ships the proceedings-mixed list. Replace with the canonical ECCV-2014 proceedings list at BibTeX-final time and verify S/M/L pixel thresholds against the official eval protocol (draft already TODOs this — keep the TODO attached to any use of mAP-S/M/L). Passage: §4 `ADD — Lin et al. COCO` + Sources [23].

## Questions for Authors
- [Q1] DA-RDD [14]: confirm the correct DOI (`10.1109/tits.2022.3221067` per OpenAlex vs your `...3226018`) and the IEEE document number; is the intended citation the Nov-2022 early-access or the vol.24-no.3 print (pp.3091–3103)?
- [Q2] YOLOv12 [2]: what venue page supports "NeurIPS 2025"? If none, will you cite arXiv:2502.12524 only?
- [Q3] REG [21]: which artifact was actually read — arXiv:2409.09877 v1 or v2 — and will the BibTeX cite arXiv (2024) until the KST/IEEE pp.324–329 page is readable?
- [Q4] Bučko [22]: which PMC paragraph/sentence supports "manhole ditambahkan karena meniru pothole; manhole empiris lebih mudah"? Quote it before using the pattern as corroboration.
- [Q5] Bandung [15] and Hugo [32]: given accuracy-vs-mAP mismatch and minimal-content fetch respectively, will both be cited for geographic relevance only (no figures), as the draft currently hedges?
- [Q6] RT-DETR [5] author order, Wu/Zhang/Fan first names [1], and VarifocalNet/GFL detail pages [19][20]: confirmed from PDF before BibTeX-final?

## Verdict
Verification judgment (not a venue prediction): **conditionally usable with mandatory fixes**. The hedging architecture works and most LIVE labels re-verify, but [W1] (DA-RDD DOI) and [W2] (YOLOv12 venue) must be corrected, [W4] (REG venue) must be downgraded to the artifact actually read, and [W3]/[W5] exclusivity/corroboration language must be softened to scope-of-brief wording until full-text passages are quoted. Confidence: **medium-high** on LIVE/UNVERIFIED labels checked here; **low** on anything marked NOT FETCHED or fetch-blocked ([6][12][40][41][42][43], [14]-fulltext, [21]-IEEE, [32]-PDF). Revision priority: fix [W1] first (wrong DOI propagates into BibTeX), then [W2]/[W4], then [W3]/[W5] wording.

## Revision Plan
1. Fix [W1]: replace DA-RDD DOI with `10.1109/tits.2022.3221067`, add vol.24 no.3 pp.3091–3103, clarify early-access-2022 vs print-2023; verify `document/9954613` resolves to this paper or drop the URL.
2. Fix [W2]: delete "NeurIPS 2025" or attach a venue URL; default citation `arXiv:2502.12524 (2025)`.
3. Fix [W4]: REG BibTeX cites `arXiv:2409.09877` with version read (v1/v2) and year 2024; keep KST/IEEE entry as TODO until readable.
4. Fix [W3]: reword all four "satu-satunya ..." to "satu preseden dalam cakupan brief"; drop any novelty inference built on exhaustiveness.
5. Fix [W5]: keep Bandung/Hugo figures UNVERIFIED and relevance-only; remove "pola yang sama dengan angka internal TA" for Bučko until PMC quote added.
6. Fix [W6]/[W8]/[Q6]: confirm RT-DETR author order, Wu et al. first names, COCO canonical author list, COCO S/M/L thresholds from primary sources before BibTeX-final.
7. Keep [W7] labels: every internal count / duplicate-key / zero-result-process claim stays tagged `internal` / `temuan proses` and is never cited as literature.

## Inline Annotations

> "Prioritas tertinggi: tutup kesenjangan bib IEEE (GhostNet [25], CBAM [26], REG [21], EfficientDet-Indonesia [32], lineage YOLOv3/v4 [34][35]) karena sudah disitasi di proposal tapi belum ada di `references.bib` (status bib internal TA)."
**[W7] MINOR:** Proposal-to-bib gap status is an internal TA claim, not independently verifiable in this pass. Keep the `(status bib internal TA)` label on any reuse; verify against `references.bib` before finalizing.

> "Klaim angka mAP50 70,8% (self-set, 16,5M params, 30,9 GFLOPs, 4,5 ms) dan mAP50 61,2% pada subset RDD2022 berasal dari pembacaan full-text file riset dan belum dire-verifikasi pada potongan yang diambil di pass ini — perlakukan sebagai perlu-konfirmasi-satu-kali sebelum dikutip sebagai fakta [1]."
**[S4-positive]:** Correct hedge, retained. Dataset/module/tiny-focus portion (10.440 citra / 36.579 area, DSCD+MFE+SPPF, retak 1–2 px / pothole <20 px) re-verified against the fetched Scientific Reports full text in this pass; only the headline mAP/latency figures remain confirm-once.

> "Klaim venue NeurIPS 2025 hanya sebagian terverifikasi (catatan OpenAlex mencatatnya sebagai conference-paper 2025) — konfirmasi halaman venue sebelum dikutip [2]."
**[W2] MAJOR:** Overstates what OpenAlex supports. The OpenAlex record re-fetched here (W4407759488) says `conference-paper`, 2025, pp.87151–87175, DOI `10.52202/085713-2627` — no "NeurIPS" string. Remove the venue name until a venue page is produced; cite arXiv:2502.12524 only.

> "FLAG: record arXiv yang sama kini berversi v4 (diperbarui Sep 2026) dengan judul diperluas mencakup YOLO27 ("...YOLO27, YOLO26, YOLO11, YOLOv8, and YOLOv5...") oleh penulis yang sama [3] — sitasi arXiv harus mencantumkan versi yang dibaca."
**[S3-positive]:** Confirmed. arXiv:2510.09653 fetched here shows v1 Oct-2025 through v4 Sep-2026 with the YOLO27-inclusive retitle. Version-pinning requirement stands. Note also that docs now cite the separate paper arXiv:2606.03748 — do not conflate the two IDs.

> "spesifikasi resmi YOLO26n yang terverifikasi langsung dari docs: 40,9 mAP (40,1 NMS-free), 1,7 ms T4 TensorRT, 2,4M params, 5,5B FLOPs, rentang family 40,9–57,5 mAP pada 1,7–11,8 ms, dan hingga 43% lebih cepat pada CPU ONNX vs YOLO11n [4]."
**[S3-positive]:** All figures re-verified verbatim against the fetched Ultralytics YOLO26 docs table/guide text in this pass, including the Intel-Xeon-@2.00GHz CPU-ONNX condition. Safe to cite with hardware/branch conditions attached.

> "Daftar penulis kini terverifikasi dari indeks arXiv: Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei, Guanzhong Wang, Qingqing Dang, Yi Liu, Jie Chen [5]"
**[W6] MINOR:** Author-list verification overclaimed for the artifact fetched. The abs page confirms title/numbers (53.1%/54.3% AP, 108/74 FPS, hybrid encoder, uncertainty-minimal query selection) but the render used here does not expose the full ordered byline. Confirm from PDF/arXiv API before BibTeX-final.

> "model terbaik (ensemble YOLO + Faster-RCNN) mencapai F1 76% pada data uji gabungan enam negara [7]."
**[S2-positive]:** Verified verbatim against the arXiv:2211.11362 abstract fetched in this pass (47.420 citra, 6 negara, 60+ tim/19 negara, lima leaderboard, ensemble YOLO+Faster-RCNN F1 76%). The companion journal figures (76,9% / 16,2–21,2%) correctly remain UNVERIFIED [43].

> "model terbaik (ensemble berbasis YOLO) F1 0,67 (test1) / 0,66 (test2) [8] — menjangkar progres 0,67 (2020) → 0,76 (2022) [7][8]."
**[S2-positive]:** Verified verbatim against arXiv:2011.08740 (26.336 citra, 121 tim, test1 2.631 / test2 2.664, F1 0,67/0,66). The cross-year progression framing is author synthesis across two verified abstracts — acceptable with both citations attached.

> "Studi fondasi crowdsensing smartphone (9.053 citra / 15.435 instance, 7 kota Jepang, 8 kelas, deteksi on-server vs on-phone — angka dari file riset, level abstrak)"
**[S4-positive, with scope note]:** Counts re-verified against arXiv:1801.09454 (9.053 images, 15.435 instances, 7 municipalities, 8 types, GPU-server vs smartphone comparison, 40+ hours acquisition). "7 kota" should read "7 municipalities" to match the source; on-server-vs-on-phone runtime comparison is abstract-supported, exact numbers still need the full text.

> "Satu-satunya framework unsupervised domain adaptation spesifik kerusakan jalan yang ditemukan (file riset): alignment adversarial level-citra + level-instance (importance weighting + RoI multi-scale context), plus RDD2021 100k citra sintetis dari RDD2020."
**[W3] MAJOR + [W1] FATAL (shared passage):** Exclusivity ("satu-satunya ... yang ditemukan") is unprovable from four scoped briefs — reword to scope-of-brief. Independently, the cited DOI `10.1109/TITS.2022.3226018` does not match the OpenAlex record (`10.1109/tits.2022.3221067`, vol.24(3):3091–3103); all method/synthetic-data details remain UNVERIFIED as the draft states, so do not cite figures yet.

> "justru kontras supervised-lokal vs zero-shot-asing adalah bukti domain gap (interpretasi penulis, bukan klaim sumber) [15]."
**[S1-positive, hold the line]:** Interpretation is correctly labeled as penulis, not sumber. Keep Bandung's 93,06% at abstract-level/UNVERIFIED and relevance-only (accuracy-vs-mAP mismatch already noted); do not promote the contrast to a measured gap.

> "Satu-satunya refinement focal spesifik domain jalan yang ditemukan; angka mAP50 80,34 / F1 77,87 kini terkonfirmasi tercantum pada abstrak preprint arXiv (14 halaman)"
**[W3] MAJOR (exclusivity) with verified numbers:** The figures and mechanism (spatial-contextual adjustment + probabilistic refinement, Thai-highway assets) re-verified verbatim against arXiv:2409.09877 abstract + 14-page comment. Keep the numbers citable to the arXiv version read; drop "satu-satunya" or scope it to the brief.

> "kelas manhole ditambahkan karena bentuk bulat meniru pothole; manhole empiris lebih mudah daripada pothole — pola yang sama dengan angka internal TA (bandingan internal, bukan klaim sumber)."
**[W5] MAJOR:** Corroboration use exceeds the evidence. The PMC mirror (PMC9694379) is readable, but the draft still sources the mechanism/pattern to "file riset, level snippet/abstrak". Quote the PMC paragraph before using "pola yang sama" language; until then keep it as candidate-preseden only.

> "Threshold piksel S/M/L perlu verifikasi ulang ke protokol evaluasi resmi saat penulisan (TODO)."
**[W8] MINOR:** Correct TODO, keep attached. COCO totals (2,5M instance / 328rb citra / 91 tipe) re-verified against arXiv:1405.0312; the arXiv-vs-ECCV author-list FLAG is real — finalize BibTeX from the canonical proceedings list.

> "Pencarian paper-DB + web mengembalikan nol sumber cocok (temuan proses dari file riset T1, tanpa URL pendukung)."
**[S5-positive, with label discipline]:** Zero-result process finding has no URL by nature and cannot be independently re-verified here. Correctly kept as process finding with DO NOT CITE; do not rephrase it as a literature fact about the name's nonexistence.

> "Dihapus: ... Dilunakkan menjadi UNVERIFIED: 76,9% / 16,2–21,2% ... −39,8% params YOLO-RD [6]; 81,7%/74,1% Pham [16]; 59,7% Hugo [32]; 43,5%@65FPS YOLOv4 [35]."
**[S1-positive]:** Correct removals/softenings. Each item re-checked: none of these figures appears in a full-text artifact fetched in this pass, so holding them UNVERIFIED is the right call.

## Sources
- [1] Sci. Rep. 15:11032 (RSDD tiny-damage) — https://doi.org/10.1038/s41598-025-95502-z — fetched full-text head; dataset/module/tiny-focus confirmed; headline mAP/latency still confirm-once.
- [2] arXiv:2502.12524 (YOLOv12) — https://arxiv.org/abs/2502.12524 — abstract confirms 40.6% mAP @ 1.64 ms T4, +2.1/+1.2 vs YOLOv10-N/YOLO11-N. OpenAlex W4407759488 (conference-paper 2025, DOI 10.52202/085713-2627, no NeurIPS string) contradicts the NeurIPS tag.
- [3] arXiv:2510.09653 — https://arxiv.org/abs/2510.09653 — v1–v4 history + YOLO27 retitle confirmed.
- [4] Ultralytics YOLO26 docs — https://docs.ultralytics.com/models/yolo26/ — specs table + DFL-free/MuSGD/Progressive-Loss/STAL/NMS-free + CPU-ONNX condition confirmed.
- [5] arXiv:2304.08069 (RT-DETR) — https://arxiv.org/abs/2304.08069 — hybrid encoder, uncertainty-minimal query selection, 53.1%/54.3% AP @ 108/74 FPS confirmed; full ordered byline not confirmed from abs render.
- [7] arXiv:2211.11362 (CRDDC'2022) — https://arxiv.org/abs/2211.11362 — all §3 figures confirmed.
- [8] arXiv:2011.08740 (GRDDC'2020) — https://arxiv.org/abs/2011.08740 — all figures confirmed.
- [9] arXiv:1801.09454 (Maeda preprint) — https://arxiv.org/abs/1801.09454 — 9,053/15,435, 7 municipalities, 8 types confirmed; journal DOI 10.1111/mice.12387 not re-fetched (Wiley 403 per draft accepted as bot-block).
- [14] OpenAlex W4313056423 (DA-RDD) — https://openalex.org/W4313056423 — correct DOI 10.1109/tits.2022.3221067, vol.24(3):3091–3103; exposes the draft's `...3226018` as wrong. IEEE Xplore page not re-fetched; method details remain UNVERIFIED.
- [20] arXiv:2008.13367 (VarifocalNet) — https://arxiv.org/abs/2008.13367 — IACS + Varifocal Loss + star-shaped + FCOS/ATSS, ~2.0 AP, 55.1 AP, CVPR-2021-oral comment confirmed.
- [21] arXiv:2409.09877 (REG) — https://arxiv.org/abs/2409.09877 — 14 pp., mAP50 80.34 / F1 77.87, spatial-contextual + probabilistic refinement confirmed; KST/IEEE pp.324–329 page still unreadable.
- [22] PMC9694379 (Bučko Sensors 22:8878) — https://pmc.ncbi.nlm.nih.gov/articles/PMC9694379/ — mirror readable; manhole-mechanism sentence not yet quoted.
- [23] arXiv:1405.0312 (COCO) — https://arxiv.org/abs/1405.0312 — 2.5M/328k/91-type totals confirmed; author-list discrepancy FLAG confirmed real.
- OpenAlex YOLOv12 + DA-RDD API endpoints (via `feynman_science_database_search`, openalex source): `https://api.openalex.org/works?search=YOLOv12+Attention-Centric+Real-Time+Object+Detectors` and `...?search=DA-RDD+Toward+Domain+Adaptive+Road+Damage+Detection` — anonymous-budget responses returned 5 records each; only W4407759488 and W4313056423 relied upon above.
- Accepted without re-fetch (draft's fetch-blocked/unreadable labels taken at face value, correctly held UNVERIFIED): [6] ScienceDirect YOLO-RD Neurocomputing; [12] ScienceDirect Measurement; [40] MDPI RDD-YOLO; [32] JMLDL PDF (minimal content); [15] JAILCD Bandung page; [16]/[41]/[42]/[43] backup/unfetched items.
