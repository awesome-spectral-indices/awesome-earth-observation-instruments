from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "code"))

from catalogue import CATALOGUE_NAME, _bands_from_range, generate_catalogue
from validators import (
    ValidationError,
    _validate_range,
    validate_all_instruments,
    validate_instrument,
)


@pytest.fixture(scope="session")
def generated_outputs(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    # Generate catalogue output in pytest's temp directory so tests never rewrite repo files.
    output_dir = tmp_path_factory.mktemp("generated")
    catalogue_path = output_dir / "catalogue.json"

    generate_catalogue(output_path=catalogue_path)

    return {
        "catalogue": catalogue_path,
    }


def test_all_instruments_validate() -> None:
    # Every YAML source file should pass schema and custom spectral validation.
    instrument_files = sorted((REPO_ROOT / "src" / "instruments").glob("*.yaml"))
    instruments = validate_all_instruments(REPO_ROOT / "src" / "instruments")

    assert len(instruments) == len(instrument_files)
    assert {instrument["id"] for instrument in instruments}


@pytest.mark.parametrize(
    ("platform_type", "status", "is_valid"),
    [
        ("satellite", "operational", True),
        ("satellite", "active", False),
        ("airborne", "retired", True),
        ("airborne", "legacy", False),
        ("uav", "active", True),
        ("uav", "operational", False),
        ("terrestrial", "legacy", True),
        ("terrestrial", "retired", False),
        ("uav", "experimental", True),
        ("satellite", "planned", True),
    ],
)
def test_status_matches_platform_lifecycle(
    tmp_path: Path,
    platform_type: str,
    status: str,
    is_valid: bool,
) -> None:
    instrument = {
        "id": "TEST_STATUS",
        "name": "Status Test Instrument",
        "acronym": "TEST",
        "type": "other",
        "platform_type": platform_type,
        "platform": ["Test platform"],
        "operator": ["Test operator"],
        "start_date": "2020-01-01",
        "status": status,
        "availability": "private",
        "references": ["https://example.com"],
    }
    instrument_path = tmp_path / "TEST_STATUS.yaml"
    instrument_path.write_text(yaml.safe_dump(instrument), encoding="utf-8")

    if is_valid:
        assert validate_instrument(instrument_path)["status"] == status
    else:
        with pytest.raises(ValidationError):
            validate_instrument(instrument_path)


def test_catalogue_structure_and_spectral_transforms(
    generated_outputs: dict[str, Path],
) -> None:
    # The public catalogue contract is metadata plus an instruments object.
    catalogue_text = generated_outputs["catalogue"].read_text(encoding="utf-8")
    catalogue = json.loads(
        catalogue_text,
        parse_constant=lambda value: pytest.fail(
            f"Catalogue contains non-standard JSON constant: {value}"
        ),
    )
    assert catalogue_text == json.dumps(
        catalogue,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    )

    assert list(catalogue.keys()) == ["name", "version", "link", "instruments"]
    assert catalogue["name"] == CATALOGUE_NAME
    assert catalogue["version"]
    assert catalogue["link"].endswith("/catalogue/catalogue.json")
    assert isinstance(catalogue["instruments"], dict)

    instruments = catalogue["instruments"]

    # EMIT is the current real fixture for range-based hyperspectral band generation.
    assert "EMIT" in instruments
    emit_bands = instruments["EMIT"]["extensions"]["spectral"]["bands"]
    assert len(emit_bands) == instruments["EMIT"]["extensions"]["spectral"]["range"]["total_bands"]
    assert set(emit_bands["B1"]) == {"center_wavelength", "bandwidth"}

    # CSV-backed spectral inputs should be materialized as dictionaries in the catalogue.
    csv_backed = [
        instrument
        for instrument in instruments.values()
        if isinstance(instrument.get("extensions", {}).get("spectral", {}).get("bands"), dict)
        and "spectral_response_function" in instrument.get("extensions", {}).get("spectral", {})
    ]
    assert csv_backed

    for instrument in csv_backed:
        spectral = instrument["extensions"]["spectral"]
        assert isinstance(spectral["bands"], dict)
        assert isinstance(spectral["spectral_response_function"], dict)
        srf_lengths = {len(values) for values in spectral["spectral_response_function"].values()}
        assert len(srf_lengths) == 1

    # Empty cells in sparse SRF CSVs must be represented by valid JSON nulls.
    assert "NaN" not in catalogue_text
    assert any(
        value is None
        for instrument in csv_backed
        for values in instrument["extensions"]["spectral"][
            "spectral_response_function"
        ].values()
        for value in values
    )


def test_range_bandwidth_overrides_generated_bandwidth() -> None:
    # An explicit range bandwidth applies uniformly without changing band centers.
    total_band_range = {
        "min": 400,
        "max": 500,
        "total_bands": 4,
        "bandwidth": 12,
    }
    total_band_result = _bands_from_range(total_band_range)

    assert [band["center_wavelength"] for band in total_band_result.values()] == [
        412.5,
        437.5,
        462.5,
        487.5,
    ]
    assert {band["bandwidth"] for band in total_band_result.values()} == {12.0}

    sampling_range = {
        "min": 400,
        "max": 410,
        "sampling": 3,
        "bandwidth": 1.5,
    }
    sampling_result = _bands_from_range(sampling_range)

    assert [band["center_wavelength"] for band in sampling_result.values()] == [
        400.0,
        403.0,
        406.0,
        409.0,
    ]
    assert {band["bandwidth"] for band in sampling_result.values()} == {1.5}


def test_range_defaults_bandwidth_to_generation_interval() -> None:
    total_band_result = _bands_from_range(
        {"min": 400, "max": 500, "total_bands": 4}
    )
    sampling_result = _bands_from_range({"min": 400, "max": 410, "sampling": 3})

    assert {band["bandwidth"] for band in total_band_result.values()} == {25.0}
    assert {band["bandwidth"] for band in sampling_result.values()} == {3.0}


def test_sampling_range_bandwidth_is_materialized_end_to_end(tmp_path: Path) -> None:
    # Exercise schema validation and catalogue generation with a sampling-based range.
    instrument = yaml.safe_load(
        (REPO_ROOT / "src" / "instruments" / "EMIT.yaml").read_text(encoding="utf-8")
    )
    instrument["id"] = "TEST_SAMPLING_RANGE"
    instrument["extensions"]["spectral"]["range"] = {
        "min": 400,
        "max": 410,
        "sampling": 3,
        "bandwidth": 1.5,
    }

    instrument_path = tmp_path / "TEST_SAMPLING_RANGE.yaml"
    instrument_path.write_text(yaml.safe_dump(instrument), encoding="utf-8")
    catalogue = generate_catalogue(
        instruments_dir=tmp_path,
        output_path=tmp_path / "catalogue.json",
    )
    bands = catalogue["instruments"]["TEST_SAMPLING_RANGE"]["extensions"][
        "spectral"
    ]["bands"]

    assert list(bands) == ["B1", "B2", "B3", "B4"]
    assert [band["center_wavelength"] for band in bands.values()] == [
        400.0,
        403.0,
        406.0,
        409.0,
    ]
    assert {band["bandwidth"] for band in bands.values()} == {1.5}


@pytest.mark.parametrize(
    "range_data",
    [
        {"min": 400, "max": 400, "total_bands": 1},
        {"min": 400, "max": 500, "sampling": 0},
        {"min": 400, "max": 500, "total_bands": 0},
        {"min": 400, "max": 500, "sampling": 5, "bandwidth": 0},
        {"min": 400, "max": 500, "sampling": 5, "total_bands": 20},
    ],
)
def test_invalid_range_generation_parameters_are_rejected(
    range_data: dict[str, float | int],
) -> None:
    with pytest.raises(ValidationError):
        _validate_range(range_data, "TEST")
