#!/usr/bin/env python3
"""
hydrate_details.py

Stub for hydrating merged records with additional details such as
photos, hours, and contact information.

Reads scripts/tmp/merged.jsonl and writes hydrated data to
scripts/tmp/hydrated.jsonl.

TODO: implement actual API calls to fetch details and download photos.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/merged.jsonl"
    output_path = "scripts/tmp/hydrated.jsonl"
    if not os.path.exists(input_path):
        print(f"No merged input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Copied merged records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()