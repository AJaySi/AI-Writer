def generate_topic_content(blog_keywords, sub_topic):
    """
    For each of given topic generate content for it.
    """
    # The outline should contain various subheadings and include the starting sentence for each section.
    # TBD: Depending on the usecase 'Voice and style' will change to professional etc.
    prompt = f"""As a professional blogger and topic authority on {blog_keywords},
            craft factual (no more than 200 characters) subtopic content on {sub_topic}.
            Your response should reflect Experience, Expertise, Authoritativeness and Trustworthiness from content.
            Voice and style guide: Write in a professional manner, giving enlightening details and reasons.
            Use natural language and phrases that a real person would use: in normal conversations.
            Format your response using markdown. REMEMBER Not to include introduction or conclusion in your response.
            Use headings(h3 to h6 only), subheadings, bullet points, and bold to organize the information."""
    logger.info(f"Generate topic content using prompt:\n{prompt}\n")
    try:
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in generating topic content: {err}")
