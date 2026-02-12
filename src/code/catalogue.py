from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from validators import BANDS_DIR, INSTRUMENTS_DIR, REPO_ROOT, SRF_DIR, validate_instrument

CATALOGUE_DIR = REPO_ROOT / "catalogue"
CATALOGUE_PATH = CATALOGUE_DIR / "catalogue.json"


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


def _materialize_spectral_csvs(instrument: dict[str, Any]) -> dict[str, Any]:
    result = json.loads(json.dumps(instrument))
    spectral = result.get("extensions", {}).get("spectral")
    if not spectral:
        return result

    bands_value = spectral.get("bands")
    if isinstance(bands_value, str):
        spectral["bands"] = _bands_csv_to_object(bands_value)

    srf_value = spectral.get("spectral_response_function")
    if isinstance(srf_value, str):
        spectral["spectral_response_function"] = _srf_csv_to_object(srf_value)
    return result


def generate_catalogue(
    instruments_dir: Path = INSTRUMENTS_DIR,
    output_path: Path = CATALOGUE_PATH,
) -> dict[str, dict[str, Any]]:
    catalogue: dict[str, dict[str, Any]] = {}
    for instrument_path in sorted(instruments_dir.glob("*.yaml")):
        validated = validate_instrument(instrument_path)
        materialized = _materialize_spectral_csvs(validated)
        catalogue[materialized["id"]] = materialized

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(catalogue, handle, indent=2, ensure_ascii=False)
    return catalogue


if __name__ == "__main__":
    generate_catalogue()
