# Common utils for web_researcher
import os
import sys
import re
import json
from pathlib import Path
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
    Read values from the main_config.json file and return them as variables and a dictionary.

    Args:
        flag (str): A flag to determine which configuration values to return.

    Returns:
        various: The values read from the config file based on the flag.
    """
    try:
        file_path = Path(os.environ.get("ALWRITY_CONFIG", ""))
        if not file_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        logger.info(f"Reading search config params from {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        web_research_section = config["Search Engine Parameters"]

        if 'serperdev' in flag:
            # Get values as variables
            geo_location = web_research_section.get("Geographic Location")
            search_language = web_research_section.get("Search Language")
            num_results = web_research_section.get("Number of Results")
            return geo_location, search_language, num_results

        elif 'tavily' in flag:
            include_urls = web_research_section.get("Include Domains")
            pattern = re.compile(r"^(https?://[^\s,]+)(,\s*https?://[^\s,]+)*$")
            if pattern.match(include_urls):
                include_urls = [url.strip() for url in include_urls.split(',')]
            else:
                include_urls = None
            return include_urls

        elif 'exa' in flag:
            include_urls = web_research_section.get("Include Domains")
            pattern = re.compile(r"^(https?://\w+)(,\s*https?://\w+)*$")
            if pattern.match(include_urls) is not None:
                include_urls = include_urls.split(',')
            elif re.match(r"^http?://\w+$", include_urls) is not None:
                include_urls = include_urls.split(" ")
            else:
                include_urls = None

            num_results = web_research_section.get("Number of Results")
            similar_url = web_research_section.get("Similar URL")
            time_range = web_research_section.get("Time Range")
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
        return file_path
    except Exception as e:
        logger.error(f"Error occurred while writing to the file: {e}")
