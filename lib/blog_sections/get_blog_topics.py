def generate_blog_topics(blog_keywords, num_blogs, niche):
    """
    For a given prompt, generate blog topics.
    Using the davinci-instruct-beta-v3 model. It’s proven to be an ideal 
    one for generating unique blog content.
    Ex: Generate SEO optimized blog topics on given keywords
    """
    prompt = f"""As an SEO specialist and blog writer, write {num_blogs} catchy
    and SEO-friendly blog topics on {blog_keywords}. The blog title must be less than 80 characters.
    The blog titles must follow best SEO practises, be engaging and invite/tempt users to read full blog.
    Do not include descriptions, explanations. Do not number the result."""

    # Beware of keywords stuffing, clustering, semantic should help avoid.
    if num_blogs > 5:
        # Get more keywords, based on user given keywords.
        more_keywords = get_related_keywords(num_blogs, blog_keywords, niche)
        prompt = prompt + """Use the following keywords wisely, without keyword stuffing: {more_keywords}"""

    logger.info(f"Prompt used for generating blog topics: \n{prompt}\n")
    try:
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in generating blog topics: {err}")


def get_related_keywords(num_blogs, keywords, niche):
    """
    Helper function to get more keywords from GPTs.
    """
    # Check if niche: use long tailed, else use popular keywords.
    if niche:
        prompt = (f"Generate a list without description of the top {num_blogs} most popular and semantically"
                f"related long-tailed keywords and entities for the topic of {keywords} that are used in"
                "high-quality content and relevant to my competitors."
                )
    else:
        prompt = (f"Generate a list without description of the top {num_blogs} most popular and"
                f" semantically related keywords and entities for the topic of {keywords} that are used"
                " in high-quality content and relevant to my competitors."
                )
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in getting related keywords.")
