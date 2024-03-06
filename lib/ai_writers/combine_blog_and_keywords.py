import os
import sys

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../.env'))

from ..gpt_providers.openai_chat_completion import openai_chatgpt
from ..gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def blog_with_keywords(blog, keywords):
    """Combine the given online research and gpt blog content"""
    gpt_providers = os.environ["GPT_PROVIDER"]
    prompt = f"""
        You are an expert copywriter specializing in content optimization for SEO. 
        I will provide you with my 'blog content' and 'list of keywords' on the same topic.
        Your task is to write an original blog, using given keywords and blog content.
        Your blog should be highly detailed and well formatted. 
        Do not miss out any details from provided blog content. 

        Blog content: '{blog}'
        list of keywords: '{keywords}'
        """

    if 'google' in gpt_providers.lower():
        prompt = f"""You are an expert copywriter specializing in content optimization for SEO. 
        I will provide you with my 'blog content' and 'list of keywords' on the same topic.
        Your task is to write an original blog, using the given keywords and blog content.
        Your blog should be highly detailed and well formatted. 
        Do not miss out any details from provided blog content. 
        Always, include figures, data, results from given content.
        It is important that your blog is original and unique. It should be highly readable and SEO optimized.

        Blog content: '{blog}'
        list of keywords: '{keywords}'
        """
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error(f"Failed to get response from gemini: {err}")
            raise err
    elif 'openai' in gpt_providers.lower():
        try:
            logger.info("Calling OpenAI LLM.")
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            logger.error(f"failed to get response from Openai: {err}")
            raise err
