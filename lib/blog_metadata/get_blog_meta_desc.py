import sys
import os

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def generate_blog_description(blog_content):
    """
        Prompt designed to give SEO optimized blog descripton
    """
    logger.info("Generating Blog Meta Description for the given blog.")
    prompt = f"""As an expert SEO and blog writer, Compose a compelling meta description for the given blog content, 
        adhering to SEO best practices. Keep it between 150-160 characters. 
        Provide a glimpse of the content's value to entice readers.
        Respond with only one of your best effort and do not include your explanations. 
        Blog Content: '{blog_content}'"""

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to get response from LLM:{err}")
        raise err
