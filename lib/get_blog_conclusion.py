def get_blog_conclusion(blog_content):
    """
    Accepts a blog content and concludes it.
    """
    prompt = f"""As an expert SEO and blog writer, please conclude the given blog providing vital take aways,
            summarise key points (no more than 300 characters) in bullet points. The blog content: {blog_content}
            """
    logger.info(f"Generating blog conclusion iwth prompt: {prompt}")
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating blog conclusion: {err}")
    else:
        return response
