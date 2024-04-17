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


def llm_text_gen(prompt):
    """
    Generate text using Language Model (LLM) based on the provided prompt.
    Args:
        prompt (str): The prompt to generate text from.
    Returns:
        str: Generated text based on the prompt.
    """
    try:
        config_path = Path(__file__).resolve().parents[3] / "main_config"
        gpt_provider, model, temperature, max_tokens, top_p, n, fp = read_llm_parameters(config_path)

        gpt_provider = check_gpt_provider(gpt_provider)
        # Check if API key is provided for the given gpt_provider
        get_api_key(gpt_provider)

        # Perform text generation using the specified LLM parameters and prompt
        if 'google' in gpt_provider.lower():
            try:
                logger.info("Using Google Gemini Pro text generation model.")
                response = gemini_text_response(prompt, temperature, top_p, n, max_tokens)
                return response
            except Exception as err:
                logger.error(f"Failed to get response from gemini: {err}")
                raise err
        elif 'openai' in gpt_provider.lower():
            try:
                logger.info(f"Using OpenAI Model: {model} for text Generation.")
                response = openai_chatgpt(prompt, model, temperature, max_tokens, top_p, n, fp)
                return response
            except Exception as err:
                logger.error(f"Failed to get response from Openai: {err}")
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

    if not api_key:
        raise ValueError(f"No API key found for the specified GPT provider: '{gpt_provider}'")

    logger.info(f"Using API key for {gpt_provider}")
    return api_key



def read_llm_parameters(config_path: str) -> tuple:
    """
    Read Language Model (LLM) parameters from the configuration file.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        tuple: A tuple containing the LLM parameters (gpt_provider, model, temperature, max_tokens, top_p, n, frequency_penalty).

    Raises:
        FileNotFoundError: If the configuration file is not found.
        configparser.Error: If there is an error parsing the configuration file.
    """
    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")

        gpt_provider = config.get('llm_options', 'gpt_provider')
        model = config.get('llm_options', 'model')
        temperature = config.getfloat('llm_options', 'temperature')
        max_tokens = config.getint('llm_options', 'max_tokens')
        top_p = config.getfloat('llm_options', 'top_p')
        n = config.getint('llm_options', 'n')
        frequency_penalty = config.getfloat('llm_options', 'frequency_penalty')

        return gpt_provider, model, temperature, max_tokens, top_p, n, frequency_penalty

    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except configparser.Error as err:
        logger.error(f"Error reading LLM parameters from config file: {err}")
        raise
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise
