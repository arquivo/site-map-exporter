# Site map exporter for NAU project

This repository contains a python script that reads a site map, extract its URLs.

It was need some customization code because NAU STAGE environment has a basic authentication access to prevent web search engines to index that data.

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


## Parameters

| Parameter | Required Description |
|------------|---------------------|
| url | True | the URL | 
| `--user` | False | the basic authentication username |
| `--pass` | False | the basic authentication password |
| `--remove_host` | if passsed it removes the protocol and hostname on the output |

## Execution

For WordPress the sitemap is located on `/sitemap_index.xml` but on Richie it's located on `/sitemap.xml`. Example:

Export STAGE environment that has Richie:
```python
python export.py https://www.stage.nau.fccn.pt/sitemap.xml --user <USER> --password <PASSWORD> --remove_host true > stage.txt
```

Export PROD environment that has WordPress:
```python
python export.py https://www.nau.edu.pt/sitemap_index.xml --remove_host true > prod.txt
```

Then you can use a comparation program, like diff, meld, etc. to compare both files.
