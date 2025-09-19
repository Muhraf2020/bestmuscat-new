#!/usr/bin/env python3
"""
validate_schema.py

Validate the final places.json file against the JSON schema defined in scripts/utils/schema_place.json.

Usage:
    python validate_schema.py
"""
import json
import os
import sys
from jsonschema import Draft202012Validator


def main() -> None:
    schema_path = "scripts/utils/schema_place.json"
    data_path = "data/places.json"
    if not os.path.exists(schema_path):
        print(f"Schema file {schema_path} not found.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(data_path):
        print(f"Data file {data_path} not found.", file=sys.stderr)
        sys.exit(1)
    schema = json.load(open(schema_path, "r", encoding="utf-8"))
    data = json.load(open(data_path, "r", encoding="utf-8"))
    errors = []
    validator = Draft202012Validator(schema)
    for place in data:
        for error in validator.iter_errors(place):
            errors.append(f"[{place.get('slug')}] {error.message}")
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    print("Schema validation passed.")


if __name__ == "__main__":
    main()