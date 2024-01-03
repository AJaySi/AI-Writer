import sys

from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def generate_blog_title(blog_article, gpt_providers="openai"):
    """
    Given a blog title generate an outline for it
    """
    logger.info("Generating blog title.")
    prompt = f"""As a SEO expert, I will provide you with a blog content. 
        Your task is write a SEO optimized, call to action and engaging blog title for it.
        Follows SEO best practises to suggest the blog title. 
        Please keep the titles concise, not exceeding 60 words. 
        Respond with only one title and no explanations. 
        Important: Your response should be in plaintext.
        Generate blog title for this given blog content:\n '{blog_article}' """

    if 'gemini' in gpt_providers:
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error(f"Failed to get response from gemini: {err}") 
    elif 'openai' in gpt_providers:
        try:
            logger.info("Calling OpenAI LLM.")
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Error in generating blog summary: {err}") 
