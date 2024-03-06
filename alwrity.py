import os
from pathlib import Path

import typer
from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog, input_dialog
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from dotenv import load_dotenv
import requests
from rich import print
from rich.console import Console
from rich.text import Text

load_dotenv(Path('.env'))

app = typer.Typer()

from lib.ai_web_researcher.gpt_online_researcher import gpt_web_researcher
from lib.ai_web_researcher.metaphor_basic_neural_web_search import metaphor_find_similar
from lib.ai_writers.keywords_to_blog import write_blog_from_keywords


def prompt_for_time_range():
    os.system("clear" if os.name == "posix" else "cls")
    print("\n🙋 If you're researching keywords that are recent, use accordingly. Default is Anytime.\n")
    choices = [("anytime", "Anytime"), ("past year", "Past Year"), ("past month", "Past Month"), 
               ("past week", "Past Week"), ("past day", "Past Day")]
    selected_time_range = radiolist_dialog(title="Select Search result time range:", values=choices).run()
    return selected_time_range[0] if selected_time_range else None


def write_blog_options():
    choices = [
        ("Keywords", "Keywords"),
        ("Audio YouTube", "Audio YouTube"),
        ("Programming", "Programming"),
        ("Scholar", "Scholar"),
        ("News/TBD", "News/TBD"),
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
    text += "If you know what to write, choose 'Write Blog'\n"
    text += "If unsure, let's 'do web research' to write on\n"
    text += "If Testing-it-out/getting-started, choose 'Blog Tools\n"
    text += "_______________________________________________________________________\n"
    print(text)
    
    choices = [
        ("Write Blog", "Write Blog"),
        ("Do keyword Research", "Do keyword Research"),
        ("Create Blog Images", "Create Blog Images"),
        ("Competitor Analysis", "Competitor Analysis"),
        ("Blog Tools", "Blog Tools"),
        ("Social Media", "Social Media"),
        ("Quit", "Quit")
    ]
    mode = radiolist_dialog(title="Choose an option:", values=choices).run()
    if mode:
        if mode == 'Write Blog':
            write_blog()
        elif mode == 'Do keyword Research':
            do_web_research()
        elif mode == 'Create Blog Images':
            faq_generator()
        elif mode == 'Competitor Analysis':
            competitor_analysis()
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
            typer.echo("Exiting, Getting Lost!")
            raise typer.Exit()


def check_search_apis():
    """
    Check if necessary environment variables are present.
    Display messages with links on how to get them if not present.
    """
    # Create a Rich console
    console = Console()

    # Use rich.print for styling and hyperlinking
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
                # Use rich.print for styling and hyperlinking
                print(f"[bold red]✖ 🚫 {key} is missing:[/bold red] [blue underline]Get {key} API Key[/blue underline]")
                typer.echo(f"[bold red]✖ 🚫 {key} is missing:[/bold red] [link={key}]Get {key} API Key[/link]")
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
    user_input = typer.prompt(f"\n🙆🙆Please enter {api_key} API Key:")
    with open(".env", "a") as env_file:
        env_file.write(f"{api_key}={user_input}\n")
    print(f"✅ {api_description} API Key added to .env file.")


def faq_generator():
    return


def blog_tools():
    os.system("clear" if os.name == "posix" else "cls")
    text = "_______________________________________________________________________\n"
    text += "\n⚠️    Alert!   💥❓💥\n"
    text += "Collection of Helpful Blogging Tools, powered by LLMs.\n"
    text += "_______________________________________________________________________\n"
    print(text)

    choices = [
        ("Write Blog Title", "Write Blog Title"),
        ("Write Blog Meta Description", "Write Blog Meta Description"),
        ("Write Blog Introduction", "Write Blog Introduction"),
        ("Write Blog conclusion", "Write Blog conclusion"),
        ("Write Blog Outline", "Write Blog Outline"),
        ("Generate Blog FAQs", "Generate Blog FAQs"),
        ("Research blog references", "Research blog references"),
        ("Convert Blog To HTML", "Convert Blog To HTML"),
        ("Convert Blog To Markdown", "Convert Blog To Markdown"),
        ("Blog Proof Reader", "Blog Proof Reader"),
        ("Get Blog Tags", "Get Blog Tags"),
        ("Get blog categories", "Get blog categories"),
        ("Get Blog Code Examples", "Get Blog Code Examples"),
        ("Check WebPage Performance", "Check WebPage Performance"),
        ("Quit/Exit", "Quit/Exit")
    ]
    selected_tool = radiolist_dialog(title="Choose a Blogging Tool:", values=choices).run()
    if selected_tool:
        tool = selected_tool[0]
        if tool == 'Write Blog Title':
            return


def competitor_analysis():
    text = "_______________________________________________________________________\n"
    text += "\n⚠️    Alert!   💥❓💥\n"
    text += "Provide competitor's URL, get details of similar/alternative companies.\n"
    text += "Usecases: Know similar companies and alternatives, to given URL\n"
    text += "_______________________________________________________________________\n"
    print(text)
    similar_url = prompt("Enter Valid URL to get web analysis")
    try:
        metaphor_find_similar(similar_url)
    except Exception as err:
        print(f"[bold red]✖ 🚫 Failed to do similar search.\nError:{err}[/bold red]")
    return


def write_blog():
    blog_type = write_blog_options()
    if blog_type:
        if blog_type == 'Keywords':
            blog_from_keyword()
        elif blog_type == 'Audio YouTube':
            audio_youtube = prompt("Enter YouTube URL for audio blog generation:")
            print(f"Write audio blog based on YouTube URL: {audio_youtube}")
        elif blog_type == 'GitHub':
            github = prompt("Enter GitHub URL, CSV file, or topic:")
            print(f"Write blog based on GitHub: {github}")
        elif blog_type == 'Scholar':
            scholar = prompt("Enter research papers keywords:")
            print(f"Write blog based on scholar: {scholar}")
        elif blog_type == 'Quit':
            typer.echo("Exiting, Getting Lost..")
            raise typer.Exit()


def blog_from_keyword():
    """ Input blog keywords, research and write a factual blog."""
    while True:
            print("________________________________________________________________")
            blog_keywords = input_dialog(
                    title='Enter Keywords/Blog Title',
                    text='Shit in, Shit Out; Better keywords, better research, hence better content.\n👋 Enter keywords/Blog Title for blog generation:',
                ).run()

            # If the user cancels, exit the loop
            if blog_keywords is None:
                break
            if blog_keywords and len(blog_keywords.split()) >= 2:
                break
            else:
                message_dialog(
                    title='Warning',
                    text='🚫 Blog keywords should be at least two words long. Please try again.'
                ).run()
    if blog_keywords:
        try:
            write_blog_from_keywords(blog_keywords)
        except Exception as err:
            print(f"Failed to write blog on {blog_keywords}, Error: {err}\n")
            exit(1)


def do_web_research():
    """ Input keywords and do web research and present a report."""
    if check_search_apis():
        while True:
            print("________________________________________________________________")
            search_keywords = input_dialog(
                    title='Enter Search Keywords below:',
                    text='👋 Enter keywords for web research (Or keywords from your blog):',
                ).run()
            if search_keywords and len(search_keywords.split()) >= 2:
                break
            else:
                message_dialog(
                    title='Warning',
                    text='🚫 Search keywords should be at least three words long. Please try again.'
                ).run()
    selected_time_range = prompt_for_time_range()

    # Display input dialog for similar search URL (optional)
    similar_url = input_dialog(
        title="Enter a similar search URL",
        text="👋 Enter a similar search URL (Optional: Enter to skip):\n🙋Usecases: Competitor Analysis Tool. 📡Discover similar companies, startups and technologies.",
        default="",
    ).run()

    # Display input dialog for included URLs (optional)
    include_urls = input_dialog(
        title="Enter URLs to include in the web search:",
        text="👋 Enter comma-separated URLs to include in web research (press Enter to skip):\n🙋 If you wish to [bold]confine search[/bold] to certain domains like wikipedia etc.",
        default="",
    ).run()


    try:
        print(f"🚀🎬🚀 [bold green]Starting web research on given keywords: {search_keywords}..")
        #print(f"Web Research: Time Range - {time_range}, Search Keywords - {search_keywords}, Include URLs - {include_urls}")
        web_research_result = gpt_web_researcher(search_keywords,
                time_range=selected_time_range,
                include_domains=include_urls,
                similar_url=similar_url)
    except Exception as err:
        print(f"\n💥🤯 [bold red]ERROR 🤯 : Failed to do web research: {err}\n")


def check_llm_environs():
    """ Function to check which LLM api is given. """
    # Check if GPT_PROVIDER is defined in .env file
    gpt_provider = os.getenv("GPT_PROVIDER")

    # Load .env file
    load_dotenv()

    # Disable unsupported GPT providers
    supported_providers = ['google', 'openai', 'mistralai']
    if gpt_provider is None or gpt_provider.lower() not in supported_providers:
        #message_dialog(
        #    title="Unsupported GPT Provider",
        #    text="GPT_PROVIDER is not set or has an unsupported value."
        #).run()

        # Prompt user to select a provider
        selected_provider = radiolist_dialog(
            title='Select your preferred GPT provider:',
            text="Please choose GPT provider Below:\n👺Google Gemini recommended, its 🆓.",
            values=[
                ("Google", "google"),
                ("Openai", "openai"),
                ("MistralAI/WIP", "mistralai/WIP"),
                ("Ollama", "Ollama (TBD)")
            ]
        ).run()
        if selected_provider:
            gpt_provider = selected_provider

    if gpt_provider.lower() == "google":
        api_key_var = "GEMINI_API_KEY"
        missing_api_msg = f"To get your {api_key_var}, please visit: https://aistudio.google.com/app/apikey"
    elif gpt_provider.lower() == "openai":
        api_key_var = "OPENAI_API_KEY"
        missing_api_msg = "To get your OpenAI API key, please visit: https://openai.com/blog/openai-api"
    elif gpt_provider.lower() == "mistralai":
        api_key_var = "MISTRAL_API_KEY"
        missing_api_msg = "To get your MistralAI API key, please visit: https://mistralai.com/api"

    if os.getenv(api_key_var) is None:
        # Ask for the API key
        print(f"🚫The {api_key_var} is missing. {missing_api_msg}")
        api_key = typer.prompt(f"\n🙆🙆Please enter {api_key_var} API Key:")

        # Update .env file
        with open(".env", "a") as env_file:
            env_file.write(f"GPT_PROVIDER={gpt_provider.lower()}\n")
            env_file.write(f"{api_key_var}={api_key}\n")


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
    print("Checking Internet, lets get the basics right.")
    check_internet()
    print("Create .env file, if not Present working directory")
    create_env_file()
    print("Check Metaphor, Tavily, YOU.com Search API keys.")
    check_search_apis()
    print("Check LLM details & AI Model to use.")
    check_llm_environs()
    load_dotenv(Path('.env'))
    app()
