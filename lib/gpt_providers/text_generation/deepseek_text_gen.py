import os
import time
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import openai
import asyncio

# Configure standard logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s-%(levelname)s-%(module)s-%(lineno)d]- %(message)s')
logger = logging.getLogger(__name__)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def deepseek_text_response(prompt, model, temperature, max_tokens, top_p, n, system_prompt):
    """
    Wrapper function for DeepSeek's text generation.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "deepseek-chat".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 4096.
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    # Wait for 10 seconds to comply with rate limits
    for _ in range(10):
        time.sleep(1)

    try:
        client = DeepSeek(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
        response = client.reasoning.create(
            model=model,
            context=system_prompt,
            query=prompt,
            max_tokens=max_tokens,
            n=n,
            top_p=top_p,
            stream=True,
            temperature=temperature
        )

        # Create variables to collect the stream of chunks
        collected_chunks = []
        collected_messages = []
        full_reply_content = None

        # Iterate through the stream of events
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk.result  # extract the message
            collected_messages.append(chunk_message)  # save the message
            print(chunk.result, end="", flush=True)

        # Clean None in collected_messages
        collected_messages = [m for m in collected_messages if m is not None]
        full_reply_content = ''.join([m for m in collected_messages])
        return full_reply_content

    except Exception as err:
        logger.error(f"DeepSeek error: {err}")
        raise SystemExit from err

async def test_deepseek_api_key(api_key: str) -> tuple[bool, str]:
    """
    Test if the provided DeepSeek API key is valid.
    
    Args:
        api_key (str): The DeepSeek API key to test
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, message)
    """
    try:
        # Create OpenAI client with DeepSeek base URL
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        # Try to list models as a simple API test
        models = client.models.list()
        
        # If we get here, the key is valid
        return True, "DeepSeek API key is valid"
        
    except openai.AuthenticationError:
        return False, "Invalid DeepSeek API key"
    except openai.RateLimitError:
        return False, "Rate limit exceeded. Please try again later."
    except Exception as e:
        return False, f"Error testing DeepSeek API key: {str(e)}"

def deepseek_text_gen(prompt, model="deepseek-chat", temperature=0.7, max_tokens=2048):
    """
    Generate text using DeepSeek's API.
    
    Args:
        prompt (str): The input text to generate completion for
        model (str, optional): Model to use. Defaults to "deepseek-chat"
        temperature (float, optional): Controls randomness. Defaults to 0.7
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 2048
        
    Returns:
        str: The generated text completion
    """
    try:
        # Create OpenAI client with DeepSeek base URL
        client = openai.OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com/v1"
        )
        
        # Generate chat completion
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Return the generated text
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error in DeepSeek text generation: {e}")
        return str(e)
