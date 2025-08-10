# Using Gemini Pro LLM model
import os
import sys
from pathlib import Path

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

from typing import Optional, Dict, Any

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
            model='gemini-2.5-pro',
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

def _dict_to_types_schema(schema: Dict[str, Any]) -> types.Schema:
    """Convert a lightweight dict schema to google.genai.types.Schema."""
    if not isinstance(schema, dict):
        raise ValueError("response_schema must be a dict compatible with types.Schema")

    def _convert(node: Dict[str, Any]) -> types.Schema:
        node_type = (node.get("type") or "OBJECT").upper()
        if node_type == "OBJECT":
            props = node.get("properties") or {}
            props_types: Dict[str, types.Schema] = {}
            for key, prop in props.items():
                if isinstance(prop, dict):
                    props_types[key] = _convert(prop)
                else:
                    props_types[key] = types.Schema(type=types.Type.STRING)
            return types.Schema(type=types.Type.OBJECT, properties=props_types if props_types else None)
        elif node_type == "ARRAY":
            items_node = node.get("items")
            if isinstance(items_node, dict):
                item_schema = _convert(items_node)
            else:
                item_schema = types.Schema(type=types.Type.STRING)
            return types.Schema(type=types.Type.ARRAY, items=item_schema)
        elif node_type == "NUMBER":
            return types.Schema(type=types.Type.NUMBER)
        elif node_type == "BOOLEAN":
            return types.Schema(type=types.Type.BOOLEAN)
        else:
            return types.Schema(type=types.Type.STRING)

    return _convert(schema)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gemini_structured_json_response(prompt, schema, temperature=0.7, top_p=0.9, top_k=40, max_tokens=2048, system_prompt=None):
    """
    Generate structured JSON response using Google's Gemini Pro model.
    """
    try:
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        # Build config using official SDK schema type
        try:
            types_schema = _dict_to_types_schema(schema) if isinstance(schema, dict) else schema
        except Exception as conv_err:
            logger.warning(f"Schema conversion warning, defaulting to OBJECT: {conv_err}")
            types_schema = types.Schema(type=types.Type.OBJECT)

        generation_config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            response_mime_type='application/json',
            response_schema=types_schema
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=generation_config,
        )

        # Prefer parsed if present and non-empty; otherwise parse text with fallbacks
        try:
            parsed = getattr(response, 'parsed', None)
            if parsed:
                return parsed if isinstance(parsed, dict) else json.loads(json.dumps(parsed))
            text = (response.text or '').strip()
            
            # Strip markdown code fences if present
            if text.startswith('```'):
                # remove leading ```json or ``` and trailing ```
                if text.lower().startswith('```json'):
                    text = text[7:]
                else:
                    text = text[3:]
                if text.endswith('```'):
                    text = text[:-3]
                text = text.strip()
            
            # Try direct JSON parsing first
            try:
                return json.loads(text)
            except json.JSONDecodeError as e:
                logger.warning(f"Direct JSON parsing failed: {e}")
                
                # Fallback 1: Extract likely JSON object substring
                first = text.find('{')
                last = text.rfind('}')
                if first != -1 and last != -1 and last > first:
                    candidate = text[first:last+1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        logger.warning("JSON object extraction failed, trying regex")
                
                # Fallback 2: Regex any object
                import re
                match = re.search(r'\{[\s\S]*\}', text)
                if match:
                    try:
                        return json.loads(match.group(0))
                    except json.JSONDecodeError:
                        logger.warning("Regex JSON extraction failed, trying repair")
                
                # Fallback 3: Attempt to repair common JSON issues
                repaired = _repair_json_string(text)
                if repaired:
                    try:
                        return json.loads(repaired)
                    except json.JSONDecodeError:
                        logger.warning("JSON repair failed")
                
                # Fallback 4: Extract and parse individual key-value pairs
                extracted = _extract_key_value_pairs(text)
                if extracted:
                    return extracted
                
                # Final fallback: return error with raw response for debugging
                logger.error(f"All JSON parsing attempts failed for text: {text[:200]}...")
                return {"error": f"Failed to parse JSON response: {e}", "raw_response": text[:500]}
                
        except Exception as e:
            logger.error(f"Error parsing structured response: {e}")
            return {"error": f"Failed to parse JSON response: {e}", "raw_response": (response.text or '')}

    except Exception as e:
        logger.error(f"Error in Gemini Pro structured JSON generation: {e}")
        return {"error": str(e)}


def _repair_json_string(text: str) -> Optional[str]:
    """
    Attempt to repair common JSON issues in AI responses.
    """
    if not text:
        return None
    
    # Remove any non-JSON content before first {
    start = text.find('{')
    if start == -1:
        return None
    text = text[start:]
    
    # Remove any content after last }
    end = text.rfind('}')
    if end == -1:
        return None
    text = text[:end+1]
    
    # Fix common issues
    repaired = text
    
    # 1. Fix unterminated arrays (add missing closing brackets)
    # Count opening and closing brackets
    open_brackets = repaired.count('[')
    close_brackets = repaired.count(']')
    if open_brackets > close_brackets:
        # Add missing closing brackets
        missing_brackets = open_brackets - close_brackets
        repaired = repaired + ']' * missing_brackets
    
    # 2. Fix unterminated strings in arrays
    # Look for patterns like ["item1", "item2" and add missing quote and bracket
    lines = repaired.split('\n')
    fixed_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Check if line ends with an unquoted string in an array
        if stripped.endswith('"') and i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if next_line.startswith(']'):
                # This is fine
                pass
            elif not next_line.startswith('"') and not next_line.startswith(']'):
                # Add missing quote and comma
                line = line + '",'
        fixed_lines.append(line)
    repaired = '\n'.join(fixed_lines)
    
    # 3. Fix unescaped quotes in string values
    # This is complex - we'll use a simple approach
    try:
        # Try to balance quotes by adding missing ones
        lines = repaired.split('\n')
        fixed_lines = []
        for line in lines:
            # Count quotes in the line
            quote_count = line.count('"')
            if quote_count % 2 == 1:  # Odd number of quotes
                # Add a quote at the end if it looks like an incomplete string
                if ':' in line and line.strip().endswith('"'):
                    line = line + '"'
                elif ':' in line and not line.strip().endswith('"') and not line.strip().endswith(','):
                    line = line + '",'
            fixed_lines.append(line)
        repaired = '\n'.join(fixed_lines)
    except Exception:
        pass
    
    # 4. Remove trailing commas before closing braces/brackets
    repaired = re.sub(r',(\s*[}\]])', r'\1', repaired)
    
    # 5. Fix missing commas between object properties
    repaired = re.sub(r'"(\s*)"', r'",\1"', repaired)
    
    return repaired


def _extract_key_value_pairs(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract key-value pairs from malformed JSON text as a last resort.
    """
    if not text:
        return None
    
    result = {}
    
    # Look for patterns like "key": "value" or "key": value
    # This regex looks for quoted keys followed by colons and values
    pattern = r'"([^"]+)"\s*:\s*(?:"([^"]*)"|([^,}\]]+))'
    matches = re.findall(pattern, text)
    
    for key, quoted_value, unquoted_value in matches:
        value = quoted_value if quoted_value else unquoted_value.strip()
        
        # Clean up the value - remove any trailing content that looks like the next key
        # This handles cases where the regex captured too much
        if value and '"' in value:
            # Split at the first quote that might be the start of the next key
            parts = value.split('"')
            if len(parts) > 1:
                value = parts[0].strip()
        
        # Try to parse the value appropriately
        if value.lower() in ['true', 'false']:
            result[key] = value.lower() == 'true'
        elif value.lower() == 'null':
            result[key] = None
        elif value.isdigit():
            result[key] = int(value)
        elif value.replace('.', '').replace('-', '').isdigit():
            try:
                result[key] = float(value)
            except ValueError:
                result[key] = value
        else:
            result[key] = value
    
    # Also try to extract array values
    array_pattern = r'"([^"]+)"\s*:\s*\[([^\]]*)\]'
    array_matches = re.findall(array_pattern, text)
    
    for key, array_content in array_matches:
        # Extract individual array items
        items = []
        # Look for quoted strings in the array
        item_pattern = r'"([^"]*)"'
        item_matches = re.findall(item_pattern, array_content)
        for item in item_matches:
            if item.strip():
                items.append(item.strip())
        
        if items:
            result[key] = items
    
    return result if result else None