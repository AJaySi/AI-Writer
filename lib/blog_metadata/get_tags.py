import sys
import os

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../.env'))
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.openai_chat_completion import openai_chatgpt
from ..gpt_providers.gemini_pro_text import gemini_text_response


def get_blog_tags(blog_article):
    """
        Function to suggest tags for the given blog content
    """
    # Suggest at least 5 tags for the following blog post [Enter your blog post text here].
    gpt_providers = os.environ["GPT_PROVIDER"]
    prompt = f"""As an expert SEO and blog writer, suggest only 2 relevant and specific blog tags
         for the given blog content. Only reply with comma separated values. 
         Blog content:  {blog_article}."""
    logger.info("Generating Blog tags for the given blog post.")
    if 'google' in gpt_providers.lower():
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error("Failed to get response from gemini.")
    elif 'openai' in gpt_providers.lower():
        try:
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Error in generating blog summary: {err}") 
