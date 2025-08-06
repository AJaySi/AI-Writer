import sys

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def summarize_web_content(page_content, gpt_providers="openai"):
    """Combine the given online research and gpt blog content"""

    prompt = f"""You are a helpful assistant that briefly summarizes the content of a webpage. 
            Summarize the given web page content below.
            Web page content: '{page_content}'"""
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"summarize_web_content: Failed to get response from LLM: {err}")
        raise err
