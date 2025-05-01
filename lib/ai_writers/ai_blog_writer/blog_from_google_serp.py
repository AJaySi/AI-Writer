import os
import sys
import json
from pathlib import Path

from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from ...gpt_providers.text_generation.main_text_generation import llm_text_gen


def write_blog_google_serp(keywords, search_results, blog_params=None):
    """
    Write a blog post using search results from Google SERP.
    
    Args:
        keywords (str): The keywords or topic for the blog
        search_results (dict): Results from Google SERP search
        blog_params (dict, optional): Blog content characteristics:
            - blog_length: Target word count
            - blog_tone: Content tone
            - blog_demographic: Target audience
            - blog_type: Type of blog post
            - blog_language: Language for the blog
    
    Returns:
        str: The generated blog content in markdown format
    """
    # If no blog parameters are provided, use defaults
    if blog_params is None:
        blog_params = {
            "blog_length": 2000,
            "blog_tone": "Professional",
            "blog_demographic": "Professional",
            "blog_type": "Informational",
            "blog_language": "English"
        }
    
    # Ensure all parameters have default values
    blog_length = blog_params.get("blog_length", 2000)
    blog_tone = blog_params.get("blog_tone", "Professional")
    blog_demographic = blog_params.get("blog_demographic", "Professional")
    blog_type = blog_params.get("blog_type", "Informational")
    blog_language = blog_params.get("blog_language", "English")
    
    logger.info(f"Generating {blog_tone} {blog_type} blog of {blog_length} words for {blog_demographic} audience in {blog_language}")
    
    try:
        # Build a prompt based on search results
        prompt_parts = [
            f"You are a specialized blog writer who writes in a {blog_tone} tone for a {blog_demographic} audience. "
            f"Create a {blog_type} blog post that is approximately {blog_length} words in {blog_language}.",
            f"The blog should be about: {keywords}",
            "Use the following search results to create an informative, accurate, and well-structured blog post:"
        ]
        
        # Add organic search results
        if 'organic' in search_results:
            prompt_parts.append("\nSearch results:")
            for i, result in enumerate(search_results['organic'][:5], 1):
                title = result.get('title', 'No title')
                snippet = result.get('snippet', 'No snippet')
                prompt_parts.append(f"{i}. {title}: {snippet}")
        
        # Add people also ask questions if available
        if 'peopleAlsoAsk' in search_results and search_results['peopleAlsoAsk']:
            prompt_parts.append("\nPeople also ask:")
            for i, question in enumerate(search_results['peopleAlsoAsk'][:3], 1):
                q_text = question.get('question', 'No question')
                q_answer = question.get('answer', {}).get('snippet', 'No answer')
                prompt_parts.append(f"{i}. Q: {q_text}\n   A: {q_answer}")
        
        # Add related searches if available
        if 'relatedSearches' in search_results and search_results['relatedSearches']:
            related = [item.get('query', '') for item in search_results['relatedSearches'][:5]]
            if related:
                prompt_parts.append("\nRelated topics to consider including:")
                prompt_parts.append(", ".join(related))
        
        # Add specific instructions based on blog_type
        type_instructions = {
            "Informational": "Focus on providing factual information and educating the reader about the topic.",
            "How-to": "Include clear step-by-step instructions with actionable advice.",
            "List": "Organize content into a numbered or bulleted list of points, tips, or examples.",
            "Review": "Provide balanced analysis with pros and cons, and a clear conclusion or recommendation.",
            "Tutorial": "Include detailed instructions with examples and explanations for each step.",
            "Opinion": "Present a clear perspective supported by evidence, while acknowledging other viewpoints."
        }
        
        prompt_parts.append(f"\nSpecific instructions: {type_instructions.get(blog_type, '')}")
        
        # Add formatting instructions
        prompt_parts.append("""
Format the blog post in markdown with:
- A compelling title (# Title)
- An introduction that hooks the reader
- Well-structured sections with appropriate headings (## Headings)
- Bullet points or numbered lists where appropriate
- A conclusion summarizing key points
- Make sure all content is accurate, informative, and adds value to the reader.
- Include 2-3 subheadings to organize the content well.
- Be concise and to the point.
- Write in an engaging, reader-friendly style.
- Avoid using phrases like "According to the search results" or "Based on the information provided."
- Present information as direct knowledge.
""")
        
        # Combine all prompt parts
        full_prompt = "\n".join(prompt_parts)
        
        # Generate the blog content using the prompt
        response = llm_text_gen(full_prompt)
        
        # Return the generated content
        return response
    
    except Exception as err:
        logger.error(f"Error generating blog from search results: {err}")
        raise


def improve_blog_intro(blog_content, blog_intro):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        You are a skilled content editor, tasked with creating an engaging peek into the blog post provided. 
        This peek should entice readers to delve into the full content. 

        Here's what you need to do:
        1. **Replace the old blog introduction with the new one provided.**
        2. **Craft a short and captivating summary of the key points and interesting takeaways from the blog.** 
            - Highlight what makes the blog unique and worth reading.
            - This peek should be placed directly before the new introduction.
        3. **Include the complete blog content, with the new introduction and the added peek.**

        Do not provide explanations for your actions, simply present the edited blog content.

        Blog Content: \"\"\"{blog_content}\"\"\"
        Blog Introduction: \"\"\"{blog_intro}\"\"\"
        """
    logger.info("Generating blog introduction from tavily answer.")
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def blog_with_keywords(blog, keywords):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        You are Sarah, the Creative Content writer, writing up fresh ideas and crafts them with care. 
        She makes complex topics easy to understand and writes in a friendly tone that connects with everyone.
        She excels at simplifying complex topics and communicates with charisma, making technical jargon come alive for her audience.

        As an expert digital content writer, specializing in content optimization and SEO. 
        I will provide you with my 'blog content' and 'list of keywords' on the same topic.
        Your task is to write an original blog, utilizing given keywords and blog content.
        Your blog should be highly detailed and well formatted. 

        Blog content: '{blog}'
        list of keywords: '{keywords}'
        """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_keywords: Failed to get response from LLM: {err}")
        raise err


def blog_with_research(report, blog):
    """Combine the given online research and gpt blog content"""
    prompt = f"""
        As expert Creative Content writer, Your task is to update a blog post using the latest research.
        
        Here's what you need to do:

        1. **Read the outdated blog content and the new research report carefully.**  
        2. **Identify key insights and updates from the research report that should be incorporated into the blog post.**
        3. **Rewrite sections of the blog post to reflect the new information, ensuring a smooth and natural flow.** 
        4. **Maintain the blog's original friendly and conversational tone throughout.**

        Remember, your goal is to seamlessly blend the new information into the existing blog post, making it accurate and engaging for readers. 
        \n\n
        Research Report: \"\"\"{report}\"\"\"

        Blog Content: \"\"\"{blog}\"\"\"
    """
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"blog_with_research: Failed to get response from LLM: {err}")
        raise err
