def get_blog_intro(blog_title, blog_topics):
    """
    Generate blog introduction as per title and sub topics
    """
    prompt = f"""As a skilled wordsmith, I'll equip you with a blog title and relevant topics, tasking you with crafting an engaging introduction. Your challenge: Create a brief, compelling entry that entices readers to explore the entire post. This introduction must be concise (under 250 characters) yet powerful, clearly stating the blog's purpose and what readers stand to gain. Reply with only the introduction.

Intrigue your audience from the start with vibrant language, employing strong verbs and vivid descriptions. Address a common challenge your readers face, demonstrating empathy and positioning yourself as their go-to expert. Pose thought-provoking questions that prompt reader engagement and contemplation.

Remember, your words matter. This introduction serves as the cornerstone of the blog post. It should not only captivate attention but also encourage deeper exploration. Additionally, strategically integrate relevant keywords to enhance visibility on search engine results pages (SERPs). Your mission: Craft a blog introduction that resonates, leaving readers eager to delve further into the titled piece: '{blog_title}', covering these sub-topics: {blog_topics}."""

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
    except Exception as err:
        SystemError(f"Error in generating Blog Introduction: {err}")
    return response
