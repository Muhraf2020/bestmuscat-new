#!/usr/bin/env python3
"""
link_checker.py

Check the validity of website and menu URLs stored in places.json.

Attempts to make a HEAD request to each URL and prints out any that fail.

Note: This stub does not perform actual HTTP requests. Implement using requests.head() if needed.
"""
def main() -> None:
    import json
    import os
    data_path = "data/places.json"
    if not os.path.exists(data_path):
        print(f"No data file found at {data_path}.")
        return
    places = json.load(open(data_path, "r", encoding="utf-8"))
    # TODO: implement requests.head() calls here and report broken links.
    print("link_checker.py is a stub.")


if __name__ == "__main__":
    main()