---
pageClass: multispectral-class
isHome: true

layout: home

hero:
  name: "ASTER"
  text: "Advanced Spaceborne Thermal Emission and Reflection Radiometer"
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
  <code class="instrument-identity-value">ASTER</code>
</div>

## Summary

<InstrumentSection instrument-id="ASTER" section="summary" />

> [!NOTE]
> ASTER includes separate VNIR, SWIR, and TIR subsystems. B3N is nadir-looking and B3B is backward-looking for along-track stereoscopic observations. The SWIR subsystem is unavailable. The TIR subsystem was permanently turned off on 2026-01-16 because of Terra power limitations. VNIR operations resumed on 2026-02-09 and remain active, which is reflected by the operational status.

<InstrumentTabs instrument-id="ASTER" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.ASTER

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
