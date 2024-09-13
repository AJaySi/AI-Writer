# Using Gemini Pro LLM model
import os
import sys
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv(Path('../../../.env'))
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt, temperature, top_p, n, max_tokens, system_prompt):
    """ Common functiont to get response from gemini pro Text. """
    #FIXME: Include : https://github.com/google-gemini/cookbook/blob/main/quickstarts/rest/System_instructions_REST.ipynb
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    except Exception as err:
        logger.error(f"Failed to configure Gemini: {err}")
    logger.info(f"Temp: {temperature}, MaxTokens: {max_tokens}, TopP: {top_p}, N: {n}")
    # Set up AI model config
    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": n,
        "max_output_tokens": max_tokens,
    }
    # FIXME: Expose model_name in main_config
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", 
                                  generation_config=generation_config,
                                  system_instruction=system_prompt)
    try:
        # text_response = []
        response = model.generate_content(prompt, stream=True)
        if response:
            for chunk in response:
                # text_response.append(chunk.text)
                print(chunk.text)
        else:
            print(response)
        logger.info(f"Number of Token in Prompt Sent: {model.count_tokens(prompt)}")
        return response.text
    except Exception as err:
        logger.error(f"Failed to get response from Gemini: {err}. Retrying.")


#@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
#def gemini_blog_metadata_json(blog_content):
#    """ Common functiont to get response from gemini pro Text. """
#    prompt =  f"I will provide you with the content of a blog post. Based on this content, you need to generate the following elements in JSON format:\n\n1. **Blog Title**: A compelling and relevant title that summarizes the blog content.\n2. **Meta Description**: A concise meta description (up to 160 characters) that captures the essence of the blog post and encourages clicks.\n3. **Tags**: A list of 5-10 relevant tags that represent the key topics covered in the blog post.\n4. **Categories**: A list of 1-3 appropriate categories that best describe the blog post's main themes.\n\nOutput your response in the following JSON format:\n\n```json\n{\n  \"type\": \"object\",\n  \"properties\": {\n    \"blog_title\": {\n      \"type\": \"string\"\n    },\n    \"meta_description\": {\n      \"type\": \"string\"\n    },\n    \"tags\": {\n      \"type\": \"array\",\n      \"items\": {\n        \"type\": \"string\"\n      }\n    },\n    \"categories\": {\n      \"type\": \"array\",\n      \"items\": {\n        \"type\": \"string\"\n      }\n    }\n  }\n}\n\n. The Blog Content is given below: \n\n{blog_content}\n\n"
#    
#    try:
#        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
#    except Exception as err:
#        logger.error(f"Failed to configure Gemini: {err}")
#
#    # Create the model
#    generation_config = {
#        "temperature": 1,
#        "top_p": 0.95,
#        "top_k": 64,
#        "max_output_tokens": 8192,
#        "response_schema": content.Schema(
#        type = content.Type.OBJECT,
#            properties = {
#                "response": content.Schema(
#                    type = content.Type.STRING,
#                    ),
#            },
#        ),
#        "response_mime_type": "application/json",
#    }
#
#    model = genai.GenerativeModel(
#        model_name="gemini-1.5-flash",
#        generation_config=generation_config,
#        # safety_settings = Adjust safety settings
#        # See https://ai.google.dev/gemini-api/docs/safety-settings
#        )
#
#        try:
#        # text_response = []
#        response = model.generate_content(prompt)
#        if response:
#            logger.info(f"Number of Token in Prompt Sent: {model.count_tokens(prompt)}")
#            return response.text
#    except Exception as err:
#        logger.error(f"Failed to get SEO METADATA from Gemini: {err}. Retrying.")
