---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "MSI"
  text: "MultiSpectral Instrument"
  tagline: "Sentinel-2C"
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
  <code class="instrument-identity-value">MSI_S2C</code>
</div>

## Summary

<InstrumentSection instrument-id="MSI_S2C" section="summary" />

<InstrumentTabs instrument-id="MSI_S2C" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.MSI_S2C

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
