#####################################################
#
# Alwrity, AI Long form writer - Writing_with_Prompt_Chaining
# and generative AI.
#
#####################################################

import os
import re
import time #iwish
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv
from configparser import ConfigParser
import streamlit as st

from google.api_core import retry
import google.generativeai as genai
from pprint import pprint
from textwrap import dedent

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..utils.read_main_config_params import read_return_config_section
from ..ai_web_researcher.gpt_online_researcher import do_metaphor_ai_research
from ..ai_web_researcher.gpt_online_researcher import do_google_serp_search, do_tavily_ai_search
from ..blog_metadata.get_blog_metadata import blog_metadata
from ..blog_postprocessing.save_blog_to_file import save_blog_to_file


def generate_with_retry(model, prompt):
    """
    Generates content from the model with retry handling for errors.

    Parameters:
        model (GenerativeModel): The generative model to use for content generation.
        prompt (str): The prompt to generate content from.

    Returns:
        str: The generated content.
    """
    try:
        # FIXME: Need a progress bar here.
        return model.generate_content(prompt, request_options={'retry':retry.Retry()})
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return ""


def long_form_generator(content_keywords):
    """
    Write long form content using prompt chaining and iterative generation.
    Parameters:
    """
    with st.status("Start Writing Long Form Article, Hold my Beer..", expanded=True) as status:
        # Read the main_config to define tone, character, personality of the content to be generated.
        try:
            status.update(label=f"Starting to write content on {content_keywords}.")
            logger.info(f"Starting to write content on {content_keywords}.")
            # Define persona and writing guidelines
            content_tone, target_audience, content_type, content_language, output_format, content_length = read_return_config_section('blog_characteristics')
        except Exception as err:
            logger.error(f"Failed to Read config params from main_config: {err}")
            st.error(f"Failed to Read config params from main_config: {err}")
            return False
    
        try:
            filepath = os.path.join(os.environ["PROMPTS_DIR"], "long_form_ai_writer.prompts")
            status.update(label=f"Reading Prompts from {filepath}.")
            # Check if file exists
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File {filepath} does not exist")
            with open(filepath, 'r') as file:
                prompts = yaml.safe_load(file)
        except Exception as err:
            st.error(f"Exit: Failed to read prompts from {filepath}: {err}")
            logger.error(f"Exit: Failed to read prompts from {filepath}: {err}")
            exit(1)
    
        writing_guidelines = prompts.get('writing_guidelines').format(
            content_language=content_language,
            content_tone=content_tone,
            content_type=content_type,
            output_format=output_format,
            content_keywords=content_keywords,
            target_audience=target_audience
        )
    
        content_title = prompts.get('content_title').format(
            content_language=content_language,
            content_keywords=content_keywords,
            target_audience=target_audience
        )
        
        content_outline = prompts.get('content_outline').format(
            content_language=content_language,
            content_title='{content_title}',
            content_type=content_type,
            target_audience=target_audience
        )
        
        starting_prompt = prompts.get('starting_prompt').format(
            content_language=content_language,
            content_title='{content_title}',
            content_outline='{content_outline}',
            writing_guidelines=writing_guidelines
        )
        
        continuation_prompt = prompts.get('continuation_prompt').format(
            content_language=content_language,
            content_title='{content_title}',
            content_outline='{content_outline}',
            content_text='{content_text}',
            web_research_result='{web_research_result}',
            writing_guidelines=writing_guidelines
        )
    
        # Configure generative AI
        load_dotenv(Path('../.env'))
        generation_config = {
           "temperature": 0.6,
           "top_p": 1,
           "max_output_tokens": 8096,
        }
        
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Initialize the generative model
        #model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
        model_pro = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
        
        # Do SERP web research for given keywords to generate title and outline.
        web_research_result, g_titles = do_google_serp_search(content_keywords)
    
        # Generate prompts
        try:
            content_title = generate_with_retry(model_pro, content_title.format(web_research_result=web_research_result)).text
            logger.info(f"The title of the content is: {content_title}")
            status.update(label=f"The title of the content is: {content_title}")
        except Exception as err:
            logger.error(f"Content title Generation Error: {err}")
            return
        
        try:
            content_outline = generate_with_retry(model_pro, content_outline.format(
                content_title=content_title, 
                web_research_result=web_research_result)).text
            logger.info(f"The content Outline is: {content_outline}\n\n")
            status.update(label=f"Completed with Content Outline.")
        except Exception as err:
            logger.error(f"Failed to generate content outline: {err}")
    
        try:
            status.update(label=f"Do web research with Tavily to provide context for content creation.")
            logger.info("Do web research with Tavily to provide context for content creation.")
            # Do Metaphor/Exa AI search.
            table_data = []
            web_research_result, m_titles, t_titles = do_tavily_ai_search(content_keywords, max_results=5)
            for item in web_research_result.get("results"):
                title = item.get("title", "")
                snippet = item.get("content", "")
                table_data.append([title, snippet])
            web_research_result = table_data
        except Exception as err:
            logger.error(f"Failed to do Tavily AI search: {err}")
            st.error(f"Failed to do Tavily AI search: {err}")
            return
    
        try:
            starting_draft = generate_with_retry(model_pro, starting_prompt.format(
                    content_title=content_title, 
                    content_outline=content_outline,
                    web_research_result=web_research_result,
                    writing_guidelines=writing_guidelines)).text
        except Exception as err:
            st.error(f"Failed to Generate Starting draft: {err}")
            logger.error(f"Failed to Generate Starting draft: {err}")
            return
        
        try:
            logger.info(f"Starting to write on the outline introduction.")
            draft = starting_draft
            continuation = generate_with_retry(model_pro, continuation_prompt.format(
                    content_title=content_title, 
                    content_outline=content_outline, 
                    content_text=draft, 
                    web_research_result=web_research_result,
                    writing_guidelines=writing_guidelines)).text
        except Exception as err:
            logger.error(f"Failed to write the initial draft: {err}")
    
        # Add the continuation to the initial draft, keep building the story until we see 'IAMDONE'
        try:
            draft += '\n\n' + continuation
        except Exception as err:
            logger.error(f"Failed as: {err} and {continuation}")
    
        logger.info(f"Writing in progress... Current draft length: {len(draft)} characters")
        status.update(label=f"Writing in progress... Current draft length: {len(draft)} characters")
        search_terms = f"""
            I will provide you with blog outline, your task is to read the outline & return 8 google search keywords.
            Your response will be used to do web research for writing on the given outline.
            Do not explain your response, provide 8 google search sentences encompassing the given content outline.
            Provide the search term results as comma separated values.\n\n
            Content Outline:\n
            '{content_outline}'
            """
        search_words = generate_with_retry(model_pro, search_terms).text
        status.update(label=f"Search terms from written draft: {search_words}")
        
        while 'IAMDONE' not in continuation:
            #web_research_result, m_titles = do_metaphor_ai_research(content_keywords)
            str_list = re.split(r',\s*', search_words)
            # Strip quotes from each element 
            str_list = [s.strip('\'"') for s in str_list]
            for search_term in str_list:
                web_research_result, m_titles, t_titles = do_tavily_ai_search(search_term, max_results=5)
                try:
                    continuation = generate_with_retry(model_pro, continuation_prompt.format(
                        content_title=content_title,
                        content_outline=content_outline, 
                        content_text=draft, 
                        web_research_result=web_research_result,
                        writing_guidelines=writing_guidelines)).text
    
                    draft += '\n\n' + continuation
                    logger.info(f"Writing in progress... Current draft length: {len(draft)} characters")
                    status.update(label=f"Writing in progress... Current draft length: {len(draft)} characters")
                    # At this point, the context is little stale. We should more web research on
                    # related queries as per the content outline, to augment the LLM context.
                except Exception as err:
                    st.error(f"Failed to continually write the Essay: {err}")
                    logger.error(f"Failed to continually write the Essay: {err}")
                    return
        
        # Remove 'IAMDONE' and print the final story
        final = draft.replace('IAMDONE', '').strip()
        status.update(label="Success: Finished writing Long form content.")

        # FIXME: The current implementation is suited for normal length content.
        # In long content sending the whole content for each content metadata is expensive.
#        blog_title, blog_meta_desc, blog_tags, blog_categories = blog_metadata(final,
#                content_keywords, m_titles)
#        status.update(label="Success: Finished with Title, Meta Description, Tags, categories")
#        generated_image_filepath = None
#        # TBD: Save the blog content as a .md file. Markdown or HTML ?
#        save_blog_to_file(final, blog_title, blog_meta_desc, blog_tags, blog_categories, generated_image_filepath)
#    
#        blog_frontmatter = dedent(f"""
#        \n---------------------------------------------------------------------
#        title: {blog_title.strip()}\n
#        categories: [{blog_categories.strip()}]\n
#        tags: [{blog_tags.strip()}]\n
#        Meta description: {blog_meta_desc.replace(":", "-").strip()}\n
#        ---------------------------------------------------------------------\n
#        """)
#
#        logger.info(f"\n{blog_frontmatter}{final}\n\n")
#        st.markdown(f"\n{blog_frontmatter}{final}\n\n")
        logger.info(f"\n{final}\n\n")

        logger.info(f"\n\n ################ Finished writing Blog for : {content_keywords} #################### \n")
    with st.expander("**Click to View the final content draft:**"):
        st.markdown(f"\n{final}\n\n")
