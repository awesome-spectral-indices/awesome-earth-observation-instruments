---
name: New Instrument
about: Suggest a new Earth observation instrument
title: 'NEW INSTRUMENT: short-name (full instrument name)'
labels: NEW INSTRUMENT
assignees: ''
---

<!--
Thank you for contributing to the catalogue.

You do not need to prepare the YAML or CSV files yourself. Providing reliable
source links is enough for maintainers to create the record. Complete only the
sections for which information is available.
-->

## Before submitting

- [ ] I searched the catalogue and existing issues for this instrument.
- [ ] I included links to authoritative sources wherever possible.
- [ ] Any files attached or proposed for redistribution can legally be included in the catalogue.

## How would you like to contribute?

Choose either option:

1. **Provide source links:** Share the available documentation below and the maintainers will create the instrument record.
2. **Prepare the files:** Follow the [catalogue schema documentation](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/SCHEMA.md) and use [`MSI_S2A.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/src/instruments/MSI_S2A.yaml) as a comprehensive example.

## Instrument identity

<!-- Complete what you know. Suggested IDs should use letters, numbers, and underscores. -->

- **Suggested instrument ID:**
- **Full name:**
- **Acronym:**
- **Instrument type:** <!-- multispectral, hyperspectral, RGB, radar, lidar, or other -->
- **Platform type:** <!-- satellite, airborne, UAV, or terrestrial -->
- **Platform name(s):**
- **Operator(s):**
- **Start date:**
- **End date, if applicable:**
- **Status:** <!-- operational/retired for satellite or airborne; active/legacy for UAV or terrestrial; experimental/planned for any platform -->
- **Data availability:** <!-- public or private -->

## Contributor attribution

<!-- GitHub profile URLs of people who should be credited for this record. -->

- **Contributor GitHub profile:**

## Authoritative sources

Please provide direct links to the pages or documents containing the instrument specifications.

Preferred sources include:

- Official mission or manufacturer documentation
- Calibration or technical documentation
- Space-agency instrument pages
- Peer-reviewed publications
- Official data-product documentation

<!-- Add or remove entries as needed. -->

1.
2.
3.

## Instrument notes

<!-- Mention different configurations, serial-number-dependent specifications, platform differences, known limitations, or other important context. -->



## Spectral bands

- [ ] Spectral-band information is available
- [ ] No spectral-band information was found
- [ ] Not applicable to this instrument

**Source link(s):**

1.
2.

If you want to prepare a bands file, use CSV format and name it following one of these patterns:

- Instrument-specific: `<INSTRUMENT_ID>_BANDS.csv`
- Shared between several instruments: `<SHARED_NAME>_BANDS.csv`

The required columns are:

```csv
band,center_wavelength,bandwidth
```

Optional columns are:

```text
band_description,common_name,gsd,snr
```

A complete example is:

```csv
band,center_wavelength,bandwidth,band_description,common_name,gsd,snr
B1,443,20,Coastal aerosol,coastal,30,100
B2,490,65,Blue,blue,30,120
```

Requirements:

- `band` identifiers must be unique.
- `center_wavelength` must be expressed in nanometres.
- `bandwidth` must be expressed in nanometres.
- `gsd`, when provided, must be expressed in metres.
- Required values must be numeric and cannot be empty.
- Band order should follow the official instrument documentation.
- If the same nominal bands apply to several platforms, a shared bands file is preferred.
- For instruments described by continuous spectral coverage, provide the minimum and maximum wavelengths and either the sampling interval or total number of bands.

## Spectral response function

- [ ] An SRF is available
- [ ] No SRF was found
- [ ] Not applicable to this instrument

**Source link(s):**

1.
2.

**Original file format:** <!-- CSV, NetCDF, TXT, XLSX, etc. -->

**Additional context:** <!-- Platform, detector, serial number, measurement method, processing version, etc. -->

If you want to prepare an SRF file, use CSV format and name it:

```text
<INSTRUMENT_ID>_SRF.csv
```

The first column must be `wavelength`, followed by columns whose names exactly match the band identifiers and order in the bands file:

```csv
wavelength,B1,B2,B3
400,0.001,,
401,0.003,,
402,0.008,0.001,
```

Requirements:

- Wavelengths must be expressed in nanometres.
- Response values must be numeric.
- Preserve the original wavelength sampling whenever possible.
- Do not interpolate, resample, smooth, or normalize the original data.
- Use an empty cell when no response value exists at a wavelength.
- Do not write the literal value `NaN`.
- A measured response of zero must be written as `0`, not left empty.
- Platform-specific or configuration-specific SRFs must use separate files.
- Please provide the original source file or a stable download link whenever possible.

If redistribution rights are unclear, provide only the source link and the maintainers will assess whether the file can be included.

## Imaging characteristics

- [ ] Imaging information is available
- [ ] No imaging information was found
- [ ] Not applicable

Provide any available values and their sources:

- **Ground sampling distance:**
- **Swath width:**
- **Horizontal field of view:**
- **Vertical field of view:**
- **Across-track field of view:**
- **Along-track field of view:**
- **Instantaneous field of view:**
- **Focal length:**
- **Entrance pupil:**
- **F-number:**

**Source link(s):**

1.
2.

<!-- State the altitude when reporting altitude-dependent UAV or airborne GSD values. -->

## Data access

- [ ] Data are available through Google Earth Engine
- [ ] Data are available through Microsoft Planetary Computer
- [ ] Data are available through the Copernicus Data Space Ecosystem
- [ ] Data are available through EOPF Sentinel Zarr Samples
- [ ] Data are available elsewhere
- [ ] No public data access is available

For each applicable provider, include the documentation URL and collection identifier.

### Google Earth Engine

- **Documentation URL:**
- **Collection ID:**
- **Processing level or product type:**

### Microsoft Planetary Computer

- **Documentation URL:**
- **STAC collection:**
- **Processing level or product type:**

### Copernicus Data Space Ecosystem

- **Documentation URL:**
- **STAC collection:**
- **Processing level or product type:**

### EOPF Sentinel Zarr Samples

- **Documentation URL:**
- **STAC collection:**
- **Processing level or product type:**

### Other access points

- **Provider:**
- **URL:**
- **Collection or product identifier:**

## External catalogue links

<!-- These fields are optional. -->

- **CEOS EO Handbook:**
- **NASA Earthdata instrument catalogue:**
- **Index DataBase:**

## Proposed files

<!-- Attach files to the issue or provide links. Remove rows that are not applicable. -->

| File | Attached or linked? | Source |
|---|---|---|
| Instrument YAML |  |  |
| Bands CSV |  |  |
| SRF CSV |  |  |
| Original SRF or calibration file |  |  |

## Additional information

<!-- Add anything else that may help create or validate the record. -->

