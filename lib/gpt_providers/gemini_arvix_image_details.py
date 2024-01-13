"""
"""
import os
import logging
from pathlib import Path

import google.generativeai as genai
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(module)s-%(lineno)d-%(message)s')
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
) # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_arxiv_img_info(img_path):
    """ Get image details from arxiv papers. """
    try:
        genai.configure(api_key=os.getenv("API_KEY"))
    except Exception as e:
        logging.error(f"Could not load gemini API key: {e}")
        raise e

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 1096,
    }

    safety_settings = [{
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },]

    try:
        model = genai.GenerativeModel(model_name="gemini-pro-vision",
            generation_config=generation_config,
            safety_settings=safety_settings)
    except Exception as e:
        logging.error(f"Could not create GenerativeModel: {e}")
        raise e

    # Validate that an image is present
    if not (img := Path(img_path)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [{
        "mime_type": "image/png",
        "data": Path(img_path).read_bytes()
    },]

    prompt_parts = [
        "As scholar on evaluating research papers, I will provide you with an image from a research paper. Your task is to explain the image in details so that I can use it in a blog article. Explain the key findings and conclusions from the image. Your description should be in simple terms to explain to a wider audience. Explain key findings from the given image.",
        image_parts[0],]

    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        logging.error(f"Could not generate gemini content: {e}")
        raise e
