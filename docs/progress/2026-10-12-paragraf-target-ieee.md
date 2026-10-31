# 2026-10-12 — Paragraf target V4 gaya IEEE (Kandidat A writer)

## Masalah
Paragraf Methods hasil fix sebelumnya repo-ish: menyebut path lokal `data/RDD-indo-v4/`,
ribut versi Roboflow v3 vs folder v4, mencantumkan remap dict `{0:2,...}` di badan teks.

## Solusi (atas arahan user)
Spawn subagent `writer`: tulis ulang gaya IEEE final — "target diambil di mana, pakai apa, dapat berapa".
Tanpa path lokal, tanpa chatter versi, tanpa remap dict di badan teks.

## Hasil (Kandidat A, dipilih user, sudah dipasang ke main.tex)
> The target data were obtained from the RDD-indo dataset, collected using a
> road-facing smartphone at 1080p with one frame sampled per second along the
> Bojongsoang–Buah Batu corridor in Bandung, Indonesia. The set comprised 307
> images and 502 annotated instances across five classes; 39 images contained
> background only. The valid split was reused as the test set, with no
> target-domain training. Longitudinal cracks dominated the annotations
> (231 instances), whereas patchy-road instances were sparse (21); the data
> represented a single-corridor pilot.

Detail versi ekspor (`rdd-indo-crop` version 3) tetap ada SATU kali — di Limitations,
bukan Methods. Cek PDF: `data/RDD-indo-v4`=0, `remap`=0, `single-corridor pilot`=1,
`Bojongsoang`=1. Compile sukses 7 halaman.
