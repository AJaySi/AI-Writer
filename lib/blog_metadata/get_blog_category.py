import sys
import os

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def get_blog_categories(blog_article):
    """
    Function to generate blog categories for given blog content.
    """
    prompt = f"""As an expert SEO and content writer, I will provide you with blog content.
            Suggest only 2 blog categories which are most relevant to provided blog content,
            by identifying the main topic. Also consider the target audience and the
            blog's category taxonomy. Only reply with comma separated values. 
            The blog content is: '{blog_article}'"
    """
    logger.info("Generating blog categories for the given blog.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"get_blog_categories:Failed to get response from LLM: {err}")
