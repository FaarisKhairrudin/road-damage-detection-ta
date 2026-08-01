"""
Training YOLOv8-PD / YOLO-RD sebagai model pembanding TA Road Damage Detection.

PENTING: patch_ultralytics() WAJIB dipanggil sebelum YOLO(...).
"""

from pathlib import Path

from custom_modules import patch_ultralytics

patch_ultralytics()

from ultralytics import YOLO

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_YAML = (
    REPO_ROOT / "runs/rdd_yolov8n_local/rdd6_local.yaml"
)
MODEL_YAML = REPO_ROOT / "code/models/yolov8-pd.yaml"  # atau yolo-rd.yaml
RUN_NAME = MODEL_YAML.stem
OUTPUT_DIR = REPO_ROOT / "runs/rdd_yolov8n_local/experiments"

if __name__ == "__main__":
    model = YOLO(str(MODEL_YAML), task="detect")

    model.train(
        data=str(DATASET_YAML),
        epochs=300,
        imgsz=640,
        batch=16,
        device=0,
        workers=0,
        patience=50,
        seed=42,
        deterministic=True,
        pretrained=True,
        optimizer="auto",
        amp=True,
        cos_lr=True,
        plots=True,
        save=True,
        save_period=25,
        close_mosaic=10,
        mosaic=1.0,
        mixup=0.05,
        fliplr=0.5,
        translate=0.10,
        scale=0.50,
        degrees=0.0,
        project=str(OUTPUT_DIR),
        name=RUN_NAME,
        exist_ok=True,
    )
