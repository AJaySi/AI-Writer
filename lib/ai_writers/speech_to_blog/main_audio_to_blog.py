import os
import datetime #I wish
import sys
from textwrap import dedent
import openai
from tqdm import tqdm, trange
import time

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from .write_blogs_from_youtube_videos import youtube_to_blog
from ...ai_web_researcher.gpt_online_researcher import do_google_serp_search
from ..blog_from_google_serp import blog_with_research
from ...blog_metadata.get_blog_metadata import blog_metadata
from ...blog_postprocessing.save_blog_to_file import save_blog_to_file


def generate_audio_blog(audio_input):
    """Takes a list of youtube videos and generates blog for each one of them.
    """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""
    try:
        logger.info(f"Starting to write blog on URL: {audio_input}")
        yt_blog, yt_title = youtube_to_blog(audio_input)
    except Exception as e:
        logger.error(f"Error in youtube_to_blog: {e}")
        sys.exit(1)

    try:
        logger.info("Starting with online research for URL title.")
        research_report = do_google_serp_search(yt_title)
        print(research_report)
    except Exception as e:
        logger.error(f"Error in do_online_research: {e}")
        sys.exit(1)

    try:
        # Note: Check if the order of input matters for your function
        logger.info("Preparing a blog content from audio script and online research content...")
        blog_markdown_str = blog_with_research(research_report, yt_blog)
    except Exception as e:
        logger.error(f"Error in blog_with_research: {e}")
        sys.exit(1)

    try:        
        blog_title, blog_meta_desc, blog_tags, blog_categories = blog_metadata(blog_markdown_str)
    except Exception as err:
        logger.error(f"Failed to generate blog metadata: {err}")

    try:
        # TBD: Save the blog content as a .md file. Markdown or HTML ?
        save_blog_to_file(blog_markdown_str, blog_title, blog_meta_desc, blog_tags, blog_categories, generated_image_filepath)
    except Exception as err:
        logger.error(f"Failed to save final blog in a file: {err}")

    blog_frontmatter = dedent(f"""\n\n\n\
                ---
                title: {blog_title}
                categories: [{blog_categories}]
                tags: [{blog_tags}]
                Meta description: {blog_meta_desc.replace(":", "-")}
                ---\n\n""")
    logger.info(f"{blog_frontmatter}{blog_markdown_str}")
    logger.info(f"\n\n ################ Finished writing Blog for : {audio_input} #################### \n")
