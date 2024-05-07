"""
This Python script uses the Tavily AI service to perform advanced searches based on specified keywords and options. It retrieves Tavily AI search results, pretty-prints them using Rich and Tabulate, and provides additional information such as the answer to the search query and follow-up questions.

Features:
- Utilizes the Tavily AI service for advanced searches.
- Retrieves API keys from the environment variables loaded from a .env file.
- Configures logging with Loguru for informative messages.
- Implements a retry mechanism using Tenacity to handle transient failures during Tavily searches.
- Displays search results, including titles, snippets, and links, in a visually appealing table using Tabulate and Rich.

Usage:
- Ensure the necessary API keys are set in the .env file.
- Run the script to perform a Tavily AI search with specified keywords and options.
- The search results, including titles, snippets, and links, are displayed in a formatted table.
- Additional information, such as the answer to the search query and follow-up questions, is presented in separate tables.

Modifications:
- To modify the script, update the environment variables in the .env file with the required API keys.
- Adjust the search parameters, such as keywords and search depth, in the `get_tavilyai_results` function as needed.
- Customize logging configurations and table formatting according to preferences.

To-Do (TBD):
- Consider adding further enhancements or customization based on specific use cases.

"""


import os
from pathlib import Path
import sys
from dotenv import load_dotenv
from loguru import logger
from tavily import TavilyClient
from rich import print
from tabulate import tabulate
# Load environment variables from .env file
load_dotenv(Path('../../.env'))
from rich import print

# Configure logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )

from .common_utils import save_in_file, cfg_search_param
from tenacity import retry, stop_after_attempt, wait_random_exponential


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_tavilyai_results(keywords):
    """
    Get Tavily AI search results based on specified keywords and options.

    Args:
        keywords (str): Keywords for Tavily AI search.
        include_urls (str): Comma-separated URLs to include in the search.
        search_depth (str, optional): Search depth option (default is "advanced").

    Returns:
        dict: Tavily AI search results.
    """
    # Run Tavily search
    logger.info(f"Running Tavily search on: {keywords}")

    # Retrieve API keys
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        raise ValueError("API keys for Tavily is Not set.")

    # Initialize Tavily client
    try:
        client = TavilyClient(api_key=api_key)
    except Exception as err:
        logger.error(f"Failed to create Tavily client. Check TAVILY_API_KEY: {err}")
    
    # Read search config params from the file.
    try:
        include_urls = cfg_search_param('tavily')
    except Exception as err:
        logger.error(f"Failed to read search params from main_config: {err}")

    try:
        if include_urls:
            tavily_search_result = client.search(keywords, 
                    search_depth="advanced", 
                    include_answer=True, 
                    include_domains=include_urls)
        else:
            tavily_search_result = client.search(keywords, 
                    search_depth = "advanced", 
                    include_answer=True)

        print_result_table(tavily_search_result)
        return(tavily_search_result)
    except Exception as err:
        logger.error(f"Failed to do Tavily Research: {err}")


def print_result_table(output_data):
    """ Pretty print the tavily AI serch result. """
    # Prepare data for tabulate
    table_data = []
    for item in output_data.get("results"):
        title = item.get("title", "")
        snippet = item.get("content", "")
        link = item.get("url", "")
        table_data.append([title, snippet, link])
    
    # Define table headers
    table_headers = ["Title", "Snippet", "Link"] 
    # Display the table using tabulate
    table = tabulate(table_data, 
            headers=table_headers, 
            tablefmt="fancy_grid", 
            colalign=["left", "left", "left"], 
            maxcolwidths=[30, 60, 30])
    # Print the table
    print(table)

    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")
    
    # Display the 'answer' in a table
    table_headers = [f"The answer to search query: {output_data.get('query')}"]
    table_data = [[output_data.get("answer")]]
    table = tabulate(table_data, 
            headers=table_headers, 
            tablefmt="fancy_grid", 
            maxcolwidths=[80])
    print(table)
    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"Failed to save search results: {save_results_err}")
    
    # Display the 'follow_up_questions' in a table
    if output_data.get("follow_up_questions"):
        table_headers = [f"Search Engine follow up questions for query: {output_data.get('query')}"]
        table_data = [[output_data.get("follow_up_questions")]]
        table = tabulate(table_data, 
            headers=table_headers, 
            tablefmt="fancy_grid",
            maxcolwidths=[80])
        print(table)
        try:
            save_in_file(table)
        except Exception as save_results_err:
            logger.error(f"Failed to save search results: {save_results_err}")


def save_in_file(table_content):
    """ Helper function to save search analysis in a file. """
    file_path = os.environ.get('SEARCH_SAVE_FILE')
    try:
        # Save the content to the file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(table_content)
            file.write("\n" * 3)  # Add three newlines at the end
        logger.info(f"Search content saved to {file_path}")
    except Exception as e:
        logger.error(f"Error occurred while writing to the file: {e}")
