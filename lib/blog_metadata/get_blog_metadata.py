import sys
import streamlit as st
from loguru import logger
import random
import time

logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen

def blog_metadata(blog_article):
    """ Common function to get blog metadata """
    logger.info(f"Generating Content MetaData\n")
    
    progress_bar = st.progress(0)
    total_steps = 4

    # Step 1: Generate blog title
    time.sleep(random.uniform(1, 3))
    blog_title = generate_blog_title(blog_article)
    progress_bar.progress(1 / total_steps)

    # Step 2: Generate blog meta description
    time.sleep(random.uniform(1, 3))
    blog_meta_desc = generate_blog_description(blog_article)
    progress_bar.progress(2 / total_steps)

    # Step 3: Generate blog tags
    time.sleep(random.uniform(1, 3))
    blog_tags = get_blog_tags(blog_article)
    progress_bar.progress(3 / total_steps)

    # Step 4: Generate blog categories
    time.sleep(random.uniform(1, 3))
    blog_categories = get_blog_categories(blog_article)
    progress_bar.progress(4 / total_steps)

    # Present the result in a table format
    st.table({
        "Metadata": ["Blog Title", "Meta Description", "Tags", "Categories"],
        "Value": [blog_title, blog_meta_desc, blog_tags, blog_categories]
    })

    return blog_title, blog_meta_desc, blog_tags, blog_categories

def generate_blog_title(blog_article):
    """
    Given a blog title generate an outline for it
    """
    logger.info("Generating blog title.")
    prompt = f"""As a SEO expert, I will provide you with a blog content.
            Your task is write a SEO optimized and call to action, blog title for given blog content.
            Follow SEO best practises to suggest the blog title.
            Please keep the titles concise, not exceeding 60 words.
            Respond with only the title and no explanations.
            Negative Keywords: Unvieling, unleash, power of. Dont use such words in your title.
            
            \nGenerate blog title for this given blog content:\n '{blog_article}' """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to get response from LLM: {err}")
        raise err

def generate_blog_description(blog_content):
    """
        Prompt designed to give SEO optimized blog descripton
    """
    logger.info("Generating Blog Meta Description for the given blog.")
    prompt = f"""As an expert SEO and blog writer, Compose a compelling meta description for the given blog content,
        adhering to SEO best practices. Keep it between 150-160 characters.
        Provide a glimpse of the content's value to entice readers.
        Respond with only one of your best effort and do not include your explanations.
        Blog Content: '{blog_content}'"""

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to get response from LLM:{err}")
        raise err

def get_blog_categories(blog_article):
    """
    Function to generate blog categories for given blog content.
    """
    prompt = f"""As an expert SEO and content writer, I will provide you with blog content.
            Suggest only 2 blog categories which are most relevant to provided blog content,
            by identifying the main topic. Also consider the target audience and the
            blog's category taxonomy. Only reply with comma separated values. 
            The blog content is: '{blog_article}'"
    """
    logger.info("Generating blog categories for the given blog.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"get_blog_categories:Failed to get response from LLM: {err}")

def get_blog_tags(blog_article):
    """
        Function to suggest tags for the given blog content
    """
    prompt = f"""As an expert SEO and blog writer, suggest only 2 relevant and specific blog tags
         for the given blog content. Only reply with comma separated values.
         Blog content:  {blog_article}."""
    logger.info("Generating Blog tags for the given blog post.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to get response from LLM: {err}")
        raise err

