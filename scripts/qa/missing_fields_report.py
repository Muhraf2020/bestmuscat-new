#!/usr/bin/env python3
"""
missing_fields_report.py

Generate a report of missing required fields per category in the places dataset.

This script is intended to help editors see where data is incomplete.
"""
import json
import os


REQUIRED_FIELDS = {
    "Restaurants": ["cuisines", "price_range", "hours"],
    "Hotels": ["price_range", "hours"],
    "Schools": ["hours"],
    "Spas": ["hours"],
    "Clinics": ["hours"],
    "Malls": ["hours"]
}


def main() -> None:
    data_path = "data/places.json"
    if not os.path.exists(data_path):
        print(f"No data file found at {data_path}.")
        return
    places = json.load(open(data_path, "r", encoding="utf-8"))
    report = {}
    for p in places:
        category = (p.get("categories") or [""])[0]
        missing = []
        for field in REQUIRED_FIELDS.get(category, []):
            if not p.get(field):
                missing.append(field)
        if missing:
            report[p["slug"]] = missing
    if report:
        print("Missing fields report:")
        for slug, fields in report.items():
            print(f"  {slug}: {', '.join(fields)}")
    else:
        print("All required fields present.")


if __name__ == "__main__":
    main()