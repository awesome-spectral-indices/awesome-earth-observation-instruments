---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "RedEdge-P"
  text: "RedEdge-P"
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
  <code class="instrument-identity-value">REDEDGEP_MICASENSE</code>
</div>

## Summary

<InstrumentSection instrument-id="REDEDGEP_MICASENSE" section="summary" />

> [!NOTE]
> Imaging extension values describe the multispectral imagers. The panchromatic imager has a 44.5 degree HFOV, 37.7 degree VFOV, and 10.0 mm focal length. Band GSD values are specified at 120 m above ground level.

<InstrumentTabs instrument-id="REDEDGEP_MICASENSE" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.REDEDGEP_MICASENSE

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
