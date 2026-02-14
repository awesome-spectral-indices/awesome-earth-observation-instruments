# Info and instructions for AI agents in this repository

This repository contains the source inputs for the creation of an open catalogue of Earth Observation instruments.

## Repo structure

- /schema/: folder with schemas in YAML files. There is a core schema and extensions (subschemas).
- /src/: source inputs: bands, instruments, srf (spectral response functions), and code.
- /catalogue/: folder for the output catalogue in JSON format.
- /docs/: folder with documentation in Markdown.
- /README.md: Readme file of the repo. Read this document for context. DO NOT CHANGE THIS FILE. This readme is created autimatically from /src/code/readme.py

## Schemas

### Core schema

- /schema/core/core.yaml is the core schema of instruments. It contains identifiers and general characteristics for an instrument. Read this and make sure descriptions are clear and formal. Do not change the schema unless specified. Always ask when you need to make changes here.

### Extensions

- /schema/extensions/spectral.yaml is the spectral extension. It contains spectral characteristics for an instrument. Read this for context and make sure descriptions are clear and formal. Do not change the subschema unless specified. Always ask when you need to make changes here.
- /schema/extensions/imaging.yaml is the imaging extension. It contains imaging and optical characteristics of an instrument. Read this for context and make sure descriptions are clear and formal. Do not change the subschema unless specified. Always ask when you need to make changes here. 
- /schema/extensions/earth-engine.yaml is the Earth Engine extension. It contains data access data for Earth Engine for an instrument. Read this for context and make sure descriptions are clear and formal. Do not change the subschema unless specified. Always ask when you need to make changes here.
- /schema/extensions/planetary-computer.yaml is the Planetary Computer extension. It contains data access data for Planetary Computer for an instrument. Read this for context and make sure descriptions are clear and formal. Do not change the subschema unless specified. Always ask when you need to make changes here. 

## Source Inputs

### Instruments

- /src/instruments/ contains the input information for each instrument as a YAML file each. You don't need to read these files as they are validated afterwards.

### Bands

- /src/bands/ contains bands information for each instrument if the "bands" property of the spectral extension is specified as a CSV file instead of an object. You don't need to read these files as they are validated afterwards.

### Spectral Response Functions

- /src/srf/ contains spectral response function information for each instrument if the "spectral_response_function" property of the spectral extension was specified. This property is always specified as a CSV file. You don't need to read these files as they are validated afterwards.

### Code

#### Validators

- /src/code/validators.py contains the code to validate each instrument represented by a YAML file in /src/instruments/. This code must read each file and validate the schema. If this file does not exist or if the validation is not complete, create it or extend it. The validation should be structured as follows:
    
    1. A function for validating the schema.
    2. A function for validating the spectral extension if it exists:
        - If there is a bands property: if the bands property is a CSV file, validate if the file exists in /src/bands/ and it should match the same validation as if it were an object property (read /schema/extensions/spectral.yaml for context, column names should be the same as the properties).
        - If there is a range property: min value should be lower than max value and none of them should be negative.
        - If there is a spectral_response_function property: validate if the CSV file exists in /src/srf/ and the bands (as columns) should be the same bands specified for the bands property, and it should include a column named wavelength.

#### Catalogue Generation

- /src/code/catalogue.py contains the code to generate the catalogue in a JSON format (catalogue.json) from all instruments in /src/instruments/. After validation passing, this code is run for creating the catalogue. The catalogue is an object in the form of a key-value, where the key is the "id" property of each instrument and the value would be the complete object (dictionary) of the instrument. If there are CSV files in the spectral extensions, their information should be transformed into a dictionary form. If the "bands" property of the spectral extension is a CSV file, it should be transformed in a way that matches the object option of that same property. If the "spectral_response_function" property of the spectral extension is passed, it should be transformed into a dictionary where each column name is a key and all the rows of that columns are the value represented as an array. If the "range" property of the spectral extension is passed instead of "bands", an additional "bands" property (in a way that matches the object option of the original "bands" property) in this extension must be created by creating the bands from the "min", "max", and "total_bands" properties of "range": the bands should be named "B1", "B2", ...., "Bn" where n is the number of total bands and center_wavelength and bandwidth should be computed for each band. Note that in spectral_response_function all of the resulting arrays must have the same length. If this file does not exist or if is not complete, create it or extend it.

#### Readme Generation

- /src/code/readme.py contains the code to create a README.md in the root of the repository. If this code does not exist or if it is incomplete, create it or extend it. Follow this structure:
    1. Header: this is the HEADER.md located in /docs/.
    2. A set of tables of instruments by reading the catalogue.json in /catalogue/. There must be 4 categories of tables, each category corresponsing to one of the platform types: satellite, airborne, uav, or terrestrial. Then, within each category there must be a table for each subcategory corresponding to each of the instrument types: multispectral, hyperspectral, radar, lidar, rgb, or other. If a category or subcategory does not exist in the catalogue, then a file for this set is not created. For each table: Each file is an instrument. The columns should be: Id (with a link to the first item in the references property), Name, Platforms (divided by commas), status (bold the text and assign a color according to the status: operational - green, planned - purple, experimental - yellow, retired - red) Earth Engine primary link (if it exists, it should be written as "link" with the markdown emoji :link: with a link to the docs of the primary link, if it doesn't, leave it blank), Planetary Computer primary link (if it exists, it should be written as "link" with the markdown emoji :link: with a link to the docs of the primary link, if it doesn't, leave it blank).
    3. Footer: this is the FOOTER.md located in /docs/.
        
