"""Facebook Story generation service."""

from typing import Dict, Any, List
from ..models.story_models import FacebookStoryRequest, FacebookStoryResponse
from .base_service import FacebookWriterBaseService


class FacebookStoryService(FacebookWriterBaseService):
    """Service for generating Facebook stories."""
    
    def generate_story(self, request: FacebookStoryRequest) -> FacebookStoryResponse:
        """
        Generate a Facebook story based on the request parameters.
        
        Args:
            request: FacebookStoryRequest containing all the parameters
            
        Returns:
            FacebookStoryResponse with the generated content
        """
        try:
            # Determine the actual story type and tone
            actual_story_type = request.custom_story_type if request.story_type.value == "Custom" else request.story_type.value
            actual_tone = request.custom_tone if request.story_tone.value == "Custom" else request.story_tone.value
            
            # Build the prompt
            prompt = self._build_story_prompt(request, actual_story_type, actual_tone)
            
            # Generate the story content
            content = self._generate_text(prompt, temperature=0.7, max_tokens=1024)
            
            if not content:
                return FacebookStoryResponse(
                    success=False,
                    error="Failed to generate story content"
                )
            
            # Generate visual suggestions and engagement tips
            visual_suggestions = self._generate_visual_suggestions(actual_story_type, request.visual_options)
            engagement_tips = self._generate_engagement_tips("story")
            
            return FacebookStoryResponse(
                success=True,
                content=content,
                visual_suggestions=visual_suggestions,
                engagement_tips=engagement_tips,
                metadata={
                    "business_type": request.business_type,
                    "target_audience": request.target_audience,
                    "story_type": actual_story_type,
                    "tone": actual_tone
                }
            )
            
        except Exception as e:
            return FacebookStoryResponse(
                **self._handle_error(e, "Facebook story generation")
            )
    
    def _build_story_prompt(self, request: FacebookStoryRequest, story_type: str, tone: str) -> str:
        """
        Build the prompt for Facebook story generation.
        
        Args:
            request: The story request
            story_type: The actual story type (resolved from custom if needed)
            tone: The actual tone (resolved from custom if needed)
            
        Returns:
            Formatted prompt string
        """
        base_prompt = self._build_base_prompt(
            request.business_type,
            request.target_audience,
            f"Create a {story_type} story"
        )
        
        prompt = f"""
        {base_prompt}
        
        Generate a Facebook Story with the following specifications:
        
        Story Type: {story_type}
        Tone: {tone}
        
        Content Requirements:
        - Include: {request.include or 'N/A'}
        - Avoid: {request.avoid or 'N/A'}
        
        Visual Options:
        - Background Type: {request.visual_options.background_type}
        - Text Overlay: {request.visual_options.text_overlay}
        - Stickers/Emojis: {request.visual_options.stickers}
        - Interactive Elements: {request.visual_options.interactive_elements}
        
        Please create a Facebook Story that:
        1. Is optimized for mobile viewing (vertical format)
        2. Has concise, impactful text (stories are viewed quickly)
        3. Includes clear visual direction for designers
        4. Maintains {tone} tone throughout
        5. Encourages viewer interaction
        6. Fits the {story_type} format
        7. Appeals to: {request.target_audience}
        
        Format the response with:
        - Main story text/copy
        - Visual description
        - Text overlay suggestions
        - Interactive element suggestions (if enabled)
        
        Keep it engaging and story-appropriate for Facebook's ephemeral format.
        """
        
        return prompt
    
    def _generate_visual_suggestions(self, story_type: str, visual_options) -> List[str]:
        """Generate visual suggestions based on story type and options."""
        suggestions = []
        
        if story_type == "Product showcase":
            suggestions.extend([
                "Use high-quality product photos with clean backgrounds",
                "Include multiple angles or features in carousel format",
                "Add animated elements to highlight key features"
            ])
        elif story_type == "Behind the scenes":
            suggestions.extend([
                "Use candid, authentic photos/videos",
                "Show the process or journey",
                "Include team members or workspace shots"
            ])
        elif story_type == "Tutorial/How-to":
            suggestions.extend([
                "Break down steps with numbered overlays",
                "Use before/after comparisons",
                "Include clear, step-by-step visuals"
            ])
        
        # Add general suggestions based on visual options
        if visual_options.text_overlay:
            suggestions.append("Use bold, readable fonts for text overlays")
        
        if visual_options.stickers:
            suggestions.append("Add relevant emojis and stickers to increase engagement")
        
        if visual_options.interactive_elements:
            suggestions.append("Include polls, questions, or swipe-up actions")
        
        return suggestions
    
    def _generate_engagement_tips(self, content_type: str) -> List[str]:
        """Generate engagement tips specific to stories."""
        return [
            "Post at peak audience activity times",
            "Use interactive stickers to encourage participation",
            "Keep text minimal and highly readable",
            "Include a clear call-to-action",
            "Use trending hashtags in story text",
            "Tag relevant accounts to increase reach",
            "Save important stories as Highlights"
        ]