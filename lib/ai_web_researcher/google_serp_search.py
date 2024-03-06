"""
This Python script performs Google searches using various services such as SerpApi, Serper.dev, and more. It displays the search results, including organic results, People Also Ask, and Related Searches, in formatted tables. The script also utilizes GPT to generate titles and FAQs for the Google search results.

Features:
- Utilizes SerpApi, Serper.dev, and other services for Google searches.
- Displays organic search results, including position, title, link, and snippet.
- Presents People Also Ask questions and snippets in a formatted table.
- Includes Related Searches in the combined table with People Also Ask.
- Configures logging with Loguru for informative messages.
- Uses Rich and Tabulate for visually appealing and formatted tables.

Usage:
- Ensure the necessary API keys are set in the .env file.
- Run the script to perform a Google search with the specified query.
- View the displayed tables with organic results, People Also Ask, and Related Searches.
- Additional information, such as generated titles and FAQs using GPT, is presented.

Modifications:
- Update the environment variables in the .env file with the required API keys.
- Customize the search parameters, such as location and language, in the functions as needed.
- Adjust logging configurations, table formatting, and other aspects based on preferences.

To-Do (TBD):
- Consider adding further enhancements or customization based on specific use cases.

Note: This script depends on external libraries such as SerpApi, Loguru, Rich, and Tabulate. Install them using 'pip install serpapi loguru rich tabulate' if not already installed.
"""

import os
from pathlib import Path
import sys

import pandas as pd
import json
import requests
from clint.textui import progress
#from serpapi import GoogleSearch
from loguru import logger
from tabulate import tabulate
from GoogleNews import GoogleNews
# Configure logger
logger.remove()
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv(Path('../../.env'))
logger.add(
    sys.stdout,
    colorize=True,
    format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )


#from tenacity import retry, stop_after_attempt, wait_random_exponential
#@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))


#FIXME: Accept language, country and time frame to search for.
def google_search(query):
    """
    Perform a Google search for the given query.

    Args:
        query (str): The search query.
        flag (str, optional): The search flag (default is "faq").

    Returns:
        list: List of search results based on the specified flag.
    """
    #try:
    #    perform_serpapi_google_search(query)
    #    logger.info(f"FIXME: Google serapi: {query}")
    #    #return process_search_results(search_result)
    #except Exception as err:
    #    logger.error(f"ERROR: Check Here: https://serpapi.com/. Your requests may be over. {err}")

    # Retry with serper.dev
    try:
        logger.info("Trying Google search with Serper.dev: https://serper.dev/api-key")
        search_result = perform_serperdev_google_search(query)
        process_search_results(search_result)
        return(search_result)
    except Exception as err:
        logger.error(f"Failed to do Google search with serper.dev: {err}")

 
#    # Retry with BROWSERLESS API
#    try:
#        search_result = perform_browserless_google_search(query)
#        #return process_search_results(search_result, flag)
#    except Exception as err:
#        logger.error("FIXME: Failed to do Google search with BROWSERLESS API.")
#        logger.debug("FIXME: Trying with dataforSEO API.")
#                
#    # Retry with dataforSEO API
#    try:
#        logger.info("Perform SERP with Data for SEO.")
#        #search_result = perform_dataforseo_google_search(query)
#        #return process_search_results(search_result, flag)
#    except Exception as err:
#        logger.error("FIXME: Failed to do Google search with dataforSEO API.")
#        logger.debug("All retries failed. Giving up.")
#        raise
 


def perform_serpapi_google_search(query, location="in"):
    """
    Perform a Google search using the SerpApi service.

    Args:
        query (str): The search query.
        location (str, optional): The location for the search (default is "Austin, Texas").
        api_key (str, optional): Your secret API key for SerpApi.

    Returns:
        dict: A dictionary containing the search results.
    """
    try:
        # Check if API key is provided
        if not os.getenv("SERPAPI_KEY"):
            #raise ValueError("SERPAPI_KEY key is required for SerpApi")
            logger.error("SERPAPI_KEY key is required for SerpApi")
            return
            

        # Create a GoogleSearch instance
        search = GoogleSearch({
            "q": query,
            "location": location,
            "api_key": api_key
        })
        # Get search results as a dictionary
        result = search.get_dict()
        return result

    except ValueError as ve:
        # Handle missing API key error
        logger.info(f"SERPAPI ValueError: {ve}")
    except Exception as e:
        # Handle other exceptions
        logger.info(f"SERPAPI An error occurred: {e}")


def perform_serperdev_google_search(query):
    """
    Perform a Google search using the Serper API.

    Args:
        query (str): The search query.

    Returns:
        dict: The JSON response from the Serper API.
    """
    # Get the Serper API key from environment variables
    logger.info("Doing serper.dev google search.")
    serper_api_key = os.getenv('SERPER_API_KEY')

    # Check if the API key is available
    if not serper_api_key:
        raise ValueError("SERPER_API_KEY is missing. Set it in the .env file.")

    # Serper API endpoint URL
    url = "https://google.serper.dev/search"

    # FIXME: Expose options to end user. Request payload
    payload = json.dumps({
        "q": query,
        "gl": "in",
        "hl": "en",
        "num": 10,
        "autocorrect": True,
        "page": 1,
        "type": "search",
        "engine": "google"
    })

    # Request headers with API key
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    # Send a POST request to the Serper API with progress bar
    with progress.Bar(label="Searching", expected_size=100) as bar:
        response = requests.post(url, headers=headers, data=payload, stream=True)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse and return the JSON response
            return response.json()
        else:
            # Print an error message if the request fails
            logger.error(f"Error: {response.status_code}, {response.text}")
            return None



def perform_browserless_google_search():
    return

def perform_dataforseo_google_search():
    return


def google_news(search_keywords, news_period="7d", region="IN"):
    """ Get news articles from google_news"""
    googlenews = GoogleNews()
    googlenews.enableException(True)
    googlenews = GoogleNews(lang='en', region=region)
    googlenews = GoogleNews(period=news_period)
    print(googlenews.get_news('APPLE'))
    print(googlenews.search('APPLE'))


def process_search_results(search_results):
    """
    Create a Pandas DataFrame from the search results.

    Args:
        search_results (dict): The search results JSON.

    Returns:
        pd.DataFrame: Pandas DataFrame containing the search results.
    """
    data = []
    logger.info(f"Google Search Parameters: {search_results.get('searchParameters', {})}")
    organic_results = search_results.get("organic", [])

    # Displaying Organic Results
    organic_data = []
    for result in search_results["organic"]:
        position = result.get("position", "")
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        organic_data.append([position, title, link, snippet])
    
    organic_headers = ["Rank", "Title", "Link", "Snippet"]
    organic_table = tabulate(organic_data, 
            headers=organic_headers, 
            tablefmt="fancy_grid", 
            colalign=["center", "left", "left", "left"], 
            maxcolwidths=[5, 25, 35, 50])

    # Print the tables
    print("\n\n📢❗🚨 Google search Organic Results:")
    print(organic_table)

    # Displaying People Also Ask and Related Searches combined
    combined_data = []
    try:
        people_also_ask_data = []
        if "peopleAlsoAsk" in search_results:
            for question in search_results["peopleAlsoAsk"]:
                title = question.get("title", "")
                snippet = question.get("snippet", "")
                link = question.get("link", "")
                people_also_ask_data.append([title, snippet, link])
    except Exception as people_also_ask_err:
        logger.error(f"Error processing 'peopleAlsoAsk': {people_also_ask_err}")
        people_also_ask_data = []

    related_searches_data = []
    for query in search_results.get("relatedSearches", []):
        related_searches_data.append([query.get("query", "")]) 
    related_searches_headers = ["Related Search"]

    if people_also_ask_data:
        # Add Related Searches as a column to People Also Ask
        combined_data = [
            row + [related_searches_data[i][0] if i < len(related_searches_data) else ""]
            for i, row in enumerate(people_also_ask_data)
        ]
        combined_headers = ["Question", "Snippet", "Link", "Related Search"]
        # Display the combined table
        combined_table = tabulate(
            combined_data,
            headers=combined_headers,
            tablefmt="fancy_grid",
            colalign=["left", "left", "left", "left"],
            maxcolwidths=[20, 50, 20, 30]
        )
    else:
        combined_table = tabulate(
            related_searches_data,
            headers=related_searches_headers,
            tablefmt="fancy_grid",
            colalign=["left"],
            maxcolwidths=[60]
        )

    print("\n\n📢❗🚨 People Also Ask & Related Searches:")
    print(combined_table)
    # Save the combined table to a file
    try:
        save_in_file(organic_table)
        save_in_file(combined_table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")
    return search_results


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
