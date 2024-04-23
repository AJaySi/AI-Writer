#
# Common utils for lib
#
import os
import sys
import configparser
from pathlib import Path
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def read_return_config_section(config_section):
    """ read_return_config_section
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
        config_path = Path(__file__).resolve().parents[2] / "main_config"
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        
        if 'llm_config' in config_section:
	        gpt_provider = config.get('llm_options', 'gpt_provider')
	        model = config.get('llm_options', 'model')
	        temperature = config.getfloat('llm_options', 'temperature')
	        max_tokens = config.getint('llm_options', 'max_tokens')
	        top_p = config.getfloat('llm_options', 'top_p')
	        n = config.getint('llm_options', 'n')
	        frequency_penalty = config.getfloat('llm_options', 'frequency_penalty')
	
	        return gpt_provider, model, temperature, max_tokens, top_p, n, frequency_penalty
        elif 'blog_characteristics' in config_section:
            # Access and return the specified config values
            blog_tone = config.get('blog_characteristics', 'blog_tone')
            blog_demographic = config.get('blog_characteristics', 'blog_demographic')
            blog_type = config.get('blog_characteristics', 'blog_type')
            blog_language = config.get('blog_characteristics', 'blog_language')
            blog_output_format = config.get('blog_characteristics', 'blog_output_format')

            return blog_tone, blog_demographic, blog_type, blog_language, blog_output_format

    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except configparser.Error as err:
        logger.error(f"Error reading LLM parameters from config file: {err}")
        raise
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise
