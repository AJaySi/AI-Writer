from typing import Dict, List, Any, Optional, Tuple
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
import sys
import json

# Add parent directory to path to import existing tools
parent_dir = str(Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from lib.database.models import ContentItem, ContentType, Platform, SEOData
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from ..utils.error_handling import handle_calendar_error

logger = logging.getLogger(__name__)

class ContentAtomizer:
    """
    Break down content into atomic pieces that can be recombined
    for different platforms and purposes.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.atomizer')
        
    def atomize_content(self, content: str, title: str = "") -> Dict[str, List[str]]:
        """
        Extract key quotes, statistics, tips, and examples from content.
        
        Args:
            content: The content text to atomize
            title: The content title for context
            
        Returns:
            Dictionary containing different types of content atoms
        """
        try:
            self.logger.info(f"Atomizing content: {title[:50]}...")
            
            # Use AI to extract content atoms
            prompt = f"""
            Analyze the following content and extract key elements that can be repurposed:

            Title: {title}
            Content: {content[:3000]}...

            Extract and categorize the following elements:
            1. Key Statistics (numbers, percentages, data points)
            2. Quotable Insights (memorable quotes or key insights)
            3. Actionable Tips (practical advice or steps)
            4. Examples/Case Studies (real examples or stories)
            5. Key Questions (thought-provoking questions)
            6. Main Arguments (core points or arguments)

            Format your response as JSON:
            {{
                "statistics": ["stat1", "stat2", ...],
                "quotes": ["quote1", "quote2", ...],
                "tips": ["tip1", "tip2", ...],
                "examples": ["example1", "example2", ...],
                "questions": ["question1", "question2", ...],
                "arguments": ["argument1", "argument2", ...]
            }}
            """
            
            response = llm_text_gen(
                prompt=prompt,
                system_prompt="You are an expert content analyst. Extract key elements that can be repurposed across different platforms.",
                json_struct={
                    "type": "object",
                    "properties": {
                        "statistics": {"type": "array", "items": {"type": "string"}},
                        "quotes": {"type": "array", "items": {"type": "string"}},
                        "tips": {"type": "array", "items": {"type": "string"}},
                        "examples": {"type": "array", "items": {"type": "string"}},
                        "questions": {"type": "array", "items": {"type": "string"}},
                        "arguments": {"type": "array", "items": {"type": "string"}}
                    }
                }
            )
            
            if response:
                return response
            else:
                # Fallback to basic extraction
                return self._basic_content_extraction(content)
                
        except Exception as e:
            self.logger.error(f"Error atomizing content: {str(e)}")
            return self._basic_content_extraction(content)
    
    def _basic_content_extraction(self, content: str) -> Dict[str, List[str]]:
        """Fallback method for basic content extraction."""
        atoms = {
            "statistics": [],
            "quotes": [],
            "tips": [],
            "examples": [],
            "questions": [],
            "arguments": []
        }
        
        # Extract statistics (numbers with %)
        stats = re.findall(r'\d+%|\d+\.\d+%|\d+,\d+|\d+ percent', content)
        atoms["statistics"] = stats[:5]  # Limit to 5
        
        # Extract questions
        questions = re.findall(r'[A-Z][^.!?]*\?', content)
        atoms["questions"] = questions[:3]  # Limit to 3
        
        # Extract sentences that might be tips (containing words like "should", "must", "need to")
        tip_patterns = r'[^.!?]*(?:should|must|need to|important to|remember to)[^.!?]*[.!?]'
        tips = re.findall(tip_patterns, content, re.IGNORECASE)
        atoms["tips"] = tips[:5]  # Limit to 5
        
        return atoms

class ContentRepurposer:
    """
    Main content repurposing engine that transforms content for different platforms.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.repurposer')
        self.atomizer = ContentAtomizer()
        
        # Platform-specific content specifications
        self.platform_specs = {
            Platform.TWITTER: {
                'max_length': 280,
                'optimal_length': 240,
                'format': 'concise',
                'tone': 'engaging',
                'hashtags': True,
                'mentions': True
            },
            Platform.LINKEDIN: {
                'max_length': 3000,
                'optimal_length': 1500,
                'format': 'professional',
                'tone': 'authoritative',
                'hashtags': True,
                'mentions': False
            },
            Platform.INSTAGRAM: {
                'max_length': 2200,
                'optimal_length': 1000,
                'format': 'visual-focused',
                'tone': 'casual',
                'hashtags': True,
                'mentions': True
            },
            Platform.FACEBOOK: {
                'max_length': 63206,
                'optimal_length': 500,
                'format': 'engaging',
                'tone': 'conversational',
                'hashtags': False,
                'mentions': True
            },
            Platform.WEBSITE: {
                'max_length': None,
                'optimal_length': 2000,
                'format': 'comprehensive',
                'tone': 'informative',
                'hashtags': False,
                'mentions': False
            }
        }
    
    @handle_calendar_error
    def repurpose_content(
        self,
        source_content: ContentItem,
        target_platforms: List[Platform],
        repurpose_strategy: str = 'adaptive'
    ) -> List[ContentItem]:
        """
        Repurpose content for multiple platforms.
        
        Args:
            source_content: Original content to repurpose
            target_platforms: List of platforms to create content for
            repurpose_strategy: Strategy for repurposing ('adaptive', 'atomic', 'series')
            
        Returns:
            List of repurposed content items
        """
        try:
            self.logger.info(f"Repurposing content '{source_content.title}' for {len(target_platforms)} platforms")
            
            repurposed_content = []
            
            # Get content text (assuming it's in description or notes)
            content_text = source_content.description or source_content.notes or ""
            
            if not content_text:
                self.logger.warning("No content text found for repurposing")
                return []
            
            # Atomize the content
            atoms = self.atomizer.atomize_content(content_text, source_content.title)
            
            # Generate repurposed content for each platform
            for platform in target_platforms:
                if platform == source_content.platforms[0] if source_content.platforms else None:
                    continue  # Skip the original platform
                
                repurposed_item = self._create_platform_specific_content(
                    source_content=source_content,
                    target_platform=platform,
                    atoms=atoms,
                    strategy=repurpose_strategy
                )
                
                if repurposed_item:
                    repurposed_content.append(repurposed_item)
            
            self.logger.info(f"Successfully repurposed content into {len(repurposed_content)} variations")
            return repurposed_content
            
        except Exception as e:
            self.logger.error(f"Error repurposing content: {str(e)}")
            return []
    
    def _create_platform_specific_content(
        self,
        source_content: ContentItem,
        target_platform: Platform,
        atoms: Dict[str, List[str]],
        strategy: str
    ) -> Optional[ContentItem]:
        """Create platform-specific content variation."""
        try:
            platform_spec = self.platform_specs.get(target_platform, {})
            
            # Generate platform-specific content using AI
            repurposed_text = self._generate_platform_content(
                source_content=source_content,
                target_platform=target_platform,
                atoms=atoms,
                platform_spec=platform_spec,
                strategy=strategy
            )
            
            if not repurposed_text:
                return None
            
            # Create new content item
            repurposed_item = ContentItem(
                title=self._adapt_title_for_platform(source_content.title, target_platform),
                description=repurposed_text,
                content_type=self._determine_content_type_for_platform(target_platform),
                platforms=[target_platform],
                publish_date=source_content.publish_date + timedelta(days=1),  # Schedule for next day
                status="draft",
                author=source_content.author,
                tags=source_content.tags + [f"repurposed_from_{source_content.id}"],
                notes=f"Repurposed from: {source_content.title}",
                seo_data=self._adapt_seo_data_for_platform(source_content.seo_data, target_platform)
            )
            
            return repurposed_item
            
        except Exception as e:
            self.logger.error(f"Error creating platform-specific content: {str(e)}")
            return None
    
    def _generate_platform_content(
        self,
        source_content: ContentItem,
        target_platform: Platform,
        atoms: Dict[str, List[str]],
        platform_spec: Dict[str, Any],
        strategy: str
    ) -> str:
        """Generate content optimized for specific platform."""
        try:
            # Prepare content elements
            title = source_content.title
            original_content = source_content.description or ""
            
            # Create platform-specific prompt
            prompt = self._create_repurposing_prompt(
                title=title,
                original_content=original_content,
                target_platform=target_platform,
                atoms=atoms,
                platform_spec=platform_spec,
                strategy=strategy
            )
            
            # Generate content using AI
            repurposed_content = llm_text_gen(prompt)
            
            return repurposed_content or ""
            
        except Exception as e:
            self.logger.error(f"Error generating platform content: {str(e)}")
            return ""
    
    def _create_repurposing_prompt(
        self,
        title: str,
        original_content: str,
        target_platform: Platform,
        atoms: Dict[str, List[str]],
        platform_spec: Dict[str, Any],
        strategy: str
    ) -> str:
        """Create AI prompt for content repurposing."""
        
        platform_guidelines = {
            Platform.TWITTER: "Create engaging tweets that drive conversation. Use threads for complex topics. Include relevant hashtags.",
            Platform.LINKEDIN: "Write professional content that provides value to business professionals. Focus on insights and actionable advice.",
            Platform.INSTAGRAM: "Create visually-oriented content with engaging captions. Use storytelling and include relevant hashtags.",
            Platform.FACEBOOK: "Write conversational content that encourages engagement. Ask questions and create community discussion.",
            Platform.WEBSITE: "Create comprehensive, SEO-optimized content with clear structure and valuable information."
        }
        
        atoms_text = ""
        for atom_type, atom_list in atoms.items():
            if atom_list:
                atoms_text += f"\n{atom_type.title()}: {', '.join(atom_list[:3])}"
        
        prompt = f"""
        Repurpose the following content for {target_platform.name}:

        Original Title: {title}
        Original Content: {original_content[:1500]}...

        Key Content Elements:{atoms_text}

        Platform Guidelines: {platform_guidelines.get(target_platform, '')}

        Platform Specifications:
        - Optimal Length: {platform_spec.get('optimal_length', 'flexible')} characters
        - Format: {platform_spec.get('format', 'standard')}
        - Tone: {platform_spec.get('tone', 'professional')}
        - Include Hashtags: {platform_spec.get('hashtags', False)}

        Requirements:
        1. Adapt the content to fit {target_platform.name}'s format and audience
        2. Maintain the core message and value
        3. Optimize for {target_platform.name} engagement
        4. Include platform-appropriate calls to action
        5. Use the extracted content elements effectively

        Create compelling, platform-optimized content that will perform well on {target_platform.name}.
        """
        
        return prompt
    
    def _adapt_title_for_platform(self, original_title: str, platform: Platform) -> str:
        """Adapt title for specific platform."""
        platform_prefixes = {
            Platform.TWITTER: "🧵 ",
            Platform.LINKEDIN: "💼 ",
            Platform.INSTAGRAM: "📸 ",
            Platform.FACEBOOK: "💬 ",
            Platform.WEBSITE: ""
        }
        
        prefix = platform_prefixes.get(platform, "")
        return f"{prefix}{original_title}"
    
    def _determine_content_type_for_platform(self, platform: Platform) -> ContentType:
        """Determine appropriate content type for platform."""
        platform_content_types = {
            Platform.TWITTER: ContentType.SOCIAL_MEDIA,
            Platform.LINKEDIN: ContentType.SOCIAL_MEDIA,
            Platform.INSTAGRAM: ContentType.SOCIAL_MEDIA,
            Platform.FACEBOOK: ContentType.SOCIAL_MEDIA,
            Platform.WEBSITE: ContentType.BLOG_POST
        }
        
        return platform_content_types.get(platform, ContentType.SOCIAL_MEDIA)
    
    def _adapt_seo_data_for_platform(self, original_seo: SEOData, platform: Platform) -> SEOData:
        """Adapt SEO data for specific platform."""
        if platform == Platform.WEBSITE:
            return original_seo
        
        # For social media platforms, create simplified SEO data
        return SEOData(
            title=original_seo.title,
            meta_description=original_seo.meta_description[:160] if original_seo.meta_description else "",
            keywords=original_seo.keywords[:5] if original_seo.keywords else [],
            structured_data={}
        )

class ContentSeriesRepurposer:
    """
    Create cross-platform content series with progressive disclosure strategy.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.series_repurposer')
        self.repurposer = ContentRepurposer()
    
    def create_cross_platform_series(
        self,
        source_content: ContentItem,
        platforms: List[Platform],
        series_strategy: str = 'progressive_disclosure'
    ) -> Dict[str, List[ContentItem]]:
        """
        Create a content series that progressively reveals information
        across different platforms, driving traffic between them.
        
        Args:
            source_content: Original comprehensive content
            platforms: Target platforms for the series
            series_strategy: Strategy for content distribution
            
        Returns:
            Dictionary mapping platforms to their content pieces
        """
        try:
            self.logger.info(f"Creating cross-platform series for: {source_content.title}")
            
            series_content = {}
            
            if series_strategy == 'progressive_disclosure':
                series_content = self._create_progressive_disclosure_series(
                    source_content, platforms
                )
            elif series_strategy == 'platform_native':
                series_content = self._create_platform_native_series(
                    source_content, platforms
                )
            else:
                # Default to simple repurposing
                repurposed = self.repurposer.repurpose_content(
                    source_content, platforms
                )
                for item in repurposed:
                    platform = item.platforms[0]
                    if platform not in series_content:
                        series_content[platform] = []
                    series_content[platform].append(item)
            
            return series_content
            
        except Exception as e:
            self.logger.error(f"Error creating cross-platform series: {str(e)}")
            return {}
    
    def _create_progressive_disclosure_series(
        self,
        source_content: ContentItem,
        platforms: List[Platform]
    ) -> Dict[str, List[ContentItem]]:
        """Create series with progressive information disclosure."""
        series_content = {}
        
        # Define disclosure strategy
        disclosure_strategy = {
            Platform.TWITTER: "teaser",      # Hook with key stat/question
            Platform.INSTAGRAM: "visual",    # Visual summary with key points
            Platform.LINKEDIN: "insight",    # Professional insight/analysis
            Platform.FACEBOOK: "discussion", # Community discussion starter
            Platform.WEBSITE: "complete"     # Full detailed content
        }
        
        for platform in platforms:
            strategy = disclosure_strategy.get(platform, "summary")
            content_piece = self._create_disclosure_content(
                source_content, platform, strategy
            )
            if content_piece:
                series_content[platform] = [content_piece]
        
        return series_content
    
    def _create_disclosure_content(
        self,
        source_content: ContentItem,
        platform: Platform,
        disclosure_type: str
    ) -> Optional[ContentItem]:
        """Create content piece for specific disclosure strategy."""
        try:
            # This would use the repurposer with specific instructions
            # for the disclosure type
            repurposed = self.repurposer._create_platform_specific_content(
                source_content=source_content,
                target_platform=platform,
                atoms=self.repurposer.atomizer.atomize_content(
                    source_content.description or "", 
                    source_content.title
                ),
                strategy=disclosure_type
            )
            
            return repurposed
            
        except Exception as e:
            self.logger.error(f"Error creating disclosure content: {str(e)}")
            return None
    
    def _create_platform_native_series(
        self,
        source_content: ContentItem,
        platforms: List[Platform]
    ) -> Dict[str, List[ContentItem]]:
        """Create series optimized for each platform's native format."""
        # Implementation for platform-native series
        # This would create multiple pieces per platform
        # optimized for that platform's specific characteristics
        return {}

# Main repurposing interface
class SmartContentRepurposingEngine:
    """
    Main interface for the Smart Content Repurposing Engine.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.repurposing_engine')
        self.repurposer = ContentRepurposer()
        self.series_repurposer = ContentSeriesRepurposer()
        self.atomizer = ContentAtomizer()
    
    def repurpose_single_content(
        self,
        content: ContentItem,
        target_platforms: List[Platform],
        strategy: str = 'adaptive'
    ) -> List[ContentItem]:
        """Repurpose a single piece of content."""
        return self.repurposer.repurpose_content(content, target_platforms, strategy)
    
    def create_content_series(
        self,
        content: ContentItem,
        platforms: List[Platform],
        series_type: str = 'progressive_disclosure'
    ) -> Dict[str, List[ContentItem]]:
        """Create a cross-platform content series."""
        return self.series_repurposer.create_cross_platform_series(
            content, platforms, series_type
        )
    
    def analyze_content_atoms(self, content: str, title: str = "") -> Dict[str, List[str]]:
        """Analyze content and extract reusable atoms."""
        return self.atomizer.atomize_content(content, title)
    
    def get_repurposing_suggestions(
        self,
        content: ContentItem,
        available_platforms: List[Platform]
    ) -> Dict[str, Any]:
        """Get AI-powered suggestions for content repurposing."""
        try:
            # Analyze content to suggest best repurposing strategies
            content_text = content.description or content.notes or ""
            atoms = self.atomizer.atomize_content(content_text, content.title)
            
            suggestions = {
                'recommended_platforms': [],
                'repurposing_strategies': [],
                'content_atoms': atoms,
                'estimated_pieces': 0
            }
            
            # Analyze content type and suggest platforms
            if content.content_type == ContentType.BLOG_POST:
                suggestions['recommended_platforms'] = [
                    Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM
                ]
                suggestions['estimated_pieces'] = len(available_platforms) * 2
            elif content.content_type == ContentType.VIDEO:
                suggestions['recommended_platforms'] = [
                    Platform.TWITTER, Platform.INSTAGRAM, Platform.FACEBOOK
                ]
                suggestions['estimated_pieces'] = len(available_platforms) * 3
            
            # Suggest strategies based on content richness
            if len(atoms.get('statistics', [])) > 3:
                suggestions['repurposing_strategies'].append('data_driven')
            if len(atoms.get('tips', [])) > 5:
                suggestions['repurposing_strategies'].append('tip_series')
            if len(atoms.get('examples', [])) > 2:
                suggestions['repurposing_strategies'].append('case_study_series')
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error getting repurposing suggestions: {str(e)}")
            return {
                'recommended_platforms': [],
                'repurposing_strategies': [],
                'content_atoms': {},
                'estimated_pieces': 0
            } 