# Common utils for web_researcher
import os
import sys
import re
import configparser
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def cfg_search_param(flag):
    """
    Read values from the main_config file and return them as variables and a dictionary.

    Args:
        file_path (str): The path to the main_config file.

    Returns:
        dict: A dictionary containing the values read from the config file.
        str: The geographic location value.
        str: The search language value.
        int: The number of search results to fetch.
    """
    try:
        file_path = Path(__file__).resolve().parents[2] / "main_config"
        logger.info(f"Reading search config params from {file_path}")
        config = configparser.ConfigParser()
        config.read(file_path, encoding="utf-8")
        web_research_section = config["web_research"]

        if 'serperdev' in flag:
            # Get values as variables
            geo_location = web_research_section.get("geo_location")
            search_language = web_research_section.get("search_language")
            num_results = web_research_section.getint("num_results")
            return geo_location, search_language, num_results

        elif 'tavily' in flag:
            include_urls = web_research_section.get("include_domains")
            pattern = re.compile(r"^(https?://[^\s,]+)(,\s*https?://[^\s,]+)*$")
            if pattern.match(include_urls):
                include_urls = [url.strip() for url in include_urls.split(',')]
            else:
                include_urls = None
            return include_urls

        elif 'exa' in flag:
            include_urls = web_research_section.get("include_domains")
            pattern = re.compile(r"^(https?://\w+)(,\s*https?://\w+)*$")
            if pattern.match(include_urls) is not None:
                include_urls = include_urls.split(',')
            elif re.match(r"^http?://\w+$", include_urls) is not None:
                include_urls = include_urls.split(" ")
            else:
                include_urls = None

            num_results = web_research_section.getint("num_results")
            similar_url = web_research_section.get("similar_url")
            time_range = web_research_section.get("time_range")
            if time_range == "past day":
                start_published_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            elif time_range == "past week":
                start_published_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            elif time_range == "past month":
                start_published_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            elif time_range == "past year":
                start_published_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            elif time_range == "anytime" or not time_range:
                start_published_date = None
            time_range = start_published_date
            return include_urls, time_range, num_results, similar_url

    except FileNotFoundError:
        logger.error(f"Error: Config file '{file_path}' not found.")
        return {}, None, None, None
    except KeyError as e:
        logger.error(f"Error: Missing section or option in config file: {e}")
        return {}, None, None, None
    except ValueError as e:
        logger.error(f"Error: Invalid value in config file: {e}")
        return {}, None, None, None


def save_in_file(table_content):
    """ Helper function to save search analysis in a file. """
    file_path = os.environ.get('SEARCH_SAVE_FILE')
    try:
        # Save the content to the file
        with open(file_path, "a+", encoding="utf-8") as file:
            file.write(table_content)
            file.write("\n" * 3)  # Add three newlines at the end
        logger.info(f"Search content saved to {file_path}")
    except Exception as e:
        logger.error(f"Error occurred while writing to the file: {e}")
