# Using Gemini Pro LLM model
import os
import sys
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv(Path('../../../.env'))
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt, temperature, top_p, n, max_tokens):
    """ Common functiont to get response from gemini pro Text. """
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    except Exception as err:
        logger.error(f"Failed to configure Gemini: {err}")
    logger.info(f"Temp: {temperature}, MaxTokens: {max_tokens}, TopP: {top_p}, N: {n}")
    # Set up the model
    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": n,
        "max_output_tokens": max_tokens
    }
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            print(chunk.text)
        return response.text
    except Exception as err:
        logger.error(response)
        logger.error(f"Failed to get response from Gemini: {err}. Retrying.")
