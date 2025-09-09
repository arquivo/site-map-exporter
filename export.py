from sitemapparser import SiteMapParser
from sitemapparser.url_set import UrlSet
from typing import List
import logging
from sitemapparser.data_helpers import data_to_element
from sitemapparser.sitemap_index import SitemapIndex
import requests
import argparse


class CustomSiteMapParser(SiteMapParser):
    """
    Overwrite site map parser, so we can add basic authentication when downloading the site maps.
    """
    def __init__(self, uri):
        """
        Parses and creates sitemap or url instances for the data retrieved

        :param uri: String, uri of the sitemap.xml you want analysed
        """
        self.logger = logging.getLogger(__name__)

        data = download_uri_data(uri)
        root_element = data_to_element(data)

        self.is_sitemap_index = self._is_sitemap_index_element(root_element)

        if self.is_sitemap_index:
            self.logger.info("Root element is sitemap index")
            self._sitemaps = SitemapIndex(root_element)
        else:
            self.logger.info("Root element is url set")
            self._url_set = UrlSet(root_element)

def download_uri_data(uri):
    """
    returns file object
    """
    logger = logging.getLogger(__name__)
    logger.info("Requesting data from: %s", uri)
    # using requests to follow any redirects that happen
    headers = {'Content-Type': 'application/xml;charset=utf-8'}
    r = requests.get(uri, headers=headers, timeout=30)
    # ensure it's the decompressed content
    r.raw.decode_content = True
    logger.debug("Request content: %s", r.content)
    return r.content


def read_sitemap(sitemap_url) -> List[UrlSet]:
    """
    Reads the site map and returns a list of UrlSet objects.
    """
    sm = CustomSiteMapParser(sitemap_url)
    urls = []
    if sm.has_sitemaps():
        for sitemap in sm.get_sitemaps():
            urls.extend(read_sitemap(sitemap))
    if sm.has_urls():
        urls = sm.get_urls()
    return urls

def print_sitemap(sitemap_url : str):
    """
    Prints the site map URLs.
    """
    urls = sorted(map(lambda url: url.loc, read_sitemap(sitemap_url)))
    for url in urls:
        print(url)

parser = argparse.ArgumentParser(description='Exports site map of a site.')
parser.add_argument('url', help='the site map URL')

args = parser.parse_args()
print_sitemap(args.url)
