import sys
import os
from textwrap import dedent
from pathlib import Path
from datetime import datetime
import streamlit as st

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
from .blog_from_google_serp import write_blog_google_serp, blog_with_research
from ..ai_web_researcher.you_web_reseacher import get_rag_results, search_ydc_index
from ..blog_metadata.get_blog_metadata import blog_metadata
from ..blog_postprocessing.save_blog_to_file import save_blog_to_file


def write_blog_from_keywords(search_keywords, url=None):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = None
    tavily_search_result = None
    example_blog_titles = []

    logger.info(f"Researching and Writing Blog on keywords: {search_keywords}")
    with st.status("Started Writing..", expanded=True) as status:
        st.empty()
        status.update(label="Researching and Writing Blog on keywords.")
        # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
        try:
            google_search_result, g_titles = do_google_serp_search(search_keywords)
            status.update(label=f"🙎 Finished with Google web for Search: {search_keywords}")
            example_blog_titles.append(g_titles)

            status.update(label=f"🛀 Starting Tavily AI research: {search_keywords}")
            tavily_search_result, t_titles, t_answer = do_tavily_ai_search(search_keywords)
            status.update(label=f"🙆 Finished Google Search & Tavily AI Search on: {search_keywords}", 
                    state="complete", expanded=False)

        except Exception as err:
            st.error(f"Failed in web research: {err}")
            logger.error(f"Failed in web research: {err}")

    with st.status("Started Writing blog from google search..", expanded=True) as status:
        status.update(label="Researching and Writing Blog on keywords.")
        # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
        try:
            status.update(label=f"🛀 Writing blog from Google Search on: {search_keywords}")
            blog_markdown_str = write_blog_google_serp(search_keywords, google_search_result)
            st.markdown(blog_markdown_str)
            status.update(label="🙎 Draft 1: Your Content from Google search result.", state="complete", expanded=False)
        except Exception as err:
            st.error(f"Failed in Google web research: {err}")
            logger.error(f"Failed in Google web research: {err}")

    # logger.info/check the final blog content.
    logger.info("######### Draft1: Finished Blog from Google web search: ###########")
    
    with st.status("Started Writing blog from Tavily Web search..", expanded=True) as status:
        # Do Tavily AI research to augument the above blog.
        try:
            #example_blog_titles.append(t_titles)
            if blog_markdown_str and tavily_search_result:
                logger.info(f"\n\n######### Blog content after Tavily AI research: ######### \n\n")
                blog_markdown_str = write_blog_google_serp(search_keywords, tavily_search_result)
                status.update(label="Finished Writing Blog From Tavily Results:{blog_markdown_str}")
            else:
                print("Not Writing with TAVILY..\n\n")
        except Exception as err:
            logger.error(f"Failed to do Tavily AI research: {err}")

        status.update(label="🙎 Generating - Title, Meta Description, Tags, Categories for the content.")
        blog_title, blog_meta_desc, blog_tags, blog_categories = blog_metadata(blog_markdown_str, 
                search_keywords, example_blog_titles)
   
        generated_image_filepath = None

        saved_blog_to_file = save_blog_to_file(blog_markdown_str, blog_title, blog_meta_desc, 
                            blog_tags, blog_categories, generated_image_filepath)
        status.update(label=f"Saved the content in this file: {saved_blog_to_file}")
        blog_frontmatter = dedent(f"""
        \n---------------------------------------------------------------------
        title: {blog_title.strip()}\n
        categories: [{blog_categories.strip()}]\n
        tags: [{blog_tags.strip()}]\n
        Meta description: {blog_meta_desc.replace(":", "-").strip()}\n
        ---------------------------------------------------------------------\n
        """)
        logger.info(f"\n\n --------- Finished writing Blog for : {search_keywords} -------------- \n")
        st.markdown(f"{blog_frontmatter}\n\n{blog_markdown_str}")
        status.update(label=f"Finished, Review & Use your Original Content Below: {saved_blog_to_file}")
