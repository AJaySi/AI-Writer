import os
import sys
import configparser
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../.env'))

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from .openai_text_gen import openai_chatgpt
from .gemini_pro_text import gemini_text_response
from .anthropic_text_gen import anthropic_text_response
from ...utils.read_main_config_params import read_return_config_section


def llm_text_gen(prompt):
    """
    Generate text using Language Model (LLM) based on the provided prompt.
    Args:
        prompt (str): The prompt to generate text from.
    Returns:
        str: Generated text based on the prompt.
    """
    try:
        # Read the config param to create system instruction for the LLM.
        gpt_provider, model, temperature, max_tokens, top_p, n, fp = read_return_config_section('llm_config')
        blog_tone, blog_demographic, blog_type, blog_language, \
            blog_output_format, blog_length = read_return_config_section('blog_characteristics')

        # Construct the system prompt with the sidebar config params.
        system_instructions = f"""
        Below are the guidelines to follow:
        1). You must respond in {blog_language} language.
        2). Tone and Brand Alignment: Adjust your tone, voice, personality for {blog_tone} audience.
        3). Make sure your response content length is of {blog_length} words.
        4). The type of blog is {blog_type}, write accordingly.
        5). The demographic for this content is {blog_demographic}.
        6). Your response should be in {blog_output_format} format.
        """

        #gpt_provider = check_gpt_provider(gpt_provider)
        # Check if API key is provided for the given gpt_provider
        get_api_key(gpt_provider)

        # Perform text generation using the specified LLM parameters and prompt
        if 'google' in gpt_provider.lower():
            try:
                logger.info("Using Google Gemini Pro text generation model.")
                response = gemini_text_response(prompt, temperature, top_p, n, max_tokens, system_instructions)
                return response
            except Exception as err:
                logger.error(f"Failed to get response from gemini: {err}")
                raise err
        elif 'openai' in gpt_provider.lower():
            try:
                logger.info(f"Using OpenAI Model: {model} for text Generation.")
                response = openai_chatgpt(prompt, model, temperature, max_tokens, top_p, n, fp, system_instructions)
                return response
            except Exception as err:
                logger.error(f"Failed to get response from Openai: {err}")
                raise err
        elif 'anthropic' in gpt_provider.lower():
            try:
                logger.info(f"Using Anthropic Model: {model} for text Generation.")
                response = anthropic_text_response(prompt)
                return response
            except Exception as err:
                logger.error(f"Failed to get response from Anthropic: {err}")
                raise err

    except Exception as err:
        logger.error(f"Failed to read LLM parameters: {err}")
        raise


def check_gpt_provider(gpt_provider):
    """
    Check if the specified GPT provider matches the environment variable GPT_PROVIDER,
    assign and export the GPT_PROVIDER value from the config file if missing,
    and continue.

    Args:
        gpt_provider (str): The specified GPT provider.

    Raises:
        ValueError: If both the specified GPT provider and environment variable GPT_PROVIDER are missing.
    """
    env_gpt_provider = os.getenv('GPT_PROVIDER')
    if gpt_provider and gpt_provider.lower() != env_gpt_provider.lower():
        logger.warning(f"Config: '{gpt_provider}' different to environment variable 'GPT_PROVIDER' '{env_gpt_provider}'")
        gpt_provider = env_gpt_provider

    return gpt_provider



def get_api_key(gpt_provider):
    """
    Get the API key for the specified GPT provider.

    Args:
        gpt_provider (str): The specified GPT provider.

    Returns:
        str: The API key for the specified GPT provider.

    Raises:
        ValueError: If no API key is found for the specified GPT provider.
    """
    api_key = None

    if gpt_provider.lower() == 'google':
        api_key = os.getenv('GEMINI_API_KEY')
    elif gpt_provider.lower() == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
    elif gpt_provider.lower() == 'anthropic':
        api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        raise ValueError(f"No API key found for the specified GPT provider: '{gpt_provider}'")

    logger.info(f"Using API key for {gpt_provider}")
    return api_key
