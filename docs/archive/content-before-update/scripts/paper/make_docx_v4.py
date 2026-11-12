#!/usr/bin/env python3
"""Generate latex/IEEE-Conference/draft/laporan-analisis-v4.docx from the V4 draft.

Plain report style: Times New Roman, 1.5 spacing, justified body,
black headings (no blue default), tables + paper figures.

Usage:
  python3 scripts/paper/make_docx_v4.py
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor

REPO = Path(__file__).resolve().parents[2]
EV = REPO / "runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4"
OUT_DOCX = REPO / "latex/IEEE-Conference/draft/laporan-analisis-v4.docx"
FIG1 = REPO / "latex/IEEE-Conference/gambar/paper_fig1_domain_gap_v4.png"
FIG2 = REPO / "latex/IEEE-Conference/gambar/paper_fig2_perclass_collapse_v12n.png"
FIG3 = REPO / "latex/IEEE-Conference/gambar/paper_fig3_qualitative_v4_dummy.png"

BLACK = RGBColor(0, 0, 0)
FONT = "Times New Roman"


def style_document(doc: Any) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(12)
    normal.font.color.rgb = BLACK
    pf = normal.paragraph_format
    pf.line_spacing = 1.5
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_after = Pt(6)
    for i in range(1, 4):
        h = doc.styles[f"Heading {i}"]
        h.font.name = FONT
        h.font.color.rgb = BLACK
        h.font.bold = True
        h.font.size = Pt({1: 16, 2: 13, 3: 12}[i])
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.line_spacing = 1.5
        h.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT


def add_italic(doc: Any, text: str) -> None:
    p = doc.add_paragraph("")
    run = p.add_run(text)
    run.italic = True
    run.font.name = FONT
    run.font.size = Pt(12)


def add_table(doc: Any, headers: list[str], rows: list[list[str]]) -> None:
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    for j, h in enumerate(headers):
        c = t.cell(0, j)
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.name = FONT
        r.font.size = Pt(11)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.text = ""
            r = c.paragraphs[0].add_run(val)
            r.font.name = FONT
            r.font.size = Pt(11)
    doc.add_paragraph("")


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    try:
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    except (OSError, csv.Error) as exc:
        raise RuntimeError(f"cannot read CSV: {path}: {exc}") from exc


MODEL_LABEL = {
    "yolov12n": "YOLOv12n",
    "yolo_rd": "YOLO-RD",
    "yolov8_pd": "YOLOv8-PD",
    "yolov8n": "YOLOv8n",
    "yolov26n": "YOLOv26n",
}


def main() -> None:
    doc: Any = Document()
    style_document(doc)

    sec = doc.sections[0]
    sec.top_margin = Pt(72)
    sec.bottom_margin = Pt(72)
    sec.left_margin = Pt(72)
    sec.right_margin = Pt(72)

    doc.add_heading("Analisis Hasil Eksperimen Deteksi Kerusakan Jalan — V4 Final", level=1)
    doc.add_paragraph(
        "Laporan ini merangkum seluruh analisis yang bisa didapat dari eksperimen: "
        "perbandingan lima model YOLO skala nano pada test sumber N-RDD2024, ablasi distractor "
        "(metrik TRUE overlap yang benar, bukan proxy), variasi per negara sumber, domain gap zero-shot "
        "ke RDD-indo-V4, collapse per-kelas, karakteristik citra per domain, dan studi kasus kilau pagi "
        "sebagai ilustrasi. Semua angka memakai data test. Target yang dipakai hanya V4 "
        "(307 citra, 514 instance, 5 kelas tanpa manhole); V1/V2/V3 tidak dipakai."
    )
    add_italic(
        doc,
        "Sumber angka: docs/RESULTS_TABLE.md, runs/rdd_yolov8n_local/*_test_per_class_metrics.csv, "
        "runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/ (domain_gap.csv, zs_per_class_metrics.csv, "
        "zs_f1_summary.csv), runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv, "
        "dan log docs/progress/2026-09-29-fp-proxy-vs-fp-overlap.md.",
    )

    doc.add_heading("1. Dataset dan Konfigurasi", level=1)
    doc.add_paragraph(
        "Sumber N-RDD2024 subset Asia (6 kelas): 9.670 citra, 24.290 instance, split ~70/20/10. "
        "Imbalance 6 kelas 9,67x didorong patchy_road (test n=69); 4 kelas inti hanya 2,08x. "
        "Target RDD-indo-V4: folder data/RDD-indo-v4 (metadata Roboflow proyek rdd-indo-crop version 3), "
        "307 citra valid dipakai sebagai test, 307 label (39 kosong), 514 instance: longitudinal 235, "
        "transverse 134, pothole 75, alligator 48, patchy 22. Mapping target-ke-sumber {0:2, 1:0, 2:5, 3:3, 4:1}."
    )
    doc.add_paragraph(
        "Training: nano semua model, 300 epoch, imgsz 640, optimizer auto (MuSGD lr 0.01), cos_lr, amp, "
        "deterministic, patience 40; batch 32/16/16/16/8; augmentasi mosaic 1.0, mixup 0.05, fliplr 0.5, "
        "translate 0.10, scale 0.50, tanpa rotasi; class-balanced Effective Number beta=0.999. "
        "Evaluasi conf=0.001, IoU NMS=0.6; visual conf=0.25. FPS di RTX 4070 SUPER, bs=1."
    )

    doc.add_heading("2. Perbandingan Lima Model pada Test Sumber", level=1)
    doc.add_paragraph(
        "YOLO-RD tertinggi di semua metrik agregat (mAP50 0,661, F1 0,633) sesuai filosofi accuracy-first, "
        "tetapi terberat dan terlambat. YOLOv8-PD membuktikan efficiency-first (68% lebih cepat dari baseline, "
        "param terkecil, akurasi setara). YOLOv12n stabil di tengah dan menjadi model terbaik di target V4. "
        "Pothole kelas struktural tersulit (0,526–0,541); manhole termudah (0,82–0,85)."
    )
    add_table(
        doc,
        ["Model", "P", "R", "mAP50", "mAP50-95", "macro F1", "weighted F1"],
        [
            ["YOLOv8n", "0,643", "0,599", "0,648", "0,364", "0,617", "0,636"],
            ["YOLOv12n", "0,638", "0,608", "0,654", "0,371", "0,619", "0,637"],
            ["YOLOv26n", "0,642", "0,580", "0,625", "0,358", "0,606", "0,622"],
            ["YOLOv8-PD", "0,675", "0,591", "0,646", "0,362", "0,627", "0,640"],
            ["YOLO-RD", "0,655", "0,618", "0,661", "0,371", "0,633", "0,650"],
        ],
    )

    doc.add_heading("3. Ablasi Distractor: Latih 6 Kelas vs 4 Kelas", level=1)
    doc.add_paragraph(
        "Koreksi metrik: angka FP di draft lama adalah proxy per-gambar (semua prediksi Pothole di gambar "
        "berpengecoh ikut terhitung tanpa cek box). Untuk yolov8n 6-kelas, proxy 53/390 = 0,1359 sedangkan "
        "TRUE overlap (IoU >= 0,5) hanya 3/390 = 0,0077. Uji-z di atas proxy tidak valid untuk klaim "
        "salah-label dan sudah dibuang. Hasil TRUE overlap: gabungan 0,0026–0,0077 (1–3 prediksi dari 390 GT), "
        "patchy = 0 di semua model, pasangan 6 vs 4 kelas se-arsitektur beda maksimal 1 prediksi. Artinya "
        "salah-label pengecoh sebagai Pothole hampir tidak pernah terjadi, dan tidak ada bukti efek distractor "
        "pada FP beneran. Di sisi mAP pothole, model 4-kelas lebih tinggi di 4/4 pasangan (+0,020, +0,001, "
        "+0,024, +0,011) — tren rugi kecil yang konsisten walau belum diuji signifikansi."
    )
    fp = read_csv_rows(REPO / "runs/rdd_yolov8n_local/fp_overlap_6cls_vs_4cls_test.csv")
    add_table(
        doc,
        ["Model", "nc", "TRUE manhole", "TRUE patchy", "TRUE gabungan"],
        [
            [
                str(r["model"]),
                str(r["nc"]),
                f'{float(str(r["true_manhole"])):.4f}',
                f'{float(str(r["true_patchy"])):.4f}',
                f'{float(str(r["true_total"])):.4f}',
            ]
            for r in fp
        ],
    )

    doc.add_heading("4. Variasi per Negara Sumber", level=1)
    doc.add_paragraph(
        "Pola peringkat identik di semua model (China >> Japan > India), jadi ini efek domain bukan arsitektur. "
        "Japan train 3x China tetapi kalah jauh, sehingga volume bukan penjelas. Concern: agregat 6-kelas "
        "tidak apple-to-apple penuh untuk India (manhole n=1, patchy n=0); untuk klaim paper ulangi pada "
        "4 kelas inti yang sama. Transverse India kolaps (train 19 instance menjadi test 0,002–0,21)."
    )
    add_table(
        doc,
        ["Model", "China (180)", "Japan (705)", "India (110)", "Gabungan (995)"],
        [
            ["YOLOv8n", "0,883", "0,581", "0,426", "0,648"],
            ["YOLOv12n", "0,890", "0,587", "0,433", "0,654"],
            ["YOLOv26n", "0,869", "0,546", "0,443", "0,625"],
            ["YOLOv8-PD", "0,907", "0,570", "0,438", "0,646"],
            ["YOLO-RD", "0,892", "0,594", "0,442", "0,661"],
        ],
    )

    doc.add_heading("5. Domain Gap Zero-Shot ke V4", level=1)
    doc.add_paragraph(
        "Semua model drop 46–59% sehingga benchmark sumber berubah total saat pindah domain. Ranking berbalik: "
        "RD nomor 1 di sumber menjadi nomor 2 di target, v12n nomor 2 di sumber menjadi nomor 1 di target "
        "(0,332). Weighted-F1 drop lebih kecil dari macro-F1 drop, artinya model kurang parah pada kelas "
        "dominan tetapi lebih parah pada kelas langka. Jangan campur angka V2/V3; kenaikan antar-ekspor "
        "adalah efek komposisi dataset, bukan model membaik."
    )
    dg = read_csv_rows(EV / "domain_gap.csv")
    dg.sort(key=lambda r: float(str(r["indo_v4_zs_5cls"])), reverse=True)
    add_table(
        doc,
        ["Model", "Sumber 5-kelas", "V4 5-kelas", "Drop", "V4 macro-F1", "V4 weighted-F1"],
        [
            [
                str(MODEL_LABEL.get(str(r["model"]), str(r["model"]))),
                f'{float(str(r["src_test_5cls"])):.3f}',
                f'{float(str(r["indo_v4_zs_5cls"])):.3f}',
                f'{float(str(r["drop_mAP50_pct"])):.1f}%',
                f'{float(str(r["tgt_macro_f1"])):.3f}',
                f'{float(str(r["tgt_weighted_f1"])):.3f}',
            ]
            for r in dg
        ],
    )
    if FIG1.exists():
        add_italic(doc, "Gambar 1. Domain gap V4 (mAP@0.5 lima kelas bersama).")
        doc.add_picture(str(FIG1), width=Pt(430))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("6. Collapse per Kelas di V4 (YOLOv12n)", level=1)
    doc.add_paragraph(
        "Collapse tidak merata: Longitudinal hampir tidak drop (0,680 menjadi 0,617), Transverse kolaps "
        "(0,582 menjadi 0,258), Alligator turun moderat (0,708 menjadi 0,506), Pothole kolaps (0,535 menjadi "
        "0,246), Patchy hancur (0,587 menjadi 0,035, tetapi n=22). Tanpa patchy, gap 4-kelas inti hanya "
        "-35,1% dibanding -46,3% lima kelas, sehingga patchy memperbesar agregat. Support V4 beda jauh dari "
        "sumber sehingga selisih per-kelas bukan efek domain murni."
    )
    if FIG2.exists():
        add_italic(doc, "Gambar 2. Collapse per-kelas YOLOv12n di V4 + support target.")
        doc.add_picture(str(FIG2), width=Pt(430))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("6b. Kualitatif V4 (DUMMY — 4 Citra Salah Prediksi)", level=2)
    doc.add_paragraph(
        "Empat citra dummy: 0453 (GT 1 transverse) — v12n/RD miss, PD Pothole 0,35 raksasa; "
        "0497 (GT 2 transverse) — v12n benar 1 (0,39), RD/PD miss; "
        "0566 (GT 2 alligator + 1 transverse) — v12n miss, RD Pothole 0,27, PD 3 box bertumpuk; "
        "0572 (GT 1 transverse) — v12n/RD miss, PD Pothole 0,42 raksasa. "
        "Pola: miss retak tipis + over-prediksi pothole besar oleh PD. "
        "Display conf=0,25; evaluasi kuantitatif conf=0,001."
    )
    if FIG3.exists():
        add_italic(doc, "Gambar 3 (DUMMY). GT vs v12n/RD/PD pada 4 citra salah prediksi.")
        doc.add_picture(str(FIG3), width=Pt(430))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("7. Karakteristik Citra per Domain", level=1)
    doc.add_paragraph(
        "Median full data (China 180, Japan 705, India 110, Indo 308): brightness Indo 160,3 (paling terang, "
        "konsisten hipotesis kilau), China 154,8, India 144,0, Japan 119,4; saturasi Japan 44,6 vs China 7,3; "
        "kontras Japan 70,3 vs China 26,8; ketajaman China 2296,8 vs India 181,4 (paling blur). UMAP embedding "
        "256-d YOLOv8n: China terisolasi, Indo klaster sendiri, India menempel Japan; silhouette 0,20. "
        "Concern: set Indo visualisasi n=308 belum tentu sama dengan 307 citra V4; UMAP ilustrasi struktur, "
        "bukan bukti jarak kuantitatif."
    )

    doc.add_heading("8. Studi Kasus Kilau Pagi (Ilustratif)", level=1)
    doc.add_paragraph(
        "Subset pagi VID_20260520_092711: 42 citra, 63 instance (longitudinal 27, transverse 25, pothole 8, "
        "alligator 3, patchy 0, 5 kosong) vs non-pagi 265 citra, 451 instance. Belum ada evaluasi subset "
        "pagi-vs-sisa pada V4 (angka 42 vs 266 di draft lama milik V3), sehingga tidak ada angka pagi turun "
        "yang boleh dilaporkan untuk V4. Komposisi kelas yang beda (pagi tanpa patchy, pothole 8 vs 67) "
        "adalah alasan utama analisis ini ilustratif. Pola failure acak V4 yang konsisten: miss retak dalam "
        "bayangan, prediksi patchy raksasa conf 0,30, dan pothole benar 0,49. Panel kurasi kilau menunggu "
        "daftar filename."
    )

    doc.add_heading("9. Gambar Diagnostik yang Tersedia", level=1)
    doc.add_paragraph(
        "Gambar paper baru: gambar/paper_fig1_domain_gap_v4.png dan gambar/paper_fig2_perclass_collapse_v12n.png "
        "(generator scripts/paper/paper_figs_v4.py). Diagnostik lama: runs/rdd_yolov8n_local/evaluation/domain_viz/ "
        "(samples.png, stats.png, umap.png, tsne.png), evaluation/zero_shot_indo_v4/ (domain_gap.png, "
        "zs_samples_gt_vs_pred.png, zs_samples_pred_only.png), viz_fp_overlap_yolov8n_test.png, dan "
        "gambar/draft_* (draft_domain_gap_v3, draft_gt_vs_3models_indo_morning/rest, draft_morning_vs_rest "
        "memakai V3 sehingga tidak untuk klaim V4; draft_ablasi_6vs4 memakai proxy sehingga perlu regenerasi "
        "dari TRUE overlap bila dibutuhkan)."
    )

    doc.add_heading("10. Yang Masih Perlu Dibuat", level=1)
    for item in [
        "Sinkron angka V4 di main.tex dan ganti gambar/domain_gap.png dengan paper_fig1_domain_gap_v4.png.",
        "Panel kualitatif V4 kurasi (2-3 citra kilau/porous + GT vs v12n/RD/PD) menunggu daftar filename.",
        "Figur metode akuisisi V4 (peta rute + alur video-frame-crop-label).",
        "Confusion matrix + kurva PR pothole v8n 6 vs 4 kelas dari artefak runs.",
        "Opsional: evaluasi subset pagi-vs-sisa V4 + stratifikasi Longitudinal + uji Mann-Whitney.",
        "Suplemen multi-seed bila compute tersedia; jika tidak, pertahankan limitasi single-seed.",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    doc.save(str(OUT_DOCX))
    print(f"wrote {OUT_DOCX} ({OUT_DOCX.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
