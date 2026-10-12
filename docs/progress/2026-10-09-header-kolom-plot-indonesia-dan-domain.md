# Plot Indonesia dan Domain: Header Kolom Tunggal

Tanggal: 2026-10-09

## Permintaan
- Gambar Indonesia (G1/G2/G3/dummy) kembali dirapikan: label cukup sekali di paling atas
  sebagai header kolom, mis. `GT  YOLOv12n  YOLO-RD  YOLOv8-PD`.
- Panel "Karakter Citra Tiap Domain" (D3/D4) hapus judul utama di atas gambar.
- Label baris China / Japan / India / Indonesia tetap dipertahankan.

## Perubahan
### `scripts/paper/paper_figs_final_G.py`
- `panel_fig` tidak lagi menerima `title`/`with_gt`.
- Judul per sel (`GT {stem} n=..`, `{Model} n=..`) dihapus.
- Header kolom hanya di baris pertama (`if i == 0: ax.set_title(c, fontsize=8, pad=3)`).
- Gridspec: `hspace=0.06, wspace=0.04, top=0.93`.
- `draw_pred` tidak lagi perlu mengembalikan jumlah box.

### `scripts/paper/paper_fig3_qualitative_v4.py`
- Judul per sel dihapus, header kolom hanya di baris pertama.
- Loop disederhanakan (`for i, img_path in enumerate(paths)`), variabel `stem` tidak dipakai lagi.
- `hspace 0.18 -> 0.06`, `top 0.96 -> 0.93`.

### `scripts/paper/paper_figs_domains.py`
- `fig.suptitle(...)` dibuang, `top 0.90 -> 0.99`.
- Label domain vertikal di kolom pertama tetap dipertahankan.

## Output (regenerate via python3.12 + python3)
- `paper_figG1_glare.png` 2534 KB
- `paper_figG2_correct.png` 2297 KB
- `paper_figG3_predonly.png` 1848 KB
- `paper_fig3_qualitative_v4_dummy.png` 3738 KB
- `paper_figD3_domains.png` 1912 KB
- `paper_figD4_domains.png` 2543 KB

## Sinkron narasi
`latex/IEEE-Conference/draft/draft-analisis-rapih.md` bagian studi kasus kilau (G1/G2/G3)
dan dummy Fig3 disesuaikan: karena penanda nomor citra di gambar sudah dihapus, narasi
memakai acuan "baris pertama sampai baris ketiga/keempat" dengan nomor citra tetap
disebut di teks (0036/0015/0041, 0436/0441/0727, 0716/0734/0768, 0453/0497/0566/0572).

## Catatan
- Citra kanan baris Indonesia D4 masih memuat traffic cone merah. Pengganti steril
  (0436, 0437, 0433) siap dipakai bila diminta.
- Verifikasi visual: header kolom muncul sekali di atas, tidak ada judul besar,
  label baris domain utuh.
