import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI

def setup_environment():
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'  # Adjust based on available model

def create_agents(search_keywords):
    search_tool = SerperDevTool()

    # Load the google gemini api key
    google_api_key = os.getenv("GEMINI_API_KEY")

    # Set gemini pro as llm
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", verbose=True, temperature=0.9, google_api_key=google_api_key
    )

    content_researcher = Agent(
        role = 'Senior Research Analyst',
        goal = f'Uncover content writing ideas for "{search_keywords}" keywords.',
        backstory = f"""You work at a leading digital marketing firm.
        Your expertise lies in identifying emerging trends, topic for content creation.
        You are expert in researching latest information about various topics and {search_keywords}.
        Your research and content suggestions are foundation for content writers.
        Your detailed content research is pivotal to company's content strategy.""",
        tools = [search_tool],
        memory = True,  # Enable memory
        verbose = True,
        max_rpm = None,  # No limit on requests per minute
        max_iter = 15,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    content_outliner = Agent(
        role = 'Senior Content Strategist',
        goal = f'Create a content outline for "{search_keywords}" keywords, from your insights & provided context.',
        backstory = """You are an expert digital content writer and marketing expert.
            The content researcher had identified ideas to write content on. 
            Use this knowledge to write your content outline.
            Take your time going over the research. Your content outline will be expanded upon after review.""",
        memory = True,  # Enable memory
        verbose = True,
        max_rpm = 10,  # No limit on requests per minute
        max_iter = 5,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    content_writer = Agent(
        role = 'Content Strategist',
        goal = f"""Craft compelling & SEO optimized content on {search_keywords}. 
        Rank high on Google for popular long-tail keywords related to the short-tail keyword {search_keywords}""",
        backstory = f"""You are a renowned Content Strategist, known for your insightful and engaging articles.
        You transform complex concepts into compelling narratives. 
        Limit them to 20 words or so, using language familiar to the majority. 
        Example: Instead of "Utilize this methodology," say "Use this method."
        Employ a clear and concise writing style.
        Engage your audience with a compelling, fun, and informative tone,
        that effectively conveys the technical aspects of the topic in simple terms.
        """,
        memory = True,  # Enable memory
        verbose = True,
        max_rpm = 10,  # No limit on requests per minute
        max_iter = 5,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    content_reviewer = Agent(
	    role="Expert Writing Critic & content Editor.",
        goal="Review the draft content and identfy potential issues.",
        backstory="""You are expert reviewer with 10 years of exprience in reviewing digital content.
        The make sure that article are interesting and correct information provided.
        Simplicity will resonate with your readers.
        Pay attention to grammar and punctuation.
        Avoid AI sounding words and pass AI detection tools.
        Engage with active voice. It’s as if you’re in conversation with the reader.
        Example: Use "You will see benefits" instead of "One will see benefits."
        Use headings, bullets, and formatting to break the monotony of the text. These elements add rhythm and can make a document more inviting.
        A concise conclusion that resonates with the beginning can bring your piece full circle, satisfying your readers.
        """,
        memory=True,  # Enable memory
        verbose=True,
        max_rpm=10,  # No limit on requests per minute
        max_iter=5,  # Default value for maximum iterations
        allow_delegation=False,
        llm=llm
    )

    return [content_researcher, content_outliner, content_writer, content_reviewer]

def create_tasks(agents, search_keywords):
    research_task = Task(
            description=f"""Conduct a comprehensive topic analysis on the following: "{search_keywords}".
        Identify keyword trends, SEO opportunities, and potential content ideas to write upon.
        """,
        expected_output="Provide Full analysis report in bullet points",
        agent=agents[0]  # Assign to the researcher agent
    )

    outline_task = Task(
        description="""Use the insights to produce a detailed content outline to expand upon later.""",
        expected_output="A detailed and insightful content outline on {search_keywords}.",
        #human_input=True,
        agent=agents[1]  # Assign to the outliner agent
    )

    writer_task = Task(
        description="""Using the insights provided, develop an engaging content that highlights {search_keywords}.
        Your post should be informative yet accessible, catering to a tech-savvy audience.
        Avoid complex words so it doesn't sound like AI.""",
        expected_output="A 2000 words content convering most sections of the provided outline.",
        agent=agents[2]  # Assign to the writer agent
    )

    proofread_task = Task(
        description=f"""Sharpen the focus of the draft content by identifying overly wordy sections and crafting concise alternatives.
        Words with many syllables are barriers to simplicity. 
        Choose simpler words, avoid sounding like AI.
        Pay special attention to readiblity, formatting & styling of the content.
        Make sure the draft content SEO optimised for keywords: {search_keywords}.
        Make sure the final content is 2000 words long.
        """,
        expected_output="Final content with your review comments edited in the content draft.",
        agent=agents[3]  # Assign to the reviewer agent
    )

    return [research_task, outline_task, writer_task, proofread_task]

def execute_tasks(agents, tasks, lang):
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=2,  # You can set it to 1 or 2 for different logging levels
        #process=Process.sequential,
        #memory=True,
        language=lang
    )
    result = crew.kickoff()
    return result

def ai_agents_writers(search_keywords, lang="en"):
    setup_environment()
    agents = create_agents(search_keywords)
    tasks = create_tasks(agents, search_keywords)
    result = execute_tasks(agents, tasks, lang)
    print("######################")
    print(result)
