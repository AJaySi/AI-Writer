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

    prompt = f"""The following is what I will refer to as an 'Exception-list'. 
    Do Not include any of the words or phrases on this list in your future responses to this chat thread. 
    These instructions are critical and require absolute adherence!

    Exception-list: ["Informed decisions", "blueprint", "realm", "holistic", "fosters", "informed investment decisions", "informed", "more than just", "it’s about" "navigating", "beacon", "bustling", "treasure trove", "landscape", "tailored", "tailor", “roadmap” , “are more than just”, "tailoring", "dive in", "delving", “streamlining” "dynamic", "robust", "stay tuned", "in conclusion", "seamless", "bustling", “isn't just”, “not just a”, “isn't merely an”, “cornerstone”, “bridge”, “whopping”, “testament”, “paramount” ,“diving into”, “delve into”, “pivotal”, “navigating”, “This isn't a”, “isn't just about“ ,“dives deep”, "It's not just about", “delve”, “harness”, journey”, “elevate”, “maze”, “puzzle”, “overwhelmed” , "and other robotic cliches”, 'It’s important to note', 'Delve into', 'Tapestry', 'Bustling', 'In summary', 'In conclusion', 'Unleash', 'Unveiling', 'ever-evolving', '', 'Remember that', 'Take a dive into', 'Navigating', 'Navigating the landscape', 'Navigating the complexities of', 'Landscape', 'The landscape of', 'Testament', 'a testament to', 'In the world of', 'Realm', 'Embark', 'virtuoso', 'Let's explore', 'symphony', 'Harnessing', 'Revolutionizing', 'Empower', 'game changing', 'ever-changing', 'Embrace', 'Embracing', 'game-changing', 'ever-evolving']

    As an expert content writer and editor, I will provide you with blog content. 
    Your task is to replace all occurances of words from Exception-list from given blog content below.
    Before generating any text, examine the Exception-list and avoid all cases of these words and phrases.
        
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
