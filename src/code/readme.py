from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from validators import REPO_ROOT

DOCS_DIR = REPO_ROOT / "docs"
CATALOGUE_PATH = REPO_ROOT / "catalogue" / "catalogue.json"
README_PATH = REPO_ROOT / "README.md"
PLATFORM_CATEGORIES = ["satellite", "airborne", "uav", "terrestrial"]
INSTRUMENT_TYPES = ["multispectral", "hyperspectral", "radar", "lidar", "rgb", "other"]
STATUS_COLORS = {
    "operational": "green",
    "planned": "purple",
    "experimental": "goldenrod",
    "retired": "red",
}


def _read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8").strip()


def _escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _normalize_platform_type(value: str) -> str:
    lower = value.lower()
    if lower in {"airborn", "airborne"}:
        return "airborne"
    return lower


def _status_cell(status: str) -> str:
    color = STATUS_COLORS.get(status.lower())
    label = _escape_markdown_cell(status)
    if not color:
        return f"**{label}**"
    return f"<span style='color:{color}'><strong>{label}</strong></span>"


def _docs_link(url: str) -> str:
    safe = _escape_markdown_cell(url)
    return f"[:link: link]({safe})"


def _ee_primary_link(instrument: dict[str, Any]) -> str:
    url = (
        instrument.get("extensions", {})
        .get("ee", {})
        .get("primary", {})
        .get("docs", "")
    )
    return _docs_link(str(url)) if url else ""


def _pc_primary_link(instrument: dict[str, Any]) -> str:
    url = (
        instrument.get("extensions", {})
        .get("planetary_computer", {})
        .get("primary", {})
        .get("docs", "")
    )
    return _docs_link(str(url)) if url else ""


def _instrument_row(instrument_id: str, instrument: dict[str, Any]) -> str:
    references = instrument.get("references") or []
    link = references[0] if references else ""
    id_cell = f"[{instrument_id}]({link})" if link else instrument_id
    name = str(instrument.get("name", ""))
    platforms = ", ".join(str(p) for p in (instrument.get("platform") or []))
    status = str(instrument.get("status", ""))
    ee_link = _ee_primary_link(instrument)
    pc_link = _pc_primary_link(instrument)

    cells = [id_cell, name, platforms, _status_cell(status), ee_link, pc_link]
    escaped = [_escape_markdown_cell(c) for c in cells]
    return f"| {' | '.join(escaped)} |"


def _table_for_group(group: list[tuple[str, dict[str, Any]]]) -> str:
    rows = [
        "| Id | Name | Platforms | Status | Earth Engine | Planetary Computer |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for instrument_id, instrument in sorted(group, key=lambda item: item[0]):
        rows.append(_instrument_row(instrument_id, instrument))
    return "\n".join(rows)


def _build_catalogue_sections(catalogue: dict[str, dict[str, Any]]) -> str:
    sections: list[str] = []

    for platform in PLATFORM_CATEGORIES:
        platform_entries = [
            (instrument_id, instrument)
            for instrument_id, instrument in catalogue.items()
            if _normalize_platform_type(str(instrument.get("platform_type", ""))) == platform
        ]
        if not platform_entries:
            continue

        section_parts: list[str] = [f"## {platform.title()} Instruments"]
        for instrument_type in INSTRUMENT_TYPES:
            type_entries = [
                (instrument_id, instrument)
                for instrument_id, instrument in platform_entries
                if str(instrument.get("type", "")).lower() == instrument_type
            ]
            if not type_entries:
                continue
            section_parts.append(f"### {instrument_type.title()}")
            section_parts.append(_table_for_group(type_entries))

        if len(section_parts) > 1:
            sections.append("\n\n".join(section_parts))
    return "\n\n".join(sections)


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
    sections = _build_catalogue_sections(catalogue)

    parts = [p for p in [header, sections, footer] if p]
    content = "\n\n".join(parts).rstrip() + "\n"
    readme_path.write_text(content, encoding="utf-8")
    return content


if __name__ == "__main__":
    generate_readme()
