import os
import sys
import json
from pathlib import Path

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def write_blog_google_serp(search_keyword, search_results):
    """Combine the given online research and GPT blog content"""
    prompt = f"""
        As expert Creative Content writer,
        I want you to write blog post, that explores {search_keyword} and also include 5 FAQs.

        I want the post to offer unique insights, relatable examples, and a fresh perspective on the topic.
        Here are some Google search results to spark your creativity on {search_keyword}:
        \n\n
        \"\"\"{search_results}\"\"\"
        """
    
    logger.info("Generating blog and FAQs from Google web search results.")
    
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def improve_blog_intro(blog_content, blog_intro):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        You are a skilled content editor, tasked with creating an engaging peek into the blog post provided. 
        This peek should entice readers to delve into the full content. 

        Here's what you need to do:
        1. **Replace the old blog introduction with the new one provided.**
        2. **Craft a short and captivating summary of the key points and interesting takeaways from the blog.** 
            - Highlight what makes the blog unique and worth reading.
            - This peek should be placed directly before the new introduction.
        3. **Include the complete blog content, with the new introduction and the added peek.**

        Do not provide explanations for your actions, simply present the edited blog content.

        Blog Content: \"\"\"{blog_content}\"\"\"
        Blog Introduction: \"\"\"{blog_intro}\"\"\"
        """
    logger.info("Generating blog introduction from tavily answer.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


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


def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        As expert Creative Content writer, Your task is to update a blog post using the latest research.
        
        Here's what you need to do:

        1. **Read the outdated blog content and the new research report carefully.**  
        2. **Identify key insights and updates from the research report that should be incorporated into the blog post.**
        3. **Rewrite sections of the blog post to reflect the new information, ensuring a smooth and natural flow.** 
        4. **Maintain the blog's original friendly and conversational tone throughout.**

        Remember, your goal is to seamlessly blend the new information into the existing blog post, making it accurate and engaging for readers. 
        \n\n
        Research Report: \"\"\"{report}\"\"\"

        Blog Content: \"\"\"{blog}\"\"\"
    """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_research: Failed to get response from LLM: {err}")
        raise err
