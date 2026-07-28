---
pageClass: instrument-page multispectral-class
instrumentId: "REDEDGEM_MICASENSE"
isHome: true

layout: home

hero:
  name: "RedEdge-M"
  text: "RedEdge-M"
  tagline: "UAV"
  image:
    src: /uav.jpg
    alt: uav platform
  actions:
    - theme: alt
      text: 🡰 Back to Instrument Index
      link: /instruments/

---

## Summary

<InstrumentSection instrument-id="REDEDGEM_MICASENSE" section="summary" />

> [!NOTE]
> Imaging extension values describe the multispectral imagers, with GSD specified at 120 m above ground level. MicaSense identifies RedEdge-M as a legacy product that is no longer supported but does not provide an exact retirement date.

<InstrumentTabs instrument-id="REDEDGEM_MICASENSE" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.REDEDGEM_MICASENSE

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
