import os
import configparser

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
        model="gemini-pro", verbose=True, temperature=0.6, google_api_key=google_api_key
    )

    role, goal, backstory = read_config("content_researcher")
    content_researcher = Agent(
        role = role,
        goal = goal,
        backstory = backstory,
        tools = [search_tool],
        memory = True,  # Enable memory
        verbose = True,
        max_rpm = None,  # No limit on requests per minute
        max_iter = 15,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    role, goal, backstory = read_config("content_outliner")
    content_outliner = Agent(
        role = role,
        goal = goal,
        backstory = backstory,
        memory = True,  # Enable memory
        verbose = True,
        max_rpm = 10,  # No limit on requests per minute
        max_iter = 5,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    role, goal, backsotry = read_config("content_writer")
    content_writer = Agent(
        role = role,
        goal = goal,
        backstory = backstory,
        memory = True,  # Enable memory
        verbose = True,
        max_rpm = 10,  # No limit on requests per minute
        max_iter = 5,  # Default value for maximum iterations
        allow_delegation = False,
        llm = llm
    )

    reviewer_config = read_config("content_reviewer")
    content_reviewer = Agent(
	    role=role,
        goal=goal,
        backstory=backstory,
        memory=True,  # Enable memory
        verbose=True,
        max_rpm=10,  # No limit on requests per minute
        max_iter=5,  # Default value for maximum iterations
        allow_delegation=False,
        llm=llm
    )

    return [content_researcher, content_outliner, content_writer, content_reviewer]

def create_tasks(agents, search_keywords):
    task_description, expected_output = read_config("research_task")
    print(task_description, expected_output)
    research_task = Task(
        description=f"""The main focus keywords are: "{search_keywords}".\n{task_description}""",
        expected_output = expected_output,
        agent=agents[0]  # Assign to the researcher agent
    )

    task_description, expected_output = read_config("outline_task")
    outline_task = Task(
        description=f"{task_description}.\n The main focus keywords are {search_keywords}",
        expected_output=f"{expected_output}",
        #human_input=True,
        agent=agents[1]  # Assign to the outliner agent
    )

    task_description, expected_output = read_config("writer_task")
    writer_task = Task(
        description=f"{task_description}\nThe main focus keywords are {search_keywords}\n.",
        expected_output=expected_output,
        agent=agents[2]  # Assign to the writer agent
    )

    task_description, expected_output = read_config("review_task")
    proofread_task = Task(
        description=f"{task_description}.\nThe main focus keywords are: {search_keywords}.",
        expected_output=expected_output,
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


def read_config(which_member):
    """
    Reads the role, goal, and backstory from the config file. 
    """
    # Assign the specific config file for each agent.
    # Base path to workspace/my_content_team
    team_dir = os.path.join(os.getcwd(), "lib", "workspace", "my_content_team")
    config_file = None
    
    if 'content_researcher' in which_member or 'research_task' in which_member:
        config_file = os.path.join(team_dir, "content_researcher.txt")
    elif 'content_writer' in which_member or 'writer_task' in which_member:
        config_file = os.path.join(team_dir, "content_writer.txt")
    elif 'content_reviewer' in which_member or 'review_task' in which_member:
        config_file = os.path.join(team_dir, "content_reviewer.txt")
    elif 'content_outliner' in which_member or 'outline_task' in which_member:
        config_file = os.path.join(team_dir, "content_outliner.txt")
    
    config = {}
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        role = config.get('main', 'role')
        goal = config.get('main', 'goal')
        backstory = config.get('backstory', 'text')
    except Exception as err:
        print(f"Error reading agent config: {err}")

    if not 'task' in which_member:
        return role, goal, backstory
    else:
        task_description = config.get('task', 'task_description')
        expected_output = config.get('task', 'task_expected_output')
        return task_description, expected_output


def ai_agents_writers(search_keywords, lang="en"):
    setup_environment()
    agents = create_agents(search_keywords)
    tasks = create_tasks(agents, search_keywords)
    result = execute_tasks(agents, tasks, lang)
    print("######################")
    print(result)
