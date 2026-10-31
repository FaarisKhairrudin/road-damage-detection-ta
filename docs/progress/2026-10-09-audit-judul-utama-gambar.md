# Audit Judul Utama Gambar Paper IEEE

Tanggal: 2026-10-09

## Aturan
Paper IEEE: gambar tidak boleh punya judul utama di tengah atas. Judul cukup di caption
LaTeX. Sub-judul per panel boleh.

## Audit semua gambar
Flag conditional di `main.tex` saat ini:
`sourceexamples=false, distractoranalysis=true, countryanalysis=true,`
`materialanalysis=true, featurevizanalysis=false`.

Gambar yang MASUK PDF:
| Gambar | Judul utama | Tindakan |
|---|---|---|
| `paper_fig_country_examples.png` (Fig 1) | ADA "Source-domain detection: GT vs 3 models" | diperbaiki |
| `paper_figD4_domains.png` (Fig 2) | tidak ada | sudah bagus |
| `paper_figG_error_success_cases.png` (Fig 3) | tidak ada | sudah bagus |

Gambar ber-flag FALSE (tidak masuk PDF):
| Gambar | Judul utama | Tindakan |
|---|---|---|
| `draft_umap_per_domain.png` | ADA "UMAP embedding YOLOv8n per domain" | diperbaiki |
| `class_examples.png` | hanya sub-judul per panel (Class 0..5) | dibiarkan, sub-judul boleh |

## Perubahan
### `scripts/paper/paper_figs_country.py`
- `fig.suptitle("Source-domain detection...")` DIHAPUS.
- Label baris negara dipindah ke kiri vertikal (miring 90 derajat), sama gaya D4.
- Header kolom `GT / YOLOv12n / YOLO-RD / YOLOv8-PD` hanya di baris pertama.
- `hspace 0.12 -> 0.06`, `wspace 0.06 -> 0.04`, `left 0.02 -> 0.055`.
- `savefig` pakai `pad_inches=0.02`.
- Output: `paper_fig_country_examples.png` 2718 KB (dari 2412 KB).

### `scripts/paper/paper_fig_umap.py` (BARU)
- Reproduksi persis notebook `code/07_domain_visualization.ipynb` cell 6
  (embeddings sama, UMAP n_neighbors=15, min_dist=0.1, random_state=42).
- Hanya bedanya `plt.title('UMAP embedding YOLOv8n per domain')` dihapus.
- Serif, 300 dpi, figsize 4,6x3,4.
- Output: `draft_umap_per_domain.png` 176 KB (dari 89 KB, dpi lama 120).

## Verifikasi
- `paper_fig_country_examples.png` 1862x1389, ratio 1,34.
- `draft_umap_per_domain.png` 1318x959, tanpa judul.
- Caption `main.tex` Fig 1 (baris 152) dan Fig UMAP (baris 275) tetap cocok,
  tidak perlu diubah.

## Catatan
- `class_examples.png` (flag `sourceexamples=false`) punya sub-judul per panel
  "Class 0 (Longitudinal_Crack)" sampai "Class 5 (patchy_road)". Itu sub-judul,
  bukan judul utama, jadi sesuai aturan.
- Generator `class_examples.png` tidak ditemukan di repo (dibuat manual/di luar repo).
