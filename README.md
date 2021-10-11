# Site map exporter for NAU project

This repository contains a python script that reads a site map, extract its URLs.

## Installation

Create a virtual environment.

```bash
virtualenv venv --python=python3
. venv/bin/activate
```

Install the package requirements in the virtual environment.
```bash
pip install -r requirements.txt
```

## Execution
For WordPress the sitemap is located on /sitemap_index.xml but on Richie it's located on /sitemap.xml.


Export STAGE environment that has Richie:
```python
python export.py https://www.stage.nau.fccn.pt/sitemap.xml --user <USER> --password <PASSWORD>
```

Export PROD environment that has WordPress:
```python
python export.py https://www.nau.edu.pt/sitemap_index.xml
```
