import sys

from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gemini_pro_text import gemini_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def write_blog_from_paper(paper_content):
    """ Write blog from given paper url. """
    prompt = f"""As an expert in NLP and AI, I will provide you with a content of a research paper. 
    Your task is to write a highly detailed blog(at least 2000 words), breaking down complex concepts for beginners.
    Take your time and do not rush to respond.
    Do not provide explanations, suggestions in your response.

    Include the below section in your blog:
    Highlights: Include a list of 5 most important and unique claims of the given research paper.
    Abstract: Start by reading the abstract, which provides a concise summary of the research, including its purpose, methodology, and key findings.
    Introduction: This section will give you background information and set the context for the research. It often ends with a statement of the research question or hypothesis.
    Methodology: Include description of how authors conducted the research. This can include data sources, experimental setup, analytical techniques, etc.
    Results: This section presents the data or findings of the research. Pay attention to figures, tables, and any statistical analysis provided.
    Discussion/Analysis: In this section, Explain how research paper answers the research questions or how they fit with existing knowledge.
    Conclusion: This part summarizes the main findings and their implications. It might also suggest areas for further research.
    References: The cited works can provide additional context or background reading.
    Remember, Please use MLA format and markdown syntax.
    Do not provide description, explanations for your response.
    Take your time in crafting your blog content, do not rush to give the response.
    Using the blog structure above, please write a detailed and original blog on given research paper: \n'{paper_content}'\n\n"""

    if 'gemini' in gpt_providers:
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error(f"Failed to get response from gemini: {err}")
            raise err
    elif 'openai' in gpt_providers:
        try:
            logger.info("Calling OpenAI LLM.")
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            logger.error(f"failed to get response from Openai: {err}")
            raise err
