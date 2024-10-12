import os
import sys

import google.generativeai as genai
from dotenv import load_dotenv

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def load_environment():
    """Loads environment variables from a .env file."""
    load_dotenv()
    logger.info("Environment variables loaded successfully.")


def configure_google_api():
    """Configures the Google Gemini API for audio transcription.

    Raises:
        ValueError: If the GEMINI_API_KEY environment variable is not set.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        error_message = "Google API key not found. Please set the GEMINI_API_KEY environment variable."
        logger.error(error_message)
        raise ValueError(error_message)
    
    genai.configure(api_key=api_key)
    logger.info("Google Gemini API configured successfully.")


def transcribe_audio(audio_file_path):
    """
    Transcribes audio using Google's Gemini Pro model.

    Args:
        audio_file_path (str): The path to the audio file to be transcribed.

    Returns:
        str: The transcribed text from the audio. 
             Returns None if transcription fails.

    Raises:
        FileNotFoundError: If the audio file is not found.
    """
    try:
        # Load environment variables and configure the Google API
        load_environment()
        configure_google_api()

        logger.info(f"Attempting to transcribe audio file: {audio_file_path}")

        # Check if file exists
        if not os.path.exists(audio_file_path):
            error_message = f"FileNotFoundError: The audio file at {audio_file_path} does not exist."
            logger.error(error_message)
            raise FileNotFoundError(error_message)

        # Initialize a Gemini model appropriate for your use case.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Upload the audio file
        try:
            audio_file = genai.upload_file(audio_file_path)
            logger.info(f"Audio file uploaded successfully: {audio_file=}")
        except FileNotFoundError:
            error_message = f"FileNotFoundError: The audio file at {audio_file_path} does not exist."
            logger.error(error_message)
            raise FileNotFoundError(error_message) 
        except Exception as e:
            logger.error(f"Error uploading audio file: {e}")
            return None

        # Generate the transcription
        try:
            response = model.generate_content([
                "Transcribe the following audio:",
                audio_file
            ])

            # Check for valid response and extract text
            if response and hasattr(response, 'text'):
                transcript = response.text
                logger.info(f"Transcription successful:\n{transcript}")
                return transcript
            else:
                logger.warning("Transcription failed: Invalid or empty response from API.")
                return None

        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return None

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None
