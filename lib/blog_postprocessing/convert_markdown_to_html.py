from .gpt_providers.openai_chat_completion import openai_chatgpt

def convert_markdown_to_html(md_content):
    """ Helper function to convert given text to HTML
    """
    prompt =f"""
			You are a skilled web developer tasked with converting a Markdown-formatted text to HTML. 
            You will be given text in markdown format. Follow these steps to perform the conversion:
			
			1. Parse User's Markdown Input: You will receive a Markdown-formatted text as input from the user. 
            Carefully analyze the provided Markdown text, paying attention to different elements such as headings (#), 
            lists (unordered and ordered), bold and italic text, links, images, and code blocks.
			2. Generate and Validate HTML: Generate corresponding HTML code for each Markdown element following 
            the conversion guidelines below. Ensure the generated HTML is well-structured and syntactically correct.
			3. Preserve Line Breaks: Markdown line breaks (soft breaks) represented by two spaces at the end of a 
            line should be converted to <br> tags in HTML to preserve the line breaks.
			4. REMEMBER to generate complete, valid HTML response only.
			
			Follow below Conversion Guidelines:
			- Headers: Convert Markdown headers (#, ##, ###, etc.) to corresponding HTML header tags (<h1>, <h2>, <h3>, etc.).
			- Lists: Convert unordered lists (*) and ordered lists (1., 2., 3., etc.) to <ul> and <ol> HTML tags, respectively. 
            List items should be enclosed in <li> tags.
			- Emphasis: Convert bold (**) and italic (*) text to <strong> and <em> HTML tags, respectively.
			- Links: Convert Markdown links ([text](url)) to HTML anchor (<a>) tags. Ensure the href attribute contains the correct URL.
			- Images: Convert Markdown image tags (![alt text](image_url)) to HTML image (<img>) tags. 
            Include the alt attribute for accessibility.
			- Code: Convert inline code (`code`) to <code> HTML tags. Convert code blocks (```) to <pre> HTML tags 
            for preserving formatting.
			- Blockquotes: Convert blockquotes (>) to <blockquote> HTML tags.
			Convert the following Markdown text to HTML:  {md_content}
            """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in convert to HTML")
