#!/usr/bin/env python3
"""
hours_parser.py

Stub for parsing opening hours strings into structured arrays.

Reads scripts/tmp/cuisine_mapped.jsonl and writes scripts/tmp/hours_parsed.jsonl.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/cuisine_mapped.jsonl"
    output_path = "scripts/tmp/hours_parsed.jsonl"
    if not os.path.exists(input_path):
        print(f"No cuisine-mapped input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Copied cuisine-mapped records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()