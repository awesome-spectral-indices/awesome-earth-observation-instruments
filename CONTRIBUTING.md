# Contributing

Thanks for helping improve Awesome Earth Observation Instruments.

This catalogue is intended to be useful to Earth Observation practitioners,
software developers, researchers, and general users who need reliable instrument
metadata. Contributions should keep the catalogue machine-readable, traceable,
and easy to understand.

## What You Can Contribute

- New instrument records in `src/instruments/`.
- Spectral band CSV files in `src/bands/`.
- Spectral response function CSV files in `src/srf/`.
- Schema improvements in `schema/`.
- Data access metadata for supported providers.
- Cross-links to trusted external catalogues.

## Instrument Records

Add one YAML file per instrument in `src/instruments/`. Use existing files as
templates and validate the record before opening a pull request. You can also check the
full schema and extensions in `schema/core/` and `schema/extensions/`.
Tables summarising the full schema can be found in `SCHEMA.md`.

Each instrument should include:

- Stable instrument `id`.
- Full `name` and `acronym`.
- Instrument `type` and `platform_type`.
- Platform, operator, lifecycle status, and availability.
- References and data links.
- Relevant extension blocks, especially spectral metadata when available.

Prefer authoritative sources such as mission pages, technical handbooks,
scientific papers, provider catalogues, and official data access documentation.

## Spectral Data

If bands are provided as a CSV file, place it in `src/bands/` and reference the
filename from the instrument YAML. If an SRF CSV is available, place it in
`src/srf/` and reference it through `spectral_response_function`.

The catalogue generator materializes these CSV files into `catalogue.json`, so
do not manually edit transformed spectral data in the generated catalogue.

## Generated Files

Do not manually edit generated files unless you are only prototyping a template.
Update the source data or generator instead.

Generated files include:

- `catalogue/catalogue.json`
- `README.md`
- `SCHEMA.md`
- `docs/schema.md`
- `docs/contributing.md`
- `docs/instruments/*.md`
- `docs/.vitepress/data/*.json`

## Local Checks

Use the project environment and run:

```bash
python src/code/catalogue.py
python src/code/readme.py
python src/code/vitepress.py
python -m pytest tests
```

If your change affects the website, also run the VitePress build in an
environment with Node.js available:

```bash
npm run docs:build
```

## Pull Request Checklist

- The source YAML/CSV files are valid.
- Generated outputs have been updated when needed.
- Tests pass.
- New metadata is supported by references or provider documentation.
- The contribution avoids duplicating information already derived by generators.
