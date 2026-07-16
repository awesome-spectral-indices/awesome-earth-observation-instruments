---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "RedEdge-MX"
  text: "RedEdge-MX RX02 (or greater) Series"
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
  <code class="instrument-identity-value">REDEDGEMX_RX02_gte_MICASENSE</code>
</div>

## Summary

<InstrumentSection instrument-id="REDEDGEMX_RX02_gte_MICASENSE" section="summary" />

> [!NOTE]
> This configuration applies to RedEdge-MX cameras with serial numbers beginning with RX02 or higher. The start date uses the month of the guide revision that documented this spectral configuration because its exact production date is not specified. Imaging extension values describe the multispectral imagers, with GSD specified at 120 m above ground level. MicaSense identifies RedEdge-MX as no longer in production but does not provide an exact retirement date.

<InstrumentTabs instrument-id="REDEDGEMX_RX02_gte_MICASENSE" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.REDEDGEMX_RX02_gte_MICASENSE

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
