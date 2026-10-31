# 2026-10-12 — Fix LaTeX langsung: provenance V4, tabel negara, FPS, UMAP OFF

## Yang diubah di `latex/IEEE-Conference/main.tex` (18 insertions, 20 deletions)

### 1. Provenance target V4 (Methods → Source and Target Data)
- SEBELUM: "The target images were collected along Jl. Raya Bojongsoang ... yielding approximately 1,000 candidate frames ..." + comment `REVIEW-METHOD [pending]`.
- SESUDAH: "The target evaluation uses a single Roboflow export (`rdd-indo-crop` version 3, stored locally as `data/RDD-indo-v4/`; the local folder name ``v4'' is not a dataset version). Only the export's `valid` split was available (307 images, 307 label files of which 39 are empty, 502 instances) ... remap `{0:2,1:0,2:5,3:3,4:1}` ... manhole excluded rather than scored as zero. This is a single-corridor pilot export, not a representative sample of Bandung or Indonesian roads." + frame-selection/QC diarahkan ke Limitations.
- Efek: tidak ada lagi klaim "data primer Bandung 1000 frame"; jelas ini satu ekspor pilot.

### 2. Tabel negara 4-kelas (Results → Country-Labeled Source Subsets)
- SEBELUM: caption "Approximate ... from rounded per-class country results" + prosa "approximate scores ... reconstructed from rounded entries; exact exports should replace them" + comment `[pending]`.
- SESUDAH: caption final tanpa "Approximate" + prosa "the scores are 0.933, 0.579, 0.293" + comment `[resolved 2026-10-12]: verified 15/15 cells` + footnote baru: "India transverse-crack test support is 6 instances (19 training instances); manhole (1 instance) is excluded and patchy road has no ground truth."
- Angka tidak berubah (sudah benar Opsi A).

### 3. `tab:source` Params/GFLOPs (Results)
- SEBELUM: 3.01/8.1, 2.56/6.3, 2.38/5.2, 2.47/7.6, 7.09/12.8 + prosa 5.2/2.47/12.8.
- SESUDAH: 3.01/8.2, 2.57/7.5, 2.51/5.9, 2.46/7.7, 7.09/12.9 + prosa 5.9/2.46/12.9 (ikut RESULTS_TABLE).
- Comment FPS `[pending]` → `[decided 2026-10-12]: stays as project-recorded estimate; canonical re-evaluation under Limitations`.

### 4. Singkatan IEEE (Methods → Metrics)
- SEBELUM: "average precision (AP) at IoU 0.5 ... macro-averaged F1".
- SESUDAH: "average precision (AP) at intersection-over-union (IoU) 0.5 ... macro-averaged F1-score (F1)"; di Results ditambah "GT denotes the annotated boxes; NMS denotes non-maximum suppression."

### 5. UMAP/feature-viz → OFF untuk submission
- SEBELUM: `\featurevizanalysistrue` → subsection + Fig UMAP ikut ke PDF (8 hlm, UMAP dari ekspor lama 308 citra).
- SESUDAH: `\featurevizanalysisfalse` → subsection hilang dari PDF (7 hlm, cek pdftotext: "UMAP" = 0). File `gambar/draft_umap_per_domain.png` tetap ada; comment diganti `[decided]: excluded from submission (earlier 308-image export, not evaluated 307-image V4); regenerate on frozen V4 for supplement or omit`.
- Aman: tidak ada file gambar yang dihapus; cukup flip satu flag untuk mengembalikan.

### 6. Limitations diperketat
- FPS: "project-recorded throughput estimates, not deployment latency, and need a canonical timed re-evaluation with documented hardware, batch size, warm-up, and timed iterations."
- Target: "single Roboflow export (`rdd-indo-crop` version 3) ... This single-corridor pilot is not a representative sample of Bandung or Indonesian roads."

## Verifikasi
- `bash latex/IEEE-Conference/compile.sh` sukses; PDF 7 halaman (`hasil/main.pdf`, `hasil/Paper_IEEE_Conference.pdf`).
- Cek isi PDF: UMAP=0, "Exploratory Image" hilang, "single-corridor pilot" + "rdd-indo-crop" muncul.
- `git diff 4fbfb8b -- main.tex`: +18/−20, hanya main.tex (draft + RESULTS_TABLE dari revisi sebelumnya tidak disentuh sesi ini).
