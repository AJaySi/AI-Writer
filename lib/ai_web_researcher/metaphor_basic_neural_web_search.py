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
from .common_utils import save_in_file, cfg_search_param


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
    urls = {}
    for c in competitors:
        print(c.title + ':' + c.url)
    for acompetitor in tqdm(competitors, desc="Processing URL content", unit="competitor"):
        all_contents = ""
        try:
            search_response = metaphor.search_and_contents(
                acompetitor.url,
                type="keyword",
                num_results=3
            )
        except Exception as err:
            logger.error(f"Failed to do metaphor keyword/url research: {err}")
    
        research_response = search_response.results
        # Add a progress bar for the inner loop
        for r in tqdm(research_response, desc=f"{acompetitor.url}", unit="research"):
            all_contents += r.text
            try:
                acompetitor.text = summarize_competitor_content(all_contents)
            except Exception as err:
                logger.error(f"Failed to summarize_web_content: {err}")
    
    print_search_result(competitors)
    return search_response



def metaphor_search_articles(query):
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
        include_domains, start_published_date, num_results, similar_url = cfg_search_param('exa')
        
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
        # FIXME: Need to summarize for smaller input context window.
#        for content in tqdm(contents_response, desc="Reading Web URL content:", unit="content"):
#            summarized_content = summarize_web_content(content.text, "gemini")
#            content.text = summarized_content
        
        print_search_result(contents_response)

        if similar_url:
            logger.info(f"Doing similar/semantic search for URL: {similar_url}")
            metaphor_find_similar(similar_url)
        return contents_response
    
    except Exception as e:
        logger.error(f"Error in Metaphor searching articles: {e}")
        raise



def metaphor_news_summarizer(news_keywords):
    """ build a LLM-based news summarizer app with the Exa API to keep us up-to-date 
    with the latest news on a given topic.
    """
    # FIXME: Needs to be user defined.
    one_week_ago = (datetime.now() - timedelta(days=7))
    date_cutoff = one_week_ago.strftime("%Y-%m-%d")

    search_response = exa.search_and_contents(
        news_keywords, use_autoprompt=True, start_published_date=date_cutoff
    )

    urls = [result.url for result in search_response.results]
    print("URLs:")
    for url in urls:
        print(url)


def print_search_result(contents_response):
    # Define the Result namedtuple
    Result = namedtuple("Result", ["url", "title", "text"])
    # Tabulate the data
    table_headers = ["URL", "Title", "Summary"]
    table_data = [(result.url, result.title, result.text) for result in contents_response]

    table = tabulate(table_data,
        headers=table_headers,
        tablefmt="fancy_grid",
        colalign=["left", "left", "left"],
        maxcolwidths=[20, 20, 70])
    print(table)
    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")


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
