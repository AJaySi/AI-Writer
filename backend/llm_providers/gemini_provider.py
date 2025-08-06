# Using Gemini Pro LLM model
import os
import sys
from pathlib import Path
from typing import Dict, Any
import time
import google.genai as genai
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

def get_gemini_api_key():
    """Get Gemini API key from API key manager or environment."""
    try:
        # Try to get from API key manager first
        from services.api_key_manager import get_api_key_manager
        api_key_manager = get_api_key_manager()
        api_key = api_key_manager.get_api_key("gemini")
        if api_key:
            return api_key
    except Exception as e:
        logger.warning(f"Could not get API key from manager: {e}")
    
    # Fallback to environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Gemini API key not found in environment variables or API key manager")
    
    return api_key

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_text_response(prompt, temperature=0.7, top_p=0.9, n=40, max_tokens=2048, system_prompt=None):
    """Get response from Gemini Pro Text using official SDK pattern."""
    try:
        # Get API key
        api_key = get_gemini_api_key()
        
        logger.info(f"Temp: {temperature}, MaxTokens: {max_tokens}, TopP: {top_p}, N: {n}")
        
        # Create the client with API key (official SDK pattern)
        client = genai.Client(api_key=api_key)
        
        # Prepare content with system instruction if provided
        if system_prompt:
            # Use system instruction in generation config (official SDK pattern)
            generation_config = types.GenerateContentConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=n,
                max_output_tokens=max_tokens,
                system_instruction=system_prompt
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",  # Using the recommended model from docs
                contents=prompt,
                config=generation_config
            )
        else:
            # Standard generation without system instruction (official SDK pattern)
            generation_config = types.GenerateContentConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=n,
                max_output_tokens=max_tokens,
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",  # Using the recommended model from docs
                contents=prompt,
                config=generation_config
            )
        
        logger.info(f"[gemini_text_response] Generated response with {len(response.text)} characters")
        return response.text
        
    except Exception as err:
        logger.error(f"Failed to get response from Gemini: {err}. Retrying.")
        raise

def _clean_schema_for_gemini(schema):
    """Clean schema to remove unsupported properties for Gemini API."""
    if isinstance(schema, dict):
        # Remove unsupported properties
        unsupported_props = ['additionalProperties', 'pattern', 'format', 'minLength', 'maxLength']
        cleaned = {}
        
        for key, value in schema.items():
            if key not in unsupported_props:
                if isinstance(value, dict):
                    cleaned_value = _clean_schema_for_gemini(value)
                    # Skip empty objects or objects with empty properties
                    if key == "properties" and not cleaned_value:
                        continue
                    if key == "properties" and isinstance(cleaned_value, dict):
                        # Remove any properties that have empty object definitions
                        non_empty_props = {}
                        for prop_key, prop_value in cleaned_value.items():
                            if isinstance(prop_value, dict):
                                if prop_value.get("type") == "object":
                                    # If it's an object type, ensure it has properties or change to string
                                    if not prop_value.get("properties"):
                                        non_empty_props[prop_key] = {"type": "string"}
                                    else:
                                        non_empty_props[prop_key] = prop_value
                                else:
                                    non_empty_props[prop_key] = prop_value
                            else:
                                non_empty_props[prop_key] = prop_value
                        cleaned[key] = non_empty_props
                    else:
                        cleaned[key] = cleaned_value
                elif isinstance(value, list):
                    cleaned[key] = [_clean_schema_for_gemini(item) if isinstance(item, dict) else item for item in value]
                else:
                    cleaned[key] = value
        
        return cleaned
    elif isinstance(schema, list):
        return [_clean_schema_for_gemini(item) if isinstance(item, dict) else item for item in schema]
    else:
        return schema

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_structured_json_response(prompt: str, schema: Dict[str, Any], model_name: str = "gemini-2.0-flash-001") -> str:
    """
    Generate structured JSON response using Gemini API according to official SDK
    """
    try:
        api_key = get_gemini_api_key()
        if not api_key:
            logger.error("Gemini API key not found")
            return json.dumps({"error": "API key not found"})
        
        # Clean and validate schema
        cleaned_schema = _clean_schema_for_gemini(schema)
        validated_schema = _validate_and_fix_schema(cleaned_schema)
        
        logger.info(f"🤖 Making Gemini API call to {model_name}")
        logger.info(f"📝 Prompt: {prompt[:200]}...")
        logger.info(f"🔧 Schema: {json.dumps(validated_schema, indent=2)}")
        
        # Create the client with API key (official SDK pattern)
        client = genai.Client(api_key=api_key)
        
        generation_config = types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=8192,
        )
        
        # Create the prompt with schema
        full_prompt = f"""
{prompt}

Please respond with a valid JSON object that matches this schema:

{json.dumps(validated_schema, indent=2)}

Ensure the response is valid JSON and matches the schema exactly.
"""
        
        logger.info(f"🚀 Sending request to Gemini API...")
        start_time = time.time()
        
        # Generate content using official SDK pattern
        response = client.models.generate_content(
            model=model_name,
            contents=full_prompt,
            config=generation_config
        )
        
        end_time = time.time()
        logger.info(f"⏱️ Gemini API response received in {end_time - start_time:.2f} seconds")
        logger.info(f"📄 Raw response: {response.text[:500]}...")
        
        # Try to parse the response as JSON
        try:
            # First, try to extract JSON from the response
            json_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if json_text.startswith("```json"):
                json_text = json_text[7:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]
            
            json_text = json_text.strip()
            
            # Try to parse as JSON
            parsed = json.loads(json_text)
            logger.info(f"✅ Successfully parsed JSON response: {json.dumps(parsed, indent=2)}")
            return json.dumps(parsed)
            
        except json.JSONDecodeError as e:
            logger.warning(f"❌ JSON parsing failed: {e}")
            logger.warning(f"📄 Attempted to parse: {json_text}")
            
            # Try to find JSON-like content in the response
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                try:
                    parsed = json.loads(json_match.group())
                    logger.info(f"✅ Found and parsed JSON in response: {json.dumps(parsed, indent=2)}")
                    return json.dumps(parsed)
                except json.JSONDecodeError:
                    logger.warning("❌ Failed to parse extracted JSON")
            
            logger.warning("❌ No valid JSON found in response, returning full text")
            return json.dumps({"error": "Invalid JSON response", "raw_text": response.text})
            
    except Exception as e:
        logger.error(f"❌ Gemini API error: {str(e)}")
        return json.dumps({"error": f"Gemini API error: {str(e)}"})

def _validate_and_fix_schema(schema):
    """Validate and fix schema to ensure it's compatible with Gemini API."""
    if isinstance(schema, dict):
        # Check for empty object properties
        if "properties" in schema and isinstance(schema["properties"], dict):
            fixed_properties = {}
            for key, value in schema["properties"].items():
                if isinstance(value, dict):
                    if value.get("type") == "object":
                        # If object has no properties or empty properties, change to string
                        if not value.get("properties") or not value["properties"]:
                            fixed_properties[key] = {"type": "string"}
                        else:
                            # Recursively fix nested objects
                            fixed_properties[key] = _validate_and_fix_schema(value)
                    else:
                        fixed_properties[key] = value
                else:
                    fixed_properties[key] = value
            
            schema["properties"] = fixed_properties
        
        # Recursively fix nested objects
        for key, value in schema.items():
            if isinstance(value, dict):
                schema[key] = _validate_and_fix_schema(value)
    
    return schema

async def test_gemini_api_key(api_key: str) -> tuple[bool, str]:
    """
    Test if the provided Gemini API key is valid using official SDK pattern.
    
    Args:
        api_key (str): The Gemini API key to test
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, message)
    """
    try:
        # Try to generate a simple response as a test using official SDK pattern
        test_prompt = "Hello"
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",  # Using the recommended model from docs
            contents=test_prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=50
            )
        )
        
        # If we get here, the key is valid
        return True, "Gemini API key is valid"
        
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "authentication" in error_msg.lower():
            return False, "Invalid Gemini API key"
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return False, "Rate limit exceeded. Please try again later."
        else:
            return False, f"Error testing Gemini API key: {error_msg}"

def gemini_pro_text_gen(prompt, temperature=0.7, top_p=0.9, top_k=40, max_tokens=2048):
    """
    Generate text using Google's Gemini Pro model according to official SDK.
    
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
        # Get API key
        api_key = get_gemini_api_key()
        
        # Create the client with API key (official SDK pattern)
        client = genai.Client(api_key=api_key)
        
        # Generate content using the official SDK pattern
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',  # Using the recommended model from docs
            contents=prompt,
            config=types.GenerateContentConfig(
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