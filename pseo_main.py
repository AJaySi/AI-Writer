#!/usr/bin/python3

"""
Main module for calling PSEO related functions. This is the end user interface and is user-driven.
Allows the user to specify various parameters for blog generation without needing to edit the code.
"""

import sys
import os
import argparse
import requests
from loguru import logger

# Logger configuration
logger.remove()
logger.add(sys.stdout, colorize=True, format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

# Importing custom functions
from lib.get_text_response import generate_detailed_blog, generate_youtube_blog


def parse_arguments():
    """Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Generate blogs based on user input.")
    parser.add_argument("--num_blogs", type=int, default=5, help="Number of blogs to generate (default: 5).")
    parser.add_argument("--keywords", type=str, help="Keywords for blog generation.")
    parser.add_argument("--niche", action='store_true', help="Flag to generate niche blogs (default: False).")
    parser.add_argument("--num_subtopics", type=int, default=6, help="Number of subtopics per blog (default: 6).")
    parser.add_argument("--youtube_urls", type=str, help="Comma-separated YouTube URLs for blog generation.")
    parser.add_argument("--wordpress", action='store_true', help="Flag to upload blogs to WordPress (default: False).")
    parser.add_argument("--output_format", choices=['plaintext', 'markdown', 'html'], default='plaintext', 
                        help="Output format of the blogs (default: plaintext).")

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
        if not args.keywords and not args.youtube_urls:
            raise ValueError("Either --keywords or --youtube_urls must be provided.")

        # Validate OpenAI API key
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key or not check_openai_api_key(openai_api_key):
            raise EnvironmentError("Invalid or missing OPENAI_API_KEY environment variable.")

        logger.info("Valid OpenAI API key found.")

        # Handle blog generation based on input
        if args.youtube_urls:
            yt_urls = args.youtube_urls.split(",")
            logger.info(f"Generating blogs from YouTube URLs: {yt_urls}")
            generate_youtube_blog(yt_urls, args.wordpress, args.output_format)
        elif args.keywords:
            logger.info(f"Generating {args.num_blogs} blogs on '{args.keywords}' with {args.num_subtopics} subtopics.")
            generate_detailed_blog(args.num_blogs, args.keywords, args.niche,
                    args.num_subtopics, args.wordpress, args.output_format)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
