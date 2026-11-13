# Penyusunan Bab IV buku TA — 4 November 2026

## Permintaan dan cakupan
Pengguna meminta langsung penyusunan Bab IV berdasarkan hasil aktual dan naskah IEEE, konsisten dengan Bab I–III serta pedoman template. Pengguna juga mengizinkan analisis tambahan dari hasil lokal, termasuk pertimbangan learning curve. Instruksi tersebut menjadi otorisasi penyusunan; tidak menjalankan training atau inferensi baru. Bab I–III, paper, bobot, data, dan abstrak/Bab V tidak diubah.

## Struktur dan sumber
- Pedoman `latex/buku-ta-template/PEDOMAN-PENULISAN.md` §9: tiga bagian utama **Skenario Percobaan**, **Hasil Percobaan**, **Analisis** dipertahankan.
- Rumusan masalah Bab I dan protokol Bab III dipetakan ke deteksi sumber/label pengecoh, efisiensi, dan transfer target.
- Membaca INDEX, RESULTS_TABLE, RESULTS, rangkuman v2, main.tex/note IEEE, audit Oktober 15/30, dan log transformasi sebelumnya. Ringkasan historis tidak otomatis mengalahkan artefak final.
- Sumber utama: lima CSV per-class test enam kelas, `*_summary.json` (waktu validator/FPS), `model_complexity.json` (fused, Ultralytics 8.4.177), target `zero_shot_indo_v4/zs_per_class_metrics.csv`, overlap `fp_overlap_6cls_vs_4cls_test.csv`.
- Pembanding empat kelas native menggunakan `runs/rdd_4class_local_pc_lab/*_4cls_class_weights_test_per_class_metrics.csv`; PD/RD memakai berkas bernama sama di `runs/rdd_4class_local/`. CSV lama tanpa `class_weights` tidak digunakan.
- Hasil negara menggunakan angka tiga desimal pada tabel final paper, dicocokkan dengan keluaran tersimpan `06_per_country_analysis.ipynb`. Tidak membuat digit presisi tambahan dari log yang dibulatkan.
- Notebook 03_1/03_2/03_3 menyimpan `OUTPUT_DIR = REPO_ROOT / "runs/rdd_yolov8n_local"`, pelatihan pada `experiments`; notebook 04_* menunjuk `runs/rdd_4class_local`. Keluaran Windows PC lab masih tersimpan dan data relevan telah disalin lokal.
- Kelima args enam kelas diperiksa: batch16, seed42, epochs300, patience40, optimizer auto; AMP true untuk native, false untuk PD/RD. Riwayat `results.csv` lengkap untuk kelima pelatihan utama.

## Tambahan dan keputusan editorial
1. Satu gambar dua panel mAP@0,5 dan mAP@0,5:0,95 **validasi** per epoch. Data mentah tanpa smoothing; titik pada epoch maksimum mAP50-95. Tidak mengekstrapolasi kurva sesudah early stopping. Kurva mendukung uraian pemilihan bobot/durasi, bukan bukti overfitting atau hasil uji.
2. Epoch terbaik/akhir: v8 108/148; v12 110/150; v26 131/171; PD150/190; RD238/278. Waktu kumulatif CSV: 4,36;4,66;5,28;6,32;11,70 jam.
3. Sembilan tabel: riwayat pelatihan, agregat sumber, AP sumber, kompleksitas/FPS, negara, ablasi+overlap, transfer empat kelas, AP target, tambahan lima kelas. Tabel dipisah agar terbaca pada lebar halaman, caption di atas, header hitam, referensi dan paragraf penjelas setelah setiap objek.
4. Gambar empat kasus target dipakai kembali byte-identical dari `paper_figG_cases_4x4.png`; ambang visual0,25 dibedakan dari AP0,001. Gambar diperiksa, narasi baris mengikuti anotasi/prediksi terlihat. Sebagian label bertumpuk/terpotong dalam panel merupakan bawaan visualisasi paper; tidak menyimpulkan angka confidence yang tidak terbaca dari gambar.
5. Tidak menambah UMAP historis308 citra atau statistik citra yang bukan ekspor target307 citra. Tidak menambahkan semua kurva loss/confusion matrix secara berulang karena belum diperlukan untuk menjawab rumusan masalah.
6. Interpretasi deskriptif: satu seed; rekonstruksi/partial pretraining, AMP dan optimizer auto bukan kontrol arsitektur murni; negara sumber bukan unseen country; target lokal/single annotator; FPS validator bukan benchmark edge. Belum mengukur ketergantungan antar-frame.

## Rekonsiliasi angka dan masalah
- Kompleksitas lama pada RESULTS_TABLE berbeda dari audit final. Memakai JSON fused: v8 3,007M/8,088GFLOPs; v12 2,558/7,306; v26 2,376/5,315; PD2,468/7,730; RD7,086/12,765. Pembulatan mengikuti tabel paper. Tidak menyebut PD model terkecil.
- AP manhole source PD =0,819155; rentang seluruh model 0,819–0,845. Mengoreksi rentang prose paper0,820–0,845 hanya pada Bab IV baru.
- Penurunan lima kelas v12 dihitung ulang dari CSV presisi penuh menjadi45,4% pada satu desimal, bukan45,5% pada ringkasan lama. Tabel dan prosa Bab IV menggunakan hasil hitung yang sama. Empat kelas tetap34,1%.
- Delta ablasi dihitung dari presisi penuh sebelum pembulatan. Karena itu v8+0,0088 dan v12+0,0017 dapat berbeda dari pengurangan angka empat-desimal yang ditampilkan. Catatan ini dijelaskan sesudah tabel.
- FPS empat kelas PD/RD berasal dari RTX3050 dan versi8.4.115 (terlihat pada notebook), berbeda dari sumber utama4070SUPER/8.4.108. Tidak memasukkan FPS tersebut ke perbandingan utama.
- Kata `true` pada CSV overlap adalah nama historis; hanya mengambil `n_true` sebagai **hitungan kotak prediksi**. Tidak menyajikannya sebagai tingkat FP unik atau uji signifikansi.

## Berkas dan reproduksi
- Naskah: `latex/buku-ta-template/Hasil-Percobaan-dan-Analisis.tex`.
- Generator: `scripts/paper/thesis_bab4_assets.py` (CSV stdlib/matplotlib; tidak memuat model).
- Tabel: `latex/buku-ta-template/tabel/bab4-*.tex`.
- Gambar: `gambar/bab4-kurva-validasi.pdf` (vektor); `gambar/bab4-contoh-target.png` (salinan paper).
- Manifest berkas sumber dan SHA-256: `build/bab4-qa/evidence.json`; QA gambar/log di folder sama.
- `python3 scripts/paper/thesis_bab4_assets.py` kemudian `bash latex/buku-ta-template/compile.sh`.
- INDEX dan README diperbarui untuk routing naskah/generator. Pratinjau `bab123` tetap dipertahankan.

## Validasi
Kompilasi penuh berhasil: 61 halaman; Bab IV pada halaman PDF43–58 (halaman isi31–46), 16 halaman. Sembilan tabel dan dua gambar; semua mempunyai label/ref serta penjelasan. Tidak ada error LaTeX, overfull, undefined reference/citation pada log. Underfull akibat gaya template tanpa pemenggalan tetap ada. Kontak render seluruh halaman Bab IV diperiksa, termasuk dua gambar dan tabel. Tidak ada tabel atau objek yang keluar margin halaman. Caption/daftar otomatis mengikuti format template. Berkas final `latex/buku-ta-template/hasil/Template_Buku_TA_FIF.pdf`.
