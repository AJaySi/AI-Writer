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
from pathlib import Path
import logging

from tavily import TavilyClient
import serpapi

from dotenv import load_dotenv
load_dotenv(Path('../.env'))

from langchain.adapters.openai import convert_openai_messages
from langchain.chat_models import ChatOpenAI
import google.generativeai as genai

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s-%(module)s-%(lineno)d-%(message)s')
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

from .gpt_providers.gemini_pro_text import gemini_text_response
from .blog_proof_reader import blog_proof_editor
from .convert_content_to_markdown import convert_tomarkdown_format


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def do_online_research(query, gpt_provider="openai"):
    # Do a google search for the given keyword. The search results will give urls, questions for faq
    faq_questions = []
    organic_results = []
    report = ''
    try:
        faq_questions = google_search(query, "faq")
        logging.info(f"Google search FAQ questions: {faq_questions}")
        # Now, get top 10 google organic results and polish the content to compete for these keywords.
        organic_results = google_search(query, "organic_result")
    except Exception as err:
        logging.error(f"Failed to do Serpapi research: {err}")
        # Not failing, as tavily would do same and then GPT-V to search.
        #exit(1)
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

        if "gemini" in gpt_provider:
            prompt = ["You are an AI critical thinker research assistant."
                    "I will provide you with json content and a list of faq questions."
                    "Use given json as context for writing your research report."
                    "Your sole purpose is to write well written, critically acclaimed, objective and structured research report"
                    "Important: Include and write code examples in your final report." 
                    "Include your own insights on the topic to make it comprehensive and detailed."
                    "Use the urls from json content to provide cititations and include it in referances section of your report."
                    "Include appropriate emojis in your research report."
                    "Include FAQs relevant to your research report. Use the given faq questions. Write answers for each faq."
                    "Format your report in MLA format and markdown style, with special focus on readibility."
                    f"Do not provide explanations for your response.\njson content: \"\"\" {content} \"\"\"\n "
                    f"\nList of FAQ questions: \"\"\" {faq_questions} \"\"\"\n"]
            report = gemini_text_response(prompt)
        
        elif "openai" in gpt_provider:
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
            report = openai_research_report(prompt)
        report = compete_organic_results(query, report, organic_results)
        return report
    except Exception as e:
        logging.error(f"Failed in online research: {e}")
        exit(1)


def openai_research_report(query):
    """ Generate research report with openai """
    # Run GPT-4
    logging.info("Generating Research report with GPT-4...")
    lc_messages = convert_openai_messages(prompt)
    try:
        report = ChatOpenAI(model='gpt-4', openai_api_key=openai_api_key).invoke(lc_messages).content
        #logging.info(f"\n Below is the online research report for given keywords/title: \n\n{report}")
        return report
    except Exception as err:
        logging.error("Failed to generate do_online_research with ChatOpenAI")
        exit(1)


def compete_organic_results(query, report, organic_results):
    """ Given a blog content and google search organinc results, create a new blog to compete against them."""
    prompt = f""" As an SEO expert and copywriter, I will provide you with my blog content on topic '{query}', and
        Top google search results. 
        Your task is to rewrite the given blog to make it compete against top position results. 
        Make sure, the new blog has high probability of ranking highest against given organic search result competitors.
        Modify the given blog content following best SEO practises.
        Make sure the blog is original, unique and highly readable.
        Remember, Maintain and adopt the formatting, structure, style and tone of the provided blog content.
        Include relevant emojis in your final blog for visual appeal. Use it sparingly.
        Your response should be well-structured, objective, and critically acclaimed blog article based on provided texts. 

        Remember, your goal is to create a detailed blog article that will compete against given organic result competitors.
        Do not provide explanations, suggestions for your response, reply only with your final response.
        Take your time in crafting your content, do not rush to give the response.
        Blog Content: '{report}'\n
        Organic Search result: '{organic_results}'
        """
    report = gemini_text_response(prompt)
    return report


def google_search(query, flag="faq"):
    """ Do google search for given query """
    try:
        api_key = os.getenv('SERPAPI_KEY')
        client = serpapi.Client(api_key=api_key)
        result = client.search(
            q=query,
            engine="google",
            hl="en",
        )
    except Exception as err:
        logging.error(f"Failed in Google Search: {err}")
        exit(1)
    if 'faq' in flag:
        # Check if 'inline_people_also_search_for' and 'related_questions' exist in result
        related_search = [item['title'] for item in result.get('inline_people_also_search_for', [])]
        related_questions = [item['question'] for item in result.get('related_questions', [])]

        # Determine which list to use for faq_questions
        if not related_search and not related_questions:
            faq_questions = [item['query'] for item in result.get('related_searches', [])]
        else:
            faq_questions = related_search + related_questions 
        return faq_questions

    elif 'organic_result' in flag:
        # Check if 'organic_results' exists in result
        return result.get('organic_results', [])
