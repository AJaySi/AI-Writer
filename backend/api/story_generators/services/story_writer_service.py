"""
AI Story Writer Service

This service provides the core functionality for generating stories using AI,
converted from the original Streamlit implementation to work with FastAPI.
"""

import asyncio
import time
from typing import Dict, Any, Optional, Generator
from ..core.logging import get_logger
from ..core.exceptions import StoryGenerationError, ModelConnectionError
from ...services.llm_providers.main_text_generation import llm_text_gen

logger = get_logger(__name__)


class StoryWriterService:
    """Service for generating AI stories with prompt chaining."""
    
    def __init__(self):
        """Initialize the story writer service."""
        self.logger = logger
    
    async def generate_story(
        self,
        persona: str,
        story_setting: str,
        character_input: str,
        plot_elements: str,
        writing_style: str,
        story_tone: str,
        narrative_pov: str,
        audience_age_group: str,
        content_rating: str,
        ending_preference: str,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete story using prompt chaining and iterative generation.
        
        Args:
            persona: The writing persona/author type
            story_setting: The setting where the story takes place
            character_input: Information about the main characters
            plot_elements: Plot elements including theme, key events, and main conflict
            writing_style: The writing style for the story
            story_tone: The overall tone or mood of the story
            narrative_pov: The narrative point of view
            audience_age_group: Target audience age group
            content_rating: Content rating for the story
            ending_preference: Preferred type of ending
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing the generated story and metadata
        """
        try:
            logger.log_generation_start("story", {
                "persona": persona,
                "setting": story_setting,
                "style": writing_style
            })
            
            start_time = time.time()
            
            # Update progress
            if progress_callback:
                await progress_callback("Generating story premise...", 10)
            
            # Generate premise
            premise = await self._generate_premise(
                persona, story_setting, character_input
            )
            
            if not premise:
                raise StoryGenerationError("Failed to generate story premise")
            
            logger.info("Story premise generated", premise_length=len(premise))
            
            # Update progress
            if progress_callback:
                await progress_callback("Creating story outline...", 25)
            
            # Generate outline
            outline = await self._generate_outline(persona, premise)
            
            if not outline:
                raise StoryGenerationError("Failed to generate story outline")
            
            logger.info("Story outline generated", outline_length=len(outline))
            
            # Update progress
            if progress_callback:
                await progress_callback("Writing initial draft...", 40)
            
            # Generate initial draft
            initial_draft = await self._generate_initial_draft(
                persona, premise, outline, story_setting, character_input,
                plot_elements, writing_style, story_tone, narrative_pov,
                audience_age_group, content_rating, ending_preference
            )
            
            if not initial_draft:
                raise StoryGenerationError("Failed to generate initial draft")
            
            logger.info("Initial draft generated", draft_length=len(initial_draft))
            
            # Update progress
            if progress_callback:
                await progress_callback("Continuing story development...", 60)
            
            # Continue story until completion
            final_story = await self._continue_story(
                persona, premise, outline, initial_draft, progress_callback
            )
            
            duration = time.time() - start_time
            word_count = len(final_story.split())
            character_count = len(final_story)
            
            logger.log_generation_complete("story", duration, True)
            
            # Update progress
            if progress_callback:
                await progress_callback("Story generation completed!", 100)
            
            return {
                "success": True,
                "story": final_story,
                "premise": premise,
                "outline": outline,
                "word_count": word_count,
                "character_count": character_count,
                "generation_time": duration
            }
            
        except Exception as e:
            logger.error_with_context(e, {
                "persona": persona,
                "setting": story_setting
            })
            
            if isinstance(e, StoryGenerationError):
                raise e
            else:
                raise StoryGenerationError(f"Story generation failed: {str(e)}")
    
    async def _generate_premise(
        self, persona: str, story_setting: str, character_input: str
    ) -> str:
        """Generate a story premise."""
        try:
            prompt = f"""
            {persona}
            
            Write a single sentence premise for a {story_setting} story featuring {character_input}.
            """
            
            result = await asyncio.to_thread(llm_text_gen, prompt)
            return result.strip() if result else ""
            
        except Exception as e:
            logger.error(f"Premise generation failed: {str(e)}")
            return ""
    
    async def _generate_outline(self, persona: str, premise: str) -> str:
        """Generate a story outline."""
        try:
            prompt = f"""
            {persona}
            
            You have a gripping premise in mind:
            
            {premise}
            
            Write an outline for the plot of your story.
            """
            
            result = await asyncio.to_thread(llm_text_gen, prompt)
            return result.strip() if result else ""
            
        except Exception as e:
            logger.error(f"Outline generation failed: {str(e)}")
            return ""
    
    async def _generate_initial_draft(
        self,
        persona: str,
        premise: str,
        outline: str,
        story_setting: str,
        character_input: str,
        plot_elements: str,
        writing_style: str,
        story_tone: str,
        narrative_pov: str,
        audience_age_group: str,
        content_rating: str,
        ending_preference: str
    ) -> str:
        """Generate the initial story draft."""
        try:
            # Build the persona with story details
            detailed_persona = f"""{persona}
            Write a story with the following details:

            **The story Setting is:**
            {story_setting}
            
            **The Characters of the story are:**
            {character_input}
            
            **Plot Elements of the story:**
            {plot_elements}
            
            **Story Writing Style:**
            {writing_style}
            
            **The story Tone is:**
            {story_tone}
            
            **Write story from the Point of View of:**
            {narrative_pov}
            
            **Target Audience of the story:**
            {audience_age_group}, **Content Rating:** {content_rating}
            
            **Story Ending:**
            {ending_preference}
            
            Make sure the story is engaging and tailored to the specified audience and content rating. 
            Ensure the ending aligns with the preference indicated.
            """
            
            # Define writing guidelines
            guidelines = """
            Writing Guidelines:

            Delve deeper. Lose yourself in the world you're building. Unleash vivid
            descriptions to paint the scenes in your reader's mind.
            Develop your characters — let their motivations, fears, and complexities unfold naturally.
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
            """
            
            prompt = f"""
            {detailed_persona}

            You have a gripping premise in mind:

            {premise}

            Your imagination has crafted a rich narrative outline:

            {outline}

            First, silently review the outline and the premise. Consider how to start the
            story.

            Start to write the very beginning of the story. You are not expected to finish
            the whole story now. Your writing should be detailed enough that you are only
            scratching the surface of the first bullet of your outline. Try to write AT
            MINIMUM 4000 WORDS.

            {guidelines}
            """
            
            result = await asyncio.to_thread(llm_text_gen, prompt)
            return result.strip() if result else ""
            
        except Exception as e:
            logger.error(f"Initial draft generation failed: {str(e)}")
            return ""
    
    async def _continue_story(
        self,
        persona: str,
        premise: str,
        outline: str,
        current_draft: str,
        progress_callback: Optional[callable] = None
    ) -> str:
        """Continue the story until completion."""
        try:
            guidelines = """
            Writing Guidelines:

            Delve deeper. Lose yourself in the world you're building. Unleash vivid
            descriptions to paint the scenes in your reader's mind.
            Develop your characters — let their motivations, fears, and complexities unfold naturally.
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
            """
            
            continuation_prompt = f"""
            {persona}

            You have a gripping premise in mind:

            {premise}

            Your imagination has crafted a rich narrative outline:

            {outline}

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
            """
            
            draft = current_draft
            iteration = 0
            max_iterations = 10  # Prevent infinite loops
            
            while 'IAMDONE' not in draft and iteration < max_iterations:
                iteration += 1
                
                # Update progress
                progress = 60 + (iteration / max_iterations) * 35  # 60% to 95%
                if progress_callback:
                    await progress_callback(
                        f"Continuing story development (iteration {iteration})...",
                        progress
                    )
                
                logger.info(f"Story continuation iteration {iteration}", draft_length=len(draft))
                
                try:
                    continuation = await asyncio.to_thread(
                        llm_text_gen,
                        continuation_prompt.format(story_text=draft)
                    )
                    
                    if continuation:
                        draft += '\n\n' + continuation
                    else:
                        logger.warning(f"Empty continuation at iteration {iteration}")
                        break
                        
                except Exception as e:
                    logger.error(f"Continuation failed at iteration {iteration}: {str(e)}")
                    break
            
            # Remove 'IAMDONE' marker and return final story
            final_story = draft.replace('IAMDONE', '').strip()
            
            logger.info(
                f"Story generation completed after {iteration} iterations",
                final_length=len(final_story)
            )
            
            return final_story
            
        except Exception as e:
            logger.error(f"Story continuation failed: {str(e)}")
            return current_draft  # Return what we have so far


# Global service instance
_story_writer_service = None


def get_story_writer_service() -> StoryWriterService:
    """Get or create the story writer service instance."""
    global _story_writer_service
    if _story_writer_service is None:
        _story_writer_service = StoryWriterService()
    return _story_writer_service