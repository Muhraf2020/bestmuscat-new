#!/usr/bin/env python3
"""
Add "menu" placeholders to Restaurant entries in data/tools.json.

Usage:
  python scripts/maint/add_menu_placeholders.py            # dry-run (prints what it WOULD change)
  python scripts/maint/add_menu_placeholders.py --write    # writes changes to data/tools.json
  python scripts/maint/add_menu_placeholders.py --file path/to/tools.json --write
"""

import argparse
import copy
import datetime as dt
import json
import os
import sys

DEFAULT_MENU = {
    "menu_version": 1,
    "menu_source": {
        "type": "manual",   # manual | talabat | zomato | website | pdf | other
        "url": ""
    },
    "price_currency": "OMR",
    "menu_last_checked": None,   # will be filled with ISO timestamp
    "menu_sections": [
        {
            "title": "Popular",
            "items": [
                {
                    "name": "Example Dish",
                    "desc": "Short description of the dish.",
                    "price": 3.5,
                    "spicy": False,
                    "veg": False,
                    "tags": []
                }
            ]
        }
    ],
    # Optional extras your extension can fill later:
    # "menu_images": ["data/media/<slug>/menu/cover.webp", ...],
    # "menu_pdf": "data/media/<slug>/menu/menu.pdf",
    "menu_notes": "Placeholder added automatically."
}

def is_restaurant(entry):
    cats = entry.get("categories") or entry.get("attributes", {}).get("category") or []
    # normalize and check
    norm = [str(c).strip().lower() for c in cats if c]
    return any(c in ("restaurant", "restaurants") for c in norm)

def ensure_menu(entry, now_iso):
    if "menu" in entry and isinstance(entry["menu"], dict):
        # make sure minimal keys exist without overwriting user content
        changed = False
        if "menu_last_checked" not in entry["menu"]:
            entry["menu"]["menu_last_checked"] = now_iso
            changed = True
        if "price_currency" not in entry["menu"]:
            entry["menu"]["price_currency"] = "OMR"
            changed = True
        if "menu_sections" not in entry["menu"]:
            entry["menu"]["menu_sections"] = copy.deepcopy(DEFAULT_MENU["menu_sections"])
            changed = True
        return changed, "updated-minor"
    else:
        # add the whole block
        entry["menu"] = copy.deepcopy(DEFAULT_MENU)
        entry["menu"]["menu_last_checked"] = now_iso
        return True, "added"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="data/tools.json", help="Path to tools.json")
    ap.add_argument("--write", action="store_true", help="Write changes in-place (default is dry-run)")
    args = ap.parse_args()

    path = args.file
    if not os.path.exists(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON parse failed: {e}", file=sys.stderr)
            sys.exit(1)

    if not isinstance(data, list):
        print("ERROR: tools.json must be a JSON array.", file=sys.stderr)
        sys.exit(1)

    now_iso = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    total = len(data)
    restaurants = 0
    changed = 0
    actions = []

    for i, entry in enumerate(data):
        try:
            if is_restaurant(entry):
                restaurants += 1
                did_change, how = ensure_menu(entry, now_iso)
                if did_change:
                    changed += 1
                    actions.append((entry.get("slug") or entry.get("name") or f"idx:{i}", how))
        except Exception as e:
            slug = entry.get("slug") or entry.get("name") or f"idx:{i}"
            print(f"WARNING: Skipped {slug}: {e}", file=sys.stderr)

    print(f"Scanned: {total} entries")
    print(f"Restaurants found: {restaurants}")
    print(f"Would change: {changed}")

    for slug, how in actions:
        print(f" - {slug}: {how}")

    if changed == 0:
        print("No changes needed.")
        return

    if args.write:
        # backup
        ts = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        backup = f"{path}.bak.{ts}"
        with open(backup, "w", encoding="utf-8") as b:
            json.dump(data, b, ensure_ascii=False, indent=2)
        # NOTE: we wrote backup with the *modified* data by mistake—fix that by reloading original,
        #       then writing modified to main path. Simpler: save original to backup before changes.
        # To keep it clean, re-load original file and save it as backup properly:
        with open(path, "r", encoding="utf-8") as f2:
            original = json.load(f2)
        with open(backup, "w", encoding="utf-8") as b2:
            json.dump(original, b2, ensure_ascii=False, indent=2)

        # now write updated data
        with open(path, "w", encoding="utf-8") as f3:
            json.dump(data, f3, ensure_ascii=False, indent=2)

        print(f"\nWrote changes to {path}")
        print(f"Backup saved to {backup}")
    else:
        print("\n(Dry-run) No files were modified. Re-run with --write to apply changes.")

if __name__ == "__main__":
    main()
