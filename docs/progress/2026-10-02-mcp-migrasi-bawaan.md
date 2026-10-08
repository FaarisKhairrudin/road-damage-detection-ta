# 2026-10-02 — Migrasi MCP adapter ke bawaan pi 0.99 + uninstall adapter

## Diskusi
Update pi ke 0.99.x menambah MCP + codemode sebagai built-in extension.
`pi mcp list` dari shell cuma menampilkan `mcp` (notion, 44 tools), padahal
di dalam sesi masih ada `mcp__context7`, `mcp__n8n_mcp_homelab`,
`mcp__postgres_homelab`, dsb. Ditanya: apa update-nya, cara uninstall
extension, ada tabrakan atau tidak, dan rekomendasi bawaan vs extension.

## Temuan
- 0.99.0: MCP + codemode + tool_search jadi built-in. Config bawaan di
  `~/.pi/agent/mcp.json` (global) dan `.pi/mcp.json` (project, perlu trust).
  Perintah `pi mcp add/remove/list/login/logout` dan `/mcp` di sesi.
- 0.99.2: server exposure default `codemode` tidak lagi memblokir prompt
  pertama dan tidak lagi disebut di deskripsi `codemode`; ada
  `describeNamespace()` + field `description` per-server untuk ranking
  tool_search.
- Server lama bukan hilang, tapi tinggal di file adapter
  `~/.config/mcp/mcp.json` (context7, n8n-mcp, n8n-mcp-homelab,
  jupyter-agent-bridge, postgres, postgres-homelab, notion). Adapter sengaja
  TIDAK membaca `~/.pi/agent/mcp.json`, begitu pula sebaliknya.
- Tabrakan terkonfirmasi: extension yang mendaftarkan `/mcp` (seperti
  `pi-mcp-adapter`) menggantikan built-in MCP di dalam sesi
  (docs/mcp.md "Replace the built-in MCP support"). `pi mcp` dari shell
  selalu pakai bawaan karena tidak me-load extension.
- Rekomendasi: satu sumber saja. Dipilih migrasi ke bawaan (native, OAuth
  rapi, didukung upstream), extension lain (lens, obsidian, subagents,
  feynman, dsb) tetap dipertahankan karena tidak ada padanan bawaan.

## Solusi diterapkan
1. Backup `~/.pi/agent/mcp.json` (isi awal: hanya `mcp` notion) ke
   `mcp.json.bak.20261002`.
2. Merge 7 server dari `~/.config/mcp/mcp.json` ke `~/.pi/agent/mcp.json`
   (notion didedupe: entri adapter `notion` menggantikan entri lama `mcp`
   agar nama konsisten; tiap server diberi `description` untuk ranking
   tool_search). File lama adapter dibiarkan apa adanya sebagai arsip.
3. Validasi `pi mcp list` (tanpa adapter, dari shell):
   - connected: context7 (2 tools), jupyter-agent-bridge (37),
     postgres-homelab (17), notion (44)
   - failed: n8n-mcp + n8n-mcp-homelab (`fetch failed` — service mati saat
     pengecekan, localhost:5679 dan 100.80.142.51:5679 dua-duanya 000),
     postgres (`ECONNREFUSED 127.0.0.1:5432` — hanya 5433 yang hidup)

## Koreksi port n8n-homelab + disable n8n-mcp lokal
- Fakta dari `docker ps` homelab: `ai-engineer-n8n` expose **5678**, bukan
  5679. Cek langsung: `100.80.142.51:5678` = 200 (root) / 401 tanpa token
  di `/mcp-server/http`; `POST initialize` dengan Bearer token lama
  sukses (`n8n MCP Server v1.1.0`). Port 5679 memang mati di kedua sisi.
- Perbaikan: `n8n-mcp-homelab.url` →
  `http://100.80.142.51:5678/mcp-server/http` di `~/.pi/agent/mcp.json`
  (dan disinkronkan ke `~/.config/mcp/mcp.json` arsip adapter); token
  lama ternyata masih valid, tidak diganti.
- `n8n-mcp` (localhost:5679) di-default-mati via `"enabled": false`
  karena tidak ada docker/n8n lokal di mesin ini (cek: tidak ada port
  5678/5679 listen, `docker` tidak terinstal).
- Validasi ulang `pi mcp list`: connected = context7, n8n-mcp-homelab
  (39 tools), jupyter-agent-bridge, postgres-homelab, notion;
  disabled = n8n-mcp; failed tersisa postgres (:5432 mati).
4. `pi remove npm:pi-mcp-adapter` (removed 26 packages). `settings.json`
   kini 13 packages, adapter hilang. `~/.config/mcp/mcp.json` TIDAK dihapus.

## Tindak lanjut
- Jalankan ulang `pi` lalu `/reload`, cek `/mcp` di dalam sesi: harusnya
  7 server bawaan tampil tanpa tool `mcp__*` model adapter.
- `n8n-mcp` lokal disabled by default; enable lagi (`"enabled": true`
  atau hapus field) saat n8n lokal sudah ada.
- Token Bearer n8n lama masih valid saat dicek (init sukses); tetap
  pertimbangkan rotasi + pindah ke env var karena plaintext di config.
- Hidupkan postgres :5432 bila butuh server `postgres`, atau disable
  (`"enabled": false`) agar tidak `failed` di `pi mcp list`.
- Pertimbangkan pindah secret (Bearer n8n, DATABASE_URL) ke env var
  `${...}` agar tidak plaintext di `mcp.json`.
