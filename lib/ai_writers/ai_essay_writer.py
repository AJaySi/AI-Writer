#####################################################
#
# Alwrity, AI essay writer - Essay_Writing_with_Prompt_Chaining
#
#####################################################

import os
from pathlib import Path
from dotenv import load_dotenv
from pprint import pprint
from loguru import logger
import sys

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def generate_with_retry(prompt, system_prompt=None):
    """
    Generates content using the llm_text_gen function with retry handling for errors.

    Parameters:
        prompt (str): The prompt to generate content from.
        system_prompt (str, optional): Custom system prompt to use instead of the default one.

    Returns:
        str: The generated content.
    """
    try:
        # Use llm_text_gen instead of directly calling the model
        return llm_text_gen(prompt, system_prompt)
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return ""


def ai_essay_generator(essay_title, selected_essay_type, selected_education_level, selected_num_pages):
    """
    Write an Essay using prompt chaining and iterative generation.

    Parameters:
        essay_title (str): The title or topic of the essay.
        selected_essay_type (str): The type of essay to write.
        selected_education_level (str): The education level of the target audience.
        selected_num_pages (int): The number of pages or words for the essay.
    """
    logger.info(f"Starting to write Essay on {essay_title}..")
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

        # Generate prompts
        try:
            premise = generate_with_retry(premise_prompt)
            logger.info(f"The title of the Essay is: {premise}")
        except Exception as err:
            logger.error(f"Essay title Generation Error: {err}")
            return

        outline = generate_with_retry(outline_prompt.format(premise=premise))
        logger.info(f"The Outline of the essay is: {outline}\n\n")
        if not outline:
            logger.error("Failed to generate Essay outline. Exiting...")
            return

        try:
            starting_draft = generate_with_retry(
                    starting_prompt.format(premise=premise, outline=outline))
            pprint(starting_draft)
        except Exception as err:
            logger.error(f"Failed to Generate Essay draft: {err}")
            return

        try:
            draft = starting_draft
            continuation = generate_with_retry(
                    continuation_prompt.format(premise=premise, outline=outline, story_text=draft))
            pprint(continuation)
        except Exception as err:
            logger.error(f"Failed to write the initial draft: {err}")

        # Add the continuation to the initial draft, keep building the story until we see 'IAMDONE'
        try:
            draft += '\n\n' + continuation
        except Exception as err:
            logger.error(f"Failed as: {err} and {continuation}")
        while 'IAMDONE' not in continuation:
            try:
                continuation = generate_with_retry(
                        continuation_prompt.format(premise=premise, outline=outline, story_text=draft))
                draft += '\n\n' + continuation
            except Exception as err:
                logger.error(f"Failed to continually write the Essay: {err}")
                return

        # Remove 'IAMDONE' and print the final story
        final = draft.replace('IAMDONE', '').strip()
        pprint(final)
        return final

    except Exception as e:
        logger.error(f"Main Essay writing: An error occurred: {e}")
        return ""
