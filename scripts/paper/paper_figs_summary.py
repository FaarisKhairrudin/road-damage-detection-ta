#!/usr/bin/env python3
"""Build canonical documentation figures and tables without changing LaTeX assets.

The earlier hardcoded summary mixed class scopes and legacy complexity values.
Its byte-exact source is preserved under docs/archive/content-before-update/.

Run: python scripts/paper/paper_figs_summary.py
Canonical implementation: scripts/build_final_results.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_final_results import main

if __name__ == '__main__':
    main()
