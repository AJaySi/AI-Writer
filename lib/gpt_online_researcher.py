################################################################
#
# GPT Researcher is an autonomous agent designed for comprehensive online research on a variety of tasks.
# The agent can produce detailed, factual and unbiased research reports, with customization options for 
# focusing on relevant resources, outlines, and lessons. Inspired by the recent Plan-and-Solve and RAG papers, 
# GPT Researcher addresses issues of speed, determinism and reliability, offering a more stable 
# performance and increased speed through parallelized agent work, as opposed to synchronous operations.
#
# The main idea is to run "planner" and "execution" agents, whereas the planner generates questions to research, 
# and the execution agents seek the most related information based on each generated research question. 
# Finally, the planner filters and aggregates all related information and creates a research report.
#
# The agents leverage both gpt3.5-turbo and gpt-4-turbo (128K context) to complete a research task. 
# We optimize for costs using each only when necessary. 
# The average research task takes around 3 minutes to complete, and costs ~$0.1.
# 
##############################################################

import os
import logging
from tavily import TavilyClient
from langchain.adapters.openai import convert_openai_messages
from langchain.chat_models import ChatOpenAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(module)s-%(lineno)d-%(message)s')
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def do_online_research(query):
    try:
        # Retrieve API keys
        api_key = os.getenv('TAVILY_API_KEY')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or not openai_api_key:
            raise ValueError("API keys for Tavily or OpenAI are not set.")

        # Initialize Tavily client
        try:
            client = TavilyClient(api_key=api_key)
        except Exception as err:
            logging.error("Failed to create Tavily client. Check TAVILY_API_KEY")
            exit(1)

        # Run tavily search
        logging.info(f"Running Tavily search on: {query}")
        try:
            content = client.search(query, search_depth="advanced")["results"]
        except Exception as err:
            logging.error(f"Failed to do Tavily Research: {err}")
            exit(1)

        # Setup prompt for GPT-4
        prompt = [{
            "role": "system",
            "content": ('You are an AI critical thinker research assistant. '
                        'Your sole purpose is to write well written, critically acclaimed, '
                        'objective and structured reports on given text.')
        }, {
            "role": "user",
            "content": (f'Information: """{content}"""\n\n'
                        f'Using the above information, answer the following '
                        f'query: "{query}" in a detailed report --'
                        f'Please use MLA format and markdown syntax.')
        }]
        # Run GPT-4
        logging.info("Generating report with GPT-4...")
        lc_messages = convert_openai_messages(prompt)
        try:
            report = ChatOpenAI(model='gpt-4', openai_api_key=openai_api_key).invoke(lc_messages).content
            logging.info(f"\n Below is the online research report for given keywords/title: \n\n{report}")
            return report
        except Exception as err:
            logging.error("Failed to generate do_online_research with ChatOpenAI")
            exit(1)

    except Exception as e:
        logging.error(f"Failed in online research: {e}")
        exit(1)
