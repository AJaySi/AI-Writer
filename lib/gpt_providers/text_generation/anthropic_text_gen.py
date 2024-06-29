import os

import anthropic
from anthropic import Anthropic
import streamlit as st


def anthropic_text_response(prompt):
    """ """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"),)

    try:
        response = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
            }
        ],
        # This will come from config file.
        model="claude-3-opus-20240229",
        )
        return(message.content)
    except anthropic.APIConnectionError as e:
        st.error("The server could not be reached")
        st.error(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except anthropic.RateLimitError as e:
        st.error("A 429 status code was received; we should back off a bit.")
    except anthropic.APIStatusError as e:
        st.error("Another non-200-range status code was received")
        st.error(e.status_code)
        st.error(e.response)
