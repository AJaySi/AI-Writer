from .gpt_providers.openai_chat_completion import openai_chatgpt
import google.generativeai as genai


def get_blog_tags(blog_article, gpt_providers):
    """
        Function to suggest tags for the given blog content
    """
    # Suggest at least 5 tags for the following blog post [Enter your blog post text here].
    prompt = f"""As an expert SEO and blog writer, suggest only 2 relevant and specific blog tags
         for the given blog content. Only reply with comma separated values. 
         Blog content:  {blog_article}."""

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
