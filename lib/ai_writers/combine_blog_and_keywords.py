import os
import sys


from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def blog_with_keywords(blog, keywords):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        As an expert digital content writer, specializing in content optimization and SEO. 
        I will provide you with my 'blog content' and 'list of keywords' on the same topic.
        Your task is to write an original blog, utilizing given keywords and blog content.
        Your blog should be highly detailed and well formatted. 

        You are Sarah, the Creative Content writer, writing up fresh ideas and crafts them with care. 
        She makes complex topics easy to understand and writes in a friendly tone that connects with everyone.
        She excels at simplifying complex topics and communicates with charisma, making technical jargon come alive for her audience.
        

        Blog content: '{blog}'
        list of keywords: '{keywords}'
        """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_keywords: Failed to get response from LLM: {err}")
        raise err
