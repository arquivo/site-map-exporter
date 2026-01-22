#!/usr/bin/env python3
"""
Sitemap URL Exporter

Extracts and prints all URLs from XML sitemaps. Supports single URLs or batch processing from stdin.

Usage Examples:
    # Single sitemap URL
    python export_urls.py --url https://example.com/sitemap.xml

    # Multiple sitemaps from stdin
    cat urls.txt | python export_urls.py
    
    # Pipe URLs directly
    echo -e "https://site1.com/sitemap.xml\\nhttps://site2.com/sitemap.xml" | python export_urls.py
    
    # Generate sitemap URLs and pipe to script
    head -10 domains.txt | awk '{print "https://" $0 "/sitemap.xml"}' | python export_urls.py
    
    # Save results and errors separately
    cat urls.txt | python export_urls.py > out.log 2> error.log

Output:
    - Extracted URLs are printed to stdout (one per line)
    - Progress and errors are printed to stderr
    
Features:
    - Streams URLs for memory efficiency
    - Handles nested sitemaps recursively
    - Only accepts HTTP 200 responses (no redirects)
    - Continues processing on errors
"""
import argparse
import sys

import requests
from sitemapparser import SiteMapParser
from sitemapparser.data_helpers import data_to_element
from sitemapparser.sitemap_index import SitemapIndex
from sitemapparser.url_set import UrlSet


def log_msg(message, *args):
    """
    Logs a message to stderr.
    
    :param message: Message format string
    :param args: Arguments for the format string
    """
    print(message % args, file=sys.stderr)


class CustomSiteMapParser(SiteMapParser):
    """
    Overwrite site map parser, so we can add basic authentication when downloading the site maps.
    """

    def __init__(self, uri):
        """
        Parses and creates sitemap or url instances for the data retrieved

        :param uri: String, uri of the sitemap.xml you want analysed
        """
        data = download_uri_data(uri)
        root_element = data_to_element(data)

        self.is_sitemap_index = self._is_sitemap_index_element(root_element)

        if self.is_sitemap_index:
            log_msg("Root element is sitemap index")
            self._sitemaps = SitemapIndex(root_element)
        else:
            log_msg("Root element is url set")
            self._url_set = UrlSet(root_element)


def download_uri_data(uri):
    """
    returns file object
    """
    log_msg("Requesting data from: %s", uri)
    # headers = {'Content-Type': 'application/xml;charset=utf-8'}
    headers = {'User-Agent': 'sitemap-exporter/1.0'}
    r = requests.get(uri, headers=headers, timeout=120, allow_redirects=False)

    if r.status_code != 200:
        error_msg = f"Error: URL {uri} returned HTTP status {r.status_code}"
        log_msg(error_msg)
        raise requests.HTTPError(error_msg)

    # ensure it's the decompressed content
    r.raw.decode_content = True
    return r.content


def read_sitemap(url: str):
    """
    Reads the site map and yields URL strings as they're discovered.
    """
    try:
        sm = CustomSiteMapParser(url)
        if sm.has_sitemaps():
            for sitemap in sm.get_sitemaps():
                yield from read_sitemap(sitemap)
        if sm.has_urls():
            for url in sm.get_urls():
                yield url.loc
    except (requests.HTTPError, requests.RequestException) as e:
        # Error already logged to stderr in download_uri_data
        log_msg("Failed to retrieve sitemap %s: %s", url, e)
        pass


def print_sitemap(sm_url: str):
    """
    Prints the site map URLs as they're discovered (streaming for efficiency).
    """
    urls_count = 0
    try:
        for url in read_sitemap(sm_url):
            print(url)
            urls_count += 1
        log_msg("Exported %d URLs", urls_count)
    except Exception as e:
        log_msg("Error processing sitemap %s: %s (exported %d URLs before error)", sm_url, e, urls_count)


parser = argparse.ArgumentParser(description='Exports site map of a site.')
parser.add_argument(
    '--url', help='the site map URL (optional, reads from stdin if not provided)')

args = parser.parse_args()

if args.url:
    # Single URL from command line argument
    log_msg("Processing: %s", args.url)
    print_sitemap(args.url)
else:
    # Read URLs from stdin
    count = 0
    for line in sys.stdin:
        sitemap_url = line.strip()
        if sitemap_url:  # Skip empty lines
            count += 1
            log_msg("[%d] Processing: %s", count, sitemap_url)
            print_sitemap(sitemap_url)
