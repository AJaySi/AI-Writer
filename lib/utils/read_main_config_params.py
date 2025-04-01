import os
import sys
import json
from pathlib import Path
from loguru import logger
import yaml

logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


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
        
        if config_section == 'system_prompt':
            prompt_file_path = os.path.join(os.getcwd(), 'lib', 'workspace', 'alwrity_prompts', 'alwrity_system_instruction.prompts')
            with open(prompt_file_path, 'r') as file:
                content = file.read()
            return content

        elif config_section == 'llm_config':
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

def get_personalization_settings():
    """Get personalization settings from ALWRITY_CONFIG."""
    try:
        config_path = Path(os.environ["ALWRITY_CONFIG"])
        config = yaml.safe_load(config_path.read_text())
        return config.get('personalization', {})
    except Exception as e:
        logger.error(f"Error reading personalization settings: {str(e)}")
        return {}

def save_personalization_settings(settings):
    """Save personalization settings to ALWRITY_CONFIG."""
    try:
        config_path = Path(os.environ["ALWRITY_CONFIG"])
        config = yaml.safe_load(config_path.read_text())
        
        # Update personalization section
        config['personalization'] = settings
        
        # Save back to file
        config_path.write_text(yaml.dump(config, default_flow_style=False))
        logger.info("Personalization settings saved successfully")
        
    except Exception as e:
        logger.error(f"Error saving personalization settings: {str(e)}")
        raise
