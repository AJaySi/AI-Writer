import sys
import os
from pathlib import Path
import datetime

from .gpt_providers.openai_chat_completion import openai_chatgpt
import google.generativeai as genai
from .gpt_providers.gemini_pro_text import gemini_text_response
from .gpt_online_researcher import do_online_research
from .get_blog_meta_desc import generate_blog_description
from .get_tags import get_blog_tags
from .get_blog_category import get_blog_categories
from .get_blog_title import generate_blog_title
from .get_code_examples import gemini_get_code_samples
from .save_blog_to_file import save_blog_to_file
from .take_url_screenshot import screenshot_api

from dotenv import load_dotenv
load_dotenv(Path('../.env'))

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def generate_keyword_blog(blog_keywords, url=None, output_format="markdown"):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """
    for akeyword in blog_keywords:
        logger.info(f"Researching and Writing Blog on keywords: {akeyword}")
        # Use to store the blog in a string, to save in a *.md file.
        blog_markdown_str = ""

        # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
        blog_markdown_str = do_online_research(akeyword, "gemini")
        # logger.info/check the final blog content.
        logger.info(f"Final blog content: {blog_markdown_str}")

        blog_title = generate_blog_title(blog_markdown_str, "gemini") 
        blog_meta_desc = generate_blog_description(blog_markdown_str, "gemini")
        logger.info(f"The blog meta description is: {blog_meta_desc}\n")
        blog_tags = get_blog_tags(blog_markdown_str, "gemini")
        logger.info(f"Blog tags for generated content: {blog_tags}")
        blog_categories = get_blog_categories(blog_markdown_str, "gemini")
        logger.info(f"Generated blog categories: {blog_categories}\n")

        #blog_markdown_str = gemini_get_code_samples(blog_markdown_str)
        #logger.info(f"Blog with code sample: \n {blog_markdown_str}")

        # fixme: Remove the hardcoding, need add another option OR in config ?
        image_dir = os.path.join(os.getcwd(), "blog_images")
        generated_image_name = f"generated_image_{datetime.datetime.now():%Y-%m-%d-%H-%M-%S}.png"
        generated_image_filepath = os.path.join(image_dir, generated_image_name)
        # Generate an image based on meta description
        #logger.info(f"Calling Image generation with prompt: {blog_meta_desc}")
        #main_img_path = generate_image(blog_meta_desc, image_dir, "dalle3")
        if url:
            try:
                generated_image_filepath = screenshot_api(url, generated_image_filepath)
            except Exception as err:
                logger.error(f"Failed in taking compnay page screenshot: {err}")
        # TBD: Save the blog content as a .md file. Markdown or HTML ?
        save_blog_to_file(blog_markdown_str, blog_title, blog_meta_desc, blog_tags, blog_categories, generated_image_filepath)

        logger.info(f"\n\n ################ Finished writing Blog for : {akeyword} #################### \n")
