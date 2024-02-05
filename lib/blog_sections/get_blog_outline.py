def generate_topic_outline(blog_title, num_subtopics):
    """
    Given a blog title generate an outline for it
    """
    # TBD: Remove hardcoding, make dynamic
    prompt = f"""As a SEO expert, suggest only {num_subtopics} beginner-friendly and 
        insightful sub topics for the blog title: {blog_title}.
        Respond with only answer and no description, explanations."""

    # The suggested {num_subtopics} outline should include few long-tailed keywords and most popular questions.
    # TBD: Include --niche
    logger.info(f"Prompt used for blog title Outline :\n{prompt}\n")
    # TBD: Add logic for which_provider and which_model
    try:
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating Blog Title: {err}")
    return response
