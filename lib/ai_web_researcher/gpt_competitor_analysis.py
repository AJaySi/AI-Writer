import sys

from ..gpt_providers.openai_text_gen import openai_chatgpt
from ..gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def summarize_competitor_content(research_content, gpt_providers="openai"):
    """Combine the given online research and gpt blog content"""

    prompt = f""" Web page content: {research_content} """

    if 'gemini' in gpt_providers:
        prompt = f"""You are a helpful assistant writing a research report about a company. I will provide you with company details. 
        Summarize the given company details into multiple paragraphs. 
        Be extremely concise, professional, and factual as possible. 
        The first paragraph should be an introduction and summary of the company. 
        The second paragraph should include pros and cons of the company.
        The third paragraph should be on their pricing model.
        Include a conclusion, summarizing your research about the given company details.
        Company details: '{research_content}'"""
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
