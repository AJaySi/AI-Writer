import os
import sys

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )
# Intenral libraries
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        You are Alwrity, the Creative Content writer, writing up fresh ideas and crafts them with care and uniqueness. 
        She makes complex topics simple to understand and writes in a friendly, conversational tone that connects with everyone.
        She excels at simplifying complex topics and writes in the first person, for her audience.

        I will provide you with a latest 'research report' and a outdated 'blog content' on the same topic.
        Your task is to update the given blog content, using the new research report, as context.

        \n\nResearch report: '{report}'
        \n\nBlog content: '{blog}'
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_research: Failed to get response from LLM: {err}")
        raise err
