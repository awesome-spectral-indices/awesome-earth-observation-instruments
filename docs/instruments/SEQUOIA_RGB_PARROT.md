---
pageClass: rgb-class
isHome: true

layout: home

hero:
  name: "Sequoia"
  text: "Sequoia RGB Camera"
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
  <code class="instrument-identity-value">SEQUOIA_RGB_PARROT</code>
</div>

## Summary

<InstrumentSection instrument-id="SEQUOIA_RGB_PARROT" section="summary" />

> [!NOTE]
> This record describes the 16 MP RGB camera integrated into Sequoia; the four synchronized multispectral cameras are represented by SEQUOIA_MULTISPECTRAL_PARROT. Imaging GSD is specified at 120 m above ground level. Parrot does not publish center wavelengths and bandwidths for the RGB channels, so no spectral bands are declared.

<InstrumentTabs instrument-id="SEQUOIA_RGB_PARROT" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.SEQUOIA_RGB_PARROT

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
