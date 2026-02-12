from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from validators import REPO_ROOT

DOCS_DIR = REPO_ROOT / "docs"
CATALOGUE_PATH = REPO_ROOT / "catalogue" / "catalogue.json"
README_PATH = REPO_ROOT / "README.md"


def _read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8").strip()


def _escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _instrument_row(instrument_id: str, instrument: dict[str, Any]) -> str:
    references = instrument.get("references") or []
    link = references[0] if references else ""
    id_cell = f"[{instrument_id}]({link})" if link else instrument_id
    name = str(instrument.get("name", ""))
    sensor_type = str(instrument.get("type", ""))
    platform_type = str(instrument.get("platform_type", ""))
    platforms = ", ".join(str(p) for p in (instrument.get("platform") or []))

    cells = [id_cell, name, sensor_type, platform_type, platforms]
    escaped = [_escape_markdown_cell(c) for c in cells]
    return f"| {' | '.join(escaped)} |"


def generate_readme(
    catalogue_path: Path = CATALOGUE_PATH,
    readme_path: Path = README_PATH,
) -> str:
    if not catalogue_path.exists():
        raise FileNotFoundError(
            f"{catalogue_path.as_posix()} not found. Run catalogue generation first."
        )

    header = _read_text(DOCS_DIR / "HEADER.md")
    footer = _read_text(DOCS_DIR / "FOOTER.md")

    catalogue = json.loads(catalogue_path.read_text(encoding="utf-8"))
    rows = [
        "| Id | Name | Type | Platform type | Platforms |",
        "| --- | --- | --- | --- | --- |",
    ]
    for instrument_id in sorted(catalogue.keys()):
        rows.append(_instrument_row(instrument_id, catalogue[instrument_id]))

    parts = [p for p in [header, "\n".join(rows), footer] if p]
    content = "\n\n".join(parts).rstrip() + "\n"
    readme_path.write_text(content, encoding="utf-8")
    return content


if __name__ == "__main__":
    generate_readme()
