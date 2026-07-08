from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from validators import BANDS_DIR, INSTRUMENTS_DIR, REPO_ROOT, SRF_DIR, validate_instrument

CATALOGUE_DIR = REPO_ROOT / "catalogue"
CATALOGUE_PATH = CATALOGUE_DIR / "catalogue.json"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
CATALOGUE_NAME = "Awesome Earth Observation Instruments"
CATALOGUE_LINK = (
    "https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/"
    "raw/refs/heads/main/catalogue/catalogue.json"
)


def _to_python_scalar(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    return value


def _bands_csv_to_object(filename: str) -> dict[str, dict[str, Any]]:
    frame = pd.read_csv(BANDS_DIR / filename)
    output: dict[str, dict[str, Any]] = {}
    for _, row in frame.iterrows():
        band_id = str(row["band"]).strip()
        band_payload: dict[str, Any] = {}
        for col in frame.columns:
            if col == "band":
                continue
            value = row[col]
            if pd.isna(value):
                continue
            band_payload[col] = _to_python_scalar(value)
        output[band_id] = band_payload
    return output


def _srf_csv_to_object(filename: str) -> dict[str, list[Any]]:
    frame = pd.read_csv(SRF_DIR / filename)
    output: dict[str, list[Any]] = {}
    for col in frame.columns:
        output[col] = [_to_python_scalar(v) for v in frame[col].tolist()]

    lengths = {len(values) for values in output.values()}
    if len(lengths) > 1:
        raise ValueError(f"SRF arrays must have identical lengths in {filename}.")
    return output


def _bands_from_range(range_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    minimum = float(range_payload["min"])
    maximum = float(range_payload["max"])
    total_bands = int(range_payload["total_bands"])
    if total_bands <= 0:
        raise ValueError("spectral.range.total_bands must be greater than 0.")
    if maximum <= minimum:
        raise ValueError("spectral.range.max must be greater than spectral.range.min.")

    bandwidth = (maximum - minimum) / total_bands
    bands: dict[str, dict[str, Any]] = {}
    for idx in range(total_bands):
        band_name = f"B{idx + 1}"
        center_wavelength = minimum + (idx + 0.5) * bandwidth
        bands[band_name] = {
            "center_wavelength": center_wavelength,
            "bandwidth": bandwidth,
        }
    return bands


def _materialize_spectral_csvs(instrument: dict[str, Any]) -> dict[str, Any]:
    result = json.loads(json.dumps(instrument))
    spectral = result.get("extensions", {}).get("spectral")
    if not spectral:
        return result

    bands_value = spectral.get("bands")
    if isinstance(bands_value, str):
        spectral["bands"] = _bands_csv_to_object(bands_value)
    elif "bands" not in spectral and isinstance(spectral.get("range"), dict):
        range_payload = spectral["range"]
        if "total_bands" in range_payload and "min" in range_payload and "max" in range_payload:
            spectral["bands"] = _bands_from_range(range_payload)

    srf_value = spectral.get("spectral_response_function")
    if isinstance(srf_value, str):
        spectral["spectral_response_function_file"] = srf_value
        spectral["spectral_response_function"] = _srf_csv_to_object(srf_value)
    return result


def _project_version(pyproject_path: Path = PYPROJECT_PATH) -> str:
    if not pyproject_path.exists():
        raise FileNotFoundError(f"{pyproject_path.as_posix()} not found.")

    in_project = False
    for line in pyproject_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"
            continue
        if in_project and stripped.startswith("version"):
            _, value = stripped.split("=", 1)
            return value.strip().strip("\"'")
    raise ValueError("Could not find [project].version in pyproject.toml.")


def _platform_set(instrument: dict[str, Any]) -> set[str]:
    platforms = instrument.get("platform", [])
    if isinstance(platforms, list):
        return {str(platform) for platform in platforms}
    if platforms:
        return {str(platforms)}
    return set()


def _same_family(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_name = left.get("name")
    right_name = right.get("name")
    left_acronym = left.get("acronym")
    right_acronym = right.get("acronym")

    return bool(
        (left_name and left_name == right_name)
        or (left_acronym and left_acronym == right_acronym)
    )


def _add_generated_relationships(instruments: dict[str, dict[str, Any]]) -> None:
    """Add catalogue-derived relationship fields to each instrument."""

    for instrument_id, instrument in instruments.items():
        platform = _platform_set(instrument)
        family: list[str] = []
        platform_companions: list[str] = []

        for other_id, other in instruments.items():
            if other_id == instrument_id:
                continue

            if _same_family(instrument, other):
                family.append(other_id)
                continue

            if platform and platform.intersection(_platform_set(other)):
                platform_companions.append(other_id)

        instrument["family"] = sorted(family)
        instrument["platform_companions"] = sorted(platform_companions)


def generate_catalogue(
    instruments_dir: Path = INSTRUMENTS_DIR,
    output_path: Path = CATALOGUE_PATH,
) -> dict[str, Any]:
    instruments: dict[str, dict[str, Any]] = {}
    for instrument_path in sorted(instruments_dir.glob("*.yaml")):
        validated = validate_instrument(instrument_path)
        materialized = _materialize_spectral_csvs(validated)
        instruments[materialized["id"]] = materialized

    _add_generated_relationships(instruments)

    catalogue = {
        "name": CATALOGUE_NAME,
        "version": _project_version(),
        "link": CATALOGUE_LINK,
        "instruments": instruments,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(catalogue, handle, indent=2, ensure_ascii=False)
    return catalogue


if __name__ == "__main__":
    generate_catalogue()
