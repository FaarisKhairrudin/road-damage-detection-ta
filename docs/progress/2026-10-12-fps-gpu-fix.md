# 2026-10-12 — FPS defensible: GPU di-fix ke RTX 4070 SUPER, tanpa subbab setup

## Keputusan user
- Tidak buat subbab "Experimental Setup" (7 halaman, mahal).
- Cukup inline mention RTX 4070 SUPER (bukan klaim semua eksperimen di GPU itu).
- Hapus bahasa ragu-ragu ("unreconciled", "canonical timed re-evaluation").

## Dasar bukti
- Log `docs/RESULTS.md` (10 blok eval): RTX 4070 SUPER 12282MiB, Ultralytics 8.4.108,
  torch 2.5.1+cu121, Python 3.12.3 → semua FPS kolom tabel sumber dari sini.
- FPS = 1000/(pre+inf+loss+post) ms per citra, terverifikasi 5/5 model vs JSON artefak.
- Re-run test v8n di RTX 3050 (bg bb9f5b3db): mAP50 0.6476 = catatan 4070 →
  mAP tidak tergantung GPU; hanya FPS hardware-dependent.

## Edit main.tex (7 blok)
1. III-B +1 kalimat: "Source-domain training and throughput measurement used an
   NVIDIA GeForce RTX 4070 SUPER 12 GB GPU."
2. Comment `[decided]` → `[resolved]` dengan detail protokol + bukti re-run 3050.
3. Prosa "highest recorded throughput estimate" → "highest measured throughput".
4. Footnote tabel: "Project-recorded estimate ... unreconciled" → end-to-end latency
   (pre+inf+post) di RTX 4070 SUPER 12GB, Ultra 8.4.108, PyTorch 2.5.1, CUDA 12.1,
   imgsz 640, 995 citra; throughput estimate bukan edge benchmark.
5. Caption tabel: hapus "; FPS is a project-recorded estimate" (detail pindah footnote).
6. Limitations: "need a canonical timed re-evaluation ..." → "end-to-end throughput
   on the RTX 4070 SUPER evaluation harness, not standalone benchmarks with dedicated
   warm-up or batch-size sweeps, not edge-device latency".
7. Conclusion: "standardized timing" dihapus dari daftar kebutuhan.

## Verifikasi compile
- Sukses, 7 halaman. PDF: 'RTX 4070 SUPER'=2, 'unreconciled'=0,
  'canonical timed re-evaluation'=0, 'throughput measurement used'=1.
