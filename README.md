# Site Map Exporter

A collection of Python utilities for extracting and validating URLs from XML sitemaps. This toolset is designed for efficient bulk processing of sitemaps, with support for nested sitemap indexes and URL validation.

## Features

- **Sitemap URL Extraction** (`export_urls.py`): Extract all URLs from XML sitemaps with recursive support for nested sitemap indexes
- **URL Status Checker** (`check_status.py`): Validate extracted URLs by checking their HTTP status
- **Streaming Architecture**: Memory-efficient processing for large sitemaps
- **Batch Processing**: Handle multiple sitemaps via stdin for automated workflows
- **Error Handling**: Continues processing on errors with detailed logging

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Requirements

- Python 3.6+
- `site-map-parser==0.3.9`
- `requests` (installed as a dependency)

## Scripts

### `export_urls.py`

Extracts and prints all URLs from XML sitemaps. Supports both single URLs and batch processing from stdin.

**Features:**
- Handles nested sitemaps recursively
- Only accepts HTTP 200 responses (no redirects)
- Streams URLs for memory efficiency
- Progress and errors logged to stderr
- Results printed to stdout

**Usage:**

```bash
# Single sitemap URL
python export_urls.py --url https://example.com/sitemap.xml > urls.txt

# Multiple sitemaps from a file
cat sitemap_list.txt | python export_urls.py > all_urls.txt 2> errors.log

# Generate sitemap URLs dynamically and pipe
cat domains.txt | awk '{print "https://" $0 "/sitemap.xml"}' | python export_urls.py > urls.txt 2> errors.log
```

### `check_status.py`

Validates URLs by checking their HTTP status. Reads URLs from stdin and outputs valid URLs (HTTP 200) to stdout, with failed URLs logged to stderr.

**Features:**
- Follows redirects automatically
- 120-second timeout per URL
- Progress tracking (every 10 URLs)
- Detailed error reporting
- Final summary statistics

**Usage:**

```bash
# Check URLs from a file
cat urls.txt | python check_status.py > valid_urls.txt 2> failed_urls.log

# Chain with sitemap exporter
python export_urls.py --url https://example.com/sitemap.xml | python check_status.py > valid_urls.txt
```

## Usage Examples

### Export URLs from a Single Sitemap

```bash
python export_urls.py --url https://example.com/sitemap_index.xml > urls.txt
```

### Process Multiple Sitemaps from a Domain List

From a list of domains, construct sitemap URLs and extract all pages:

```bash
cat domains.txt | awk '{print "https://" $0 "/sitemap.xml"}' | python export_urls.py 2>> error.log 1>> all_pages.txt
```

### Filter URLs by HTTP Status

Check which domains from a list return HTTP 200:

```bash
cat domains.txt | awk '{print "https://" $0}' | python check_status.py 2>> error.log 1>> valid_domains.txt
```

### Complete Pipeline: Extract and Validate URLs

Extract URLs from sitemaps and validate them in one pipeline:

```bash
cat sitemap_urls.txt | python export_urls.py 2>> export_errors.log | python check_status.py 1>> validated_urls.txt 2>> check_errors.log
```

### Process a List of Sitemaps with Validation

```bash
# Step 1: Extract all URLs from multiple sitemaps
cat domains.txt | awk '{print "https://" $0 "/sitemap.xml"}' | python export_urls.py > all_urls.txt 2> export_errors.log

# Step 2: Validate the extracted URLs
cat all_urls.txt | python check_status.py > valid_urls.txt 2> validation_errors.log
```

## Output Format

### `export_urls.py`

- **stdout**: One URL per line (extracted from sitemaps)
- **stderr**: Progress messages and error logs

### `check_status.py`

- **stdout**: Valid URLs (HTTP 200), one per line
- **stderr**: Failed URLs with error messages, progress updates, and summary

## Error Handling

Both scripts are designed to continue processing even when individual URLs fail. Errors are logged to stderr, allowing you to:

1. Monitor progress in real-time
2. Save errors separately from results using file redirection
3. Review failed URLs after processing completes

## License

See [LICENSE](LICENSE) file for details.

