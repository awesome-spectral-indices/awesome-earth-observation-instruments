# Changelog

All notable changes to Awesome Earth Observation Instruments are summarized here.

## 0.3.0 (Upcoming)

### Catalogue

- Serialized missing spectral response samples as JSON `null` values instead
  of non-standard `NaN` constants.
- Minified `catalogue.json` by removing non-semantic formatting whitespace.

### Schema

- Added platform-specific lifecycle validation: satellite and airborne
  instruments use `operational` or `retired`, while UAV and terrestrial
  instruments use `active` or `legacy`; all platforms retain `experimental`
  and `planned`.

### Instruments And Metadata

- Added separate Parrot Sequoia multispectral and RGB UAV instrument records,
  including the four-band multispectral definition.
- Added Sentinel-3A and Sentinel-3B OLCI instrument records with shared nominal
  band definitions and platform-specific mean spectral response functions.
- Migrated existing UAV instrument lifecycle statuses from `operational` and
  `retired` to `active` and `legacy`.

## 0.2.0

### Catalogue

- Consolidated provider-specific data access metadata under the `data_access`
  extension.
- Added generated `family` and `platform_companions` relationship fields to
  each instrument in `catalogue.json`.
- Preserved the original SRF CSV filename in
  `spectral.spectral_response_function_file` while still materializing SRF CSV
  content into the catalogue.
- Added generated spectral bands for range-based instruments using either
  `total_bands` or `sampling`.
- Added support for assigning an optional range-level `bandwidth` to every
  generated spectral band.
- Added Copernicus Data Space Ecosystem data access support.
- Added EOPF Sentinel Zarr Samples data access support.

### Schema

- Added the `cross_links` extension for external catalogue URLs.
- Added the consolidated `data-access.yaml` extension.
- Moved provider-specific access schemas into
  `schema/extensions/data_access_points/`.
- Added the optional `spectral.range.bandwidth` property for declaring a common
  bandwidth across generated bands.
- Updated schema identifiers and references to raw GitHub URLs.
- Improved schema property descriptions.

### Instruments And Metadata

- Added ASTER with VNIR, SWIR, and TIR band definitions, system response
  functions, data-access metadata, and external catalogue links.
- Added MODIS instrument records for the Terra and Aqua platforms.
- Added the MicaSense RedEdge-P, Altum-PT, and three Altum serial-number UAV
  instrument configurations with their corresponding spectral band
  definitions.
- Added MicaSense RedEdge-MX RX01 and RX02-or-higher UAV configurations with
  their serial-dependent spectral band definitions.
- Added the legacy MicaSense RedEdge 3 UAV instrument and spectral band
  definitions.
- Added the legacy MicaSense RedEdge-M UAV instrument and spectral band
  definitions.
- Added shared MODIS band definitions and platform-specific Terra and Aqua
  spectral response functions.
- Added Google Earth Engine and Microsoft Planetary Computer access metadata
  for the MODIS MCD43A4 NBAR product.
- Added EarthData, CEOS EO Handbook, and IndexDataBase cross-links for MODIS.
- Added cross-links for EMIT, ETM+, MSS, MSI, OLI, TIRS, and TM records where
  available.
- Added EarthData, CEOS EO Handbook, and IndexDataBase links where available.
- Added CDSE access metadata for Landsat and Sentinel records where available.
- Added EOPF access metadata for Sentinel-2 MSI records.

### Documentation

- Moved README source fragments into `readme/`.
- Split schema documentation out of the root README into `SCHEMA.md`.
- Added generated VitePress instrument pages.
- Added searchable VitePress instrument index.
- Added richer single-instrument pages with quick facts, spectral summaries,
  searchable band tables, data access cards, external catalogue cards, related
  instruments, and separated source/reference links.
- Grouped single-instrument metadata into responsive, keyboard-accessible tabs
  for quick facts, spectral and imaging characteristics, data access, external
  catalogues, and references.
- Added generated VitePress schema and contributing pages.

### Project Infrastructure

- Added `pyproject.toml`.
- Added `.gitignore` entries for Python, packaging, test, and VitePress
  artefacts.
- Added pytest validation for catalogue generation.
- Added GitHub Actions-oriented generation and validation workflow support.

## 0.1.0

### Initial Catalogue

- Added the initial instrument catalogue with the current instrument set:
  EMIT, ETM_L7, MSI_S2A, MSI_S2B, MSI_S2C, MSS_L1, MSS_L2, MSS_L3, MSS_L4,
  MSS_L5, OLI2_L9, OLI_L8, TIRS2_L9, TIRS_L8, TM_L4, and TM_L5.

### Initial Schema

- Added the original core schema.
- Added the original spectral extension.
- Added the original imaging extension.
- Added the original provider-specific data access extensions for Google Earth
  Engine and Microsoft Planetary Computer.

This release did not include the later `cross_links` extension or the current
consolidated `data_access` extension.
