import sys
import os
import re
import datetime
import random
from dateutil.relativedelta import relativedelta
from textwrap import dedent
import logging
from zoneinfo import ZoneInfo
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def random_date_last_three_months():
    current_date = datetime.datetime.now(ZoneInfo('Asia/Kolkata'))
    three_months_ago = current_date - relativedelta(months=3)

    # Generate a random date between three_months_ago and current_date
    random_date = three_months_ago + datetime.timedelta(
        seconds=random.randint(0, int((current_date - three_months_ago).total_seconds()))
    )

    return random_date.strftime('%Y-%m-%d %H:%M:%S %z')


def save_blog_to_file(blog_content, blog_title, blog_meta_desc, blog_tags, blog_categories, main_img_path=None, file_type="md"):
    """
    Saves the provided blog content to a file in the specified format.

    Args:
        blog_content (str): The main content of the blog.
        blog_title (str): Title of the blog.
        blog_meta_desc (str): Meta description of the blog.
        blog_tags (list): List of tags associated with the blog.
        blog_categories (list): List of categories associated with the blog.
        main_img_path (str): Path to the main image of the blog.
        output_path (str): Path to the directory where the blog will be saved.
        file_type (str, optional): The file format for saving the blog ('md' for Markdown or 'html' for HTML). Defaults to 'md'.

    Raises:
        FileNotFoundError: If the output_path does not exist.
        Exception: If the blog content cannot be written to the file.
    """
    blog_frontmatter = ''
    # Sanitize and prepare the blog title
    # Remove colon and ampersand
    blog_title_md = blog_title.replace(":", "").replace("&", "")
    # Replace spaces with hyphens
    blog_title_md = blog_title_md.replace(" ", "-")
    blog_title_md = re.sub('[^A-Za-z0-9-]', '', blog_title_md)
    # Replace multiple consecutive dashes with a single dash
    blog_title_md = re.sub('-+', '-', blog_title_md)
    #blog_title_md = remove_stop_words(blog_title_md)
    logger.debug(f"Blog Title is: {blog_title_md}")

    # Check if output path exists
    output_path = os.getenv('CONTENT_SAVE_DIR')
    if not os.path.exists(output_path):
        logger.error(f"Error: Blog output directory is set to {output_path}, which does not exist.")
        raise FileNotFoundError(f"Output directory does not exist: {output_path}")

    # Handle Markdown file type
    if file_type == "md":
        logger.info("Writing/Saving the resultant blog content in Markdown format.")
        # Hmmmm, bulk generation will benefit from randomizing publishing dates.
        #dtobj = datetime.datetime.now(ZoneInfo('Asia/Kolkata'))
        #formatted_date = dtobj.strftime('%Y-%m-%d %H:%M:%S %z')
        formatted_date = random_date_last_three_months()
        blog_title = blog_title.replace(":", "-").replace('"', '').replace('**', '')
        if main_img_path:
            blog_frontmatter = dedent(f"""\
                ---
                title: {blog_title}
                date: {formatted_date}
                categories: [{blog_categories}]
                tags: [{blog_tags}]
                description: {blog_meta_desc.replace(":", "-").replace('**', '')}
                img_path: '/assets/'
                image:
                    path: {os.path.basename(main_img_path)}
                    alt: {blog_title}
                ---\n\n""")
        else:
            blog_frontmatter = dedent(f"""\
                ---
                title: {blog_title}
                date: {formatted_date}
                categories: [{blog_categories}]
                tags: [{blog_tags}]
                description: {blog_meta_desc.replace(":", "-")}
                ---\n\n""").strip()

        blog_output_path = os.path.join(
            output_path,
            f"{datetime.date.today().strftime('%Y-%m-%d')}-{blog_title_md}.md"
        )

        # Write to the file
        try:
            with open(blog_output_path, "w", encoding="utf-8") as f:
                f.write(blog_frontmatter)
                f.write(blog_content)
        except Exception as e:
            raise Exception(f"Failed to write blog content: {e}")

        logger.info(f"Successfully saved and posted blog at: {blog_output_path}")
        return(blog_output_path)
