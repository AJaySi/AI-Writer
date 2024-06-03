import sys
import configparser
import json

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )   

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def blog_metadata(blog_content):
    """ Common function to get blog metadata """
    logger.info(f"Generating Content MetaData\n")

    blog_metadata_prompt = """
		As an expert SEO and content writer, I will provide you with blog content.
		
		1. Suggest only 2 blog categories which are most relevant to the provided blog content, by identifying the main topic. 
        Also consider the target audience and the blog's category taxonomy. Only reply with comma-separated values.
		2. Compose a compelling meta description for the given blog content, adhering to SEO best practices. 
        Keep it between 150-160 characters. Provide a glimpse of the content's value to entice readers. 
        Respond with only one of your best efforts and do not include your explanations.
		3. Write 1 blog title following SEO best practices. Please keep the title concise, not exceeding 60 words. 
        Respond with only 1 title and no explanations. Negative Keywords: Unveiling, unleash, power of. Don't use such words in your title.
		4. Suggest only 2 relevant and specific blog tags for the given blog content. Only reply with comma-separated values.
		
		The blog content is: '{blog_article}'
		
		Please provide the result in the following JSON format:
		
		{
		  "title": "Your generated blog title",
		  "meta_description": "Your generated meta description",
		  "tags": ["tag1", "tag2"],
		  "categories": ["category1", "category2"]
		}
		"""
    try:
        response = llm_text_gen(blog_metadata_prompt)
        """ Cleans the response by removing ``` and 'json' strings """
        result_json = response.replace("```", "").replace("json", "").strip()
        # Convert the cleaned response to JSON
        result_json = json.loads(result_json)
    except Exception as err:
        logger.error(f"Failed to get response from LLM: {err}")
        raise err

    # Extract the data from the JSON response
    blog_title = result_json.get("title")
    blog_meta_desc = result_json.get("meta_description")
    blog_tags = result_json.get("tags")
    blog_categories = result_json.get("categories")

    return blog_title, blog_meta_desc, blog_tags, blog_categories
