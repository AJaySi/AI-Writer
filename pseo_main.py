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
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

from lib.generate_image_from_prompt import generate_image, gen_new_from_given_img
from lib.get_text_response import get_prompt_reply, generate_detailed_blog


def main():
    """Parses user arguments and prints them to the console.

    Raises:
        TypeError: If the user input is not valid.
        ValueError: If the number of blogs is less than 1.
    """

    parser = argparse.ArgumentParser(
        description="Accepts user input for the number of blogs, keywords, and niche."
    )
    parser.add_argument("--num_blogs", type=int, default=1, help="The number of blogs (default: 1).")
    parser.add_argument("--keywords", type=str, required=True, help="The keywords.")
    parser.add_argument("--niche", type=bool, default=False, help="Whether the blog is a niche blog (default: False).")

    args = parser.parse_args()

    # Check if the user input is valid
    if not isinstance(args.num_blogs, int) or not isinstance(args.keywords, str) or not isinstance(args.niche, bool):
        raise TypeError("Invalid user input.")

    # Check if the number of blogs is less than 1
    if args.num_blogs < 1:
        raise ValueError("The number of blogs must be at least 1.")

    # Print the user input to the console
    print(f"Number of blogs: {args.num_blogs}")
    print(f"Keywords: {args.keywords}")
    print(f"Niche blog: {args.niche}")

    return args.num_blogs, args.keywords, args.niche


if __name__ == "__main__":
    # Check if we have everything, we need to start writing blogs.
    try:
        num_blogs, keywords, niche = main()
        print(f"returned value: {num_blogs} {keywords}")
    except TypeError as e:
        print(e)
    except ValueError as e:
        print(e)
    else:
        print(f"Starting to write {num_blogs} on {keywords}")
        generate_detailed_blog(num_blogs, keywords, niche)
