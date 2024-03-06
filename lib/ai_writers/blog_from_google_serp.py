import os
import sys
import json
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


# FIXME: Provide num_blogs, num_faqs as inputs.
def write_blog_google_serp(search_keyword, search_results):
    """Combine the given online research and gpt blog content"""
    gpt_providers = os.environ["GPT_PROVIDER"]
    prompt = f"""
        As a SEO expert and content writer, I will provide you with my web research keyword and its google search result in json format.
        Your task is to write a SEO optimized, unique blog and 5 FAQs.
        
        1). Your blog content should compete against all, in the provided search results. Follow best SEO practises.
        2). Your FAQ should be based on 'People also ask' and 'Related Queries' from given result. 
        Always include answers for each FAQ, use your knowledge and confirm with snippets given in search result.
        3). Your blog should be detailed, unique and written in markdown language.
        4). Do not explain, describe your response.

        Web Research Keyword: "{search_keyword}"
        Google search Result: "{search_results}"
        """
    logger.info("Generating blog and FAQs from web search result.")
    if 'google' in gpt_providers.lower():
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
            logger.error(f"Failed to get response from Openai: {err}")
            raise err
