########################################################################
#
# Common module for getting response from gpt for given prompt.
# This module includes following capabilities:
# 
#
#
########################################################################

import json
import os
import datetime #I wish
import sys
import time

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

# Load configuration
#with open('config.json') as config_file:
#    config = json.load(config_file)

#wordpress_url = config['wordpress_url']
# fixme: Remove the hardcoding, need add another option OR in config ?
image_dir = "blog_images"
image_dir = os.path.join(os.getcwd(), image_dir)
# TBD: This can come from config file.
output_path = "blogs"
output_path = os.path.join(os.getcwd(), output_path)
wordpress_url = ''
wordpress_username = ''
wordpress_password = ''

