#########################################################
#
# This module will generate images for the blogs using APIs
# from Dall-E and other free resources. Given a prompt, the
# images will be stored in local directory.
# Required: openai API key.
#
#########################################################

# imports
import os
import sys
import datetime
import streamlit as st

import openai  # OpenAI Python library to make API calls
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

#from .gen_dali2_images
from .gen_dali3_images import generate_dalle3_images
from .gen_stabl_diff_img import generate_stable_diffusion_image
from ..text_generation.main_text_generation import llm_text_gen
from .gen_gemini_images import generate_gemini_image

def generate_image(user_prompt):
    """
    The generation API endpoint creates an image based on a text prompt.

    Required inputs:
    prompt (str): A text description of the desired image(s). The maximum length is 1000 characters.

    Optional inputs:
    --> image_engine: dalle2, dalle3, stable diffusion are supported.
    --> num_images (int): The number of images to generate. Must be between 1 and 10. Defaults to 1.
    --> size (str): The size of the generated images. Must be one of "256x256", "512x512", or "1024x1024". 
    Smaller images are faster. Defaults to "1024x1024".
    -->response_format (str): The format in which the generated images are returned. 
    Must be one of "url" or "b64_json". Defaults to "url".
    --> user (str): A unique identifier representing your end-user, which will help OpenAI to monitor and detect abuse.
    """
    # FIXME: Need to remove default value to match sidebar input.
    image_engine = 'Gemini-AI'
    image_stored_at = None

    if user_prompt:
        try:
            img_prompt = generate_img_prompt(user_prompt)
            if 'Dalle3' in image_engine:
                logger.info(f"Calling Dalle3 text-to-image with prompt: {img_prompt}")
                image_stored_at = generate_dalle3_images(img_prompt)
            elif 'Stability-AI' in image_engine:
                logger.info(f"Calling Stable diffusion text-to-image with prompt: \n{img_prompt}")
                image_stored_at = generate_stable_diffusion_image(img_prompt)
            elif 'Gemini-AI' in image_engine:
                logger.info(f"Calling Gemini text-to-image with prompt: \n{img_prompt}")
                image_stored_at = generate_gemini_image(img_prompt)
            return image_stored_at
        except Exception as err:
            logger.error(f"Failed to generate Image: {err}")
            st.warning(f"Failed to generate Image: {err}")
    else:
        logger.error("Skipping Image creation, No prompt provided.")


def generate_img_prompt(user_prompt):
    """
    Given prompt, this functions generated a prompt for image generation.
    """
    prompt = f"""
        As an expert prompt generator for AI text to image models and artist, I will provide you with 'user text' for creating images.
        Your task is to create a prompt for a highly relevant image from given 'user text'.
        \n
        Choose from various art styles, utilize light & shadow effects etc.
        Make sure to avoid common image generation mistakes.
        Reply with only one answer, no descrition and in plaintext.
        Make sure your prompt is detailed and creative descriptions that will inspire unique and interesting images from the AI. 
        
        \n\nuser text:  
        '''{user_prompt}'''"""

    response = llm_text_gen(prompt)
    return response
