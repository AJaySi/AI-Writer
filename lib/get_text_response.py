########################################################################
#
# Common module for getting response from gpt for given prompt.
# This module includes following capabilities:
# 
#
#
########################################################################

import json
import os
import datetime #I wish
import sys

import openai
from tqdm import tqdm, trange
import time
import re
from textwrap import dedent

from .gpt_providers.openai_gpt_provider import gen_new_from_given_img
from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gpt_vision_img_details import analyze_and_extract_details_from_image
from .generate_image_from_prompt import generate_image
from .write_blogs_from_youtube_videos import youtube_to_blog
from .wordpress_blog_uploader import compress_image, upload_blog_post, upload_media
from .gpt_online_researcher import do_online_research
from .save_blog_to_file import save_blog_to_file
from .optimize_images_for_upload import optimize_image
from .combine_research_and_blog import blog_with_research
from .get_blog_meta_desc import generate_blog_description
from .get_blog_title import generate_blog_title
from .get_tags import get_blog_tags
from .get_blog_category import get_blog_categories
from .convert_content_to_markdown import convert_tomarkdown_format
from .convert_markdown_to_html import convert_markdown_to_html
from .utils.youtube_keyword_research import research_yt
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

# Load configuration
#with open('config.json') as config_file:
#    config = json.load(config_file)

#wordpress_url = config['wordpress_url']
# fixme: Remove the hardcoding, need add another option OR in config ?
image_dir = "blog_images"
image_dir = os.path.join(os.getcwd(), image_dir)
# TBD: This can come from config file.
output_path = "blogs"
output_path = os.path.join(os.getcwd(), output_path)
wordpress_url = ''
wordpress_username = ''
wordpress_password = ''

def generate_youtube_blog(yt_url_list, output_format="markdown"):
    """Takes a list of youtube videos and generates blog for each one of them.
    """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""
    if isinstance(yt_url_list, str):
        yt_url_list = [yt_url_list]
    for a_yt_url in yt_url_list:
        try:
            logger.info(f"Starting to write blog on URL: {a_yt_url}")
            blog_markdown_str, yt_title = youtube_to_blog(a_yt_url)
            logger.warning("\n\n--------------- First Draft of the Blog: --------\n\n")
            logger.info(f"{blog_markdown_str}\n")
            logger.warning("--------------------END of First draft----------\n\n")
            if not yt_title or not blog_markdown_str:
                logger.error("No content or title for audio to proceed.")
                sys.exit(1)
        except Exception as e:
            logger.error(f"Error in youtube_to_blog: {e}")
            sys.exit(1)

        try:
            logger.info(f"Starting with online research for URL title: {yt_title}")
            research_report = do_online_research(yt_title)
            if not research_report:
                logger.error(f"Error in do_online_research returned no report: {e}")
                sys.exit(1)
            logger.warning(f"\n\n---------------Online Research Report: {yt_title} --------\n\n")
            logger.info(f"{research_report}\n")
            logger.warning("--------------------END of Research Report----------\n\n")
        except Exception as e:
            logger.error(f"Error in do_online_research: {e}")
            sys.exit(1)

        try:
            logger.info("Preparing a blog content from audio script and online research content...")
            blog_markdown_str = blog_with_research(research_report, blog_markdown_str)
            logger.warning("\n\n--------------- Second Blog Draft after online research: --------\n\n")
            logger.info(f"{blog_markdown_str}\n")
            logger.warning("--------------------END of Second draft----------\n\n")
        except Exception as e:
            logger.error(f"Error in blog_with_research: {e}")
            sys.exit(1)

        try:
            # Get the title and meta description of the blog.
            logger.info("Generating Blog Description.")
            blog_meta_desc = generate_blog_description(blog_markdown_str, "gemini")
            logger.info("Generating Blog Title.")
            title = generate_blog_title(blog_meta_desc, "gemini")
            logger.info(f"Title is {title} and description is {blog_meta_desc}")
            # Regex pattern to match 'Title:', 'title:', 'TITLE:', etc., followed by optional whitespace
            title = re.sub(re.compile(r'(?i)title:\s*'), '', title)
            #blog_markdown_str = "# " + title.replace('"', '') + "\n\n"

            # Get blog tags and categories.
            blog_tags = get_blog_tags(blog_meta_desc, "gemini")
            logger.info(f"Blog tags are: {blog_tags}")
            blog_categories = get_blog_categories(blog_meta_desc, "gemini")
            logger.info(f"Blog categories are: {blog_categories}")

            # Generate an introduction for the blog
            #blog_intro = get_blog_intro(title, blog_markdown_str)
            #logger.info(f"The Blog intro is:\n {blog_intro}")
            #blog_markdown_str = blog_markdown_str + "\n\n" + f"{blog_intro}" + "\n\n"

            # Generate an image based on meta description
            logger.info(f"Calling Image generation with prompt: {blog_meta_desc}")
            main_img_path = generate_image(blog_meta_desc, image_dir, "dalle3")
            main_img_path = optimize_image(main_img_path)

            # Get a variation of the yt url screenshot to use in the blog.
            #varied_img_path = gen_new_from_given_img(yt_img_path, image_dir)
            #logger.info(f"Image path: {main_img_path} and varied path: {varied_img_path}")
            #blog_markdown_str = blog_markdown_str + f'![img-description]({os.path.basename(varied_img_path)})' + f'_{yt_title}_'

            #stbdiff_img_path = generate_image(yt_img_path, image_dir, "stable_diffusion")
            #logger.info(f"Image path: {main_img_path} from stable diffusion: {stbdiff_img_path}")
            #blog_markdown_str = blog_markdown_str + f'![img-description]({os.path.basename(stbdiff_img_path)})' + f'_{yt_title}_'
            
            # Add the body of the blog content.
            #blog_markdown_str = blog_markdown_str + "\n\n" + f'{yt_blog}' + "\n\n"
            # Get the Conclusion of the blog, by passing the generated blog.
            #blog_conclusion = get_blog_conclusion(blog_markdown_str)
            # TBD: Add another image.
            #blog_markdown_str = blog_markdown_str + "### Conclusion" + "\n\n" + f"{blog_conclusion}" + "\n"

            # Proofread the blog, edit and remove dubplicates and refine it further.
            # Presently, fixing the blog keywords to be tags and categories.
            #blog_keywords = f"{blog_tags} + {blog_categories}"
            #blog_markdown_str = blog_proof_editor(blog_markdown_str, blog_keywords)
            #logger.warning("\n\n--------------- 3rd draft after proofreading: --------\n\n")
            #logger.info(f"{blog_markdown_str}\n")
            #logger.warning("--------------------END of 3rd draft----------\n\n")

            # Check the type of blog format needed by the user.
            if 'html' in output_format:
                logger.info("Converting final blog to HTML format.")
                blog_markdown_str = convert_markdown_to_html(blog_markdown_str)
            elif 'markdown' in output_format:
                logger.info("Converting final blog to Markdown style.")
                blog_markdown_str = convert_tomarkdown_format(blog_markdown_str)

            logger.warning("\n\n--------------- Final Blog Content: --------\n\n")
            logger.info(f"{blog_markdown_str}\n")
            logger.warning("--------------------END of Blog Content----------\n\n")


            # Try to save the blog content in a file, in whichever format. Just dump it.
            try:
                save_blog_to_file(blog_markdown_str, title, blog_meta_desc, 
                        blog_tags, blog_categories, main_img_path, output_path)
            except Exception as err:
                logger.error(f"Failed to Save blog content: {err}")

        except Exception as e:
            # raise assertionerror
            logger.error(f"Error: Failed to generate_youtube_blog: {e}")
            exit(1)


def generate_detailed_blog(num_blogs, blog_keywords, niche, num_subtopics,
        wordpress=False, research_online=False, output_format="HTML"):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""

    # TBD: Check if the generated topics are equal to what user asked.
    blog_topic_arr = generate_blog_topics(blog_keywords, num_blogs, niche)
    logger.info(f"Generated Blog Topics:---- \n{blog_topic_arr}\n")
    # Split the string at newlines
    blog_topic_arr = blog_topic_arr.split('\n')

    # For each of blog topic, generate content.
    for a_blog_topic in blog_topic_arr:
        # if md/html
        a_blog_topic = a_blog_topic.replace('"', '')
        a_blog_topic = re.sub(r'^[\d.\s]+', '', a_blog_topic)
        blog_markdown_str = "# " + a_blog_topic + "\n\n"
        
        # Get the introduction specific to blog title and sub topics.
        tpc_outlines = generate_topic_outline(a_blog_topic, num_subtopics)
        tpc_outlines = tpc_outlines.split("\n")
        
        blog_intro = get_blog_intro(a_blog_topic, tpc_outlines)
        logger.info(f"The intro is:\n{blog_intro}")
        blog_markdown_str = blog_markdown_str + "### Introduction" + "\n\n" + f"{blog_intro}" + "\n\n"
        
        # Now, for each blog we have sub topic. Generate content for each of the sub topic.
        for a_outline in tpc_outlines:
            a_outline = a_outline.replace('"', '')
            logger.info(f"Generating content for sub-topic: {a_outline}")
            sub_topic_content = generate_topic_content(blog_keywords, a_outline)
            # a_outline is sub topic heading, hence part ToC also.
            #blog_markdown_str = blog_markdown_str + "\n\n" + f"### {a_outline}" + "\n\n"
            blog_markdown_str = blog_markdown_str + "\n" + f"\n {sub_topic_content}" + "\n\n"

        # Get the Conclusion of the blog, by passing the generated blog.
        blog_conclusion = get_blog_conclusion(blog_markdown_str)
        blog_markdown_str = blog_markdown_str + "### Conclusion" + "\n" + f"{blog_conclusion}" + "\n"

        # logger.info/check the final blog content.
        logger.info(f"Final blog content: {blog_markdown_str}")

        #if research_online:
        #    # Call on the got-researcher, tavily apis for this. So many apis floating around.
        #    report = do_online_research_on(blog_keywords)
        #    blog_markdown_str = blog_with_research(report, blog_markdown_str)

        blog_meta_desc = generate_blog_description(blog_markdown_str)
        logger.info(f"\nThe blog meta description is:{blog_meta_desc}\n")

        # Generate an image based on meta description
        logger.info(f"Calling Image generation with prompt: {blog_meta_desc}")
        main_img_path = generate_image(blog_meta_desc, image_dir, "dalle3")
        
        blog_tags = get_blog_tags(blog_markdown_str)
        logger.info(f"\nBlog tags for generated content: {blog_tags}\n")

        blog_categories = get_blog_categories(blog_markdown_str)
        logger.info(f"Generated blog categories: {blog_categories}\n")

        # Use chatgpt to convert the text into HTML or markdown.
        if 'html' in output_format:
            blog_markdown_str = convert_markdown_to_html(blog_markdown_str)

        # Check if blog needs to be posted on wordpress.
        if wordpress:
            # Fixme: Fetch all tags and categories to check, if present ones are present and
            # use them else create new ones. Its better to use chatgpt than string comparison.
            # Similar tags and categories will be missed.
            # blog_categories = 
            # blog_tags = 
            logger.info("Uploading the blog to wordpress.\n")
            main_img_path = compress_image(main_img_path, quality=85)
            try:
                img_details = analyze_and_extract_details_from_image(main_img_path)
                alt_text = img_details.get('alt_text')
                img_description = img_details.get('description')
                img_title = img_details.get('title')
                caption = img_details.get('caption')
                try:
                    media = upload_media(wordpress_url, wordpress_username, wordpress_password, 
                        main_img_path, alt_text, img_description, img_title, caption)
                except Exception as err:
                    sys.exit(f"Error occurred in upload_media: {err}")
            except Exception as e:
                sys.exit(f"Error occurred in analyze_and_extract_details_from_image: {e}")

            # Then create the post with the uploaded media as the featured image
            media_id = media['id']
            blog_markdown_str = convert_markdown_to_html(blog_markdown_str)
            try:
                upload_blog_post(wordpress_url, wordpress_username, wordpress_password, a_blog_topic, 
                        blog_markdown_str, media_id, blog_meta_desc, blog_categories, blog_tags, status='publish')
            except Exception as err:
                sys.exit(f"Failed to upload blog to wordpress.Error: {err}")

        # TBD: Save the blog content as a .md file. Markdown or HTML ?
        save_blog_to_file(blog_markdown_str,
                a_blog_topic,
                blog_meta_desc, blog_tags,
                blog_categories, main_img_path)

    # Now, we need perform some *basic checks on the blog content, such as:
    # is_content_ai_generated.py, plagiarism_checker_from_known_sources.py
    # seo_analyzer.py . These are present in the lib folder.
    # prompt: Rewrite, improve and paraphrase [text] and use headings and subheadings 
    # to break up the content and make it easier to read using the keyword [keyword].



def generate_blog_topics(blog_keywords, num_blogs, niche):
    """
    For a given prompt, generate blog topics.
    Using the davinci-instruct-beta-v3 model. It’s proven to be an ideal 
    one for generating unique blog content.
    Ex: Generate SEO optimized blog topics on given keywords
    """
    prompt = f"""As an SEO specialist and blog writer, write {num_blogs} catchy
    and SEO-friendly blog topics on {blog_keywords}. The blog title must be less than 80 characters.
    The blog titles must follow best SEO practises, be engaging and invite/tempt users to read full blog.
    Do not include descriptions, explanations. Do not number the result."""

    # Beware of keywords stuffing, clustering, semantic should help avoid.
    if num_blogs > 5:
        # Get more keywords, based on user given keywords.
        more_keywords = get_related_keywords(num_blogs, blog_keywords, niche)
        prompt = prompt + """Use the following keywords wisely, without keyword stuffing: {more_keywords}"""

    logger.info(f"Prompt used for generating blog topics: \n{prompt}\n")
    try:
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in generating blog topics: {err}")


    """
    Given a blog title generate an outline for it
    """
    # TBD: Remove hardcoding, make dynamic
    prompt = f"""As a SEO expert, suggest only {num_subtopics} beginner-friendly and 
        insightful sub topics for the blog title: {blog_title}.
        Respond with only answer and no description, explanations."""

    # The suggested {num_subtopics} outline should include few long-tailed keywords and most popular questions.
    # TBD: Include --niche
    logger.info(f"Prompt used for blog title Outline :\n{prompt}\n")
    # TBD: Add logic for which_provider and which_model
    try:
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating Blog Title: {err}")
    return response


def generate_topic_content(blog_keywords, sub_topic):
    """
    For each of given topic generate content for it.
    """
    # The outline should contain various subheadings and include the starting sentence for each section.
    # TBD: Depending on the usecase 'Voice and style' will change to professional etc.
    prompt = f"""As a professional blogger and topic authority on {blog_keywords},
            craft factual (no more than 200 characters) subtopic content on {sub_topic}.
            Your response should reflect Experience, Expertise, Authoritativeness and Trustworthiness from content.
            Voice and style guide: Write in a professional manner, giving enlightening details and reasons.
            Use natural language and phrases that a real person would use: in normal conversations.
            Format your response using markdown. REMEMBER Not to include introduction or conclusion in your response.
            Use headings(h3 to h6 only), subheadings, bullet points, and bold to organize the information."""
    logger.info(f"Generate topic content using prompt:\n{prompt}\n")
    try:
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in generating topic content: {err}")


def get_blog_intro(blog_title, blog_topics):
    """
    Generate blog introduction as per title and sub topics
    """
    prompt = f"""As a skilled wordsmith, I'll equip you with a blog title and relevant topics, tasking you with crafting an engaging introduction. Your challenge: Create a brief, compelling entry that entices readers to explore the entire post. This introduction must be concise (under 250 characters) yet powerful, clearly stating the blog's purpose and what readers stand to gain. Reply with only the introduction.

Intrigue your audience from the start with vibrant language, employing strong verbs and vivid descriptions. Address a common challenge your readers face, demonstrating empathy and positioning yourself as their go-to expert. Pose thought-provoking questions that prompt reader engagement and contemplation.

Remember, your words matter. This introduction serves as the cornerstone of the blog post. It should not only captivate attention but also encourage deeper exploration. Additionally, strategically integrate relevant keywords to enhance visibility on search engine results pages (SERPs). Your mission: Craft a blog introduction that resonates, leaving readers eager to delve further into the titled piece: '{blog_title}', covering these sub-topics: {blog_topics}."""

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating Blog Introduction: {err}")
    return response


def get_blog_conclusion(blog_content):
    """
    Accepts a blog content and concludes it.
    """
    prompt = f"""As an expert SEO and blog writer, please conclude the given blog providing vital take aways,
            summarise key points (no more than 300 characters) in bullet points. The blog content: {blog_content}
            """
    logger.info(f"Generating blog conclusion iwth prompt: {prompt}")
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating blog conclusion: {err}")
    else:
        return response


def get_related_keywords(num_blogs, keywords, niche):
    """
    Helper function to get more keywords from GPTs.
    """
    # Check if niche: use long tailed, else use popular keywords.
    if niche:
        prompt = (f"Generate a list without description of the top {num_blogs} most popular and semantically"
                f"related long-tailed keywords and entities for the topic of {keywords} that are used in"
                "high-quality content and relevant to my competitors."
                )
    else:
        prompt = (f"Generate a list without description of the top {num_blogs} most popular and"
                f" semantically related keywords and entities for the topic of {keywords} that are used"
                " in high-quality content and relevant to my competitors."
                )
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in getting related keywords.")


def blog_proof_editor(blog_content, blog_keywords):
    """
        Helper for blog proof reading.
    """
    if not blog_content and not blog_keywords:
        logger.error("Blog proof reader has no content to proofread.")
        exit(1)

    prompt = f"""I am looking for detailed editing and enhancement of the given blog post, 
        with a particular focus on originality. I will provide you with a blog content and its keywords. 
        The keywords for the blog are [{blog_keywords}]. Please go through the blog and make direct edits to improve it, 
        ensuring the final output is both high-quality and original. 
        Note: There are duplicates headings and corresponding paragraphs, rewrite into one subheading.

        Here are the specific guidelines to focus on:

        1). Ensure Originality: Edit any sections that lack originality, replacing them with unique and creative content.
        2). Eliminate Repetitive Language: Rewrite repetitive phrases with varied and engaging language.
        3). Vocabulary and Grammar Enhancement: Directly correct any grammatical errors and upgrade the 
        vocabulary for better readability.
        4). Improve Sentence Structure: Enhance sentence construction for better clarity and flow.
        5). Tone and Brand Alignment: Adjust the tone, voice, personality of given content to make it unique.
        6). Optimize Content Structure: Reorganize the content for a more impactful presentation, 
        including better paragraphing and transitions.
        7). Remove Redundancies: Important, Cut out any redundant information or overly complex jargon.
        8). Refine Overall Structure: Make structural changes to improve the overall impact of the content.
        9). Remember, rewrite all content that repeated, while maintaining the formatting of the given blog text.
        10). Remember Not to include SEO meta description and Title in your final response.
        11). REMEMBER to maintain the formatting style of the provided blog.
        12). Judge if the given blog is about technology then provide code snippets and examples for it.

        Please make direct changes as per above guideline to the provided blog text below: 
        [{blog_content}]. """

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error Blog Proof Reading: {err}")
