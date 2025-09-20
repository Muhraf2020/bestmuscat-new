#!/usr/bin/env python3
import argparse, json, sys, copy, datetime, pathlib

# Resolve repo root relative to THIS file: <repo>/scripts/maint/add_menu_placeholders.py
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]  # scripts/maint -> scripts -> <repo>
DEFAULT_FILE = REPO_ROOT / "data" / "tools.json"

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

def ensure_menu_placeholder(obj, now_iso, debug=False):
    if not isinstance(obj, dict):
        return False

    categories = obj.get("categories") or obj.get("category") or []
    if isinstance(categories, str):
        categories = [categories]
    categories_norm = {str(c).strip().lower() for c in categories}

    is_restaurant = "restaurants" in categories_norm
    if debug:
        print(f"DEBUG: slug={obj.get('slug') or obj.get('id')} cats={categories} is_restaurant={is_restaurant} has_menu={'menu' in obj}")

    if not is_restaurant:
        return False
    if "menu" in obj and isinstance(obj["menu"], dict):
        return False

    obj["menu"] = copy.deepcopy(DEFAULT_PLACEHOLDER["menu"])
    obj["menu"]["last_updated"] = now_iso
    return True

def main():
    ap = argparse.ArgumentParser(description="Add menu placeholders to restaurant records")
    ap.add_argument("--file", default=str(DEFAULT_FILE), help="Path to JSON file (array of place objects)")
    ap.add_argument("--write", action="store_true", help="Actually write changes")
    ap.add_argument("--currency", default="AED", help="Currency code for placeholders")
    ap.add_argument("--debug", action="store_true", help="Print per-record classification")
    args = ap.parse_args()

    p = pathlib.Path(args.file)
    if not p.exists():
        sys.exit(f"ERROR: File not found: {args.file}")

    try:
        with p.open("r", encoding="utf-8") as f:
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
        if ensure_menu_placeholder(obj, now_iso, debug=args.debug):
            changed += 1
            changed_ids.append(obj.get("slug") or obj.get("id"))

    if not args.write:
        print(f"[dry-run] Would add menu placeholders to {changed} records.")
        if changed_ids:
            print("First few:", ", ".join([str(x) for x in changed_ids[:10]]))
        return

    # backup next to target
    bak = p.with_suffix(p.suffix + f".bak.{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}")
    p.rename(bak)

    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Wrote changes to {p} (backup at {bak}). Added placeholders to {changed} records.")

if __name__ == "__main__":
    main()
