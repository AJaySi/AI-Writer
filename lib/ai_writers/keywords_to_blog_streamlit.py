import sys
import os
import asyncio
from textwrap import dedent
from pathlib import Path
from datetime import datetime
import streamlit as st
from gtts import gTTS
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path('../../.env'))
# Logger setup
from loguru import logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}")

# Import other necessary modules
from ..ai_web_researcher.gpt_online_researcher import (
        do_google_serp_search, do_tavily_ai_search, 
        do_metaphor_ai_research, do_google_pytrends_analysis)
from .blog_from_google_serp import write_blog_google_serp, blog_with_research
from ..ai_web_researcher.you_web_reseacher import get_rag_results, search_ydc_index
from ..blog_metadata.get_blog_metadata import blog_metadata
from ..blog_postprocessing.save_blog_to_file import save_blog_to_file
from ..gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image


# Function to convert text to speech and save as an audio file
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    return "output.mp3"


# Function to get audio file as a downloadable link
def get_audio_file(audio_file):
    with open(audio_file, "rb") as file:
        data = file.read()
        b64_data = base64.b64encode(data).decode()
        return f'<a href="data:audio/mp3;base64,{b64_data}" download="output.mp3">Download audio file</a>'


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
    with st.status("Started Web Research..", expanded=True) as status:
        st.empty()
        status.update(label="Researching and Writing Blog on keywords.")
        # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
        try:
            google_search_result, g_titles = do_google_serp_search(search_keywords)
            if google_search_result:
                status.update(label=f"🙎 Finished with Google web for Search: {search_keywords}")
                example_blog_titles.append(g_titles)
            else:
                st.warning("Failed to Google SERP results.")
        except Exception as err:
            st.warning(f"Failed in Google web research: {err}")
            logger.error(f"Failed in Google web research: {err}")

        try:
            status.update(label=f"🛀 Starting Tavily AI research: {search_keywords}")
            tavily_search_result, t_titles, t_answer = do_tavily_ai_search(search_keywords)
            status.update(label=f"🙆 Finished Google Search & Tavily AI Search on: {search_keywords}",
                          state="complete", expanded=False)
        except Exception as err:
            st.warning(f"Failed in Tavily web research: {err}")
            logger.error(f"Failed in Tavily web research: {err}")


    with st.status("Started Writing blog from google search..", expanded=True) as status:
        status.update(label="Researching and Writing Blog on keywords.")
        # Call on the got-researcher, tavily apis for this. Do google search for organic competition.
        try:
            status.update(label=f"🛀 Writing blog from Google Search on: {search_keywords}")
            blog_markdown_str = write_blog_google_serp(search_keywords, google_search_result)
            st.markdown(blog_markdown_str)
            status.update(label="🙎 Draft 1: Your Content from Google search result.", state="complete", expanded=False)
        except Exception as err:
            status.update(label="🙎 Failed Content from Google SERP.", state="error", expanded=False)
            st.error(f"Failed in Google web research: {err}")
            logger.error(f"Failed in Google web research: {err}")

    # logger.info/check the final blog content.
    logger.info("######### Draft1: Finished Blog from Google web search: ###########")

    with st.status("Started Writing blog from Tavily Web search..", expanded=True) as status:
        # Do Tavily AI research to augment the above blog.
        try:
            # example_blog_titles.append(t_titles)
            if tavily_search_result:
                logger.info(f"\n\n######### Blog content after Tavily AI research: ######### \n\n")
                blog_markdown_str = write_blog_google_serp(search_keywords, tavily_search_result)
                status.update(label=f"Finished Writing Blog From Tavily Results:{blog_markdown_str}", expanded=True)
        except Exception as err:
            status.update(label="🙎 Failed content from Tavily search.", state="error", expanded=False)
            logger.error(f"Failed to do Tavily AI research: {err}")

        status.update(label="🙎 Generating - Title, Meta Description, Tags, Categories for the content.", expanded=True)
        try:
            blog_title, blog_meta_desc, blog_tags, blog_categories = asyncio.run(blog_metadata(blog_markdown_str))
        except Exception as err:
            st.error(f"Failed to get blog metadata: {err}")

        generated_image_filepath = None
        try:
            # FIXME: Temporary fix.
            text_to_image = f"{blog_title} + ' ' + {blog_meta_desc}"
            if not text_to_image:
                text_to_image = blog_markdown_str
            generated_image_filepath = generate_image(text_to_image)
        except Exception as err:
            st.warning(f"Failed in Image generation: {err}")

        saved_blog_to_file = save_blog_to_file(blog_markdown_str, blog_title, blog_meta_desc,
                                               blog_tags, blog_categories, generated_image_filepath)
        status.update(label=f"Saved the content in this file: {saved_blog_to_file}")
        logger.info(f"\n\n --------- Finished writing Blog for : {search_keywords} -------------- \n")

        # Render the result on streamlit UI
        if generated_image_filepath:
            st.image(generated_image_filepath)
        st.markdown(f"{blog_markdown_str}")
        status.update(label=f"Finished, Review & Use your Original Content Below: {saved_blog_to_file}",
                      state="complete")

        # Passing the text and language to the engine, here we have marked slow=False. Which tells
        # the module that the converted audio should have a high speed
        tts = gTTS(text=blog_markdown_str, lang='en', slow=False)
        # Saving the converted audio in a mp3 file
        tts.save("delete_me.mp3")
        st.audio("delete_me.mp3")
