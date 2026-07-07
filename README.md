<p align="center">
  <a href="https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments"><img src="readme/cover-picture.png" alt="Awesome Earth Observation Instruments"></a>
</p>
<p align="center">
    <em>A machine-readable catalogue of Earth observation instruments with spectral, spatial, temporal, and operational characteristics</em>
</p>
<p align="center">
<a href="https://github.com/sindresorhus/awesome" target="_blank">
    <img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg" alt="Awesome">
</a>
<a href="https://arxiv.org/abs/2606.13923" target="_blank">
    <img src="https://img.shields.io/badge/arXiv-2606.13923-b31b1b.svg" alt="arXiv">
</a>
<a href="https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/actions/workflows/tests.yml/badge.svg" alt="Tests">
</a>
<a href="https://github.com/sponsors/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/GitHub%20Sponsors-Donate-ff69b4.svg" alt="GitHub Sponsors">
</a>
<a href="https://www.buymeacoffee.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/Buy%20me%20a%20coffee-Donate-ff69b4.svg" alt="Buy me a coffee">
</a>
<a href="https://ko-fi.com/davemlz" target="_blank">
    <img src="https://img.shields.io/badge/kofi-Donate-ff69b4.svg" alt="Ko-fi">
</a>
<a href="https://twitter.com/dmlmont" target="_blank">
    <img src="https://img.shields.io/twitter/follow/dmlmont?style=social" alt="Twitter">
</a>
</p>

---

**GitHub**: <a href="https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments" target="_blank">https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments</a>

---

# Earth Observation

Earth observation (EO) instruments measure our planet from satellites, aircraft, drones, and ground systems.
They capture information about land, oceans, atmosphere, ice, and human activity, helping both experts and the public understand environmental change.

This catalogue organizes EO instrument metadata in a consistent, machine-readable format.
The goal is to make comparison, discovery, and downstream use easier for research, operations, and education.

# Schema

The core schema defines the common metadata required for every instrument, such as identifier, platform, status, operators, and reference links.
Using a single core structure improves interoperability across missions, agencies, and processing systems.

In practical terms, the core schema makes data exchange more reliable:
- developers can validate files automatically,
- analysts can query instrument metadata consistently,
- users can trace information back to references and data access links.

Additionally, we added some extensions to the core schema. They add domain-specific details without changing the core model:
- `spectral` for band and wavelength information,
- `imaging` for optical and geometric parameters,
- `data_access` for data access metadata, with access points such as Google Earth Engine and Microsoft Planetary Computer.
- `cross_links` for links to matching instrument records in external catalogues and indexes.

This modular design keeps the catalogue flexible.
Simple instruments can use only the core fields, while advanced instruments can provide richer spectral and platform access details.

See the [schema specification](SCHEMA.md) for the complete list of core and extension properties.

# Catalogue

This section organizes instruments by platform type and sensing modality to make discovery and comparison easier.
Use the table of contents below to jump directly to available categories and subcategories.

## Table of Contents
- [Satellite Instruments](#catalogue-satellite-instruments)
  - [Multispectral](#catalogue-satellite-multispectral)
  - [Hyperspectral](#catalogue-satellite-hyperspectral)

<a id="catalogue-satellite-instruments"></a>

## Satellite Instruments

<a id="catalogue-satellite-multispectral"></a>

### Multispectral

| Id | Name | Platforms | Status | Earth Engine | Planetary Computer |
| --- | --- | --- | --- | --- | --- |
| [ETM_L7](https://science.nasa.gov/mission/landsat/etm-plus/) | Enhanced Thematic Mapper Plus | Landsat 7 | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2) |
| [MSI_S2A](https://sentiwiki.copernicus.eu/web/s2-mission#S2-Mission-MSI-Instrument) | MultiSpectral Instrument | Sentinel-2A | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED) | [:link: link](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a) |
| [MSI_S2B](https://sentiwiki.copernicus.eu/web/s2-mission#S2-Mission-MSI-Instrument) | MultiSpectral Instrument | Sentinel-2B | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED) | [:link: link](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a) |
| [MSI_S2C](https://sentiwiki.copernicus.eu/web/s2-mission#S2-Mission-MSI-Instrument) | MultiSpectral Instrument | Sentinel-2C | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED) | [:link: link](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a) |
| [MSS_L1](https://science.nasa.gov/mission/landsat/mss/) | Multispectral Scanner System | Landsat 1 | **retired :no_entry:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LM01_C02_T1) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l1) |
| [MSS_L2](https://science.nasa.gov/mission/landsat/mss/) | Multispectral Scanner System | Landsat 2 | **retired :no_entry:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LM02_C02_T1) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l1) |
| [MSS_L3](https://science.nasa.gov/mission/landsat/mss/) | Multispectral Scanner System | Landsat 3 | **retired :no_entry:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LM03_C02_T1) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l1) |
| [MSS_L4](https://science.nasa.gov/mission/landsat/mss/) | Multispectral Scanner System | Landsat 4 | **retired :no_entry:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LM04_C02_T1) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l1) |
| [MSS_L5](https://science.nasa.gov/mission/landsat/mss/) | Multispectral Scanner System | Landsat 5 | **retired :no_entry:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LM05_C02_T1) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l1) |
| [OLI2_L9](https://science.nasa.gov/mission/landsat/oli/) | Operational Land Imager 2 | Landsat 9 | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2) |
| [OLI_L8](https://science.nasa.gov/mission/landsat/oli/) | Operational Land Imager | Landsat 8 | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2) |
| [TIRS2_L9](https://science.nasa.gov/mission/landsat/tirs/) | Thermal Infrared Sensor 2 | Landsat 9 | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2) |
| [TIRS_L8](https://science.nasa.gov/mission/landsat/tirs/) | Thermal Infrared Sensor | Landsat 8 | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2) |
| [TM_L4](https://science.nasa.gov/mission/landsat/tm/) | Thematic Mapper | Landsat 4 | **retired :no_entry:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT04_C02_T1_L2) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2) |
| [TM_L5](https://science.nasa.gov/mission/landsat/tm/) | Thematic Mapper | Landsat 5 | **retired :no_entry:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2) | [:link: link](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2) |

<a id="catalogue-satellite-hyperspectral"></a>

### Hyperspectral

| Id | Name | Platforms | Status | Earth Engine | Planetary Computer |
| --- | --- | --- | --- | --- | --- |
| [EMIT](https://earth.jpl.nasa.gov/emit/) | Earth Surface Mineral Dust Source Investigation | ISS | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/NASA_EMIT_L2A_RFL) |  |

---

> [!WARNING]  
> This README.md is generated automatically from source files in `src/instruments/` via `src/code/catalogue.py` and `src/code/readme.py`. DO NOT MODIFY THIS FILE DIRECTLY.
