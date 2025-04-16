import os
import sys
import json
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
from .gemini_pro_text import gemini_text_response, gemini_structured_json_response
from .anthropic_text_gen import anthropic_text_response
from .deepseek_text_gen import deepseek_text_response 
from ...utils.read_main_config_params import read_return_config_section


def llm_text_gen(prompt, system_prompt=None, json_struct=None):
    """
    Generate text using Language Model (LLM) based on the provided prompt.
    Args:
        prompt (str): The prompt to generate text from.
        system_prompt (str, optional): Custom system prompt to use instead of the default one.
        json_struct (dict, optional): JSON schema structure for structured responses.
    Returns:
        str: Generated text based on the prompt.
    """
    try:
        logger.info("[llm_text_gen] Starting text generation")
        logger.debug(f"[llm_text_gen] Prompt length: {len(prompt)} characters")
        
        try:
            # Read the config param to create system instruction for the LLM.
            gpt_provider, model, temperature, max_tokens, top_p, n, fp = read_return_config_section('llm_config')
            blog_tone, blog_demographic, blog_type, blog_language, \
            blog_output_format, blog_length = read_return_config_section('blog_characteristics')
            
            logger.debug(f"[llm_text_gen] Config loaded successfully - Provider: {gpt_provider}, Model: {model}")
            
        except Exception as err:
            logger.error(f"[llm_text_gen] Error reading config params: {err}")
            raise err

        # Construct the system prompt with the sidebar config params if no custom system_prompt is provided
        if system_prompt is None:
            system_instructions = f"""You are a highly skilled content writer with a knack for creating engaging and informative content. 
                Your expertise spans various writing styles and formats.

                Here's a breakdown of the instructions for this writing task:

                **Content Guidelines:**

                1. **Language:** Your response must be in **{blog_language}** language. 
                2. **Tone and Brand Alignment:** Adjust your tone, voice, and personality to be appropriate for a **{blog_tone}** audience. 
                3. **Content Length:**  Ensure your response is approximately **{blog_length}** words in length.
                4. **Blog Type:**  The type of blog is **{blog_type}**. Write accordingly, adhering to the conventions and expectations of this type of content.
                5. **Target Audience:** The demographic for this content is **{blog_demographic}**. Keep their interests and needs in mind.
                6. **Output Format:** Your response should be in **{blog_output_format}** format. This could be Markdown, HTML, or a specific structured format, depending on the user's preference.

                **Additional Instructions:**

                *  **SEO Optimization:**  Incorporate relevant keywords naturally throughout the content to improve its search engine visibility.
                * **Call to Action:** Include a call to action if appropriate for the blog type and target audience.
                * **Factual Accuracy:**  Ensure your content is accurate and reliable. Back up any claims with credible sources.
                * **Unique Voice and Style:** Inject your unique voice and writing style to make the content engaging and memorable. """
        else:
            system_instructions = system_prompt
            logger.info("[llm_text_gen] Using custom system prompt")
        
        # Check if API key is provided for the given gpt_provider
        get_api_key(gpt_provider)

        # Perform text generation using the specified LLM parameters and prompt
        if 'google' in gpt_provider.lower():
            try:
                logger.info("Using Google Gemini Pro text generation model.")
                if json_struct:
                    response = gemini_structured_json_response(prompt, json_struct, temperature, top_p, n, max_tokens, system_instructions)
                else:
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
                response = anthropic_text_response(prompt, model, temperature, max_tokens, top_p, n, system_instructions)
                return response
            except Exception as err:
                logger.error(f"Failed to get response from Anthropic: {err}")
                raise err
        elif 'deepseek' in gpt_provider.lower():
            try:
                logger.info(f"Using DeepSeek Model: {model} for text Generation.")
                response = deepseek_text_response(prompt, model, temperature, max_tokens, top_p, n, system_instructions)
                return response
            except Exception as err:
                logger.error(f"Failed to get response from DeepSeek: {err}")
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
    elif gpt_provider.lower() == 'deepseek':
        api_key = os.getenv('DEEPSEEK_API_KEY')

    if not api_key:
        raise ValueError(f"No API key found for the specified GPT provider: '{gpt_provider}'")

    logger.info(f"Using API key for {gpt_provider}")
    return api_key
