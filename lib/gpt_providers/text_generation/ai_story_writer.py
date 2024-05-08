#####################################################
#
# google-gemini-cookbook - Story_Writing_with_Prompt_Chaining
#
#####################################################

import os
from pathlib import Path
from dotenv import load_dotenv
from google.api_core import retry
import google.generativeai as genai
from pprint import pprint


def generate_with_retry(model, prompt):
    """
    Generates content from the model with retry handling for errors.

    Parameters:
        model (GenerativeModel): The generative model to use for content generation.
        prompt (str): The prompt to generate content from.

    Returns:
        str: The generated content.
    """
    try:
        # FIXME: Need a progress bar here.
        return model.generate_content(prompt, request_options={'retry':retry.Retry()})
    except Exception as e:
        print(f"Error generating content: {e}")
        return ""

def ai_story_generator(persona, story_genre, characters):
    """
    Write a story using prompt chaining and iterative generation.

    Parameters:
        persona (str): The persona statement for the author.
        story_genre (str): The genre of the story.
        characters (str): The characters in the story.
    """
    print(f"Starting to write {story_genre} story based on characters: {characters}..")
    try:
        # Define persona and writing guidelines
        guidelines = f'''\
        Writing Guidelines

        Delve deeper. Lose yourself in the world you're building. Unleash vivid
        descriptions to paint the scenes in your reader's mind.
        Develop your characters—let their motivations, fears, and complexities unfold naturally.
        Weave in the threads of your outline, but don't feel constrained by it.
        Allow your story to surprise you as you write. Use rich imagery, sensory details, and
        evocative language to bring the setting, characters, and events to life.
        Introduce elements subtly that can blossom into complex subplots, relationships,
        or worldbuilding details later in the story.
        Keep things intriguing but not fully resolved.
        Avoid boxing the story into a corner too early.
        Plant the seeds of subplots or potential character arc shifts that can be expanded later.

        Remember, your main goal is to write as much as you can. If you get through
        the story too fast, that is bad. Expand, never summarize.
        '''

        # Generate prompts
        premise_prompt = f'''\
        {persona}

        Write a single sentence premise for a {story_genre} story featuring {characters}.
        '''

        outline_prompt = f'''\
        {persona}

        You have a gripping premise in mind:

        {{premise}}

        Write an outline for the plot of your story.
        '''

        starting_prompt = f'''\
        {persona}

        You have a gripping premise in mind:

        {{premise}}

        Your imagination has crafted a rich narrative outline:

        {{outline}}

        First, silently review the outline and the premise. Consider how to start the
        story.

        Start to write the very beginning of the story. You are not expected to finish
        the whole story now. Your writing should be detailed enough that you are only
        scratching the surface of the first bullet of your outline. Try to write AT
        MINIMUM 5000 WORDS.

        {guidelines}
        '''

        continuation_prompt = f'''\
        {persona}

        You have a gripping premise in mind:

        {{premise}}

        Your imagination has crafted a rich narrative outline:

        {{outline}}

        You've begun to immerse yourself in this world, and the words are flowing.
        Here's what you've written so far:

        {{story_text}}

        =====

        First, silently review the outline and story so far. Identify what the single
        next part of your outline you should write.

        Your task is to continue where you left off and write the next part of the story.
        You are not expected to finish the whole story now. Your writing should be
        detailed enough that you are only scratching the surface of the next part of
        your outline. Try to write AT MINIMUM 2000 WORDS. However, only once the story
        is COMPLETELY finished, write IAMDONE. Remember, do NOT write a whole chapter
        right now.

        {guidelines}
        '''

        # Configure generative AI
        load_dotenv(Path('../.env'))
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-1.0-pro')

        # Generate prompts
        try:
            premise = generate_with_retry(model, premise_prompt).text
            print(f"The premise of the story is: {premise}")
        except Exception as err:
            print(f"Premise Generation Error: {err}")
            return

        outline = generate_with_retry(model, outline_prompt.format(premise=premise)).text
        print(f"The Outline of the story is: {outline}\n\n")
        if not outline:
            print("Failed to generate outline. Exiting...")
            return

        # Generate starting draft
        try:
            starting_draft = generate_with_retry(model, 
                    starting_prompt.format(premise=premise, outline=outline)).text
        except Exception as err:
            print(f"Failed to Generate Story draft: {err}")
            return

        try:
            draft = starting_draft
            continuation = generate_with_retry(model, 
                    continuation_prompt.format(premise=premise, outline=outline, story_text=draft)).text
        except Exception as err:
            print(f"Failed to write the initial draft: {err}")

        # Add the continuation to the initial draft, keep building the story until we see 'IAMDONE'
        try:
            draft += '\n\n' + continuation
        except Exception as err:
            print(f"Failed as: {err} and {continuation}")
        while 'IAMDONE' not in continuation:
            try:
                continuation = generate_with_retry(model, 
                        continuation_prompt.format(premise=premise, outline=outline, story_text=draft)).text
                draft += '\n\n' + continuation
            except Exception as err:
                print(f"Failed to continually write the story: {err}")
                return

        # Remove 'IAMDONE' and print the final story
        final = draft.replace('IAMDONE', '').strip()
        print(final)

    except Exception as e:
        print(f"Main Story writing: An error occurred: {e}")
