import os
import time
import sys

from pytube import YouTube
import tempfile
import openai
from html2image import Html2Image
from tqdm import tqdm, trange
import google.generativeai as genai

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


from ...gpt_providers.audio_to_text_generation.stt_audio_blog import speech_to_text
from ...gpt_providers.text_generation.main_text_generation import llm_text_gen


def youtube_to_blog(video_url):
    """Function to transcribe a given youtube url """
    # fixme: Doesnt work all types of yt urls.
    vid_id = video_url.split("=")[1]

    try:
        # Starting the speech-to-text process
        logger.info("Starting with Speech to Text.")
        audio_text, audio_title = speech_to_text(video_url)
    except Exception as e:
        logger.error(f"Error in speech_to_text: {e}")
        sys.exit(1)  # Exit the program due to error in speech_to_text

    try:
        # Summarizing the content of the YouTube video
        audio_blog_content = summarize_youtube_video(audio_text, "gemini")
        logger.info("Successfully converted given URL to blog article.")
        return audio_blog_content, audio_title
    except Exception as e:
        logger.error(f"Error in summarize_youtube_video: {e}")
        sys.exit(1)  # Exit the program due to error in summarize_youtube_video


def summarize_youtube_video(user_content, gpt_providers):
    """Generates a summary of a YouTube video using OpenAI GPT-3 and displays a progress bar. 
    Args:
      video_link: The URL of the YouTube video to summarize.
    Returns:
      A string containing the summary of the video.
    """

    logger.info("Start summarize_youtube_video..")
    prompt = f"""
        You are an expert copywriter specializing in digital content writing. I will provide you with a transcript. 
        Your task is to transform a given transcript into a well-structured and informative blog article. 
        Please follow the below objectives:

        1. Master the Transcript: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and coherence. Dont quote anyone from video.
        3. Note: Check if the transcript is about programming, then include code examples and snippets in your article.
        4. Write Unique Content: Avoid direct copying; rewrite in your own words. 
        5. REMEMBER to avoid direct quoting and maintain uniqueness.
        6. Proofread: Check for grammar, spelling, and punctuation errors.
        7. Use Creative and Human-like Style: Incorporate contractions, idioms, transitional phrases, interjections, and colloquialisms.        8. Avoid repetitive phrases and unnatural sentence structures.
        9. Ensure Uniqueness: Guarantee the article is plagiarism-free.
        10. Punctuation: Use appropriate question marks at the end of questions.
        11. Pass AI Detection Tools: Create content that easily passes AI plagiarism detection tools.
        12. Rephrase words like 'video, youtube, channel' with 'article, blog' and such suitable words.

        Follow the above guidelines to create a well-optimized, unique, and informative article,
        that will rank well in search engine results and engage readers effectively.
        Follow above guidelines to craft a blog content from the following transcript:\n{user_content}
        """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to summarize_youtube_video: {err}")
        exit(1)
