import os
import sys

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))
import configparser

from ..gpt_providers.gemini_pro_text import gemini_text_response
from ..gpt_providers.openai_text_gen import openai_chatgpt


def blog_proof_editor(blog_content):
    """ Helper for blog proof reading. """

    gpt_provider = os.environ["GPT_PROVIDER"]
    try:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'main_config'))
        config = configparser.ConfigParser()
        #config = configparser.RawConfigParser()
        config.read(config_path, encoding='utf-8-sig')
    except Exception as err:
        print(f"ProofReader: Failed to read values from config: {err}")

    prompt = f"""As an expert content writer and editor, I will provide you with 'my blog' content.
        Your task is to rewrite my blog, by following the guidelines below.
        
        Below are the guidelines to follow:

        1). You must respond in {config.get('blog_characteristics', 'blog_language')} language.
        2). Vocabulary and Grammar Enhancement: Directly correct any grammatical errors and upgrade the 
        vocabulary for better readability.
        3). Improve Sentence Structure: Enhance sentence construction for better clarity and conversational flow.
        4). Tone and Brand Alignment: Adjust tone, voice, personality for {config.get('blog_characteristics', 'blog_tone')} audience.
        5). Optimize Content Structure: Reorganize content for more impactful presentation, including better paragraphing & transitions.
        6). Simplify content: Simplify concepts and replace overly complex words. Use simple english words.
        7). Make sure your response content length is of {config.get('blog_characteristics', 'blog_length')} words.

        \n\nMy Blog: '{blog_content}'. """

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
