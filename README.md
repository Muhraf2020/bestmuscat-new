# Best Muscat Automation Repository

This repository contains a static website and a set of automation scripts designed to power the Best Muscat listings site. The site showcases restaurants, hotels, schools, spas, clinics and malls with rich metadata and is able to ingest new places automatically from external APIs.

## Directory layout

See the specification in the project documentation for a full description of the directory structure. In brief:

- **index.html** – Landing page displaying all places with filters and sorting.
- **tool.html** – Detail page template used for a single place.
- **assets/** – Contains styles and JavaScript for the site.
- **data/** – Houses the canonical `places.json` and supporting taxonomies.
- **scripts/** – Python scripts for ingestion, enrichment, QA and build processes.
- **.github/workflows/** – Continuous integration configuration.

## Getting started

1. Copy `.env.example` to `.env` and fill in your API keys.
2. Create a virtual environment and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the discovery scripts to fetch new places around Muscat. See `scripts/ingest/discover_google_places.py` for usage.
4. Run the enrichment and QA scripts to build `data/places.json`.
5. Serve the site locally with your favourite static server (for example `python -m http.server`).

## Contributing

This repository is intended as a starting point. Feel free to extend the schema, add more categories, or improve the UI.