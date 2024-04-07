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
        You are an expert content editor specializing in SEO content optimization for blogs.
        I will provide you with a 'research report' and a 'blog content' on the same topic.
        Your task is to follow below given guidelines to write a new, unique, and informative blog article
        that will rank well in search engine results and engage readers effectively.

        Follow below given guidelines:
        1. Master the report and blog content: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and conversational tone.
        3. Identify Main Keywords: Determine the primary topic and combine the articles on that main topic.
        4. Use Creative and Human-like Style: Incorporate contractions, idioms, transitional phrases,
        interjections, and colloquialisms.
        5. Blog Structuring: Include an Introduction, subtopics and use bullet points or
        numbered lists if appropriate. Important to include FAQs, Conclusion and Referances.
        6. Ensure Uniqueness: Guarantee the article is plagiarism-free. Write in human-like and informative style.
        7. Act as subject matter expert and include statistics and facts in your combined article.
        8. Do not provide explanations for your response.
        Important: Please read the entire prompt before writing anything. Follow the prompt exactly as I instructed.\n\n

        Research report: '{report}'
        Blog content: '{blog}'
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_research: Failed to get response from LLM: {err}")
        raise err
