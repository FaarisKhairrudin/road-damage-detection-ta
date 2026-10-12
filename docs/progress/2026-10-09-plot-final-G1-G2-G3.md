# 2026-10-09 — Plot final kurasi G1/G2/G3 + update draf rapih dan DOCX

## Diskusi
- User memilih dari contact sheet: G1 = 1/9/11 (mp4-0036, 0015, 0041), G2 = 2/3/5 (mp4-0436, 0441, 0727), G3 = 4/5/8 (mp4-0716, 0734, 0768). Minta plot compact hemat tempat: G1 GT+3 model (kilau + pori), G2 GT+3 model, G3 3 model saja, plus analisis dan taruh di draf rapih.
- Window matplotlib tidak bisa dibuka dari environment agent; contact sheet di-render ke PNG dan ditampilkan di chat sebagai gantinya.

## Yang dikerjakan
1. `scripts/paper/view_selection_v4.py` (baru): contact sheet 3 grup ke /tmp/select_v4. Dua hash lama dari list user tidak ada di dataset baru (0015 bd83, 0767 e099) lalu diganti hash baru dengan stem sama (0015 5662, 0767 a99f). Fix checker: zip strict=False, fig.get_axes(), py_compile bersih.
2. `scripts/paper/paper_figs_final_G.py` (baru, run python3.12): inferensi v12n/RD/PD conf 0.25 NMS 0.6 pada 9 citra; output `paper_figG1_glare.png` (3x4), `paper_figG2_correct.png` (3x4), `paper_figG3_predonly.png` (3x3), compact pad 0.4.
3. Analisis hasil: G1 = bukti pori dibaca sebagai kerusakan (0036 GT kosong tapi Patchy 0.78 + Pothole 0.69; 0041 ketiga model miss total). G2 = retak tegas masih dikenali (0436 semua benar, RD 0.56; 0441 v12n salah jadi Alligator; 0727 pola 4 box sama). G3 = perilaku lapangan (0716 sepakat 0.60-0.74; 0734 beda label Patchy vs Long; 0768 RD Manhole 0.45 padahal tanpa manhole di target = bias sumber terbawa).
4. `draft-analisis-rapih.md`: bagian kilau ditambah 3 figur + analisis masing-masing; daftar gambar/tabel diupdate (Gambar 3a/3b/3c). DOCX rapih regenerate 14 MB dan 17 halaman, render LibreOffice diverifikasi halaman 13-15 (G1/G2/G3 tampil penuh).

## Artefak
- `scripts/paper/view_selection_v4.py`, `scripts/paper/paper_figs_final_G.py`
- `latex/IEEE-Conference/gambar/paper_figG1_glare.png`, `paper_figG2_correct.png`, `paper_figG3_predonly.png`
- `latex/IEEE-Conference/draft/draft-analisis-rapih.md`, `laporan-analisis-rapih.docx` (17 halaman)

## Tindak lanjut
- Rerun zero-shot V4 sudah selesai (dataset refinement 514 ke 502 instance, skema CSV dibetulkan, Fig1/Fig2 regenerate). Draf teknis + DOCX v4 menyusul sinkron angka baru bila diminta.
- G2 vs G3: saran simpan G2 bila halaman ketat (ada GT sebagai jangkar), G3 sebagai suplemen perilaku lapangan.
