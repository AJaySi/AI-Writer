import os
import time #IWish
import logging
import openai
import configparser

# Configure standard logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s-%(levelname)s-%(module)s-%(lineno)d]- %(message)s')

logger = logging.getLogger(__name__)
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
 

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt):
    """
    Wrapper function for OpenAI's ChatGPT completion.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "gpt-4-1106-preview".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 4096
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    try:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'main_config'))

        config = configparser.ConfigParser()
        config.read(config_path)

        model = config.get('llm_options', 'model')
        temperature = config.getfloat('llm_options', 'temperature')
        max_tokens = config.getint('llm_options', 'max_tokens')
        top_p = config.getfloat('llm_options', 'top_p')
        n = config.getint('llm_options', 'n')
        fp = config.getfloat('llm_options', 'frequency_penalty')
    except Exception as err:
        logger.error(f"Unable to read Openai parameters from config file:{err}")
    
    # Wait for 10 seconds to comply with rate limits
    for _ in range(5):
        time.sleep(1)

    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p,
            stream=True,
            frequency_penalty=fp
            # Additional parameters can be included here
        )
        # create variables to collect the stream of chunks
        collected_chunks = []
        collected_messages = []
        # iterate through the stream of events
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            chunk_message = chunk.choices[0].delta.content  # extract the message
            collected_messages.append(chunk_message)  # save the message
            print(chunk.choices[0].delta.content, end = "", flush = True)
        
        # clean None in collected_messages
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
