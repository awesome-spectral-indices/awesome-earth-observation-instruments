<p align="center">
  <a href="https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments"><img src="docs/cover-picture.png" alt="Awesome Earth Observation Instruments"></a>
</p>
<p align="center">
    <em>A machine-readable catalogue of Earth observation instruments with spectral, spatial, temporal, and operational characteristics</em>
</p>
<p align="center">
<a href="https://github.com/sindresorhus/awesome" target="_blank">
    <img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg" alt="Awesome">
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

**Python Package**: <a href="https://github.com/awesome-spectral-indices/earth-observation" target="_blank">https://github.com/awesome-spectral-indices/earth-observation</a>

---

## Core Schema ([`schema/core/core.yaml`](schema/core/core.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| **id** | **Yes** | string | Alphanumerical identifier of the instrument |
| **name** | **Yes** | string | Full name of the instrument |
| **acronym** | **Yes** | string | Instrument acronym |
| **type** | **Yes** | string | Instrument sensing modality category |
| **platform_type** | **Yes** | string | Platform class carrying the instrument |
| **platform** | **Yes** | array | Satellite name, UAV model, aircraft, or terrestrial platform |
| **operator** | **Yes** | array | Organization operating the instrument |
| **start_date** | **Yes** | string | Start of operation (YYYY-MM-DD) |
| **status** | **Yes** | string | Operational lifecycle state of the instrument |
| **availability** | **Yes** | string | Data accessibility level |
| end_date | No | string | End of operation (YYYY-MM-DD) |
| notes | No | string | Free-form additional notes |
| **references** | **Yes** | array | URLs of references (papers, web pages, etc.) |
| data_links | No | array | URLs where instrument data products can be accessed |
| extensions | No | object | Optional extension blocks with domain-specific properties |

## Spectral Extension ([`schema/extensions/spectral.yaml`](schema/extensions/spectral.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| bands | No | oneOf | Band definitions provided inline or via a CSV file |
| range | No | object | Continuous spectral coverage metadata for instruments without explicit bands |
| spectral_response_function | No | string | Filename of the spectral response function (SRF) CSV file (with extension) |

## Imaging Extension ([`schema/extensions/imaging.yaml`](schema/extensions/imaging.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| swath_width | No | number | Swath width (km) |
| across_fov | No | number | Across-track Field of View (FOV) (degrees). Relevant for satellite platforms |
| along_fov | No | number | Along-track Field of View (FOV) (degrees). Relevant for satellite platforms |
| across_ifov | No | number | Across-track Instantaneous Field of View (IFOV) (microradians). Relevant for satellite platforms |
| along_ifov | No | number | Along-track Instantaneous Field of View (IFOV) (microradians). Relevant for satellite platforms |
| hfov | No | number | Horizontal Field of View (HFOV) (degrees). Relevant for UAV or similar platforms |
| vfov | No | number | Vertical Field of View (VFOV) (degrees). Relevant for UAV or similar platforms |
| entrance_pupil | No | number | Diameter of the entrance pupil (mm) |
| focal_length | No | number | Focal length (mm) |
| fnumber | No | number | F-number |
| gsd | No | number | Ground Sampling Distance (m). If GSD varies by band, define per-band values in the spectral bands data |

## Earth Engine Extension ([`schema/extensions/earth-engine.yaml`](schema/extensions/earth-engine.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| **primary** | **Yes** | object | Primary Earth Engine dataset metadata for this instrument |
| raw | No | object | Optional Earth Engine metadata for raw (unprocessed) products |
| boa | No | object | Optional Earth Engine metadata for bottom-of-atmosphere (BOA) products |
| toa | No | object | Optional Earth Engine metadata for top-of-atmosphere (TOA) products |

## Planetary Computer Extension ([`schema/extensions/planetary-computer.yaml`](schema/extensions/planetary-computer.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| **stac_endpoint** | **Yes** | string | Planetary Computer STAC API endpoint |
| **primary** | **Yes** | object | Primary Planetary Computer dataset metadata for this instrument |
| raw | No | object | Optional Planetary Computer metadata for raw (unprocessed) products |
| boa | No | object | Optional Planetary Computer metadata for bottom-of-atmosphere (BOA) products |
| toa | No | object | Optional Planetary Computer metadata for top-of-atmosphere (TOA) products |

## Satellite Instruments

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

### Hyperspectral

| Id | Name | Platforms | Status | Earth Engine | Planetary Computer |
| --- | --- | --- | --- | --- | --- |
| [EMIT](https://earth.jpl.nasa.gov/emit/) | Earth Surface Mineral Dust Source Investigation | ISS | **operational :white_check_mark:** | [:link: link](https://developers.google.com/earth-engine/datasets/catalog/NASA_EMIT_L2A_RFL) |  |

---
Generated from source files in `src/instruments/` via `src/code/catalogue.py` and `src/code/readme.py`.
