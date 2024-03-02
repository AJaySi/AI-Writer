import os
from pathlib import Path

import requests
import typer
from PyInquirer import prompt
from rich import print
from rich.text import Text

from dotenv import load_dotenv
load_dotenv(Path('.env'))

app = typer.Typer()

from lib.ai_web_researcher.gpt_online_researcher import gpt_web_researcher
from lib.ai_web_researcher.metaphor_basic_neural_web_search import metaphor_find_similar
from lib.ai_writers.keywords_to_blog import write_blog_from_keywords


def prompt_for_time_range():
    os.system("clear" if os.name == "posix" else "cls")
    print("\n🙋 If you researching keywords that are recent than use accordingly, Default is Anytime.\n")
    questions = [
        {
            'type': 'list',
            'name': 'time_range',
            'message': '👋 Select Search result time range:',
            'choices': ["anytime", "past year", "past month", "past week", "past day"],
            'default': 'anytime'
        }
    ]
    answers = prompt(questions)
    return answers['time_range']

def write_blog_options():
    questions = [
        {
            'type': 'list',
            'name': 'blog_type',
            'message': '📝 Choose a blog type:',
            'choices': ['Keywords', 'Audio YouTube', 'Programming', 
                'Scholar', 'News/TBD','Finance/TBD', 'Quit'],
        }
    ]
    answers = prompt(questions)
    return answers['blog_type']


@app.command()
def start_interactive_mode():
    """
    This function is executed when no command is provided.
    It prompts the user to choose between "Write Blog" and "Do Web Research."
    """
    os.system("clear" if os.name == "posix" else "cls")
    text = Text()
    text.append("_______________________________________________________________________")
    text.append("\n⚠️    Alert!   💥❓💥\n", style="bold red") 
    text.append("If you know what to write, choose 'Write Blog'\n", style="bold blue")
    text.append("If unsure, lets 'do web research' to write on\n", style="bold red")
    text.append("If Testing-it-out/getting-started, choose 'Blog Tools\n", style="bold green")
    text.append("_______________________________________________________________________\n")

    print(text)
    
    questions = [
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Choose an option:',
            'choices': ['Write Blog', 'Do keyword Research', 'Create Blog Images',
                'Competitor Analysis', 'Blog Tools', 'Social Media', 'Quit'],
        }
    ]   
    answers = prompt(questions)
    mode = answers['mode']
    if mode == 'Write Blog':
        write_blog()
    elif mode == 'Do keyword Research':
        do_web_research()
    elif mode == 'Create Blog Images':
        faq_generator()
    elif mode == 'Competitor Analysis':
        # Metaphor similar search
        competitor_analysis()
    elif mode == 'Recent News Summarizer':
        print("""TBD: 1. Get tavily News.
                2. Get metaphor news.
                3. Get from NewsApi
                4. Get YOU.com News.""")
        recent_news_summarizer()
    elif mode == 'Blog Tools':
        blog_tools()
    elif mode == 'Social Media':
        print("""
        #whatsapp
        #instagram
        #youtube
        #twitter/X
        #Linked-in posts
        """)
        raise typer.Exit()
    elif mode == 'Quit':
        typer.echo("Exiting, F*** Off!")
        raise typer.Exit()


def get_api_key(api_key: str, api_description: str):
    """
    Ask the user to input the missing API key and add it to the .env file.

    Args:
        api_key (str): The name of the API key variable.
        api_description (str): The description of the API key.
    """
    user_input = typer.prompt(f"{api_description} is missing. Please enter {api_key} API Key:")
    with open(".env", "a") as env_file:
        env_file.write(f"{api_key}={user_input}\n")
    print(f"✅ {api_description} API Key added to .env file.")



def check_search_apis():
    """
    Check if necessary environment variables are present.
    Display messages with links on how to get them if not present.
    """
    print("\n\n🙋♂️  🙋♂️   Before doing web research, ensure the following API keys are available:")
    print("Blogen uses Basic, Semantic, Neural web search using above APIs for contextual blog generation.\n")

    api_keys = {
        "METAPHOR_API_KEY": "Metaphor AI Key (Get it here: [link=https://dashboard.exa.ai/login]Metaphor API[/link])",
        "TAVILY_API_KEY": "Tavily AI Key (Get it here: [link=https://tavily.com/#api]Tavily API[/link])",
        "SERPER_API_KEY": "Serper API Key (Get it here: [link=https://serper.dev/signup]SerperDev API[/link])",
    }

    missing_keys = []

    with typer.progressbar(api_keys.items(), label="Checking API keys", length=len(api_keys)) as progress:
        for key, description in progress:
            if os.getenv(key) is None:
                print(f"[bold red]✖ 🚫 {key} is missing:[/bold red] [link={key}]Get {key} API Key[/link]")
                missing_keys.append((key, description))

    if missing_keys:
        print("\nMost are Free APIs and really worth your while signing up for them.")
        print(":pile_of_poo: :pile_of_poo: GO GET THEM, on above urls. [bold red]")
        print("Note: They offer free/limited api calls, so we use most of them to have a lot of free api calls.")
        print("\n[bold red]TBD: Provide option to use user defined search engines.\n")
        for key, description in missing_keys:
            get_api_key(key, description)
    else:
        return True


def check_llm_environs():
    """ Function to check which LLM api is given. """
    gpt_provider = os.getenv("GPT_PROVIDER")
    
    if gpt_provider == "google":
        api_key_var = "GEMINI_API_KEY"
        missing_api_msg = f"To get your {api_key_var}, please visit: https://aistudio.google.com/app/apikey"
    elif gpt_provider == "openai":
        api_key_var = "OPENAI_API_KEY"
        missing_api_msg = "To get your OpenAI API key, please visit: https://openai.com/blog/openai-api"
    else:
        typer.echo("Unsupported GPT provider specified in GPT_PROVIDER environment variable.")
        return

    if os.getenv(api_key_var) is None:
        typer.echo(f"The {api_key_var} environment variable is missing.")
        typer.echo(missing_api_msg)
        api_key = typer.prompt(f"Please enter your {api_key_var} API Key:")
        # Update .env file
        with open(".env", "a") as env_file:
            env_file.write(f"{api_key_var}={api_key}\n")
        typer.echo(f"{api_key_var} API Key added to .env file.")
        return

    if gpt_provider == "openai" and os.getenv("OPENAI_API_KEY") is None:
        typer.echo("To get your OpenAI API key, please visit: https://openai.com/blog/openai-api") 


def faq_generator():
    return


def blog_tools():
    """ Blogging Aid Tools """
    os.system("clear" if os.name == "posix" else "cls")
    text = Text()
    text.append("_______________________________________________________________________")
    text.append("\n⚠️    Alert!   💥❓💥\n", style="bold red")
    text.append("Collection of Helpful Blogging Tools, powered by LLMs.\n", style="bold green")
    text.append("_______________________________________________________________________\n")

    print(text)

    # https://developers.google.com/speed/docs/insights/v5/get-started
    questions = [
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Choose a Blogging Tool:',
            'choices': ['Write Blog Title', 'Write Blog Meta Description', 'Write Blog Introduction',
                'Write Blog conclusion', 'Write Blog Outline', 'Generate Blog FAQs', 'Research blog referances',
                'Convert Blog To HTML', 'Convert Blog To Markdown', 'Blog Proof Reader',
                'Get Blog Tags', 'Get blog categories', 'Get Blog Code Examples', 'Check WebPage Performance',
                'Quit/Exit',],
        }
    ]
    answers = prompt(questions)
    mode = answers['mode']
    if mode == 'Write Blog Title':
        return

    
def competitor_analysis():
    """ Do metaphor similar search """
    text = Text()
    text.append("_______________________________________________________________________")
    text.append("\n⚠️    Alert!   💥❓💥\n", style="bold red")
    text.append("Provide competitor's URL, get details of similar/alternative companies.\n", style="bold red")
    text.append("Usecases: Know similar companies and alternatives, to given URL\n", style="bold blue")
    text.append("_______________________________________________________________________\n")
    print(text)
    similar_url = typer.prompt(f"Enter Valid URL to get web analysis")

    try:
        metaphor_find_similar(similar_url)
    except Exception as err:
        print(f"[bold red]✖ 🚫 Failed to do similar search.\nError:{err}[/bold red]")
    return


def write_blog():
    """
    Write Blog option with sub-options like Keywords, Audio YouTube, GitHub, and Scholar.
    """
    blog_type = write_blog_options()

    if blog_type == 'Keywords':
        blog_from_keyword()
    elif blog_type == 'Audio YouTube':
        audio_youtube = typer.prompt("Enter YouTube URL for audio blog generation:")
        print(f"Write audio blog based on YouTube URL: {audio_youtube}")
    elif blog_type == 'GitHub':
        github = typer.prompt("Enter GitHub URL, CSV file, or topic:")
        print(f"Write blog based on GitHub: {github}")
    elif blog_type == 'Scholar':
        scholar = typer.prompt("Enter research papers keywords:")
        print(f"Write blog based on scholar: {scholar}")
    elif blog_type == 'Quit':
        typer.echo("Exiting, F*** Off!")
        raise typer.Exit()


def blog_from_keyword():
    """ Write blog from given keyword. """
    print("Write blog based on keywords.")
    check_llm_environs()
    keywords = typer.prompt("Enter 'keywords/Blog Title' for blog generation:")
    final_blog = write_blog_from_keywords(keywords)


def do_web_research():
    """
    Do Web Research option with time_range, search_keywords, and include_urls sub-options.
    """
    if check_search_apis():
        while True:
            print("________________________________________________________________")
            search_keywords = typer.prompt("👋 Enter keywords for web research:")
            # Giving a single keywords, yields bad results.
            if search_keywords and len(search_keywords.split()) >= 2:
                break
            else:
                print("🚫 Search keywords should be at least three words long. Please try again.")

            # Display available choices
#            print("Choose from the following options:")
#            search_keyword_choices = ["choice1", "choice2", "choice3"]
#            for i, choice in enumerate(search_keyword_choices, start=1):
#                print(f"{i}. '{choice}'")
#
#            choice_index = typer.prompt("Enter the NUMBER to choose which keywords to use:")
#
#            try:
#                choice_index = int(choice_index)
#                if 1 <= choice_index <= len(search_keyword_choices):
#                    search_keywords = search_keyword_choices[choice_index - 1]
#                    break
#                else:
#                    print("🚫 Invalid choice. Please try again.")
#            except ValueError:
#                print("🚫 Invalid input. Please enter a valid number.")

        
        print("________________________________________________________________")
        time_range = prompt_for_time_range()

        os.system("clear" if os.name == "posix" else "cls")
        print("\n________________________________________________________________")
        print("\n🙋 Include a [green]URL[/green] to get [bold]similar/semantic[/bold]. For example, competitor's url.")
        print("📡 Usecases: Competitor Analysis Tool. Discover similar companies, startups and technologies.\n")
        similar_url = typer.prompt("👋 Enter a similar search URL (press Enter to continue):", default="")

        os.system("clear" if os.name == "posix" else "cls")
        print("\n________________________________________________________________")
        print("\n🙋 If you wish to [bold]confine search[/bold] to certain domains like wikipedia etc.\n")
        include_urls = typer.prompt("👋 Enter comma-separated URLs to include in web research (press Enter if none):", default="")
    
        try:
            print(f"🚀🚀 [bold green]Starting web research on given keywords: {search_keywords}..")
            #print(f"Web Research: Time Range - {time_range}, Search Keywords - {search_keywords}, Include URLs - {include_urls}")
            web_research_result = gpt_web_researcher(search_keywords,
                    time_range=time_range,
                    include_domains=include_urls,
                    similar_url=similar_url)
        except Exception as err:
            print(f"\n💥🤯 [bold red]ERROR 🤯 : Failed to do web research: {err}\n")


def check_internet():
    try:
        # Attempt to send a GET request to a well-known website
        response = requests.get("http://www.google.com", timeout=20)
        if not response.status_code == 200:
            print("💥🤯 WTFish, Internet is NOT available. Enjoy the wilderness..")
            exit(1)
        else:
            return
    except requests.ConnectionError:
        print("💥🤯 WTFish: Internet is NOT available. Enjoy the wilderness..")
        exit(1)
    except requests.Timeout:
        print("Request timed out. Internet might be slow.")
        exit(1)
    except Exception as e:
        print("Internet: An error occurred:", e)
        exit(1)

if __name__ == "__main__":
    check_internet()
    check_search_apis()
    check_llm_environs()
    app()
