import os
import sys
import pandas as pd
from io import StringIO
from pathlib import Path

from metaphor_python import Metaphor
from datetime import datetime, timedelta

from loguru import logger
from tqdm import tqdm
from tabulate import tabulate
from collections import namedtuple
import textwrap
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

from exa_py import Exa

from tenacity import (retry, stop_after_attempt, wait_random_exponential,)# for exponential backoff
from .gpt_summarize_web_content import summarize_web_content
from .gpt_competitor_analysis import summarize_competitor_content


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_metaphor_client():
    """
    Get the Metaphor client.

    Returns:
        Metaphor: An instance of the Metaphor client.
    """
    METAPHOR_API_KEY = os.environ.get('METAPHOR_API_KEY')
    if not METAPHOR_API_KEY:
        raise ValueError("METAPHOR_API_KEY environment variable not set!")
    return Exa(METAPHOR_API_KEY)


def metaphor_rag_search():
    """ Mainly used for researching blog sections. """
    metaphor = get_metaphor_client()



def metaphor_find_similar(similar_url):
    """
    Find similar content using the Metaphor API.

    Args:
        url (str): The URL to find similar content.

    Returns:
        MetaphorResponse: The response from the Metaphor API.
    """
    metaphor = get_metaphor_client()
    try:
        logger.info(f"Doing similar web search for url: {similar_url}")
        search_response = metaphor.find_similar_and_contents(
            similar_url,
            highlights=True,
            num_results=10)
    except Exception as e:
        logger.error(f"Metaphor: Error in finding similar content: {e}")
        raise

    competitors = search_response.results
    for acompetitor in tqdm(competitors, desc="Processing Competitors", unit="competitor"):
        all_contents = ""
        try:
            search_response = metaphor.search_and_contents(
                acompetitor.url,
                type="keyword",
                num_results=5
            )
        except Exception as err:
            logger.error(f"Failed to do metaphor keyword/url research: {err}")
    
        research_response = search_response.results
    
        # Add a progress bar for the inner loop
        for r in tqdm(research_response, desc=f"{acompetitor.url}", unit="research"):
            all_contents += r.text
        try:
            acompetitor.text = summarize_competitor_content(all_contents, "gemini")
        except Exception as err:
            logger.error(f"Failed to summarize_web_content: {err}")
    
    # Convert the data into a list of lists
    print_search_result(competitors)
    return search_response



def metaphor_search_articles(query, 
        num_results=5,
        use_autoprompt=True,
        include_domains=[],
        time_range=None,
        similar_url=None):
    """
    Search for articles using the Metaphor API.

    Args:
        query (str): The search query.
        num_results (int): Number of results to retrieve.
        use_autoprompt (bool): Whether to use autoprompt.
        include_domains (list): List of domains to include.
        time_range (str): Time range for published articles ("day", "week", "month", "year", "anytime").

    Returns:
        MetaphorResponse: The response from the Metaphor API.
    """
    metaphor = get_metaphor_client()
    try:
        if time_range == "past day":
            start_published_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        elif time_range == "past week":
            start_published_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        elif time_range == "past month":
            start_published_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        elif time_range == "past year":
            start_published_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        else:
            start_published_date = None
        
        logger.info(f"Metaphor web search with Date: {start_published_date} and Query: {query}")
        try:
            search_response = metaphor.search_and_contents(
                query,
                include_domains=include_domains,
                use_autoprompt=True,
                start_published_date=start_published_date,
                num_results=num_results
            )
        except Exception as err:
            logger.error(f"Failed in metaphor.search_and_contents: {err}")
        
        # From each webpage, get a summary of the web page.
        contents_response = search_response.results
        for content in tqdm(contents_response, desc="Reading Web URL content:", unit="content"):
            summarized_content = summarize_web_content(content.text, "gemini")
            content.text = summarized_content
        
        print_search_result(contents_response)

        if similar_url:
            logger.info(f"Doing similar/semantic search for URL: {similar_url}")
            metaphor_find_similar(similar_url)
        return contents_response
    
    except Exception as e:
        logger.error(f"Error in Metaphor searching articles: {e}")
        raise


def print_search_result(contents_response):
    # Define the Result namedtuple
    Result = namedtuple("Result", ["url", "title", "published_date", "text"])
    # Tabulate the data
    table_headers = ["URL", "Title", "Published Date", "Summary"]
    table_data = [(result.url, result.title, result.published_date, result.text) for result in contents_response]

    table = tabulate(table_data,
        headers=table_headers,
        tablefmt="fancy_grid",
        colalign=["left", "left", "left", "left"],
        maxcolwidths=[20, 20, 10, 60])
    print(table)
    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")


def save_in_file(table_content):
    """ Helper function to save search analysis in a file. """
    file_path = os.environ.get('SEARCH_SAVE_FILE')
    try:
        # Save the content to the file
        with open(file_path, "a") as file:
            file.write(table_content)
            file.write("\n" * 3)  # Add three newlines at the end
        logger.info(f"Search content saved to {file_path}")
    except Exception as e:
        logger.error(f"Error occurred while writing to the file: {e}")


def metaphor_scholar_search(query, include_domains=None, time_range="anytime"):
    """
    Search for papers using the Metaphor API.

    Args:
        query (str): The search query.
        include_domains (list): List of domains to include.
        time_range (str): Time range for published articles ("day", "week", "month", "year", "anytime").

    Returns:
        MetaphorResponse: The response from the Metaphor API.
    """
    client = get_metaphor_client()
    try:
        if time_range == "day":
            start_published_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        elif time_range == "week":
            start_published_date = (datetime.utcnow() - timedelta(weeks=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        elif time_range == "month":
            start_published_date = (datetime.utcnow() - timedelta(weeks=4)).strftime('%Y-%m-%dT%H:%M:%SZ')
        elif time_range == "year":
            start_published_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            start_published_date = None

        response = client.search(query, include_domains=include_domains, start_published_date=start_published_date, use_autoprompt=True)
        return response
    except Exception as e:
        logger.error(f"Error in searching papers: {e}")
