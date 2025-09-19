#!/usr/bin/env python3
"""
build_sitemaps.py

Generate XML sitemaps for the static site.

This stub writes no-op sitemap files into data/sitemaps/.
"""
import os


def main() -> None:
    output_dir = "data/sitemaps"
    os.makedirs(output_dir, exist_ok=True)
    # TODO: implement real sitemap generation.
    for name in ["sitemap.xml", "sitemap-places.xml"]:
        with open(os.path.join(output_dir, name), "w", encoding="utf-8") as f:
            f.write("<!-- sitemap stub -->\n")
    print(f"Wrote stub sitemaps to {output_dir}.")


if __name__ == "__main__":
    main()