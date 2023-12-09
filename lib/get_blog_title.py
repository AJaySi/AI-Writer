def generate_blog_title(blog_meta_desc):
    """
    Given a blog title generate an outline for it
    """
    # TBD: Remove hardcoding, make dynamic
    prompt = f"""As a SEO expert and content writer, I will provide you with meta description of blog. 
        Your task is write a SEO optimized, call to action and engaging blog title for it.
        Follows SEO best practises to suggest the blog title. 
        Please keep the titles concise, not exceeding 60 words, and ensure to maintain their meaning. 
        Respond with only one title and no description or keyword like Title: 
        Generate blog title for this given blog content: {blog_meta_desc}
        """
    # The suggested {num_subtopics} outline should include few long-tailed keywords and most popular questions.
    # TBD: Include --niche
    logger.info(f"Prompt used for blog title :{prompt}")
    try:
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating Blog Title: {err}")
    return response
