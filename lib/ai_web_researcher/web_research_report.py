from langchain.adapters.openai import convert_openai_messages
from langchain.chat_models import ChatOpenAI

from ..gpt_providers.gemini_pro_text import gemini_text_response


def write_web_research_report(web_research, faq_questions, gpt_provider="gemini"):
    """ """
    if "gemini" in gpt_provider:
            prompt = ["You are an SEO and marketing expert, who writes unique, factual and comprehensive research reports."
                    "I will provide you web research report as json data and a list of related FAQ questions."
                    "Use given json as context for writing your research report."
                    "Your sole purpose is to write well written, critically acclaimed, objective and structured research report"
                    "Use the urls from json content to provide cititations and include it in referances section of your report."
                    "Include appropriate emojis in your research report."
                    "Format your report in MLA format and markdown style, with special focus on readibility."
                    f"Do not provide explanations for your response.\nWeb research Report: \"\"\" {web_research} \"\"\"\n "
                    f"\nList of FAQ questions: \"\"\" {faq_questions} \"\"\"\n"]
            report = gemini_text_response(prompt)
        
    elif "openai" in gpt_provider:
        report = openai_research_report(prompt)
    return report
