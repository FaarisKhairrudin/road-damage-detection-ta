#!/usr/bin/env python3
"""
Interactive Dataset Visualizer for Road Damage Detection (6 Classes) using FiftyOne.
Includes country metadata extraction and distinct per-class color palette.
"""

import argparse
import os
import sys
from pathlib import Path
import yaml
from tqdm import tqdm
import fiftyone as fo


# Distinct High-Contrast Hex Colors for 6 Classes
CLASS_COLORS = {
    "Longitudinal_Crack": "#00E676",  # Bright Green
    "Transverse_Crack": "#00B0FF",    # Bright Cyan/Blue
    "Alligator_Crack": "#FFD600",     # Bright Yellow
    "Pothole": "#FF1744",             # Bright Red
    "Penutup_Jalan": "#D500F9",       # Purple
    "Tambalan": "#FF6D00",            # Orange
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Launch FiftyOne to visualize the 6-class Road Damage Detection dataset."
    )
    parser.add_argument(
        "--yaml-path",
        type=str,
        default="data/NRDD-2024/RDD_Split_Final_china_japan_india_6_classes/RDD_Split_Final_china_japan_india_6_classes/data.yaml",
        help="Path to data.yaml",
    )
    parser.add_argument(
        "--dataset-name",
        type=str,
        default="rdd_6classes",
        help="FiftyOne dataset name",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5151,
        help="Port to run the FiftyOne web app",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing FiftyOne dataset if it already exists",
    )
    parser.add_argument(
        "--desktop",
        action="store_true",
        help="Launch FiftyOne in desktop App mode if supported",
    )
    return parser.parse_args()


def extract_country_from_filename(filename: str) -> str:
    """Extract country name from filename pattern (e.g. China_MotorBike_..., India_..., Japan_...)."""
    parts = filename.split("_")
    prefix = parts[0] if parts else "Unknown"
    if prefix in {"China", "India", "Japan"}:
        return prefix
    return "Other"


def load_yolo_labels(label_file_path, class_names):
    """
    Parse a YOLO format label file (.txt) and convert to FiftyOne Detections.
    YOLO bbox format: [class_id, x_center, y_center, width, height] (normalized)
    FiftyOne bbox format: [top_left_x, top_left_y, width, height] (normalized)
    """
    detections = []
    if not os.path.exists(label_file_path):
        return fo.Detections(detections=detections)

    with open(label_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        try:
            cls_id = int(float(parts[0]))
            xc = float(parts[1])
            yc = float(parts[2])
            w = float(parts[3])
            h = float(parts[4])
        except ValueError:
            continue

        x_min = max(0.0, min(1.0, xc - (w / 2.0)))
        y_min = max(0.0, min(1.0, yc - (h / 2.0)))
        w = max(0.0, min(1.0 - x_min, w))
        h = max(0.0, min(1.0 - y_min, h))

        label_name = class_names[cls_id] if 0 <= cls_id < len(class_names) else f"class_{cls_id}"

        detections.append(
            fo.Detection(
                label=label_name,
                bounding_box=[x_min, y_min, w, h],
            )
        )

    return fo.Detections(detections=detections)


def build_or_load_dataset(yaml_path_str: str, dataset_name: str, overwrite: bool = False):
    yaml_file = Path(yaml_path_str).resolve()
    if not yaml_file.exists():
        raise FileNotFoundError(f"data.yaml not found at: {yaml_file}")

    with open(yaml_file, "r", encoding="utf-8") as f:
        data_cfg = yaml.safe_load(f)

    class_names = data_cfg.get("names", [])
    if isinstance(class_names, dict):
        class_names = [class_names[k] for k in sorted(class_names.keys())]

    print(f"Loaded {len(class_names)} classes from {yaml_file.name}:")
    for idx, name in enumerate(class_names):
        print(f"  [{idx}] {name} -> Color: {CLASS_COLORS.get(name, '#FFFFFF')}")

    if fo.dataset_exists(dataset_name):
        if overwrite:
            print(f"Overwriting existing FiftyOne dataset '{dataset_name}'...")
            fo.delete_dataset(dataset_name)
        else:
            print(f"Loading existing FiftyOne dataset '{dataset_name}'...")
            dataset = fo.load_dataset(dataset_name)
            _configure_app_colors(dataset, class_names)
            return dataset

    print(f"Creating new FiftyOne dataset '{dataset_name}'...")
    dataset = fo.Dataset(dataset_name)
    dataset.persistent = True

    base_dir = yaml_file.parent
    splits = ["train", "val", "test"]

    for split in splits:
        split_path_rel = data_cfg.get(split)
        if not split_path_rel:
            continue

        images_dir = (base_dir / split_path_rel).resolve()
        if not images_dir.exists():
            custom_path = data_cfg.get("path", ".")
            images_dir = (base_dir / custom_path / split_path_rel).resolve()

        if not images_dir.exists():
            print(f"Warning: Directory for {split} images not found at {images_dir}, skipping.")
            continue

        if images_dir.name == "images":
            labels_dir = images_dir.parent / "labels"
        else:
            labels_dir = images_dir / "labels"

        valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        image_files = [p for p in images_dir.iterdir() if p.suffix.lower() in valid_extensions]

        print(f"Processing split '{split}': found {len(image_files)} images...")
        samples = []
        for img_path in tqdm(image_files, desc=f"Loading {split} samples"):
            country = extract_country_from_filename(img_path.name)
            sample = fo.Sample(
                filepath=str(img_path),
                country=country,
                split=split,
            )
            sample.tags.append(split)
            sample.tags.append(country)

            label_file = labels_dir / f"{img_path.stem}.txt"
            sample["ground_truth"] = load_yolo_labels(label_file, class_names)
            samples.append(sample)

        dataset.add_samples(samples)

    _configure_app_colors(dataset, class_names)
    dataset.save()
    print(f"Dataset successfully created with {len(dataset)} total samples!")
    return dataset


def _configure_app_colors(dataset, class_names):
    """Configure FiftyOne ColorScheme to give each class a distinct vivid color."""
    try:
        label_colors = []
        for name in class_names:
            if name in CLASS_COLORS:
                label_colors.append({"label": name, "color": CLASS_COLORS[name]})

        dataset.app_config.color_scheme = fo.ColorScheme(
            color_by="label",
            color_pool=list(CLASS_COLORS.values()),
            label_colors=label_colors,
        )
        dataset.save()
    except Exception as e:
        print(f"Note: ColorScheme configuration: {e}")


def main():
    args = parse_args()
    dataset = build_or_load_dataset(
        yaml_path_str=args.yaml_path,
        dataset_name=args.dataset_name,
        overwrite=args.overwrite,
    )

    print("\n" + "=" * 60)
    print(f"Launching FiftyOne App on port {args.port}...")
    print(f"Open your browser and navigate to: http://localhost:{args.port}")
    print("Features available:")
    print("  1. Filter by Country ('China', 'India', 'Japan') under TAGS / country field.")
    print("  2. Filter by Split ('train', 'val', 'test') under TAGS / split field.")
    print("  3. Distinct color per class in ground_truth bounding boxes.")
    print("Press Ctrl+C to stop the FiftyOne server.")
    print("=" * 60 + "\n")

    session = fo.launch_app(dataset, port=args.port, remote=not args.desktop)
    session.wait()


if __name__ == "__main__":
    main()
