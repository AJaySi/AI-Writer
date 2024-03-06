from .gpt_providers.openai_chat_completion import openai_chatgpt
from .gpt_providers.gemini_pro_text import gemini_text_response


def convert_tomarkdown_format(blog_content, gpt_provider="openai"):
    """ Helper for converting content to markdown format for static sites. """
    
    prompt = f"""As an expert in markdown language format and font matter,
    I will provide you with a blog post.
    Your task is to only Improve the formatting and structure of a blog post to enhance readability, visual appeal, and overall user experience. Do not alter the content of the provided blog. Modify only for the formatting.
    Dont provide explanations, just your final response.

    Guidelines to do formatting:
    1. **Headings for Structure:**
   - Use # for the main title of the blog post.
   - Use ## for subheadings that divide the post into clear sections.
   - Use ###, ####, etc. for additional subheadings as needed.
   - Keep the headings concise and descriptive.

    2. **Emphasizing Text:**
   - Use * or _ for italicizing important words or phrases.
   - Use ** or __ for bolding key points.
   - Use *** or ___ for bold italicizing very important text.
   - Use sparingly to avoid overwhelming the reader.

    3. **Lists:**
   - Use - or * for unordered lists.
   - Use 1., 2., etc. for ordered lists.
   - Keep list items concise and to the point.
   - Use consistent formatting for all lists.

    4. **Blockquotes:**
   - Use > to indent and highlight quotes or important information.
   - Use additional > for nested blockquotes.
   - Attribute quotes to their original source if applicable.

    5. **Code Blocks:**
   - Use backticks ` for inline code.
   - Use triple backticks ``` for code blocks.
   - Specify the language of the code block for syntax highlighting, e.g., ```python```.
   - Use code blocks to display code snippets or technical information.

    6. **Horizontal Lines:**
   - Use three or more asterisks, dashes, or underscores to create a horizontal line, e.g., ***, ---, or ___
   - Use horizontal lines to separate different sections of the blog post.

    7. **Table Formatting:**
   - Use pipes | and dashes - to create tables.
   - Align text within columns using colons :.
   - Use tables to present data or information in a structured format.

    8. **Other Best Practices:**
   - Use emojis sparingly and appropriately to add visual interest and enhance the reader's experience.
   - Proofread carefully for any errors in grammar, spelling, or formatting.
   - Keep the blog post organized and easy to navigate.
   - Use a consistent formatting style throughout the post.
    
    Blog Post: '{blog_content}'"""
    
    if 'openai' in gpt_provider.lower():
        try:
            response = openai_chatgpt(prompt)
            return response
        except Exception as err:
            SystemError(f"Openai Error in converting to Markdown format.")
    elif 'gemini' in gpt_provider.lower():

        prompt = f""" Convert the given blog post into well structured MARKDOWN content. 
        Do not alter the given blog post.
        blog post: "{blog_content}" """
        try:
            response = gemini_text_response(prompt)
            return response
        except Exception as err:
            SystemError(f"Gemini Error in converting to Markdown format.")
