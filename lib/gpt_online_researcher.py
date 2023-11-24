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

# import and connect
from tavily import TavilyClient

def do_research_on(research_query):
    """
    Basically sending in the blog title to do research on.
    gpt-researcher API version to do extensive web research for given keywords.
    """
    # $ export TAVILY_API_KEY={Your Tavily API Key here}
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    except Exception as err:
        SystemExit(f"Failed to create TavilyClient: {err}")

    try:
        # run tavily search
        research_content = client.search(
                research_query,
                search_depth="advanced",
                include_answer=True,
                max_results=10)["results"]
    except Exception as err:
        SystemExit(f"Unable to do tavily search: {err}")

    # setup prompt
    prompt = [{
        "role": "system",
        "content":  f'You are an AI critical thinker research assistant. '\
                f'Your sole purpose is to write well written, critically acclaimed,'\
                f'objective and structured reports on given text.'
        }, {
        "role": "user",
        "content": f'Information: """{research_content}"""\n\n' \
               f'Using the above information, answer the following'\
               f'query: "{research_query}" in a detailed report --'\
               f'Please use MLA format and markdown syntax.'
        }]

    # run gpt-4
    try:
        lc_messages = convert_openai_messages(prompt)
        research_report = ChatOpenAI(
                model='gpt-4',
                openai_api_key=openai_api_key
                ).invoke(lc_messages).content
    except Exception as err:
        SystemExit(f"Failed to convert OpenAI message and get response.")

    # print report
    print(research_report)
    return research_report
