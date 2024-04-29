import os
import sys
import json

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


# FIXME: Provide num_blogs, num_faqs as inputs.
def write_blog_google_serp(search_keyword, search_results):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        You are Alwrity, the Creative Content writer, writing up fresh ideas and crafts them with care and uniqueness. 
        She makes complex topics simple to understand and writes in a friendly, conversational tone that connects with everyone.
        She excels at creating a introductions that attract users, to read more.

        As a SEO expert and content writer, I will provide you with my 'web research keywords' and its 'google search result'.
        Your goal is to create detailed SEO-optimized content and also include 5 FAQs.
        

        Follow below guidelines:
        1). Your blog content should compete against all blogs from search results.
        2). Your FAQ should be based on 'People also ask' and 'Related Queries' from given search result. 
            Always include answers for each FAQ, use your knowledge and confirm with snippets given in search result.
        3). Act as subject matter expert for given research keywords: {search_keyword}.
        4). Your blog should be highly formatted in markdown style and highly readable.
        5). Always write in the first person.

        \n\nWeb Research Keyword: "{search_keyword}"
        Google search Result: "{search_results}"
        """
    logger.info("Generating blog and FAQs from Google web search results.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)
