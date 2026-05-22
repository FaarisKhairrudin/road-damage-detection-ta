from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


KEEP_PATTERNS = {
    "args.yaml",
    "results.csv",
    "results.png",
    "confusion_matrix.png",
    "confusion_matrix_normalized.png",
    "F1_curve.png",
    "PR_curve.png",
    "P_curve.png",
    "R_curve.png",
    "labels.jpg",
    "labels_correlogram.jpg",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, base_dir: Path) -> dict:
    return {
        "path": path.relative_to(base_dir).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def collect_eval_files(run_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in run_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name in KEEP_PATTERNS:
            files.append(path)
        elif path.name.startswith(("val_batch", "train_batch")) and path.suffix.lower() in {".jpg", ".png"}:
            files.append(path)
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser(description="Package YOLO experiment artifacts without committing large files.")
    parser.add_argument("--run-dir", required=True, type=Path, help="Path to Ultralytics run directory.")
    parser.add_argument("--run-id", required=True, help="Stable experiment ID, e.g. yolov8n_baseline_native_loss_v1.")
    parser.add_argument("--output-dir", default=Path("artifacts"), type=Path, help="Local output directory, ignored by Git.")
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    artifact_dir = args.output_dir.resolve() / args.run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)

    eval_files = collect_eval_files(run_dir)
    eval_zip = artifact_dir / f"{args.run_id}_eval_artifacts.zip"
    with zipfile.ZipFile(eval_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in eval_files:
            zf.write(file_path, arcname=file_path.relative_to(run_dir).as_posix())

    weights_dir = run_dir / "weights"
    weight_files = [p for p in [weights_dir / "best.pt", weights_dir / "last.pt"] if p.exists()]
    copied_weights = []
    for weight_path in weight_files:
        target = artifact_dir / f"{args.run_id}_{weight_path.name}"
        shutil.copy2(weight_path, target)
        copied_weights.append(target)

    manifest = {
        "run_id": args.run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_run_dir": str(run_dir),
        "eval_zip": file_record(eval_zip, artifact_dir),
        "weights": [file_record(path, artifact_dir) for path in copied_weights],
        "included_eval_files": [path.relative_to(run_dir).as_posix() for path in eval_files],
        "next_step": "Upload files in this artifact directory to GitHub Releases or external storage, then record URLs in experiments/registry.csv.",
    }

    manifest_path = artifact_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Artifact directory: {artifact_dir}")
    print(f"Manifest          : {manifest_path}")
    print(f"Eval zip          : {eval_zip}")
    for weight in copied_weights:
        print(f"Weight copy       : {weight}")


if __name__ == "__main__":
    main()
