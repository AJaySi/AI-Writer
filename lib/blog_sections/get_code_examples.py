"""
At the command line, only need to run once to install the package via pip:
$ pip install google-generativeai
"""
from .gpt_providers.gemini_pro_text import gemini_text_response


def gemini_get_code_samples(blog_article):
    """ Provide a programming blog and get code exmaples."""
    prompt = f"""As an expert programmer and copywriter, I will provide you with blog article.
        Your task is to research and write one code example for the given blog article.
        Do not include your explanations in response.
        Blog Article: '{blog_article}' """
    try:
        code_sample = gemini_text_response(prompt)
        response = combine_blog_code_sample(blog_article, code_sample)
        return response
    except Exception as err:
        raise ValueError(f"Failed to get response from Gemini pro: {err}")


def combine_blog_code_sample(blog_article, code_sample):
    """ Include the code sample into the given blog. """
    prompt = """You are expert document editor, I will provide you blog article and a code sample.
        Your task is to edit the given blog article to include the code sample after the introduction section.
        Do not modify the content of the given blog article. Your response should include the whole blog_article with
        the code sample added to it.
        Adopt the formatting of the given blog article. Do not include explanations of your response.
        Edit the given blog to include the code sample in it.
        Blog Article: {blog_article}\n
        Code sample: {code_sample}\n"""

    try:
        response = gemini_text_response(prompt)
        return response
    except Exception as err:
        raise ValueError(f"Failed to combine blog and code: {err}")
