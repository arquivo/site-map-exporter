# Site map exporter

This repository contains a python script that reads a site map and extract its URLs.

## Installation

Create a virtual environment.

```bash
python venv .venv
. .venv/bin/activate
```

Install the package requirements in the virtual environment.
```bash
pip install -r requirements.txt
```


## Parameters

This requires a root link to the site map URL.

## Execution

Export STAGE environment that has Richie:

```python
python export.py https://example.com/sitemap_index.xml > urls.txt
```
