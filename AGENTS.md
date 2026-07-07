# Agent Guide

This repository is the source for **Awesome Earth Observation Instruments**, a
machine-readable catalogue of Earth Observation (EO) instruments.

## Repository Map

| Path | Purpose |
| --- | --- |
| `schema/core/core.yaml` | Core instrument schema |
| `schema/extensions/*.yaml` | Spectral, imaging, data access, and cross-link extensions |
| `schema/extensions/data_access_points/*.yaml` | Provider-specific data access schemas |
| `src/instruments/*.yaml` | One source record per instrument |
| `src/bands/*.csv` | Optional external spectral-band definitions |
| `src/srf/*.csv` | Optional spectral response functions (SRFs) |
| `src/code/validators.py` | Source input validation |
| `src/code/catalogue.py` | JSON catalogue generation |
| `src/code/readme.py` | Root `README.md` and `SCHEMA.md` generation |
| `tests/` | Pytest checks for validation and generated outputs |
| `catalogue/catalogue.json` | Generated catalogue output |
| `SCHEMA.md` | Generated schema specification tables |
| `readme/HEADER.md`, `readme/BODY.md`, `readme/FOOTER.md` | README source sections |
| `pyproject.toml` | Project metadata, version, and runtime dependencies |

## Editing Rules

- Treat `README.md`, `SCHEMA.md`, and `catalogue/catalogue.json` as generated files. Update
  their source or generator, then regenerate them.
- Do not change files in `schema/` unless the task explicitly requires schema
  changes. If a schema change becomes necessary but was not requested, ask first.
- Keep schema property descriptions clear, formal, and suitable for EO users.
- Use `src/instruments/`, `src/bands/`, and `src/srf/` as the authoritative
  source inputs; do not manually edit transformed data in the generated catalogue.
- Keep `pyproject.toml` minimal and ensure it lists dependencies required by the
  validation and generation scripts.

## Validation Requirements

`src/code/validators.py` must validate every YAML file in `src/instruments/`.

It must provide:

1. Core and extension schema validation.
2. Spectral extension validation, when present:
   - `bands` as CSV: the file must exist in `src/bands/`, and CSV columns/values
     must validate as the inline `bands` schema representation.
   - `range`: `min` and `max` must be non-negative, and `min < max`.
   - `spectral_response_function`: the CSV must exist in `src/srf/`, include a
     `wavelength` column, and its band columns must match the spectral bands.

## Catalogue Generation

`src/code/catalogue.py` generates `catalogue/catalogue.json` only after input
validation passes.

The output structure is:

```json
{
  "name": "Awesome Earth Observation Instruments",
  "version": "<version from pyproject.toml>",
  "link": "<URL to catalogue/catalogue.json>",
  "instruments": {
    "<instrument id>": "<complete transformed instrument object>"
  }
}
```

Transformation rules:

- Convert a CSV `spectral.bands` value to the inline dictionary form defined by
  `schema/extensions/spectral.yaml`.
- Convert `spectral.spectral_response_function` CSV content to an object keyed
  by column name, with each column represented as an array. All arrays must have
  equal length.
- When `spectral.range` is supplied instead of `spectral.bands`, create
  `spectral.bands` as `B1` through `Bn`, using `min`, `max`, and `total_bands`
  to calculate `center_wavelength` and `bandwidth`.

## Documentation Generation

`src/code/readme.py` generates the root `README.md` from the catalogue and
documentation fragments in this order:

1. `readme/HEADER.md`
2. `readme/BODY.md`
3. A first-level `# Catalogue` section with a short introduction and a table of
   contents containing only existing platform/type groupings.
4. Instrument tables grouped by platform type (`satellite`, `airborne`, `uav`,
   `terrestrial`) and then instrument type (`multispectral`, `hyperspectral`,
   `radar`, `lidar`, `rgb`, `other`). Omit empty groups.
5. `readme/FOOTER.md`

The same script generates root `SCHEMA.md` with one table for the core schema,
one for each extension, and one for each data access point schema. Each table
title links to its YAML source. Columns: `Property`, `Required`, `Type`,
`Description`. Bold required property names and `Yes` values. `readme/BODY.md`
should link readers to `SCHEMA.md`.

Instrument table columns:

| Column | Content |
| --- | --- |
| `Id` | Instrument id linked to its first `references` URL |
| `Name` | Instrument name |
| `Platforms` | Comma-separated platforms |
| `Status` | Bold status with emoji: `operational :white_check_mark:`, `planned :stars:`, `experimental :warning:`, `retired :no_entry:` |
| `Earth Engine` | `[:link: link](docs-url)` for `extensions.data_access.ee.primary.docs`, otherwise blank |
| `Planetary Computer` | `[:link: link](docs-url)` for `extensions.data_access.planetary_computer.primary.docs`, otherwise blank |

## Completion Checklist

After changes that affect source inputs, schemas, or generators:

1. Run validation for all instrument source files.
2. Regenerate `catalogue/catalogue.json`.
3. Regenerate `README.md` and `SCHEMA.md`.
4. Run `python -m pytest tests`.
5. Confirm generated output reflects the requested change.
