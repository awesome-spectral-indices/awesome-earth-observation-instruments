from pathlib import Path
import json
import yaml
import datetime

import pandas as pd

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

def _get_base_path():
    return Path("schema").resolve()

def _load_yaml(path: Path):
    with open(path) as f:
        return yaml.safe_load(f)

def _normalize_dates(obj):
    """Recursively convert datetime.date to ISO strings."""
    if isinstance(obj, dict):
        return {k: _normalize_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_normalize_dates(i) for i in obj]
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    return obj

class ValidationError(Exception):
    """Custom validation error with clean messages."""
    pass

def validate_schema(instrument: str):

    # Get base path
    base = _get_base_path()    

    # Every schema and extension goes into the registry
    registry = Registry()
    
    # Load core schema
    core_path = base / "core/core.yaml"
    core_schema = _load_yaml(core_path)
    registry = registry.with_resource(
        core_path.as_uri(),
        Resource.from_contents(core_schema),
    )
    
    # Load extensions
    for rel in [
        "extensions/spectral.yaml",
        "extensions/imaging.yaml",
        "extensions/earth-engine.yaml",
        "extensions/planetary-computer.yaml",
    ]:
        path = base / rel
        registry = registry.with_resource(
            path.as_uri(),
            Resource.from_contents(_load_yaml(path)),
        )

    # Create validator with the registry
    validator = Draft202012Validator(core_schema, registry=registry)

    # Open the instrument data
    data = _load_yaml(Path(instrument))
    data = _normalize_dates(data)

    # Get the errors
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    # If there are errors raise them
    if errors:
        messages = [
            f"{'.'.join(map(str, e.path))}: {e.message}"
            for e in errors
        ]
        raise ValidationError(
            "Schema validation failed:\n" + "\n".join(messages)
        )

    return data