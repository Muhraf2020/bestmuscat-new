#!/usr/bin/env python3
"""
generate_about.py

Stub for generating an 'about' paragraph for each place using AI.

The script should read the latest enriched JSONL (e.g. badges_resolved.jsonl),
call a language model to generate a concise, factual description of each place,
store the results in the "about" field, and write to scripts/tmp/about_generated.jsonl.

The OPENAI_API_KEY environment variable must be set when implementing this script.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/badges_resolved.jsonl"
    output_path = "scripts/tmp/about_generated.jsonl"
    if not os.path.exists(input_path):
        print(f"No badges-resolved input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            # Simply copy input to output in this stub.
            fout.write(line)
    print(f"Copied badges-resolved records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()