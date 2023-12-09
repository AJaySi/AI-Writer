import json
import os
import datetime #I wish
import sys

import openai
from tqdm import tqdm, trange
import time
import re
from textwrap import dedent
import nltk
nltk.download('punkt', quiet=True)
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

from .write_blogs_from_youtube_videos import youtube_to_blog
from .wordpress_blog_uploader import compress_image, upload_blog_post, upload_media
from .gpt_online_researcher import do_online_research

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

# fixme: Remove the hardcoding, need add another option OR in config ?
image_dir = "blog_images"
image_dir = os.path.join(os.getcwd(), image_dir)
# TBD: This can come from config file.
output_path = "blogs"
output_path = os.path.join(os.getcwd(), output_path)
wordpress_url = 'https://latestaitools.in/'
wordpress_username = 'upaudel750'
wordpress_password = 'YvCS VbzQ QSp8 4XZe 0DUw Myys'


def generate_youtube_blog(yt_url_list, output_format="markdown"):
    """Takes a list of youtube videos and generates blog for each one of them.
    """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""
    for a_yt_url in yt_url_list:
        try:
            logger.info(f"Starting to write blog on URL: {a_yt_url}")
            yt_blog = youtube_to_blog(a_yt_url)
        except Exception as e:
            logger.error(f"Error in youtube_to_blog: {e}")
            sys.exit(1)

        try:
            logger.info("Starting with online research for URL title.")
            research_report = do_online_research(yt_blog)
        except Exception as e:
            logger.error(f"Error in do_online_research: {e}")
            sys.exit(1)

        try:
            # Note: Check if the order of input matters for your function
            logger.info("Preparing a blog content from audio script and online research content...")
            blog_with_research(research_report, yt_blog)
        except Exception as e:
            logger.error(f"Error in blog_with_research: {e}")
            sys.exit(1)

        try:
            # Get the title and meta description of the blog.
            blog_meta_desc = generate_blog_description(yt_blog)
            title = generate_blog_title(blog_meta_desc)
            logger.info(f"Title is {title} and description is {blog_meta_desc}")
            blog_markdown_str = "# " + title.replace('"', '') + "\n\n"
            # Get blog tags and categories.
            blog_tags = get_blog_tags(blog_meta_desc)
            logger.info(f"Blog tags are: {blog_tags}")
            blog_categories = get_blog_categories(blog_meta_desc)
            logger.info(f"Blog categories are: {blog_categories}")

            # Generate an introduction for the blog
            blog_intro = get_blog_intro(title, yt_blog)
            logger.info(f"The Blog intro is:\n {blog_intro}")
            blog_markdown_str = blog_markdown_str + "\n\n" + f"{blog_intro}" + "\n\n"

            # Generate an image based on meta description
            logger.info(f"Calling Image generation with prompt: {blog_meta_desc}")
            main_img_path = generate_image(blog_meta_desc, image_dir, "dalle3")

            # Get a variation of the yt url screenshot to use in the blog.
            #varied_img_path = gen_new_from_given_img(yt_img_path, image_dir)
            #logger.info(f"Image path: {main_img_path} and varied path: {varied_img_path}")
            #blog_markdown_str = blog_markdown_str + f'![img-description]({os.path.basename(varied_img_path)})' + '_Image Caption_'

            #stbdiff_img_path = generate_image(yt_img_path, image_dir, "stable_diffusion")
            #logger.info(f"Image path: {main_img_path} from stable diffusion: {stbdiff_img_path}")
            #blog_markdown_str = blog_markdown_str + f'![img-description]({os.path.basename(stbdiff_img_path)})' + f'_{title}_'
            
            # Add the body of the blog content.
            blog_markdown_str = blog_markdown_str + "\n\n" + f'{yt_blog}' + "\n\n"

            # Get the Conclusion of the blog, by passing the generated blog.
            blog_conclusion = get_blog_conclusion(blog_markdown_str)
            # TBD: Add another image.
            blog_markdown_str = blog_markdown_str + "### Conclusion" + "\n\n" + f"{blog_conclusion}" + "\n"

            # Proofread the blog, edit and remove dubplicates and refine it further.
            # Presently, fixing the blog keywords to be tags and categories.
            blog_keywords = f"{blog_tags} + {blog_categories}"
            blog_markdown_str = blog_proof_editor(blog_markdown_str, blog_keywords)

            # Check the type of blog format needed by the user.
            if 'html' in output_format:
                blog_markdown_str = convert_tomarkdown_format(blog_markdown_str)
            elif 'markdown' in output_path:
                blog_markdown_str = convert_markdown_to_html(blog_markdown_str)

            # Try to save the blog content in a file, in whichever format. Just dump it.
            try:
                save_blog_to_file(blog_markdown_str, title, blog_meta_desc, blog_tags, blog_categories, main_img_path)
            except Exception as err:
                logger.error("Failed to Save blog content: {blog_markdown_str}")

        except Exception as e:
            # raise assertionerror
            logger.error(f"Error: Failed to generate_youtube_blog: {e}")
            exit(1)
