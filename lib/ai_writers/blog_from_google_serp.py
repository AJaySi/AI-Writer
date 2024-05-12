import os
import sys
import json

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


# FIXME: Provide num_blogs, num_faqs as inputs.
def write_blog_google_serp(search_keyword, search_results):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        As expert Creative Content writer, writing up fresh ideas with care and uniqueness.
        I will provide you with my 'web research keywords' and its 'google search result'.
        Your goal is to create detailed SEO-optimized content and also include 5 FAQs.
        
        Follow below guidelines:
        1). Your blog content should compete against all blogs from search results.
        2). Your FAQ should be based on 'People also ask' and 'Related Queries' from given search result. 
            Always include answers for each FAQ, use your knowledge and confirm with snippets given in search result.
        3). Act as subject matter expert for given research keywords: {search_keyword}.
        4). Conversational tone:  Write like you're chatting with a friend, making the topic approachable and interesting.
        5). Your blog should be highly formatted in markdown style and highly readable.
        6). Friendly tone:  Write like you're talking to a friend, not giving a lecture.
        7). Simple explanations:  No robotic jargon! Make AI writing easy to understand.
        8). Personal touch:  Share your own experiences and opinions to make it relatable.
        9). Examples and stories:  Bring the topic to life with real-world examples.

        \n\nWeb Research Keyword: "{search_keyword}"
        Here are some Google search results to spark your creativity: "{search_results}". 
        But don't just rehash them - use your own voice and insights!
        """
    logger.info("Generating blog and FAQs from Google web search results.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def improve_blog_intro(blog_content, blog_intro):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        As an expert Content editor, I will provide you with my 'blog content' and its new 'blog introduction'.
        Your goal is to replace the old introduction with the given new introduction. 
        Do Not change any other section of the blog content.
        You must respond with the complete blog content with replaced introduction.
        Do not provide explanations for your response.

        \n\nBlog Content: "{blog_content}"
        Blog Introduction: "{blog_intro}".
        """
    logger.info("Generating blog introduction from tavily answer.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def blog_with_keywords(blog, keywords):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        As an expert digital content writer, specializing in content optimization and SEO. 
        I will provide you with my 'blog content' and 'list of keywords' on the same topic.
        Your task is to write an original blog, utilizing given keywords and blog content.
        Your blog should be highly detailed and well formatted. 

        You are Sarah, the Creative Content writer, writing up fresh ideas and crafts them with care. 
        She makes complex topics easy to understand and writes in a friendly tone that connects with everyone.
        She excels at simplifying complex topics and communicates with charisma, making technical jargon come alive for her audience.
        

        Blog content: '{blog}'
        list of keywords: '{keywords}'
        """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_keywords: Failed to get response from LLM: {err}")
        raise err


def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        You are Alwrity, the Creative Content writer, writing up fresh ideas and crafts them with care and uniqueness. 
        She makes complex topics simple to understand and writes in a friendly, conversational tone that connects with everyone.
        She excels at simplifying complex topics and writes in the first person, for her audience.

        I will provide you with a latest 'research report' and a outdated 'blog content' on the same topic.
        Your task is to update the given blog content, using the new research report, as context.

        \n\nResearch report: '{report}'
        \n\nBlog content: '{blog}'
        """

    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_research: Failed to get response from LLM: {err}")
        raise err
