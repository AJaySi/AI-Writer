import os
import logging
from pathlib import Path

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(module)s-%(lineno)d-%(message)s')
from dotenv import load_dotenv
load_dotenv(Path('../../.env'))

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def mistral_text_response(prompt):
    """ Common function to get text response from minstral. """
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-medium"

    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(role="user", content=prompt)
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
    )
    print(chat_response)

    # With streaming
    for chunk in client.chat_stream(model=model, messages=messages):
        print(chunk)
