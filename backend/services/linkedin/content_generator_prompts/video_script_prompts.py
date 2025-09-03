"""
LinkedIn Video Script Generation Prompts

This module contains prompt templates and builders for generating LinkedIn video scripts.
"""

from typing import Any


class VideoScriptPromptBuilder:
    """Builder class for LinkedIn video script generation prompts."""
    
    @staticmethod
    def build_video_script_prompt(request: Any) -> str:
        """
        Build prompt for video script generation.
        
        Args:
            request: LinkedInVideoScriptRequest object containing generation parameters
            
        Returns:
            Formatted prompt string for video script generation
        """
        prompt = f"""
        You are a video content strategist and {request.industry} industry expert. Create a compelling LinkedIn video script that captures attention in the first 3 seconds and maintains engagement throughout the entire duration.

        TOPIC: {request.topic}
        INDUSTRY: {request.industry}
        TONE: {request.tone}
        TARGET AUDIENCE: {request.target_audience or 'Industry professionals and decision-makers'}
        DURATION: {request.video_duration} seconds
        INCLUDE CAPTIONS: {request.include_captions}
        INCLUDE THUMBNAIL SUGGESTIONS: {request.include_thumbnail_suggestions}

        VIDEO STRUCTURE & TIMING:
        - Hook (0-3 seconds): Compelling opening that stops the scroll
        - Introduction (3-8 seconds): Establish credibility and preview value
        - Main Content (8-{request.video_duration-5} seconds): 2-3 key insights with examples
        - Conclusion (Last 5 seconds): Clear call-to-action and engagement prompt

        CONTENT REQUIREMENTS:
        - Start with a surprising statistic, question, or bold statement
        - Include specific examples and case studies from the industry
        - Use conversational, engaging language that feels natural when spoken
        - Include 2-3 actionable takeaways viewers can implement immediately
        - End with a question that encourages comments and discussion

        VISUAL & AUDIO GUIDELINES:
        - Suggest background music style and mood
        - Recommend visual elements (text overlays, graphics, charts)
        - Include specific camera angle and movement suggestions
        - Suggest props or visual aids that enhance the message

        CAPTION OPTIMIZATION:
        - Write captions that are engaging even without audio
        - Include emojis and formatting for visual appeal
        - Ensure captions complement the spoken content
        - Make captions scannable and easy to read

        THUMBNAIL DESIGN:
        - Suggest compelling thumbnail text and imagery
        - Recommend color schemes that match the industry
        - Include specific design elements that increase click-through rates

        ENGAGEMENT STRATEGY:
        - Include moments that encourage viewers to pause and think
        - Suggest interactive elements (polls, questions, challenges)
        - Create emotional connection through storytelling
        - End with clear next steps and hashtag suggestions

        KEY INSIGHTS TO COVER: {', '.join(request.key_points) if request.key_points else 'Industry trends, challenges, solutions, and opportunities'}

        REMEMBER: This video should provide immediate value while building the creator's authority. Every second should count toward engagement and viewer retention.
        """
        return prompt.strip()
