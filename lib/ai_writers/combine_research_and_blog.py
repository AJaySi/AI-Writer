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

        I will provide you with a 'research report' and a 'blog content' on the same topic.
        Your task is to follow below given guidelines to write a detailed blog article,
        that will rank well in search engine results and engage readers effectively.

        Follow below given guidelines:
        1. Master the report and blog content: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and conversational tone.
        3. Identify Main Keywords: Determine the primary topic and combine the articles on that main topic.
        5. Blog Structuring: Include an Introduction, subtopics and use bullet points or
        numbered lists if appropriate. Important to include FAQs, Conclusion and Referances.
        7. .\n\n

        Research report: '{report}'
        Blog content: '{blog}'
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_research: Failed to get response from LLM: {err}")
        raise err
