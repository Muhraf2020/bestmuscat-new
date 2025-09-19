#!/usr/bin/env python3
"""
badges_resolver.py

Stub for assigning badges (e.g. Gem, Best 100, MICHELIN stars) to places
based on editorial lists or provider metadata.

Reads scripts/tmp/price_mapped.jsonl and writes scripts/tmp/badges_resolved.jsonl.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/price_mapped.jsonl"
    output_path = "scripts/tmp/badges_resolved.jsonl"
    if not os.path.exists(input_path):
        print(f"No price-mapped input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Copied price-mapped records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()