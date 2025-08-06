"""Anthropic Provider Service for ALwrity Backend.

This service handles Anthropic Claude API integrations,
migrated from the legacy lib/gpt_providers/text_generation/anthropic_text_gen.py
"""

import os
import time
import anthropic
from typing import Tuple
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def anthropic_text_response(prompt: str, model: str = "claude-3-5-sonnet-20241022", 
                           temperature: float = 0.7, max_tokens: int = 4000, 
                           system_prompt: str = None) -> str:
    """
    Generate text using Anthropic's Claude model.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "claude-3-5-sonnet-20241022".
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
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("Anthropic API key not found in environment variables")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.messages.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        logger.info(f"[anthropic_text_response] Generated response with {len(response.content[0].text)} characters")
        return response.content[0].text

    except anthropic.AuthenticationError as e:
        logger.error(f"Anthropic Authentication Error: {e}")
        raise SystemExit from e
    except anthropic.RateLimitError as e:
        logger.error(f"Anthropic Rate Limit Error: {e}")
        raise SystemExit from e
    except anthropic.APIConnectionError as e:
        logger.error(f"Anthropic API Connection Error: {e}")
        raise SystemExit from e
    except Exception as e:
        logger.error(f"Unexpected error in Anthropic API call: {e}")
        raise SystemExit from e

async def test_anthropic_api_key(api_key: str) -> Tuple[bool, str]:
    """
    Test if the provided Anthropic API key is valid.
    
    Args:
        api_key (str): The Anthropic API key to test
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, message)
    """
    try:
        # Create Anthropic client with the provided key
        client = anthropic.Anthropic(api_key=api_key)
        
        # Try to generate a simple response as a test
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
            temperature=0.1
        )
        
        # If we get here, the key is valid
        return True, "Anthropic API key is valid"
        
    except anthropic.AuthenticationError:
        return False, "Invalid Anthropic API key"
    except anthropic.RateLimitError:
        return False, "Rate limit exceeded. Please try again later."
    except Exception as e:
        return False, f"Error testing Anthropic API key: {str(e)}" 