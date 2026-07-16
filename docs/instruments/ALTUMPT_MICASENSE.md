---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "Altum-PT"
  text: "Altum-PT"
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
  <code class="instrument-identity-value">ALTUMPT_MICASENSE</code>
</div>

## Summary

<InstrumentSection instrument-id="ALTUMPT_MICASENSE" section="summary" />

> [!NOTE]
> Imaging extension values describe the multispectral imagers. The panchromatic imager has a 46 degree HFOV, 35 degree VFOV, and 16.3 mm focal length, while the thermal imager has a 48 degree HFOV, 39 degree VFOV, and 4.5 mm focal length. Band GSD values are specified at 120 m above ground level.

<InstrumentTabs instrument-id="ALTUMPT_MICASENSE" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.ALTUMPT_MICASENSE

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
