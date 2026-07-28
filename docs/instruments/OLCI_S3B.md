---
pageClass: instrument-page multispectral-class
instrumentId: "OLCI_S3B"
isHome: true

layout: home

hero:
  name: "OLCI"
  text: "Ocean and Land Colour Instrument"
  tagline: "Sentinel-3B"
  image:
    src: /satellite.jpg
    alt: satellite platform
  actions:
    - theme: alt
      text: 🡰 Back to Instrument Index
      link: /instruments/

---

## Summary

<InstrumentSection instrument-id="OLCI_S3B" section="summary" />

> [!NOTE]
> The nominal band definitions are shared by OLCI-A and OLCI-B. The supplied spectral response functions are representative mean responses derived from preflight spectral characterization. Spectral characteristics vary across CCD columns and can evolve during the mission; orbit-dependent spectral characterization LUTs should be used when that variability matters.

<InstrumentTabs instrument-id="OLCI_S3B" />

## Explore it with `xeo`

```python
import xeo

instrument = xeo.instruments.OLCI_S3B

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
