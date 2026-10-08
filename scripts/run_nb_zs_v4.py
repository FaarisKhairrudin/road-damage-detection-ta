#!/usr/bin/env python3
"""Run all cell notebook zero-shot V4 (kernel python3_12), tulis balik outputnya."""
import contextlib
import sys
from pathlib import Path

import nbformat
from jupyter_client.manager import KernelManager
from nbclient import NotebookClient

NB = Path(__file__).resolve().parent.parent / "code/05_zero_shot_indo_v4.ipynb"
CWD = NB.parent.parent

nb = nbformat.read(str(NB), as_version=4)
km = KernelManager(kernel_name="python3_12")
km.start_kernel(cwd=str(CWD))
try:
    client = NotebookClient(
        nb,
        timeout=1800,
        kernel_name="python3_12",
        resources={"metadata": {"path": str(CWD)}},
        allow_errors=True,
        km=km,
    )
    client.execute()
finally:
    with contextlib.suppress(Exception):
        km.shutdown_kernel(now=True)

nbformat.write(nb, str(NB))
print("NOTEBOOK DONE ->", NB)

for i, cell in enumerate(nb.cells):
    src = "".join(cell.get("source", []))
    if cell.cell_type == "code" and ("run_zs(" in src or "zs_f1_summary" in src):
        for out in cell.get("outputs", []):
            text = "".join(out.get("text", [])) if out.get("output_type") == "stream" else ""
            for line in text.splitlines():
                if any(k in line for k in ("F1macro", "macro_f1", "indo_v4_zs",
                                           "yolov12n", "yolo_rd ", "yolov8_pd",
                                           "yolov8n ", "yolov26n", "tersimpan",
                                           "Ringkasan")):
                    print(f"[cell {i}] {line}")
sys.exit(0)
