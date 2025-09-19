#!/usr/bin/env python3
"""
dedupe_merge.py

Stub for de-duplicating and merging normalized records into a unified dataset.

This script reads normalized JSONL records and writes merged output to
scripts/tmp/merged.jsonl. The merging logic should compare names, addresses and
geographical proximity to collapse duplicates.

TODO: implement fuzzy matching and merging policies.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/normalized.jsonl"
    output_path = "scripts/tmp/merged.jsonl"
    if not os.path.exists(input_path):
        print(f"No normalized input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # For now, just copy the normalized file.
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Copied normalized records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()