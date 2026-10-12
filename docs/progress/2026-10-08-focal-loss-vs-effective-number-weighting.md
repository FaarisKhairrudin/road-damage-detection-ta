# 2026-10-08 — Klarifikasi Focal Loss dan pembobotan kelas pada paper

## Diskusi / masalah
- Proposal merencanakan Focal Loss, sedangkan hasil final yang dilaporkan pada paper memakai run bernama `*_class_weight`. Kalimat lama paper menyebut "Focal Loss was not the active imbalance intervention"; penulis meminta deskripsi metode yang lebih relevan tanpa membahas rencana proposal.
- Klaim bahwa Task-Aligned Assigner pada YOLOv8 ke atas telah mengatasi sebagian besar ketimpangan foreground--background tidak didukung: assigner memilih lokasi positif, sedangkan classification BCE masih dihitung pada keluaran semua lokasi/kelas, termasuk label negatif/background.
- Focal Loss (Lin dkk., arXiv:1708.02002, ICCV 2017) memodulasi contoh mudah dan semula dimotivasi oleh banyaknya negatif mudah pada dense detection. Effective-number class weighting (Cui dkk., arXiv:1901.05555, CVPR 2019) menggunakan jumlah contoh per kelas untuk bobot relatif. Keduanya tidak eksklusif: Cui dkk. membahas kombinasi class-balanced focal loss pada §4.3. Task-aligned learning TOOD (Feng dkk., arXiv:2108.07755) berfokus pada alignment assignment klasifikasi/lokalisasi, bukan bukti penghapusan semua negatif mudah.

## Pemeriksaan implementasi
- `code/03_3_modelling_comparative_local.ipynb` menghitung bobot dari instance train dengan rumus `(1-beta)/(1-beta**n)`, dinormalisasi agar jumlah bobot sama dengan banyak kelas, `beta=0.999`; bobot enam kelas yang tercatat sekitar `[0.761, 0.784, 0.763, 0.848, 0.840, 2.004]`.
- Notebook tersebut menambal `DetectionModel.init_criterion` pada tingkat kelas agar model yang dibuat ulang oleh Trainer menerima `class_weights`. Blok Focal Loss lama dalam notebook ini dikomentari; notebook eksperimen Focal terpisah bukan sumber hasil final paper.
- Sumber Ultralytics lokal 8.4.115 di `/home/varys/.local/lib/python3.12/site-packages/ultralytics/utils/loss.py` memakai `BCEWithLogitsLoss(reduction='none')`, lalu mengalikan tensor BCE `(batch, anchors, classes)` dengan `class_weights` per kanal kelas sebelum reduksi. Pemeriksaan kecil pada logits nol/semua target negatif menunjukkan bobot berlaku juga untuk term negatif. Hasil training yang tercatat menggunakan Ultralytics 8.4.108; pemeriksaan lokal 8.4.115 menguatkan pembacaan kode, bukan audit ulang langsung terhadap seluruh run historis.
- Dengan demikian frasa yang presisi adalah **effective-number-derived per-class weighting of the BCE classification component**, adaptasi inspirasi Cui dkk., bukan klaim implementasi identik formula per-sampel Cui atau keunggulan empiris atas Focal Loss. Belum ada ablasi loss.

## Solusi pada naskah
- Di `latex/IEEE-Conference/main.tex`, ganti dua kalimat lama dengan: “To account for unequal training-instance counts across classes, we applied effective-number-derived per-class weights ($\beta=0.999$) to the binary-cross-entropy classification component of the detection loss \cite{cui2019class}.”
- Kalimat negatif mengenai Focal Loss dihapus dari paper konferensi karena bukan metode aktif yang perlu dijelaskan ke pembaca. Jangan menambahkan klaim bahwa TAL membuat Focal Loss redundant atau bahwa bobot kelas meningkatkan AP tanpa pembanding unweighted/Focal.

## Sumber daring
- https://arxiv.org/abs/1708.02002 — Lin dkk., Focal Loss for Dense Object Detection.
- https://arxiv.org/html/1901.05555v1 — Cui dkk., Class-Balanced Loss Based on Effective Number of Samples (khususnya §4.3).
- https://arxiv.org/abs/2108.07755 — Feng dkk., TOOD/Task Alignment Learning.
- https://docs.ultralytics.com/reference/utils/loss/ — dokumentasi kode loss Ultralytics (versi daring terkini, tidak otomatis sama dengan versi training historis).
