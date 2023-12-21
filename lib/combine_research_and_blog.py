from .gpt_providers.openai_chat_completion import openai_chatgpt


def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""

    prompt = f"""
        You are an expert copywriter specializing in content optimization for SEO.
        I will provide you with a 'research report' and a 'blog content' on the same topic.
        Your task is to transform and combine the given research and blog content into a well-structured, unique
        and engaging blog article.

        Your objectives include:
        1. Master the report and blog content: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and coherence.
        3. Identify Main Keywords: Determine the primary topic and combine the articles on the main topic.
        4. REMEMBER: From the research report, include links and cititations to make your article more authoratative.
        5. Write Code snippets: Check if given report is on programming, then write code snippets where applicable.
        6. Optimize for SEO: Generate high quality informative content.
        Implement SEO best practises with appropriate keyword density.
        7. Craft Engaging and Informative Article: Provide value and insight to readers.
        8. Proofread: Important to Check for grammar, spelling, and punctuation errors.
        9. Use Creative and Human-like Style: Incorporate contractions, idioms, transitional phrases,
        interjections, and colloquialisms. Avoid repetitive phrases and unnatural sentence structures.
        10. Blog Structuring: Include an Introduction, subtopics and use bullet points or
        numbered lists if appropriate. Important to include FAQs, Conclusion and Referances.
        11. Ensure Uniqueness: Guarantee the article is plagiarism-free. Write in unique, informative style.
        12. Punctuation: Use appropriate question marks at the end of questions.
        13. Pass AI Detection Tools: Create content that easily passes AI plagiarism detection tools.
        14. REMEMBER: Use the formatting style of given research report and include citations, referances in combined article.

                Follow these guidelines to combine and write a new, unique, and informative blog article
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
        SystemError(f"Error in combining blog and research report.")
