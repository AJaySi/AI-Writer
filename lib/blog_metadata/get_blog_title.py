import os
import sys

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

from ..gpt_providers.openai_text_gen import openai_chatgpt
from ..gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def generate_blog_title(blog_article, keywords=None, example_titles=None, num_titles=1):
    """
    Given a blog title generate an outline for it
    """
    prompt = ''
    gpt_providers = os.environ["GPT_PROVIDER"]
    logger.info("Generating blog title.")
    if not keywords and not example_titles:
        prompt = f"""As a SEO expert, I will provide you with a blog content. 
            Your task is write a SEO optimized and call to action, blog title for given blog content.
            Follow SEO best practises to suggest the blog title. 
            Please keep the titles concise, not exceeding 60 words. 
            Respond with only {num_titles} title and no explanations.
            Negative Keywords: Unvieling, unleash, power of. Dont use such words in your title.
            Generate {num_titles} blog title for this given blog content:\n '{blog_article}' """
    elif keywords and example_titles:
        prompt = f"""As a SEO expert, I will provide you with my blog keywords and example titles.
            Your task is to write {num_titles} blog title.
            Ensure that your blog titles will help in competing against given example titles.
            Follow SEO best practises to suggest the blog title.
            Please keep the titles concise, not exceeding 60 words.
            Respond with only {num_titles} title and no explanations.
            Negative Keywords: Unvieling, unleash, power of. Dont use such words in your title.
            Blog Keywords: '{keywords}'
            Example Titles: '{example_titles}'
        """
    elif not example_titles:
        prompt = prompt = f"""As a SEO expert, I will provide you with my blog article.
            Your task is to write {num_titles} blog title.
            Follow SEO best practises to suggest the blog title.
            Please keep the titles concise, not exceeding 60 words.
            Respond with only {num_titles} title and no explanations.
            Negative Keywords: Unvieling, unleash, power of. Dont use such words in your title.
            Blog Article: '{keywords}'
        """
    if 'google' in gpt_providers.lower():
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error(f"Failed to get response from gemini: {err}") 
    elif 'openai' in gpt_providers.lower():
        try:
            logger.info("Calling OpenAI LLM.")
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Failed to get response from Openai: {err}") 
