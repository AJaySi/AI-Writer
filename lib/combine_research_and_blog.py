def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        You are an expert copywriter specializing in content optimization for SEO.
        I will provide you with a research report and a blog content on the same topic.
        Treat the research report as the context for the blog and better it accordingly.
        Your task is to transform and combine the given research and blog content into a well-structured, unique
        and engaging blog article. 
        Your objectives include:
        1. Master the report and blog content: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and coherence.
        3. Identify Main Keyword: Determine the primary topic and combine the articles on the main topic.
        4. Keyword Integration: Naturally integrate keywords in headings, subheadings, and body text, avoiding overuse.
        5. Write Unique Content: Avoid direct copying from given report and blog; rewrite in your own words and style.
        6. Optimize for SEO: Generate high quality informative content. 
        Implement SEO best practises with appropriate keyword density.
        7. Craft Engaging and Informative Article: Provide value and insight to readers.
        8. Proofread: Important to Check for grammar, spelling, and punctuation errors.
        9. Use Creative and Human-like Style: Incorporate contractions, idioms, transitional phrases, 
        interjections, and colloquialisms. Avoid repetitive phrases and unnatural sentence structures.
        10. Structuring: Include an Introduction, subtopics and use bullet points or 
        numbered lists if appropriate. Important to include FAQs, and Conclusion.
        11. Ensure Uniqueness: Guarantee the article is plagiarism-free. Write in unique, informative style.
        12. Punctuation: Use appropriate question marks at the end of questions.
        13. Pass AI Detection Tools: Create content that easily passes AI plagiarism detection tools.
        14. REMEMBER to give final response as complete HTML.
        Follow these guidelines to create a well-optimized, unique, and informative article 
        that will rank well in search engine results and engage readers effectively.

        Create a blog post from the given research report and blog content below.
        Research report: {report}
        Blog content: {blog}
        """
    try:
        # TBD: Add logic for which_provider and which_model
        response = openai_chatgpt(prompt)
        return response
    except Exception as err:
        SystemError(f"Error in combining research report and blog content.")
