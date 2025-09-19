#!/usr/bin/env python3
"""
generate_faqs.py

Stub for generating frequently asked questions and answers for each place.

This script should use a language model to create 3–6 realistic questions and
answers based on the category and known attributes of a place.

Reads scripts/tmp/about_generated.jsonl and writes scripts/tmp/faqs_generated.jsonl.
"""
def main() -> None:
    import os
    input_path = "scripts/tmp/about_generated.jsonl"
    output_path = "scripts/tmp/faqs_generated.jsonl"
    if not os.path.exists(input_path):
        print(f"No about-generated input found at {input_path}.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)
    print(f"Copied about-generated records to {output_path}. This is a stub.")


if __name__ == "__main__":
    main()