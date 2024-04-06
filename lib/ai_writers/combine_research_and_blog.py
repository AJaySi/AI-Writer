import os
import sys

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../.env'))

from ..gpt_providers.openai_text_gen import openai_chatgpt
from ..gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""
    gpt_providers = os.environ["GPT_PROVIDER"]
    prompt = f"""
        You are an expert content editor specializing in SEO content optimization for blogs.
        I will provide you with a 'research report' and a 'blog content' on the same topic.
        Your task is to follow below given guidelines to write a new, unique, and informative blog article
        that will rank well in search engine results and engage readers effectively.

        Follow below given guidelines:
        1. Master the report and blog content: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and conversational tone.
        3. Identify Main Keywords: Determine the primary topic and combine the articles on that main topic.
        4. Implement SEO best practises with appropriate keyword density.
        5. Use Creative and Human-like Style: Incorporate contractions, idioms, transitional phrases,
        interjections, and colloquialisms.
        6. Blog Structuring: Include an Introduction, subtopics and use bullet points or
        numbered lists if appropriate. Important to include FAQs, Conclusion and Referances.
        7. Ensure Uniqueness: Guarantee the article is plagiarism-free. Write in human-like and informative style.
        9. Pass AI Detection Tools: Create content that easily passes AI plagiarism detection tools.
        10. Act as subject matter expert and include statistics and facts in your combined article.

        Important: Please read the entire prompt before writing anything. Follow the prompt exactly as I instructed.\n\n

        Research report: '{report}'
        Blog content: '{blog}'
        """

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
            logger.error(f"failed to get response from Openai: {err}")
            raise err
    else:
        logger.error(f"Unrecognised/Un-Supoorted GPT_PROVIDER: {gpt_providers}\n")
        return
