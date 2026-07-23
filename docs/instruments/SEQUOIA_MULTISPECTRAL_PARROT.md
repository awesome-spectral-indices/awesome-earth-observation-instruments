---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "Sequoia"
  text: "Sequoia Multispectral Sensor"
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
  <code class="instrument-identity-value">SEQUOIA_MULTISPECTRAL_PARROT</code>
</div>

## Summary

<InstrumentSection instrument-id="SEQUOIA_MULTISPECTRAL_PARROT" section="summary" />

> [!NOTE]
> This record describes Sequoia's four synchronized 1.2 MP monochrome multispectral cameras; the integrated 16 MP RGB camera is represented by SEQUOIA_RGB_PARROT. Band GSD values are specified at 120 m above ground level. The sunshine sensor measures incident light to support radiometric calibration.

<InstrumentTabs instrument-id="SEQUOIA_MULTISPECTRAL_PARROT" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.SEQUOIA_MULTISPECTRAL_PARROT

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
