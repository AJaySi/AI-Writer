from .gpt_providers.openai_chat_completion import openai_chatgpt
import google.generativeai as genai


def generate_blog_description(blog_content, gpt_providers):
    """
        Prompt designed to give SEO optimized blog descripton
    """
    prompt = f"""As an expert SEO and blog writer, Compose a compelling meta description for the given blog content, 
        adhering to SEO best practices. Keep it between 150-160 characters. 
        Provide a glimpse of the content's value to entice readers.
        Respond with only one of your best effort and do not include your explanations. 
        Blog Content: {blog_content}"""
    if 'gemini' in gpt_providers:
        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        except Exception as err:
            logger.error("Failed in getting GEMINI_API_KEY")
        # Use gemini-pro model for text and image.
        model = genai.GenerativeModel('gemini-pro')
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as err:
            logger.error("Failed to get response from gemini.")
    elif 'openai' in gpt_providers:
        try:
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Error in generating blog summary: {err}")
