# Status proyek TA

## Tujuan besar
Menyelesaikan penelitian dan buku Tugas Akhir program Data Science Telkom
University sebagai bagian dari persyaratan kelulusan. Pertahankan tujuan ini
lintas sesi; pekerjaan satu sesi adalah bagian dari tujuan tersebut.

## Tahap sekarang
- Paper konferensi ISRITI sudah disubmit menurut pengguna. Status penerimaan atau
  hasil review belum diketahui; jangan menyebut paper sudah diterima/terbit.
- Fokus proyek berlanjut ke penyusunan dan penyempurnaan buku TA di
  `latex/buku-ta-template/`, sesuai arahan pembimbing dan pedoman kampus.
- README template mencatat Bab I–IV sudah berupa draf; abstrak, Bab V dan
  lampiran masih perlu disusun. Periksa file aktual sebelum pekerjaan lanjutan.

## Progres penting
- Repo riset telah ditata dan hasil final didokumentasikan; riwayat arsip ada
  di `docs/REORGANIZATION.md` dan `docs/archive/MANIFEST.json`.
- Analisis domain V4 selesai: 995 gambar sumber + 307 target, embedding
  1.302 × 256, beserta UMAP/t-SNE/statistik. Ini analisis eksploratif.
- Tabel hasil final dan narasi bergambar ada di `docs/RESULTS_TABLE.md` dan
  `docs/draft-analisis-rapih.md`; perhatikan cakupan kelas dan batas klaim.
- Snapshot paper review terunggah dipertahankan di `latex/ISRITI-submission/hasil/`.

## Pekerjaan tersisa dan hal yang perlu dipantau
- Lanjutkan buku TA sesuai permintaan pengguna: tinjau draf yang ada, lengkapi
  bagian yang masih berupa petunjuk, dan selaraskan isi dengan hasil final.
- Jika ada tanggapan konferensi atau arahan pembimbing, ikuti instruksi terbaru
  pengguna; jangan mengubah snapshot paper yang sudah disubmit.
- Kurva training PD empat kelas `results.csv` belum ditemukan. Jangan mengganti
  dengan run lain atau mengarang data.
- Source buku `latex/buku-ta-template/` ditambahkan ke Git atas izin pengguna,
  beserta aset, bibliografi, panduan dan script pembuat tabel/kurva Bab IV.
- Notebook 07 memiliki perubahan lokal yang sudah ada sebelumnya; pertahankan.

## Acuan dan pemeriksaan
- Mulai dari `docs/INDEX.md`, `.agents/MEMORY.md` dan `docs/FINAL_ARTIFACTS.json`.
- Pedoman penulisan: `latex/buku-ta-template/PEDOMAN-PENULISAN.md`.
- Referensi 40 dependensi TeX dan syntax script kompilasi buku diperiksa; isi
  source dipertahankan. Tidak dilakukan training, eksekusi notebook atau build PDF.

## Tindakan berikutnya
Tunggu tugas buku TA berikutnya dari pengguna; sebelum menulis, baca bab yang
relevan dan pedomannya. Perbarui progres di tempat tanpa mengganti tujuan besar.
