import os
from pathlib import Path

from firecrawl import FirecrawlApp
import logging
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv(Path('../../.env'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_client():
    """
    Initialize and return a Firecrawl client.

    Args:
        api_key (str): Your Firecrawl API key.

    Returns:
        firecrawl.Client: An instance of the Firecrawl client.
    """
    return FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))


def scrape_website(website_url, depth=1, max_pages=10):
    """
    Scrape a website starting from the given URL.

    Args:
        api_key (str): Your Firecrawl API key.
        website_url (str): The URL of the website to scrape.
        depth (int, optional): The depth of crawling. Default is 1.
        max_pages (int, optional): The maximum number of pages to scrape. Default is 10.

    Returns:
        dict: The result of the website scraping, or None if an error occurred.
    """
    client = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
    try:
        result = client.crawl_url({
            'url': website_url,
            'depth': depth,
            'max_pages': max_pages
        })
        return result
    except Exception as e:
        logging.error(f"Error scraping website: {e}")
        return None


def scrape_url(url):
    """
    Scrape a specific URL.

    Args:
        api_key (str): Your Firecrawl API key.
        url (str): The URL to scrape.

    Returns:
        dict: The result of the URL scraping, or None if an error occurred.
    """
    client = initialize_client()
    #params = {
    #'pageOptions': {
    #    'onlyMainContent': True
    #    }
    #}
    try:
        #result = client.scrape_url(url, params=params)
        result = client.scrape_url(url)
        return result
    except Exception as e:
        logging.error(f"Error scraping URL: {e}")
        return None


def extract_data(url, schema):
    """
    Extract structured data from a URL using the provided schema.

    Args:
        api_key (str): Your Firecrawl API key.
        url (str): The URL to extract data from.
        schema (dict): The schema to use for data extraction.

    Returns:
        dict: The extracted data, or None if an error occurred.
    """
    client = initialize_client()
    try:
        result = client.extract({
            'url': url,
            'schema': schema
        })
        return result
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        return None
