#!/usr/bin/env python3
"""
emit_category_feeds.py

Stub for emitting per-category JSON shards of the places dataset.

This can be used to improve page load performance by only downloading the
places for a given category.

Reads data/places.json and writes data/categories/<category>.json.
"""
import json
import os


def main() -> None:
    data_path = "data/places.json"
    output_dir = "data/categories"
    if not os.path.exists(data_path):
        print(f"No data file found at {data_path}.")
        return
    os.makedirs(output_dir, exist_ok=True)
    places = json.load(open(data_path, "r", encoding="utf-8"))
    by_category = {}
    for p in places:
        for cat in p.get("categories", []):
            by_category.setdefault(cat, []).append(p)
    for cat, records in by_category.items():
        out_path = os.path.join(output_dir, f"{cat}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    print(f"Emitted {len(by_category)} category feeds to {output_dir}.")


if __name__ == "__main__":
    main()