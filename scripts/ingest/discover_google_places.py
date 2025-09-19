#!/usr/bin/env python3
"""
discover_google_places.py

Stub for discovering places via the Google Places API.

This script should query the Google Places Text Search or Nearby Search
endpoints for a given category around a lat/lng coordinate and write the
raw results to a JSONL file under scripts/tmp/discovered_raw.jsonl.

Usage:
    python discover_google_places.py --category restaurants --lat 23.5859 --lng 58.4059 --radius 35000

The script requires a valid Google Maps API key in the environment variable
GOOGLE_MAPS_API_KEY.
"""
import argparse
import json
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover places via Google Places API")
    parser.add_argument("--category", required=True, help="Type of place to discover (e.g. restaurants, schools)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude of search center")
    parser.add_argument("--lng", type=float, required=True, help="Longitude of search center")
    parser.add_argument("--radius", type=int, default=10000, help="Search radius in meters")
    parser.add_argument("--output", default="scripts/tmp/discovered_raw.jsonl", help="Output JSONL file")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("Missing GOOGLE_MAPS_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    # TODO: implement API calls. For now, just write an empty file.
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("")
    print(f"Wrote {args.output}. This is a stub.")


if __name__ == "__main__":
    main()