import os
import anthropic
import asyncio
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

# Configure standard logging
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s-%(levelname)s-%(module)s-%(lineno)d]- %(message)s')
logger = logging.getLogger(__name__)

async def test_anthropic_api_key(api_key: str) -> tuple[bool, str]:
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
        
        # Try a simple completion as a test
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": "Say hello"
            }]
        )
        
        # If we get here, the key is valid
        return True, "Anthropic API key is valid"
        
    except anthropic.AuthenticationError:
        return False, "Invalid Anthropic API key"
    except anthropic.RateLimitError:
        return False, "Rate limit exceeded. Please try again later."
    except Exception as e:
        return False, f"Error testing Anthropic API key: {str(e)}"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def anthropic_text_response(prompt, model="claude-3-haiku-20240307", temperature=0.7, max_tokens=2048, top_p=0.9, n=1, system_prompt="You are a helpful AI assistant."):
    """
    Generate text using Anthropic's Claude model with retry logic.
    
    Args:
        prompt (str): The input text to generate completion for
        model (str, optional): Model to use. Defaults to "claude-3-haiku-20240307"
        temperature (float, optional): Controls randomness. Defaults to 0.7
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 2048
        top_p (float, optional): Controls diversity. Defaults to 0.9
        n (int, optional): Number of completions to generate. Defaults to 1
        system_prompt (str, optional): System prompt to guide the model. Defaults to "You are a helpful AI assistant."
        
    Returns:
        str: The generated text completion
    """
    try:
        # Create Anthropic client
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Generate completion
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Return the generated text
        return response.content[0].text
        
    except Exception as e:
        logger.error(f"Error in Anthropic text generation: {e}")
        raise SystemExit from e

def anthropic_text_gen(prompt, model="claude-3-haiku-20240307", temperature=0.7, max_tokens=2048):
    """
    Generate text using Anthropic's Claude model.
    
    Args:
        prompt (str): The input text to generate completion for
        model (str, optional): Model to use. Defaults to "claude-3-haiku-20240307"
        temperature (float, optional): Controls randomness. Defaults to 0.7
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 2048
        
    Returns:
        str: The generated text completion
    """
    try:
        # Create Anthropic client
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Generate completion
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Return the generated text
        return response.content[0].text
        
    except Exception as e:
        logger.error(f"Error in Anthropic text generation: {e}")
        return str(e)
