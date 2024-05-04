import os
from pathlib import Path
import configparser
from datetime import datetime

import typer
from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog, input_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl

from dotenv import load_dotenv
import requests
from rich import print
from rich.text import Text
load_dotenv(Path('.env'))

app = typer.Typer()

from lib.utils.alwrity_utils import blog_from_audio, blog_from_keyword, do_web_research, do_web_research, ai_news_writer
from lib.utils.alwrity_utils import write_story, essay_writer, blog_tools, competitor_analysis, image_to_text_writer, image_generator


def prompt_for_time_range():
    os.system("clear" if os.name == "posix" else "cls")
    print("\n🙋 If you're researching keywords that are recent, use accordingly. Default is Anytime.\n")
    choices = [("anytime", "Anytime"), ("past year", "Past Year"), ("past month", "Past Month"), 
               ("past week", "Past Week"), ("past day", "Past Day")]
    selected_time_range = radiolist_dialog(title="Select Search result time range:", values=choices).run()
    return selected_time_range[0] if selected_time_range else None


def write_blog_options():
    choices = [
        ("Keywords", "Keywords - Provide main blog keywords Or Title"),
        ("Audio To Blog", "Audio To Blog - Transcribe Audio files into blog content"),
        ("AI Story Writer", "AI Story Writer"),
        ("AI Essay Writer", "AI Essay writer"),
        ("AI News Articles", "News - AI News article writer, factual trusted sources"),
        ("Programming", "Programming - Write technical blogs on latest topics"),
        ("Scholar", "Scholar - Research Reports from google scholar, arxiv articles."),
        ("Finance/TBD", "Finance/TBD"),
        ("Quit", "Quit")
    ]
    selected_blog_type = radiolist_dialog(title="Choose a blog type:", values=choices).run()
    return selected_blog_type if selected_blog_type else None


@app.command()
def start_interactive_mode():
    os.system("clear" if os.name == "posix" else "cls")
    text = "_______________________________________________________________________\n"
    text += "\n⚠️    Alert!   💥❓💥\n"
    text += "Interactive tool, needs your attention/inputs, get off your mobile..'\n"
    text += "_______________________________________________________________________\n"
    print(text)
    
    choices = [
        ("AI Writers", "Choose AI Writers - (I Know What To Write)"),
        ("Content Planning", "Content Planning Tools - (I Don't Know, What to write)"),
        ("AI Image to Text Writer", "AI Image to Text Writer"),
        ("Online Blog Tools/Apps", "Online AI Apps - Content & Digital marketing"),
        ("Create Blog Images", "Create Images - Stability, Dalle3"),
        ("AI Social Media(TBD)", "AI Social Media(TBD)"),
        ("AI Code Writer(TBD)", "AI Code Writer(TBD)"),
        ("Quit", "Quit")
    ]
    mode = radiolist_dialog(title="Choose an option:", values=choices).run()
    if mode:
        if mode == 'AI Writers':
            write_blog()
        elif mode == 'AI Image to Text Writer':
            image_to_text_writer()
        elif mode == 'Create Blog Images':
            image_generator()
        elif mode == 'Content Planning':
            content_planning_tools()
        elif mode == 'Online Blog Tools/Apps':
            blog_tools()
        elif mode == 'AI Social Media(TBD)':
            print("""  #whatsapp  #instagram  #youtube  #twitter/X  #Linked-in posts  """)
            raise typer.Exit()
        elif mode == 'AI Code Writer(TBD)':
            print("Coming soon, TBD")
            raise typer.Exit()
        elif mode == 'Quit':
            typer.echo("Exiting, Getting Lost!")
            raise typer.Exit()


def content_planning_tools():
    """ """
    os.system("clear" if os.name == "posix" else "cls")
    text = "_______________________________________________________________________\n"
    text += "\n⚠️    Alert!   💥❓💥\n"
    text += "作家的障碍 - Writer's block - Bloqueo de escritor - Schreibblockade\n"
    text += "Use Google Keyword planner, google ads instead. Better tools than below.\n"
    text += "Note: Who Cares, just give some titles, keywords to get started.. To Err is Human & AI..\n"
    text += "_______________________________________________________________________\n"
    print(text)

    choices = [
        ("Do keyword Research", "Keywords web research - 🤓 Will read & earn my bread.."),
        ("Competitor Analysis", "Competitor Analysis - 🧐What's my neighbour doing.."),
        ("Blog Titles", "🥹🥹 Just give me Topic titles")
    ]
    mode = radiolist_dialog(title="Choose an option:", values=choices).run()
    
    if mode == 'Do keyword Research':
        if check_search_apis():
            do_web_research()
    elif mode == 'Competitor Analysis':
        competitor_analysis()


def check_search_apis():
    """
    Check if necessary environment variables are present.
    Display messages with links on how to get them if not present.
    """

    # Use rich.print for styling and hyperlinking
    print("Alwrity uses Basic, Semantic, Neural web search using above APIs for contextual blog generation.\n")

    api_keys = {
        "METAPHOR_API_KEY": "Metaphor AI Key (Get it here: [link=https://dashboard.exa.ai/login]Metaphor API[/link])",
        "TAVILY_API_KEY": "Tavily AI Key (Get it here: [link=https://tavily.com/#api]Tavily API[/link])",
        "SERPER_API_KEY": "Serper API Key (Get it here: [link=https://serper.dev/signup]SerperDev API[/link])",
    }

    missing_keys = []

    with typer.progressbar(api_keys.items(), label="Checking API keys", length=len(api_keys)) as progress:
        for key, description in progress:
            if os.getenv(key) is None:
                # Use rich.print for styling and hyperlinking
                print(f"[bold red]✖ 🚫 {key} is missing:[/bold red] [blue underline]Get {key} API Key[/blue underline]")
                missing_keys.append((key, description))

    if missing_keys:
        print("\nMost are Free APIs and really worth your while signing up for them.")
        print("💩💩💩: GO GET THEM, on above urls. [bold red]")
        #print("Note: They offer free/limited api calls, so we use most of them to have a lot of free api calls.")
        for key, description in missing_keys:
            get_api_key(key, description)
    else:
        return True


def get_api_key(api_key: str, api_description: str):
    """
    Ask the user to input the missing API key and add it to the .env file.

    Args:
        api_key (str): The name of the API key variable.
        api_description (str): The description of the API key.
    """
    print("\n\n")
    print(f"[bold green] 🙋 Attention Here: 🙋 -- {api_description}")
    user_input = typer.prompt(f"💩 -**Please Enter(copy/paste) {api_key} API Key** - Here🙋:")
    with open(".env", "a") as env_file:
        env_file.write(f"{api_key}={user_input}\n")
        print(f"✅ API Key added to .env file.")


def write_blog():
    blog_type = write_blog_options()
    if blog_type:
        if blog_type == 'Keywords':
            blog_from_keyword()
        elif mode == 'AI Story Writer':
            write_story()
        elif mode == 'AI Essay Writer':
            essay_writer()
        elif blog_type == 'Audio To Blog':
            blog_from_audio()
        elif blog_type == 'AI News Articles':
            ai_news_writer()
        elif blog_type == 'GitHub':
            github = prompt("Enter GitHub URL, CSV file, or topic:")
            print(f"Write blog based on GitHub: {github}")
        elif blog_type == 'Scholar':
            scholar = prompt("Enter research papers keywords:")
            print(f"Write blog based on scholar: {scholar}")
        elif blog_type == 'Quit':
            typer.echo("Exiting, Getting Lost..")
            raise typer.Exit()


def check_llm_environs():
    """ Function to check which LLM api is given. """
    # Load .env file
    load_dotenv(Path('.env'))
    gpt_provider = os.getenv("GPT_PROVIDER")
    
    # Disable unsupported GPT providers
    supported_providers = ['google', 'openai', 'mistralai']
    if gpt_provider is None or gpt_provider.lower() not in map(str.lower, supported_providers):
        # Prompt user to select a provider
        gpt_provider = radiolist_dialog(
            title="Select your GPT Provider(llm) from 'google', 'openai', 'mistralai'",
            values=[("google", "Google Gemini Pro"), ("openai", "OpenAI- ChatGPT"), ("mistralai", "MistralAI/WIP")]).run()
        # Update .env file
        os.environ["GPT_PROVIDER"] = gpt_provider
        with open(".env", "a") as env_file:
            env_file.write(f"GPT_PROVIDER={gpt_provider}\n")
            print(f"✅ API Key added to .env file.")

    if gpt_provider.lower() == "google":
        api_key_var = "GEMINI_API_KEY"
        missing_api_msg = f"To get your {api_key_var}, please visit: https://aistudio.google.com/app/apikey"
    elif gpt_provider.lower() == "openai": 
        api_key_var = "OPENAI_API_KEY"
        missing_api_msg = "To get your OpenAI API key, please visit: https://openai.com/blog/openai-api"
    elif gpt_provider.lower() == "mistralai":
        api_key_var = "MISTRAL_API_KEY"
        missing_api_msg = "To get your MistralAI API key, please visit: https://mistralai.com/api"

    if api_key_var not in os.environ:
        get_api_key(api_key_var, missing_api_msg)


def check_internet():
    try:
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


def create_env_file():
    env_file = Path('.env')
    if not env_file.is_file():
        try:
            with open('.env', 'w') as f:
                f.write('# Alwrity will add your environment variables here\n')
        except Exception as e:
            print(f"💥🤯Error occurred while creating .env file: {e}")


if __name__ == "__main__":
    print("Checking Internet..")
    check_internet()
    print("Creating .env file")
    create_env_file()
    print("Clear, all this..")
    os.system("clear" if os.name == "posix" else "cls")
    print("Checking Search APIs..")
    check_search_apis()
    print("Checking LLM APIs..")
    check_llm_environs()

    # Export the paths and file names. Dont want alwrity to be chatty and prompt for inputs.
    os.environ["SEARCH_SAVE_FILE"] = os.path.join(os.getcwd(), "lib", "workspace",
                                                  f"web_research_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    os.environ["IMG_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace")
    os.environ["CONTENT_SAVE_DIR"] = os.path.join(os.getcwd(), "lib", "workspace")

    load_dotenv(Path('.env'))
    app()
