#!/usr/bin/env python3
"""
Check HTTP status of URLs read from stdin.
Prints successful URLs (200) to stdout, failed URLs to stderr.

Usage Examples:
    # Check URLs from a file
    cat urls.txt | python check_status.py
    
    # Chain with sitemap exporter to verify exported URLs
    python export_urls.py --url https://example.com/sitemap.xml | python check_status.py
    
    # Save successful and failed URLs separately
    cat urls.txt | python check_status.py > valid_urls.txt 2> failed_urls.txt
    
    # Process multiple sitemaps and check all URLs
    cat sitemap_urls.txt | python export_urls.py | python check_status.py > all_valid_urls.txt

Output:
    - Valid URLs (HTTP 200) are printed to stdout
    - Failed URLs with error messages are printed to stderr
    - Progress updates every 10 URLs to stderr
    - Final summary printed to stderr

Features:
    - Follows redirects (allow_redirects=True)
    - 120 second timeout per URL
    - Detailed error reporting
    - Progress tracking
"""
import sys
from urllib.parse import urlparse

import requests



def check_url(url):
    """
    Check if URL returns status 200.
    Returns (success, status_code, error_message) tuple.
    """
    try:
        headers = {'User-Agent': 'Arquivo-web-crawler-site-map-exporter/1.0'}
        response = requests.get(url, headers=headers, timeout=120, allow_redirects=True)
        return response.status_code == 200, response.status_code, None
    except Exception as e:
        return False, None, f"Unexpected error: {str(e)}"


def main():
    """Process URLs from stdin and check their status."""
    processed = 0
    successful = 0
    failed = 0

    for line in sys.stdin:
        url = line.strip()
        if not url:
            continue

        processed += 1
        success, status_code, error_msg = check_url(url)

        if success:
            print(url, flush=True)
            successful += 1
        else:
            if error_msg:
                print(f"{url} - Error: {error_msg}", file=sys.stderr, flush=True)
            else:
                print(f"{url} - HTTP Status: {status_code}", file=sys.stderr, flush=True)
            failed += 1

        # Print progress to stderr
        if processed % 10 == 0:
            print(f"Progress: {processed} URLs processed ({successful} successful, {failed} failed)", 
                  file=sys.stderr, flush=True)

    # Final summary
    print(f"\nFinal: {processed} URLs processed ({successful} successful, {failed} failed)", 
          file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()