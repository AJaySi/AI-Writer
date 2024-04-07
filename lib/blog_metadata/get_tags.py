import sys
import os

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


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
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to get response from LLM: {err}")
        raise err
