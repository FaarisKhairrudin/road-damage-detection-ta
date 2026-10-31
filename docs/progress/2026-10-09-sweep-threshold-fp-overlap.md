# Sweep Threshold Tabel FP/GT Pothole vs Pengecoh

Tanggal: 2026-10-09

## Pertanyaan user
Tabel FP yang membandingkan prediksi Pothole melawan pengecoh (manhole, patchy_road)
memakai conf=0,25 dan IoU match 0,5. User penasaran: kalau threshold diturunkan,
apakah hasilnya berubah dan jadi berapa.

## Keputusan user
- Sweep conf **dan** IoU match sekaligus.
- **Dicatat di markdown saja**, tabel/angka di draf TIDAK diubah dulu.
- Model: 5 arsitektur 6-kelas (v8n, v12n, v26n, v8pd, RD).

## Metode
- Script baru: `scripts/fp_overlap_threshold_sweep.py`.
- Satu kali inferensi pada conf=0,001 (iou NMS 0,60, imgsz 640) untuk 272 citra test
  berpengecoh, 5 model 6-kelas.
- Semua prediksi Pothole disimpan bersama IoU maksimum terhadap GT manhole dan
  patchy_road, lalu tabel dihitung ulang untuk tiap kombinasi threshold.
- Sweep conf: 0,001 / 0,01 / 0,05 / 0,1 / 0,25 / 0,5.
- Sweep IoU match: 0,3 / 0,5 / 0,7.
- Penyebut tetap: manhole 321, patchy 69, gabungan 390.

## Output
- `runs/rdd_yolov8n_local/fp_overlap_conf_sweep_raw.csv` — 6061 baris prediksi Pothole mentah.
- `docs/analisis-threshold-fp-overlap.md` — 3 blok tabel (gabungan / manhole / patchy) x 3 IoU.

## Validasi
Di conf=0,25 dan IoU match=0,5 hasilnya 3/2/1/2/3 untuk v8n/v12n/v26n/v8pd/RD.
Ini **persis sama** dengan tabel lama (`fp_overlap_6cls_vs_4cls_test.csv`:
0,0077/0,0051/0,0026/0,0051/0,0077 x 390). Script baru tervalidasi.

## Temuan
1. **Turunkan conf = naikkan jumlah.** Gabungan di IoU 0,5: v8n dari 3 (conf 0,25) ke 21
   (conf 0,001), sekitar 7 kali. Tapi tidak meledak tak terbatas, tetap puluhan dari 390 GT.
2. **Urutan model berubah di conf rendah.** Di conf 0,25 v26n paling rendah (1), di
   conf 0,001 v26n jadi tertinggi di IoU 0,5 (30). Artinya v26n punya banyak box pothole
   berkeyakinan rendah yang tepat menimpa manhole.
3. **Patchy road tetap nol** di conf >= 0,1 untuk SEMUA model dan SEMUA IoU. Temuan lama
   "tidak ada prediksi pothole menimpa patchy" sangat robust. Baru muncul di conf 0,001
   (maksimum 9 oleh v26n).
4. **Anomali v26n di IoU 0,7**: 24 tumpang tindih di conf 0,001, jauh di atas model lain
   (3 sampai 10). Box pothole v26n sering sangat presisi menimpa manhole.
5. Tabel lama di conf 0,25 bersifat **konservatif**. Klaim "nyaris tidak ada salah label
   pengecoh" bertahan, bahkan diperkuat karena patchy tetap nol.

## Catatan metodologis
Penyebut tetap (390 GT) membuat angka ini naik tanpa batas atas saat conf diturunkan.
Beda dengan mAP yang punya kurva presisi-recall. Jadi angka di conf rendah lebih tepat
dibaca sebagai "seberapa agresif model menembak" bukan "seberapa sering salah label".

## Belum dikerjakan
- Draf dan tabel paper belum diubah (sesuai permintaan user).
- Belum dibuat gambar/plot dari hasil sweep ini.
