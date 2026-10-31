"""Recompute Params(M) & GFLOPs for the five six-class models from final weights.

Protocol per Table I footnote: Ultralytics fused model summary at 640-pixel input.
Output: runs/rdd_yolov8n_local/model_complexity.json + printed comparison table.
"""

import json
import os
import sys
import warnings

from ultralytics import YOLO

warnings.filterwarnings("ignore")

# Custom reconstructions (YOLOv8-PD / YOLO-RD) unpickle modules from code/models.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code", "models"))

BASE = "runs/rdd_yolov8n_local/experiments"
MODELS = {
    "yolov8n": f"{BASE}/yolov8n_class_weight/weights/best.pt",
    "yolov12n": f"{BASE}/yolov12n_class_weight/weights/best.pt",
    "yolov26n": f"{BASE}/yolov26n_class_weight/weights/best.pt",
    "yolov8_pd": f"{BASE}/yolov8_pd_class_weight/weights/best.pt",
    "yolo_rd": f"{BASE}/yolo_rd_class_weight/weights/best.pt",
}

TEX = {
    "yolov8n": (3.01, 8.2),
    "yolov12n": (2.57, 7.5),
    "yolov26n": (2.51, 5.9),
    "yolov8_pd": (2.46, 7.7),
    "yolo_rd": (7.09, 12.9),
}


def measure(name: str, path: str) -> dict:
    """Measure one model, returning params/GFLOPs or an error payload."""
    if not os.path.exists(path):
        return {"error": "weights not found", "weights": path}
    try:
        model = YOLO(path)
        model.fuse()
        # model.info() prints the summary and may return None on some versions;
        # prefer the return value, fall back to parsing nothing (handled below).
        info = model.info(imgsz=640, verbose=False)
    except Exception as exc:  # noqa: BLE001 - audit script must not crash on one bad model
        return {"error": str(exc), "weights": path}
    if isinstance(info, (list, tuple)) and len(info) >= 4:
        layers, params, _gradients, gflops = info[:4]
        return {
            "params_M": round(params / 1e6, 3),
            "gflops": gflops,
            "layers": layers,
            "weights": path,
        }
    if info is None:
        # Newer Ultralytics returns None but prints the summary; measure directly.
        try:
            from ultralytics.utils.torch_utils import model_info
            mi = model_info(model.model, detailed=False, verbose=True, imgsz=640)
            if isinstance(mi, (list, tuple)) and len(mi) >= 4:
                layers, params, _gradients, gflops = mi[:4]
                return {
                    "params_M": round(params / 1e6, 3),
                    "gflops": gflops,
                    "layers": layers,
                    "weights": path,
                }
        except Exception as exc:  # noqa: BLE001
            return {"error": f"info None + model_info failed: {exc}", "weights": path}
    return {"error": f"unexpected info shape: {info!r}", "weights": path}


def main() -> None:
    results = {name: measure(name, path) for name, path in MODELS.items()}

    print(f"{'model':10s} {'tex P/G':>12s} {'repo P/G':>16s}")
    for name, res in results.items():
        tp, tg = TEX[name]
        if "params_M" in res:
            print(f"{name:10s} {tp}/{tg:<8} {res['params_M']}/{res['gflops']}")
        else:
            print(f"{name:10s} ERROR: {res['error']}")

    out = "runs/rdd_yolov8n_local/model_complexity.json"
    payload = {
        "protocol": "ultralytics fused model.info(imgsz=640) on final best.pt weights",
        "models": results,
    }
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"saved -> {out}")
    except OSError as exc:
        print(f"could not save {out}: {exc}")


if __name__ == "__main__":
    main()
