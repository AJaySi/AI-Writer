import os
from pathlib import Path
import configparser
from datetime import datetime

from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog, input_dialog
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog

from lib.ai_web_researcher.gpt_online_researcher import gpt_web_researcher
from lib.ai_web_researcher.metaphor_basic_neural_web_search import metaphor_find_similar
from lib.ai_writers.keywords_to_blog import write_blog_from_keywords
from lib.ai_writers.speech_to_blog.main_audio_to_blog import generate_audio_blog
from lib.gpt_providers.text_generation.ai_story_writer import ai_story_generator
from lib.gpt_providers.text_generation.ai_essay_writer import ai_essay_generator


def blog_from_audio():
    """
    Prompt the user to input either a YouTube URL, a file location, or keywords to search on YouTube.
    Validate the input and take appropriate actions based on the input type.
    """

    while True:
        print("https://github.com/AJaySi/AI-Blog-Writer/wiki/Audio-to-blog-AI-article-writer-%E2%80%90-Alwrity-Speech-To-Text-Feature")
        audio_input = prompt("""Enter Youtube video URL OR provide Full-Path to audio file.\n👋 : """)
        # If the user cancels, exit the loop and the application
        if audio_input is None:
            break

        # If the user presses OK without providing any input, prompt again
        if not audio_input.strip():
            continue

        # Check if the input is a valid YouTube URL
        if audio_input.startswith("https://www.youtube.com/") or audio_input.startswith("http://www.youtube.com/") or os.path.exists(audio_input):
            # Validate YouTube URL, Process YouTube URL
            generate_audio_blog(audio_input)
            break


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
                    title='Error',
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
                    title='Enter Search Keywords below: More Options in main_config.',
                    text='👋 Enter keywords for web research (Or keywords from your blog):',
                ).run()
            if search_keywords and len(search_keywords.split()) >= 2:
                break
            else:
                message_dialog(
                    title='Warning',
                    text='🚫 Search keywords should be at least three words long. Please try again.'
                ).run()

    try:
        print(f"🚀🎬🚀 [bold green]Starting web research on given keywords: {search_keywords}..")
        web_research_result = gpt_web_researcher(search_keywords)
    except Exception as err:
        print(f"\n💥🤯 [bold red]ERROR 🤯 : Failed to do web research: {err}\n")

def write_story():
    """ Alwrity AI Story Writer """
    personas = [
        ("Award-Winning Science Fiction Author", "Award-Winning Science Fiction Author"),
        ("Historical Fiction Author", "Historical Fiction Author"),
        ("Fantasy World Builder", "Fantasy World Builder"),
        ("Mystery Novelist", "Mystery Novelist"),
        ("Romantic Poet", "Romantic Poet"),
        ("Thriller Writer", "Thriller Writer"),
        ("Children's Book Author", "Children's Book Autho"),
        ("Satirical Humorist", "Satirical Humorist"),
        ("Biographical Writer", "Biographical Writer"),
        ("Dystopian Visionary", "Dystopian Visionary"),
        ("Magical Realism Author", "Magical Realism Author")
    ]

    dialog = radiolist_dialog(
        title="Select Your Story Writing Persona Or Book Genre",
        text="Choose a persona that resonates you want AI Story Writer to adopt.",
        values=personas
    )

    selected_persona_name = dialog.run()
    # Define persona descriptions
    persona_descriptions = {
        "Award-Winning Science Fiction Author": "You are an award-winning science fiction author with a penchant for expansive, intricately woven stories. Your ultimate goal is to write the next award-winning sci-fi novel.",
        "Historical Fiction Author": "You are a seasoned historical fiction author, meticulously researching past eras to weave captivating narratives. Your goal is to transport readers to different times and places through your vivid storytelling.",
        "Fantasy World Builder": "You are a world-building enthusiast, crafting intricate realms filled with magic, mythical creatures, and epic quests. Your ambition is to create the next immersive fantasy saga that captivates readers' imaginations.",
        "Mystery Novelist": "You are a master of suspense and intrigue, intricately plotting out mysteries with unexpected twists and turns. Your aim is to keep readers on the edge of their seats, eagerly turning pages to unravel the truth.",
        "Romantic Poet": "You are a romantic at heart, composing verses that capture the essence of love, longing, and human connections. Your dream is to write the next timeless love story that leaves readers swooning.",
        "Thriller Writer": "You are a thrill-seeker, crafting adrenaline-pumping tales of danger, suspense, and high-stakes action. Your mission is to keep readers hooked from start to finish with heart-pounding thrills and unexpected twists.",
        "Children's Book Author": "You are a storyteller for the young and young at heart, creating whimsical worlds and lovable characters that inspire imagination and wonder. Your goal is to spark joy and curiosity in young readers with enchanting tales.",
        "Satirical Humorist": "You are a keen observer of society, using humor and wit to satirize the absurdities of everyday life. Your aim is to entertain and provoke thought, delivering biting social commentary through clever and humorous storytelling.",
        "Biographical Writer": "You are a chronicler of lives, delving into the stories of real people and events to illuminate the human experience. Your passion is to bring history to life through richly detailed biographies that resonate with readers.",
        "Dystopian Visionary": "You are a visionary writer, exploring dark and dystopian futures that reflect contemporary fears and anxieties. Your vision is to challenge societal norms and provoke reflection on the path humanity is heading.",
        "Magical Realism Author": "You are a purveyor of magical realism, blending the ordinary with the extraordinary to create enchanting and thought-provoking tales. Your goal is to blur the lines between reality and fantasy, leaving readers enchanted and introspective."
    }
    if selected_persona_name:
        selected_persona = next((persona for persona in personas if persona[0] == selected_persona_name), None)
        if selected_persona:
            character_input = input_dialog(
                title=f"Enter characters for {selected_persona[0]}",
                text=persona_descriptions[selected_persona_name]
            ).run()

    #FIXME/TBD: Presently supports gemini only. Openai, minstral coming up.
    # Check if LLM API KEYS are present and Not none.
    if os.getenv('GEMINI_API_KEY'):
        ai_story_generator(selected_persona_name, selected_persona_name, character_input)
    else:
        print(f"ERROR: Provide Google Gemini API keys. Openai, mistral, ollama coming up.")
        exit(1)



def essay_writer():
    # Define essay types and education levels
    essay_types = [
        ("Argumentative", "Argumentative - Forming an opinion via research. Building an evidence-based argument."),
        ("Expository", "Expository - Knowledge of a topic. Communicating information clearly."),
        ("Narrative", "Narrative - Creative language use. Presenting a compelling narrative."),
        ("Descriptive", "Descriptive - Creative language use. Describing sensory details.")
    ]

    education_levels = [
        ("Primary School", "Primary School"),
        ("High School", "High School"),
        ("College", "College"),
        ("Graduate School", "Graduate School")
    ]

    # Define the options for number of pages
    num_pages_options = [
        ("Short Form (1-2 pages)", "Short Form"),
        ("Medium Form (3-5 pages)", "Medium Form"),
        ("Long Form (6+ pages)", "Long Form")
    ]

    # Ask the user for the title of the essay
    essay_title = input_dialog(title="Essay Title", text="Enter the title of your essay:").run()
    while not essay_title.strip():
        print("Please enter a valid title for your essay.")
        essay_title = input_dialog(title="Essay Title", text="Enter the title of your essay:").run()

    # Ask the user for type of essay, level of education, and number of pages
    selected_essay_type = radiolist_dialog(title="Type of Essay", text="Choose the type of essay you want to write:",
                                           values=essay_types).run()

    selected_education_level = radiolist_dialog(title="Level of Education", text="Choose your level of education:",
                                               values=education_levels).run()

    # Prompt the user to select the length of the essay
    num_pages_prompt = "Select the length of your essay:"
    selected_num_pages = radiolist_dialog(title="Number of Pages", text=num_pages_prompt, values=num_pages_options).run()

    ai_essay_generator(essay_title, selected_essay_type, selected_education_level, selected_num_pages)



def blog_tools():
    os.system("clear" if os.name == "posix" else "cls")
    text = "_______________________________________________________________________\n"
    text += "\n⚠️    Alert!   💥❓💥\n"
    text += "Collection of Helpful Blogging Tools, powered by LLMs.\n"
    text += "_______________________________________________________________________\n"
    print(text)

    personas = [
        ("Get Content Outline", "Get Content Outline"),
        ("Write Blog Title", "Write Blog Title"),
        ("Write Blog Meta Description", "Write Blog Meta Description"),
#        ("Write Blog Introduction", "Write Blog Introduction"),
#        ("Write Blog conclusion", "Write Blog conclusion"),
#        ("Write Blog Outline", "Write Blog Outline"),
        ("Generate Blog FAQs", "Generate Blog FAQs"),
        ("AI Linkedin Post", "AI Linkedin Post"),
        ("YouTube To Blog", "YouTube To Blog"),
        ("AI Essay Writer", "AI Essay Writer"),
        ("AI Story Writer", "AI Story Writer"),
#        ("Research blog references", "Research blog references"),
#        ("Convert Blog To HTML", "Convert Blog To HTML"),
#        ("Convert Blog To Markdown", "Convert Blog To Markdown"),
#        ("Blog Proof Reader", "Blog Proof Reader"),
#        ("Get Blog Tags", "Get Blog Tags"),
#        ("Get blog categories", "Get blog categories"),
#        ("Get Blog Code Examples", "Get Blog Code Examples"),
#        ("Check WebPage Performance", "Check WebPage Performance"),
        ("Quit/Exit", "Quit/Exit")
    ]
    dialog = radiolist_dialog(
        title = "Select Your AI content tool.",
        text = "Choose a tool to use and visit provided online link to try them out.",
        values = personas
    )

    selected_persona_name = dialog.run()

    persona_descriptions = {
        "Get Content Outline": "Get Content Outline - VISIT: https://alwrity-outline.streamlit.app/",
        "Write Blog Title": "Write Blog Title - VISIT: https://alwrity-title.streamlit.app/",
        "Write Blog Meta Description": "Write Blog Meta Description - VISIT: https://alwrity-metadesc.streamlit.app/",
#        "Write Blog Introduction": "Write Blog Introduction - To Be Done (TBD)",
#        "Write Blog conclusion": "Write Blog conclusion - ",
#        "Write Blog Outline": "Write Blog Outline - ",
        "Generate Blog FAQs": "Generate Blog FAQs - VISIT: https://alwrity-faq.streamlit.app/",
        "AI Linkedin Post": "AI Linkedin Post writer - VISIT: https://alwrity-linkedin.streamlit.app/",
        "YouTube To Blog": "YouTube To Blog - VISIT: https://alwrity-yt-blog.streamlit.app/",
        "AI Essay Writer": "AI Essay Writer - VISIT: https://alwrity-essay.streamlit.app/",
        "AI Story Writer": "AI Story Writer - VISIT: https://alwrity-story.streamlit.app/",
#        "Research blog references": "Research blog references - Example: https://example.com/research-blog-references",
#        "Convert Blog To HTML": "Convert Blog To HTML - Example: https://example.com/convert-blog-to-html",
#        "Convert Blog To Markdown": "Convert Blog To Markdown - Example: https://example.com/convert-blog-to-markdown",
#        "Blog Proof Reader": "Blog Proof Reader - Example: https://example.com/blog-proof-reader",
#        "Get Blog Tags": "Get Blog Tags - Example: https://example.com/get-blog-tags",
#        "Get blog categories": "Get blog categories - Example: https://example.com/get-blog-categories",
#        "Get Blog Code Examples": "Get Blog Code Examples - Example: https://example.com/get-blog-code-examples",
#        "SEO Checks": "SEO checks - TBD",
        "Quit/Exit": "Quit/Exit - Example: Quit/Exit"
    }

    if selected_persona_name:
        selected_persona = next((persona for persona in personas if persona[0] == selected_persona_name), None)
        if selected_persona:
            character_input = message_dialog(
                    title=f"To Try {selected_persona_name}, Visit below URL:",
                    text=persona_descriptions[selected_persona_name]
            ).run()



def competitor_analysis():
    text = "_______________________________________________________________________\n"
    text += "\n⚠️    Alert!   💥❓💥\n"
    text += "Provide competitor's URL, get details of similar/alternative companies.\n"
    text += "Usecases: Know similar companies and alternatives, to given URL\n"
    text += "Usecases: Write about similar companies, tools, alternative-to, similar products, similar websites etc\n"
    text += "Read More Here: https://docs.exa.ai/reference/company-analyst \n"
    text += "_______________________________________________________________________\n"
    print(text)
    similar_url = prompt("Enter Valid URL to get web analysis:: ")
    try:
        metaphor_find_similar(similar_url)
    except Exception as err:
        print(f"[bold red]✖ 🚫 Failed to do similar search.\nError:{err}[/bold red]")
    return

