"""
LinkedIn Article Generation Prompts

This module contains prompt templates and builders for generating LinkedIn articles.
"""

from typing import Any


class ArticlePromptBuilder:
    """Builder class for LinkedIn article generation prompts."""
    
    @staticmethod
    def build_article_prompt(request: Any) -> str:
        """
        Build prompt for article generation.
        
        Args:
            request: LinkedInArticleRequest object containing generation parameters
            
        Returns:
            Formatted prompt string for article generation
        """
        prompt = f"""
        You are a senior content strategist and industry expert specializing in {request.industry}. Create a comprehensive, thought-provoking LinkedIn article that establishes authority, drives engagement, and provides genuine value to professionals in this field.

        TOPIC: {request.topic}
        INDUSTRY: {request.industry}
        TONE: {request.tone}
        TARGET AUDIENCE: {request.target_audience or 'Industry professionals, executives, and thought leaders'}
        WORD COUNT: {request.word_count} words

        CONTENT STRUCTURE:
        - Compelling headline that promises specific value
        - Engaging introduction with a hook and clear value proposition
        - 3-5 main sections with actionable insights and examples
        - Data-driven insights with proper citations
        - Practical takeaways and next steps
        - Strong conclusion with a call-to-action

        CONTENT QUALITY REQUIREMENTS:
        - Include current industry statistics and trends (2024-2025)
        - Provide real-world examples and case studies
        - Address common challenges and pain points
        - Offer actionable strategies and frameworks
        - Use industry-specific terminology appropriately
        - Include expert quotes or insights when relevant

        SEO & ENGAGEMENT OPTIMIZATION:
        - Use relevant keywords naturally throughout the content
        - Include engaging subheadings for scannability
        - Add bullet points and numbered lists for key insights
        - Include relevant hashtags for discoverability
        - End with thought-provoking questions to encourage comments

        VISUAL ELEMENTS:
        - Suggest 2-3 relevant images or graphics
        - Recommend data visualization opportunities
        - Include pull quotes for key insights

        KEY SECTIONS TO COVER: {', '.join(request.key_sections) if request.key_sections else 'Industry overview, current challenges, emerging trends, practical solutions, future outlook'}

        REMEMBER: This article should position the author as a thought leader while providing actionable insights that readers can immediately apply in their professional lives.
        """
        return prompt.strip()
