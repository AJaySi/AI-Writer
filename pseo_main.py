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

import argparse
import json
import traceback
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
        description="Accepts user input for the number of blogs, keywords, and niche."
    )
    parser.add_argument("--num_blogs", type=int, default=1, help="The number of blogs (default: 5).")
    parser.add_argument("--keywords", type=str, required=True, help="The keywords.A broad idea to write multiple blogs on.")
    parser.add_argument("--niche", type=bool, default=False, help="Written blogs on long tailed search topics (default: False).")

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

    return args.num_blogs, args.keywords, args.niche


if __name__ == "__main__":
    # Check if we have everything, we need to start writing blogs.
    try:
        num_blogs, keywords, niche = main()
        logger.info(f"returned value: {num_blogs} {keywords}")
    except TypeError as e:
        logger.error(e)
    except ValueError as e:
        logger.error(e)
    else:
        logger.info(f"Starting to write {num_blogs} blogs on {keywords}")
        generate_detailed_blog(num_blogs, keywords, niche)
