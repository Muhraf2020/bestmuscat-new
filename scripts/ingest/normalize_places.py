#!/usr/bin/env python3
"""
normalize_places.py

Normalize raw discovery records into the canonical place schema.

Reads JSONL from scripts/tmp/discovered_raw.jsonl and writes JSONL to
scripts/tmp/normalized.jsonl.

This script uses the utils.slugify module to generate slugs and utils.provenance
to record provenance information.
"""
import json
import os
import uuid
from scripts.utils.slugify import slugify
from scripts.utils.provenance import make_prov


def main() -> None:
    input_path = "scripts/tmp/discovered_raw.jsonl"
    output_path = "scripts/tmp/normalized.jsonl"
    if not os.path.exists(input_path):
        print(f"No input file found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            rec = json.loads(line)
            slug = slugify(rec.get("name", ""))
            normalized = {
                "id": str(uuid.uuid4()),
                "slug": slug,
                "name": rec.get("name", "").strip(),
                "categories": rec.get("categories", []),
                "location": {
                    "lat": rec.get("lat"),
                    "lng": rec.get("lng"),
                    "address": rec.get("address"),
                    "neighborhood": rec.get("neighborhood"),
                },
                "actions": {
                    "website": rec.get("website"),
                    "phone": rec.get("phone"),
                    "maps_url": rec.get("maps_url")
                },
                "hours": rec.get("hours") or {},
                "provenance": [make_prov("discovery", rec.get("provider", "unknown"), list(rec.keys()))],
                "last_updated": rec.get("collected_at")
            }
            fout.write(json.dumps(normalized) + "\n")
    print(f"Wrote normalized records to {output_path}.")


if __name__ == "__main__":
    main()