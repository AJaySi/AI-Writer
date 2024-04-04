import os
import sys

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

from ..gpt_providers.gemini_pro_text import gemini_text_response
from ..gpt_providers.openai_text_gen import openai_chatgpt


def blog_humanize(blog_content):
    """ Helper for blog proof reading. """
    gpt_provider = os.environ["GPT_PROVIDER"]

    prompt = f"""As an expert content writer and editor, I will provide you with blog content. 
        
        Your task is to replace all occurances of words given below:
        ['It’s important to note', 'Delve into', 'Tapestry', 'Bustling', 'In summary', 'In conclusion', 'Unleash', 'Unveiling', 'ever-evolving', '', 'Remember that', 'Take a dive into', 'Navigating', 'Navigating the landscape', 'Navigating the complexities of', 'Landscape', 'The landscape of', 'Testament', 'a testament to', 'In the world of', 'Realm', 'Embark', 'virtuoso', 'Let's explore', 'symphony', 'Harnessing', 'Revolutionizing', 'Empower', 'game changing', 'ever-changing', 'Embrace', 'Embracing', 'game-changing', 'ever-evolving']
        
        \n\nBlog Content: '{blog_content}'
        """
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
