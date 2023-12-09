def blog_proof_editor(blog_content, blog_keywords):
    """
        Helper for blog proof reading.
    """
    prompt = """I am looking for detailed editing and enhancement of the given blog post, 
        with a particular focus on maintaining originality. 
        The topic of the content is [{blog_keywords}]. Please go through the blog and make direct edits to improve it, 
        ensuring the final output is both high-quality and original. 
        Note: There are duplicates headings and corresponding paragraphs, rewrite into one subheading.

        Here are the specific areas to focus on:

        1). Ensure Originality: Edit any sections that lack originality, replacing them with unique and creative content.
        2). Eliminate Repetitive Language: Rewrite repetitive phrases with varied and engaging language.
        3). Vocabulary and Grammar Enhancement: Directly correct any grammatical errors and upgrade the 
        vocabulary for better readability.
        4). Improve Sentence Structure: Enhance sentence construction for better clarity and flow.
        5). Tone and Brand Alignment: Adjust the tone, voice, personality of given content to make it unique.
        6). Optimize Content Structure: Reorganize the content for a more impactful presentation, 
        including better paragraphing and transitions.
        7). Remove Redundancies: Important, Cut out any redundant information or overly complex jargon.
        8). Refine Overall Structure: Make structural changes to improve the overall impact of the content.
        9). Remember, rewrite all content that repeated, while maintaining the formatting of the given blog text.

        Please apply these changes directly to the following blog text and provide the edited version: 
        [blog_content]. """

    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error Blog Proof Reading: {err}")
