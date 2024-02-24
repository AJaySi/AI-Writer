import os

import requests
from clint.textui import progress
from loguru import logger
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))


def search_ydc_index(search_query, num_web_results=10, country="IN"):
    """
    Search YDC Index API and retrieve results.

    Args:
        search_query (str): The search query.
        num_web_results (int): Number of web results to retrieve.
        country (str): Country code.
        api_key (str): YDC Index API key.

    Returns:
        dict: The response from the YDC Index API in JSON format.
    """
    api_key = os.environ["YOU_API_KEY"]
    try:
        url = "https://api.ydc-index.io/search"

        querystring = {
            "query": search_query,
        }

        headers = {"X-API-Key": api_key}

        response = requests.get(url, headers=headers, params=querystring, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        result_json = response.json()
        return result_json

    except requests.exceptions.RequestException as req_exc:
        logger.error(f"Request to YDC Index API failed: {req_exc}")
        return {"error": str(req_exc)}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": str(e)}


def get_rag_results(search_query, num_web_results=10, country="IN"):
    """
    Retrieve RAG (Relevance, Authority, and Goodness) results from YDC Index API.

    Args:
        search_query (str): The search query.
        num_web_results (int): Number of web results to retrieve.
        country (str): Country code

    Returns:
        dict: The response from the YDC Index API in JSON format.
    """
    api_key = os.environ["YOU_API_KEY"]
    try:
        url = "https://api.ydc-index.io/rag"

        querystring = {
            "query": search_query,
            "num_web_results": str(num_web_results),
            "country": country
        }

        headers = {"X-API-Key": api_key}

        with progress.Bar(expected_size=num_web_results, label="Fetching RAG Results") as bar:
            response = requests.get(url, headers=headers, params=querystring, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            result_json = response.json()
            bar.show(result_json.get("web_results", []))  # Update progress bar with the number of web results

        return result_json

    except requests.exceptions.RequestException as req_exc:
        logger.error(f"Request to YDC Index API failed: {req_exc}")
        return {"error": str(req_exc)}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": str(e)}


def get_news_results(query, spellcheck=True):
    """
    Retrieve news results from YDC Index API.

    Args:
        query (str): The search query.
        spellcheck (bool): Whether to enable spellcheck.
        api_key (str): YDC Index API key.

    Returns:
        dict: The response from the YDC Index API in JSON format.
    """
    api_key = os.environ["YOU_API_KEY"]
    try:
        url = "https://api.ydc-index.io/news"

        querystring = {
            "q": query,
            "spellcheck": str(spellcheck).lower()
        }

        headers = {"X-API-Key": api_key}

        with progress.Bar(expected_size=1, label="Fetching News Results") as bar:
            response = requests.get(url, headers=headers, params=querystring, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            result_json = response.json()
            bar.show()  # Update progress bar

        return result_json

    except requests.exceptions.RequestException as req_exc:
        logger.error(f"Request to YDC Index API failed: {req_exc}")
        return {"error": str(req_exc)}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": str(e)}
