import sys

from ..gpt_providers.openai_chat_completion import openai_chatgpt
from ..gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def summarize_web_content(page_content, gpt_providers="openai"):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        Web page content: {page_content}
        """

    if 'gemini' in gpt_providers:
        prompt = f"""You are a helpful assistant that briefly summarizes the content of a webpage. 
            Summarize the given web page content below.
            Web page content: '{page_content}'"""
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error(f"Failed to get response from gemini: {err}")
            raise err
    elif 'openai' in gpt_providers:
        try:
            logger.info("Calling OpenAI LLM.")
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            logger.error(f"failed to get response from Openai: {err}")
            raise err
