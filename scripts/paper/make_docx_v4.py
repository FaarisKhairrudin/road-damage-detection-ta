#!/usr/bin/env python3
"""Deprecated legacy report entry point; use the current Markdown-based exporter.

The original generator hardcoded the superseded V3/514-annotation description,
mixed primary and supplementary metrics, and embedded outdated interpretations.
Its byte-exact source is retained under docs/archive/content-before-update/.
This entry point creates no document and prints the current source/export path.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    narrative = repo / "docs/draft-analisis-rapih.md"
    exporter = repo / "scripts/paper/make_docx_rapih.py"
    archived = repo / "docs/archive/content-before-update/scripts/paper/make_docx_v4.py"
    print("make_docx_v4.py is deprecated; no DOCX file was created.")
    print(f"Current narrative: {narrative}")
    print(f"Review the narrative, then explicitly run: python3 {exporter}")
    print(f"Historical generator source: {archived}")


if __name__ == "__main__":
    main()
