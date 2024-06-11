import os
import google.generativeai as genai
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from a .env file."""
    load_dotenv()

def configure_google_api():
    """Configure the Google API for audio summarization."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Please set the GEMINI_API_KEY environment variable.")
    genai.configure(api_key=api_key)

def transcribe_audio(audio_file_path):
    """Summarize the audio using Google's Generative API.
    
    Args:
        audio_file_path (str): The path to the audio file to be summarized.
    
    Returns:
        str: The summary text of the audio.
    
    Raises:
        ValueError: If the audio file path is invalid or the API response is not successful.
        Exception: For any other errors that occur during the process.
    """
    try:
        # Load environment variables and configure API
        load_environment()
        configure_google_api()

        # Create generative model instance
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        audio_file = None
        try:
            # Upload the audio file
            audio_file = genai.upload_file(path=audio_file_path)
        except Exception as err:
            print(err)
        # Generate the summary
        response = model.generate_content(
            [
                "Listen carefully to the given following audio file. Transcribe the following given audio.",
                audio_file
            ]
        )
        
        # Check if the response contains text
        if not hasattr(response, 'text'):
            raise ValueError("The API response does not contain text.")
        
        return response.text

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError:
        print(f"FileNotFoundError: The audio file at {audio_file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
