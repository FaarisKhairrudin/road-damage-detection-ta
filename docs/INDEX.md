# INDEX — Project Context Map (for AI & humans)

> **Purpose of this file:** a single entry point for finding *which file contains what* in this repo, without reading everything. If you are an LLM/agent new to this project, **read this file first**, then jump to the relevant files via the routing tables below.
>
> **How to use:** find your question in [§3 Quick Routing Table](#3-quick-routing-table-looking-for-x--open-y), open the 1–3 files it points to, and do not sweep the whole repo. Section [§7 Constraints & Pitfalls](#7-constraints--pitfalls-you-must-know) is mandatory reading before asserting any number.

- **Last audited:** 2026-10-09 (filesystem audit; content reflects the repo state at that time).
- **Scope:** all Git-*tracked* files + local result folders (`runs/`, `data/`, `latex/**/build/`) that are Git-*ignored*. Binary dataset/image files are not enumerated individually — only structure and key files.

---

## 1. Project Identity (brief)

| Item | Value |
| --- | --- |
| Title | Comparative Evaluation and Generalization Testing of Deep Learning Architectures for Road Damage and Surface Defect Detection in Indonesia |
| Author | Faaris Khairrudin — NIM 103052300115 — Data Science Program, Telkom University |
| Advisor | Dr. Gamma Kosala, S.Si. |
| Core | Compare 5 nano-scale YOLO detectors on the N-RDD2024 Asia subset (6 classes), then test zero-shot generalization to Indonesian road data |
| 5 models | `yolov8n`, `yolov12n`, `yolov26n`, `yolov8_pd` (reconstruction), `yolo_rd` (reconstruction) |
| 6 source classes | `Longitudinal_Crack`, `Transverse_Crack`, `Alligator_Crack`, `Pothole`, `manhole`*, `patchy_road`* (*= distractor classes) |
| Imbalance intervention | *Effective-number* per-class weighting (β=0.999) on the BCE classification component — **not** Focal Loss |
| Deliverables | TA proposal, thesis draft (Telkom), IEEE Conference paper draft |

---

## 2. Directory Structure (macro map)

```text
TA-Project/
├── README.md                 # Setup & how to run (for humans)
├── AGENTS.md                 # Working rules for agents (must be followed)
├── docs/                     # ← DOCUMENTATION & RESULTS (start here)
│   ├── INDEX.md              #   ← THIS FILE
│   ├── RESULTS.md            #   Raw Ultralytics evaluation log (val & test)
│   ├── RESULTS_TABLE.md      #   Tidy tables from RESULTS.md + per-country + zero-shot
│   ├── rangkuman-eksperimen-ta.md      # Experiment summary v1 (partly superseded)
│   ├── rangkuman-eksperimen-ta-v2.md   # Experiment summary v2 (FINAL CONTEXT for writers)
│   ├── proposal.pdf          #   TA proposal (binary, gitignored)
│   └── progress/             #   Per-date bug/discussion/decision logs (MUST be written)
├── code/                     # Training/evaluation notebooks & scripts
│   ├── 00_EDA.ipynb … 07_domain_visualization.ipynb
│   ├── models/               # YOLOv8-PD & YOLO-RD reconstructions (code + yaml + README)
│   └── *.py                  # confusion_6cls_vs_4cls.py, prepare_4class_dataset.py
├── scripts/                  # Support scripts: Streamlit viewers, packaging, FP overlap
├── data/                     # Datasets (gitignored; see data/README.md)
│   ├── NRDD-2024/            #   source 6-class + RDD_4class (derived)
│   ├── RDD-Indonesia.v1i.yolov8/, RDD-indo-v2/, -v3/, -v4/   # Indonesian targets
│   └── archive/              #   Raw Indonesian imagery
├── runs/                     # Training/evaluation outputs (gitignored, ~5 GB)
├── latex/                    # Manuscripts: proposal, IEEE paper, thesis
│   ├── PROPOSAL_TA.md        #   Token-efficient proposal index
│   ├── IEEE-Conference/      #   IEEE paper draft (main.tex, draft/, gambar/)
│   ├── skripsi-telkom/       #   Telkom thesis draft (per-chapter .tex)
│   ├── figures/              #   Shared figures (distribution, architecture, methodology)
│   └── refference/           #   Reference paper PDFs (11 files) — NB: typo "refference"
└── outputs/                  # Deep-research output for extra references (T1–T4 + provenance)
```

---

## 3. Quick Routing Table ("looking for X → open Y")

### 3a. Questions about results & numbers

| I want to know… | Open |
| --- | --- |
| Final mAP/F1 for all models (tidy tables) | `docs/RESULTS_TABLE.md` |
| Raw evaluation log (verbatim Ultralytics output) | `docs/RESULTS.md` |
| Experiment context summary for writing the paper | `docs/rangkuman-eksperimen-ta-v2.md` (**use this**, not v1) |
| Methodological decisions + list of bugs fixed | `docs/rangkuman-eksperimen-ta.md` §4–§6 |
| Zero-shot results on Indonesia (mAP50, F1, drop) | `docs/RESULTS_TABLE.md` §"Hasil Zero-Shot RDD-indo-v4"; CSV details in `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/` |
| Per-source-country results (China/Japan/India) | `docs/RESULTS_TABLE.md` §"Per-Negara"; artifacts in `runs/rdd_yolov8n_local/per_country/` |
| 6-class vs 4-class comparison (ablation) | `docs/RESULTS_TABLE.md` §"Training 4 Kelas"; `runs/rdd_4class_local/` |
| FP *proxy* vs FP *overlap* analysis (optional) | `docs/progress/2026-09-29-fp-proxy-vs-fp-overlap.md`; `scripts/fp_overlap_table.py`, `scripts/viz_fp_overlap.py` |

### 3b. Questions about code & reproduction

| I want to know… | Open |
| --- | --- |
| How to train the comparative 6-class models (final) | `code/03_3_modelling_comparative_local.ipynb` |
| How to train the 4-class ablation | `code/04_1`…`04_4_modelling_4class.ipynb` (one model per notebook) |
| How to prepare the 4-class dataset | `code/prepare_4class_dataset.py` |
| How to run the Indonesia zero-shot test | `code/05_zero_shot_indo_v4.ipynb` (final), `05_zero_shot_indo_v2.ipynb` |
| How to do per-country analysis / domain visualization | `code/06_per_country_analysis.ipynb`, `code/07_domain_visualization.ipynb` |
| YOLOv8-PD / YOLO-RD architecture (reconstruction) | `code/models/README.md` + `custom_modules.py` + `*.yaml` |
| Interactive dataset/prediction viewer (Streamlit) | `scripts/visualize_streamlit.py`, `zero_shot_viewer_v4.py` |
| How to build an experiment artifact package | `scripts/package_experiment.py` |
| Python dependencies | `code/requirements_yolov8_local.txt` |

### 3c. Questions about manuscripts & references

| I want to know… | Open |
| --- | --- |
| Proposal structure & content (token-efficient) | `latex/PROPOSAL_TA.md` |
| IEEE paper draft | `latex/IEEE-Conference/main.tex` + `draft/draft-analisis-hasil.md` + `note.md` |
| Telkom thesis draft per chapter | `latex/skripsi-telkom/{Pendahuluan,Kajian-Pustaka,Metodologi,Hasil-dan-Pembahasan,Kesimpulan-dan-Saran}.tex` |
| IEEE paper bibliography | `latex/IEEE-Conference/references.bib` |
| Thesis bibliography | `latex/skripsi-telkom/References.bib` |
| Reference paper PDFs (local full text) | `latex/refference/` (11 PDFs, numbered 01–11) |
| Extra references from deep research | `outputs/yolo-road-damage-references.md` (+ `.provenance.md`) |
| Notes on items not yet validated in the paper | `latex/IEEE-Conference/note.md` |
| How to compile LaTeX | `latex/IEEE-Conference/compile.sh`, `latex/skripsi-telkom/compile.sh` |

### 3d. Questions about data

| I want to know… | Open |
| --- | --- |
| Which datasets exist & their classes | `data/README.md` + `data/*/data.yaml` |
| Source 6-class dataset | `data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/` |
| Derived 4-class dataset | `data/NRDD-2024/RDD_4class/` |
| Indonesian target dataset (which version is used) | `data/RDD-indo-v4/` (final); see [§7](#7-constraints--pitfalls-you-must-know) about version naming |
| Raw Indonesian imagery | `data/archive/` |

### 3e. Questions about decision/bug history

| I want to know… | Open |
| --- | --- |
| All progress logs (chronological) | `docs/progress/` (full table in [§5](#5-docs--documentation--results)) |
| Why class-weight instead of Focal Loss | `docs/progress/2026-10-08-focal-loss-vs-effective-number-weighting.md` |
| Why the FP number in the old notebooks is a *proxy* | `docs/progress/2026-09-29-fp-proxy-vs-fp-overlap.md` |
| RDD-indo-v4 audit details & final-context assembly | `docs/progress/2026-10-08-rdd-indo-v4-and-summary.md` |
| `class_result` positional bug + per-class F1 | `docs/progress/2026-10-08-zero-shot-v4-dan-f1-per-kelas.md` |
| Shi_2026 / YOLO-LWD claim verified from a local PDF | `docs/progress/2026-10-02-cek-klaim-shi-2026.md` |

---

## 4. `code/` — Notebooks & Scripts

**Important convention:** 1 cell = 1 logical unit; every notebook has a `MODELS` + `SMOKE_TEST` block in its global-config cell. Notebooks numbered `03_*`/`04_*` are **staged variants** (one model per notebook to save GPU memory) — not duplicates.

| File | Content | Status |
| --- | --- | --- |
| `00_EDA.ipynb` | EDA of class & object distributions, dataset label samples | Early |
| `01_modelling_baseline.ipynb` | YOLOv8n baseline, **Kaggle** version (path `/kaggle/input/...`) | Baseline |
| `02_modelling_baseline_local.ipynb` | YOLOv8n baseline, **local/GPU-server** version (the one referenced in README) | Baseline |
| `03_modelling_comparative_local.ipynb` | Comparative 5-model scaffold, `SMOKE_TEST = True` | Smoke |
| `03_1_modelling_comparative_local.ipynb` | Comparative — batch 1: `yolov8n_class_weight` (rest commented out) | Final (v8n) |
| `03_2_modelling_comparative_local.ipynb` | Comparative — batch 2: `yolov26n`, `yolov8_pd`, `yolo_rd` class_weight | Final (3 models) |
| `03_3_modelling_comparative_local.ipynb` | Comparative — batch 3 (same pattern); **reference notebook** for final weights & class-weight patch | **Final** |
| `04_1_modelling_4class.ipynb` | 4-class ablation — `yolov8n_4cls_class_weights` | Final |
| `04_2_modelling_4class.ipynb` | 4-class ablation — `yolov12n_4cls_class_weights` | Final |
| `04_3_modelling_4class.ipynb` | 4-class ablation — `yolov8_pd_4cls_class_weights` | Final |
| `04_4_modelling_4class.ipynb` | 4-class ablation — `yolo_rd_4cls_class_weights` | Final |
| `05_zero_shot_indonesia.ipynb` | Zero-shot to `RDD-Indonesia.v1i.yolov8` (first version) | Archive |
| `05_zero_shot_indo_v2.ipynb` | Zero-shot to `RDD-indo-v2` | Archive |
| `05_zero_shot_indo_v4.ipynb` | Zero-shot to `RDD-indo-v4` + macro/weighted F1 (**final**) | **Final** |
| `06_per_country_analysis.ipynb` | Per-source-country accuracy (China/Japan/India) vs train distribution | Final |
| `07_domain_visualization.ipynb` | t-SNE/UMAP YOLO embeddings per domain + image statistics | Final |
| `confusion_6cls_vs_4cls.py` | 6-class vs 4-class confusion analysis (FP *proxy*) | Support |
| `prepare_4class_dataset.py` | Build `data/NRDD-2024/RDD_4class/` by filtering manhole/patchy labels | Support |
| `requirements_yolov8_local.txt` | Dependencies (torch/torchvision **deliberately omitted**) | — |

### `code/models/` — YOLOv8-PD & YOLO-RD reconstructions

| File | Content |
| --- | --- |
| `README.md` | **Read this first** — reconstruction status, fixed bugs, fidelity caveats, version compatibility |
| `custom_modules.py` | Modules for both models (BoT, LSKA, C2fGhost, LSCDHead / SOM, ARM, WTConv) + `patch_ultralytics()` |
| `yolov8-pd.yaml` | YOLOv8-PD architecture |
| `yolo-rd.yaml` | YOLO-RD architecture |
| `train_example.py` | Training example (remember: call `patch_ultralytics()` before `YOLO(...)`) |

### Model weights (`.pt`, gitignored)

| Path | Content |
| --- | --- |
| `yolo26n.pt` (root), `code/yolo26n.pt` | Pretrained COCO YOLOv26n weights (download) |
| `code/yolov8n.pt` | Pretrained COCO YOLOv8n weights (download) |
| `runs/rdd_yolov8n_local/experiments/*/weights/best.pt` | Final 6-class weights per model |
| `runs/rdd_4class_local/experiments/*/weights/best.pt` | Final 4-class weights per model |

---

## 5. `docs/` — Documentation & Results

| File | Content | Note |
| --- | --- | --- |
| `INDEX.md` | **This file** | Context map |
| `RESULTS.md` | Raw Ultralytics log (val & test per model, including FPS) | Primary number source |
| `RESULTS_TABLE.md` | Tidy tables: overall, per-class, F1, per-country, zero-shot v4 | **Main source for reading numbers** |
| `rangkuman-eksperimen-ta.md` | Summary v1: design, results, bugs, decisions, limitations | Some numbers marked *superseded* |
| `rangkuman-eksperimen-ta-v2.md` | Summary v2 = final context for writers | **Use this one** |
| `proposal.pdf` | Final TA proposal (binary, gitignored) | — |
| `Salah prediksi Merge 1.txt` | List of mispredicted / hard image filenames (Indo data) | Working note |

### `docs/progress/` — Per-date logs (per `AGENTS.md`: log every bug discussion + fix)

| File | Topic |
| --- | --- |
| `2026-09-29-fp-proxy-vs-fp-overlap.md` | Clarifies that the FP "rate" in the 04_* notebooks is a *proxy*, not IoU-based FP |
| `2026-10-01-domain-viz.md` | Domain visualization of 3 countries + Indo in YOLO feature space (t-SNE/UMAP) |
| `2026-10-01-zero-shot-indo-v3.md` | Zero-shot adaptation to RDD-indo-v3 (5 classes, valid split only) |
| `2026-10-02-cek-klaim-shi-2026.md` | Verifies the Shi_2026 / YOLO-LWD claim from local PDF `latex/refference/05_` |
| `2026-10-02-mcp-migrasi-bawaan.md` | Migration of MCP adapter to built-in pi 0.99 (tooling note) |
| `2026-10-02-streamlit-source-test-predictions.md` | N-RDD2024 test-set prediction page in Streamlit |
| `2026-10-08-focal-loss-vs-effective-number-weighting.md` | Clarifies Focal Loss vs effective-number class weighting |
| `2026-10-08-hyperref-clickable-citation.md` | Fix for hyperref clickable citations in the IEEE paper |
| `2026-10-08-paper-ekspor-v2-v4-dan-analisis-opsional.md` | V2/V4 export & modular paper analysis (301 shared images audit) |
| `2026-10-08-rdd-indo-v4-and-summary.md` | RDD-indo-v4 audit + final-context assembly |
| `2026-10-08-zero-shot-v4-dan-f1-per-kelas.md` | Zero-shot v4 + macro/weighted F1 + `class_result` bug |

---

## 6. `scripts/`, `latex/`, `outputs/`, `runs/`

### `scripts/` — Support scripts

| File | Content | How to run |
| --- | --- | --- |
| `visualize_streamlit.py` | Dataset & prediction explorer (Inspect Dataset + N-RDD2024 Test Prediction pages) | `streamlit run scripts/visualize_streamlit.py` |
| `launch_fiftyone.py` | FiftyOne-based 6-class dataset visualizer + country metadata | `python scripts/launch_fiftyone.py` |
| `zero_shot_viewer.py` / `_v2.py` / `_v4.py` | Zero-shot GT vs prediction viewers (v1/v2/v4) | `streamlit run scripts/zero_shot_viewer_v4.py` |
| `fp_overlap_table.py` | FP *proxy* vs *overlap* (IoU-based) table per model | `python scripts/fp_overlap_table.py` |
| `viz_fp_overlap.py` | FP proxy vs true FP visualization (2×2 PNG + CSV) | `python scripts/viz_fp_overlap.py` |
| `package_experiment.py` | Bundle one run into an upload-ready `.zip` artifact | see the example in `README.md` §Storing Experiment Results |
| `run_nb_zs_v4.py` | Run all cells of the zero-shot v4 notebook (nbclient) | `python scripts/run_nb_zs_v4.py` |
| `run_zs_v4_finish.py` | Zero-shot v4 finishing: val v8n/v12n, domain_gap plot, pred samples | `python scripts/run_zs_v4_finish.py` |

### `latex/` — Manuscripts

| Path | Content |
| --- | --- |
| `PROPOSAL_TA.md` | **Token-efficient proposal index** — read this before opening the `.tex` files |
| `IEEE-Conference/main.tex` | IEEE paper draft (English) |
| `IEEE-Conference/draft/draft-analisis-hasil.md` | Results-analysis draft (Indonesian) for the paper |
| `IEEE-Conference/note.md` | Provisional items to validate before submission |
| `IEEE-Conference/IEEE-FORMATTING-RULES.md` | IEEE conference formatting rules checklist (from official template) |
| `IEEE-Conference/references.bib` | Paper BibTeX (13 entries at audit time) |
| `IEEE-Conference/gambar/` | Paper figures (`draft_*` = from analysis; others = final) |
| `IEEE-Conference/build/` | Compilation artifacts (gitignored); `render*/` = per-page PNGs |
| `IEEE-Conference/hasil/` | Final PDF (gitignored) |
| `skripsi-telkom/*.tex` | Thesis draft per chapter (Pendahuluan, Kajian-Pustaka, Metodologi, Hasil-dan-Pembahasan, Kesimpulan-dan-Saran, Lampiran, Cover, Abstrak) |
| `skripsi-telkom/References.bib` | Thesis BibTeX (28 entries at audit time; `PROPOSAL_TA.md` says 26) |
| `skripsi-telkom/gambar/` | Thesis figures (flowchart, architecture, distribution) |
| `skripsi-telkom/build/`, `hasil/` | Artifacts & PDF (gitignored) |
| `figures/` | Shared figures (used across manuscripts) |
| `refference/` | 11 reference paper PDFs (numbered 01–11) — **note the "refference" spelling** |

### `outputs/` — Deep research on references

| File | Content |
| --- | --- |
| `yolo-road-damage-references.md` | **Final deliverable**: reference candidates + ready-to-use BibTeX |
| `yolo-road-damage-references.provenance.md` | Provenance: sources, verification, decisions |
| `.plans/` | Research plan + T1–T4 briefs + workflow |
| `.drafts/` | Draft chain: research-{models,domain,loss,efficiency} → draft → cited → verification → revised |

### `runs/` — Training/evaluation outputs (gitignored, ~5 GB)

| Path | Content |
| --- | --- |
| `rdd_yolov8n_local/` | **Main 6-class run**: `experiments/` (weights+args), `evaluation/` (per-model test/val metrics, zero_shot_indo_*, domain_viz), per-class & F1 metric CSVs, `predictions/`, `per_country/` |
| `rdd_4class_local/` | 4-class ablation run (similar structure + `dataset_split_summary_4cls.csv`) |
| `rdd_4class_local_pc_lab/` | Copy of the 4-class run from the lab PC (model subset) |
| `rdd_yolov8n_local_bak/` | Backup of an older run (smoke test) |
| `detect/` | Ad-hoc Ultralytics `model.val()` outputs (`val`, `val-2`, … `val-88`) |
| `../code/runs/detect/` | Duplicate `val-*` artifacts (~145 MB); the `.gitignore` pattern `runs/` also ignores this folder |
| `proposal_text_mining_render/` | PNG render of the Text Mining course proposal + contact sheets (separate project) |

**Key files for numbers:**
- Per-class metrics: `runs/rdd_yolov8n_local/<model>_test_per_class_metrics.csv`, `*_f1_summary.csv`, `*_summary.json`
- 4-class: `runs/rdd_4class_local/*_4cls_*_per_class_metrics.csv`
- Zero-shot: `runs/rdd_yolov8n_local/evaluation/zero_shot_indo_v4/{domain_gap.csv, zs_f1_summary.csv, zs_per_class_metrics.csv}`
- Run configuration: `runs/*/experiments/*/args.yaml` (**more authoritative** than notebook constants)

---

## 7. Constraints & Pitfalls You Must Know

1. **Use `rangkuman-eksperimen-ta-v2.md`, not v1.** v1 contains older numbers, some marked *superseded*.
2. **Test = final results; val is monitoring/early-stopping only.** Do not mix them.
3. **`args.yaml` > notebook constants.** Some notebook cells contain stale model lists/values; the actual run configuration lives in `runs/*/experiments/*/args.yaml`.
4. **The imbalance intervention is effective-number class weighting, not Focal Loss.** Stale Focal Loss variables/cells in the notebooks **do not** mean Focal Loss was active. See `docs/progress/2026-10-08-focal-loss-vs-effective-number-weighting.md`.
5. **The FP "rate" in the `04_*` notebooks is a per-image *proxy***, not IoU-based FP. Do not cite it as true FP. See `docs/progress/2026-09-29-fp-proxy-vs-fp-overlap.md`.
6. **RDD-indo naming is potentially misleading.** The `data/RDD-indo-v4/` folder is a Roboflow `rdd-indo-crop` **version 3** export with only the `valid/` split (307 images). Do not call it "dataset version 4" or "primary Bandung data" without provenance. V2 and V4 are not identical splits (only 301 shared images).
7. **YOLOv8-PD & YOLO-RD are reconstructions**, not the papers' official code → mAP will not exactly match the published numbers. See `code/models/README.md`.
8. **The 6-class source `data.yaml` uses the names `Penutup_Jalan`/`Tambalan`** (IDs 4/5), while the manuscripts & runs use `manhole`/`patchy_road`. Notebooks write a derived YAML with consistent names; be careful when reading the raw `data.yaml`.
9. **`runs/`, `data/`, `latex/**/build/`, `latex/**/hasil/`, `*.pt` are Git-ignored.** After a fresh clone on another machine these folders won't exist — numbers must be reproduced or taken from `docs/RESULTS*.md`.
10. **`README.md` mentions `experiments/registry.csv` and `artifacts/`** which do not yet exist in the repo. Use `docs/RESULTS_TABLE.md` as the interim registry.
11. **The folder `latex/refference/` is misspelled** (should be `reference`), and `AGENTS.md` used to reference `latex_skripsi/skripsi-telkom` (the actual folder is `latex/skripsi-telkom`).

---

## 8. Typical Workflows (if you are an agent)

| Task | Steps |
| --- | --- |
| Write/revise the paper | Read `docs/rangkuman-eksperimen-ta-v2.md` → `docs/RESULTS_TABLE.md` → `latex/IEEE-Conference/{main.tex,note.md}` |
| Answer a numbers question | Start with `docs/RESULTS_TABLE.md`; if precision is needed, open the CSVs in `runs/.../evaluation/` |
| Add/change an experiment | Follow the notebook conventions (`AGENTS.md`), write a log in `docs/progress/YYYY-MM-DD-topic.md` |
| Trace why a decision was made | `docs/progress/` (chronological) → `docs/rangkuman-eksperimen-ta.md` §5–§6 |
| Add a reference | `outputs/yolo-road-damage-references.md` → add to `latex/*/references.bib`/`References.bib` |

---

## 9. Maintaining This Index

- **Update when:** adding a new notebook/script, moving folders, changing the final target dataset, or changing a main results file.
- **Quick drift check:** run
  ```bash
  git ls-files | sort            # tracked files
  ls code docs docs/progress scripts latex outputs runs   # key folders
  ```
  and compare against the tables above.
- **Relevant `AGENTS.md` rules:** *"Always ask permission before implementing anything"* and *"write every experiment bug discussion, and solution applied at `docs/progress/date-problem`"*.
