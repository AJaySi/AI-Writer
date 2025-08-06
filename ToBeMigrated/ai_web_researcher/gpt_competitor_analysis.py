import sys

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def summarize_competitor_content(research_content):
    """Combine the given online research and gpt blog content"""

    prompt = f"""You are a helpful assistant writing a research report about a company. I will provide you with company details. 
        Summarize the given company details into multiple paragraphs. 
        Be extremely concise, professional, and factual as possible. 
        The first paragraph should be an introduction and summary of the company. 
        The second paragraph should include pros and cons of the company.
        The third paragraph should be on their pricing model.
        Include a conclusion, summarizing your research about the given company details.
        Company details: '{research_content}'"""
    
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Failed to get response from LLM: {err}")
        raise err
