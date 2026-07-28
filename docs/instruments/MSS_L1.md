---
pageClass: instrument-page multispectral-class
instrumentId: "MSS_L1"
isHome: true

layout: home

hero:
  name: "MSS"
  text: "Multispectral Scanner System"
  tagline: "Landsat 1"
  image:
    src: /satellite.jpg
    alt: satellite platform
  actions:
    - theme: alt
      text: 🡰 Back to Instrument Index
      link: /instruments/

---

## Summary

<InstrumentSection instrument-id="MSS_L1" section="summary" />

<InstrumentTabs instrument-id="MSS_L1" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.MSS_L1

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
