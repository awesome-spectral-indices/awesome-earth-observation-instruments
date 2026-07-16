"""Generate VitePress instrument pages from the catalogue JSON."""

from __future__ import annotations

import json
import math
import re
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import quote

from readme import generate_schema_document


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOGUE_PATH = REPO_ROOT / "catalogue" / "catalogue.json"
DOCS_DIR = REPO_ROOT / "docs"
INSTRUMENTS_DIR = REPO_ROOT / "docs" / "instruments"
VITEPRESS_DATA_DIR = REPO_ROOT / "docs" / ".vitepress" / "data"
SPECTRAL_COMPARISON_PATH = VITEPRESS_DATA_DIR / "spectral-comparison.json"
SPECTRAL_RESPONSE_PATH = VITEPRESS_DATA_DIR / "spectral-response-functions.json"
CONTRIBUTING_PATH = REPO_ROOT / "CONTRIBUTING.md"
DOCS_CONTRIBUTING_PATH = DOCS_DIR / "contributing.md"
DOCS_SCHEMA_PATH = DOCS_DIR / "schema.md"
GITHUB_BLOB_BASE_URL = (
    "https://github.com/"
    "awesome-spectral-indices/awesome-earth-observation-instruments/"
    "blob/main/"
)
SRF_RAW_BASE_URL = (
    "https://raw.githubusercontent.com/"
    "awesome-spectral-indices/awesome-earth-observation-instruments/"
    "main/src/srf"
)

ACCESS_POINT_LABELS = {
    "ee": {
        "title": "Google Earth Engine",
        "details": "Data documentation in Google Earth Engine.",
        "link_text": "To Earth Engine Data Catalog",
    },
    "planetary_computer": {
        "title": "Microsoft Planetary Computer",
        "details": "Data documentation in Microsoft Planetary Computer.",
        "link_text": "To Planetary Computer Datasets",
    },
    "cdse": {
        "title": "Copernicus Data Space Ecosystem",
        "details": "Data documentation in Copernicus Data Space Ecosystem.",
        "link_text": "To CDSE STAC Browser",
    },
    "eopf": {
        "title": "EOPF Sentinel Zarr Samples",
        "details": "Data documentation in the EOPF Sentinel Zarr Samples Service.",
        "link_text": "To EOPF STAC Browser",
    },
}

CROSS_LINK_LABELS = {
    "idb": "IndexDataBase",
    "ceos": "CEOS EO Handbook",
    "earthdata": "EarthData",
}

PRODUCT_LABELS = {
    "primary": "Primary",
    "raw": "Raw",
    "toa": "Top of atmosphere",
    "boa": "Bottom of atmosphere",
}


def load_catalogue() -> dict[str, dict[str, Any]]:
    """Load the generated catalogue and return the instruments dictionary."""

    catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    instruments = catalogue.get("instruments")

    if not isinstance(instruments, dict):
        raise ValueError(f"{CATALOGUE_PATH} does not contain an instruments object.")

    return instruments


def yaml_quote(value: Any) -> str:
    """Return a YAML-safe double-quoted scalar."""

    return json.dumps("" if value is None else str(value))


def css_class(value: Any) -> str:
    """Return a CSS-safe class fragment."""

    text = "" if value is None else str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "other"


def markdown_cell(value: Any) -> str:
    """Format a value for a Markdown table cell."""

    if value is None:
        return ""

    if isinstance(value, float):
        value = f"{value:g}"
    elif isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    else:
        value = str(value)

    return value.replace("\n", " ").replace("|", "\\|")


def markdown_link(url: str) -> str:
    """Return a compact Markdown link for a URL."""

    return f"[{url}]({url})"


def platforms_text(instrument: dict[str, Any]) -> str:
    """Return the instrument platform list as text."""

    platforms = instrument.get("platform", [])
    return text_value(platforms)


def text_value(value: Any) -> str:
    """Return a catalogue value as display/search text."""

    if value is None:
        return ""

    if isinstance(value, float):
        return f"{value:g}"

    if isinstance(value, list):
        return ", ".join(str(item) for item in value)

    return str(value)


def article_for(value: str) -> str:
    """Return an English indefinite article for a phrase."""

    return "an" if value[:1].lower() in {"a", "e", "i", "o", "u"} else "a"


def heading_text(value: Any) -> str:
    """Return a readable label from a catalogue key."""

    text = text_value(value).strip()
    if not text:
        return "Other"

    return text.replace("_", " ").replace("-", " ").title()


def number_value(value: Any) -> float | None:
    """Return a numeric value when a catalogue value is numeric."""

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    return None


def range_text(values: list[float], unit: str = "") -> str:
    """Return a compact range from numeric values."""

    if not values:
        return ""

    unique_values = sorted(set(values))
    suffix = f" {unit}" if unit else ""

    if len(unique_values) == 1:
        return f"{unique_values[0]:g}{suffix}"

    return f"{unique_values[0]:g}-{unique_values[-1]:g}{suffix}"


def render_frontmatter(instrument: dict[str, Any]) -> str:
    """Render the VitePress home layout frontmatter for an instrument page."""

    instrument_id = instrument.get("id", "")
    acronym = instrument.get("acronym") or instrument_id
    name = instrument.get("name", "")
    platform = platforms_text(instrument)
    platform_type = css_class(instrument.get("platform_type"))

    lines = [
        "---",
        f"pageClass: {css_class(instrument.get('type'))}-class",
        "isHome: true",
        "",
        "layout: home",
        "",
        "hero:",
        f"  name: {yaml_quote(acronym)}",
        f"  text: {yaml_quote(name)}",
        f"  tagline: {yaml_quote(platform)}",
        "  image:",
        f"    src: /{platform_type}.png",
        f"    alt: {platform_type}",
        "  actions:",
        "    - theme: alt",
        "      text: 🡰 Back to Instrument Index",
        "      link: /instruments/",
        "",
        "---",
    ]
    return "\n".join(lines)


def render_overview(instrument: dict[str, Any]) -> str:
    """Render a compact instrument metadata table."""

    rows = [
        ("Id", instrument.get("id")),
        ("Name", instrument.get("name")),
        ("Acronym", instrument.get("acronym")),
        ("Type", instrument.get("type")),
        ("Platform type", instrument.get("platform_type")),
        ("Platform", platforms_text(instrument)),
        ("Operator", instrument.get("operator")),
        ("Start date", instrument.get("start_date")),
        ("End date", instrument.get("end_date")),
        ("Status", instrument.get("status")),
        ("Availability", instrument.get("availability")),
    ]

    rendered = ["## Overview", "", "| Property | Value |", "| --- | --- |"]
    for key, value in rows:
        if value not in (None, "", []):
            rendered.append(f"| {markdown_cell(key)} | {markdown_cell(value)} |")

    return "\n".join(rendered)


def render_bands(instrument: dict[str, Any]) -> str:
    """Render the spectral bands table when band metadata is available."""

    extensions = instrument.get("extensions", {})
    spectral = extensions.get("spectral", {}) if isinstance(extensions, dict) else {}
    bands = spectral.get("bands", {}) if isinstance(spectral, dict) else {}

    if not bands:
        return "## Bands\n\nNo spectral band information is available."

    lines = [
        "## Bands",
        "",
        "| Band | Center wavelength | Bandwidth | Common name | GSD | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for band_id, band in bands.items():
        if not isinstance(band, dict):
            lines.append(f"| {markdown_cell(band_id)} | {markdown_cell(band)} |  |  |  |  |")
            continue

        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(band_id),
                    markdown_cell(band.get("center_wavelength")),
                    markdown_cell(band.get("bandwidth")),
                    markdown_cell(band.get("common_name")),
                    markdown_cell(band.get("gsd")),
                    markdown_cell(band.get("band_description")),
                ]
            )
            + " |"
        )

    return "\n".join(lines)


def render_links(instrument: dict[str, Any]) -> str:
    """Render reference and data access URLs."""

    lines = ["## Links", ""]

    link_groups = [
        ("Data links", instrument.get("data_links", [])),
        ("References", instrument.get("references", [])),
    ]

    for title, links in link_groups:
        lines.extend([f"### {title}", ""])
        if links:
            for url in links:
                lines.append(f"- {markdown_link(str(url))}")
        else:
            lines.append("No links are available.")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_notes(instrument: dict[str, Any]) -> str:
    """Render optional instrument notes as a GitHub-style Markdown alert."""

    notes = instrument.get("notes")
    if not isinstance(notes, str) or not notes.strip():
        return ""

    lines = ["> [!NOTE]"]
    for line in notes.strip().splitlines():
        lines.append(f"> {line}" if line else ">")
    return "\n".join(lines)


def render_instrument_identity(instrument_id: Any) -> str:
    """Render a compact visual callout for the catalogue instrument ID."""

    safe_id = escape(text_value(instrument_id), quote=True)
    return "\n".join(
        [
            '<div class="instrument-identity" aria-label="Instrument identifier">',
            '  <span class="instrument-identity-label">Instrument ID</span>',
            f'  <code class="instrument-identity-value">{safe_id}</code>',
            "</div>",
        ]
    )


def render_xeo_example(instrument_id: Any) -> str:
    """Render a Python example for exploring the instrument with xeo."""

    return "\n".join(
        [
            "## Explore it with `xeo`",
            "",
            "```python",
            "import xeo",
            "",
            f"instrument = xeo.instruments.{text_value(instrument_id)}",
            "",
            "# Extract metadata",
            "metadata = {",
            '    "id": instrument.id,',
            '    "name": instrument.name,',
            '    "acronym": instrument.acronym,',
            '    "type": instrument.type,',
            '    "platform_type": instrument.platform_type,',
            '    "platform": instrument.platform,',
            '    "operator": instrument.operator,',
            '    "start_date": instrument.start_date,',
            '    "end_date": instrument.end_date,',
            '    "status": instrument.status,',
            '    "availability": instrument.availability,',
            "}",
            "",
            "# Get the bands as a pandas DataFrame (returns None if it is not available)",
            "instrument.bands()",
            "",
            "# Get the Spectral Response Function as a pandas DataFrame (returns None if it is not available)",
            "instrument.srf()",
            "",
            "# Check the available extensions",
            "print(instrument.extension_names)",
            "for name, extension in instrument.extensions.items():",
            '    print(name, "->", list(extension))',
            "```",
        ]
    )


def render_instrument_page(instrument: dict[str, Any]) -> str:
    """Render a single VitePress instrument page."""

    instrument_id = instrument.get("id", "")

    sections = [
        render_frontmatter(instrument),
        render_instrument_identity(instrument_id),
        "## Summary",
        f'<InstrumentSection instrument-id="{instrument_id}" section="summary" />',
        render_notes(instrument),
        f'<InstrumentTabs instrument-id="{instrument_id}" />',
        render_xeo_example(instrument_id),
    ]
    return "\n\n".join(section for section in sections if section).rstrip() + "\n"


def render_index(instruments: dict[str, dict[str, Any]]) -> str:
    """Render the VitePress instrument index page."""

    lines = [
        "# Instrument Index",
        "",
        "Browse the instruments currently available in the Awesome Earth Observation Instruments catalogue.",
        "",
        "<InstrumentIndex />",
    ]

    return "\n".join(lines).rstrip() + "\n"


def render_index_data(instruments: dict[str, dict[str, Any]]) -> str:
    """Render searchable instrument index data as JSON."""

    records = []
    for instrument_id in sorted(instruments):
        instrument = instruments[instrument_id]
        platform = platforms_text(instrument)
        record = {
            "id": instrument_id,
            "name": text_value(instrument.get("name", "")),
            "acronym": text_value(instrument.get("acronym", "")),
            "platform": platform,
            "platform_type": text_value(instrument.get("platform_type", "other")),
            "type": text_value(instrument.get("type", "other")),
            "operator": text_value(instrument.get("operator", "")),
            "status": text_value(instrument.get("status", "")),
            "availability": text_value(instrument.get("availability", "")),
            "href": f"/instruments/{instrument_id}",
        }
        record["search_text"] = " ".join(str(value) for value in record.values()).lower()
        records.append(record)

    return json.dumps(records, indent=2) + "\n"


def render_instrument_details(instruments: dict[str, dict[str, Any]]) -> str:
    """Render rich data for generated instrument detail pages."""

    details = {}
    for instrument_id in sorted(instruments):
        instrument = instruments[instrument_id]
        details[instrument_id] = {
            "id": instrument_id,
            "summary": summary_text(instrument),
            "quick_facts": quick_facts(instrument),
            "timeline": {
                "name": text_value(instrument.get("name")),
                "acronym": text_value(instrument.get("acronym")),
                "type": text_value(instrument.get("type")),
                "status": text_value(instrument.get("status")),
                "start_date": text_value(instrument.get("start_date")),
                "end_date": text_value(instrument.get("end_date")),
            },
            "spectral_summary": spectral_summary(instrument),
            "bands": band_records(instrument),
            "imaging": imaging_records(instrument),
            "data_access": data_access_records(instrument),
            "external_catalogues": external_catalogue_records(instrument),
            "related": related_instruments(instrument_id, instrument, instruments),
            "data_links": link_records(instrument.get("data_links", [])),
            "references": link_records(instrument.get("references", [])),
        }

    return json.dumps(details, indent=2) + "\n"


def render_spectral_comparison_data(
    instruments: dict[str, dict[str, Any]],
) -> str:
    """Render compact band coverage data for interactive plots."""

    records = {}
    for instrument_id in sorted(instruments):
        instrument = instruments[instrument_id]
        extensions = instrument.get("extensions", {})
        spectral = extensions.get("spectral", {}) if isinstance(extensions, dict) else {}
        bands = spectral.get("bands", {}) if isinstance(spectral, dict) else {}
        band_intervals = []
        if isinstance(bands, dict):
            for band_id, band in bands.items():
                if not isinstance(band, dict):
                    continue

                center = number_value(band.get("center_wavelength"))
                bandwidth = number_value(band.get("bandwidth"))
                if center is None or bandwidth is None:
                    continue

                band_intervals.append(
                    {
                        "id": text_value(band_id),
                        "start": max(0.0, center - bandwidth / 2),
                        "end": center + bandwidth / 2,
                        "center": center,
                    }
                )

        records[instrument_id] = {
            "id": instrument_id,
            "name": text_value(instrument.get("name")),
            "acronym": text_value(instrument.get("acronym")),
            "bands": band_intervals,
        }

    return json.dumps(records, separators=(",", ":"), allow_nan=False) + "\n"


def render_spectral_response_data(
    instruments: dict[str, dict[str, Any]],
) -> str:
    """Render full-resolution finite SRF points for on-demand plotting."""

    records = {}
    for instrument_id in sorted(instruments):
        instrument = instruments[instrument_id]
        extensions = instrument.get("extensions", {})
        spectral = extensions.get("spectral", {}) if isinstance(extensions, dict) else {}
        bands = spectral.get("bands", {}) if isinstance(spectral, dict) else {}
        srf = (
            spectral.get("spectral_response_function", {})
            if isinstance(spectral, dict)
            else {}
        )
        wavelengths = srf.get("wavelength", []) if isinstance(srf, dict) else []
        response_curves = []

        if isinstance(wavelengths, list) and isinstance(bands, dict):
            for band_id in bands:
                responses = srf.get(band_id, [])
                if not isinstance(responses, list) or len(responses) != len(wavelengths):
                    continue

                points = []
                for wavelength, response in zip(wavelengths, responses):
                    if isinstance(wavelength, bool) or isinstance(response, bool):
                        continue
                    if not isinstance(wavelength, (int, float)) or not isinstance(
                        response, (int, float)
                    ):
                        continue
                    if not math.isfinite(wavelength) or not math.isfinite(response):
                        continue
                    points.append((float(wavelength), float(response)))

                if points:
                    response_curves.append(
                        {
                            "id": text_value(band_id),
                            "points": points,
                            "peak": max(points, key=lambda point: point[1]),
                        }
                    )

        records[instrument_id] = response_curves

    return json.dumps(records, separators=(",", ":"), allow_nan=False) + "\n"


def summary_text(instrument: dict[str, Any]) -> str:
    """Return a short human-readable mission context summary."""

    instrument_id = text_value(instrument.get("id"))
    name = text_value(instrument.get("name"))
    instrument_type = text_value(instrument.get("type"))
    platform_type = text_value(instrument.get("platform_type"))
    platform = platforms_text(instrument)
    operator = text_value(instrument.get("operator"))
    status = text_value(instrument.get("status"))
    availability = text_value(instrument.get("availability"))

    descriptor = f"{status} {instrument_type}".strip()
    article = article_for(descriptor)
    summary = (
        f"{instrument_id} ({name}) is {article} {descriptor} instrument "
        f"operated by {operator} on {platform}."
    )

    if platform_type or availability:
        summary += (
            f" It is associated with a {platform_type} platform"
            f" and has {availability} data availability."
        )

    return summary


def quick_facts(instrument: dict[str, Any]) -> list[dict[str, str]]:
    """Return compact core metadata facts."""

    facts = [
        ("Instrument id", instrument.get("id")),
        ("Name", instrument.get("name")),
        ("Acronym", instrument.get("acronym")),
        ("Type", instrument.get("type")),
        ("Platform type", instrument.get("platform_type")),
        ("Platform", platforms_text(instrument)),
        ("Operator", instrument.get("operator")),
        ("Start date", instrument.get("start_date")),
        ("End date", instrument.get("end_date")),
        ("Status", instrument.get("status")),
        ("Availability", instrument.get("availability")),
    ]

    return [
        {"label": label, "value": text_value(value)}
        for label, value in facts
        if text_value(value)
    ]


def spectral_summary(instrument: dict[str, Any]) -> list[dict[str, str]]:
    """Return high-level spectral characteristics."""

    extensions = instrument.get("extensions", {})
    spectral = extensions.get("spectral", {}) if isinstance(extensions, dict) else {}
    bands = spectral.get("bands", {}) if isinstance(spectral, dict) else {}
    range_info = spectral.get("range", {}) if isinstance(spectral, dict) else {}

    center_wavelengths: list[float] = []
    bandwidths: list[float] = []
    gsds: list[float] = []

    if isinstance(bands, dict):
        for band in bands.values():
            if not isinstance(band, dict):
                continue

            center_wavelength = number_value(band.get("center_wavelength"))
            bandwidth = number_value(band.get("bandwidth"))
            gsd = number_value(band.get("gsd"))

            if center_wavelength is not None:
                center_wavelengths.append(center_wavelength)
            if bandwidth is not None:
                bandwidths.append(bandwidth)
            if gsd is not None:
                gsds.append(gsd)

    srf_file = text_value(spectral.get("spectral_response_function_file"))
    srf_item = {
        "label": "Spectral response function",
        "value": "Available" if spectral.get("spectral_response_function") else "Not available",
    }
    if srf_file:
        srf_item["url"] = f"{SRF_RAW_BASE_URL}/{quote(srf_file)}"
        srf_item["link_text"] = "Download CSV"

    summary = [
        {"label": "Total bands", "value": str(len(bands)) if isinstance(bands, dict) else ""},
        {"label": "Wavelength range", "value": range_text(center_wavelengths, "nm")},
        {"label": "Bandwidth range", "value": range_text(bandwidths, "nm")},
        {"label": "Ground sampling distance", "value": range_text(gsds, "m")},
        srf_item,
    ]

    if isinstance(range_info, dict) and range_info:
        summary.append(
            {
                "label": "Declared spectral range",
                "value": f"{range_info.get('min', '')}-{range_info.get('max', '')} nm",
            }
        )

    return [item for item in summary if item["value"]]


def band_records(instrument: dict[str, Any]) -> list[dict[str, str]]:
    """Return spectral band rows for the interactive table."""

    extensions = instrument.get("extensions", {})
    spectral = extensions.get("spectral", {}) if isinstance(extensions, dict) else {}
    bands = spectral.get("bands", {}) if isinstance(spectral, dict) else {}
    records = []

    if not isinstance(bands, dict):
        return records

    for band_id, band in bands.items():
        if not isinstance(band, dict):
            continue

        record = {
            "id": text_value(band_id),
            "center_wavelength": text_value(band.get("center_wavelength")),
            "bandwidth": text_value(band.get("bandwidth")),
            "common_name": text_value(band.get("common_name")),
            "gsd": text_value(band.get("gsd")),
            "description": text_value(band.get("band_description")),
            "snr": text_value(band.get("snr")),
        }
        record["search_text"] = " ".join(record.values()).lower()
        records.append(record)

    return records


def imaging_records(instrument: dict[str, Any]) -> list[dict[str, str]]:
    """Return imaging extension properties."""

    extensions = instrument.get("extensions", {})
    imaging = extensions.get("imaging", {}) if isinstance(extensions, dict) else {}

    if not isinstance(imaging, dict):
        return []

    return [
        {"label": heading_text(key), "value": text_value(value)}
        for key, value in sorted(imaging.items())
        if text_value(value)
    ]


def data_access_records(instrument: dict[str, Any]) -> list[dict[str, Any]]:
    """Return structured data access provider records."""

    extensions = instrument.get("extensions", {})
    data_access = extensions.get("data_access", {}) if isinstance(extensions, dict) else {}

    if not isinstance(data_access, dict):
        return []

    providers = []
    for provider_key, provider in data_access.items():
        if not isinstance(provider, dict):
            continue

        products = []
        for product_key, product in provider.items():
            if product_key == "stac_endpoint" or not isinstance(product, dict):
                continue

            products.append(
                {
                    "label": PRODUCT_LABELS.get(product_key, heading_text(product_key)),
                    "docs": text_value(product.get("docs")),
                    "collection": text_value(product.get("collection")),
                }
            )

        labels = ACCESS_POINT_LABELS.get(provider_key, {})
        providers.append(
            {
                "key": provider_key,
                "title": labels.get("title", heading_text(provider_key)),
                "stac_endpoint": text_value(provider.get("stac_endpoint")),
                "products": products,
            }
        )

    return providers


def external_catalogue_records(instrument: dict[str, Any]) -> list[dict[str, str]]:
    """Return external catalogue cross-links."""

    extensions = instrument.get("extensions", {})
    cross_links = extensions.get("cross_links", {}) if isinstance(extensions, dict) else {}

    if not isinstance(cross_links, dict):
        return []

    return [
        {"label": CROSS_LINK_LABELS.get(key, heading_text(key)), "url": text_value(url)}
        for key, url in cross_links.items()
        if text_value(url)
    ]


def link_records(links: Any) -> list[dict[str, str]]:
    """Return URL records from a link list."""

    if not isinstance(links, list):
        return []

    return [{"url": text_value(link)} for link in links if text_value(link)]


def related_instruments(
    instrument_id: str,
    instrument: dict[str, Any],
    instruments: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    """Return instruments related by catalogue-generated relationship fields."""

    related = []
    seen = set()

    relationship_groups = [
        ("family", "same instrument family"),
        ("platform_companions", "same platform"),
    ]

    for field_name, reason in relationship_groups:
        related_ids = instrument.get(field_name, [])
        if not isinstance(related_ids, list):
            continue

        for related_id in related_ids:
            related_id = str(related_id)
            if related_id in seen or related_id not in instruments:
                continue

            related_instrument = instruments[related_id]
            related.append(
                {
                    "id": related_id,
                    "name": text_value(related_instrument.get("name")),
                    "platform": platforms_text(related_instrument),
                    "href": f"/instruments/{related_id}",
                    "reason": reason,
                }
            )
            seen.add(related_id)

    return related


def generate_pages() -> None:
    """Generate the VitePress instrument index and instrument pages."""

    instruments = load_catalogue()
    INSTRUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    VITEPRESS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    (INSTRUMENTS_DIR / "index.md").write_text(render_index(instruments), encoding="utf-8")
    (VITEPRESS_DATA_DIR / "instruments.json").write_text(
        render_index_data(instruments), encoding="utf-8"
    )
    (VITEPRESS_DATA_DIR / "instrument-details.json").write_text(
        render_instrument_details(instruments), encoding="utf-8"
    )
    SPECTRAL_COMPARISON_PATH.write_text(
        render_spectral_comparison_data(instruments), encoding="utf-8"
    )
    SPECTRAL_RESPONSE_PATH.write_text(
        render_spectral_response_data(instruments), encoding="utf-8"
    )

    for instrument_id, instrument in instruments.items():
        output_path = INSTRUMENTS_DIR / f"{instrument_id}.md"
        output_path.write_text(render_instrument_page(instrument), encoding="utf-8")

    generate_schema_document(schema_path=DOCS_SCHEMA_PATH, link_base=GITHUB_BLOB_BASE_URL)
    if CONTRIBUTING_PATH.exists():
        DOCS_CONTRIBUTING_PATH.write_text(
            CONTRIBUTING_PATH.read_text(encoding="utf-8"), encoding="utf-8"
        )

    print(f"Generated {len(instruments)} instrument pages in {INSTRUMENTS_DIR}")


if __name__ == "__main__":
    generate_pages()
