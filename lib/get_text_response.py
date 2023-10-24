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

import openai
from tqdm import tqdm, trange
import time
import re
from textwrap import dedent

from .gpt_providers.openai_gpt_provider import openai_chatgpt


def generate_detailed_blog(num_blogs, blog_keywords, niche, num_subtopics):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """
    # I want you to act as a blogger and you want to write a blog post about [topic], 
    # with a friendly and approachable tone that engages readers. 
    # Your target audience is [define your target audience]. 
    # Write in a personal style using singular first-person pronouns only. 
    # I want you to include these keywords: [keyword 1], [keyword 2], [keyword 3] throughout the article.
    # Format your response using markdown. 
    # Use headings, subheadings, bullet points, and bold to organize the information.
    # Answer the most commonly asked questions about the topic at the end of the article.
    # Create a list of the most popular tools used by the [Field of Interest] professionals with the pros and cons of each tool.

    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""

    # TBD: Check if the generated topics are equal to what user asked.
    blog_topic_arr = generate_blog_topics(blog_keywords, num_blogs, niche)
    print(f"Generated Blog Topics:---- {blog_topic_arr}\n")
    
    # For each of blog topic, generate content.
    for a_blog_topic in blog_topic_arr:
        # if md/html
        blog_markdown_str = "# " + a_blog_topic.replace('"', '') + "\n\n"
        # Get the introduction specific to blog title and sub topics.
        tpc_outlines = generate_topic_outline(a_blog_topic, num_subtopics)
        blog_intro = get_blog_intro(a_blog_topic, tpc_outlines)
        print(f"The intro is:\n {blog_intro}")
        blog_markdown_str = blog_markdown_str + "### Introduction" + "\n\n" + f"{blog_intro}" + "\n\n"
        # Now, for each blog we have sub topic. Generate content for each of the sub topic.
        for a_outline in tpc_outlines:
            sub_topic_content = generate_topic_content(blog_keywords, a_outline)
            print(f"Generating content for sub-topic: {a_outline}")
            # a_outline is sub topic heading, hence part ToC also.
            blog_markdown_str = blog_markdown_str + "\n\n" + f"### {a_outline}" + "\n\n"
            blog_markdown_str = blog_markdown_str + "\n" + f"\n {sub_topic_content}" + "\n\n"
            blog_markdown_str = blog_markdown_str + "\n" + "-------------------------" + "\n"

        # Get the Conclusion of the blog, by passing the generated blog.
        blog_conclusion = get_blog_conclusion(blog_markdown_str)
        blog_markdown_str = blog_markdown_str + "### Conclusion" + "\n" + f"{blog_conclusion}" + "\n"

        # print/check the final blog content.
        print(f"Final blog content: {blog_markdown_str}")
        blog_meta_desc = generate_blog_description(blog_markdown_str)
        print(f"\nGet the blog meta description:{blog_meta_desc}")
        blog_tags = get_blog_tags(blog_markdown_str)
        print(f"\nBlog tags for generated content: {blog_tags}")
        blog_categories = get_blog_categories(blog_markdown_str)
        print(f"Generated blog categories: {blog_categories}")

        # TBD: Save the blog content as a .md file. Markdown or HTML ?
        save_blog_to_file(blog_markdown_str, a_blog_topic, blog_meta_desc, blog_tags, blog_categories)

        exit(1)

    # Use chatgpt to convert the text into HTML or markdown.

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
    prompt = f"""As an SEO specialist and blog content writer, please write {num_blogs} catchy 
    and SEO-friendly blog topics on {blog_keywords}. The blog title must be less than 80 characters.
    """
    # Beware of keywords stuffing, clustering, semantic should help avoid.
    if num_blogs > 5:
        # Get more keywords, based on user given keywords.
        more_keywords = get_related_keywords(num_blogs, blog_keywords, niche)
        prompt = prompt + """Use the following keywords wisely, without keyword stuffing: {more_keywords}"""

    print(f"prompt used for blog titles: {prompt}\n")
    # Calculate the max tokens based on the number of blogs
    max_tokens = min(1000, num_blogs * 100)
    try:
        response = openai_chatgpt(
                prompt, 
                model="text-davinci-003", 
                temperature=0.1, 
                max_tokens=max_tokens, 
                top_p=1,
                n=1
                )
        topic_list = extract_key_text(response)
        return(topic_list)
    except Exception as err:
        SystemError(f"Error in generating blog topics: {err}")


def generate_topic_outline(blog_title, num_subtopics):
    """
    Given a blog title generate an outline for it
    """
    # TBD: Remove hardcoding, make dynamic
    prompt = f"""As a SEO expert, suggest only {num_subtopics} 
        beginner-friendly and insightful sub topic for the blog title: {blog_title}.
        """
    # The suggested {num_subtopics} outline should include few long-tailed keywords and most popular questions.
    # TBD: Include --niche
    print(f"prompt used for blog title Outline :{prompt}")
    # TBD: Add logic for which_provider and which_model
    response = openai_chatgpt(
            prompt,
            model="text-davinci-003",
            temperature=0.1,
            max_tokens=100,
            top_p=0.9,
            n=1
            )
    text_values = []
    for choice in response["choices"]:
        text_values.extend(choice["text"].split("\n"))
    return ([element for element in text_values if element])


def generate_topic_content(blog_keywords, sub_topic):
    """
    For each of given topic generate content for it.
    """
    # The outline should contain various subheadings and include the starting sentence for each section.
    # TBD: Depending on the usecase 'Voice and style' will change to professional etc.
    prompt = (f"As a professional blogger and topic authority on '{blog_keywords}',"
            f"craft factual (no more than 700 characters) blog content on {sub_topic}."
            "Your response should reflect Experience, Expertise, Authoritativeness, and Trustworthiness from content."
            "Voice and style guide: Write in a professional manner, giving enlightening details and reasons."
            "Use natural language and phrases that a real person would use: in normal conversations."
            "Format your response using markdown. Use headings, subheadings, bullet points, and bold to organize the information."
            )
    try:
        response = openai_chatgpt(prompt)
        response = openai_chatgpt(
            prompt,
            model="text-davinci-003",
            temperature=0.7,
            max_tokens=1000,
            top_p=0.9,
            n=1
            )
        text_values = []
        for choice in response["choices"]:
            text_values.extend(choice["text"].split("\n"))
        return (' '.join([element for element in text_values if element]))
    except Exception as err:
        SystemError(f"Error in generating topic content: {err}")

    return response.choices[0].text


def get_blog_intro(blog_title, blog_topics):
    """
    Generate blog introduction as per title and sub topics
    """
    prompt = f"""As a professional writer, craft a captivating, inviting, and concise (no more than 550 characters).
            The introduction should compel readers to delve deeper into the blog post,
            titled: {blog_title} with the following sub-topics: {blog_topics}
            """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(
            prompt,
            model="text-davinci-003",
            temperature=0.1,
            max_tokens=1000,
            top_p=0.9,
            n=1
            )
        text_values = []
        for choice in response["choices"]:
            text_values.extend(choice["text"].split("\n"))
        return (' '.join([element for element in text_values if element]))
    except Exception as err:
        SystemError(f"Error in generating topic content: {err}")


def get_blog_conclusion(blog_content):
    """
    Accepts a blog content and concludes it.
    """
    prompt = f"""As an expert SEO and blog writer, please conclude the given blog providing vital take aways,
            summarise key points (no more than 300 characters) in bullet points. The blog content: {blog_content}
            """
    print(f"Generating blog conclusion iwth prompt: {prompt}")
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(
            prompt,
            model="text-davinci-003",
            temperature=0.1,
            max_tokens=450,
            top_p=0.7,
            n=1
        )
        text_values = []
        for choice in response["choices"]:
            text_values.extend(choice["text"].split("\n"))
        return (' '.join([element for element in text_values if element]))
    except Exception as err:
        SystemError(f"Error in generating blog conclusion: {err}")


def generate_blog_description(blog_content):
    """
        Prompt designed to give SEO optimized blog descripton
    """
    # Suggest keywords that I should include in my meta description for my blog post on [topic]
    # I want to generate high CTR meta and keyword rich meta title and meta descriptions in text format. 
    # My keywords are – [keyword 1], [keyword 2], [keyword 3]
    # Suggest a meta description for the content above, make it user-friendly 
    # and with a call to action, include the keyword [keyword].
    prompt = f"""As an expert SEO and blog writer, write meta description for given blog content.
        The description should be between 150 and 160 characters long, uses strong, active verbs,
        avoids using all caps or excessive punctuation, and is relevant to the blog content.
        It should be engaging and encourages users to click on the link.
        The blog content: {blog_content}"""

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(
            prompt,
            model="text-davinci-003",
            temperature=0.1,
            max_tokens=450,
            top_p=0.7,
            n=1
        )
        text_values = []
        for choice in response["choices"]:
            text_values.extend(choice["text"].split("\n"))
        return (' '.join([element for element in text_values if element]))
    except Exception as err:
        SystemError(f"Error in generating blog description: {err}")


def get_blog_tags(blog_article):
    """
        Function to suggest tags for the given blog content
    """
    # Suggest at least 5 tags for the following blog post [Enter your blog post text here].
    prompt = f"""As an expert SEO and blog writer, suggest 3 to 5 relevant, specific, 
                and popular tags that are unique and consistent to improve the visibility 
                and discoverability of following blog content: {blog_article}"
            """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(
            prompt,
            model="text-davinci-003",
            temperature=0.1,
            max_tokens=450,
            top_p=0.7,
            n=1
        )   
        text_values = []
        for choice in response["choices"]:
            text_values.extend(choice["text"].split("\n"))
        return (' '.join([element for element in text_values if element]))
    except Exception as err:
        SystemError(f"Error in generating blog tags: {err}")


def get_blog_categories(blog_article):
    """
    Function to generate blog categories for given blog content.
    """
    prompt = f"""As an expert SEO and content writer, Suggest 2-3 blog categories by identifying 
            the main topic, most relevant categories, considering the target 
            audience and the blog's category taxonomy for the following blog content: {blog_article}"
            """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(
            prompt,
            model="text-davinci-003",
            temperature=0.1,
            max_tokens=100,
            top_p=0.7,
            n=1
        )   
        text_values = []
        for choice in response["choices"]:
            text_values.extend(choice["text"].split("\n"))
        return (' '.join([element for element in text_values if element]))
    except Exception as err:
        SystemError(f"Error in generating blog categories: {err}")


def save_blog_to_file(blog_content, blog_title, 
        blog_meta_desc, blog_tags, blog_categories, file_type="md"
        ):
    """ Common function to save the generated blog to a file.
    arg: file_type can be md or html
    """
    # TBD: This can come from config file.
    output_path = "pseo_website/_posts/"
    output_path = os.path.join(os.getcwd(), output_path)
    # Convert the spaces in blog_title with dash
    regex = re.compile('[^a-zA-Z0-9- ]')
    blog_title = regex.sub('', blog_title)
    blog_title = re.sub('--+', '-', blog_title)
    blog_title = blog_title.replace(' ', '-')

    if not os.path.exists(output_path):
        # If the directory does not exist, create it
        #os.makedirs(output_path)
        print("Error: Blog output directory is set to {output_path}, which Does Not Exist.")

    if file_type in "md":
        # fill the Front Matter as below at the top of the post: https://jekyllrb.com/docs/front-matter/
        # date: YYYY-MM-DD HH:MM:SS +/-TTTT
        formatted_date = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S %z}"
        blog_frontmatter = """---
                           title: {blog_title}
                           date: {formatted_date}
                           categories: [{blog_categories}]
                           tags: [{blog_tags}]
                           description: {blog_meta_desc}
                           img_path: '/posts/20180809'
                           ---\n\n"""

        # Create a new file named YYYY-MM-DD-TITLE.EXTENSION and put it in the _posts of the root directory. 
        # Please note that the EXTENSION must be one of md or markdown
        blog_output_path = os.path.join(
                output_path,
                f"{datetime.date.today().strftime('%Y-%m-%d')}-{blog_title}.md"
                )
        # Save the generated blog content to a file.
        try:
            with open(blog_output_path, "w") as f:
                f.write(dedent(blog_frontmatter))
                f.write(blog_content)
        except Exception as e:
            raise Exception(f"Failed to write blog content: {e}")
        print(f"\nSuccessfully saved and Posted blog at: {blog_output_path,}\n")


def extract_key_text(json_data):
    """Extracts key text from a given JSON object.
        Args:json_data: A JSON object.
        Returns: A list of strings containing the key text.
        Raises: ValueError: If the JSON object is not valid.
    """

    try:
        # Extract the "choices" key from the JSON object.
        choices = json_data["choices"]

        # Iterate over the "choices" list and extract the "text" key from each item.
        key_text = []
        for choice in choices:
            text = choice["text"]

            # Split the text into a list of sentences.
            sentences = text.split("\n")

            # Iterate over the list of sentences and extract the first sentence.
            for sentence in sentences:
                # The generated topics usually have 1) or ^\W*\D* . Remove them from prompt.
                new_str = sentence.replace("'", '')
                new_str = re.sub(r'^(\d*\.)', '', new_str)
                key_text.append(new_str)

        # Remove duplicate key text.
        key_text = list(set(key_text))
        # Remove empty values.
        key_text = [i for i in key_text if i]
        return key_text
    except KeyError as e:
        raise ValueError(f"Missing key in JSON object: {e.args[0]}")
    except TypeError as e:
        raise ValueError(f"Invalid JSON object: {e.args[0]}")


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
        response = openai_chatgpt(
                prompt,
                model="text-davinci-003",
                temperature=0.7,
                max_tokens=100,
                top_p=0.9,
                n=10 
                )

        # Extract the keywords from the response
        keywords = []
        for choice in response.choices:
            # Split the response into words
            words = choice.text.split(" ")

        # Add the words to the list of keywords
        for text in words:
            # Remove digits
            text = re.sub(r'\d', '', text)

            # Remove special characters
            text = re.sub(r'[^\w\s]', '', text)
            # Remove newline characters
            text = text.replace('\n', '')

            keywords.append(text)

        # Remove any duplicate keywords
        keywords = set(keywords)

        # Return the list of keywords
        return (' '.join(keywords))
    except Exception as err:
        SystemError(f"Error in getting related keywords.")
