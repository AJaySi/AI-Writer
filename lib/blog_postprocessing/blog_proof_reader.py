import os
import sys

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

from ..gpt_providers.gemini_pro_text import gemini_text_response
from ..gpt_providers.openai_text_gen import openai_chatgpt


def blog_proof_editor(blog_content, blog_keywords):
    """
        Helper for blog proof reading.
    """
    gpt_provider = os.environ["GPT_PROVIDER"]
    prompt = f"""As an expert copywriter, I will provide you with 'my blog' and its 'main keywords'.
        Your task is to rewrite my blog, by following the guidelines below.
        
        Below are the guidelines to follow:

        1). Ensure Originality: Edit any sections that lack originality, replacing them with unique and creative content.
        2). Vocabulary and Grammar Enhancement: Directly correct any grammatical errors and upgrade the 
        vocabulary for better readability.
        3). Improve Sentence Structure: Enhance sentence construction for better clarity and flow.
        4). Tone and Brand Alignment: Adjust the tone, voice, personality of given content to make it unique.
        5). Optimize Content Structure: Reorganize the content for a more impactful presentation, 
        including better paragraphing and transitions.
        6). Simplify content: Simplify concepts and replace overly complex words. Use simple english words.
        7). Refine Overall Structure: Make structural changes to improve the overall impact of the content.

        \n\nMain keywords: '{blog_keywords}'
        My Blog: '{blog_content}'. """

    if 'openai' in gpt_provider.lower():
        try:
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Openai Error Blog Proof Reading: {err}")
    elif 'google' in gpt_provider.lower():
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            SystemError(f"Gemini Error Blog Proof Reading: {err}")
