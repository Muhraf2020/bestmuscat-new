#!/usr/bin/env python3
"""
cuisine_mapper.py

Stub for normalising cuisine strings to a controlled vocabulary defined in
data/categories.json or other controlled lists.

Reads scripts/tmp/geocoded.jsonl and writes scripts/tmp/cuisine_mapped.jsonl.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/geocoded.jsonl"
    output_path = "scripts/tmp/cuisine_mapped.jsonl"
    if not os.path.exists(input_path):
        print(f"No geocoded input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Copied geocoded records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()