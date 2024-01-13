# Using Gemini Pro LLM model
import os
import logging
from pathlib import Path

import google.generativeai as genai
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(module)s-%(lineno)d-%(message)s')
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))
from .mistral_chat_completion import mistral_text_response

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt):
    """ Common functiont to get response from gemini pro Text. """
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

    # Set up the model
    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 6096,
    }

    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
    try:
        response = model.generate_content(prompt)

    except Exception as err:
        logger.error(f"Failed to get response from Gemini: {err}. Retrying.")
        # Try with minstral.
        print(f"\n\n\n--MINSTRAL--\n\n\n\n")
        response = mistral_text_response(prompt)
        return response
    return response.text
