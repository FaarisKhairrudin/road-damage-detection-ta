# 2026-10-09 — Draft analisis V4 final + figur paper IEEE-ready + laporan DOCX

## Diskusi
- Draft `latex/IEEE-Conference/draft/draft-analisis-hasil.md` masih memakai angka V3 dan metrik FP proxy yang sudah terbukti salah (log 2026-09-29). Diminta: semua pakai V4, betulkan FP, taruh semua analisis yang bisa didapat + concern keterbandingan, sediakan contoh gambar + kode di folder baru, update MD, generate MD→DOCX laporan biasa (TNR, spasi 1.5, justify, heading hitam bukan biru).

## Audit sebelum tulis ulang
- `runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv` (test, conf=0.25, IoU match ≥0.5; GT manhole=321, patchy=69): TRUE gabungan 0.0026–0.0077 (1–3 prediksi/390 GT); TRUE patchy=0 semua model; pasangan 6vs4 se-arsitektur beda ≤1 prediksi → tidak ada bukti efek distractor pada FP beneran. Proxy lama (v8n 0.1359 vs TRUE 0.0077) dibuang + uji-z proxy dibuang.
- V4: 307 citra valid, 307 label (39 kosong), 514 instance; komposisi target id (0=allig 48, 1=long 235, 2=patchy 22, 3=poth 75, 4=trans 134). Subset pagi VID_20260520_092711: 42 citra/63 instance (long 27, trans 25, poth 8, allig 3, patchy 0, 5 kosong); non-pagi 265 citra/451 instance. Belum ada evaluasi subset pagi-vs-sisa pada V4 (angka 42 vs 266 di draft lama milik V3) → tidak ada klaim "pagi turun X%" untuk V4.
- Per-country 6-kelas (China 0.87–0.91, Japan 0.55–0.59, India 0.43–0.44) tidak apple-to-apple penuh untuk India (manhole n=1, patchy n=0) → catat concern, rujuk agregat 4-inti untuk klaim paper.
- Domain viz Indo n=308 (ekspor lama) vs evaluasi V4 n=307 → jangan klaim UMAP menjelaskan angka V4 langsung.
- Bobot final 4-kelas dari PC lab: `runs/rdd_4class_local_pc_lab/*_test_per_class_metrics.csv` (v8n 0.6311, v12n 0.6280, v26n 0.6036) + PD lokal 0.6341. File `runs/rdd_4class_local/yolov8n_4cls_test_per_class_metrics.csv` adalah run gagal (0.27) — jangan dipakai.

## Yang dikerjakan
1. `scripts/paper/paper_figs_v4.py` (baru, folder baru `scripts/paper/`): baca `domain_gap.csv` + `zs_per_class_metrics.csv` + source per-class CSV, output `latex/IEEE-Conference/gambar/paper_fig1_domain_gap_v4.png` + `paper_fig2_perclass_collapse_v12n.png` (English, serif, 300 dpi, ~7 in). Fix: `parents[2]`, label overlap (ylim + legend lower-left + support n di xtick Fig2).
2. `latex/IEEE-Conference/draft/draft-analisis-hasil.md`: tulis ulang penuh ke V4 — §4.3 diganti TRUE overlap + mAP pothole + agregat 4-inti; §4.5/§4.6 angka V4 dari `domain_gap.csv`; §4.7 pagi jadi ilustratif + komposisi terverifikasi filesystem; §4.4/§4.7 concern keterbandingan eksplisit; lampiran angka V4 final.
3. `scripts/paper/make_docx_v4.py` (baru): python-docx → `latex/IEEE-Conference/draft/laporan-analisis-v4.docx` (TNR, spasi 1.5, justify, heading hitam, tabel + Fig1/Fig2 + daftar gambar diagnostik). Lihat hasil di bawah.

## Artefak
- `scripts/paper/paper_figs_v4.py`, `scripts/paper/make_docx_v4.py`
- `latex/IEEE-Conference/gambar/paper_fig1_domain_gap_v4.png` (137 KB), `paper_fig2_perclass_collapse_v12n.png` (114 KB)
- `latex/IEEE-Conference/draft/draft-analisis-hasil.md` (ditulis ulang)
- `latex/IEEE-Conference/draft/laporan-analisis-v4.docx`

## Tindak lanjut (menunggu user)
- List filename Indo kurasi (kilau + porous + over-prediksi) → panel kualitatif V4 GT vs v12n/RD/PD baru.
- Sinkron `main.tex` ke angka V4 + ganti `gambar/domain_gap.png` → `paper_fig1_domain_gap_v4.png`.
- (Opsional) evaluasi subset pagi-vs-sisa V4 + stratifikasi Longitudinal + Mann-Whitney brightness.

## Update 2026-10-09 — Fig3 DUMMY dari 7 citra "Salah prediksi"
- User memberi 7 nama Merge-1 (0453/0497/0566/0572/0571/0554/0570); ketujuh file + label ketemu di V4.
- GT: 0453 trans×1; 0497 trans×2; 0566 allig×2+trans×1; 0572 trans×1; 0571 poth×1; 0554 allig+poth+trans; 0570 allig+2poth.
- Script baru `scripts/paper/paper_fig3_qualitative_v4.py` (run dengan `python3.12` karena ultralytics hanya ada di python3.12; `python3` default tidak punya modul). Patch custom via `custom_modules.patch_ultralytics()` untuk PD/RD. Default 4 baris, `argv 6` untuk 6 baris (0571/0554 cadangan; 0570 baris ke-7 tidak dipakai default).
- Output `latex/IEEE-Conference/gambar/paper_fig3_qualitative_v4_dummy.png` (3,7 MB, 4×4 GT+v12n/RD/PD, conf display 0.25). Pola: 0453 v12n/RD miss + PD Pothole 0.35 raksasa; 0497 v12n benar 1 (0.39), RD/PD miss; 0566 v12n miss, RD Pothole 0.27, PD 3 box bertumpuk; 0572 v12n/RD miss + PD Pothole 0.42 raksasa.
- Draft §4.9 + DOCX (§6b, Gambar 3) diupdate; DOCX regenerate 3,9 MB / 7 halaman, render LibreOffice diverifikasi per halaman.
