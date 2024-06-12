#####################################################
#
# Alwrity, AI essay writer - Essay_Writing_with_Prompt_Chaining
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


def ai_essay_generator(essay_title, selected_essay_type, selected_education_level, selected_num_pages):
    """
    Write an Essay using prompt chaining and iterative generation.

    Parameters:
        persona (str): The persona statement for the author.
        story_genre (str): The genre of the story.
        characters (str): The characters in the story.
    """
    print(f"Starting to write Essay on {essay_title}..")
    try:
        # Define persona and writing guidelines
        guidelines = f'''\
        Writing Guidelines

        As an expert Essay writer and academic researcher, demostrate your world class essay writing skills.
        
        Follow the below writing guidelines for writing your essay:
        1). You specialize in {selected_essay_type} essay writing.
        2). Your target audiences include readers from {selected_education_level} level.
        3). The title of the essay is {essay_title}.
        5). The final essay should of {selected_num_pages} words/pages.
        3). Plant the seeds of subplots or potential character arc shifts that can be expanded later.

        Remember, your main goal is to write as much as you can. If you get through
        the story too fast, that is bad. Expand, never summarize.
        '''
        # Generate prompts
        premise_prompt = f'''\
        As an expert essay writer, specilizing in {selected_essay_type} essay writing.

        Write an Essay title for given keywords {essay_title}. 
        The title should appeal to audience level of {selected_education_level}.
        '''

        outline_prompt = f'''\
        As an expert essay writer, specilizing in {selected_essay_type} essay writing.

        Your Essay title is:

        {{premise}}

        Write an outline for the essay.
        '''

        starting_prompt = f'''\
        As an expert essay writer, specilizing in {selected_essay_type} essay writing.

        Your essay title is:

        {{premise}}

        The outline of the Essay is:

        {{outline}}

        First, silently review the outline and the essay title. Consider how to start the Essay.
        Start to write the very beginning of the Essay. You are not expected to finish
        the whole Essay now. Your writing should be detailed enough that you are only
        scratching the surface of the first bullet of your outline. Try to write AT
        MINIMUM 1000 WORDS.

        {guidelines}
        '''

        continuation_prompt = f'''\
        As an expert essay writer, specilizing in {selected_essay_type} essay writing.

        Your essay title is:

        {{premise}}

        The outline of the Essay is:

        {{outline}}

        You've begun to write the essay and continue to do so.
        Here's what you've written so far:

        {{story_text}}

        =====

        First, silently review the outline and essay so far. 
        Identify what the single next part of your outline you should write.

        Your task is to continue where you left off and write the next part of the Essay.
        You are not expected to finish the whole essay now. Your writing should be
        detailed enough that you are only scratching the surface of the next part of
        your outline. Try to write AT MINIMUM 1000 WORDS. However, only once the essay
        is COMPLETELY finished, write IAMDONE. Remember, do NOT write a whole chapter
        right now.

        {guidelines}
        '''

        # Configure generative AI
        load_dotenv(Path('../.env'))
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-pro')

        # Generate prompts
        try:
            premise = generate_with_retry(model, premise_prompt).text
            print(f"The title of the Essay is: {premise}")
        except Exception as err:
            print(f"Essay title Generation Error: {err}")
            return

        outline = generate_with_retry(model, outline_prompt.format(premise=premise)).text
        print(f"The Outline of the essay is: {outline}\n\n")
        if not outline:
            print("Failed to generate Essay outline. Exiting...")
            return

        try:
            starting_draft = generate_with_retry(model, 
                    starting_prompt.format(premise=premise, outline=outline)).text
            pprint(starting_draft)
        except Exception as err:
            print(f"Failed to Generate Essay draft: {err}")
            return

        try:
            draft = starting_draft
            continuation = generate_with_retry(model, 
                    continuation_prompt.format(premise=premise, outline=outline, story_text=draft)).text
            pprint(continuation)
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
                print(f"Failed to continually write the Essay: {err}")
                return

        # Remove 'IAMDONE' and print the final story
        final = draft.replace('IAMDONE', '').strip()
        pprint(final)

    except Exception as e:
        print(f"Main Essay writing: An error occurred: {e}")
