#!/usr/bin/python3

#########################################################
#
# This is the main module for calling pseo related functions.
# This is the end user interface and is user driven.
# TBD: argsparser and taking config file. For usuability,
# no editing of code should be required.
#
#########################################################
import sys
import os

import argparse
import json
import traceback
import requests
from loguru import logger
logger.remove()
logger.add(sys.stdout, 
        colorize=True, 
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from lib.generate_image_from_prompt import generate_image, gen_new_from_given_img
from lib.get_text_response import generate_detailed_blog


def main():
    """Parses user arguments and prints them to the console.

    Raises:
        TypeError: If the user input is not valid.
        ValueError: If the number of blogs is less than 1.
    """

    parser = argparse.ArgumentParser(
        description="Accepts user input for the number of blogs, subtopics, keywords, and niche."
    )
    parser.add_argument("--num_blogs", type=int, default=5, help="The number of blogs (default: 5).")
    parser.add_argument("--keywords", type=str, required=True, help="The keywords.A broad idea to write multiple blogs on.")
    parser.add_argument("--niche", type=bool, default=False, help="Written blogs on long tailed search topics (default: False).")
    parser.add_argument("--num_subtopics", type=int, default=6, help="The number of sub topics to write (default: 6).")

    args = parser.parse_args()

    # Check if the user input is valid
    if not isinstance(args.num_blogs, int) or not isinstance(args.keywords, str) or not isinstance(args.niche, bool):
        raise TypeError("Invalid: So, int, str, quotes should be present in command.")

    # Check if the number of blogs is less than 1
    if args.num_blogs < 1:
        raise ValueError("The number of blogs must be at least 1.")

    # Print the user input to the console
    logger.info(f"Number of blogs: {args.num_blogs}")
    logger.info(f"Keywords: {args.keywords}")
    logger.info(f"Niche blog: {args.niche}")

    return args

def check_openai_api_key(openai_api_key):
	"""Checks if the given OpenAI API key is valid and works.
	
	Args:
	    openai_api_key: The OpenAI API key to check.
	
	Returns:
	    True if the OpenAI API key is valid and works, False otherwise.
	"""
	
	headers = {
	    "Authorization": f"Bearer {openai_api_key}"
	    }
	
	# Make a test request to the OpenAI API.
	response = requests.get(
	    "https://api.openai.com/v1/engines",
	    headers=headers
	    )
	
	# If the request was successful, the API key is valid and works.
	return response.status_code == 200


if __name__ == "__main__":
    # Check if we have everything, we need to start writing blogs.
     """Checks for the OPENAI_API_KEY environment variable, if it is not exported or if it is not valid."""
     openai_api_key = os.environ.get("OPENAI_API_KEY")
     if not openai_api_key:
         logger.error("Error: Please    export OPENAI_API_KEY=''  - before running this script.")
         exit(1)
     # Check if the OpenAI API key is valid.
     if not check_openai_api_key(openai_api_key):
         logger.error("The OPENAI_API_KEY not valid. Check your API key and make sure its correct.")
         exit(1)
     # The OpenAI API key is valid and works.
     logger.info("The OPENAI_API_KEY environment variable is valid and works.")

     try:
         args = main()
     except TypeError as e:
         logger.error(e)
     except ValueError as e:
         logger.error(e)
     else:
         logger.info(f"Writing {args.num_blogs} blogs on '{args.keywords}' with {args.num_subtopics} subtopics.")
         generate_detailed_blog(args.num_blogs, args.keywords, args.niche, args.num_subtopics) 
