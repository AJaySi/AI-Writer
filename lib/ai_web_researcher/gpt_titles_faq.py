import sys
import json

from ..gpt_providers.openai_chat_completion import openai_chatgpt
from ..gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


# FIXME: Provide num_blogs, num_faqs as inputs.
def gpt_titles_faqs_google_search(search_keyword, search_results, gpt_providers="openai"):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        As a SEO expert and content writer, I will provide you with my web research keyword and its google search result in json format.
        Your task is to write 1 blog title and 10 FAQs.
        
        1). Your blog title should compete against all the provided search results.
        2). Your FAQ should be based on 'People also ask' and 'Related Queries' from given result. 
        Always include answers for each FAQ, use your knowledge and confirm with snippets given in search result.
        3). Respond in json data with 'blogTitles' and 'FAQs' as json keys. Do not explain, describe your response.
        4). Follow best practises of SEO.

        Web Research Keyword: "{search_keyword}"
        Google search Result: "{search_results}"
        """
    logger.info("Generating blog title and FAQs from web search result.")
    if 'gemini' in gpt_providers:
        try:
            response = gemini_text_response(prompt)
            print(f"\n\n\n RESPONSE: {response}\n\n\n")
            if '```' in response and '\n' in response:
                response = response.strip().split('\n')
                # Remove the first and last lines
                response = '\n'.join(response[1:-1])
            response = json.loads(response)
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
            logger.error(f"Failed to get response from Openai: {err}")
            raise err
