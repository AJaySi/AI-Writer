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
import nltk
nltk.download('punkt', quiet=True)
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)

from .gpt_providers.openai_gpt_provider import openai_chatgpt, gen_new_from_given_img
from .gpt_providers.openai_gpt_provider import analyze_and_extract_details_from_image
from .generate_image_from_prompt import generate_image
from .write_blogs_from_youtube_videos import youtube_to_blog
from .wordpress_blog_uploader import compress_image, upload_blog_post, upload_media

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

# fixme: Remove the hardcoding, need add another option OR in config ?
image_dir = "pseo_website/assets/"
image_dir = os.path.join(os.getcwd(), image_dir)
# TBD: This can come from config file.
output_path = "pseo_website/_posts/"
output_path = os.path.join(os.getcwd(), output_path)
wordpress_url = 'https://latestaitools.in/'
wordpress_username = 'upaudel750'
wordpress_password = 'YvCS VbzQ QSp8 4XZe 0DUw Myys'


def generate_youtube_blog(yt_url_list):
    """Takes a list of youtube videos and generates blog for each one of them.
    """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""
    for a_yt_url in yt_url_list:
        try:
            yt_img_path, yt_blog = youtube_to_blog(a_yt_url)

            # Get the title and meta description of the blog.
            title = generate_blog_title(yt_blog)
            blog_meta_desc = generate_blog_description(yt_blog)
            logger.info(f"Title is {title} and description is {blog_meta_desc}")
            #blog_markdown_str = "# " + title.replace('"', '') + "\n\n"
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
            print(f"Conclusion: {blog_markdown_str}")
            
            # Get blog tags and categories.
            blog_tags = get_blog_tags(yt_blog)
            logger.info(f"Blog tags are: {blog_tags}")
            blog_categories = get_blog_categories(yt_blog)
            logger.info(f"Blog categories are: {blog_categories}")

            save_blog_to_file(blog_markdown_str, title, blog_meta_desc, blog_tags, blog_categories, main_img_path)
            if 'html' in output_format:
                blog_markdown_str = convert_markdown_to_html(blog_markdown_str)

            save_blog_to_file(blog_markdown_str, title, blog_meta_desc, blog_tags, blog_categories, main_img_path)
            #print(html_blog)

        except Exception as e:
            # raise assertionerror
            logger.info(f"Error: Failed to generate_youtube_blog: {e}")
            exit(1)


def generate_detailed_blog(num_blogs, blog_keywords, niche, num_subtopics,
        wordpress=False, output_format="HTML"):
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
        print(f"\n\n 1 -- BLOG_STR : {blog_markdown_str}\n\n")
        # Now, for each blog we have sub topic. Generate content for each of the sub topic.
        for a_outline in tpc_outlines:
            a_outline = a_outline.replace('"', '')
            logger.info(f"Generating content for sub-topic: {a_outline}")
            sub_topic_content = generate_topic_content(blog_keywords, a_outline)
            # a_outline is sub topic heading, hence part ToC also.
            #blog_markdown_str = blog_markdown_str + "\n\n" + f"### {a_outline}" + "\n\n"
            blog_markdown_str = blog_markdown_str + "\n" + f"\n {sub_topic_content}" + "\n\n"
            print(f"\n\n 3 -- BLOG_STR : {blog_markdown_str}\n\n")

        # Get the Conclusion of the blog, by passing the generated blog.
        blog_conclusion = get_blog_conclusion(blog_markdown_str)
        blog_markdown_str = blog_markdown_str + "### Conclusion" + "\n" + f"{blog_conclusion}" + "\n"

        # logger.info/check the final blog content.
        logger.info(f"Final blog content: {blog_markdown_str}")

        blog_meta_desc = generate_blog_description(blog_markdown_str)
        logger.info(f"\nThe blog meta description is:{blog_meta_desc}\n")

        # Generate an image based on meta description
        logger.info(f"Calling Image generation with prompt: {blog_meta_desc}")
        main_img_path = generate_image(blog_meta_desc, image_dir, "dalle3")
        
        blog_tags = get_blog_tags(blog_markdown_str)
        logger.info(f"\nBlog tags for generated content: {blog_tags}")

        blog_categories = get_blog_categories(blog_markdown_str)
        logger.info(f"Generated blog categories: {blog_categories}")

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


def generate_blog_title(blog_meta_desc):
    """
    Given a blog title generate an outline for it
    """
    # TBD: Remove hardcoding, make dynamic
    prompt = f"""As a SEO expert and content writer, I will provide you with blog. Your task is write title for it.
        Follows SEO best practises to suggest the blog title. 
        Please keep the titles concise, not exceeding 60 words, and ensure to maintain their meaning. 
        Respond with only one title and no description, for this given blog content: {blog_meta_desc}
        """
    # The suggested {num_subtopics} outline should include few long-tailed keywords and most popular questions.
    # TBD: Include --niche
    logger.debug(f"Prompt used for blog title :{prompt}")
    try:
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating Blog Title: {err}")
    return response


def generate_topic_outline(blog_title, num_subtopics):
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


def generate_blog_description(blog_content):
    """
        Prompt designed to give SEO optimized blog descripton
    """
    prompt = f"""As an expert SEO and blog writer, Compose a compelling meta description for the given blog content, 
        adhering to SEO best practices. Keep it between 150-160 characters, incorporating active verbs, 
        avoiding all caps and excessive punctuation. Ensure relevance, engage users, and encourage clicks.
        Use keywords naturally and provide a glimpse of the content's value to entice readers.
        Respond with only one of your best effort and do not include your explanations. 
        Blog Content: {blog_content}"""

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in generating blog description: {err}")


def get_blog_tags(blog_article):
    """
        Function to suggest tags for the given blog content
    """
    # Suggest at least 5 tags for the following blog post [Enter your blog post text here].
    prompt = f"""As an expert SEO and blog writer, suggest only 2 relevant and specific blog tags
         for the given blog content. Only reply with comma separated values. 
         Blog content:  {blog_article}."""

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating blog tags: {err}")
    else:
        return response


def get_blog_categories(blog_article):
    """
    Function to generate blog categories for given blog content.
    """
    prompt = f"""As an expert SEO and content writer, I will provide you with blog content.
            Suggest only 2 blog categories which are most relevant to provided blog content,
            by identifying the main topic. Also consider the target audience and the
            blog's category taxonomy. Only reply with comma separated values. The blog content is: {blog_article}"
            """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating blog categories: {err}")
    else:
        return response


def save_blog_to_file(blog_content, blog_title, 
        blog_meta_desc, blog_tags, blog_categories, main_img_path, file_type="md"):
    """ Common function to save the generated blog to a file.
    arg: file_type can be md or html
    """
    # Convert the spaces in blog_title with dash
    logger.info(f"The blog will be saved at: {output_path}")
    logger.debug(f"Blog Title is: {blog_title}")
    blog_title_md = blog_title
    regex = re.compile('[^a-zA-Z0-9- ]')
    blog_title_md = regex.sub('', blog_title_md)
    blog_title= blog_title.replace(":", "")
    blog_title_md = re.sub('--+', '-', blog_title_md)
    blog_title_md = blog_title_md.replace(' ', '-')
    blog_title_md = remove_stop_words(blog_title_md)

    if ':' in blog_meta_desc:
        blog_meta_desc  = blog_meta_desc.split(':')[1].strip()

    if not os.path.exists(output_path):
        logger.error("Error: Blog output directory is set to {output_path}, which Does Not Exist.")

    # Different output formats are plaintext, html and markdown.
    if file_type in "md":
        logger.info(f"Writing/Saving the resultant blog content in Markdown format.")
        # fill the Front Matter as below at the top of the post: https://jekyllrb.com/docs/front-matter/
        # date: YYYY-MM-DD HH:MM:SS +/-TTTT
        from zoneinfo import ZoneInfo
        tz=ZoneInfo('Asia/Kolkata')
        dtobj = datetime.datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        formatted_date = f"{dtobj.strftime('%Y-%m-%d %H:%M:%S %z')}"

        blog_frontmatter = f"""\
                        ---
                        title: {blog_title}
                        date: {formatted_date}
                        categories: [{blog_categories}]
                        tags: [{blog_tags}]
                        description: {blog_meta_desc}
                        img_path: '/assets/'
                        image:
                            path: {os.path.basename(main_img_path)}
                            alt: {blog_title}
                        ---\n\n"""

        # Create a new file named YYYY-MM-DD-TITLE.EXTENSION and put it in the _posts of the root directory. 
        # Please note that the EXTENSION must be one of md or markdown
        blog_output_path = os.path.join(
                output_path,
                f"{datetime.date.today().strftime('%Y-%m-%d')}-{blog_title_md}.md"
                )
        # Save the generated blog content to a file.
        try:
            with open(blog_output_path, "w") as f:
                f.write(dedent(blog_frontmatter))
                f.write(blog_content)
        except Exception as e:
            raise Exception(f"Failed to write blog content: {e}")
        logger.info(f"\nSuccessfully saved and Posted blog at: {blog_output_path,}\n")


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


# Helper function
def remove_stop_words(sentence):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)

    # Get the list of English stop words
    stop_words = set(stopwords.words('english'))

    # Remove stop words from the sentence
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Join the filtered words back into a sentence
    filtered_sentence = ' '.join(filtered_words)

    return filtered_sentence


def convert_markdown_to_html(md_content):
    """ Helper function to convert given text to HTML
    """
    prompt =f"""
			You are a skilled web developer tasked with converting a Markdown-formatted text to HTML. 
            You will be given text in markdown format. Follow these steps to perform the conversion:
			
			1. Parse User's Markdown Input: You will receive a Markdown-formatted text as input from the user. 
            Carefully analyze the provided Markdown text, paying attention to different elements such as headings (#), 
            lists (unordered and ordered), bold and italic text, links, images, and code blocks.
			2. Generate and Validate HTML: Generate corresponding HTML code for each Markdown element following 
            the conversion guidelines below. Ensure the generated HTML is well-structured and syntactically correct.
			3. Preserve Line Breaks: Markdown line breaks (soft breaks) represented by two spaces at the end of a 
            line should be converted to <br> tags in HTML to preserve the line breaks.
			4. REMEMBER to generate complete, valid HTML response only.
			
			Follow below Conversion Guidelines:
			- Headers: Convert Markdown headers (#, ##, ###, etc.) to corresponding HTML header tags (<h1>, <h2>, <h3>, etc.).
			- Lists: Convert unordered lists (*) and ordered lists (1., 2., 3., etc.) to <ul> and <ol> HTML tags, respectively. 
            List items should be enclosed in <li> tags.
			- Emphasis: Convert bold (**) and italic (*) text to <strong> and <em> HTML tags, respectively.
			- Links: Convert Markdown links ([text](url)) to HTML anchor (<a>) tags. Ensure the href attribute contains the correct URL.
			- Images: Convert Markdown image tags (![alt text](image_url)) to HTML image (<img>) tags. 
            Include the alt attribute for accessibility.
			- Code: Convert inline code (`code`) to <code> HTML tags. Convert code blocks (```) to <pre> HTML tags 
            for preserving formatting.
			- Blockquotes: Convert blockquotes (>) to <blockquote> HTML tags.
			Convert the following Markdown text to HTML:  {md_content}
            """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in getting related keywords.")
