# Road Damage Detection TA

Thesis (Tugas Akhir) research code for a baseline of road damage and surface defect detection using YOLOv8n on the N-RDD2024 Asia subset (6 classes).

## Context Map (read before exploring)

This repo is fairly large and layered. To find **which file contains what** without reading everything, start with:

- **[`docs/INDEX.md`](docs/INDEX.md)** — the full context map: "looking for X → open Y" routing, the contents of every folder, and a list of pitfalls you must know.
- **[`AGENTS.md`](AGENTS.md)** — working rules (notebook & LaTeX conventions, and the requirement to write progress logs).

Shortcuts to the sources of numbers and manuscript context:

| I need… | Open |
| --- | --- |
| Final mAP/F1 (tables) | [`docs/RESULTS_TABLE.md`](docs/RESULTS_TABLE.md) |
| Raw evaluation log | [`docs/RESULTS.md`](docs/RESULTS.md) |
| Final experiment context for writing | [`docs/rangkuman-eksperimen-ta-v2.md`](docs/rangkuman-eksperimen-ta-v2.md) |
| Bug/decision logs by date | [`docs/progress/`](docs/progress/) |
| Token-efficient proposal index | [`latex/PROPOSAL_TA.md`](latex/PROPOSAL_TA.md) |

## Experiment Focus

- Secondary dataset: N-RDD2024, subset of China, Japan, India.
- Classes: `Longitudinal_Crack`, `Transverse_Crack`, `Alligator_Crack`, `Pothole`, `manhole`, `patchy_road`.
- Main baseline: YOLOv8n pretrained on COCO with the native Ultralytics loss.
- Evaluation: mAP50, mAP50-95, precision, recall, per-class F1, confusion matrix, PR/F1 curves, and FPS estimation.
- Focal loss is prepared as an optional ablation, not the main baseline.

## Expected Data Structure

Data is not stored on GitHub. After cloning the repo, copy the dataset from the SSD to the following location:

```text
data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/
  data.yaml
  train/
    images/
    labels/
  val/
    images/
    labels/
  test/
    images/
    labels/
```

The local notebooks already use this path automatically.

## Local or GPU-Server Setup

```bash
git clone https://github.com/FaarisKhairrudin/road-damage-detection-ta.git
cd road-damage-detection-ta
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -U pip
pip install -r code/requirements_yolov8_local.txt
```

If an NVIDIA GPU is available, make sure PyTorch CUDA is installed to match the server's CUDA version. If `torch.cuda.is_available()` is still `False`, install PyTorch CUDA from the official PyTorch instructions first, then install the requirements above.

## Main Notebooks

> The full notebook list (including the comparative experiments, the 4-class ablation, and zero-shot) is in [`docs/INDEX.md`](docs/INDEX.md) §4.

- `code/01_modelling_baseline.ipynb`: Kaggle version.
- `code/02_modelling_baseline_local.ipynb`: local/GPU-server version.

To run the local baseline:

1. Open `code/02_modelling_baseline_local.ipynb`.
2. Run the dependency-install cell if the environment is incomplete.
3. Restart the kernel.
4. Run the cells from the top.
5. For a smoke test, temporarily set `EPOCHS = 5` and `RUN_NAME = "yolov8n_smoke_test"`.
6. For the final experiment, use `EPOCHS = 300`, `PATIENCE = 50`, and `RUN_NAME = "yolov8n_baseline_native_loss"`.

## Baseline Augmentation Notes

The baseline does not use rotation:

```python
degrees = 0.0
```

Augmentations used:

- Mosaic
- Light MixUp
- Horizontal flip
- Translate
- Scale
- Close mosaic for the last 10 epochs

## Output

Training and evaluation outputs appear under:

```text
runs/rdd_yolov8n_local/
```

The `runs/` folder, the dataset, the proposal document, and model weights are ignored by Git to keep the repository light. The contents of `runs/` and the key per-run files are described in [`docs/INDEX.md`](docs/INDEX.md) §6.

## Storing Experiment Results

Do not commit model weights or training-output folders directly to GitHub. GitHub warns for files above 50 MiB and rejects files above 100 MiB on a normal Git repository. YOLOv8n weights can still be small, but many experiments will quickly make the repository heavy because `.pt` files are binary and do not version well.

Recommended pattern:

- GitHub repository: code, notebooks, requirements, README, and the experiment registry.
- `runs/`: local, temporary training/evaluation output.
- `artifacts/`: local upload-ready packages, still ignored by Git.
- GitHub Releases / Hugging Face / Google Drive / Kaggle: where `.pt` weights and evaluation `.zip` packages live.
- `experiments/registry.csv`: a record of weight links, eval-artifact links, key metrics, commits, and run notes.

> Note: `experiments/registry.csv` and the `artifacts/` folder **do not yet exist** in this repo. In the meantime, the metrics registry is held by [`docs/RESULTS_TABLE.md`](docs/RESULTS_TABLE.md).

To build an artifact package from one run:

```bash
python scripts/package_experiment.py --run-dir runs/rdd_yolov8n_local/experiments/yolov8n_baseline_native_loss --run-id yolov8n_baseline_native_loss_v1
```

Upload the files from `artifacts/yolov8n_baseline_native_loss_v1/`, then fill in their links in `experiments/registry.csv`.
