from pytube import YouTube
import os
import sys
from loguru import logger
from openai import OpenAI
from tqdm import tqdm

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


def progress_function(stream, chunk, bytes_remaining):
    # Calculate the percentage completion
    current = ((stream.filesize - bytes_remaining) / stream.filesize)
    progress_bar.update(current - progress_bar.n)  # Update the progress bar


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def speech_to_text(video_url, output_path='.'):
    """
    Transcribes speech to text from a YouTube video URL using OpenAI's Whisper model.

    Args:
        video_url (str): URL of the YouTube video to transcribe.
        output_path (str, optional): Directory where the audio file will be saved. Defaults to '.'.

    Returns:
        str: The transcribed text from the video.

    Raises:
        SystemExit: If a critical error occurs that prevents successful execution.
    """
    try:
        logger.info(f"Accessing YouTube URL: {video_url}")
        yt = YouTube(video_url, on_progress_callback=progress_function)

        logger.info("Fetching the highest quality audio stream")
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream is None:
            logger.warning("No audio stream found for this video.")
            return None

        #logger.info(f"Downloading audio for: {yt.title}")
        global progress_bar
        progress_bar = tqdm(total=1.0, unit='iB', unit_scale=True, desc=yt.title)
        audio_file = audio_stream.download(output_path)
        progress_bar.close()
        logger.info(f"Audio downloaded: {yt.title} to {output_path}")

        # Checking file size
        max_file_size = 24 * 1024 * 1024  # 24MB
        file_size = os.path.getsize(audio_file)
        # Convert file size to MB for logging
        file_size_MB = file_size / (1024 * 1024)  # Convert bytes to MB
        logger.info(f"Downloaded Audio Size is: {file_size_MB:.2f} MB")
        if file_size > max_file_size:
            logger.error("File size exceeds 24MB limit.")
            sys.exit("File size limit exceeded.")

        try:
            logger.info("Initializing OpenAI client for transcription.")
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

            logger.info("Transcribing using OpenAI's Whisper model.")
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=open(audio_file, "rb"),
                response_format="text"
            )
            logger.info("\nYouTube video transcription:\n\n{transcript}\n")
            return transcript, yt.title

        except Exception as e:
            logger.error(f"Failed in Whisper transcription: {e}")
            sys.exit("Transcription failure.")

    except Exception as e:
        logger.error(f"An error occurred during YouTube video processing: {e}")
        sys.exit("Video processing failure.")

    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)
            logger.info("Temporary audio file removed.")
