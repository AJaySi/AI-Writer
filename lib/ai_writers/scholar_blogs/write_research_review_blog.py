import sys

from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gemini_pro_text import gemini_text_response
from .gpt_providers.mistral_chat_completion import mistral_text_response

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


def review_research_paper(research_blog):
    """ """
    prompt = f"""As world's top researcher and academician, I will provide you with research paper.
    Your task is to write a highly detailed review report. 
    Important, your report should be factual, original and demostrate your expertise.

    Review guidelines:
    1). Read the Abstract and Introduction Carefully:
        Begin by thoroughly reading the abstract and introduction of the paper.
        Try to understand the research question, the objectives, and the background information.
        Identify the central argument or hypothesis that the study is examining.

    2). Examine the Methodology and Methods:
        Read closely at the research design, whether it is experimental, observational, qualitative, or a combination of methods.
        Check the sampling strategy and the size of the sample.
        Review the methods of data collection and the instruments used for this purpose.
        Think about any ethical issues and possible biases in the study.

    3). Analyze the Results and Discussion:
        Review how the results are presented, including any tables, graphs, and statistical analysis.
        Evaluate the findings' validity and reliability.
        Analyze whether the results support or contradict the research question and hypothesis.
        Read the discussion section where the authors interpret their findings and their significance.

    4). Consider the Limitations and Strengths:
        Spot any limitations or potential weaknesses in the study.
        Evaluate the strengths and contributions that the research makes.
        Think about how generalizable the findings are to other populations or situations.

    5). Assess the Writing and Organization:
        Judge the clarity and structure of the report.
        Consider the use of language, grammar, and the overall formatting.
        Assess how well the arguments are logically organized and how coherent the report is.

    6). Evaluate the Literature Review:
        Examine how comprehensive and relevant the literature review is.
        Consider how the study adds to or builds upon existing research.
        Evaluate the timeliness and quality of the sources cited in the research.

    7). Review the Conclusion and Implications:
        Look at the conclusions drawn from the study and how well they align with the findings.
        Think about the practical implications and potential applications of the research.
        Evaluate the suggestions for further research or policy actions.

    8). Overall Assessment:
        Formulate an overall opinion about the research report's quality and thoroughness.
        Consider the significance and impact of the findings.
        Evaluate how the study contributes to its field of research.

    9). Provide Constructive Feedback:
        Offer constructive criticism and suggestions for improvement, where necessary.
        Think about possible biases or alternative ways to interpret the findings.
        Suggest ideas for future research or for replicating the study.

    Do not provide description, explanations for your response.
    Using the above review guidelines, write a detailed review report on the below research paper.
    Research Paper: '{research_blog}'
    """

    if 'gemini' in gpt_providers:
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            logger.error(f"Failed to get response from gemini: {err}")
            response = mistral_text_response(prompt)
            return response

    elif 'openai' in gpt_providers:
        try:
            logger.info("Calling OpenAI LLM.")
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Failed to get response from Openai: {err}")
