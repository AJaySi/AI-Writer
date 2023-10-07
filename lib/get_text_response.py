########################################################################
#
# Common module for getting response from gpt for given prompt.
# This module includes following capabilities:
# 
#
#
########################################################################

import openai
from tqdm import tqdm, trange
import time
import re


def get_prompt_reply(prompt, max_token, outputs=1):
    try:
        # using OpenAI's Completion module that helps execute
        # any tasks involving text
        response = openai.Completion.create(
            # model name used here is text-davinci-003
            # there are many other models available under the
            # umbrella of GPT-3
            model="text-davinci-003",
            # passing the user input
            prompt=prompt,
            # generated output can have "max_tokens" number of tokens
            max_tokens=max_token,
            # number of outputs generated in one call
            n=outputs
    )
    except openai.error.Timeout as e:
       #Handle timeout error, e.g. retry or log
       print(f"OpenAI API request timed out: {e}")
       pass
    except openai.error.APIError as e:
       #Handle API error, e.g. retry or log
       print(f"OpenAI API returned an API Error: {e}")
       pass
    except openai.error.APIConnectionError as e:
       #Handle connection error, e.g. check network or log
       print(f"OpenAI API request failed to connect: {e}")
       pass
    except openai.error.InvalidRequestError as e:
       #Handle invalid request error, e.g. validate parameters or log
       print(f"OpenAI API request was invalid: {e}")
       pass
    except openai.error.AuthenticationError as e:
       #Handle authentication error, e.g. check credentials or log
       print(f"OpenAI API request was not authorized: {e}")
       pass
    except openai.error.PermissionError as e:
       #Handle permission error, e.g. check scope or log
       print(f"OpenAI API request was not permitted: {e}")
       pass
    except openai.error.RateLimitError as e:
       #Handle rate limit error, e.g. wait or log
       print(f"OpenAI API request exceeded rate limit: {e}")
       pass

    print(f"Prompt output: {response.choices[0].text.strip()}")
    # creating a list to store all the outputs
    output = list()
    for k in response['choices']:
        output.append(k['text'].strip())
    return output


def generate_detailed_blog(blog_keywords):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """

    # TBD
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
    blog_topic_arr = list(generate_blog_topics(blog_keywords).split("\n"))
    # Remove null values and incomplete results.
    while('' in blog_topic_arr):
        blog_topic_arr.remove('')

    print(f"Generated Blog Topics:---- {blog_topic_arr}")
    
    # For each of blog topic, generate content.
    for a_blog_topic in blog_topic_arr:
        # Error in generating topic content: Rate limit reached for default-global-with-image-limits 
        # in free account on requests per min. Limit: 3 / min. Please try again in 20s.
        for i in trange(30):
            time.sleep(1)
        # The generated topics usually have 1) or ^\W*\D* . Remove them from prompt.
        a_topic = re.sub(r"^\W*\D*", "", a_blog_topic)
        
        tpc_cnt = generate_topic_content(a_topic)
        print(f"{a_topic} ------ {tpc_cnt}")

        # We now need to concatenate all the sections and sew it into blog content.
        tmp_blog_markdown_str = blog_markdown_str + " " + a_blog_topic + " " + f"{tpc_cnt}"
        blog_markdown_str = blog_markdown_str + a_blog_topic + "\n\n" + f"{tpc_cnt}" + "\n\n"

    # print/check the final blog content.
    print(f"Final blog content: {blog_markdown_str}")
    # Save the blog content as a .md file. Markdown or HTML ?
    # Use chatgpt to convert the text into HTML or markdown.

    # Now, we need perform some *basic checks on the blog content, such as:
    # is_content_ai_generated.py, plagiarism_checker_from_known_sources.py
    # seo_analyzer.py . These are present in the lib folder.
    # prompt: Rewrite, improve and paraphrase [text] and use headings and subheadings to break up the content and make it easier to read using the keyword [keyword].



def generate_blog_topics(blog_keywords):
    """
    For a given prompt, generate blog topics.
    Using the davinci-instruct-beta-v3 model. It’s proven to be an ideal 
    one for generating unique blog content.
    Ex: Generate SEO optimized blog topics on AI text to image with Python
    """
    # Prompt engineering, huh ?
    # Create a blog post about “{blogPostTopic}” . Write it in a “{tone}” tone. Use transition words. 
    # Use active voice. Write over 1000 words. The blog post should be in a beginners guide style. 
    # Add title and subtitle for each section. It should have a minimum of 6 sections. 
    # Include the following keywords: “{keywords}”. Create a good slug for this post and a 
    # meta description with a maximum of 100 words. and add it to the end of the blog post

    prompt = f"As an experienced AI scientist and technical writer, generate SEO optimized blog topics about {blog_keywords}."
    #prompt = "Generate SEO optimized blog topics for" + " " + f"{blog_keywords}"
    try:
        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=prompt,
            temperature=0.7,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text
    except Exception as err:
        print(f"Error in generating blog topics: {err}")


def generate_topic_content(prompt):
    """
    For each of given topic generate content for it.
    """
    try:
        # Generate a blog post outline for the following topic: {topic}. 
        # The outline should contain various subheadings and include the starting sentence for each section.
        prompt = f"As an experienced AI researcher and technical writer, blog about {prompt}."
        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as err:
        print(f"Error in generating topic content: {err}")

    return response.choices[0].text


def generate_blog_description():
    """
        Prompt designed to give SEO optimized blog descripton
    """
    # Suggest keywords that I should include in my meta description for my blog post on [topic]

    # I want to generate high CTR meta and keyword rich meta title and meta descriptions in text format. 
    # My keywords are – [keyword 1], [keyword 2], [keyword 3]

    pass


def get_blog_tags(blog_article):
    """
        Function to suggest tags for the given blog content
    """
    # Suggest at least 5 tags for the following blog post [Enter your blog post text here].
    pass


def get_long_tailed_keywords(blog_article):
    """
        Function to get long tailed keywords for the blog article.
    """
    #  want you to generate a list of long-tail keywords that are related to the following blog post [Enter blog post text here]
    pass
