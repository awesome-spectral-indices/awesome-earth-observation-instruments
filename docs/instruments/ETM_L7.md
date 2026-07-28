---
pageClass: instrument-page multispectral-class
instrumentId: "ETM_L7"
isHome: true

layout: home

hero:
  name: "ETM+"
  text: "Enhanced Thematic Mapper Plus"
  tagline: "Landsat 7"
  image:
    src: /satellite.jpg
    alt: satellite platform
  actions:
    - theme: alt
      text: 🡰 Back to Instrument Index
      link: /instruments/

---

## Summary

<InstrumentSection instrument-id="ETM_L7" section="summary" />

> [!NOTE]
> The thermal band's NE(Δ)T value is specified for the high-gain acquisition at 280 K. The corresponding low-gain NE(Δ)T is 0.28 K.

<InstrumentTabs instrument-id="ETM_L7" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.ETM_L7

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
