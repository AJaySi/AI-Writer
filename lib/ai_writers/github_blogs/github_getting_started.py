import sys

from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )



def github_readme_blog(readme_content):
    """ """
    prompt = f"""As an expert programmer and teacher, Write an original, detailed and step-by-step guide, from the provided Text below.
    Your guide should be original, engaging and help beginners get started easily.
    Write new  example codes and detailed comments on how to run them. Include appropriate emoji where applicable.
    Include a referances section that links to more code examples.
    Your response MUST be a how-to blog in markdown format. 
    Respond ONLY with your blog content. 

    Text: '{readme_content}' 
    """
    if 'gemini' in gpt_providers:
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error(f"Failed to get response from gemini: {err}")
            sys.exit(1)
    elif 'openai' in gpt_providers:
        try:
            logger.info("Calling OpenAI LLM.")
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Failed to get response from Openai: {err}")
