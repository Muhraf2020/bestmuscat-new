#!/usr/bin/env python3
"""
discover_osm.py

Stub for discovering places via the OpenStreetMap Overpass API.

This script should query OSM data for relevant tags and write the raw
results to scripts/tmp/discovered_raw.jsonl.

Usage:
    python discover_osm.py --category restaurants --bbox 23.4,58.3,23.8,58.7
"""
import argparse
import os


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover places via OpenStreetMap Overpass API")
    parser.add_argument("--category", required=True, help="Type of place to discover")
    parser.add_argument("--bbox", required=True, help="Bounding box south,west,north,east")
    parser.add_argument("--output", default="scripts/tmp/discovered_raw.jsonl", help="Output JSONL file")
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    # TODO: implement OSM queries
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("")
    print(f"Wrote {args.output}. This is a stub.")


if __name__ == "__main__":
    main()