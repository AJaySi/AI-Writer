def get_blog_tags(blog_article):
    """
        Function to suggest tags for the given blog content
    """
    # Suggest at least 5 tags for the following blog post [Enter your blog post text here].
    prompt = f"""As an expert SEO and blog writer, suggest only 2 relevant and specific blog tags
         for the given blog content. Only reply with comma separated values. 
         Blog content:  {blog_article}."""

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating blog tags: {err}")
    else:
        return response
