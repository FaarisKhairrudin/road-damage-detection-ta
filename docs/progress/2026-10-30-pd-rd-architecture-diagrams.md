# Diagram arsitektur reimplementasi PD dan RD

## Permintaan dan sumber
Pengguna meminta diagram bergaya paper asli, disesuaikan dengan implementasi lokal dan tidak terlalu ramai. Figure 2 PD pada halaman 4 PDF lokal dan Figure 2 RD pada halaman 6 diperiksa secara visual. Sumber implementasi: code/models/yolov8-pd.yaml, yolo-rd.yaml, custom_modules.py, dan README.md.

## Implementasi
Dibuat scripts/paper/paper_fig_architectures.py memakai ReportLab untuk PDF vektor. Dua panel memakai kotak pastel, garis tipis, serta pengelompokan backbone/neck/head. PD menggambarkan rute top-down dan bottom-up dengan C2fGhost/LSKA dan keluaran LSCD tiga skala. RD menggambarkan backbone SOM, tiga tap ARM, fusion top-down adaptasi lokal (Upsample/Concat/Conv1x1), PAN yang diringkas sebagai grup, serta tiga keluaran WT-Head. Channel, repeat, dan detail internal modul sengaja tidak ditampilkan; ini skema tingkat grup, bukan visualisasi setiap layer.

## Keluaran dan batas
PDF: latex/IEEE-Conference/gambar/paper_fig_architectures.pdf. PNG pratinjau pada folder yang sama. Gambar dibuat ulang dari struktur kode, bukan menyalin artwork asli. Saat dipasang di paper, caption harus mengutip Zeng2024 dan Wang2025 serta menjelaskan reimplementasi dan pengelompokan. Belum dimasukkan ke main.tex: pratinjau diberikan dahulu karena label dua panel berdampingan menjadi kecil bila diperkecil ke lebar halaman IEEE. Perlu pemilihan layout cetak setelah pengguna meninjau gambar.

## Validasi
PDF dirender dan diperiksa: tidak ada label terpotong atau kotak bertumpuk. Rute tingkat grup diperiksa terhadap YAML; jumlah input/output tiga skala konsisten. Tidak ada perubahan model, bobot, hasil, atau angka paper. INDEX diperbarui untuk script baru.

## Perbaikan rendering font
Pengguna melihat font seperti bertabrakan. Pratinjau awal memang bermasalah: glyph tampak bergaris/berkontur dan sukar dibaca. Font bawaan PDF diganti Liberation Sans TTF tertanam dan mode render teks disetel fill (mode 0) secara eksplisit. PDF dan PNG dibuat ulang, lalu diperiksa visual: karakter solid, antarbaris jelas, label tidak melewati batas kotak. Perbaikan ini tidak mengubah rute arsitektur.

## Versi detail per layer
Pengguna menyetujui pembuatan ulang setelah versi ringkas dinilai terlalu sederhana. Script baru paper_fig_architectures_detailed.py menghasilkan dua PDF/PNG terpisah: architecture_pd_detailed dan architecture_rd_detailed. Seluruh node YAML ditampilkan (head multi-input digambarkan sebagai tiga cabang dari satu head), dengan nomor layer, ukuran feature map, channel, repeat aktual, dan setiap sambungan input. Detail internal tiap modul tidak diurai; tingkat detail mengikuti diagram arsitektur utama pada paper asal. Nilai channel/repeat dihitung dari scales n dan aturan parser lokal, bukan channel konfigurasi asli sebelum scaling. SOM nominal 8/5 menjadi 3/2 setelah depth 0.33. Ukuran spasial setiap input Concat diperiksa konsisten. Font TTF tertanam dan mode fill dipertahankan. Render diperiksa dan jarak judul group/input diperbaiki agar tidak menimpa. Belum dipasang ke main.tex, sesuai tahap pratinjau gambar.

## Penghapusan judul dan catatan dalam gambar
Atas permintaan pengguna, judul model, subjudul konfigurasi, dan tiga baris catatan bawah dihapus pada kedua diagram detail. Halaman PDF dipangkas untuk menghilangkan ruang kosong bekas teks. Label bagian, layer ID, dimensi, repeat, dan koneksi tetap ada. Metadata judul PDF tetap tersedia. Penjelasan scaling, arti layer ID/dimensi, shared head, serta adaptasi fusion dapat dimasukkan dalam caption saat penyisipan ke naskah.

## Uji penyisipan dalam paper
Pengguna meminta dimasukkan untuk melihat apakah melewati 7 halaman. Dua PDF detail dipasang sebagai satu figure dua kolom dengan panel berdampingan, dirujuk dari III-B, caption menjelaskan layer ID/dimensi/scaling/adaptasi dan menyitir kedua paper asal. Hasil kompilasi: 6 halaman, arsitektur Fig. 2 pada halaman 3. Render diperiksa; panel tidak terpotong atau bertumpuk, tetapi label internal kecil pada ukuran cetak karena detail tinggi. Ini versi pratinjau; memperbesar tiap panel layak dipertimbangkan bila keterbacaan lebih diprioritaskan daripada ruang.

## Diagram dikeluarkan dari naskah utama
Setelah meninjau ukuran cetak, pengguna menyetujui penghilangan diagram dari naskah utama. Figure dua panel dan kalimat rujukannya dihapus, sementara file PDF/PNG serta script tetap disimpan. Methods diperjelas dengan nano depth/width scaling dan adaptasi fusion YOLO-RD memakai Upsample/Concat/Conv1x1 alih-alih formulasi weighted-sum asal. Diagram belum dilampirkan ke suplemen; hanya dikeluarkan dari main.tex.
