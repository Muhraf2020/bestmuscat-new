#!/usr/bin/env python3
"""
build_search_index.py

Generate a client-side search index from places.json.

For example, this script could build a Fuse.js index and write it to
data/search-index.json. This stub simply writes an empty object.
"""
import json
import os


def main() -> None:
    data_path = "data/places.json"
    index_path = "data/search-index.json"
    if not os.path.exists(data_path):
        print(f"No data file found at {data_path}.")
        return
    # TODO: implement actual search index generation.
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({}, f)
    print(f"Wrote empty search index to {index_path}.")


if __name__ == "__main__":
    main()