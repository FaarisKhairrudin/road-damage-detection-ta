# 2026-10-12 — Revisi Bab 4 IEEE: Tabel India 4-kelas + sinkron V4 FINAL + checkpoint git

## Konteks
- Fokus final: `latex/IEEE-Conference/draft/draft-analisis-hasil.md` (V4 FINAL) + `docs/RESULTS_TABLE.md`.
- Pertanyaan user: Tabel 2 India "nggak sejelek itu, kayaknya ~0,4" → ternyata ada dua angka India.

## Temuan cek Tabel India (dari RESULTS_TABLE per-kelas + GT test)
- GT test India (110 citra, 233 instance): Long 47, Trans **6**, Allig 76, Pothole 103, manhole **1**, patchy **0**.
- Angka 0.426–0.443 = agregat Ultralytics 5-kelas `(L+T+A+P+M)/5` — terdongkrak 1 GT manhole 0.995.
  Contoh v8n: (0.273+0.038+0.501+0.323+0.995)/5 = 0.426.
- Angka benar apple-to-apple = agregat 4-kelas inti `(L+T+A+P)/4`: v8n 0.284, v12n 0.293, v26n 0.305, PD 0.299, RD 0.304.
- Justru lebih jelek dari 0.43 karena transverse India kolaps (train 19 → test n=6, skor 0.002–0.214).
- Urutan China ≫ Japan > India identik di 5 model → efek domain, bukan arsitektur.

## Keputusan
- Opsi A dipakai: model tetap 6-kelas, cara hitung rata-rata = 4 kelas inti.
- `main.tex` tab:country-four SUDAH Opsi A (15/15 sel cocok hitung ulang) — draft yang nyusul.

## Verifikasi presisi penuh CSV (koreksi temuan audit sebelumnya)
- Δ dihitung dari presisi penuh lalu dibulatkan — BUKAN selisih angka 4dp.
- v8n Δ full 0.0087659 → +0.0088 (paper benar, draft +0.0087 salah).
- v12n Δ full 0.0016749 → +0.0017 (paper benar, draft +0.0016 salah).
- Wajib-1 audit dicabut: `tab:ablation` LaTeX tidak diubah.
- File 4-kelas final = `runs/rdd_4class_local_pc_lab/*_class_weights_*` (copy PC lab); file `runs/rdd_4class_local/yolov8n_4cls_test_per_class_metrics.csv` adalah non-weighting lama (0.24/0.18) — jangan dipakai.
- Pothole Δ 3dp: v8n +0.020, v12n +0.001, v26n +0.024, PD +0.011 (draft benar).
- `tab:core-transfer` LaTeX (S 0.622/0.626/0.604/0.623/0.633, T 0.303/0.413/0.301/0.342/0.359, drop 51.4/34.1/50.2/45.2/43.4) cocok persis dengan CSV — tidak diubah.
- Source weighted-F1 PD = 0.640 (bukan 0.617/0.618) — dibetulkan di RESULTS_TABLE.
- Zero-shot V4 FINAL (dari domain_gap.csv + zs_per_class_metrics.csv + zs_f1_summary.csv):
  target 0.253/0.337/0.249/0.286/0.302; drop 58.6/45.5/57.5/53.3/51.6;
  macro-F1 0.308/0.383/0.281/0.312/0.336 (drop 46.9/34.5/50.8/47.4/43.6);
  weighted 0.397/0.471/0.370/0.412/0.440 (drop 35.1/23.1/38.1/35.6/29.6);
  per-kelas v12n Long 0.629/Trans 0.256/Allig 0.506/Pothole 0.260/Patchy 0.036.

## Perubahan file (42 insertions, 40 deletions)
1. `draft-analisis-hasil.md` §4.3(c): Δ +0.0087→+0.0088, +0.0016→+0.0017.
2. `draft-analisis-hasil.md` §4.4: tabel → 4-kelas (0.931/0.578/0.284 dst), hapus kolom Gabungan, tambah footnote pembulatan + support India + pointer ke country-four.
3. `draft-analisis-hasil.md` §4.5/4.6: gap 0.88→0.43 jadi 0.93→0.29; V4 ~0.413 (−34%) jadi eksak 0.413 (−34.1%).
4. `main.tex` `tab:source`: Params/GFLOPs → RESULTS_TABLE (3.01/8.2, 2.57/7.5, 2.51/5.9, 2.46/7.7, 7.09/12.9); prosa 5.2→5.9 GFLOPs, 2.47→2.46 M, 12.8→12.9.
5. `main.tex` `tab:country-four`: hapus "Approximate/reconstructed", tambah footnote India n=6/19, manhole excluded.
6. `docs/RESULTS_TABLE.md`: kolom Indonesia V4 → V4 FINAL (0.253/0.337/0.249/0.286/0.302), 514→502 instance, ringkasan F1 + per-kelas V4 → V4 FINAL, footnote 4-kelas vs ultra.

## Git safety
- Tag `v-pre-revisi-bab4-2026-10-12` → HEAD lama 8a1b7ea.
- Commit checkpoint `4fbfb8b` (57 files) sebelum revisi.
- Cara kembali: `git checkout v-pre-revisi-bab4-2026-10-12 -- <file>` (1 file) atau `git reset --hard v-pre-revisi-bab4-2026-10-12` (semua).

## Compile
- `bash latex/IEEE-Conference/compile.sh` sukses: `hasil/main.pdf` + `hasil/Paper_IEEE_Conference.pdf` (7 halaman).

## Sisa (belum dikerjakan)
- Heatmap `per_country_heatmap.png` masih skema ultra lama → regenerasi 4-kelas atau caption disclaimer.
- `rangkuman-eksperimen-ta-v2.md` §5 masih run lama 514 — sinkronkan bila dipakai sebagai konteks writer.
