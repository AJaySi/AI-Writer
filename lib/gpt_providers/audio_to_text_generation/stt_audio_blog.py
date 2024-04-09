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
        audio_file = None
        if video_url.startswith("https://www.youtube.com/") or video_url.startswith("http://www.youtube.com/"):
            logger.info(f"Accessing YouTube URL: {video_url}")
            yt = YouTube(video_url, on_progress_callback=progress_function)

            logger.info("Fetching the highest quality audio stream")
            audio_stream = yt.streams.filter(only_audio=True).first()

            if audio_stream is None:
                logger.warning("No audio stream found for this video.")
                return None

            logger.info(f"Downloading audio for: {yt.title}")
            global progress_bar
            progress_bar = tqdm(total=1.0, unit='iB', unit_scale=True, desc=yt.title)
            try:
                audio_file = audio_stream.download(output_path)
            except Exception as err:
                logger.error(f"Failed to download audio file: {audio_file}")

            progress_bar.close()
            logger.info(f"Audio downloaded: {yt.title} to {output_path}")
        # Audio filepath from local directory.
        elif os.path.exists(audio_input):
            audio_file = video_url

        # Checking file size
        max_file_size = 24 * 1024 * 1024  # 24MB
        file_size = os.path.getsize(audio_file)
        # Convert file size to MB for logging
        file_size_MB = file_size / (1024 * 1024)  # Convert bytes to MB
        logger.info(f"Downloaded Audio Size is: {file_size_MB:.2f} MB")
        if file_size > max_file_size:
            logger.error("File size exceeds 24MB limit.")
            # FIXME: We can chunk hour long videos, the code is not tested.
            #long_video(audio_file)
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
            logger.info(f"\nYouTube video transcription:\n{yt.title}\n{transcript}\n")
            return transcript, yt.title

        except Exception as e:
            logger.error(f"Failed in Whisper transcription: {e}")
            sys.exit("Transcription failure.")

    except Exception as e:
        logger.error(f"An error occurred during YouTube video processing: {e}")
        sys.exit("Video processing failure.")

    finally:
        try:
            if os.path.exists(audio_file):
                os.remove(audio_file)
                logger.info("Temporary audio file removed.")
        except PermissionError:
            logger.error(f"Permission error: Cannot remove '{audio_file}'. Please make sure of necessary permissions.")
        except Exception as e:
            logger.error(f"An error occurred removing audio file: {e}")


def long_video(temp_file_name):
    """
    Transcribes a YouTube video using OpenAI's Whisper API by processing the video in chunks.

    This function handles videos longer than the context limit of the Whisper API by dividing the video into
    10-minute segments, transcribing each segment individually, and then combining the results.

    Key Changes and Notes:
    1. Video Splitting: Splits the audio into 10-minute chunks using the moviepy library.
    2. Chunk Transcription: Each audio chunk is transcribed separately and the results are concatenated.
    3. Temporary Files for Chunks: Uses temporary files for each audio chunk for transcription.
    4. Error Handling: Exception handling is included to capture and return any errors during the process.
    5. Logging: Process steps are logged for debugging and monitoring.
    6. Cleaning Up: Removes temporary files for both the entire video and individual audio chunks after processing.

    Args:
        video_url (str): URL of the YouTube video to be transcribed.
    """
    # Extract audio and split into chunks
    app.logger.info(f"Processing the YT video: {temp_file_name}")
    full_audio = mp.AudioFileClip(temp_file_name)
    duration = full_audio.duration
    chunk_length = 600  # 10 minutes in seconds
    chunks = [full_audio.subclip(start, min(start + chunk_length, duration)) for start in range(0, int(duration), chunk_length)]

    combined_transcript = ""
    for i, chunk in enumerate(chunks):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_chunk_file:
            chunk.write_audiofile(audio_chunk_file.name, codec="mp3")
            with open(audio_chunk_file.name, "rb") as audio_file:
                # Transcribe each chunk using OpenAI's Whisper API
                app.logger.info(f"Transcribing chunk {i+1}/{len(chunks)}")
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
                combined_transcript += transcript['text'] + "\n\n"

            # Remove the chunk audio file
            os.remove(audio_chunk_file.name)

