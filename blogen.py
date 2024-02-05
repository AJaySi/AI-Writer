import os
from pathlib import Path

import typer
from PyInquirer import prompt
from rich import print
from rich.text import Text

from dotenv import load_dotenv
load_dotenv(Path('.env'))

app = typer.Typer()

from lib.ai_web_researcher.gpt_online_researcher import gpt_web_researcher



def prompt_for_time_range():
    os.system("clear" if os.name == "posix" else "cls")
    print("\n🙋 If you researching keywords that are recent than use accordingly, Default is Anytime.\n")
    questions = [
        {
            'type': 'list',
            'name': 'time_range',
            'message': '👋 Select Search result time range:',
            'choices': ["past day", "past week", "past month", "past year", "anytime"],
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
            'choices': ['Keywords', 'Audio YouTube', 'GitHub', 'Scholar', 'Quit'],
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
    text.append("_______________________________________________________________________\n")

    print(text)
    
    questions = [
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Choose an option:',
            'choices': ['Write Blog', 'Do Web Research', 'Competitor Analysis', 'FAQ Generator', 'Quit'],
        }
    ]   
    answers = prompt(questions)
    mode = answers['mode']
    if mode == 'Write Blog':
        write_blog()
    elif mode == 'Do Web Research':
        do_web_research()
    elif mode == 'FAQ Generator':
        faq_generator()
    elif mode == 'Competitor Analysis':
        # https://github.com/com-puter-tips/SEO-Analysis
        # https://github.com/sundios/SEO-Lighthouse-Multiple-URLs
        # https://github.com/Gingerbreadfork/Cutlery
        # Metaphor similar search
        competitor_analysis()
    elif mode == 'News Analysis':
        print("""1. Get tavily News.
                2. Get metaphor news.
                3. Get from NewsApi
                4. Get YOU.com News.""")
    elif mode == 'Quit':
        typer.echo("Exiting, Fuck Off!")
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



def check_environment_variables():
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
        print(":pile_of_poo::pile_of_poo::pile_of_poo: GO GET THEM, on above urls. [bold red]")
        print("Note: They offer free/limited api calls, so we use most of them to have a lot of free api calls.")
        print("\n[bold red]TBD: Provide option to use user defined search engines.\n")
        for key, description in missing_keys:
            get_api_key(key, description)
    else:
        return True

def faq_generator():
    return


def competitor_analysis():
    return


def write_blog():
    """
    Write Blog option with sub-options like Keywords, Audio YouTube, GitHub, and Scholar.
    """
    blog_type = write_blog_options()

    if blog_type == 'Keywords':
        keywords = typer.prompt("Enter keywords for blog generation:")
        print(f"Write blog based on keywords: {keywords}")
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
        typer.echo("Exiting, Fuck Off!")
        raise typer.Exit()


def do_web_research():
    """
    Do Web Research option with time_range, search_keywords, and include_urls sub-options.
    """
    if check_environment_variables():
        while True:
            print("________________________________________________________________")
            search_keywords = typer.prompt("👋 Enter keywords for web research:")
            if search_keywords and len(search_keywords.split()) >= 3:
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


if __name__ == "__main__":
    app()
