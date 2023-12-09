def generate_blog_description(blog_content):
    """
        Prompt designed to give SEO optimized blog descripton
    """
    prompt = f"""As an expert SEO and blog writer, Compose a compelling meta description for the given blog content, 
        adhering to SEO best practices. Keep it between 150-160 characters, incorporating active verbs, 
        avoiding all caps and excessive punctuation. Ensure relevance, engage users, and encourage clicks.
        Use keywords naturally and provide a glimpse of the content's value to entice readers.
        Respond with only one of your best effort and do not include your explanations. 
        Blog Content: {blog_content}"""

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in generating blog description: {err}")
