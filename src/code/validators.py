from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schema"
INSTRUMENTS_DIR = REPO_ROOT / "src" / "instruments"
BANDS_DIR = REPO_ROOT / "src" / "bands"
SRF_DIR = REPO_ROOT / "src" / "srf"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _normalize_dates(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _normalize_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_normalize_dates(i) for i in obj]
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    return obj


def _resolve_instrument_path(instrument: str | Path) -> Path:
    candidate = Path(instrument)
    if candidate.is_absolute():
        return candidate
    return INSTRUMENTS_DIR / candidate


def _with_resource(registry: Registry, uri: str, schema: dict[str, Any]) -> Registry:
    return registry.with_resource(uri, Resource.from_contents(schema))


def _schema_registry() -> tuple[Registry, dict[str, Any], dict[str, Any]]:
    registry = Registry()

    core_path = SCHEMA_DIR / "core" / "core.yaml"
    core_schema = _load_yaml(core_path)
    registry = _with_resource(registry, core_path.as_uri(), core_schema)
    if "$id" in core_schema:
        registry = _with_resource(registry, str(core_schema["$id"]), core_schema)

    extension_files = [
        "extensions/spectral.yaml",
        "extensions/imaging.yaml",
        "extensions/earth-engine.yaml",
        "extensions/planetary-computer.yaml",
    ]
    spectral_schema: dict[str, Any] | None = None
    for rel in extension_files:
        path = SCHEMA_DIR / rel
        schema = _load_yaml(path)
        registry = _with_resource(registry, path.as_uri(), schema)
        if "$id" in schema:
            registry = _with_resource(registry, str(schema["$id"]), schema)
        if rel.endswith("spectral.yaml"):
            spectral_schema = schema

    if spectral_schema is None:
        raise ValidationError("Missing spectral schema.")
    return registry, core_schema, spectral_schema


def _format_path(path_parts: Any) -> str:
    path = ".".join(map(str, path_parts))
    return path or "<root>"


class ValidationError(Exception):
    pass


def validate_schema(instrument: str | Path) -> dict[str, Any]:
    registry, core_schema, _ = _schema_registry()
    validator = Draft202012Validator(core_schema, registry=registry)

    instrument_path = _resolve_instrument_path(instrument)
    data = _normalize_dates(_load_yaml(instrument_path))

    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        messages = [f"{_format_path(e.path)}: {e.message}" for e in errors]
        raise ValidationError("Schema validation failed:\n" + "\n".join(messages))
    return data


def _validate_bands_csv(
    bands_filename: str,
    instrument_id: str,
    spectral_schema: dict[str, Any],
) -> list[str]:
    bands_path = BANDS_DIR / bands_filename
    if not bands_path.exists():
        raise ValidationError(
            f"[{instrument_id}] bands CSV not found: {bands_path.as_posix()}"
        )

    df = pd.read_csv(bands_path)
    band_props = (
        spectral_schema["properties"]["bands"]["oneOf"][1]["additionalProperties"]["properties"]
    )
    required = set(
        spectral_schema["properties"]["bands"]["oneOf"][1]["additionalProperties"]["required"]
    )
    allowed_columns = set(band_props.keys()) | {"band"}
    csv_columns = set(df.columns)

    missing = (required | {"band"}) - csv_columns
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValidationError(f"[{instrument_id}] bands CSV missing columns: {missing_cols}")

    unexpected = csv_columns - allowed_columns
    if unexpected:
        unexpected_cols = ", ".join(sorted(unexpected))
        raise ValidationError(
            f"[{instrument_id}] bands CSV has unexpected columns: {unexpected_cols}"
        )

    band_schema = {
        "type": "object",
        "required": sorted(required),
        "properties": band_props,
        "additionalProperties": False,
    }
    band_validator = Draft202012Validator(band_schema)
    ordered_band_ids: list[str] = []

    for idx, row in df.iterrows():
        band_id = row.get("band")
        if pd.isna(band_id) or str(band_id).strip() == "":
            raise ValidationError(f"[{instrument_id}] bands CSV row {idx + 2}: empty band id.")
        band_id = str(band_id).strip()
        ordered_band_ids.append(band_id)

        band_payload: dict[str, Any] = {}
        for col in band_props:
            if col in df.columns and not pd.isna(row[col]):
                band_payload[col] = row[col].item() if hasattr(row[col], "item") else row[col]

        row_errors = sorted(band_validator.iter_errors(band_payload), key=lambda e: list(e.path))
        if row_errors:
            messages = [f"{_format_path(e.path)}: {e.message}" for e in row_errors]
            raise ValidationError(
                f"[{instrument_id}] bands CSV row {idx + 2} failed validation:\n"
                + "\n".join(messages)
            )

    if len(set(ordered_band_ids)) != len(ordered_band_ids):
        raise ValidationError(f"[{instrument_id}] bands CSV has duplicate band identifiers.")
    return ordered_band_ids


def _validate_range(range_data: dict[str, Any], instrument_id: str) -> None:
    minimum = range_data.get("min")
    maximum = range_data.get("max")
    if minimum is None or maximum is None:
        return
    if minimum < 0 or maximum < 0:
        raise ValidationError(f"[{instrument_id}] spectral.range values cannot be negative.")
    if minimum > maximum:
        raise ValidationError(
            f"[{instrument_id}] spectral.range.min must be lower than spectral.range.max."
        )


def _validate_srf_csv(
    srf_filename: str,
    instrument_id: str,
    expected_bands: list[str] | None,
) -> None:
    srf_path = SRF_DIR / srf_filename
    if not srf_path.exists():
        raise ValidationError(
            f"[{instrument_id}] SRF CSV not found: {srf_path.as_posix()}"
        )

    df = pd.read_csv(srf_path)
    if "wavelength" not in df.columns:
        raise ValidationError(f"[{instrument_id}] SRF CSV must include a 'wavelength' column.")

    if expected_bands is not None:
        srf_bands = [c for c in df.columns if c != "wavelength"]
        if srf_bands != expected_bands:
            raise ValidationError(
                f"[{instrument_id}] SRF columns must match spectral bands in the same order. "
                f"Expected {expected_bands}, found {srf_bands}."
            )


def validate_spectral_extension(instrument_data: dict[str, Any]) -> None:
    _, _, spectral_schema = _schema_registry()

    instrument_id = str(instrument_data.get("id", "<unknown>"))
    spectral = instrument_data.get("extensions", {}).get("spectral")
    if not spectral:
        return

    expected_bands: list[str] | None = None
    if "bands" in spectral:
        bands = spectral["bands"]
        if isinstance(bands, str):
            expected_bands = _validate_bands_csv(bands, instrument_id, spectral_schema)
        elif isinstance(bands, dict):
            expected_bands = list(bands.keys())

    if "range" in spectral:
        _validate_range(spectral["range"], instrument_id)

    if "spectral_response_function" in spectral:
        _validate_srf_csv(
            spectral["spectral_response_function"], instrument_id, expected_bands
        )


def validate_instrument(instrument: str | Path) -> dict[str, Any]:
    data = validate_schema(instrument)
    validate_spectral_extension(data)
    return data


def validate_all_instruments(instruments_dir: Path | None = None) -> list[dict[str, Any]]:
    target_dir = instruments_dir or INSTRUMENTS_DIR
    results: list[dict[str, Any]] = []
    for instrument_path in sorted(target_dir.glob("*.yaml")):
        results.append(validate_instrument(instrument_path))
    return results
