from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "code"))

from catalogue import CATALOGUE_NAME, generate_catalogue
from readme import generate_readme, generate_schema_document
from validators import validate_all_instruments


@pytest.fixture(scope="session")
def generated_outputs(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    # Generate files in pytest's temp directory so tests never rewrite repo outputs.
    output_dir = tmp_path_factory.mktemp("generated")
    catalogue_path = output_dir / "catalogue.json"
    schema_path = output_dir / "SCHEMA.md"
    readme_path = output_dir / "README.md"

    generate_catalogue(output_path=catalogue_path)
    generate_schema_document(schema_path=schema_path)
    generate_readme(catalogue_path=catalogue_path, readme_path=readme_path)

    return {
        "catalogue": catalogue_path,
        "schema": schema_path,
        "readme": readme_path,
    }


def test_all_instruments_validate() -> None:
    # Every YAML source file should pass schema and custom spectral validation.
    instrument_files = sorted((REPO_ROOT / "src" / "instruments").glob("*.yaml"))
    instruments = validate_all_instruments(REPO_ROOT / "src" / "instruments")

    assert len(instruments) == len(instrument_files)
    assert {instrument["id"] for instrument in instruments}


def test_catalogue_structure_and_spectral_transforms(
    generated_outputs: dict[str, Path],
) -> None:
    # The public catalogue contract is metadata plus an instruments object.
    catalogue = json.loads(generated_outputs["catalogue"].read_text(encoding="utf-8"))

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


def test_documentation_outputs_have_expected_sections(
    generated_outputs: dict[str, Path],
) -> None:
    # README keeps the human overview; SCHEMA.md owns the generated schema tables.
    readme = generated_outputs["readme"].read_text(encoding="utf-8")
    schema = generated_outputs["schema"].read_text(encoding="utf-8")

    assert "See the [schema specification](SCHEMA.md)" in readme
    assert "# Catalogue" in readme
    assert "## Core Schema" not in readme
    assert "## Spectral Extension" not in readme

    assert schema.startswith("# Schema Specification")
    assert "## Core Schema" in schema
    assert "## Spectral Extension" in schema


def test_generated_files_are_current(generated_outputs: dict[str, Path]) -> None:
    # Generated files in the repo should match fresh output from the generators.
    expected_outputs = {
        "catalogue": REPO_ROOT / "catalogue" / "catalogue.json",
        "schema": REPO_ROOT / "SCHEMA.md",
        "readme": REPO_ROOT / "README.md",
    }

    for name, committed_path in expected_outputs.items():
        assert generated_outputs[name].read_text(encoding="utf-8") == committed_path.read_text(
            encoding="utf-8"
        )
