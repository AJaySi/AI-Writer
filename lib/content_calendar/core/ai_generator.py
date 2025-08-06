from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import sys
import json

# Add parent directory to path to import existing tools
parent_dir = str(Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from lib.database.models import ContentType, ContentItem, Platform
from lib.ai_seo_tools.content_calendar.utils.error_handling import handle_calendar_error
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main

logger = logging.getLogger(__name__)

class AIGenerator:
    """AI-powered content generation and enhancement."""
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.ai_generator')
        self.logger.info("Initializing AIGenerator")
        self._setup_logging()
        self._load_ai_tools()
    
    def _setup_logging(self):
        """Configure logging for AI generator."""
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def _load_ai_tools(self):
        """Load and initialize AI tools."""
        try:
            # Initialize AI tools
            self.gap_analyzer = ContentGapAnalysis()
            self.title_generator = ai_title_generator
            self.meta_generator = metadesc_generator_main
            
        except Exception as e:
            logger.error(f"Error loading AI tools: {str(e)}")
            raise
    
    def generate_content(self, content_item: ContentItem, target_audience: Dict[str, Any]) -> Dict[str, Any]:
        """Generate base content using AI."""
        try:
            self.logger.info(f"Generating content for: {content_item.title}")
            
            # Generate content based on type and platform
            content = {
                'title': content_item.title,
                'content_flow': {
                    'introduction': {
                        'summary': f"An engaging introduction about {content_item.title}",
                        'key_points': [
                            f"Key point 1 about {content_item.title}",
                            f"Key point 2 about {content_item.title}",
                            f"Key point 3 about {content_item.title}"
                        ]
                    },
                    'main_content': {
                        'sections': [
                            {
                                'title': f"Section 1: Understanding {content_item.title}",
                                'content': f"Detailed content about {content_item.title}",
                                'subsections': []
                            },
                            {
                                'title': f"Section 2: Best Practices for {content_item.title}",
                                'content': "Best practices and recommendations",
                                'subsections': []
                            }
                        ]
                    },
                    'conclusion': {
                        'summary': f"Concluding thoughts about {content_item.title}",
                        'call_to_action': "Next steps and actions"
                    }
                },
                'metadata': {
                    'tone': target_audience.get('content_settings', {}).get('tone', 'professional'),
                    'length': target_audience.get('content_settings', {}).get('length', 'medium'),
                    'platform': content_item.platforms[0].name if content_item.platforms else 'Unknown',
                    'content_type': content_item.content_type.name
                }
            }
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating content: {str(e)}", exc_info=True)
            return {}

    def enhance_content(self, content: ContentItem, enhancement_type: str, target_audience: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance existing content using AI."""
        try:
            self.logger.info(f"Enhancing content: {content.title}")
            
            # Enhance content based on type
            enhanced = {
                'content': f"Enhanced version of {content.description}",
                'changes': [
                    "Improved readability",
                    "Enhanced engagement elements",
                    "Optimized for target audience"
                ],
                'metadata': {
                    'enhancement_type': enhancement_type,
                    'target_audience': target_audience
                }
            }
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing content: {str(e)}", exc_info=True)
            return {}

    def enhance_for_platform(self, content: Dict[str, Any], platform: Platform, enhancement_type: str) -> Dict[str, Any]:
        """Enhance content specifically for a platform."""
        try:
            self.logger.info(f"Enhancing content for platform: {platform.name}")
            
            # Platform-specific enhancements
            enhanced = {
                'content': content.get('content', ''),
                'changes': [
                    f"Optimized for {platform.name}",
                    "Platform-specific formatting",
                    "Enhanced engagement elements"
                ],
                'metadata': {
                    'platform': platform.name,
                    'enhancement_type': enhancement_type
                }
            }
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing for platform: {str(e)}", exc_info=True)
            return {}

    def enhance_variant(self, content: Dict[str, Any], variant_type: str, optimization_goals: List[str]) -> Dict[str, Any]:
        """Enhance a content variant for A/B testing."""
        try:
            self.logger.info(f"Enhancing variant: {variant_type}")
            
            # Variant-specific enhancements
            enhanced = {
                'content': content.get('content', ''),
                'changes': [
                    f"Optimized for {', '.join(optimization_goals)}",
                    "Enhanced variant-specific elements",
                    "Improved engagement metrics"
                ],
                'metadata': {
                    'variant_type': variant_type,
                    'optimization_goals': optimization_goals
                }
            }
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing variant: {str(e)}", exc_info=True)
            return {}

    def enhance_for_seo(self, content: Dict[str, Any], seo_goals: List[str]) -> Dict[str, Any]:
        """Enhance content for SEO optimization."""
        try:
            self.logger.info("Enhancing content for SEO")
            
            # SEO-specific enhancements
            enhanced = {
                'content': content.get('content', ''),
                'changes': [
                    f"Optimized for {', '.join(seo_goals)}",
                    "Enhanced keyword placement",
                    "Improved meta information"
                ],
                'metadata': {
                    'seo_goals': seo_goals
                }
            }
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error enhancing for SEO: {str(e)}", exc_info=True)
            return {}

    def generate_series_content(self, content_item: ContentItem, series_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content for a series."""
        try:
            self.logger.info(f"Generating series content: {content_item.title}")
            
            # Generate series-specific content
            content = {
                'title': content_item.title,
                'content_flow': {
                    'introduction': {
                        'summary': f"Part {series_info['part_number']} of {series_info['total_parts']} about {series_info['topic']}",
                        'key_points': [
                            f"Key point 1 for part {series_info['part_number']}",
                            f"Key point 2 for part {series_info['part_number']}",
                            f"Key point 3 for part {series_info['part_number']}"
                        ]
                    },
                    'main_content': {
                        'sections': [
                            {
                                'title': f"Section 1: Part {series_info['part_number']} Overview",
                                'content': f"Detailed content for part {series_info['part_number']}",
                                'subsections': []
                            },
                            {
                                'title': f"Section 2: Part {series_info['part_number']} Details",
                                'content': "Specific details and information",
                                'subsections': []
                            }
                        ]
                    },
                    'conclusion': {
                        'summary': f"Concluding thoughts for part {series_info['part_number']}",
                        'next_part': f"Preview of part {series_info['part_number'] + 1}" if series_info['part_number'] < series_info['total_parts'] else "Series conclusion"
                    }
                },
                'metadata': {
                    'series_info': series_info,
                    'platform': content_item.platforms[0].name if content_item.platforms else 'Unknown',
                    'content_type': content_item.content_type.name
                }
            }
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating series content: {str(e)}", exc_info=True)
            return {}

    @handle_calendar_error
    def generate_headings(
        self,
        title: str,
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate content headings using AI.
        
        Args:
            title: Content title
            content_type: Type of content
            context: Content context from gap analysis
            
        Returns:
            List of generated headings with metadata
        """
        try:
            # Get content gaps and opportunities
            gaps = self.gap_analyzer.analyze_gaps(context.get('website_url', ''))
            
            # Generate headings based on content type and gaps
            prompt = self._create_heading_prompt(title, content_type, gaps)
            headings = self._call_ai_model(prompt)
            
            return self._format_headings(headings)
            
        except Exception as e:
            logger.error(f"Error generating headings: {str(e)}")
            return []
    
    @handle_calendar_error
    def generate_subheadings(
        self,
        main_heading: Dict[str, Any],
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate subheadings for a main heading.
        
        Args:
            main_heading: Main heading to generate subheadings for
            content_type: Type of content
            context: Content context
            
        Returns:
            List of generated subheadings
        """
        try:
            # Create prompt for subheading generation
            prompt = self._create_subheading_prompt(
                main_heading,
                content_type,
                context
            )
            
            # Generate subheadings
            subheadings = self._call_ai_model(prompt)
            
            return self._format_subheadings(subheadings)
            
        except Exception as e:
            logger.error(f"Error generating subheadings: {str(e)}")
            return []
    
    @handle_calendar_error
    def generate_key_points(
        self,
        title: str,
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate key points for content.
        
        Args:
            title: Content title
            content_type: Type of content
            context: Content context
            
        Returns:
            List of key points with supporting information
        """
        try:
            # Generate title and meta description for SEO context
            seo_title = self.title_generator(title)
            meta_desc = self.meta_generator(title)
            
            # Create prompt for key points
            prompt = self._create_key_points_prompt(
                title,
                content_type,
                {'title': seo_title, 'meta_description': meta_desc},
                context
            )
            
            # Generate key points
            points = self._call_ai_model(prompt)
            
            return self._format_key_points(points)
            
        except Exception as e:
            logger.error(f"Error generating key points: {str(e)}")
            return []
    
    @handle_calendar_error
    def generate_content_flow(
        self,
        title: str,
        content_type: ContentType,
        outline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate content flow and structure.
        
        Args:
            title: Content title
            content_type: Type of content
            outline: Content outline with headings and key points
            
        Returns:
            Dictionary containing content flow and structure
        """
        try:
            # Create prompt for content flow
            prompt = self._create_flow_prompt(title, content_type, outline)
            
            # Generate content flow
            flow = self._call_ai_model(prompt)
            
            return self._format_content_flow(flow)
            
        except Exception as e:
            logger.error(f"Error generating content flow: {str(e)}")
            return {}
    
    def _create_heading_prompt(
        self,
        title: str,
        content_type: ContentType,
        gaps: Dict[str, Any]
    ) -> str:
        """Create prompt for heading generation."""
        return f"""
        Generate main headings for a {content_type.value} titled "{title}".
        Consider the following content gaps and opportunities:
        {json.dumps(gaps, indent=2)}
        
        For each heading, provide:
        1. Title
        2. Level (1 for main headings)
        3. Key keywords to include
        4. Brief summary of what this section should cover
        
        Format the response as a JSON array of heading objects.
        """
    
    def _create_subheading_prompt(
        self,
        main_heading: Dict[str, Any],
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> str:
        """Create prompt for subheading generation."""
        return f"""
        Generate subheadings for the main heading "{main_heading['title']}" 
        in a {content_type.value}.
        
        Main heading details:
        {json.dumps(main_heading, indent=2)}
        
        For each subheading, provide:
        1. Title
        2. Level (2 for subheadings)
        3. Key keywords to include
        4. Brief summary of what this subsection should cover
        
        Format the response as a JSON array of subheading objects.
        """
    
    def _create_key_points_prompt(
        self,
        title: str,
        content_type: ContentType,
        seo_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Create prompt for key points generation."""
        return f"""
        Generate key points for a {content_type.value} titled "{title}".
        
        SEO Requirements:
        {json.dumps(seo_data, indent=2)}
        
        For each key point, provide:
        1. Main point
        2. Importance level (high/medium/low)
        3. Supporting evidence or examples
        4. Related keywords to include
        
        Format the response as a JSON array of key point objects.
        """
    
    def _create_flow_prompt(
        self,
        title: str,
        content_type: ContentType,
        outline: Dict[str, Any]
    ) -> str:
        """Create prompt for content flow generation."""
        return f"""
        Generate content flow and structure for a {content_type.value} titled "{title}".
        
        Content Outline:
        {json.dumps(outline, indent=2)}
        
        Provide:
        1. Introduction structure
        2. Main sections flow
        3. Conclusion approach
        4. Transition points between sections
        5. Content pacing recommendations
        
        Format the response as a JSON object with these sections.
        """
    
    def _call_ai_model(self, prompt: str) -> Any:
        """
        Call the AI model with the given prompt.
        
        Args:
            prompt: The prompt to send to the AI model
            
        Returns:
            The AI model's response, parsed as JSON
        """
        try:
            # Call the AI model
            response = llm_text_gen(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            # Parse the response as JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing AI response as JSON: {str(e)}")
                logger.error(f"Raw response: {response}")
                return {}
            
        except Exception as e:
            logger.error(f"Error calling AI model: {str(e)}")
            return {}
    
    def _format_headings(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format and validate generated headings."""
        formatted = []
        for heading in headings:
            formatted.append({
                'title': heading.get('title', ''),
                'level': heading.get('level', 1),
                'keywords': heading.get('keywords', []),
                'summary': heading.get('summary', '')
            })
        return formatted
    
    def _format_subheadings(self, subheadings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format and validate generated subheadings."""
        formatted = []
        for subheading in subheadings:
            formatted.append({
                'title': subheading.get('title', ''),
                'level': subheading.get('level', 2),
                'keywords': subheading.get('keywords', []),
                'summary': subheading.get('summary', '')
            })
        return formatted
    
    def _format_key_points(self, points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format and validate generated key points."""
        formatted = []
        for point in points:
            formatted.append({
                'point': point.get('point', ''),
                'importance': point.get('importance', 'medium'),
                'supporting_evidence': point.get('evidence', []),
                'related_keywords': point.get('keywords', [])
            })
        return formatted
    
    def _format_content_flow(self, flow: Dict[str, Any]) -> Dict[str, Any]:
        """Format and validate generated content flow."""
        return {
            'introduction': flow.get('introduction', {}),
            'main_sections': flow.get('main_sections', []),
            'conclusion': flow.get('conclusion', {}),
            'transitions': flow.get('transitions', []),
            'content_pacing': flow.get('pacing', {})
        }

    def generate_ai_suggestions(
        self,
        content_type: str,
        topic: str,
        audience: str,
        goals: List[str],
        tone: str,
        length: str,
        model_settings: Dict[str, Any],
        style_preferences: List[str],
        seo_preferences: Dict[str, Any],
        platform_settings: Dict[str, Any],
        platform: str
    ) -> List[Dict[str, Any]]:
        """
        Generate AI content suggestions based on input parameters.
        """
        try:
            self.logger.info(f"Generating AI suggestions for topic: {topic}")
            
            # Create a comprehensive prompt for content generation
            prompt = f"""Generate content suggestions for the following parameters:

Content Type: {content_type}
Topic: {topic}
Target Audience: {audience}
Goals: {', '.join(goals)}
Tone: {tone}
Length: {length}

Style Preferences:
- Creativity Level: {model_settings.get('Creativity Level', 'medium')}
- Formality Level: {model_settings.get('Formality Level', 'professional')}
- Style Elements: {', '.join(style_preferences)}

SEO Preferences:
- Keyword Density: {seo_preferences.get('Keyword Density', 2)}%
- Internal Linking: {'Enabled' if seo_preferences.get('Internal Linking', True) else 'Disabled'}
- External Linking: {'Enabled' if seo_preferences.get('External Linking', True) else 'Disabled'}

Platform Settings:
- Platform: {platform}
- Platform-specific requirements: {', '.join(platform_settings)}

Please generate 3 different content suggestions. Format your response as a valid JSON object with the following structure:
{{
    "suggestions": [
        {{
            "title": "string",
            "introduction": "string",
            "key_points": ["string"],
            "main_sections": [
                {{
                    "title": "string",
                    "content": "string",
                    "engagement_elements": ["string"],
                    "seo_elements": ["string"]
                }}
            ],
            "conclusion": "string",
            "seo_elements": ["string"],
            "platform_optimizations": ["string"],
            "engagement_strategies": ["string"],
            "content_metrics": {{
                "estimated_read_time": "string",
                "word_count": "number",
                "keyword_density": "number",
                "engagement_score": "number"
            }}
        }}
    ]
}}

IMPORTANT: Your response must be a valid JSON object. Do not include any text before or after the JSON object."""

            # Generate content using llm_text_gen
            generated_content = llm_text_gen(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            if not generated_content:
                self.logger.error("No content generated from AI model")
                return []

            # Parse the generated content
            try:
                # If generated_content is already a dict, use it directly
                if isinstance(generated_content, dict):
                    content_data = generated_content
                else:
                    # Try to parse as JSON string
                    content_data = json.loads(generated_content)
                
                if not content_data or 'suggestions' not in content_data:
                    self.logger.error("Invalid content structure in AI response")
                    return []

                return self._format_suggestions(
                    content_data,
                    content_type,
                    audience,
                    goals,
                    tone,
                    length,
                    model_settings,
                    seo_preferences,
                    platform
                )
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing generated content: {str(e)}")
                # Try to extract JSON from the response if it's wrapped in other text
                try:
                    # Find the first '{' and last '}'
                    start = generated_content.find('{')
                    end = generated_content.rfind('}') + 1
                    if start >= 0 and end > start:
                        json_str = generated_content[start:end]
                        content_data = json.loads(json_str)
                        if not content_data or 'suggestions' not in content_data:
                            self.logger.error("Invalid content structure in extracted JSON")
                            return []
                        return self._format_suggestions(
                            content_data,
                            content_type,
                            audience,
                            goals,
                            tone,
                            length,
                            model_settings,
                            seo_preferences,
                            platform
                        )
                except Exception as e2:
                    self.logger.error(f"Error extracting JSON from response: {str(e2)}")
                    return []
            
        except Exception as e:
            self.logger.error(f"Error generating AI suggestions: {str(e)}", exc_info=True)
            return []

    def _format_suggestions(
        self,
        content_data: Dict[str, Any],
        content_type: str,
        audience: str,
        goals: List[str],
        tone: str,
        length: str,
        model_settings: Dict[str, Any],
        seo_preferences: Dict[str, Any],
        platform: str
    ) -> List[Dict[str, Any]]:
        """Format and process suggestions from content data."""
        suggestions = []
        for suggestion in content_data.get('suggestions', []):
            formatted_suggestion = {
                'title': suggestion.get('title', ''),
                'type': content_type,
                'platform': platform,
                'audience': audience,
                'impact': f"High impact for {', '.join(goals)}",
                'preview': suggestion.get('introduction', ''),
                'style_elements': [
                    f"Tone: {tone}",
                    f"Length: {length}",
                    f"Creativity: {model_settings['Creativity Level']}",
                    f"Formality: {model_settings['Formality Level']}"
                ],
                'seo_elements': [
                    f"Keyword Density: {seo_preferences['Keyword Density']}%",
                    "Internal Linking: Enabled" if seo_preferences['Internal Linking'] else "Internal Linking: Disabled",
                    "External Linking: Enabled" if seo_preferences['External Linking'] else "External Linking: Disabled"
                ],
                'engagement_score': f"{85 + len(suggestions)*5}%",
                'reach': 'High',
                'conversion': f"{3.5 + len(suggestions)*0.5}%",
                'seo_impact': 'Strong',
                'platform_optimizations': suggestion.get('platform_optimizations', []),
                'variations': [
                    "Alternative headline",
                    "Different content angle",
                    "Alternative format"
                ],
                'seo_recommendations': suggestion.get('seo_elements', []),
                'media_suggestions': [
                    "Featured image",
                    "Supporting graphics",
                    "Social media visuals"
                ]
            }
            suggestions.append(formatted_suggestion)
        return suggestions 