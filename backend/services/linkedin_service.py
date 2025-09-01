"""
LinkedIn Content Generation Service

This service provides comprehensive LinkedIn content generation functionality,
migrated from the legacy Streamlit implementation to FastAPI with improved
error handling, logging, and integration with the existing backend services.
"""

import json
import time
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from loguru import logger
import traceback

from models.linkedin_models import (
    LinkedInPostRequest, LinkedInArticleRequest, LinkedInCarouselRequest,
    LinkedInVideoScriptRequest, LinkedInCommentResponseRequest,
    LinkedInPostResponse, LinkedInArticleResponse, LinkedInCarouselResponse,
    LinkedInVideoScriptResponse, LinkedInCommentResponseResult,
    PostContent, ArticleContent, CarouselContent, VideoScript,
    ResearchSource, HashtagSuggestion, ImageSuggestion, CarouselSlide
)

from services.llm_providers.main_text_generation import llm_text_gen
from services.llm_providers.gemini_provider import gemini_structured_json_response, gemini_text_response


class LinkedInContentService:
    """
    Service class for generating LinkedIn content using AI.
    
    This service provides methods for:
    - Generating LinkedIn posts with research
    - Creating LinkedIn articles with SEO optimization
    - Generating carousel posts
    - Creating video scripts
    - Generating comment responses
    """
    
    def __init__(self):
        """Initialize the LinkedIn Content Service."""
        self.generation_metadata = {
            "service_version": "1.0.0",
            "model_provider": "gemini",
            "model_version": "gemini-2.0-flash-001"
        }
        logger.info("LinkedInContentService initialized")
    
    async def generate_post(self, request: LinkedInPostRequest) -> LinkedInPostResponse:
        """
        Generate a LinkedIn post based on the request parameters.
        
        Args:
            request: LinkedInPostRequest containing post generation parameters
            
        Returns:
            LinkedInPostResponse with generated content and metadata
        """
        start_time = time.time()
        logger.info(f"Starting LinkedIn post generation for topic: {request.topic}")
        
        try:
            # Initialize response
            response = LinkedInPostResponse(
                success=True,
                research_sources=[],
                generation_metadata=self.generation_metadata.copy()
            )
            
            # Step 1: Research if enabled
            research_data = {}
            if request.research_enabled:
                logger.info(f"Conducting research using {request.search_engine}")
                research_data = await self._conduct_research(
                    topic=request.topic,
                    industry=request.industry,
                    search_engine=request.search_engine
                )
                
                # Add research sources to response
                if research_data.get("sources"):
                    response.research_sources = [
                        ResearchSource(
                            title=source.get("title", ""),
                            url=source.get("url", ""),
                            content=source.get("content", "")[:500] + "...",  # Truncate for response
                            relevance_score=source.get("relevance_score")
                        )
                        for source in research_data.get("sources", [])[:5]  # Limit to top 5
                    ]
            
            # Step 2: Generate post content
            logger.info("Generating post content")
            post_content = await self._generate_post_content(request, research_data)
            
            # Step 3: Generate hashtags if requested
            hashtags = []
            if request.include_hashtags:
                logger.info("Generating hashtags")
                hashtags = await self._generate_hashtags(request.topic, request.industry)
            
            # Step 4: Generate call-to-action if requested
            call_to_action = None
            if request.include_call_to_action:
                logger.info("Generating call-to-action")
                call_to_action = await self._generate_call_to_action(request)
            
            # Step 5: Predict engagement (simplified)
            engagement_prediction = await self._predict_engagement(post_content, hashtags)
            
            # Assemble final content
            response.data = PostContent(
                content=post_content,
                character_count=len(post_content),
                hashtags=hashtags,
                call_to_action=call_to_action,
                engagement_prediction=engagement_prediction
            )
            
            # Update generation metadata
            generation_time = time.time() - start_time
            response.generation_metadata.update({
                "generation_time": round(generation_time, 2),
                "timestamp": datetime.utcnow().isoformat(),
                "request_parameters": request.dict()
            })
            
            logger.info(f"Post generation completed in {generation_time:.2f} seconds")
            return response
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn post: {str(e)}")
            logger.error(traceback.format_exc())
            return LinkedInPostResponse(
                success=False,
                error=f"Post generation failed: {str(e)}",
                generation_metadata=self.generation_metadata.copy()
            )
    
    async def generate_article(self, request: LinkedInArticleRequest) -> LinkedInArticleResponse:
        """
        Generate a LinkedIn article based on the request parameters.
        
        Args:
            request: LinkedInArticleRequest containing article generation parameters
            
        Returns:
            LinkedInArticleResponse with generated content and metadata
        """
        start_time = time.time()
        logger.info(f"Starting LinkedIn article generation for topic: {request.topic}")
        
        try:
            # Initialize response
            response = LinkedInArticleResponse(
                success=True,
                research_sources=[],
                generation_metadata=self.generation_metadata.copy()
            )
            
            # Step 1: Research if enabled
            research_data = {}
            if request.research_enabled:
                logger.info(f"Conducting research using {request.search_engine}")
                research_data = await self._conduct_research(
                    topic=request.topic,
                    industry=request.industry,
                    search_engine=request.search_engine
                )
                
                # Add research sources to response
                if research_data.get("sources"):
                    response.research_sources = [
                        ResearchSource(
                            title=source.get("title", ""),
                            url=source.get("url", ""),
                            content=source.get("content", "")[:500] + "...",
                            relevance_score=source.get("relevance_score")
                        )
                        for source in research_data.get("sources", [])[:10]
                    ]
            
            # Step 2: Generate article outline
            logger.info("Generating article outline")
            outline = await self._generate_article_outline(request, research_data)
            
            # Step 3: Generate article content
            logger.info("Generating article content")
            article_content = await self._generate_article_content(request, outline, research_data)
            
            # Step 4: Generate SEO metadata if requested
            seo_metadata = None
            if request.seo_optimization:
                logger.info("Generating SEO metadata")
                seo_metadata = await self._generate_seo_metadata(request, article_content)
            
            # Step 5: Generate image suggestions if requested
            image_suggestions = []
            if request.include_images:
                logger.info("Generating image suggestions")
                image_suggestions = await self._generate_image_suggestions(request, outline)
            
            # Step 6: Calculate reading time
            reading_time = self._calculate_reading_time(article_content.get("content", ""))
            
            # Assemble final content
            response.data = ArticleContent(
                title=article_content.get("title", ""),
                content=article_content.get("content", ""),
                word_count=len(article_content.get("content", "").split()),
                sections=article_content.get("sections", []),
                seo_metadata=seo_metadata,
                image_suggestions=image_suggestions,
                reading_time=reading_time
            )
            
            # Update generation metadata
            generation_time = time.time() - start_time
            response.generation_metadata.update({
                "generation_time": round(generation_time, 2),
                "timestamp": datetime.utcnow().isoformat(),
                "request_parameters": request.dict()
            })
            
            logger.info(f"Article generation completed in {generation_time:.2f} seconds")
            return response
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn article: {str(e)}")
            logger.error(traceback.format_exc())
            return LinkedInArticleResponse(
                success=False,
                error=f"Article generation failed: {str(e)}",
                generation_metadata=self.generation_metadata.copy()
            )
    
    async def generate_carousel(self, request: LinkedInCarouselRequest) -> LinkedInCarouselResponse:
        """
        Generate a LinkedIn carousel post based on the request parameters.
        
        Args:
            request: LinkedInCarouselRequest containing carousel generation parameters
            
        Returns:
            LinkedInCarouselResponse with generated content and metadata
        """
        start_time = time.time()
        logger.info(f"Starting LinkedIn carousel generation for topic: {request.topic}")
        
        try:
            # Generate carousel content
            carousel_data = await self._generate_carousel_content(request)
            
            # Assemble final content
            response = LinkedInCarouselResponse(
                success=True,
                data=carousel_data,
                generation_metadata=self.generation_metadata.copy()
            )
            
            # Update generation metadata
            generation_time = time.time() - start_time
            response.generation_metadata.update({
                "generation_time": round(generation_time, 2),
                "timestamp": datetime.utcnow().isoformat(),
                "request_parameters": request.dict()
            })
            
            logger.info(f"Carousel generation completed in {generation_time:.2f} seconds")
            return response
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn carousel: {str(e)}")
            logger.error(traceback.format_exc())
            return LinkedInCarouselResponse(
                success=False,
                error=f"Carousel generation failed: {str(e)}",
                generation_metadata=self.generation_metadata.copy()
            )
    
    async def generate_video_script(self, request: LinkedInVideoScriptRequest) -> LinkedInVideoScriptResponse:
        """
        Generate a LinkedIn video script based on the request parameters.
        
        Args:
            request: LinkedInVideoScriptRequest containing video script generation parameters
            
        Returns:
            LinkedInVideoScriptResponse with generated content and metadata
        """
        start_time = time.time()
        logger.info(f"Starting LinkedIn video script generation for topic: {request.topic}")
        
        try:
            # Generate video script
            script_data = await self._generate_video_script_content(request)
            
            # Assemble final content
            response = LinkedInVideoScriptResponse(
                success=True,
                data=script_data,
                generation_metadata=self.generation_metadata.copy()
            )
            
            # Update generation metadata
            generation_time = time.time() - start_time
            response.generation_metadata.update({
                "generation_time": round(generation_time, 2),
                "timestamp": datetime.utcnow().isoformat(),
                "request_parameters": request.dict()
            })
            
            logger.info(f"Video script generation completed in {generation_time:.2f} seconds")
            return response
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn video script: {str(e)}")
            logger.error(traceback.format_exc())
            return LinkedInVideoScriptResponse(
                success=False,
                error=f"Video script generation failed: {str(e)}",
                generation_metadata=self.generation_metadata.copy()
            )
    
    async def generate_comment_response(self, request: LinkedInCommentResponseRequest) -> LinkedInCommentResponseResult:
        """
        Generate a LinkedIn comment response based on the request parameters.
        
        Args:
            request: LinkedInCommentResponseRequest containing comment response generation parameters
            
        Returns:
            LinkedInCommentResponseResult with generated response and metadata
        """
        start_time = time.time()
        logger.info(f"Starting LinkedIn comment response generation")
        
        try:
            # Generate comment response
            response_data = await self._generate_comment_response_content(request)
            
            # Assemble final content
            response = LinkedInCommentResponseResult(
                success=True,
                response=response_data.get("primary_response"),
                alternative_responses=response_data.get("alternative_responses", []),
                tone_analysis=response_data.get("tone_analysis"),
                generation_metadata=self.generation_metadata.copy()
            )
            
            # Update generation metadata
            generation_time = time.time() - start_time
            response.generation_metadata.update({
                "generation_time": round(generation_time, 2),
                "timestamp": datetime.utcnow().isoformat(),
                "request_parameters": request.dict()
            })
            
            logger.info(f"Comment response generation completed in {generation_time:.2f} seconds")
            return response
            
        except Exception as e:
            logger.error(f"Error generating LinkedIn comment response: {str(e)}")
            logger.error(traceback.format_exc())
            return LinkedInCommentResponseResult(
                success=False,
                error=f"Comment response generation failed: {str(e)}",
                generation_metadata=self.generation_metadata.copy()
            )
    
    # Private helper methods
    
    async def _conduct_research(self, topic: str, industry: str, search_engine: str) -> Dict:
        """
        Conduct research using the specified search engine.
        
        Note: This is a simplified version. In production, you would integrate
        with actual search APIs (Metaphor, Google, Tavily).
        """
        try:
            # Simulate research results for now
            # In production, this would call actual search APIs
            logger.info(f"Simulating research for {topic} in {industry} using {search_engine}")
            
            # Mock research data
            research_data = {
                "sources": [
                    {
                        "title": f"Latest trends in {topic} for {industry}",
                        "url": f"https://example.com/{topic.lower().replace(' ', '-')}",
                        "content": f"Recent developments in {topic} show significant impact on {industry} sector...",
                        "relevance_score": 0.9
                    },
                    {
                        "title": f"Industry analysis: {topic} in {industry}",
                        "url": f"https://example.com/analysis-{topic.lower().replace(' ', '-')}",
                        "content": f"Expert analysis reveals key insights about {topic} implementation...",
                        "relevance_score": 0.8
                    }
                ],
                "key_insights": [
                    f"{topic} is transforming {industry} operations",
                    f"Industry leaders are investing heavily in {topic}",
                    f"Expected growth in {topic} adoption within {industry}"
                ],
                "statistics": [
                    f"85% of {industry} companies are exploring {topic}",
                    f"Investment in {topic} increased by 40% this year"
                ]
            }
            
            return research_data
            
        except Exception as e:
            logger.error(f"Error in research: {str(e)}")
            return {"sources": [], "key_insights": [], "statistics": []}
    
    async def _generate_post_content(self, request: LinkedInPostRequest, research_data: Dict) -> str:
        """Generate the main post content."""
        try:
            # Prepare research context
            research_context = ""
            if research_data.get("sources"):
                research_context = f"""
                Research insights:
                - Key insights: {', '.join(research_data.get('key_insights', []))}
                - Statistics: {', '.join(research_data.get('statistics', []))}
                """
            
            # Prepare key points
            key_points_text = ""
            if request.key_points:
                key_points_text = f"Key points to include: {', '.join(request.key_points)}"
            
            # Construct prompt
            prompt = f"""
            Create an engaging LinkedIn post about "{request.topic}" for the {request.industry} industry.
            
            Requirements:
            - Post type: {request.post_type.value}
            - Tone: {request.tone.value}
            - Target audience: {request.target_audience or 'Professionals in ' + request.industry}
            - Maximum length: {request.max_length} characters
            
            {key_points_text}
            {research_context}
            
            Guidelines:
            - Start with an attention-grabbing hook
            - Include relevant insights and data
            - Make it engaging and professional
            - Use line breaks for readability
            - Don't include hashtags (they will be added separately)
            - End with an engaging question or statement that encourages interaction
            
            Write a compelling LinkedIn post that will resonate with the target audience.
            """
            
            # Generate content using LLM
            content = llm_text_gen(prompt)
            
            # Ensure content doesn't exceed max length
            if len(content) > request.max_length:
                # Truncate and add ellipsis
                content = content[:request.max_length-3] + "..."
            
            return content.strip()
            
        except Exception as e:
            logger.error(f"Error generating post content: {str(e)}")
            return f"Error generating content for {request.topic}. Please try again."
    
    async def _generate_hashtags(self, topic: str, industry: str) -> List[HashtagSuggestion]:
        """Generate relevant hashtags for the post."""
        try:
            prompt = f"""
            Generate 8-12 relevant LinkedIn hashtags for a post about "{topic}" in the {industry} industry.
            
            Include:
            - Industry-specific hashtags
            - Topic-related hashtags
            - General professional hashtags
            - Trending hashtags when relevant
            
            Return as a JSON array with format:
            [
                {{"hashtag": "#ExampleHashtag", "category": "industry", "popularity_score": 0.8}},
                ...
            ]
            
            Categories can be: "industry", "topic", "general", "trending"
            Popularity score is 0.0 to 1.0 (estimated popularity)
            """
            
            hashtag_schema = {
                "type": "object",
                "properties": {
                    "hashtags": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "hashtag": {"type": "string"},
                                "category": {"type": "string"},
                                "popularity_score": {"type": "number"}
                            }
                        }
                    }
                }
            }
            
            # Generate structured response
            response = gemini_structured_json_response(
                prompt=prompt,
                json_schema=hashtag_schema,
                temperature=0.3,
                max_tokens=1000
            )
            
            if response and response.get("hashtags"):
                return [
                    HashtagSuggestion(
                        hashtag=h.get("hashtag", ""),
                        category=h.get("category", "general"),
                        popularity_score=h.get("popularity_score", 0.5)
                    )
                    for h in response["hashtags"]
                ]
            else:
                # Fallback hashtags
                return [
                    HashtagSuggestion(hashtag=f"#{industry.replace(' ', '')}", category="industry", popularity_score=0.8),
                    HashtagSuggestion(hashtag=f"#{topic.replace(' ', '')}", category="topic", popularity_score=0.7),
                    HashtagSuggestion(hashtag="#LinkedIn", category="general", popularity_score=0.9),
                    HashtagSuggestion(hashtag="#Professional", category="general", popularity_score=0.6)
                ]
                
        except Exception as e:
            logger.error(f"Error generating hashtags: {str(e)}")
            return [
                HashtagSuggestion(hashtag=f"#{industry.replace(' ', '')}", category="industry", popularity_score=0.8),
                HashtagSuggestion(hashtag="#LinkedIn", category="general", popularity_score=0.9)
            ]
    
    async def _generate_call_to_action(self, request: LinkedInPostRequest) -> str:
        """Generate a call-to-action for the post."""
        try:
            prompt = f"""
            Create an engaging call-to-action for a LinkedIn post about "{request.topic}" in the {request.industry} industry.
            
            The CTA should:
            - Encourage engagement (comments, shares, likes)
            - Be relevant to the topic and audience
            - Be professional yet conversational
            - Prompt specific actions or responses
            
            Examples:
            - Ask a thought-provoking question
            - Request experiences or opinions
            - Invite discussion or debate
            - Suggest sharing or tagging others
            
            Keep it concise (1-2 sentences).
            """
            
            cta = llm_text_gen(prompt)
            return cta.strip()
            
        except Exception as e:
            logger.error(f"Error generating call-to-action: {str(e)}")
            return "What are your thoughts on this topic? Share your experience in the comments!"
    
    async def _predict_engagement(self, content: str, hashtags: List[HashtagSuggestion]) -> Dict[str, Any]:
        """Predict engagement metrics for the post (simplified)."""
        try:
            # Simple engagement prediction based on content characteristics
            content_length = len(content)
            hashtag_count = len(hashtags)
            
            # Base engagement (simplified algorithm)
            base_likes = max(20, min(200, content_length // 10))
            base_comments = max(2, min(25, content_length // 100))
            base_shares = max(1, min(15, content_length // 150))
            
            # Hashtag boost
            hashtag_boost = min(1.5, 1.0 + (hashtag_count * 0.05))
            
            return {
                "estimated_likes": int(base_likes * hashtag_boost),
                "estimated_comments": int(base_comments * hashtag_boost),
                "estimated_shares": int(base_shares * hashtag_boost),
                "engagement_score": round((base_likes + base_comments * 5 + base_shares * 10) * hashtag_boost, 1)
            }
            
        except Exception as e:
            logger.error(f"Error predicting engagement: {str(e)}")
            return {"estimated_likes": 50, "estimated_comments": 5, "estimated_shares": 2}
    
    # Additional helper methods for article, carousel, video, and comment generation
    # These would be implemented similarly with proper error handling and logging
    
    async def _generate_article_outline(self, request: LinkedInArticleRequest, research_data: Dict) -> Dict:
        """Generate article outline based on research."""
        try:
            # Prepare research context
            research_context = ""
            if research_data.get("sources"):
                research_context = f"""
                Research insights:
                - Key insights: {', '.join(research_data.get('key_insights', []))}
                - Statistics: {', '.join(research_data.get('statistics', []))}
                """
            
            # Prepare key sections
            key_sections_text = ""
            if request.key_sections:
                key_sections_text = f"Required sections: {', '.join(request.key_sections)}"
            
            # Construct outline prompt
            prompt = f"""
            Create a detailed outline for a LinkedIn article about "{request.topic}" in the {request.industry} industry.
            
            Requirements:
            - Target word count: {request.word_count} words
            - Tone: {request.tone.value}
            - Target audience: {request.target_audience or 'Professionals in ' + request.industry}
            
            {key_sections_text}
            {research_context}
            
            Create an outline with:
            1. Compelling article title
            2. Hook/opening paragraph
            3. 4-6 main sections with detailed content points
            4. Conclusion with call-to-action
            
            Return as JSON with this structure:
            {{
                "title": "Article Title",
                "hook": "Opening hook paragraph",
                "sections": [
                    {{
                        "title": "Section Title",
                        "content_points": ["Point 1", "Point 2", "Point 3"],
                        "word_count_target": 200
                    }}
                ],
                "conclusion": "Conclusion paragraph outline"
            }}
            """
            
            outline_schema = {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "hook": {"type": "string"},
                    "sections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "content_points": {"type": "array", "items": {"type": "string"}},
                                "word_count_target": {"type": "number"}
                            }
                        }
                    },
                    "conclusion": {"type": "string"}
                }
            }
            
            # Generate structured outline
            outline = gemini_structured_json_response(
                prompt=prompt,
                json_schema=outline_schema,
                temperature=0.3,
                max_tokens=2000
            )
            
            if outline:
                return outline
            else:
                # Fallback outline
                return {
                    "title": f"{request.topic} in {request.industry}: A Comprehensive Analysis",
                    "hook": f"The {request.industry} industry is undergoing significant transformation...",
                    "sections": [
                        {
                            "title": "Current State of Affairs",
                            "content_points": ["Market overview", "Key challenges", "Emerging opportunities"],
                            "word_count_target": request.word_count // 4
                        },
                        {
                            "title": "Expert Insights and Analysis",
                            "content_points": ["Industry expert opinions", "Data analysis", "Trend identification"],
                            "word_count_target": request.word_count // 4
                        },
                        {
                            "title": "Future Implications",
                            "content_points": ["Predictions", "Strategic recommendations", "Action items"],
                            "word_count_target": request.word_count // 4
                        }
                    ],
                    "conclusion": "Looking ahead, the future of {request.topic} in {request.industry}..."
                }
                
        except Exception as e:
            logger.error(f"Error generating article outline: {str(e)}")
            return {"sections": [], "title": "", "introduction": "", "conclusion": ""}
    
    async def _generate_article_content(self, request: LinkedInArticleRequest, outline: Dict, research_data: Dict) -> Dict:
        """Generate full article content based on outline."""
        try:
            title = outline.get("title", f"{request.topic} in {request.industry}")
            hook = outline.get("hook", "")
            sections = outline.get("sections", [])
            conclusion = outline.get("conclusion", "")
            
            # Generate content for each section
            section_contents = []
            full_content = f"# {title}\n\n{hook}\n\n"
            
            for section in sections:
                section_title = section.get("title", "")
                content_points = section.get("content_points", [])
                target_words = section.get("word_count_target", 200)
                
                # Generate section content
                section_prompt = f"""
                Write a detailed section for a LinkedIn article with the title "{section_title}".
                
                Key points to cover:
                {chr(10).join(['- ' + point for point in content_points])}
                
                Requirements:
                - Target approximately {target_words} words
                - Professional and engaging tone
                - Include specific examples where possible
                - Make it actionable and valuable
                - Use clear subheadings if needed
                
                Topic context: {request.topic} in {request.industry}
                Article tone: {request.tone.value}
                """
                
                section_content = llm_text_gen(section_prompt)
                section_contents.append({
                    "title": section_title,
                    "content": section_content
                })
                
                full_content += f"## {section_title}\n\n{section_content}\n\n"
            
            # Generate enhanced conclusion
            conclusion_prompt = f"""
            Write a compelling conclusion for a LinkedIn article about "{request.topic}" in {request.industry}.
            
            The conclusion should:
            - Summarize key insights
            - Provide actionable next steps
            - Include a strong call-to-action
            - Encourage engagement (comments, shares, connections)
            - Be inspiring and forward-looking
            
            Base outline: {conclusion}
            Tone: {request.tone.value}
            Target audience: {request.target_audience or 'Professionals in ' + request.industry}
            """
            
            enhanced_conclusion = llm_text_gen(conclusion_prompt)
            full_content += f"## Conclusion\n\n{enhanced_conclusion}\n\n"
            
            return {
                "title": title,
                "content": full_content,
                "sections": section_contents + [{"title": "Conclusion", "content": enhanced_conclusion}]
            }
            
        except Exception as e:
            logger.error(f"Error generating article content: {str(e)}")
            return {
                "title": f"Error generating article about {request.topic}",
                "content": "Unable to generate article content. Please try again.",
                "sections": []
            }
    
    async def _generate_seo_metadata(self, request: LinkedInArticleRequest, content: Dict) -> Dict:
        """Generate SEO metadata for the article."""
        try:
            title = content.get("title", "")
            article_content = content.get("content", "")
            
            seo_prompt = f"""
            Generate SEO metadata for a LinkedIn article:
            
            Title: {title}
            Topic: {request.topic}
            Industry: {request.industry}
            Content excerpt: {article_content[:500]}...
            
            Create:
            1. Meta description (150-160 characters)
            2. 8-10 relevant keywords
            3. Optimized title tag (50-60 characters)
            4. LinkedIn article tags (5-7 tags)
            
            Return as JSON:
            {{
                "meta_description": "...",
                "keywords": ["keyword1", "keyword2", ...],
                "title_tag": "...",
                "linkedin_tags": ["tag1", "tag2", ...]
            }}
            """
            
            seo_schema = {
                "type": "object",
                "properties": {
                    "meta_description": {"type": "string"},
                    "keywords": {"type": "array", "items": {"type": "string"}},
                    "title_tag": {"type": "string"},
                    "linkedin_tags": {"type": "array", "items": {"type": "string"}}
                }
            }
            
            seo_data = gemini_structured_json_response(
                prompt=seo_prompt,
                json_schema=seo_schema,
                temperature=0.2,
                max_tokens=800
            )
            
            if seo_data:
                return seo_data
            else:
                return {
                    "meta_description": f"Professional insights on {request.topic} in {request.industry}",
                    "keywords": [request.topic, request.industry, "LinkedIn", "professional"],
                    "title_tag": title[:60] if len(title) <= 60 else title[:57] + "...",
                    "linkedin_tags": [request.industry, request.topic.split()[0]]
                }
                
        except Exception as e:
            logger.error(f"Error generating SEO metadata: {str(e)}")
            return {"meta_description": "", "keywords": [], "title_tag": ""}
    
    async def _generate_image_suggestions(self, request: LinkedInArticleRequest, outline: Dict) -> List[ImageSuggestion]:
        """Generate image suggestions for the article."""
        try:
            sections = outline.get("sections", [])
            image_suggestions = []
            
            # Hero image
            image_suggestions.append(ImageSuggestion(
                description=f"Hero image showing {request.topic} concept in {request.industry} context",
                alt_text=f"{request.topic} in {request.industry}",
                style="professional",
                placement="header"
            ))
            
            # Section images
            for i, section in enumerate(sections[:3]):  # Limit to 3 section images
                section_title = section.get("title", f"Section {i+1}")
                image_suggestions.append(ImageSuggestion(
                    description=f"Visual representation of {section_title}",
                    alt_text=f"Illustration for {section_title}",
                    style="infographic",
                    placement=f"section_{i+1}"
                ))
            
            # Conclusion image
            image_suggestions.append(ImageSuggestion(
                description=f"Call-to-action visual for {request.topic}",
                alt_text="Call to action graphic",
                style="motivational",
                placement="conclusion"
            ))
            
            return image_suggestions
            
        except Exception as e:
            logger.error(f"Error generating image suggestions: {str(e)}")
            return []
    
    async def _generate_carousel_content(self, request: LinkedInCarouselRequest) -> CarouselContent:
        """Generate carousel content with slides."""
        try:
            carousel_prompt = f"""
            Create a LinkedIn carousel about "{request.topic}" for the {request.industry} industry.
            
            Requirements:
            - {request.slide_count} slides total
            - Tone: {request.tone.value}
            - Target audience: {request.target_audience or 'Professionals in ' + request.industry}
            - Visual style: {request.visual_style}
            
            Key takeaways to include: {', '.join(request.key_takeaways or [])}
            
            Return as JSON with this structure:
            {{
                "title": "Carousel Title",
                "slides": [
                    {{
                        "slide_number": 1,
                        "title": "Slide Title",
                        "content": "Slide content",
                        "visual_elements": ["element1", "element2"],
                        "design_notes": "Design guidance"
                    }}
                ],
                "design_guidelines": {{
                    "color_scheme": "professional",
                    "typography": "clean",
                    "layout": "minimal"
                }}
            }}
            """
            
            carousel_schema = {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "slides": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "slide_number": {"type": "number"},
                                "title": {"type": "string"},
                                "content": {"type": "string"},
                                "visual_elements": {"type": "array", "items": {"type": "string"}},
                                "design_notes": {"type": "string"}
                            }
                        }
                    },
                    "design_guidelines": {"type": "object"}
                }
            }
            
            carousel_data = gemini_structured_json_response(
                prompt=carousel_prompt,
                json_schema=carousel_schema,
                temperature=0.4,
                max_tokens=3000
            )
            
            if carousel_data:
                slides = [
                    CarouselSlide(
                        slide_number=slide.get("slide_number", i+1),
                        title=slide.get("title", ""),
                        content=slide.get("content", ""),
                        visual_elements=slide.get("visual_elements", []),
                        design_notes=slide.get("design_notes", "")
                    )
                    for i, slide in enumerate(carousel_data.get("slides", []))
                ]
                
                return CarouselContent(
                    title=carousel_data.get("title", ""),
                    slides=slides,
                    design_guidelines=carousel_data.get("design_guidelines", {})
                )
            else:
                # Fallback carousel
                return CarouselContent(
                    title=f"{request.topic} in {request.industry}",
                    slides=[],
                    design_guidelines={"color_scheme": "professional"}
                )
                
        except Exception as e:
            logger.error(f"Error generating carousel content: {str(e)}")
            return CarouselContent(title="", slides=[], design_guidelines={})
    
    async def _generate_video_script_content(self, request: LinkedInVideoScriptRequest) -> VideoScript:
        """Generate video script content."""
        try:
            script_prompt = f"""
            Create a LinkedIn video script about "{request.topic}" for the {request.industry} industry.
            
            Requirements:
            - Video length: {request.video_length} seconds
            - Tone: {request.tone.value}
            - Target audience: {request.target_audience or 'Professionals in ' + request.industry}
            - Include hook: {request.include_hook}
            - Include captions: {request.include_captions}
            
            Key messages: {', '.join(request.key_messages or [])}
            
            Structure:
            1. Hook (first 3-5 seconds)
            2. Main content (scenes with timing)
            3. Conclusion with CTA
            4. Thumbnail suggestions
            5. Video description
            
            Return as JSON with timing for each scene.
            """
            
            script_schema = {
                "type": "object",
                "properties": {
                    "hook": {"type": "string"},
                    "main_content": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "scene_number": {"type": "number"},
                                "content": {"type": "string"},
                                "duration": {"type": "string"},
                                "visual_notes": {"type": "string"}
                            }
                        }
                    },
                    "conclusion": {"type": "string"},
                    "captions": {"type": "array", "items": {"type": "string"}},
                    "thumbnail_suggestions": {"type": "array", "items": {"type": "string"}},
                    "video_description": {"type": "string"}
                }
            }
            
            script_data = gemini_structured_json_response(
                prompt=script_prompt,
                json_schema=script_schema,
                temperature=0.4,
                max_tokens=2500
            )
            
            if script_data:
                return VideoScript(
                    hook=script_data.get("hook", ""),
                    main_content=script_data.get("main_content", []),
                    conclusion=script_data.get("conclusion", ""),
                    captions=script_data.get("captions", []) if request.include_captions else None,
                    thumbnail_suggestions=script_data.get("thumbnail_suggestions", []),
                    video_description=script_data.get("video_description", "")
                )
            else:
                # Fallback script
                return VideoScript(
                    hook=f"Here's what you need to know about {request.topic}...",
                    main_content=[],
                    conclusion="What's your experience with this? Comment below!",
                    thumbnail_suggestions=[f"{request.topic} tips"],
                    video_description=f"Professional insights on {request.topic} in {request.industry}"
                )
                
        except Exception as e:
            logger.error(f"Error generating video script: {str(e)}")
            return VideoScript(hook="", main_content=[], conclusion="", thumbnail_suggestions=[], video_description="")
    
    async def _generate_comment_response_content(self, request: LinkedInCommentResponseRequest) -> Dict:
        """Generate comment response content."""
        try:
            response_prompt = f"""
            Generate a professional LinkedIn comment response.
            
            Original post: {request.original_post}
            Comment to respond to: {request.comment}
            Response type: {request.response_type}
            Tone: {request.tone.value}
            Include follow-up question: {request.include_question}
            Brand voice: {request.brand_voice or 'Professional and approachable'}
            
            Generate:
            1. Primary response (main response)
            2. 2-3 alternative responses
            3. Tone analysis of the original comment
            
            Return as JSON:
            {{
                "primary_response": "...",
                "alternative_responses": ["response1", "response2", "response3"],
                "tone_analysis": {{
                    "sentiment": "positive/negative/neutral",
                    "intent": "question/appreciation/disagreement/etc",
                    "engagement_level": "high/medium/low"
                }}
            }}
            """
            
            response_schema = {
                "type": "object",
                "properties": {
                    "primary_response": {"type": "string"},
                    "alternative_responses": {"type": "array", "items": {"type": "string"}},
                    "tone_analysis": {
                        "type": "object",
                        "properties": {
                            "sentiment": {"type": "string"},
                            "intent": {"type": "string"},
                            "engagement_level": {"type": "string"}
                        }
                    }
                }
            }
            
            response_data = gemini_structured_json_response(
                prompt=response_prompt,
                json_schema=response_schema,
                temperature=0.3,
                max_tokens=1500
            )
            
            if response_data:
                return response_data
            else:
                # Fallback response
                return {
                    "primary_response": "Thank you for your comment! I appreciate you sharing your perspective.",
                    "alternative_responses": [
                        "Great point! Thanks for adding to the discussion.",
                        "I'm glad this resonated with you. What's been your experience?"
                    ],
                    "tone_analysis": {
                        "sentiment": "neutral",
                        "intent": "engagement",
                        "engagement_level": "medium"
                    }
                }
                
        except Exception as e:
            logger.error(f"Error generating comment response: {str(e)}")
            return {"primary_response": "", "alternative_responses": [], "tone_analysis": {}}
    
    def _calculate_reading_time(self, content: str, words_per_minute: int = 200) -> int:
        """Calculate reading time in minutes."""
        word_count = len(content.split())
        return max(1, round(word_count / words_per_minute))


# Initialize service instance
linkedin_service = LinkedInContentService()