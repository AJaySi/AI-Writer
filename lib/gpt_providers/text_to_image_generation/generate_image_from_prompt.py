#########################################################
#
# This module will generate images for the blogs using APIs
# from Dall-E and other free resources. Given a prompt, the
# images will be stored in local directory.
# Required: openai API key.
#
#########################################################

# imports
import sys
import datetime

import openai  # OpenAI Python library to make API calls
import os  # used to access filepaths
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

#from .gen_dali2_images
from .gen_dali3_images import generate_dalle3_images
from .gen_stabl_diff_img import generate_stable_diffusion_image


def generate_image(user_prompt, image_engine="dalle3"):
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
    img_prompt = generate_img_prompt(user_prompt) 
    # call the OpenAI API to generate image from prompt.
    logger.info(f"Calling image.generate with prompt: {img_prompt}")

    if 'Dalle3' in image_engine:
        image_stored_at = generate_dalle3_images(img_prompt)
    elif 'Stable Diffusion' in image_engine:
        image_stored_at = generate_stable_diffusion_image(img_prompt)

    return image_stored_at


def generate_img_prompt(user_prompt):
    """
    Given prompt, this functions generated a prompt for image generation.
    """
    # I want you to act as an artist advisor providing advice on various art styles such tips on utilizing 
    # light & shadow effects effectively in painting, shading techniques while sculpting etc.
    # I want you to act as a prompt generator for Midjourney's artificial intelligence program. 
    # Your job is to provide detailed and creative descriptions that will inspire unique and interesting images from the AI. 
    # Here is your first prompt: ""
    logger.info(f"Generate image prompt for : {user_prompt}")
    prompt = f"""As an educationist and expert infographic artist, your tasked to create prompts that will be used for image generation.
            Craft prompt for Openai Dall-e image generation program. Clearly describe the given text to represent it as image.
            Make sure to avoid common image generation mistakes. 
            Advice for creating prompt for image from the given text(no more than 150 words).
            Reply with only one answer and no descrition. Generate image prompt for the below text.
            Text: {user_prompt}"""
    response = (prompt)
    return response
