from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import existing tools
parent_dir = str(Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from lib.database.models import ContentItem, ContentType, Platform
from ..utils.error_handling import handle_calendar_error
from lib.ai_seo_tools.content_gap_analysis.main import ContentGapAnalysis
from lib.ai_seo_tools.content_title_generator import ai_title_generator
from lib.ai_seo_tools.meta_desc_generator import metadesc_generator_main
from lib.ai_seo_tools.content_calendar.core.content_repurposer import SmartContentRepurposingEngine

logger = logging.getLogger(__name__)

class ContentGenerator:
    """
    Enhanced content generator with smart repurposing capabilities.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('content_calendar.content_generator')
        self.logger.info("Initializing ContentGenerator")
        self._setup_logging()
        self._load_ai_tools()
        # Initialize the Smart Content Repurposing Engine
        self.repurposing_engine = SmartContentRepurposingEngine()
    
    def _setup_logging(self):
        """Configure logging for content generator."""
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
    
    @handle_calendar_error
    def generate_headings(
        self,
        content_item: ContentItem,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate main headings for content.
        
        Args:
            content_item: Content item to generate headings for
            context: Content context from gap analysis
            
        Returns:
            List of main headings with metadata
        """
        try:
            # Use AI to generate headings based on content type and context
            headings = self._generate_ai_headings(
                title=content_item.title,
                content_type=content_item.content_type,
                context=context
            )
            
            # Format and validate headings
            formatted_headings = []
            for heading in headings:
                formatted_heading = {
                    'title': heading['title'],
                    'level': heading.get('level', 1),
                    'keywords': heading.get('keywords', []),
                    'summary': heading.get('summary', '')
                }
                formatted_headings.append(formatted_heading)
            
            return formatted_headings
            
        except Exception as e:
            logger.error(f"Error generating headings: {str(e)}")
            return []
    
    @handle_calendar_error
    def generate_subheadings(
        self,
        content_item: ContentItem,
        main_headings: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate subheadings for each main heading.
        
        Args:
            content_item: Content item to generate subheadings for
            main_headings: List of main headings
            context: Content context from gap analysis
            
        Returns:
            Dictionary mapping main headings to their subheadings
        """
        try:
            subheadings = {}
            
            for heading in main_headings:
                # Generate subheadings for each main heading
                heading_subheadings = self._generate_ai_subheadings(
                    main_heading=heading,
                    content_type=content_item.content_type,
                    context=context
                )
                
                # Format and validate subheadings
                formatted_subheadings = []
                for subheading in heading_subheadings:
                    formatted_subheading = {
                        'title': subheading['title'],
                        'level': subheading.get('level', 2),
                        'keywords': subheading.get('keywords', []),
                        'summary': subheading.get('summary', '')
                    }
                    formatted_subheadings.append(formatted_subheading)
                
                subheadings[heading['title']] = formatted_subheadings
            
            return subheadings
            
        except Exception as e:
            logger.error(f"Error generating subheadings: {str(e)}")
            return {}
    
    @handle_calendar_error
    def generate_key_points(
        self,
        content_item: ContentItem,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate key points for the content.
        
        Args:
            content_item: Content item to generate key points for
            context: Content context from gap analysis
            
        Returns:
            List of key points with supporting information
        """
        try:
            # Generate key points using AI
            key_points = self._generate_ai_key_points(
                title=content_item.title,
                content_type=content_item.content_type,
                context=context
            )
            
            # Format and validate key points
            formatted_points = []
            for point in key_points:
                formatted_point = {
                    'point': point['point'],
                    'importance': point.get('importance', 'medium'),
                    'supporting_evidence': point.get('evidence', []),
                    'related_keywords': point.get('keywords', [])
                }
                formatted_points.append(formatted_point)
            
            return formatted_points
            
        except Exception as e:
            logger.error(f"Error generating key points: {str(e)}")
            return []
    
    @handle_calendar_error
    def generate_content_flow(
        self,
        content_item: ContentItem,
        outline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate content flow and structure.
        
        Args:
            content_item: Content item to generate flow for
            outline: Content outline with headings and key points
            
        Returns:
            Dictionary containing content flow and structure
        """
        try:
            # Generate content flow using AI
            flow = self._generate_ai_content_flow(
                title=content_item.title,
                content_type=content_item.content_type,
                outline=outline
            )
            
            return {
                'introduction': flow.get('introduction', {}),
                'main_sections': flow.get('main_sections', []),
                'conclusion': flow.get('conclusion', {}),
                'transitions': flow.get('transitions', []),
                'content_pacing': flow.get('pacing', {})
            }
            
        except Exception as e:
            logger.error(f"Error generating content flow: {str(e)}")
            return {}
    
    def _generate_ai_headings(
        self,
        title: str,
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Use AI to generate content headings.
        """
        # TODO: Implement AI heading generation
        # This would use the existing AI tools to generate headings
        return []
    
    def _generate_ai_subheadings(
        self,
        main_heading: Dict[str, Any],
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Use AI to generate subheadings.
        """
        # TODO: Implement AI subheading generation
        return []
    
    def _generate_ai_key_points(
        self,
        title: str,
        content_type: ContentType,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Use AI to generate key points.
        """
        # TODO: Implement AI key point generation
        return []
    
    def _generate_ai_content_flow(
        self,
        title: str,
        content_type: ContentType,
        outline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use AI to generate content flow.
        """
        # TODO: Implement AI content flow generation
        return {}
    
    def generate_variation(self, content: Dict[str, Any], variation_type: str) -> Dict[str, Any]:
        """Generate a variation of the given content.
        
        Args:
            content: Original content to vary
            variation_type: Type of variation to generate ('tone', 'length', 'style', etc.)
            
        Returns:
            Dictionary containing the varied content
        """
        try:
            self.logger.info(f"Generating {variation_type} variation for content")
            
            # Generate variation based on type
            variation = {
                'title': f"{content.get('title', '')} - {variation_type.title()} Variation",
                'content_flow': {
                    'introduction': {
                        'summary': f"Varied introduction for {content.get('title', '')}",
                        'key_points': [
                            f"Varied key point 1 for {variation_type}",
                            f"Varied key point 2 for {variation_type}",
                            f"Varied key point 3 for {variation_type}"
                        ]
                    },
                    'main_content': {
                        'sections': [
                            {
                                'title': f"Varied Section 1: {variation_type.title()} Approach",
                                'content': f"Varied content for {variation_type}",
                                'subsections': []
                            },
                            {
                                'title': f"Varied Section 2: {variation_type.title()} Details",
                                'content': "Varied details and information",
                                'subsections': []
                            }
                        ]
                    },
                    'conclusion': {
                        'summary': f"Varied conclusion for {variation_type}",
                        'call_to_action': "Varied call to action"
                    }
                },
                'metadata': {
                    'variation_type': variation_type,
                    'original_content': content.get('title', ''),
                    'platform': content.get('metadata', {}).get('platform', 'Unknown'),
                    'content_type': content.get('metadata', {}).get('content_type', 'Unknown')
                }
            }
            
            return variation
            
        except Exception as e:
            self.logger.error(f"Error generating variation: {str(e)}")
            return {}
    
    @handle_calendar_error
    def repurpose_content_for_platforms(
        self,
        content_item: ContentItem,
        target_platforms: List[Platform],
        strategy: str = 'adaptive'
    ) -> List[ContentItem]:
        """
        Repurpose existing content for multiple platforms using the Smart Content Repurposing Engine.
        
        Args:
            content_item: Original content to repurpose
            target_platforms: List of platforms to create content for
            strategy: Repurposing strategy ('adaptive', 'atomic', 'series')
            
        Returns:
            List of repurposed content items optimized for each platform
        """
        try:
            self.logger.info(f"Repurposing content '{content_item.title}' for {len(target_platforms)} platforms")
            
            # Use the repurposing engine to create platform-specific content
            repurposed_content = self.repurposing_engine.repurpose_single_content(
                content=content_item,
                target_platforms=target_platforms,
                strategy=strategy
            )
            
            self.logger.info(f"Successfully created {len(repurposed_content)} repurposed content pieces")
            return repurposed_content
            
        except Exception as e:
            self.logger.error(f"Error repurposing content: {str(e)}")
            return []
    
    @handle_calendar_error
    def create_content_series_across_platforms(
        self,
        source_content: ContentItem,
        platforms: List[Platform],
        series_type: str = 'progressive_disclosure'
    ) -> Dict[str, List[ContentItem]]:
        """
        Create a cross-platform content series with progressive disclosure strategy.
        
        Args:
            source_content: Original comprehensive content
            platforms: Target platforms for the series
            series_type: Type of series ('progressive_disclosure', 'platform_native')
            
        Returns:
            Dictionary mapping platforms to their content pieces
        """
        try:
            self.logger.info(f"Creating cross-platform series for '{source_content.title}'")
            
            # Use the repurposing engine to create a content series
            series_content = self.repurposing_engine.create_content_series(
                content=source_content,
                platforms=platforms,
                series_type=series_type
            )
            
            total_pieces = sum(len(pieces) for pieces in series_content.values())
            self.logger.info(f"Successfully created series with {total_pieces} pieces across {len(series_content)} platforms")
            
            return series_content
            
        except Exception as e:
            self.logger.error(f"Error creating content series: {str(e)}")
            return {}
    
    @handle_calendar_error
    def analyze_content_for_repurposing(
        self,
        content_item: ContentItem,
        available_platforms: List[Platform]
    ) -> Dict[str, Any]:
        """
        Analyze content and get AI-powered repurposing suggestions.
        
        Args:
            content_item: Content to analyze
            available_platforms: Available platforms for repurposing
            
        Returns:
            Dictionary containing repurposing suggestions and analysis
        """
        try:
            self.logger.info(f"Analyzing content '{content_item.title}' for repurposing opportunities")
            
            # Get repurposing suggestions from the engine
            suggestions = self.repurposing_engine.get_repurposing_suggestions(
                content=content_item,
                available_platforms=available_platforms
            )
            
            # Add content analysis
            content_text = content_item.description or content_item.notes or ""
            content_atoms = self.repurposing_engine.analyze_content_atoms(
                content=content_text,
                title=content_item.title
            )
            
            analysis = {
                'content_analysis': {
                    'word_count': len(content_text.split()) if content_text else 0,
                    'content_richness': self._assess_content_richness(content_atoms),
                    'repurposing_potential': self._assess_repurposing_potential(content_atoms),
                    'content_atoms': content_atoms
                },
                'platform_suggestions': suggestions['recommended_platforms'],
                'strategy_suggestions': suggestions['repurposing_strategies'],
                'estimated_output': {
                    'total_pieces': suggestions['estimated_pieces'],
                    'time_savings': f"{suggestions['estimated_pieces'] * 2} hours",
                    'content_multiplication': f"{suggestions['estimated_pieces']}x"
                }
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing content for repurposing: {str(e)}")
            return {}
    
    def _assess_content_richness(self, content_atoms: Dict[str, List[str]]) -> str:
        """Assess the richness of content based on extracted atoms."""
        total_atoms = sum(len(atoms) for atoms in content_atoms.values())
        
        if total_atoms >= 15:
            return "High"
        elif total_atoms >= 8:
            return "Medium"
        else:
            return "Low"
    
    def _assess_repurposing_potential(self, content_atoms: Dict[str, List[str]]) -> str:
        """Assess the repurposing potential based on content atoms."""
        # Check for diverse content types
        atom_types_with_content = sum(1 for atoms in content_atoms.values() if atoms)
        
        if atom_types_with_content >= 4:
            return "Excellent"
        elif atom_types_with_content >= 3:
            return "Good"
        elif atom_types_with_content >= 2:
            return "Fair"
        else:
            return "Limited"
    
    @handle_calendar_error
    def generate_content_with_repurposing_plan(
        self,
        content_item: ContentItem,
        context: Dict[str, Any],
        target_platforms: List[Platform] = None
    ) -> Dict[str, Any]:
        """
        Generate content along with a comprehensive repurposing plan.
        
        Args:
            content_item: Content item to generate
            context: Content context from gap analysis
            target_platforms: Platforms to include in repurposing plan
            
        Returns:
            Dictionary containing generated content and repurposing plan
        """
        try:
            self.logger.info(f"Generating content with repurposing plan for '{content_item.title}'")
            
            # Generate the main content structure
            headings = self.generate_headings(content_item, context)
            subheadings = self.generate_subheadings(content_item, headings, context)
            key_points = self.generate_key_points(content_item, context)
            
            outline = {
                'headings': headings,
                'subheadings': subheadings,
                'key_points': key_points
            }
            
            content_flow = self.generate_content_flow(content_item, outline)
            
            # Create repurposing plan if platforms are specified
            repurposing_plan = {}
            if target_platforms:
                # Analyze repurposing potential
                analysis = self.analyze_content_for_repurposing(content_item, target_platforms)
                
                # Generate repurposing suggestions
                repurposing_plan = {
                    'analysis': analysis,
                    'recommended_strategy': self._recommend_repurposing_strategy(analysis),
                    'platform_roadmap': self._create_platform_roadmap(content_item, target_platforms),
                    'content_calendar_integration': self._suggest_calendar_integration(content_item, target_platforms)
                }
            
            return {
                'content': {
                    'outline': outline,
                    'content_flow': content_flow,
                    'metadata': {
                        'generated_at': str(datetime.now()),
                        'content_type': content_item.content_type.name,
                        'platforms': [p.name for p in content_item.platforms] if content_item.platforms else []
                    }
                },
                'repurposing_plan': repurposing_plan
            }
            
        except Exception as e:
            self.logger.error(f"Error generating content with repurposing plan: {str(e)}")
            return {}
    
    def _recommend_repurposing_strategy(self, analysis: Dict[str, Any]) -> str:
        """Recommend the best repurposing strategy based on content analysis."""
        content_richness = analysis.get('content_analysis', {}).get('content_richness', 'Low')
        repurposing_potential = analysis.get('content_analysis', {}).get('repurposing_potential', 'Limited')
        
        if content_richness == 'High' and repurposing_potential in ['Excellent', 'Good']:
            return 'progressive_disclosure'
        elif content_richness in ['Medium', 'High']:
            return 'adaptive'
        else:
            return 'atomic'
    
    def _create_platform_roadmap(
        self,
        content_item: ContentItem,
        target_platforms: List[Platform]
    ) -> Dict[str, Any]:
        """Create a roadmap for content distribution across platforms."""
        roadmap = {
            'timeline': {},
            'platform_sequence': [],
            'cross_promotion_opportunities': []
        }
        
        # Create a timeline for content release
        base_date = content_item.publish_date or datetime.now()
        
        for i, platform in enumerate(target_platforms):
            release_date = base_date + timedelta(days=i)
            roadmap['timeline'][platform.name] = {
                'release_date': release_date.strftime('%Y-%m-%d'),
                'content_type': self._get_optimal_content_type_for_platform(platform),
                'engagement_strategy': self._get_engagement_strategy_for_platform(platform)
            }
            roadmap['platform_sequence'].append(platform.name)
        
        return roadmap
    
    def _suggest_calendar_integration(
        self,
        content_item: ContentItem,
        target_platforms: List[Platform]
    ) -> Dict[str, Any]:
        """Suggest how to integrate repurposed content into the content calendar."""
        return {
            'scheduling_recommendations': {
                'primary_content': 'Schedule as main content piece',
                'repurposed_content': 'Schedule 1-2 days after primary content',
                'series_content': 'Schedule weekly releases for maximum impact'
            },
            'calendar_tags': [
                'repurposed_content',
                f'source_{content_item.id}',
                'multi_platform_series'
            ],
            'performance_tracking': {
                'metrics_to_track': ['engagement_rate', 'cross_platform_traffic', 'conversion_rate'],
                'comparison_baseline': 'Compare against single-platform content performance'
            }
        }
    
    def _get_optimal_content_type_for_platform(self, platform: Platform) -> str:
        """Get the optimal content type for a specific platform."""
        platform_content_types = {
            Platform.TWITTER: 'Thread or single tweet',
            Platform.LINKEDIN: 'Professional post or article',
            Platform.INSTAGRAM: 'Visual post with caption',
            Platform.FACEBOOK: 'Engaging post with discussion starter',
            Platform.WEBSITE: 'Full blog post or article'
        }
        return platform_content_types.get(platform, 'Standard post')
    
    def _get_engagement_strategy_for_platform(self, platform: Platform) -> str:
        """Get the engagement strategy for a specific platform."""
        engagement_strategies = {
            Platform.TWITTER: 'Use hashtags, engage in conversations, create polls',
            Platform.LINKEDIN: 'Professional networking, thought leadership, industry discussions',
            Platform.INSTAGRAM: 'Visual storytelling, user-generated content, stories',
            Platform.FACEBOOK: 'Community building, discussions, live interactions',
            Platform.WEBSITE: 'SEO optimization, internal linking, lead magnets'
        }
        return engagement_strategies.get(platform, 'Standard engagement tactics') 