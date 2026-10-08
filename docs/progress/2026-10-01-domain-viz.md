# 2026-10-01 — Visualisasi domain 3 negara + Indo di ruang fitur YOLO

## Diskusi
Drop zero-shot Indo 73–78% (0.65 → 0.14) memicu pertanyaan: label salah atau
gap visual beneran? Diminta visualisasi perbedaan karakteristik domain
seperti yang model baca (t-SNE/UMAP/setara).

## Eksperimen (`code/07_domain_visualization.ipynb`)
- Full data test per domain, tanpa subsampling
  (China 180, Japan 705, India 110, Indo 308; total 1303 citra).
  Update 15:10: rerun full-data menggantikan versi sampel 100/domain.
- Embedding 256-d dari `model.embed()` YOLOv8n terlatih-sumber (lapisan
  kedua-terakhir) → t-SNE (perplexity 30) + UMAP (n_neighbors 15).
- Pendamping interpretable: brightness/saturasi/kontras/ketajaman (OpenCV) +
  grid contoh citra. Output di `runs/rdd_yolov8n_local/evaluation/domain_viz/`.

## Hasil
- t-SNE dan UMAP sama-sama menunjukkan 4 klaster per domain;
  silhouette ruang 256-d full-data = **0.20**
  (versi sampel seimbang: 0.26 — turun wajar akibat dominasi Japan n=705).
  China paling terisolasi di kedua plot; Indo klaster sendiri dengan sedikit
  overlap tepi ke Japan; India klaster kecil rapat menempel massa Japan.
  Median statistik nyaris identik dengan versi sampel → pola robust.
- Median (n=100/domain): kecerahan Indo 161 (terang) vs Japan 118 (gelap);
  saturasi China 6.6 (nyaris grayscale) vs Japan 46.5; ketajaman China 2220
  vs India 194 (paling blur); kontras China 26 vs Japan 69.
- Grid sampel: China = close-up aspal sibuk, Japan = wide-shot mobil +
  langit/rumah, India = dashboard + kap mobil + debu, Indo = sudut motor,
  beton terang, ruko/motor.

## Solusi / implikasi
- Gap bersifat visual dan terbaca backbone model sendiri → drop Indo bukan
  sekadar artefak label. Figure ini pemecah kebuntuan arah paper: Indo bisa
  tampil sebagai karakterisasi/pilot tanpa jadi klaim utama.
- Caveat untuk naskah: t-SNE/UMAP hanya untuk identifikasi klaster, bukan
  klaim jarak antar-klaster (paper "Stop Misusing t-SNE and UMAP", 2025).
- Referensi: PROBE WACV2026 (frozen ViT + PCA + K-means untuk cross-domain
  road damage), StreetSurfaceVis (CLIP/DINOv2 untuk generalisasi lintas
  dataset), pola t-SNE ala DANN untuk alignment fitur.
