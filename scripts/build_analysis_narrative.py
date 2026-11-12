"""Build the illustrated Indonesian analysis from final CSVs and the V4 domain bundle.
No training, inference, manuscript rewriting or notebook execution.
"""
from pathlib import Path
import json
import pandas as pd
from domain_bundle import completed_bundle

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'runs/rdd_yolov8n_local/evaluation/final_report'
DOMAIN=ROOT/'runs/rdd_yolov8n_local/evaluation/domain_viz_v4'
MODELS=['yolov8n','yolov12n','yolov26n','yolov8_pd','yolo_rd']
DISPLAY=dict(zip(MODELS,['YOLOv8n','YOLOv12n','YOLO26n','YOLOv8-PD','YOLO-RD']))
CLASS={0:'Retak memanjang',1:'Retak melintang',2:'Retak buaya',3:'Lubang jalan',4:'Manhole',5:'Patchy road'}


def number(value,digits=3):return f'{float(value):.{digits}f}'.replace('.',',')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'---|'*len(headers)]+['| '+' | '.join(map(str,r))+' |' for r in rows])
def fig(caption,name):return f'![{caption}](figures/{name})'


def main():
    load=lambda n:pd.read_csv(REPORT/(n+'.csv'))
    source=load('source_six_class').set_index('model').loc[MODELS]
    transfer=load('transfer_four_class').set_index('model').loc[MODELS]
    ablation=load('ablation_four_vs_six').set_index('model').loc[MODELS]
    country=load('country_four_class').set_index('model').loc[MODELS]
    supp=load('supplementary_five_class').set_index('model').loc[MODELS]
    source_pc=load('source_per_class');target_pc=load('target_per_class')
    distribution=pd.read_csv(ROOT/'runs/rdd_yolov8n_local/dataset_class_distribution.csv')
    provenance=completed_bundle(DOMAIN)
    medians=pd.read_csv(DOMAIN/'domain_medians.csv') if provenance is not None else None
    s=[]
    def add(text):s.append(text.strip())
    add('# Analisis Hasil Eksperimen Deteksi Kerusakan Jalan')
    add('Dokumen naratif ini mengikuti artefak final pada [peta artefak](FINAL_ARTIFACTS.json) dan [tabel hasil](RESULTS_TABLE.md). Tabel/grafik akurasi dihitung dari CSV final tanpa training ulang. Regenerasi visualisasi domain V4 disiapkan melalui script terpisah; status pelaksanaannya dijelaskan pada bagian analisis domain. Notebook lama, naskah LaTeX dan PDF submission tidak ditulis ulang.')
    add('## Ringkasan temuan')
    add('YOLO-RD hasil reimplementasi memperoleh mAP@0,5 tertinggi pada uji sumber enam kelas, yaitu 0,661. Pada transfer empat kelas kerusakan yang sama, YOLOv12n memperoleh nilai target tertinggi 0,413 dari nilai sumber 0,626, dengan penurunan relatif 34,1%. Model yang memimpin di sumber karena itu tidak selalu memimpin pada target yang diuji. Semua perbandingan ini berasal dari satu seed per konfigurasi.')
    add('Pelatihan empat versus enam kelas menghasilkan perubahan kecil dan tidak seragam pada mAP empat kelas. Diagnostik overlap hanya menemukan 1–3 kotak pothole yang bertumpang tindih dengan anotasi distractor per konfigurasi. Temuan tersebut belum menetapkan manfaat yang konsisten dari penambahan label manhole dan patchy road.')
    add('## Data dan batas perbandingan')
    add('N-RDD2024 subset China, Jepang dan India terdiri dari 6.777 gambar latih, 1.898 validasi dan 995 uji, dengan 24.290 anotasi pada inventaris enam kelas. Validasi dipakai untuk pemilihan checkpoint; tabel hasil utama memakai test. Penanganan ketimpangan adalah effective-number weighting pada BCE klasifikasi dengan beta 0,999, bukan Focal Loss.')
    add(table(['Kelas','Latih','Validasi','Uji','Total'],[[CLASS[int(r.class_id)],int(r.train),int(r.val),int(r.test),int(r.total)] for r in distribution.itertuples()]))
    add('Target final adalah ekspor Roboflow rdd-indo-crop versi 4, dengan 307 gambar dan 502 anotasi; 39 gambar memiliki label kosong. Split valid dipakai sebagai uji target, tanpa fine-tuning. Tidak ada anotasi manhole. Semua gambar dipertahankan, termasuk background. Empat kelas kerusakan berjumlah 481 anotasi, sedangkan 21 anotasi patchy road menjadi kelas tambahan.')
    t=target_pc[target_pc.model=='yolov12n'].sort_values('class_id')
    add(table(['Kelas target','Anotasi','Persentase dari 502'],[[CLASS[int(r.class_id)],int(r.support),number(100*r.support/502,1)+'%'] for r in t.itertuples() if r.support>0]))
    add('Overall sumber memakai enam kelas. Transfer utama dan perbandingan negara memakai empat kelas kerusakan yang sama (D00, D10, D20, D40). Hasil lima kelas bersama, termasuk patchy road dan tanpa manhole, disajikan terpisah. Mengganti cakupan kelas mengubah rata-rata, sehingga nilai 0,413 empat kelas tidak boleh dilabeli sebagai nilai 0,337 lima kelas atau sebaliknya.')
    add('## Akurasi dan biaya komputasi di sumber')
    add(table(['Model','mAP@0,5','mAP@0,5:0,95','F1 makro','Parameter fused (juta)','GFLOPs fused','FPS arsip'],[[DISPLAY[m],number(r['mAP50']),number(r['mAP50-95']),number(r['f1']),number(r.params_M_fused,2),number(r.GFLOPs_fused,1),number(r.FPS_archived,1)] for m,r in source.iterrows()]))
    add(fig('Akurasi pada uji sumber enam kelas','final_results/source_accuracy.png'))
    add('YOLO-RD memimpin mAP@0,5 dan F1 makro pada run sumber ini. mAP@0,5:0,95 YOLOv12n dan YOLO-RD sama-sama membulat menjadi 0,371, sehingga tidak tepat menyebut YOLO-RD unggul mutlak pada seluruh metrik. Model custom merupakan rekonstruksi lokal dengan transfer bobot parsial; perbandingan tidak mengisolasi efek arsitektur.')
    add(fig('Akurasi versus throughput arsip dan ukuran model','final_results/efficiency_tradeoff.png'))
    add('YOLO26n memiliki estimasi parameter dan GFLOPs terendah di antara kelima checkpoint fused. YOLOv8-PD memiliki throughput terukur tertinggi pada perangkat pengujian arsip. FPS berasal dari RTX 4070 SUPER dan protokol preprocessing, inference, serta postprocessing yang tercatat; ini bukan benchmark perangkat edge atau jaminan real-time pada perangkat lain. Kompleksitas mengikuti audit fused model, bukan konstanta lama pada script.')
    add(fig('AP per kelas pada sumber','final_results/source_per_class.png'))
    add('AP pothole sumber berada sekitar 0,526–0,541, sedangkan AP manhole sekitar 0,819–0,845. Perbedaan ini menggambarkan kelas dan split yang diuji; bentuk objek atau mekanisme arsitektur tidak diuji secara terpisah sebagai penyebab. Patchy road hanya memiliki 69 anotasi uji, sehingga interpretasinya memerlukan kehati-hatian.')
    add('## Ablasi label dan diagnostik distractor')
    add(table(['Model','mAP empat kelas: training 6','Training 4','Delta (4 − 6)','Overlap pothole 6 / 4'],[[DISPLAY[m],number(r.six_class_training_mAP50,4),number(r.four_class_training_mAP50,4),f'{r.delta_four_minus_six:+.4f}'.replace('.',','),f'{int(r.six_class_pothole_overlap_boxes)} / {int(r.four_class_pothole_overlap_boxes)}'] for m,r in ablation.iterrows()]))
    add(fig('Ablasi himpunan label pada empat kelas kerusakan','final_results/ablation_four_vs_six.png'))
    add('Training empat kelas menghasilkan mAP sedikit lebih tinggi pada empat arsitektur dan sedikit lebih rendah pada YOLO26n. Perubahan YOLO-RD sebesar +0,0180 adalah pengamatan satu pasangan run, bukan hasil uji signifikansi. Konfigurasi AMP custom empat kelas berbeda dari enam kelas; RD juga memiliki perbedaan workers dan warmup, yang dicatat dalam tabel konfigurasi.')
    add('Overlap dihitung sebagai jumlah kotak prediksi pothole dengan confidence minimal 0,25 yang menyentuh minimal satu box distractor pada IoU minimal 0,5. Terdapat 321 anotasi manhole dan 69 patchy road. Seluruh overlap yang tercatat melibatkan manhole; patchy road nol. Numerator ini bukan matching unik objek dan bukan false-positive rate. Proxy lama yang menghitung prediksi pada seluruh gambar mengandung distractor tidak digunakan untuk klaim tersebut.')
    add('## Perbedaan antarnegara sumber')
    add(table(['Model','China (180 gambar)','Jepang (705)','India (110)'],[[DISPLAY[m],number(r.China),number(r.Japan),number(r.India)] for m,r in country.iterrows()]))
    add(fig('Perbandingan negara dengan empat kelas yang sama','final_results/country_four_class.png'))
    add('Nilai negara berasal dari tabel paper pada presisi tiga desimal, bukan presisi tambahan yang direka dari log yang telah dibulatkan. China memiliki skor tertinggi dan India terendah pada kelima model. Ukuran subset, distribusi objek dan tampilan citra berbeda; pola ini tidak membuktikan bahwa negara, jumlah data atau satu ciri visual tertentu menyebabkan selisih tersebut.')
    add('![Contoh anotasi per negara](../latex/IEEE-Conference/gambar/paper_fig_country_gt.png)')
    add('Sampel berlabel memperlihatkan variasi tampilan dari subset sumber. Ini adalah ilustrasi terpilih, bukan pengukuran frekuensi setiap kondisi visual.')
    add('![Contoh GT dan prediksi per negara](../latex/IEEE-Conference/gambar/paper_fig_country_examples.png)')
    add('Contoh GT versus prediksi menunjukkan keberhasilan dan kegagalan individual. Contoh tersebut membantu inspeksi, tetapi tidak dapat menggantikan metrik seluruh subset atau membuktikan penyebab perbedaan skor.')
    add('## Transfer utama ke Indonesia V4: empat kelas yang sama')
    add(table(['Model','Sumber','Target V4','Penurunan relatif','F1 makro target (4 kelas)'],[[DISPLAY[m],number(r.source_mAP50),number(r.target_mAP50),number(r.relative_drop_pct,1)+'%',number(r.target_macro_f1)] for m,r in transfer.iterrows()]))
    add(fig('Transfer empat kelas sumber dan Indonesia V4','final_results/transfer_four_class.png'))
    add('YOLOv12n memperoleh target mAP@0,5 tertinggi pada V4. YOLO-RD yang memimpin empat kelas sumber sebesar 0,633 mencapai 0,359 di target. Penurunan dihitung dari nilai tanpa pembulatan dengan 100 × (1 − target/source). Hasil ini mendukung pemilihan model berdasarkan evaluasi target yang relevan, tetapi belum menetapkan model terbaik untuk seluruh Indonesia.')
    add(fig('AP per kelas pada Indonesia V4','final_results/target_per_class.png'))
    src12=source_pc[source_pc.model=='yolov12n'].set_index('class_id');tgt12=target_pc[target_pc.model=='yolov12n'].set_index('class_id')
    add(table(['Kelas YOLOv12n','AP sumber','AP target','Selisih sumber − target','Anotasi target'],[[CLASS[c],number(src12.loc[c,'mAP50']),number(tgt12.loc[c,'mAP50']),number(src12.loc[c,'mAP50']-tgt12.loc[c,'mAP50']),int(tgt12.loc[c,'support'])] for c in [0,1,2,3,5]]))
    add('Pada YOLOv12n, longitudinal crack mempertahankan AP lebih tinggi dibanding transverse crack dan pothole pada target ini. Patchy road memiliki AP rendah dengan hanya 21 anotasi. Pengamatan permukaan berpori dan pencahayaan dapat menjadi hipotesis untuk pemeriksaan lanjutan, tetapi hasil agregat dan contoh pilihan tidak mengidentifikasi faktor penyebabnya.')
    add('## Tambahan: lima kelas bersama')
    add(table(['Model','Sumber (5 kelas)','Target (5 kelas)','Penurunan relatif','F1 makro target (5 kelas)'],[[DISPLAY[m],number(r.source_mAP50),number(r.target_mAP50),number(r.relative_drop_pct,1)+'%',number(r.target_macro_f1)] for m,r in supp.iterrows()]))
    add(fig('Evaluasi tambahan lima kelas bersama','final_results/supplementary_five_class.png'))
    add('Nilai YOLOv12n 0,337 pada lima kelas tetap valid sebagai hasil tambahan. Perbedaan dari 0,413 pada empat kelas muncul karena penambahan patchy road ke rata-rata. F1 berbobot memakai support GT sedangkan F1 makro memberi bobot sama pada setiap kelas; keduanya harus dibandingkan dalam cakupan kelas yang sama. Ambang P/R/F1 mengikuti ambang mean-F1 optimal split pada Ultralytics, bukan confidence tampilan contoh.')
    if provenance is not None:
        add('## Karakter citra dan fitur: regenerasi pada V4')
        add('Analisis eksploratif ini kini memakai 1.302 gambar: China 180, Jepang 705, India 110, dan Indonesia V4 307. Seluruh sampel sumber dan target dicatat beserta hash gambar/label dalam manifest. Statistik dihitung pada resolusi citra asli; perbedaan resolusi, kamera, framing dan komposisi adegan ikut memengaruhi ukuran ini.')
        add(fig('Empat sampel per domain dari manifest V4 dengan seed 42','domain_v4/samples.png'))
        add(fig('Distribusi statistik citra pada V4 dan uji sumber','domain_v4/stats.png'))
        add(table(['Domain','Kecerahan: mean V','Kejenuhan: mean S','Kontras: std gray','Ketajaman: var Laplacian','Gambar'],[[r.domain]+[number(getattr(r,k),1) for k in ['brightness','saturation','contrast','sharpness']]+[int(r.images)] for r in medians.itertuples()]))
        add('Tabel berisi median antar-gambar atas masing-masing statistik. Varian Laplacian adalah proxy ketajaman yang peka terhadap tekstur dan resolusi, bukan ukuran kualitas kamera yang terisolasi. Statistik ini deskriptif dan tidak menjelaskan selisih AP secara kausal.')
        add(fig('UMAP embedding YOLOv8n pada source test dan Indonesia V4','domain_v4/umap.png'))
        add(fig('t-SNE dari embedding dan manifest V4 yang sama','domain_v4/tsne.png'))
        add(f'Fitur berdimensi {provenance["embedding_shape"][1]} diambil dari layer {provenance["inputs"]["embedding_layer"]} checkpoint YOLOv8n final, dengan input 640 piksel lalu normalisasi L2. UMAP memakai n_neighbors=15, min_dist=0,1, seed=42; t-SNE memakai perplexity=30, init PCA, seed=42. Silhouette deskriptif pada ruang fitur ternormalisasi adalah {number(provenance["silhouette_normalized_feature_space"])}. Koordinat dan jarak dua dimensi tidak merupakan ukuran fisik domain shift atau bukti penyebab kegagalan deteksi. Klaster/tumpang tindih harus dibaca sebagai struktur eksploratif dari fitur model ini.')
        add('Regenerasi memakai torch '+provenance['inputs']['versions']['torch']+', Ultralytics '+provenance['inputs']['versions']['ultralytics']+' dan device '+provenance['inputs']['device']+'. Lingkungan ini dicatat sebagai environment analisis baru, terpisah dari environment training/benchmark arsip. Bundle V2 lama tetap diarsipkan dan tidak ditimpa.')
    else:
        add('## Analisis domain V4 — ditunda')
        add('Regenerasi embeddings, UMAP, t-SNE, statistik dan sampel pada 995 gambar sumber + 307 gambar V4 belum selesai. Pengguna meminta proses yang memerlukan GPU ditunda sampai setelah restart. Ekstraksi CPU dihentikan; keluaran parsial tidak dipakai sebagai hasil final atau dasar kesimpulan.')
        add('Bundle domain lama berisi 995 sumber + 308 target Indonesia V2 dan tetap berada di arsip. Grafik V2 tidak ditampilkan sebagai hasil V4 di dokumen ini. Notebook lama dipertahankan. Setelah eksekusi V4 diizinkan kembali dan berhasil, dokumen ini dapat dibangun ulang untuk memasukkan statistik serta proyeksi yang sesuai.')
    add('## Contoh kesalahan dan deteksi pada target')
    add('![GT dan prediksi empat contoh target](../latex/IEEE-Conference/gambar/paper_figG_cases_4x4.png)')
    add('Kolom memperlihatkan GT, YOLOv12n, YOLO-RD dan YOLOv8-PD pada confidence tampilan 0,25. Contoh mencakup prediksi patchy/pothole pada permukaan tanpa anotasi damage, transverse crack yang terlewat atau salah lokasi, serta longitudinal cracks yang terdeteksi dengan kotak tambahan. Patchy road dalam contoh tetap observasi kualitatif di luar rata-rata transfer empat kelas. Contoh terpilih tidak mengukur frekuensi kesalahan dan tidak mengisolasi pengaruh kilau atau tekstur.')
    add('## Kesimpulan dan batas bukti')
    add('Pada eksperimen yang tercatat, YOLO-RD memimpin akurasi sumber, YOLOv12n memimpin transfer V4, dan YOLOv8-PD memiliki throughput arsip tertinggi. Training empat versus enam kelas tidak menetapkan manfaat yang konsisten dari label distractor. Evaluasi Indonesia mencakup area terbatas dengan satu anotator, dan eksperimen memakai satu seed. Generalisasi geografis, variasi seed serta hipotesis pencahayaan/tekstur memerlukan evaluasi lanjutan. ' + ('Analisis domain V4 yang diperbarui bersifat eksploratif dan tidak mengubah angka deteksi arsip atau isi paper yang sudah disubmit.' if provenance is not None else 'Regenerasi domain V4 masih ditunda; ketika dilanjutkan, hasilnya tidak otomatis mengubah angka deteksi arsip atau isi paper yang sudah disubmit.'))
    add('## Reproduksi dan sumber')
    add('1. `python3.12 scripts/build_final_results.py` meregenerasi tabel/grafik dari CSV final.\n2. `python3.12 scripts/domain_analysis_v4.py --device 0 --resume` menggunakan folder V4 terpisah dan memeriksa kecocokan input cache. Pastikan CUDA tersedia; gunakan direktori output baru untuk eksperimen terpisah.\n3. `python3.12 scripts/build_analysis_narrative.py` membangun ulang narasi dari tabel final saat ini; bagian V4 baru ditambahkan setelah bundle domain berstatus lengkap dan hash output terverifikasi.\n\nDetail input, hash, versi dan parameter ada dalam `runs/rdd_yolov8n_local/evaluation/final_report/provenance.json` dan, setelah run V4 berhasil, `domain_viz_v4/provenance.json`. Bukti mentah tetap pada [RESULTS.md](RESULTS.md); catatan lokasi/status tersedia pada [INDEX.md](INDEX.md).')
    text='\n\n'.join(s)+'\n'
    (ROOT/'docs/draft-analisis-rapih.md').write_text(text)
    print('Wrote narrative with',text.count('!['),'figures.')


if __name__=='__main__':main()
