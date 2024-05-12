import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import ScrapeWebsiteTool, tool
from crewai_tools import FileReadTool

from ..ai_web_researcher.google_trends_researcher import do_google_trends_analysis


def setup_environment():
    os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'  # Adjust based on given model

def create_agents(search_keywords):

    # Tools for the agents.
    search_tool = SerperDevTool()

    # To enable scrapping any website it finds during it's execution
    #scrape_tool = ScrapeWebsiteTool()

    # To read results from a file.
    # Initialize the tool to read any files the agents knows or lean the path for
    # file_read_tool = FileReadTool()
    # Initialize the tool with a specific file path, so the agent can only read the content of the specified file
    file_read_tool = FileReadTool(file_path=os.getenv('SEARCH_SAVE_FILE'))
    # The manager keeps an eye on the content already planned to give new ideas.
    # TBD: Accept the user website urls and populate the file with sitemap.xml
    manager_read_tool = FileReadTool(file_path="content_already_planned.txt")

    # Load the google gemini api key
    google_api_key = os.getenv("GEMINI_API_KEY")

    # Set gemini pro as llm
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", verbose=True, temperature=0.7, google_api_key=google_api_key
    )

    content_researcher = Agent(
        role = 'Senior Web Research Analyst (Content Strategy): Aisha Sharma',
        goal = f"""
            Recommend unique blog titles for "{search_keywords}" keywords.
            Provide researched titles to be used for content calender & planning.""",
        backstory = f"""
        
        Your Focus: Content Opportunity Analysis & Keyword Research ({search_keywords}).

        Your Skills:

        1). Web Research & Content Gap Identification (Expert).
        2). SEO Best Practices, Keyword Research & content planning expert (Advanced).
        3). Analyzes search trends and competitor content.
        
        Mission:  

        1). Fuel company's content strategy with data-driven insights to attract and educate online readers.
        2). Identifies high-volume, low-competition keywords relevant to {search_keywords}.

        Responsibilities:

        1). Recommend high-value content opportunities through in-depth web research and competitor analysis.
        2). Do competitor analysis for {search_keywords} for content calender & planning.
        
        """,
        tools = [search_tool],
        memory = True,  # Enable memory
        verbose = True,
        max_rpm = None,  # No limit on requests per minute
        max_iter = 10,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    content_planner = Agent(
        role = 'Senior Content Strategist & planner - Ted XingPi',
        goal = f"""
            Craft a series of content titles around {search_keywords} that can be expanded into 2 month-long series.
            Do not repeat the blog titles, always consult the previously written blog titles from the file(content_already_planned.txt).
            Set the """,
        backstory = """You are Ted XingPi, with Experience of 15 years.

            Your Skills:
            1). Content Opportunity Analysis & Content calender planning (Expert).
            2). AI Applications for Content Marketing (Highly Knowledgeable).
            3). Content Strategy Development & planning.
            4). Analyze keyword research for content opportunities.

            Your Responsibilties:

            1). Identify content topics and keywords for {search_keywords}.
            2). Create content calender that showcases the value proposition around {search_keywords}.
            3). Collaborate with team to identify content gaps and trending topics, relevant to given keywords.
            4). Develop content calender with a focus on organic marketing to attract online customers.
            5). The content calender should include, Head Term Keyword, Long-Tail Keyword and Blog Post Title.
            """,
        memory = True,  # Enable memory
        verbose = True,
        tools = [manager_read_tool],
        max_rpm = None,  # No limit on requests per minute
        max_iter = 15,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    google_trends_researcher = Agent(
        role = 'Content Marketing & Google Trends Specialist - Sarah Qureshi.',

        goal = f"""Use Google Trends to suggest AI writing keywords & titles, optimized for {search_keywords}.
            All the required google trends data is present in the file({os.getenv('SEARCH_SAVE_FILE')}).""",
        
        backstory = f"""You are Sarah Qureshi, with 10 years as a content writer and planner.
            Your Skills:
                1). Proven experience in using Google Trends for keyword research.
                2). Strong understanding of SEO best practices.
                3). Reading files and understanding long table with data.
                4). Ability to communicate complex data insights in a clear and concise way.
            
            Your Personality:
                1). Enjoys breaking down complex topics into clear and concise information.
                2). Strong communicator with a knack for explaining technical concepts in an engaging way.

            Your responsibilties:
                1). Collaborate on content strategy, provide keyword, titles recommendations and integrate them into the content calendar.
                2). Recommend high-volume, low-competition keywords, titles with strong user intent.
                3). Recommend, Rising search queries related to {search_keywords}.
                5). Recommend keywords, blog titles for preparing/planning the content calender.
        """,
        memory = True,  # Enable memory
        tools = [file_read_tool],
        verbose = True,
        max_rpm = None,  # No limit on requests per minute
        max_iter = 15,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    content_marketing_manager = Agent(
	    role="Content Marketing Manager - Diksha Yuj",
        goal=f"""Create highly detailed 2 month-long content calender, focused around keywords: {search_keywords}.
            Important to ensure the keywords and titles are not already written on, consult the file(content_already_planned.txt).""",
        backstory="""
            Content Marketing Manager: Diksha Yuj
            Experience: Digital Marketing Veteran (15+ years)
            
            Mission: Supercharge organic growth of the company, with content marketing.

            Responsibilities:

                1). Ensures that content titles are not repeated & No keyword cannabilization.
                2). Maintains and consults a file for all previous written titles.
                3). Develops a content calendar aligned and optimized around {search_keywords}.
                4). Keenly follows & learns the research and communication of other team members.
                5). The content calender should include, Head Term Keyword, Long-Tail Keyword and Blog Post Title.
        """,
        memory=True,  # Enable memory
        verbose=True,
        tools = [manager_read_tool],
        max_rpm=None,  # No limit on requests per minute
        max_iter=10,  # Default value for maximum iterations
        allow_delegation=False,
        llm=llm
    )

    return [content_researcher, google_trends_researcher, content_planner, content_marketing_manager]


def create_tasks(agents, search_keywords):
    research_task = Task(
        description=f"""Conduct a analysis on the following: "{search_keywords}". Suggest blog titles for content calender.
            Set the input parameter as : search_query""",
        expected_output=f"""Analyze keywords {search_keywords} to provide content ideas for content calender.""",
        agent=agents[0]  # Assign to the researcher agent
    )

    google_trends_task = Task(
            description=f"""Conduct Google Trends analysis, on keywords: {search_keywords}, from the file({os.getenv('SEARCH_SAVE_FILE')}).
            Suggest blog titles for content calender. Recommend high-volume, low-competition keywords with strong user intent.
            Set the input parameter file_path to {os.getenv('SEARCH_SAVE_FILE')}""",
        expected_output=f"Recommend content ideas, blog titles to be included in the content calender.",
        agent=agents[1]  # Assign to the researcher agent
    )
    planner_task = Task(
        description=f"""Develop a content calendar for {search_keywords} that includes evergreen, trending, and seasonal post ideas.""",
        expected_output=f"""
            A Highly detailed content calender that positions {search_keywords} as a must-read for industry insiders and newcomers alike.
            Prioritize keywords relevant to user needs and search intent, leveraging Google Trends insights.
            Employ a balance of head terms (broad topics) and long-tail keywords (specific phrases) for optimal reach and targeting.
            New content should target unique keywords to avoid competition with existing content.
            Focus on specific aspects within a theme to differentiate semantically similar keywords for {search_keywords}.
            Use context & insights from Aisha Sharma & Sarah Qureshi.
            Set the input parameter file_path to content_already_planned.txt""",
        #human_input=True,
        agent=agents[2] # Assign to the outliner agent
    )

    marketing_manager_task = Task(
        description=f"""Make sure the content calender is optimised for keywords: '{search_keywords}'.
            Make sure the titles are unique, semantically unique and mitigate keyword cannabilization.
            Use context & insights from Aisha Sharma & Sarah Qureshi.
            Set the input parameter file_path to content_already_planned.txt
        """,
        expected_output=f"""Final content calender for the next 2 months. Targeting 5 articles per week.
            Make sure to present the content calender in tabular format. Include details of how to use the content calender.""",
        agent=agents[3]  # Assign to the reviewer agent
    )

    return [research_task, google_trends_task, planner_task, marketing_manager_task]


def execute_tasks(agents, tasks):
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=2,  # You can set it to 1 or 2 for different logging levels
        #process=Process.sequential,
        #memory=True,
        language="en"
    )
    result = crew.kickoff()
    return result


def ai_agents_writers(search_keywords):
    do_google_trends_analysis(search_keywords)
    #setup_environment()
    agents = create_agents(search_keywords)
    tasks = create_tasks(agents, search_keywords)
    result = execute_tasks(agents, tasks)
    print("########## Final Output Result ############")
    print(result)
