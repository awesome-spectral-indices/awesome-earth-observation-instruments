---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "MODIS"
  text: "Moderate Resolution Imaging Spectroradiometer"
  tagline: "Terra"
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
  <code class="instrument-identity-value">MODIS_TERRA</code>
</div>

## Summary

<InstrumentSection instrument-id="MODIS_TERRA" section="summary" />

<InstrumentTabs instrument-id="MODIS_TERRA" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.MODIS_TERRA

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
