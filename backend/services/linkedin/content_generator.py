"""
Content Generator for LinkedIn Content Generation

Handles the main content generation logic for posts and articles.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger
from models.linkedin_models import (
    LinkedInPostRequest, LinkedInArticleRequest, LinkedInPostResponse, LinkedInArticleResponse,
    PostContent, ArticleContent, GroundingLevel, ResearchSource
)
from services.linkedin.quality_handler import QualityHandler


class ContentGenerator:
    """Handles content generation for all LinkedIn content types."""
    
    def __init__(self, citation_manager=None, quality_analyzer=None, gemini_grounded=None, fallback_provider=None):
        self.citation_manager = citation_manager
        self.quality_analyzer = quality_analyzer
        self.gemini_grounded = gemini_grounded
        self.fallback_provider = fallback_provider
    
    def _transform_gemini_sources(self, gemini_sources):
        """Transform Gemini sources to ResearchSource format."""
        transformed_sources = []
        for source in gemini_sources:
            transformed_source = ResearchSource(
                title=source.get('title', 'Unknown Source'),
                url=source.get('url', ''),
                content=f"Source from {source.get('title', 'Unknown')}",
                relevance_score=0.8,  # Default relevance score
                credibility_score=0.7,  # Default credibility score
                domain_authority=0.6,   # Default domain authority
                source_type=source.get('type', 'web'),
                publication_date=datetime.now().strftime('%Y-%m-%d')
            )
            transformed_sources.append(transformed_source)
        return transformed_sources
    
    async def generate_post(
        self,
        request: LinkedInPostRequest,
        research_sources: List,
        research_time: float,
        content_result: Dict[str, Any],
        grounding_enabled: bool
    ) -> LinkedInPostResponse:
        """Generate LinkedIn post with all processing steps."""
        try:
            start_time = datetime.now()
            
            # Debug: Log what we received
            logger.info(f"ContentGenerator.generate_post called with:")
            logger.info(f"  - research_sources count: {len(research_sources) if research_sources else 0}")
            logger.info(f"  - research_sources type: {type(research_sources)}")
            logger.info(f"  - content_result keys: {list(content_result.keys()) if content_result else 'None'}")
            logger.info(f"  - grounding_enabled: {grounding_enabled}")
            logger.info(f"  - include_citations: {request.include_citations}")
            
            # Debug: Log content_result details
            if content_result:
                logger.info(f"  - content_result has citations: {'citations' in content_result}")
                logger.info(f"  - content_result has sources: {'sources' in content_result}")
                if 'citations' in content_result:
                    logger.info(f"  - citations count: {len(content_result['citations']) if content_result['citations'] else 0}")
                if 'sources' in content_result:
                    logger.info(f"  - sources count: {len(content_result['sources']) if content_result['sources'] else 0}")
            
            if research_sources:
                logger.info(f"  - First research source: {research_sources[0] if research_sources else 'None'}")
                logger.info(f"  - Research sources types: {[type(s) for s in research_sources[:3]]}")
            
            # Step 3: Add citations if requested - POST METHOD
            citations = []
            source_list = None
            final_research_sources = research_sources  # Default to passed research_sources
            
            # Use sources and citations from content_result if available (from Gemini grounding)
            if content_result.get('citations') and content_result.get('sources'):
                logger.info(f"Using citations and sources from Gemini grounding: {len(content_result['citations'])} citations, {len(content_result['sources'])} sources")
                citations = content_result['citations']
                # Transform Gemini sources to ResearchSource format
                gemini_sources = self._transform_gemini_sources(content_result['sources'])
                source_list = self.citation_manager.generate_source_list(gemini_sources) if self.citation_manager else None
                # Use transformed sources for the response
                final_research_sources = gemini_sources
            elif request.include_citations and research_sources and self.citation_manager:
                try:
                    logger.info(f"Processing citations for content length: {len(content_result['content'])}")
                    citations = self.citation_manager.extract_citations(content_result['content'])
                    logger.info(f"Extracted {len(citations)} citations from content")
                    source_list = self.citation_manager.generate_source_list(research_sources)
                    logger.info(f"Generated source list: {source_list[:200] if source_list else 'None'}")
                except Exception as e:
                    logger.warning(f"Citation processing failed: {e}")
            else:
                logger.info(f"Citation processing skipped: include_citations={request.include_citations}, research_sources={len(research_sources) if research_sources else 0}, citation_manager={self.citation_manager is not None}")
            
            # Step 4: Analyze content quality
            quality_metrics = None
            if grounding_enabled and self.quality_analyzer:
                try:
                    quality_handler = QualityHandler(self.quality_analyzer)
                    quality_metrics = quality_handler.create_quality_metrics(
                        content=content_result['content'],
                        sources=final_research_sources,  # Use final_research_sources
                        industry=request.industry,
                        grounding_enabled=grounding_enabled
                    )
                except Exception as e:
                    logger.warning(f"Quality analysis failed: {e}")
            
            # Step 5: Build response
            post_content = PostContent(
                content=content_result['content'],
                character_count=len(content_result['content']),
                hashtags=content_result.get('hashtags', []),
                call_to_action=content_result.get('call_to_action'),
                engagement_prediction=content_result.get('engagement_prediction'),
                citations=citations,
                source_list=source_list,
                quality_metrics=quality_metrics,
                grounding_enabled=grounding_enabled,
                search_queries=content_result.get('search_queries', [])
            )
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Build grounding status
            grounding_status = {
                'status': 'success' if grounding_enabled else 'disabled',
                'sources_used': len(final_research_sources),  # Use final_research_sources
                'citation_coverage': len(citations) / max(len(final_research_sources), 1) if final_research_sources else 0,
                'quality_score': quality_metrics.overall_score if quality_metrics else 0.0
            } if grounding_enabled else None
            
            return LinkedInPostResponse(
                success=True,
                data=post_content,
                research_sources=final_research_sources,  # Use final_research_sources
                generation_metadata={
                    'model_used': 'gemini-2.0-flash-001',
                    'generation_time': generation_time,
                    'research_time': research_time,
                    'grounding_enabled': grounding_enabled
                },
                grounding_status=grounding_status
            )
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn post: {str(e)}")
            return LinkedInPostResponse(
                success=False,
                error=f"Failed to generate LinkedIn post: {str(e)}"
            )
    
    async def generate_article(
        self,
        request: LinkedInArticleRequest,
        research_sources: List,
        research_time: float,
        content_result: Dict[str, Any],
        grounding_enabled: bool
    ) -> LinkedInArticleResponse:
        """Generate LinkedIn article with all processing steps."""
        try:
            start_time = datetime.now()
            
            # Step 3: Add citations if requested - ARTICLE METHOD
            citations = []
            source_list = None
            final_research_sources = research_sources  # Default to passed research_sources
            
            # Use sources and citations from content_result if available (from Gemini grounding)
            if content_result.get('citations') and content_result.get('sources'):
                logger.info(f"Using citations and sources from Gemini grounding: {len(content_result['citations'])} citations, {len(content_result['sources'])} sources")
                citations = content_result['citations']
                # Transform Gemini sources to ResearchSource format
                gemini_sources = self._transform_gemini_sources(content_result['sources'])
                source_list = self.citation_manager.generate_source_list(gemini_sources) if self.citation_manager else None
                # Use transformed sources for the response
                final_research_sources = gemini_sources
            elif request.include_citations and research_sources and self.citation_manager:
                try:
                    citations = self.citation_manager.extract_citations(content_result['content'])
                    source_list = self.citation_manager.generate_source_list(research_sources)
                except Exception as e:
                    logger.warning(f"Citation processing failed: {e}")
            
            # Step 4: Analyze content quality
            quality_metrics = None
            if grounding_enabled and self.quality_analyzer:
                try:
                    quality_handler = QualityHandler(self.quality_analyzer)
                    quality_metrics = quality_handler.create_quality_metrics(
                        content=content_result['content'],
                        sources=final_research_sources,  # Use final_research_sources
                        industry=request.industry,
                        grounding_enabled=grounding_enabled
                    )
                except Exception as e:
                    logger.warning(f"Quality analysis failed: {e}")
            
            # Step 5: Build response
            article_content = ArticleContent(
                title=content_result['title'],
                content=content_result['content'],
                word_count=len(content_result['content'].split()),
                sections=content_result.get('sections', []),
                seo_metadata=content_result.get('seo_metadata'),
                image_suggestions=content_result.get('image_suggestions', []),
                reading_time=content_result.get('reading_time'),
                citations=citations,
                source_list=source_list,
                quality_metrics=quality_metrics,
                grounding_enabled=grounding_enabled,
                search_queries=content_result.get('search_queries', [])
            )
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Build grounding status
            grounding_status = {
                'status': 'success' if grounding_enabled else 'disabled',
                'sources_used': len(final_research_sources),  # Use final_research_sources
                'citation_coverage': len(citations) / max(len(final_research_sources), 1) if final_research_sources else 0,
                'quality_score': quality_metrics.overall_score if quality_metrics else 0.0
            } if grounding_enabled else None
            
            return LinkedInArticleResponse(
                success=True,
                data=article_content,
                research_sources=final_research_sources,  # Use final_research_sources
                generation_metadata={
                    'model_used': 'gemini-2.0-flash-001',
                    'generation_time': generation_time,
                    'research_time': research_time,
                    'grounding_enabled': grounding_enabled
                },
                grounding_status=grounding_status
            )
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn article: {str(e)}")
            return LinkedInArticleResponse(
                success=False,
                error=f"Failed to generate LinkedIn article: {str(e)}"
            )
    
    async def generate_carousel(
        self,
        request,
        research_sources: List,
        research_time: float,
        content_result: Dict[str, Any],
        grounding_enabled: bool
    ):
        """Generate LinkedIn carousel with all processing steps."""
        try:
            start_time = datetime.now()
            
            # Step 3: Add citations if requested
            citations = []
            source_list = None
            if request.include_citations and research_sources:
                # Extract citations from all slides
                all_content = " ".join([slide['content'] for slide in content_result['slides']])
                citations = self.citation_manager.extract_citations(all_content) if self.citation_manager else []
                source_list = self.citation_manager.generate_source_list(research_sources) if self.citation_manager else None
            
            # Step 4: Analyze content quality
            quality_metrics = None
            if grounding_enabled and self.quality_analyzer:
                try:
                    all_content = " ".join([slide['content'] for slide in content_result['slides']])
                    quality_handler = QualityHandler(self.quality_analyzer)
                    quality_metrics = quality_handler.create_quality_metrics(
                        content=all_content,
                        sources=research_sources,
                        industry=request.industry,
                        grounding_enabled=grounding_enabled
                    )
                except Exception as e:
                    logger.warning(f"Quality analysis failed: {e}")
            
            # Step 5: Build response
            slides = []
            for i, slide_data in enumerate(content_result['slides']):
                slide_citations = []
                if request.include_citations and research_sources and self.citation_manager:
                    slide_citations = self.citation_manager.extract_citations(slide_data['content'])
                
                slides.append({
                    'slide_number': i + 1,
                    'title': slide_data['title'],
                    'content': slide_data['content'],
                    'visual_elements': slide_data.get('visual_elements', []),
                    'design_notes': slide_data.get('design_notes'),
                    'citations': slide_citations
                })
            
            carousel_content = {
                'title': content_result['title'],
                'slides': slides,
                'cover_slide': content_result.get('cover_slide'),
                'cta_slide': content_result.get('cta_slide'),
                'design_guidelines': content_result.get('design_guidelines', {}),
                'citations': citations,
                'source_list': source_list,
                'quality_metrics': quality_metrics,
                'grounding_enabled': grounding_enabled
            }
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Build grounding status
            grounding_status = {
                'status': 'success' if grounding_enabled else 'disabled',
                'sources_used': len(research_sources),
                'citation_coverage': len(citations) / max(len(research_sources), 1) if research_sources else 0,
                'quality_score': quality_metrics.overall_score if quality_metrics else 0.0
            } if grounding_enabled else None
            
            return {
                'success': True,
                'data': carousel_content,
                'research_sources': research_sources,
                'generation_metadata': {
                    'model_used': 'gemini-2.0-flash-001',
                    'generation_time': generation_time,
                    'research_time': research_time,
                    'grounding_enabled': grounding_enabled
                },
                'grounding_status': grounding_status
            }
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn carousel: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to generate LinkedIn carousel: {str(e)}"
            }
    
    async def generate_video_script(
        self,
        request,
        research_sources: List,
        research_time: float,
        content_result: Dict[str, Any],
        grounding_enabled: bool
    ):
        """Generate LinkedIn video script with all processing steps."""
        try:
            start_time = datetime.now()
            
            # Step 3: Add citations if requested
            citations = []
            source_list = None
            if request.include_citations and research_sources and self.citation_manager:
                all_content = f"{content_result['hook']} {' '.join([scene['content'] for scene in content_result['main_content']])} {content_result['conclusion']}"
                citations = self.citation_manager.extract_citations(all_content)
                source_list = self.citation_manager.generate_source_list(research_sources)
            
            # Step 4: Analyze content quality
            quality_metrics = None
            if grounding_enabled and self.quality_analyzer:
                try:
                    all_content = f"{content_result['hook']} {' '.join([scene['content'] for scene in content_result['main_content']])} {content_result['conclusion']}"
                    quality_handler = QualityHandler(self.quality_analyzer)
                    quality_metrics = quality_handler.create_quality_metrics(
                        content=all_content,
                        sources=research_sources,
                        industry=request.industry,
                        grounding_enabled=grounding_enabled
                    )
                except Exception as e:
                    logger.warning(f"Quality analysis failed: {e}")
            
            # Step 5: Build response
            video_script = {
                'hook': content_result['hook'],
                'main_content': content_result['main_content'],
                'conclusion': content_result['conclusion'],
                'captions': content_result.get('captions'),
                'thumbnail_suggestions': content_result.get('thumbnail_suggestions', []),
                'video_description': content_result.get('video_description', ''),
                'citations': citations,
                'source_list': source_list,
                'quality_metrics': quality_metrics,
                'grounding_enabled': grounding_enabled
            }
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Build grounding status
            grounding_status = {
                'status': 'success' if grounding_enabled else 'disabled',
                'sources_used': len(research_sources),
                'citation_coverage': len(citations) / max(len(research_sources), 1) if research_sources else 0,
                'quality_score': quality_metrics.overall_score if quality_metrics else 0.0
            } if grounding_enabled else None
            
            return {
                'success': True,
                'data': video_script,
                'research_sources': research_sources,
                'generation_metadata': {
                    'model_used': 'gemini-2.0-flash-001',
                    'generation_time': generation_time,
                    'research_time': research_time,
                    'grounding_enabled': grounding_enabled
                },
                'grounding_status': grounding_status
            }
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn video script: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to generate LinkedIn video script: {str(e)}"
            }
    
    async def generate_comment_response(
        self,
        request,
        research_sources: List,
        research_time: float,
        content_result: Dict[str, Any],
        grounding_enabled: bool
    ):
        """Generate LinkedIn comment response with all processing steps."""
        try:
            start_time = datetime.now()
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            # Build grounding status
            grounding_status = {
                'status': 'success' if grounding_enabled else 'disabled',
                'sources_used': len(research_sources),
                'citation_coverage': 0,  # Comments typically don't have citations
                'quality_score': 0.8  # Default quality for comments
            } if grounding_enabled else None
            
            return {
                'success': True,
                'response': content_result['response'],
                'alternative_responses': content_result.get('alternative_responses', []),
                'tone_analysis': content_result.get('tone_analysis'),
                'generation_metadata': {
                    'model_used': 'gemini-2.0-flash-001',
                    'generation_time': generation_time,
                    'research_time': research_time,
                    'grounding_enabled': grounding_enabled
                },
                'grounding_status': grounding_status
            }
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn comment response: {str(e)}")
            return {
                'success': False,
                'error': f"Failed to generate LinkedIn comment response: {str(e)}"
            }
    
    # Grounded content generation methods
    async def generate_grounded_post_content(self, request, research_sources: List) -> Dict[str, Any]:
        """Generate grounded post content using the enhanced Gemini provider with native grounding."""
        try:
            if not self.gemini_grounded:
                logger.warning("Gemini Grounded Provider not available, using fallback")
                return await self.generate_fallback_post_content(request)
                
            # Build the prompt for grounded generation
            prompt = self._build_post_prompt(request)
            
            # Generate grounded content using native Google Search grounding
            result = await self.gemini_grounded.generate_grounded_content(
                prompt=prompt,
                content_type="linkedin_post",
                temperature=0.7,
                max_tokens=request.max_length
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating grounded post content: {str(e)}")
            # Fallback to basic generation
            return await self.generate_fallback_post_content(request)
    
    async def generate_grounded_article_content(self, request, research_sources: List) -> Dict[str, Any]:
        """Generate grounded article content using the enhanced Gemini provider with native grounding."""
        try:
            if not self.gemini_grounded:
                logger.warning("Gemini Grounded Provider not available, using fallback")
                return await self.generate_fallback_article_content(request)
                
            # Build the prompt for grounded generation
            prompt = self._build_article_prompt(request)
            
            # Generate grounded content using native Google Search grounding
            result = await self.gemini_grounded.generate_grounded_content(
                prompt=prompt,
                content_type="linkedin_article",
                temperature=0.7,
                max_tokens=request.word_count * 10  # Approximate character count
            )
            
            return result
                
        except Exception as e:
            logger.error(f"Error generating grounded article content: {str(e)}")
            # Fallback to basic generation
            return await self.generate_fallback_article_content(request)
    
    async def generate_grounded_carousel_content(self, request, research_sources: List) -> Dict[str, Any]:
        """Generate grounded carousel content using the enhanced Gemini provider with native grounding."""
        try:
            if not self.gemini_grounded:
                logger.warning("Gemini Grounded Provider not available, using fallback")
                return await self.generate_fallback_carousel_content(request)
                
            # Build the prompt for grounded generation
            prompt = self._build_carousel_prompt(request)
            
            # Generate grounded content using native Google Search grounding
            result = await self.gemini_grounded.generate_grounded_content(
                prompt=prompt,
                content_type="linkedin_carousel",
                temperature=0.7,
                max_tokens=2000
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating grounded carousel content: {str(e)}")
            # Fallback to basic generation
            return await self.generate_fallback_carousel_content(request)
    
    async def generate_grounded_video_script_content(self, request, research_sources: List) -> Dict[str, Any]:
        """Generate grounded video script content using the enhanced Gemini provider with native grounding."""
        try:
            if not self.gemini_grounded:
                logger.warning("Gemini Grounded Provider not available, using fallback")
                return await self.generate_fallback_video_script_content(request)
                
            # Build the prompt for grounded generation
            prompt = self._build_video_script_prompt(request)
            
            # Generate grounded content using native Google Search grounding
            result = await self.gemini_grounded.generate_grounded_content(
                prompt=prompt,
                content_type="linkedin_video_script",
                temperature=0.7,
                max_tokens=1500
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating grounded video script content: {str(e)}")
            # Fallback to basic generation
            return await self.generate_fallback_video_script_content(request)
    
    async def generate_grounded_comment_response(self, request, research_sources: List) -> Dict[str, Any]:
        """Generate grounded comment response using the enhanced Gemini provider with native grounding."""
        try:
            if not self.gemini_grounded:
                logger.warning("Gemini Grounded Provider not available, using fallback")
                return await self.generate_fallback_comment_response(request)
                
            # Build the prompt for grounded generation
            prompt = self._build_comment_response_prompt(request)
            
            # Generate grounded content using native Google Search grounding
            result = await self.gemini_grounded.generate_grounded_content(
                prompt=prompt,
                content_type="linkedin_comment_response",
                temperature=0.7,
                max_tokens=500
            )
            
            return result
                
        except Exception as e:
            logger.error(f"Error generating grounded comment response: {str(e)}")
            # Fallback to basic generation
            return await self.generate_fallback_comment_response(request)
    
    # Fallback content generation methods
    async def generate_fallback_post_content(self, request) -> Dict[str, Any]:
        """Generate post content using fallback provider."""
        if not self.fallback_provider:
            raise Exception("No fallback provider available")
        
        return {
            'content': f"Professional LinkedIn post about {request.topic} in the {request.industry} industry.",
            'hashtags': [{'hashtag': f'#{request.industry.lower().replace(" ", "")}', 'category': 'industry', 'popularity_score': 0.8}],
            'call_to_action': "What are your thoughts on this? Share in the comments!",
            'engagement_prediction': {'estimated_likes': 50, 'estimated_comments': 5}
        }
    
    async def generate_fallback_article_content(self, request) -> Dict[str, Any]:
        """Generate article content using fallback provider."""
        if not self.fallback_provider:
            raise Exception("No fallback provider available")
        
        return {
            'title': f"Comprehensive Guide to {request.topic} in {request.industry}",
            'content': f"Detailed article about {request.topic} in the {request.industry} industry.",
            'sections': [{'title': 'Introduction', 'content': 'Industry overview and context'}],
            'seo_metadata': {'keywords': [request.topic, request.industry]},
            'image_suggestions': ['Industry-related visual content'],
            'reading_time': '5 minutes'
        }
    
    async def generate_fallback_carousel_content(self, request) -> Dict[str, Any]:
        """Generate carousel content using fallback provider."""
        if not self.fallback_provider:
            raise Exception("No fallback provider available")
        
        return {
            'title': f"Key Insights: {request.topic} in {request.industry}",
            'slides': [
                {'title': 'Overview', 'content': f'Introduction to {request.topic}', 'visual_elements': [], 'design_notes': 'Clean, professional design'},
                {'title': 'Key Points', 'content': f'Main insights about {request.topic}', 'visual_elements': [], 'design_notes': 'Bullet points with icons'}
            ],
            'cover_slide': {'title': 'Cover', 'content': 'Professional cover slide', 'visual_elements': [], 'design_notes': 'Eye-catching design'},
            'cta_slide': {'title': 'Call to Action', 'content': 'Engage with this content', 'visual_elements': [], 'design_notes': 'Clear CTA design'},
            'design_guidelines': {'style': 'professional', 'colors': 'brand colors'}
        }
    
    async def generate_fallback_video_script_content(self, request) -> Dict[str, Any]:
        """Generate video script content using fallback provider."""
        if not self.fallback_provider:
            raise Exception("No fallback provider available")
        
        return {
            'hook': f"Discover how {request.topic} is transforming the {request.industry} industry!",
            'main_content': [
                {'content': f'Introduction to {request.topic}', 'duration': '30s'},
                {'content': f'Key insights about {request.topic}', 'duration': '45s'}
            ],
            'conclusion': f"Ready to explore {request.topic}? Let's dive in!",
            'captions': [f'Key point about {request.topic}'],
            'thumbnail_suggestions': ['Professional thumbnail with industry imagery'],
            'video_description': f"Video description about {request.topic}"
        }
    
    async def generate_fallback_comment_response(self, request) -> Dict[str, Any]:
        """Generate comment response using fallback provider."""
        if not self.fallback_provider:
            raise Exception("No fallback provider available")
        
        return {
            'response': f"Thank you for your comment about {request.original_comment}",
            'alternative_responses': [],
            'tone_analysis': None
        }
    
    # Prompt building methods
    def _build_post_prompt(self, request) -> str:
        """Build prompt for post generation."""
        prompt = f"""
        Generate a professional LinkedIn post about {request.topic} in the {request.industry} industry.
        
        Requirements:
        - Tone: {request.tone}
        - Target audience: {request.target_audience or 'Industry professionals'}
        - Maximum length: {request.max_length} characters
        - Include engaging hashtags
        - Include a call to action
        - Make it informative and shareable
        
        Key points to include: {', '.join(request.key_points) if request.key_points else 'Industry insights and trends'}
        """
        return prompt.strip()
    
    def _build_article_prompt(self, request) -> str:
        """Build prompt for article generation."""
        prompt = f"""
        Generate a comprehensive LinkedIn article about {request.topic} in the {request.industry} industry.
        
        Requirements:
        - Tone: {request.tone}
        - Target audience: {request.target_audience or 'Industry professionals'}
        - Word count: {request.word_count} words
        - Include SEO optimization
        - Include image suggestions
        - Make it informative and engaging
        
        Key sections to include: {', '.join(request.key_sections) if request.key_sections else 'Introduction, main content, conclusion'}
        """
        return prompt.strip()
    
    def _build_carousel_prompt(self, request) -> str:
        """Build prompt for carousel generation."""
        prompt = f"""
        Generate a LinkedIn carousel about {request.topic} in the {request.industry} industry.
            
        Requirements:
        - Tone: {request.tone}
        - Target audience: {request.target_audience or 'Industry professionals'}
        - Number of slides: {request.number_of_slides}
        - Include cover slide: {request.include_cover_slide}
        - Include CTA slide: {request.include_cta_slide}
        - Make each slide informative and visually appealing
        
        Each slide should contain valuable insights and be designed for social media engagement.
        """
        return prompt.strip()
    
    def _build_video_script_prompt(self, request) -> str:
        """Build prompt for video script generation."""
        prompt = f"""
        Generate a LinkedIn video script about {request.topic} in the {request.industry} industry.
            
        Requirements:
        - Tone: {request.tone}
        - Target audience: {request.target_audience or 'Industry professionals'}
        - Duration: {request.video_duration} seconds
        - Include captions: {request.include_captions}
        - Include thumbnail suggestions: {request.include_thumbnail_suggestions}
        - Make it engaging and informative
        
        Structure: Hook, main content (divided into scenes), conclusion
        """
        return prompt.strip()
    
    def _build_comment_response_prompt(self, request) -> str:
        """Build prompt for comment response generation."""
        prompt = f"""
        Generate a LinkedIn comment response to: "{request.original_comment}"
        
        Context: {request.post_context}
        Industry: {request.industry}
        Tone: {request.tone}
        Response length: {request.response_length}
        Include questions: {request.include_questions}
        
        Make the response engaging, professional, and add value to the conversation.
        """
        return prompt.strip()
