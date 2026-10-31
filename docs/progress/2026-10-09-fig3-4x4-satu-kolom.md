# Fig 3 Jadi 4x4 Satu Kolom

Tanggal: 2026-10-09

## Masalah
Fig 3 (`paper_figG_error_success_cases.png`) memakai `figure*` dua kolom dengan
rasio 1,92 (landscape lebar). User ingin jadi satu kolom teks saja dan tidak lonjong
horizontal.

## Keputusan user
- Layout: 4x4 (4 kolom x 4 baris).
- Isi: 2 kasus gagal + 2 kasus benar.
- Kasus gagal: G1 baris 1 dan 2 (mp4-0036, mp4-0015).
- Kasus benar: diambil dari G2.

## Pilihan kasus (diverifikasi prediksi langsung, conf 0,25)
| Citra | GT | YOLOv12n | YOLO-RD | YOLOv8-PD | Verdict |
|---|---|---|---|---|---|
| 0036 | kosong | Patchy 0,78 | - | Poth 0,69 | gagal (pori ditembak) |
| 0015 | Trans | - | Trans 0,36 | Poth 0,28 | gagal (hampir semua luput) |
| 0436 | Long | Long 0,47 | Long 0,56 | Long x3 | benar |
| 0727 | Long x2 + Trans | Long x2 + Trans x2 | Long x2 + Trans x2 | Long x2 + Trans x2 | benar |

Catatan: 0441 TIDAK dipakai walau ada di G2, karena YOLOv12n salah melabeli
Long jadi Allig 0,33 sehingga tidak bersih untuk baris "benar".

## Script
`scripts/paper/paper_figG_cases.py` (BARU)
- STEMS = [mp4-0036, mp4-0015, mp4-0436, mp4-0727], COLS = GT/v12n/RD/PD.
- Tanpa judul utama, header kolom hanya baris pertama, hspace 0,05.
- CELL = 0,88 inci supaya figure ~3,52 inci, mendekati lebar 1 kolom IEEE (~3,5 inci)
  sehingga saat masuk PDF hampir tidak diperkecil dan label tetap terbaca.
- Output: `latex/IEEE-Conference/gambar/paper_figG_cases_4x4.png` (1073x1053, ratio 1,02).

## Perubahan main.tex (atas izin user)
- Baris 234-239: `figure*` -> `figure`, `width=0.68\textwidth` -> `\columnwidth`,
  gambar `paper_figG_error_success_cases.png` -> `paper_figG_cases_4x4.png`.
- Caption ditulis ulang: 4 baris, dua false alarm dan dua correct detection.
- Prose subsection "Visual Error Examples" diperbarui: menyebut baris 1 (pori),
  baris 2 (retak melintang luput), baris 3 dan 4 (retak memanjang benar).

## Verifikasi
- PNG 1073x1053 rasio 1,02 (persegi), label box terbaca.
- Keempat citra dipastikan berbeda (korelasi antar baris maksimum +0,217).
- Recompile PDF, cek Fig 3 muat satu kolom.
