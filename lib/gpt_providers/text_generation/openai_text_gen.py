import os
import time #IWish
import openai
import asyncio

# Configure standard logging
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s-%(levelname)s-%(module)s-%(lineno)d]- %(message)s')
logger = logging.getLogger(__name__)
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
 

async def test_openai_api_key(api_key: str) -> tuple[bool, str]:
    """
    Test if the provided OpenAI API key is valid.
    
    Args:
        api_key (str): The OpenAI API key to test
        
    Returns:
        tuple[bool, str]: A tuple containing (is_valid, message)
    """
    try:
        # Create OpenAI client with the provided key
        client = openai.OpenAI(api_key=api_key)
        
        # Try to list models as a simple API test
        models = client.models.list()
        
        # If we get here, the key is valid
        return True, "OpenAI API key is valid"
        
    except openai.AuthenticationError:
        return False, "Invalid OpenAI API key"
    except openai.RateLimitError:
        return False, "Rate limit exceeded. Please try again later."
    except Exception as e:
        return False, f"Error testing OpenAI API key: {str(e)}"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model, temperature, max_tokens, top_p, n, fp, system_prompt):
    """
    Wrapper function for OpenAI's ChatGPT completion.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "gpt-4o".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 4096
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    # Wait for 10 seconds to comply with rate limits
    for _ in range(5):
        time.sleep(1)

    try:
        # Create variables to collect the stream of chunks
        collected_chunks = []
        collected_messages = []
        full_reply_content = None
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}, 
                      {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p,
            stream=True,
            frequency_penalty=fp
            # Additional parameters can be included here
        )
        
        # Iterate through the stream of events
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk.choices[0].delta.content  # extract the message
            collected_messages.append(chunk_message)  # save the message
            print(chunk.choices[0].delta.content, end = "", flush = True)
        
        # Clean None in collected_messages
        collected_messages = [m for m in collected_messages if m is not None]
        full_reply_content = ''.join([m for m in collected_messages])
        return full_reply_content

    except openai.APIError as e:
        logger.error(f"OpenAI API Error: {e}")
        raise SystemExit from e
    except openai.APIConnectionError as e:
        logger.error(f"Failed to connect to OpenAI API: {e}")
        raise SystemExit from e
    except openai.RateLimitError as e:
        logger.error(f"Rate limit exceeded on OpenAI API request: {e}")
        raise SystemExit from e
    except Exception as err:
        logger.error(f"OpenAI error: {err}")
        raise SystemExit from e
