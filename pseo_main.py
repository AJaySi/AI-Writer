#!/usr/bin/python3

"""
Main module for calling PSEO related functions. This is the end user interface and is user-driven.
Allows the user to specify various parameters for blog generation without needing to edit the code.
"""

import sys
import os
import re
import argparse
import requests
from loguru import logger
import csv
import json

# Logger configuration
logger.remove()
logger.add(sys.stdout, colorize=True, format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

# Importing custom functions
from lib.get_text_response import generate_detailed_blog, generate_youtube_blog
from lib.main_youtube_research_blog import generate_youtube_research_blog
from lib.main_keywords_to_blog import generate_keyword_blog
from lib.main_arxiv_to_blog import blog_arxiv_keyword, blog_arxiv_url_list


def parse_arguments():
    """Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    example_usage = """
    Example Usage:
    Keyword usage: python pseo_main.py --keywords "Writesonic AI SEO-optimized blog writing,PepperType AI virtual content assistant,Copysmith AI enterprise eCommerce content,Copy AI artificial intelligence content generator,Jasper AI creative content platform,Contents generative AI content strategy"
    YouTube usage: python pseo_main.py --youtube https://www.youtube.com/watch?v=yu27PWzJI_Y,https://www.youtube.com/watch?v=WGzoBD-xthI,https://www.youtube.com/watch?v=zizonToFXDs
    Scholar usage: python pseo_main.py --scholar "GPT-4 Technical Report"
    """

    parser = argparse.ArgumentParser(description="Generate blogs based on user input.", epilog=example_usage, formatter_class=argparse.RawDescriptionHelpFormatter)
    # Inputs csv, keywords, youtube_urls and scholar are mandatory.
    parser.add_argument("--csv", type=str, help="Provide path csv file. Check the template csv for example.")
    parser.add_argument("--keywords", type=str, help="Keywords for blog generation.")
    parser.add_argument("--youtube_urls", type=str, help="Comma-separated YouTube URLs for blog generation.")
    parser.add_argument("--scholar", type=str, help="Write blog from latest research papers on given keywords. Use 'arxiv_papers_url' to provide a file arxiv url list.")
    # Optional options.
    parser.add_argument("--niche", action='store_true', default=False, help="Flag to generate niche blogs (default: False).")
    parser.add_argument("--wordpress", action='store_true', default=False, help="Flag to upload blogs to WordPress (default: False).")
    # Add options for blog_tone and blog_personality.
    parser.add_argument("--output_format", choices=['plaintext', 'markdown', 'html'], default='markdown', help="Output format of the blogs (default: plaintext).")

    return parser.parse_args()


def check_openai_api_key(api_key):
    """Checks if the OpenAI API key is valid.

    Args:
        api_key (str): The OpenAI API key.

    Returns:
        bool: True if the key is valid, False otherwise.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.openai.com/v1/engines", headers=headers)
    return response.status_code == 200


def main():
    """Main function to handle blog generation based on user input."""
    try:
        args = parse_arguments()
        logger.info("Fetch and Validate Openai key.")
        # Validate user input
        if not args.keywords and not args.youtube_urls and not args.csv and not args.scholar:
            raise ValueError("Either --keywords, --youtube_urls, --csv Or --scholar must be provided.")

        # Validate OpenAI API key
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key or not check_openai_api_key(openai_api_key):
            raise EnvironmentError("Invalid or missing OPENAI_API_KEY environment variable.")

        logger.info("Valid OpenAI API key found.")

        # Handle blog generation based on input
        if args.youtube_urls:
            yt_urls = args.youtube_urls.split(",")
            valid_urls = [url for url in yt_urls if is_valid_url(url)]
            quoted_strings = [url for url in yt_urls if not is_valid_url(url)]

            if valid_urls:
                logger.info(f"Generating blogs from YouTube URLs: {valid_urls}")
                generate_youtube_blog(valid_urls)
            if quoted_strings:
                logger.info(f"Do youtube research and write blogs for: {quoted_strings}")
                generate_youtube_research_blog(quoted_strings)

        elif args.keywords:
            logger.info(f"Generating {args.num_blogs} blogs on '{args.keywords}' with {args.num_subtopics} subtopics.")
            #generate_detailed_blog(args.num_blogs, args.keywords, args.niche,
            #        args.num_subtopics, args.wordpress, args.output_format)
            keyword_list = args.keywords.split(",")
            generate_keyword_blog(keyword_list)

        elif args.csv:
            try:
                data = read_csv_to_json(args.csv)
                logger.info(f"Generating blogs from csv file: {json.dumps(data, indent=4)}")
                for item in data:
                    keyword_list = [item['keyword']]
                    generate_keyword_blog(keyword_list, item['URL'])
            except Exception as err:
                logger.error(f"Failed to generate blogs the CSV file:{err}")
                sys.exit(1)

        elif args.scholar:
            logger.info(f"Writing blog on {args.scholar} from research papers of arxiv, google & Semantic scholar.")
            # Write from arxiv urls given in a file.
            if 'arxiv_papers_url' in args.scholar:
                try:
                    logger.info(f"Writing scholar blogs from arxiv url list.")
                    blog_arxiv_url_list(args.scholar)
                except Exception as err:
                    logger.error(f"Failed to write from file {args.scholar} in present directory: {err}")
                    sys.exit(1)
            # Write scholar blogs from given keywords.
            else:
                try:
                    blog_arxiv_keyword(args.scholar)
                except Exception as err:
                    logger.error(f"Failed to write blog from research papers: {err}")
                    raise err

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


def read_csv_to_json(file_path):
    # Initialize a list to store JSON objects
    json_data = []

    try:
        # Read the CSV file
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Iterate over each row and convert it to a JSON object
            for row in reader:
                json_data.append(row)

        return json_data
    except Exception as err:
        logger.error(f"Failed to read the CSV file:{err}")
        sys.exit(1)


def is_valid_url(url):
    """
    Check if the given string is a valid URL.

    Args:
        url (str): String to check.

    Returns:
        bool: True if the string is a valid URL, False otherwise.
    """
    # Regular expression to check for a valid URL
    url_pattern = re.compile(     
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_pattern, url) is not None


if __name__ == "__main__":
    main()
