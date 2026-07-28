---
pageClass: instrument-page multispectral-class
instrumentId: "SLSTR_S3A"
isHome: true

layout: home

hero:
  name: "SLSTR"
  text: "Sea and Land Surface Temperature Radiometer"
  tagline: "Sentinel-3A"
  image:
    src: /satellite.jpg
    alt: satellite platform
  actions:
    - theme: alt
      text: 🡰 Back to Instrument Index
      link: /instruments/

---

## Summary

<InstrumentSection instrument-id="SLSTR_S3A" section="summary" />

> [!NOTE]
> SLSTR uses nadir and oblique views to improve atmospheric correction and surface-temperature retrievals. The recorded 1470 km swath is the nominal nadir-view coverage; the oblique view covers approximately 768 km. F1 and F2 share the spectral responses of S7 and S8, respectively, but use an extended dynamic range for active-fire observations. The nominal band definitions are shared by SLSTR-A and SLSTR-B, while their SRFs come from separate pre-flight calibration measurements.

<InstrumentTabs instrument-id="SLSTR_S3A" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.SLSTR_S3A

# Extract metadata
metadata = {
    "id": instrument.id,
    "name": instrument.name,
    "acronym": instrument.acronym,
    "type": instrument.type,
    "platform_type": instrument.platform_type,
    "platform": instrument.platform,
    "operator": instrument.operator,
    "start_date": instrument.start_date,
    "end_date": instrument.end_date,
    "status": instrument.status,
    "availability": instrument.availability,
}

# Get the bands as a pandas DataFrame (returns None if it is not available)
instrument.bands()

# Get the Spectral Response Function as a pandas DataFrame (returns None if it is not available)
instrument.srf()

# Check the available extensions
print(instrument.extension_names)
for name, extension in instrument.extensions.items():
    print(name, "->", list(extension))
```
