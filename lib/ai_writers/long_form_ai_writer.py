#####################################################
#
# Alwrity, AI Long form writer - Writing_with_Prompt_Chaining
# and generative AI.
#
#####################################################

import os
import time #iwish
import sys
from pathlib import Path
from dotenv import load_dotenv
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
from ..ai_web_researcher.gpt_online_researcher import do_google_serp_search
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
    # Read the main_config to define tone, character, personality of the content to be generated.
    try:    
        logger.info(f"Starting to write content on {content_keywords}.")
        # Define persona and writing guidelines
        content_tone, target_audience, content_type, content_language, output_format = read_return_config_section('blog_characteristics')
    except Exception as err:
        logger.error(f"Failed to Read config params from main_config: {err}")
        return

    writing_guidelines = f'''\
    Writing Guidelines

    As an expert Content writer and web researcher, demostrate your world class {content_type} content writing skills.
    
    Follow the below writing guidelines for writing your content:
    1). You must write in {content_language} language.
    2). Your content should appeal to target audience of {target_audience}.
    3). The tone of your content should be consistent for {content_tone}.
    4). Always ensure orignality and human-like content.
    5). Use simple {content_language} words, to appeal to all readers.
    6). Your content must be well formatted using {output_format} language.
    7). Do not use words like: Unleash, ultimate, Uncover, Discover, Elevate, Revolutionizing, Unveiling, Harnessing, Dive, Delve into, Embrace.

    Remember, your main goal is to write as much as you can. If you get through the content too fast, that is bad. 
    Expand, never summarize.
    '''


    # Generate prompts
    content_title = f'''\
    As an expert {content_language} content writer, specilizing in SEO writing.
    Your task is to write a blog title following guidelines below:

    1). Write a blog title for given keywords {content_keywords}.
    2). The title should appeal to audience level of {target_audience}.
    3). Review the given web research result for {content_keywords}. Your title should compete against them.
    4). Do not use words like: Unleash, ultimate, Uncover, Discover, Elevate, Revolutionizing, Unveiling, Harnessing, Dive, Delve into, Embrace.

    Web research Result:

    """{{web_research_result}}"""

    '''

    content_outline = f'''\
    As an expert {content_language} content outliner, specilizing in SEO optimised content.
    The title of my content is {{content_title}}. I will provide you with its web research results, as context.
    Your task is write a detailed content outline for the given 'Title', based on the given context.

    Instructions:
    1). Make sure the outline includes most of the topics from the below given web research results, as context.
    2). The outline should appeal to audience of {target_audience}.
    \n
    web research results is:
    
    """{{web_research_result}}"""

    '''

    starting_prompt = f'''\
    As an expert {content_language} content writer, specilizing in writing SEO optimised content.
    
    Your Content title is:

    """{{content_title}}"""

    The outline of the content is:

    """{{content_outline}}"""

    First, silently review the given content outline and the title. Consider how to start writing your content.
    Start to write the very beginning of the outline. You are not expected to finish the whole content now. 
    Your writing should be detailed enough that you are only scratching the surface of the first bullet of your outline. 
    Try to write AT MINIMUM 600 WORDS.

    """{writing_guidelines}"""
    '''

    continuation_prompt = f'''\
    As an expert {content_language} content writer & web researcher, specilizing in writing SEO optimised content.

    Your Content title is:

    """{{content_title}}"""

    The outline of the content is:

    """{{content_outline}}"""

    Relevant web research results:

    """{{web_research_result}}"""

    ============\n

    You've begun to write the content and continue to do so.
    Here's what you've written so far:

    """{{content_text}}"""

    =====

    First, take your time and silently review the content outline and what you have written so far. 
    Identify what the single next part of your outline you should write.

    Your task is to continue where you left off and write only the next parts of given outline.
    You are not expected to finish the whole content now. 
    Try to write AT MINIMUM 600 WORDS. However, only once the content
    is COMPLETELY finished, write IAMDONE. Remember, do NOT write a whole sections right now.
    \n\n
    {writing_guidelines}
    '''

    # Configure generative AI
    load_dotenv(Path('../.env'))
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    # Initialize the generative model
    model = genai.GenerativeModel('gemini-pro')
    model_pro = genai.GenerativeModel('gemini-1.5-flash-latest')
    # Do SERP web research for given keywords to generate title and outline.
    web_research_result, g_titles = do_google_serp_search(content_keywords)
    # Generate prompts
    try:
        content_title = generate_with_retry(model_pro, content_title.format(web_research_result=web_research_result)).text
        logger.info(f"The title of the content is: {content_title}")
    except Exception as err:
        logger.error(f"Content title Generation Error: {err}")
        return
    
    try:
        content_outline = generate_with_retry(model_pro, 
                        content_outline.format(content_title=content_title, web_research_result=web_research_result)).text
        logger.info(f"The content Outline is: {content_outline}\n\n")
    except Exception as err:
        logger.error(f"Failed to generate content outline: {err}")

    try:
        starting_draft = generate_with_retry(model_pro, 
                starting_prompt.format(content_title=content_title, content_outline=content_outline)).text
    except Exception as err:
        logger.error(f"Failed to Generate Starting draft: {err}")
        return
    
    try:
        logger.info(f"Starting to write on the outline introduction.")
        draft = starting_draft
        continuation = generate_with_retry(model, 
                continuation_prompt.format(content_title=content_title, 
                            content_outline=content_outline, content_text=draft, web_research_result=web_research_result)).text
    except Exception as err:
        logger.error(f"Failed to write the initial draft: {err}")

    # Add the continuation to the initial draft, keep building the story until we see 'IAMDONE'
    try:
        draft += '\n\n' + continuation
    except Exception as err:
        logger.error(f"Failed as: {err} and {continuation}")
    try:
        logger.info("Do web research with Tavily to provide context for content creation.")
        # Do Metaphor/Exa AI search.
        table_data = []
        web_research_result, m_titles, t_titles = do_tavily_ai_search(content_keywords)
        for item in web_research_result.get("results"):
            title = item.get("title", "")
            snippet = item.get("content", "")
            table_data.append([title, snippet])
        web_research_result = table_data 
    except Exception as err:
        logger.error(f"Failed to do Tavily AI search: {err}")
        return

    logger.info(f"Writing in progress... Current draft length: {len(draft)} characters")
    while 'IAMDONE' not in continuation:
        try:
            continuation = generate_with_retry(model,
                    continuation_prompt.format(content_title=content_title,
                    content_outline=content_outline, content_text=draft, web_research_result=web_research_result)).text
            draft += '\n\n' + continuation
            logger.info(f"Writing in progress... Current draft length: {len(draft)} characters")
        except Exception as err:
            logger.error(f"Failed to continually write the Essay: {err}")
            return
    
    # Remove 'IAMDONE' and print the final story
    final = draft.replace('IAMDONE', '').strip()

    blog_title, blog_meta_desc, blog_tags, blog_categories = blog_metadata(final,
            content_keywords, m_titles)

    generated_image_filepath = None
    # TBD: Save the blog content as a .md file. Markdown or HTML ?
    save_blog_to_file(final, blog_title, blog_meta_desc, blog_tags, blog_categories, generated_image_filepath)

    blog_frontmatter = f"""
    ---
    title: {blog_title}
    categories: [{blog_categories}]
    tags: [{blog_tags}]
    Meta description: {blog_meta_desc.replace(":", "-")}
    ---"""
    logger.info(f"\n{blog_frontmatter}{final}\n\n")
    logger.info(f"\n\n ################ Finished writing Blog for : {content_keywords} #################### \n")
