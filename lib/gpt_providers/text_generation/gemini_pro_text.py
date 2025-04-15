# Using Gemini Pro LLM model
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types

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

import asyncio
import json
import re

# Configure standard logging
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s-%(levelname)s-%(module)s-%(lineno)d]- %(message)s')
logger = logging.getLogger(__name__)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt, temperature, top_p, n, max_tokens, system_prompt):
    """ Common functiont to get response from gemini pro Text. """
    #FIXME: Include : https://github.com/google-gemini/cookbook/blob/main/quickstarts/rest/System_instructions_REST.ipynb
    try:
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
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
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=n,
            ),
        )
        
        #logger.info(f"Number of Token in Prompt Sent: {model.count_tokens(prompt)}")
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

async def test_gemini_api_key(api_key: str) -> tuple[bool, str]:
    """
    Test if the provided Gemini API key is valid.
    
    Args:
        api_key (str): The Gemini API key to test
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, message)
    """
    try:
        # Configure Gemini with the provided key
        genai.configure(api_key=api_key)
        
        # Try to list models as a simple API test
        models = genai.list_models()
        
        # Check if Gemini Pro is available
        if any(model.name == "gemini-pro" for model in models):
            return True, "Gemini API key is valid"
        else:
            return False, "Gemini Pro model not available with this API key"
        
    except Exception as e:
        return False, f"Error testing Gemini API key: {str(e)}"

def gemini_pro_text_gen(prompt, temperature=0.7, top_p=0.9, top_k=40, max_tokens=2048):
    """
    Generate text using Google's Gemini Pro model.
    
    Args:
        prompt (str): The input text to generate completion for
        temperature (float, optional): Controls randomness. Defaults to 0.7
        top_p (float, optional): Controls diversity. Defaults to 0.9
        top_k (int, optional): Controls vocabulary size. Defaults to 40
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 2048
        
    Returns:
        str: The generated text completion
    """
    try:
        # Configure the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate content
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                max_output_tokens=max_tokens,
            )
        )
        
        # Return the generated text
        return response.text
        
    except Exception as e:
        logger.error(f"Error in Gemini Pro text generation: {e}")
        return str(e)

def gemini_structured_json_response(prompt, schema, temperature=0.7, top_p=0.9, top_k=40, max_tokens=2048, system_prompt=None):
    """
    Generate structured JSON response using Google's Gemini Pro model.
    
    Args:
        prompt (str): The input text to generate completion for
        schema (dict): The JSON schema to follow for the response
        temperature (float, optional): Controls randomness. Defaults to 0.7
        top_p (float, optional): Controls diversity. Defaults to 0.9
        top_k (int, optional): Controls vocabulary size. Defaults to 40
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 2048
        system_prompt (str, optional): System instructions for the model
        
    Returns:
        dict: The generated structured JSON response
    """
    try:
        # Configure the model
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Set up generation config
        generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_tokens,
        }
        
        # Generate content with structured response
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                response_mime_type='application/json',
                response_schema=schema
            ),
        )
        
        # Parse the response
        try:
            # First try to get the parsed response
            if hasattr(response, 'parsed'):
                return response.parsed
            
            # If parsed is not available, try to parse the text
            response_text = response.text
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return {"error": f"Failed to parse JSON response: {e}", "raw_response": response_text}
            
    except Exception as e:
        logger.error(f"Error in Gemini Pro structured JSON generation: {e}")
        return {"error": str(e)}
