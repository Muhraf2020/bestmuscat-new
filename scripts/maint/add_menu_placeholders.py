#!/usr/bin/env python3
import argparse, json, sys, copy, datetime, pathlib

DEFAULT_PLACEHOLDER = {
    "menu": {
        "status": "placeholder",          # placeholder | scraped | verified
        "source": {"type": "unknown", "url": "", "captured_at": None},  # talabat|zomato|website|unknown
        "currency": "AED",                # adjust per region
        "last_updated": None,             # ISO8601
        "sections": [
            {
                "title": "Featured",
                "items": [
                    {"name": "TBA", "price": None, "desc": "", "tags": []}
                ]
            }
        ],
        "notes": "Auto-added placeholder. Replace with real menu data."
    }
}

def ensure_menu_placeholder(obj, now_iso):
    if not isinstance(obj, dict):
        return False

    # categorize: only for Restaurants
    categories = obj.get("categories") or obj.get("category") or []
    if isinstance(categories, str):
        categories = [categories]
    # normalize case
    categories_norm = {str(c).strip().lower() for c in categories}

    if "restaurants" not in categories_norm:
        return False

    if "menu" in obj and isinstance(obj["menu"], dict):
        # already has menu; do nothing
        return False

    obj["menu"] = copy.deepcopy(DEFAULT_PLACEHOLDER["menu"])
    obj["menu"]["last_updated"] = now_iso
    return True

def main():
    ap = argparse.ArgumentParser(description="Add menu placeholders to restaurant records")
    ap.add_argument("--file", default="data/tools.json", help="Path to JSON file (array of place objects)")
    ap.add_argument("--write", action="store_true", help="Actually write changes")
    ap.add_argument("--currency", default="AED", help="Currency code for placeholders")
    args = ap.parse_args()

    p = pathlib.Path(args.file)
    if not p.exists():
        sys.exit(f"ERROR: File not found: {args.file}")

    with p.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            sys.exit(f"ERROR: JSON parse failed: {e}")

    if not isinstance(data, list):
        sys.exit("ERROR: Expected a JSON array of place objects at top level.")

    now_iso = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    # patch currency default if user overrides
    DEFAULT_PLACEHOLDER["menu"]["currency"] = args.currency

    changed = 0
    changed_ids = []
    for obj in data:
        if ensure_menu_placeholder(obj, now_iso):
            changed += 1
            changed_ids.append(obj.get("slug") or obj.get("id"))

    if not args.write:
        print(f"[dry-run] Would add menu placeholders to {changed} records.")
        if changed_ids:
            print("First few:", ", ".join([str(x) for x in changed_ids[:10]]))
        return

    # backup
    bak = p.with_suffix(p.suffix + f".bak.{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}")
    p.rename(bak)

    # write
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Wrote changes to {p} (backup at {bak}). Added placeholders to {changed} records.")

if __name__ == "__main__":
    main()
