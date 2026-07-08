from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import yaml

from validators import REPO_ROOT

README_SOURCE_DIR = REPO_ROOT / "readme"
CATALOGUE_PATH = REPO_ROOT / "catalogue" / "catalogue.json"
README_PATH = REPO_ROOT / "README.md"
SCHEMA_PATH = REPO_ROOT / "SCHEMA.md"
SCHEMA_TABLES = [
    ("Core Schema", REPO_ROOT / "schema" / "core" / "core.yaml"),
    ("Spectral Extension", REPO_ROOT / "schema" / "extensions" / "spectral.yaml"),
    ("Imaging Extension", REPO_ROOT / "schema" / "extensions" / "imaging.yaml"),
    ("Data Access Extension", REPO_ROOT / "schema" / "extensions" / "data-access.yaml"),
    ("Cross Links Extension", REPO_ROOT / "schema" / "extensions" / "cross-links.yaml"),
    (
        "Earth Engine Access Point",
        REPO_ROOT / "schema" / "extensions" / "data_access_points" / "earth-engine.yaml",
    ),
    (
        "Planetary Computer Access Point",
        REPO_ROOT
        / "schema"
        / "extensions"
        / "data_access_points"
        / "planetary-computer.yaml",
    ),
    (
        "Copernicus Data Space Ecosystem Access Point",
        REPO_ROOT
        / "schema"
        / "extensions"
        / "data_access_points"
        / "copernicus-data-space-ecosystem.yaml",
    ),
    (
        "EOPF Sentinel Zarr Samples Access Point",
        REPO_ROOT
        / "schema"
        / "extensions"
        / "data_access_points"
        / "eopf-sentinel-zarr-samples.yaml",
    ),
]
PLATFORM_CATEGORIES = ["satellite", "airborne", "uav", "terrestrial"]
INSTRUMENT_TYPES = ["multispectral", "hyperspectral", "radar", "lidar", "rgb", "other"]
STATUS_EMOJIS = {
    "operational": ":white_check_mark:",
    "planned": ":stars:",
    "experimental": ":warning:",
    "retired": ":no_entry:",
}


def _read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8").strip()


def _escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _schema_type(schema_property: dict[str, Any]) -> str:
    if "type" in schema_property:
        value = schema_property["type"]
        return ", ".join(value) if isinstance(value, list) else str(value)
    if "oneOf" in schema_property:
        return "oneOf"
    if "anyOf" in schema_property:
        return "anyOf"
    if "$ref" in schema_property:
        return f"ref: {schema_property['$ref']}"
    return "unspecified"


def _build_schema_table(title: str, schema_path: Path, link_base: str = "") -> str:
    data = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    properties: dict[str, dict[str, Any]] = data.get("properties", {})
    required = set(data.get("required", []))
    rel_path = schema_path.relative_to(REPO_ROOT).as_posix()
    link_target = f"{link_base}{rel_path}" if link_base else rel_path

    rows = [
        f"## {title} ([`{rel_path}`]({link_target}))",
        "",
        "| Property | Required | Type | Description |",
        "| --- | --- | --- | --- |",
    ]

    for prop in properties:
        schema_prop = properties[prop]
        prop_name = f"**{prop}**" if prop in required else prop
        required_cell = "**Yes**" if prop in required else "No"
        type_cell = _schema_type(schema_prop)
        description = str(schema_prop.get("description", ""))
        row_cells = [
            _escape_markdown_cell(prop_name),
            _escape_markdown_cell(required_cell),
            _escape_markdown_cell(type_cell),
            _escape_markdown_cell(description),
        ]
        rows.append(f"| {' | '.join(row_cells)} |")
    return "\n".join(rows)


def _build_schema_sections(link_base: str = "") -> str:
    return "\n\n".join(
        _build_schema_table(title, path, link_base=link_base) for title, path in SCHEMA_TABLES
    )


def generate_schema_document(schema_path: Path = SCHEMA_PATH, link_base: str = "") -> str:
    parts = [
        "# Schema Specification",
        "The tables below summarize the properties defined by the core schema and its extensions.",
        _build_schema_sections(link_base=link_base),
    ]
    content = "\n\n".join(parts).rstrip() + "\n"
    schema_path.write_text(content, encoding="utf-8")
    return content


def _normalize_platform_type(value: str) -> str:
    lower = value.lower()
    if lower in {"airborn", "airborne"}:
        return "airborne"
    return lower


def _status_cell(status: str) -> str:
    emoji = STATUS_EMOJIS.get(status.lower())
    label = _escape_markdown_cell(status)
    if not emoji:
        return f"**{label}**"
    return f"**{label} {emoji}**"


def _docs_link(url: str) -> str:
    safe = _escape_markdown_cell(url)
    return f"[:link: link]({safe})"


def _ee_primary_link(instrument: dict[str, Any]) -> str:
    url = (
        instrument.get("extensions", {})
        .get("data_access", {})
        .get("ee", {})
        .get("primary", {})
        .get("docs", "")
    )
    return _docs_link(str(url)) if url else ""


def _pc_primary_link(instrument: dict[str, Any]) -> str:
    url = (
        instrument.get("extensions", {})
        .get("data_access", {})
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

        category_id = f"catalogue-{platform}-instruments"
        section_parts: list[str] = [
            f"<a id=\"{category_id}\"></a>",
            f"## {platform.title()} Instruments",
        ]
        for instrument_type in INSTRUMENT_TYPES:
            type_entries = [
                (instrument_id, instrument)
                for instrument_id, instrument in platform_entries
                if str(instrument.get("type", "")).lower() == instrument_type
            ]
            if not type_entries:
                continue
            subcategory_id = f"catalogue-{platform}-{instrument_type}"
            section_parts.append(f"<a id=\"{subcategory_id}\"></a>")
            section_parts.append(f"### {instrument_type.title()}")
            section_parts.append(_table_for_group(type_entries))

        if len(section_parts) > 1:
            sections.append("\n\n".join(section_parts))
    return "\n\n".join(sections)


def _catalogue_groups(
    catalogue: dict[str, dict[str, Any]],
) -> list[tuple[str, list[str]]]:
    groups: list[tuple[str, list[str]]] = []
    for platform in PLATFORM_CATEGORIES:
        platform_entries = [
            instrument
            for _, instrument in catalogue.items()
            if _normalize_platform_type(str(instrument.get("platform_type", ""))) == platform
        ]
        if not platform_entries:
            continue

        available_types = []
        for instrument_type in INSTRUMENT_TYPES:
            if any(str(i.get("type", "")).lower() == instrument_type for i in platform_entries):
                available_types.append(instrument_type)
        if available_types:
            groups.append((platform, available_types))
    return groups


def _catalogue_intro_and_toc(catalogue: dict[str, dict[str, Any]]) -> str:
    groups = _catalogue_groups(catalogue)
    lines = [
        "# Catalogue",
        "",
        "This section organizes instruments by platform type and sensing modality to make discovery and comparison easier.",
        "Use the table of contents below to jump directly to available categories and subcategories.",
        "",
        "## Table of Contents",
    ]
    for platform, instrument_types in groups:
        category_title = f"{platform.title()} Instruments"
        lines.append(f"- [{category_title}](#catalogue-{platform}-instruments)")
        for instrument_type in instrument_types:
            lines.append(f"  - [{instrument_type.title()}](#catalogue-{platform}-{instrument_type})")
    return "\n".join(lines)


def generate_readme(
    catalogue_path: Path = CATALOGUE_PATH,
    readme_path: Path = README_PATH,
) -> str:
    if not catalogue_path.exists():
        raise FileNotFoundError(
            f"{catalogue_path.as_posix()} not found. Run catalogue generation first."
        )

    header = _read_text(README_SOURCE_DIR / "HEADER.md")
    body = _read_text(README_SOURCE_DIR / "BODY.md")
    footer = _read_text(README_SOURCE_DIR / "FOOTER.md")

    catalogue_doc = json.loads(catalogue_path.read_text(encoding="utf-8"))
    catalogue = catalogue_doc.get("instruments", catalogue_doc)
    if not isinstance(catalogue, dict):
        raise ValueError("Invalid catalogue format: 'instruments' must be an object.")
    catalogue_intro = _catalogue_intro_and_toc(catalogue)
    sections = _build_catalogue_sections(catalogue)

    parts = [p for p in [header, body, catalogue_intro, sections, footer] if p]
    content = "\n\n".join(parts).rstrip() + "\n"
    readme_path.write_text(content, encoding="utf-8")
    return content


if __name__ == "__main__":
    generate_schema_document()
    generate_readme()
