import os
import json
from pathlib import Path

def read_return_config_section(config_section):
    """ read_return_config_section
    Read configuration parameters from the JSON configuration file.

    Args:
        config_section (str): The section of the configuration file to read.

    Returns:
        tuple: A tuple containing the specified configuration parameters.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If there is an error parsing the JSON configuration file.
    """
    try:
        config_path = Path(os.environ["ALWRITY_CONFIG"])
        
        with open(config_path, 'r', encoding="utf-8") as file:
            config = json.load(file)
        
        if config_section == 'llm_config':
            gpt_provider = config['LLM Options']['GPT Provider']
            model = config['LLM Options']['Model']
            temperature = config['LLM Options']['Temperature']
            max_tokens = config['LLM Options']['Max Tokens']
            top_p = config['LLM Options']['Top-p']
            n = config['LLM Options']['N']
            frequency_penalty = config['LLM Options']['Frequency Penalty']
            presence_penalty = config['LLM Options']['Presence Penalty']
            
            return gpt_provider, model, temperature, max_tokens, top_p, n, frequency_penalty

        elif config_section == 'blog_characteristics':
            blog_tone = config['Blog Content Characteristics']['Blog Tone']
            blog_demographic = config['Blog Content Characteristics']['Blog Demographic']
            blog_type = config['Blog Content Characteristics']['Blog Type']
            blog_language = config['Blog Content Characteristics']['Blog Language']
            blog_output_format = config['Blog Content Characteristics']['Blog Output Format']
            blog_length = config['Blog Content Characteristics']['Blog Length']

            return blog_tone, blog_demographic, blog_type, blog_language, blog_output_format, blog_length

        elif config_section == 'web_research':
            geo_location = config['Search Engine Parameters']['Geographic Location']
            search_language = config['Search Engine Parameters']['Search Language']
            num_results = config['Search Engine Parameters']['Number of Results']
            time_range = config['Search Engine Parameters']['Time Range']
            include_domains = config['Search Engine Parameters']['Include Domains']
            similar_url = config['Search Engine Parameters']['Similar URL']

            return geo_location, search_language, num_results, time_range, include_domains, similar_url

    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Error reading parameters from config file: {err}")
        raise
    except KeyError as err:
        logger.error(f"Missing key in the configuration file: {err}")
        raise
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        raise
