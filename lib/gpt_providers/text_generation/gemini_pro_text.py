# Using Gemini Pro LLM model
import os
import sys
from pathlib import Path

import google.generativeai as genai
from google.api_core import retry
from dotenv import load_dotenv
load_dotenv(Path('../../../.env'))
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def gemini_text_response(prompt, temperature, top_p, n, max_tokens):
    """ Common functiont to get response from gemini pro Text. """
    #FIXME: Include : https://github.com/google-gemini/cookbook/blob/main/quickstarts/rest/System_instructions_REST.ipynb
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
    # FIXME: Expose model_name in main_config
    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)
    try:
        # text_response = []
        response = model.generate_content(prompt, stream=True, request_options={'retry':retry.Retry()})
        for chunk in response:
            # text_response.append(chunk.text)
            print(chunk.text)
        return response.text
    except Exception as err:
        logger.error(response)
        logger.error(f"Failed to get response from Gemini: {err}. Retrying.")
