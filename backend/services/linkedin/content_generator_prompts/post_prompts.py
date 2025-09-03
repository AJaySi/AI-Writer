"""
LinkedIn Post Generation Prompts

This module contains prompt templates and builders for generating LinkedIn posts.
"""

from typing import Any


class PostPromptBuilder:
    """Builder class for LinkedIn post generation prompts."""
    
    @staticmethod
    def build_post_prompt(request: Any) -> str:
        """
        Build prompt for post generation.
        
        Args:
            request: LinkedInPostRequest object containing generation parameters
            
        Returns:
            Formatted prompt string for post generation
        """
        prompt = f"""
        You are an expert LinkedIn content strategist with 10+ years of experience in the {request.industry} industry. Create a highly engaging, professional LinkedIn post that drives meaningful engagement and establishes thought leadership.

        TOPIC: {request.topic}
        INDUSTRY: {request.industry}
        TONE: {request.tone}
        TARGET AUDIENCE: {request.target_audience or 'Industry professionals, decision-makers, and thought leaders'}
        MAX LENGTH: {request.max_length} characters

        CONTENT REQUIREMENTS:
        - Start with a compelling hook that addresses a pain point or opportunity
        - Include 2-3 specific, actionable insights or data points
        - Use storytelling elements to make it relatable and memorable
        - Include industry-specific examples or case studies when relevant
        - End with a thought-provoking question or clear call-to-action
        - Use professional yet conversational language that encourages discussion

        ENGAGEMENT STRATEGY:
        - Include 3-5 highly relevant, trending hashtags (mix of broad and niche)
        - Use line breaks and emojis strategically for readability
        - Encourage comments by asking for opinions or experiences
        - Make it shareable by providing genuine value

        KEY POINTS TO COVER: {', '.join(request.key_points) if request.key_points else 'Current industry trends, challenges, and opportunities'}

        FORMATTING:
        - Use bullet points or numbered lists for key insights
        - Include relevant emojis to enhance visual appeal
        - Break text into digestible paragraphs (2-3 lines max)
        - Leave space for engagement (don't fill the entire character limit)

        REMEMBER: This post should position the author as a knowledgeable industry expert while being genuinely helpful to the audience.
        """
        return prompt.strip()
