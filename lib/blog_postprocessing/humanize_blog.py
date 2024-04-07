import os
import sys

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def blog_humanize(blog_content):
    """ Helper for blog proof reading. """

    prompt = f"""The following is what I will refer to as an 'Exception-list'. 
    Do Not include any of the words or phrases on this list in your future responses to this chat thread. 
    These instructions are critical and require absolute adherence!

    Exception-list: ["Informed decisions", "blueprint", "realm", "holistic", "fosters", "informed investment decisions", "informed", "more than just", "it’s about" "navigating", "beacon", "bustling", "treasure trove", "landscape", "tailored", "tailor", “roadmap” , “are more than just”, "tailoring", "dive in", "delving", “streamlining” "dynamic", "robust", "stay tuned", "in conclusion", "seamless", "bustling", “isn't just”, “not just a”, “isn't merely an”, “cornerstone”, “bridge”, “whopping”, “testament”, “paramount” ,“diving into”, “delve into”, “pivotal”, “navigating”, “This isn't a”, “isn't just about“ ,“dives deep”, "It's not just about", “delve”, “harness”, journey”, “elevate”, “maze”, “puzzle”, “overwhelmed” , "and other robotic cliches”, 'It’s important to note', 'Delve into', 'Tapestry', 'Bustling', 'In summary', 'In conclusion', 'Unleash', 'Unveiling', 'ever-evolving', '', 'Remember that', 'Take a dive into', 'Navigating', 'Navigating the landscape', 'Navigating the complexities of', 'Landscape', 'The landscape of', 'Testament', 'a testament to', 'In the world of', 'Realm', 'Embark', 'virtuoso', 'Let's explore', 'symphony', 'Harnessing', 'Revolutionizing', 'Empower', 'game changing', 'ever-changing', 'Embrace', 'Embracing', 'game-changing', 'ever-evolving']

    As an expert content writer and editor, I will provide you with blog content. 
    Your task is to replace all occurances of words from Exception-list from given blog content below.
    Before generating any text, examine the Exception-list and avoid all cases of these words and phrases.
        
        \n\nBlog Content: '{blog_content}'
        """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Openai Error Blog Proof Reading: {err}")
        raise err
