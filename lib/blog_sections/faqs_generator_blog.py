import sys

from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def generate_blog_faq(blog_article, gpt_providers="openai"):
    """
    Given a blog title generate an outline for it
    """
    logger.info("Generating blog FAQs.")
    prompt = f"""As an expert writer, I will provide you with blog content below. 
    Your task is to write 5 FAQs based on the given blog content.
    Always, write fact based answers. Use emojis where applicable.
    You must reply in MARKDOWN format.
    blog content: '{blog_article}' """

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
            SystemError(f"Failed to get response from Openai: {err}") 
