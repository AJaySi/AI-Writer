import os
import time
from deepseek import DeepSeek
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

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
