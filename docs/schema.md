# Schema Specification

The tables below summarize the properties defined by the core schema and its extensions.

## Core Schema ([`schema/core/core.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/core/core.yaml))

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
| **status** | **Yes** | string | Instrument lifecycle state, using mission terms for satellite and airborne instruments and product terms for UAV and terrestrial instruments |
| **availability** | **Yes** | string | Data accessibility level |
| end_date | No | string | End of operation (YYYY-MM-DD) |
| notes | No | string | Free-form additional notes |
| **references** | **Yes** | array | URLs of references (papers, web pages, etc.) |
| data_links | No | array | URLs where instrument data products can be accessed |
| extensions | No | object | Optional extension blocks with domain-specific properties |

## Spectral Extension ([`schema/extensions/spectral.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/spectral.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| bands | No | oneOf | Band definitions provided inline or via a CSV file |
| range | No | object | Continuous spectral coverage metadata for instruments without explicit bands |
| spectral_response_function | No | string | Filename of the spectral response function (SRF) CSV file (with extension) |

## Imaging Extension ([`schema/extensions/imaging.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/imaging.yaml))

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

## Data Access Extension ([`schema/extensions/data-access.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/data-access.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| ee | No | ref: data_access_points/earth-engine.yaml | Google Earth Engine access metadata |
| planetary_computer | No | ref: data_access_points/planetary-computer.yaml | Microsoft Planetary Computer access metadata |
| cdse | No | ref: data_access_points/copernicus-data-space-ecosystem.yaml | Copernicus Data Space Ecosystem access metadata |
| eopf | No | ref: data_access_points/eopf-sentinel-zarr-samples.yaml | EOPF Sentinel Zarr Samples access metadata |

## Cross Links Extension ([`schema/extensions/cross-links.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/cross-links.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| idb | No | string | URL of the instrument in the Index DataBase (IDB) |
| ceos | No | string | URL of the instrument in the CEOS EO Handbook Instrument Index |
| earthdata | No | string | URL of the instrument in the Earthdata catalogue of instruments |

## Earth Engine Access Point ([`schema/extensions/data_access_points/earth-engine.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/data_access_points/earth-engine.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| **primary** | **Yes** | object | Primary Earth Engine dataset metadata for this instrument |
| raw | No | object | Optional Earth Engine metadata for raw (unprocessed) products |
| boa | No | object | Optional Earth Engine metadata for bottom-of-atmosphere (BOA) products |
| toa | No | object | Optional Earth Engine metadata for top-of-atmosphere (TOA) products |

## Planetary Computer Access Point ([`schema/extensions/data_access_points/planetary-computer.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/data_access_points/planetary-computer.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| **stac_endpoint** | **Yes** | string | Planetary Computer STAC API endpoint |
| **primary** | **Yes** | object | Primary Planetary Computer dataset metadata for this instrument |
| raw | No | object | Optional Planetary Computer metadata for raw (unprocessed) products |
| boa | No | object | Optional Planetary Computer metadata for bottom-of-atmosphere (BOA) products |
| toa | No | object | Optional Planetary Computer metadata for top-of-atmosphere (TOA) products |

## Copernicus Data Space Ecosystem Access Point ([`schema/extensions/data_access_points/copernicus-data-space-ecosystem.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/data_access_points/copernicus-data-space-ecosystem.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| **stac_endpoint** | **Yes** | string | Copernicus Data Space Ecosystem STAC API endpoint |
| **primary** | **Yes** | object | Primary Copernicus Data Space Ecosystem dataset metadata for this instrument |
| raw | No | object | Optional Copernicus Data Space Ecosystem metadata for raw (unprocessed) products |
| boa | No | object | Optional Copernicus Data Space Ecosystem metadata for bottom-of-atmosphere (BOA) products |
| toa | No | object | Optional Copernicus Data Space Ecosystem metadata for top-of-atmosphere (TOA) products |

## EOPF Sentinel Zarr Samples Access Point ([`schema/extensions/data_access_points/eopf-sentinel-zarr-samples.yaml`](https://github.com/awesome-spectral-indices/awesome-earth-observation-instruments/blob/main/schema/extensions/data_access_points/eopf-sentinel-zarr-samples.yaml))

| Property | Required | Type | Description |
| --- | --- | --- | --- |
| **stac_endpoint** | **Yes** | string | EOPF Sentinel Zarr Samples STAC API endpoint |
| **primary** | **Yes** | object | Primary EOPF Sentinel Zarr Samples dataset metadata for this instrument |
| raw | No | object | Optional EOPF Sentinel Zarr Samples metadata for raw (unprocessed) products |
| boa | No | object | Optional EOPF Sentinel Zarr Samples metadata for bottom-of-atmosphere (BOA) products |
| toa | No | object | Optional EOPF Sentinel Zarr Samples metadata for top-of-atmosphere (TOA) products |
