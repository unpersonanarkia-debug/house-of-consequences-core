import json
from jsonschema import validate, ValidationError
from pathlib import Path


SCHEMA_PATH = Path("schemas/evidence.pack.schema.json")


def validate_evidence_pack(data: dict) -> None:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validate(instance=data, schema=schema)
