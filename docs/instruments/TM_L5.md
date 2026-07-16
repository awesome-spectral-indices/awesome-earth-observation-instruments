---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "TM"
  text: "Thematic Mapper"
  tagline: "Landsat 5"
  image:
    src: /satellite.png
    alt: satellite
  actions:
    - theme: alt
      text: 🡰 Back to Instrument Index
      link: /instruments/

---

<div class="instrument-identity" aria-label="Instrument identifier">
  <span class="instrument-identity-label">Instrument ID</span>
  <code class="instrument-identity-value">TM_L5</code>
</div>

## Summary

<InstrumentSection instrument-id="TM_L5" section="summary" />

<InstrumentTabs instrument-id="TM_L5" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.TM_L5

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
