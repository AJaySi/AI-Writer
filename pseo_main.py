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

import json
import traceback
from loguru import logger
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")

from lib.generate_image_from_prompt import generate_image, gen_new_from_given_img
from lib.get_text_response import get_prompt_reply, generate_detailed_blog


try:
    logger.info("Starting homebrew pseo blog generator.")
    prompt = "Create a detailed and technical blog of best AI tools for text-to-video conversion in 2023, along with features, pricing, pros, cons, and website links and if free or paid version. Summarize this blog in conclusion at the end. Write in markdown."
    #txt_reply = get_prompt_reply(prompt, 2000)

    # The idea is to 
    #generate_image(logger)
    #gen_new_from_given_img(logger)

    # Generate detailed blog by only providing keywords from blog title.
    # Example: AI text to video tools
    generate_detailed_blog("text to video AI tools")

except Exception as err:
    #logger.exception(f"traceback.print_exc()")
    logger.error(f"Error occured in main::{err}")
