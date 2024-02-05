import sys

from .get_blog_meta_desc import generate_blog_description
from .get_tags import get_blog_tags
from .get_blog_category import get_blog_categories
from .get_blog_title import generate_blog_title

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def blog_metadata(blog_content, gpt_providers="openai"):
    """ Common function to get blog metadata """
    blog_title = generate_blog_title(blog_content, gpt_providers)
    blog_meta_desc = generate_blog_description(blog_content, gpt_providers)
    logger.info(f"The blog meta description is: {blog_meta_desc}\n")
    blog_tags = get_blog_tags(blog_content, gpt_providers)
    logger.info(f"Blog tags for generated content: {blog_tags}")
    blog_categories = get_blog_categories(blog_content, gpt_providers)
    logger.info(f"Generated blog categories: {blog_categories}\n")

    return(blog_title, blog_meta_desc, blog_tags, blog_categories)
