import sys
import os
from textwrap import dedent
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
from ..blog_metadata.get_blog_metadata import blog_metadata
from ..blog_postprocessing.save_blog_to_file import save_blog_to_file
from ..blog_postprocessing.blog_proof_reader import blog_proof_editor
from ..blog_postprocessing.humanize_blog import blog_humanize


def write_blog_from_keywords(search_keywords, url=None):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """
    # TBD: Keeping the results directory as fixed, for now.
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "workspace", "web_research_reports",
            search_keywords.replace(" ", "_") + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""
    example_blog_titles = []
    
    logger.info(f"Researching and Writing Blog on keywords: {search_keywords}")
    # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
    try:
        google_search_result, g_titles = do_google_serp_search(search_keywords)
        example_blog_titles.append(g_titles)
        blog_markdown_str = write_blog_google_serp(search_keywords, google_search_result)
    except Exception as err:
        logger.error(f"Failed in Google web research: {err}")
    # logger.info/check the final blog content.
    logger.info("\n######### Draft1: Finished Blog from Google web search: ###########\n\n")
    exit(1)


    # Do Tavily AI research to augument the above blog.
    try:
        tavily_search_result, t_titles = do_tavily_ai_search(search_keywords)
        example_blog_titles.append(t_titles)
        blog_markdown_str = blog_with_research(blog_markdown_str, tavily_search_result)
        logger.info(f"######### Blog content after Tavily AI research: ######### \n\n{blog_markdown_str}\n\n")
    except Exception as err:
        logger.error(f"Failed to do Tavily AI research: {err}")
    logger.info("######### Draft2: Blog content after Tavily AI research: #########\n\n")

    try:
        # Do Metaphor/Exa AI search.
        metaphor_search_result, m_titles = do_metaphor_ai_research(search_keywords)
        example_blog_titles.append(m_titles)
        blog_markdown_str = blog_with_research(blog_markdown_str, metaphor_search_result)
    except Exception as err:
        logger.error(f"Failed to do Metaphor AI search: {err}")
    logger.info("######### Draft3: Blog content after Tavily AI research: ######### \n\n")

    # Do Google trends analysis and combine with latest blog.
    try:
        pytrends_search_result = do_google_pytrends_analysis(search_keywords)
        logger.info(f"Google Trends keywords to use in the blog: {pytrends_search_result}\n")
        blog_markdown_str = blog_with_keywords(blog_markdown_str, pytrends_search_result)
    except Exception as err:
        logger.error(f"Failed to do Google Trends Analysis:{err}")
    logger.info(f"########### Blog Content After Google Trends Analysis:######### \n {blog_markdown_str}\n\n")
    
    # Combine YOU.com RAG search with the latest blog content.
    #you_rag_result = get_rag_results(search_keywords)
    #you_search_result = search_ydc_index(search_keywords)
    #blog_markdown_str = blog_with_research(blog_markdown_str, you_search_result)
    #logger.info(f"Final blog content: {blog_markdown_str}")

    logger.info("Pass Final blog for blog-proof reading and *improvements.")
    # Pass the final content for proofreading.
    blog_markdown_str = blog_proof_editor(blog_markdown_str)

    # Pass the content to remove obivious words used by AI.
    logger.info("Pass Final blog for Humanizing it further, Doesn't matter, Really?")
    blog_markdown_str = blog_humanize(blog_markdown_str)

    blog_title, blog_meta_desc, blog_tags, blog_categories = blog_metadata(blog_markdown_str, 
            search_keywords, example_blog_titles)

    # fixme: Remove the hardcoding, need add another option OR in config ?
    image_dir = os.path.join(os.getcwd(), "blog_images")
    generated_image_name = f"generated_image_{datetime.now():%Y-%m-%d-%H-%M-%S}.png"
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

    blog_frontmatter = dedent(f"""\n\n\n\
                ---
                title: {blog_title}
                categories: [{blog_categories}]
                tags: [{blog_tags}]
                Meta description: {blog_meta_desc.replace(":", "-")}
                ---\n\n""")
    logger.info(f"{blog_frontmatter}{blog_markdown_str}")
    logger.info(f"\n\n ################ Finished writing Blog for : {search_keywords} #################### \n")
