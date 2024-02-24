import sys
import os
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(Path('../../.env'))
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..ai_web_researcher.gpt_online_researcher import do_google_serp_search,\
        do_tavily_ai_search, do_metaphor_ai_research, do_google_pytrends_analysis
from .blog_from_google_serp import write_blog_google_serp
from .combine_research_and_blog import blog_with_research
from .combine_blog_and_keywords import blog_with_keywords
from ..ai_web_researcher.you_web_reseacher import get_rag_results, search_ydc_index


def write_blog_from_keywords(search_keywords, url=None, output_format="markdown"):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """
    # TBD: Keeping the results directory as fixed, for now.
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "workspace", "web_research_reports",
            search_keywords.replace(" ", "_") + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    logger.info(f"Researching and Writing Blog on keywords: {search_keywords}")
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""

    # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
    google_search_result = do_google_serp_search(search_keywords)
    blog_markdown_str = write_blog_google_serp(search_keywords, google_search_result)
    # logger.info/check the final blog content.
    logger.info(f"Final blog content: {blog_markdown_str}")

    # Do Tavily AI research to augument the above blog.
    tavily_search_result = do_tavily_ai_search(search_keywords)
    blog_markdown_str = blog_with_research(blog_markdown_str, tavily_search_result)
    logger.info(f"Final blog content: {blog_markdown_str}")

    # Do Metaphor/Exa AI search.
    metaphor_search_result = do_metaphor_ai_research(search_keywords)
    blog_markdown_str = blog_with_research(blog_markdown_str, metaphor_search_result)
    logger.info(f"Final blog content: {blog_markdown_str}")
   
    # Do Google trends analysis and combine with latest blog.
    pytrends_search_result = do_google_pytrends_analysis(search_keywords)
    blog_markdown_str = blog_with_keywords(blog_markdown_str, pytrends_search_result)
    logger.info(f"Final blog content: {blog_markdown_str}")

    # Combine YOU.com RAG search with the latest blog content.
    #you_rag_result = get_rag_results(search_keywords)
    you_search_result = search_ydc_index(search_keywords)
    blog_markdown_str = blog_with_research(blog_markdown_str, you_search_result)
    logger.info(f"Final blog content: {blog_markdown_str}")

    exit(1)

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
