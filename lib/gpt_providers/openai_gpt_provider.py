########################################################
#
# openai chatgpt integration for blog generation.
# Choosing a model from openai and fine tuning its various paramters. 
#
########################################################

from tqdm import tqdm, trange
import openai
import time # I wish


def openai_chatgpt(prompt, model="text-davinci-003", temperature=0.5, max_tokens=2048, top_p=0.9, n=10):
    try:
        # Error in generating topic content: Rate limit reached for default-global-with-image-limits
        # in free account on requests per min. Limit: 3 / min. Please try again in 20s.
        for i in trange(21):
            time.sleep(1)
        # using OpenAI's Completion module that helps execute
        # any tasks involving text
        response = openai.Completion.create(
            # model name used here is text-davinci-003
            # there are many other models available under the
            # umbrella of GPT-3
            model="text-davinci-003",
            # passing the user input
            prompt=prompt,
            # generated output can have "max_tokens" number of tokens
            max_tokens=max_tokens,
            # number of outputs generated in one call
            n=n,
            top_p=top_p,
            #frequency_penalty=0,
            #presence_penalty=0
        )
        return(response)
    except openai.error.Timeout as e:
       #Handle timeout error, e.g. retry or log
       SystemError(f"OpenAI API request timed out: {e}")
    except openai.error.APIError as e:
       #Handle API error, e.g. retry or log
       SystemError(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
       #Handle connection error, e.g. check network or log
       SystemError(f"OpenAI API request failed to connect: {e}")
    except openai.error.InvalidRequestError as e:
       #Handle invalid request error, e.g. validate parameters or log
       SystemError(f"OpenAI API request was invalid: {e}")
    except openai.error.AuthenticationError as e:
       #Handle authentication error, e.g. check credentials or log
       SystemError(f"OpenAI API request was not authorized: {e}")
    except openai.error.PermissionError as e:
       #Handle permission error, e.g. check scope or log
       SystemError(f"OpenAI API request was not permitted: {e}")
    except openai.error.RateLimitError as e:
       #Handle rate limit error, e.g. wait or log
       SystemError(f"OpenAI API request exceeded rate limit: {e}")
