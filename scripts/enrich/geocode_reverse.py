#!/usr/bin/env python3
"""
geocode_reverse.py

Stub for adding neighborhood information by reverse geocoding lat/lng
coordinates against a local dataset or external API.

Reads scripts/tmp/hydrated.jsonl and writes scripts/tmp/geocoded.jsonl.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/hydrated.jsonl"
    output_path = "scripts/tmp/geocoded.jsonl"
    if not os.path.exists(input_path):
        print(f"No hydrated input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Copied hydrated records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()