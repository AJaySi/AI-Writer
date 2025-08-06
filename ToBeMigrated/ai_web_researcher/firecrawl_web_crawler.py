import os
from pathlib import Path
from firecrawl import FirecrawlApp
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path('../../.env'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_client() -> FirecrawlApp:
    """
    Initialize and return a Firecrawl client.

    Returns:
        FirecrawlApp: An instance of the Firecrawl client.
    """
    return FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

def scrape_website(website_url: str, depth: int = 1, max_pages: int = 10) -> dict:
    """
    Scrape a website starting from the given URL.

    Args:
        website_url (str): The URL of the website to scrape.
        depth (int, optional): The depth of crawling. Default is 1.
        max_pages (int, optional): The maximum number of pages to scrape. Default is 10.

    Returns:
        dict: The result of the website scraping, or None if an error occurred.
    """
    client = initialize_client()
    try:
        result = client.crawl_url({
            'url': website_url,
            'depth': depth,
            'max_pages': max_pages
        })
        return result
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")
    except ValueError as e:
        logging.error(f"Value error: {e}")
    except Exception as e:
        logging.error(f"Error scraping website: {e}")
    return None

def scrape_url(url: str) -> dict:
    """
    Scrape a specific URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        dict: The result of the URL scraping, or None if an error occurred.
    """
    client = initialize_client()
    try:
        result = client.scrape_url(url)
        return result
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")
    except ValueError as e:
        logging.error(f"Value error: {e}")
    except Exception as e:
        logging.error(f"Error scraping URL: {e}")
    return None

def extract_data(url: str, schema: dict) -> dict:
    """
    Extract structured data from a URL using the provided schema.

    Args:
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
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")
    except ValueError as e:
        logging.error(f"Value error: {e}")
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
    return None
