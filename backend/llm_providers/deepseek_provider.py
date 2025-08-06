"""DeepSeek Provider Service for ALwrity Backend.

This service handles DeepSeek API integrations,
migrated from the legacy lib/gpt_providers/text_generation/deepseek_text_gen.py
"""

import os
import time
import requests
from typing import Tuple
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def deepseek_text_response(prompt: str, model: str = "deepseek-chat", 
                          temperature: float = 0.7, max_tokens: int = 4000, 
                          system_prompt: str = None) -> str:
    """
    Generate text using DeepSeek's API.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "deepseek-chat".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.7.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 4000.
        system_prompt (str, optional): System prompt for the conversation. Defaults to None.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    # Wait for 5 seconds to comply with rate limits
    for _ in range(5):
        time.sleep(1)

    try:
        # Get API key from environment
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("DeepSeek API key not found in environment variables")
        
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Make API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            logger.info(f"[deepseek_text_response] Generated response with {len(content)} characters")
            return content
        else:
            error_msg = f"DeepSeek API Error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise SystemExit(error_msg)

    except requests.exceptions.RequestException as e:
        logger.error(f"DeepSeek API Connection Error: {e}")
        raise SystemExit from e
    except Exception as e:
        logger.error(f"Unexpected error in DeepSeek API call: {e}")
        raise SystemExit from e

async def test_deepseek_api_key(api_key: str) -> Tuple[bool, str]:
    """
    Test if the provided DeepSeek API key is valid.
    
    Args:
        api_key (str): The DeepSeek API key to test
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, message)
    """
    try:
        # Make a simple API test request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10,
            "temperature": 0.1
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return True, "DeepSeek API key is valid"
        elif response.status_code == 401:
            return False, "Invalid DeepSeek API key"
        elif response.status_code == 429:
            return False, "Rate limit exceeded. Please try again later."
        else:
            return False, f"Error testing DeepSeek API key: {response.status_code} - {response.text}"
        
    except requests.exceptions.RequestException as e:
        return False, f"Connection error testing DeepSeek API key: {str(e)}"
    except Exception as e:
        return False, f"Error testing DeepSeek API key: {str(e)}" 