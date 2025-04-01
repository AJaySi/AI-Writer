import os
import logging
from pathlib import Path
from mistralai import Mistral
import asyncio
from loguru import logger

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

# Configure standard logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s-%(levelname)s-%(module)s-%(lineno)d]- %(message)s')
logger = logging.getLogger(__name__)

async def test_mistral_api_key(api_key: str) -> tuple[bool, str]:
    """
    Test if the provided Mistral API key is valid.
    
    Args:
        api_key (str): The Mistral API key to test
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, message)
    """
    try:
        async with Mistral(api_key=api_key) as client:
            # Try a simple completion as a test
            response = await client.chat.complete_async(
                model="mistral-small-latest",
                messages=[{
                    "role": "user",
                    "content": "Hello"
                }],
                max_tokens=10
            )
            
            if response and response.choices:
                return True, "Mistral API key is valid"
            else:
                return False, "Invalid response from Mistral API"
                
    except Exception as e:
        return False, f"Error testing Mistral API key: {str(e)}"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
async def mistral_chat_completion_async(
    prompt: str,
    model: str = "mistral-small-latest",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.9,
    system_prompt: str = "You are a helpful AI assistant."
) -> str:
    """
    Generate text using Mistral's chat completion API asynchronously.
    
    Args:
        prompt (str): The input text to generate completion for
        model (str, optional): Model to use. Defaults to "mistral-small-latest"
        temperature (float, optional): Controls randomness. Defaults to 0.7
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 2048
        top_p (float, optional): Controls diversity. Defaults to 0.9
        system_prompt (str, optional): System prompt to guide the model. Defaults to "You are a helpful AI assistant."
        
    Returns:
        str: The generated text completion
    """
    try:
        async with Mistral(api_key=os.getenv('MISTRAL_API_KEY')) as client:
            messages = []
            
            # Add system message if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Generate chat completion
            response = await client.chat.complete_async(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p
            )
            
            if response and response.choices:
                return response.choices[0].message.content
            else:
                raise Exception("No response generated")
                
    except Exception as e:
        logger.error(f"Error in Mistral chat completion: {e}")
        raise SystemExit from e

# Synchronous wrapper for compatibility
def mistral_chat_completion(
    prompt: str,
    model: str = "mistral-small-latest",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.9,
    system_prompt: str = "You are a helpful AI assistant."
) -> str:
    """
    Synchronous wrapper for mistral_chat_completion_async.
    """
    try:
        return asyncio.run(mistral_chat_completion_async(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            system_prompt=system_prompt
        ))
    except Exception as e:
        logger.error(f"Error in Mistral chat completion: {e}")
        return str(e)

# For backward compatibility
def mistral_text_response(prompt, model="mistral-small-latest", temperature=0.7, max_tokens=2048):
    """
    Legacy function for backward compatibility.
    """
    return mistral_chat_completion(
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
