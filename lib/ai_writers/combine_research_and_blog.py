import os
import sys

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


def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""
    gpt_providers = os.environ["GPT_PROVIDER"]
    prompt = f"""
        You are an expert copywriter specializing in SEO content optimization for blogs.
        I will provide you with a 'research report' and a 'blog content' on the same topic.
        Your task is to transform and combine the given 'research report' and 'blog content' into a well-structured, unique
        and original blog article.

        Your objectives include:
        1. Master the report and blog content: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and coherence.
        3. Identify Main Keywords: Determine the primary topic and combine the articles on the main topic.
        4. REMEMBER: From the research report, include links and cititations to make your article more authoratative.
        5. Optimize for SEO: Generate high quality informative content.
        6. Implement SEO best practises with appropriate keyword density.
        7. Craft Engaging and Informative Article: Provide value and insight to readers.
        8. Proofread: Important to Check for grammar, spelling, and punctuation errors.
        9. Use Creative and Human-like Style: Incorporate contractions, idioms, transitional phrases,
        interjections, and colloquialisms. Avoid repetitive phrases and unnatural sentence structures.
        10. Blog Structuring: Include an Introduction, subtopics and use bullet points or
        numbered lists if appropriate. Important to include FAQs, Conclusion and Referances.
        11. Ensure Uniqueness: Guarantee the article is plagiarism-free. Write in unique, informative style.
        12. Punctuation: Use appropriate question marks at the end of questions.
        13. Pass AI Detection Tools: Create content that easily passes AI plagiarism detection tools.
        14. REMEMBER: Use the formatting style of given research report and include highlights, citations, referances in combined article.

        Follow these guidelines to combine and write a new, unique, and informative blog article
        that will rank well in search engine results and engage readers effectively.

        Create a blog post, in markdown, from the given research report and blog content below.
        Research report: '{report}'
        Blog content: '{blog}'
        """

    if 'google' in gpt_providers.lower():
        prompt = f"""You are an expert copywriter specializing in content optimization for SEO. 
        I will provide you with my 'research report' and 'blog content' on the same topic.
        Your task is to transform and combine the given research and blog content into a blog article.
        Your blog should be highly detailed, original and well formatted.
        Do not miss out any details from provided content. 
        Always, enhance the blog FAQs section with more information from given research.
        It is important that your blog provides detailed insights and engaging to readers.
        It should be highly readable and SEO optimized.

        Research report: '{report}'
        Blog content: '{blog}'
        """
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
