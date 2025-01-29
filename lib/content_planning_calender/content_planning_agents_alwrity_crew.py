import os
import streamlit as st

from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import FileReadTool

from ..ai_web_researcher.google_trends_researcher import do_google_trends_analysis


def create_agents(search_keywords, already_written_on):

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
    manager_read_tool = FileReadTool(file_path=already_written_on)

    # Load the google gemini api key
    google_api_key = os.getenv("GEMINI_API_KEY")

    # Set gemini pro as llm
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", verbose=True, temperature=0.7, google_api_key=google_api_key
    )

    content_researcher = Agent(
        role = 'Senior Web Research Analyst (Content Strategy): Aisha Sharma',
        goal = f"""Help Create a highly detailed 2 month-long content calender, focused around keywords: {search_keywords}.
            Provide web researched titles to be used for content calender & planning to Ted XingPi""",
        backstory = f"""
        
        Your Focus: Content Opportunity Analysis & Keyword Research ({search_keywords}).

        Your Skills:

        1). Web Research & Content Gap Identification (Expert).
        2). SEO Best Practices, Keyword Research & content planning expert (Advanced).
        3). Analyzes search trends and competitor content.
        4). Fuel company's content strategy with data-driven insights to attract and educate online readers.
        5). Identifies high-volume, low-competition keywords relevant to {search_keywords}.

        Responsibilities:

        1). Recommend high-value content opportunities through in-depth web research and competitor analysis.
        2). Provide your research to Senior Content Strategist & planner - Ted XingPi
        
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
            Do not repeat the blog titles, always consult the previously written blog titles from the file: {already_written_on}.""",
            
        backstory = """You are Ted XingPi, with Experience of 15 years.

            Your Skills:
            1). Content Opportunity Analysis & Content calender planning (Expert).
            2). AI Applications for Content Marketing (Highly Knowledgeable).
            3). Content Strategy Development & keyword research for content opportunities.


            Your Responsibilties:
            
            1). Employ a balance of head terms (broad topics) and long-tail keywords (specific phrases) for optimal reach and targeting.
            2). Review & Include suggestions from Content Marketing & Google Trends Specialist - Sarah Qureshi.
            3). Identify content topics and keywords for {search_keywords}.
            4). Senior Web Research Analyst (Content Strategy): Aisha Sharma
            5). Create content calender that showcases the value proposition around {search_keywords}.
            6). New content should target unique keywords to avoid competition with existing content.
            7). Focus on specific aspects within a theme to differentiate semantically similar keywords for {search_keywords}.
            8). Collaborate with team to identify content gaps and trending topics, relevant to given keywords.
            9). Develop content calender with a focus on organic marketing to attract online customers.
            10). The content calender should include, Head Term Keyword, Long-Tail Keyword and Blog Post Title.
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

        goal = f"""Help Create a highly detailed 2 month-long content calender, focused around keywords: {search_keywords}.
            Analyse & provide Google trends data for content calender & planning to Ted XingPi""",
        
        backstory = f"""You are Sarah Qureshi, with 10 years as a content writer and planner.
            Your Skills:
                1). Proven experience in using Google Trends for keyword research.
                2). Strong understanding of SEO best practices.
                3). Reading files and understanding long table with data.

            Your responsibilties:
                1). Collaborate on content strategy, provide keyword, titles recommendations to Ted XingPi.
                2). Recommend high-volume, low-competition keywords, titles with strong user intent.
                3). Recommend, Rising search queries related to {search_keywords}.
                4). Recommend keywords, blog titles for preparing/planning the content calender.
                5). Provide your research to Senior Content Strategist & planner - Ted XingPi
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
            Use insights and context from team members: Sarah Qureshi, Ted XingPi and Aisha Sharma""",
        backstory="""
            Content Marketing Manager: Diksha Yuj
            Experience: Digital Marketing Veteran (15+ years)
            
            Mission: Supercharge organic growth of the company, with content marketing.

            Responsibilities:

                1). Ensures that content titles are not repeated & No keyword cannabilization.
                2). Maintains and consults a file for all previous written titles({already_written_on}).
                3). Develops a content calendar aligned and optimized around {search_keywords}.
                4). Keenly follows & learns the research and communication of other team members.
                5). The content calender should include, Head Term Keyword, Long-Tail Keyword and Blog Post Title.
                6). Use insights and context from team members: Sarah Qureshi, Ted XingPi and Aisha Sharma
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


def create_tasks(agents, search_keywords, already_written_on):
    research_task = Task(
        description=f"""Conduct web analysis on "{search_keywords}",for content calender.
            Set the input parameter 'search_query' to query""",
        expected_output=f"""Provide comprehensive content calender ideas to Senior Content Strategist & planner - Ted XingPi""",
        agent=agents[0]  # Assign to the researcher agent
    )

    google_trends_task = Task(
            description=f"""Conduct Google Trends analysis, on keywords: {search_keywords}, from the file({os.getenv('SEARCH_SAVE_FILE')}).
            Suggest blog titles for content calender. Recommend high-volume, low-competition keywords with strong user intent.
            Set the input parameter 'file_path' to {os.getenv('SEARCH_SAVE_FILE')}""",
        expected_output=f"Provide comprehensive content calender ideas to Senior Content Strategist & planner - Ted XingPi",
        agent=agents[1]  # Assign to the researcher agent
    )
    planner_task = Task(
        description=f"""Develop a content calendar for {search_keywords}, based team member's.
            New content should target unique keywords to avoid competition with existing content.
            Use context & insights from Aisha Sharma & Sarah Qureshi.
            Set the input parameter file_path to {already_written_on}""",
        expected_output=f"""A Highly detailed content calender that positions {search_keywords} as a must-read for industry insiders and newcomers alike. Final content calender for the next 2 months. Targeting 5 articles per week.
            """,
        #human_input=True,
        agent=agents[2] # Assign to the outliner agent
    )

    marketing_manager_task = Task(
        description=f"""Make sure the content calender is optimised for keywords: '{search_keywords}'.
            Make sure the titles are unique, semantically unique and mitigate keyword cannabilization.
            Use context & insights from Aisha Sharma, Ted XingPi & Sarah Qureshi.
            Set the input parameter 'file_path' to {already_written_on}
        """,
        expected_output=f"""Final content calender for the next 2 months. Targeting 5 articles per week.
            Make sure to present the content calender in tabular format. Include details of how to use the content calender.
            """,
        agent=agents[3]  # Assign to the reviewer agent
    )

    return [research_task, google_trends_task, planner_task, marketing_manager_task]


def execute_tasks(agents, tasks):
    """ WIP """
    result = None
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=2,  # You can set it to 1 or 2 for different logging levels
        #process=Process.sequential,
        #memory=True,
        language="en"
    )
    try:
        result = crew.kickoff()
        return result
    except Exception as err:
        print(err)


def ai_agents_content_planner(search_keywords):
    already_written_on = os.path.join(os.getcwd(), "lib", "content_planning_calender", "content_already_planned.txt")
    do_google_trends_analysis(search_keywords)
    result = None
    #setup_environment()
    try:
        agents = create_agents(search_keywords, already_written_on)
    except Exception as err:
        st.error(f"Failed in Creating in Agents: {err}")
    try:
        tasks = create_tasks(agents, search_keywords, already_written_on)
    except Exception as err:
        st.error(f"Failed to Create Agent Tasks: {err}")
    try:
        result = execute_tasks(agents, tasks)
    except Exception as err:
        st.error(f"Failed to execute Agent Tasks: {err}")
    st.markdown("### Final Content Calender:")
    st.markdown(result)
