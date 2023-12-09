def get_blog_categories(blog_article):
    """
    Function to generate blog categories for given blog content.
    """
    prompt = f"""As an expert SEO and content writer, I will provide you with blog content.
            Suggest only 2 blog categories which are most relevant to provided blog content,
            by identifying the main topic. Also consider the target audience and the
            blog's category taxonomy. Only reply with comma separated values. The blog content is: {blog_article}"
            """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating blog categories: {err}")
    else:
        return response
