---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "Altum"
  text: "Altum AL05 Series"
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
  <code class="instrument-identity-value">ALTUMAL05_MICASENSE</code>
</div>

## Summary

<InstrumentSection instrument-id="ALTUMAL05_MICASENSE" section="summary" />

> [!NOTE]
> This configuration applies to Altum cameras with serial numbers beginning with AL05. The start date uses the guide revision that documented the updated spectral configuration because its exact production date is not specified. Imaging extension values describe the multispectral imagers, with GSD specified at 120 m above ground level. The thermal imager has a 57 degree HFOV, 44.3 degree VFOV, 1.77 mm focal length, and 0.81 m GSD at 120 m. MicaSense identifies Altum as discontinued but does not provide an exact retirement date.

<InstrumentTabs instrument-id="ALTUMAL05_MICASENSE" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.ALTUMAL05_MICASENSE

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
