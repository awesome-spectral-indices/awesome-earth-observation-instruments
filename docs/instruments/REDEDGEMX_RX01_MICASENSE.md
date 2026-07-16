---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "RedEdge-MX"
  text: "RedEdge-MX RX01 Series"
  tagline: "UAV"
  image:
    src: /uav.png
    alt: uav
  actions:
    - theme: alt
      text: 🡰 Back to Instrument Index
      link: /instruments/

---

<div class="instrument-identity" aria-label="Instrument identifier">
  <span class="instrument-identity-label">Instrument ID</span>
  <code class="instrument-identity-value">REDEDGEMX_RX01_MICASENSE</code>
</div>

## Summary

<InstrumentSection instrument-id="REDEDGEMX_RX01_MICASENSE" section="summary" />

> [!NOTE]
> This configuration applies to RedEdge-MX cameras with serial numbers beginning with RX01. Imaging extension values describe the multispectral imagers, with GSD specified at 120 m above ground level. MicaSense identifies RedEdge-MX as no longer in production but does not provide an exact retirement date.

<InstrumentTabs instrument-id="REDEDGEMX_RX01_MICASENSE" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.REDEDGEMX_RX01_MICASENSE

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
