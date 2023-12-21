from .gpt_providers.openai_chat_completion import openai_chatgpt


def convert_tomarkdown_format(blog_content):
    """ Helper for converting content to markdown format for static sites. """
    prompt = f"""
    As an expert in markdown language format and font matter, used for static webpages.
    Your task is to convert and improve formatting of given blog content.
    Do Not modify the content, only modify to convert it into highly readable blog content.

    Use below guidelines and include other best practises:
    1). Headers for Structure: Use # for main headings and increase the number of # for 
    subheadings (##, ###, etc.). Organize given content into clear, hierarchical sections.
    2). Emphasizing Text: Use single asterisks or underscores for italic (*italic* or _italic_), 
    double for bold (**bold** or __bold__), and triple for bold italic (***bold italic***).
    3). Lists: For unordered lists, use dashes, asterisks, or plus signs (-, *, +). 
    For ordered lists, use numbers followed by periods (1., 2., etc.).
    4). Blockquotes: Use > for blockquotes, and add additional > for nested blockquotes.
    5). Code Blocks: Use backticks for inline code (code) and triple backticks for code blocks. 
    Specify a language for syntax highlighting.
    6). Horizontal Lines: Create a horizontal line using three or more asterisks, dashes, or underscores (---, ***).
    7). Table Formatting: Use pipes | and dashes - to create tables. Align text with colons.
    8). Remember to use suitable emojis for the given blog content.

    Convert the given blog content in well organised markdown content: {blog_content}"""
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in converting to Markdown format.")
