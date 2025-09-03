"""
Enhanced Gemini Provider for Grounded Content Generation

This provider uses native Google Search grounding to generate content that is
factually grounded in current web sources, with automatic citation generation.
Based on Google AI's official grounding documentation.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

try:
    from google import genai
    from google.genai import types
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False
    logger.warn("Google GenAI not available. Install with: pip install google-genai")


class GeminiGroundedProvider:
    """
    Enhanced Gemini provider for grounded content generation with native Google Search.
    
    This provider uses the official Google Search grounding tool to generate content
    that is factually grounded in current web sources, with automatic citation generation.
    
    Based on: https://ai.google.dev/gemini-api/docs/google-search
    """
    
    def __init__(self):
        """Initialize the Gemini Grounded Provider."""
        if not GOOGLE_GENAI_AVAILABLE:
            raise ImportError("Google GenAI library not available. Install with: pip install google-genai")
        
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Initialize the Gemini client
        self.client = genai.Client(api_key=self.api_key)
        logger.info("✅ Gemini Grounded Provider initialized with native Google Search grounding")
    
    async def generate_grounded_content(
        self, 
        prompt: str, 
        content_type: str = "linkedin_post",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Generate grounded content using native Google Search grounding.
        
        Args:
            prompt: The content generation prompt
            content_type: Type of content to generate
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary containing generated content and grounding metadata
        """
        try:
            logger.info(f"Generating grounded content for {content_type} using native Google Search")
            
            # Build the grounded prompt
            grounded_prompt = self._build_grounded_prompt(prompt, content_type)
            
            # Configure the grounding tool
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )
            
            # Configure generation settings
            config = types.GenerateContentConfig(
                tools=[grounding_tool],
                max_output_tokens=max_tokens,
                temperature=temperature
            )
            
            # Make the request with native grounding
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=grounded_prompt,
                config=config,
            )
            
            # Process the grounded response
            result = self._process_grounded_response(response, content_type)
            
            logger.info(f"✅ Grounded content generated successfully with {len(result.get('sources', []))} sources")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error generating grounded content: {str(e)}")
            raise
    
    def _build_grounded_prompt(self, prompt: str, content_type: str) -> str:
        """
        Build a prompt optimized for grounded content generation.
        
        Args:
            prompt: Base prompt
            content_type: Type of content being generated
            
        Returns:
            Enhanced prompt for grounded generation
        """
        content_type_instructions = {
            "linkedin_post": "You are an expert LinkedIn content strategist. Generate a highly engaging, professional LinkedIn post that drives meaningful engagement, establishes thought leadership, and includes compelling hooks, actionable insights, and strategic hashtags. Every element should be optimized for maximum engagement and shareability.",
            "linkedin_article": "You are a senior content strategist and industry thought leader. Generate a comprehensive, SEO-optimized LinkedIn article with compelling headlines, structured content, data-driven insights, and practical takeaways. Include proper source citations and engagement elements throughout.",
            "linkedin_carousel": "You are a visual content strategist specializing in LinkedIn carousels. Generate compelling, story-driven carousel content with clear visual hierarchy, actionable insights per slide, and strategic engagement elements. Each slide should provide immediate value while building anticipation for the next.",
            "linkedin_video_script": "You are a video content strategist and LinkedIn engagement expert. Generate a compelling video script optimized for LinkedIn's algorithm with attention-grabbing hooks, strategic timing, and engagement-driven content. Include specific visual and audio recommendations for maximum impact.",
            "linkedin_comment_response": "You are a LinkedIn engagement specialist and industry expert. Generate thoughtful, value-adding comment responses that encourage further discussion, demonstrate expertise, and build meaningful professional relationships. Focus on genuine engagement over generic responses."
        }
        
        instruction = content_type_instructions.get(content_type, "Generate professional content with factual accuracy.")
        
        grounded_prompt = f"""
        {instruction}
        
        CRITICAL REQUIREMENTS FOR LINKEDIN CONTENT:
        - Use ONLY current, factual information from reliable sources (2024-2025)
        - Cite specific sources for ALL claims, statistics, and recent developments
        - Ensure content is optimized for LinkedIn's algorithm and engagement patterns
        - Include strategic hashtags and engagement elements throughout
        
        User Request: {prompt}
        
        CONTENT QUALITY STANDARDS:
        - All factual claims must be backed by current, authoritative sources
        - Use professional yet conversational language that encourages engagement
        - Include relevant industry insights, trends, and data points
        - Make content highly shareable with clear value proposition
        - Optimize for LinkedIn's professional audience and engagement metrics
        
        ENGAGEMENT OPTIMIZATION:
        - Include thought-provoking questions and calls-to-action
        - Use storytelling elements and real-world examples
        - Ensure content provides immediate, actionable value
        - Optimize for comments, shares, and professional networking
        - Include industry-specific terminology and insights
        
        REMEMBER: This content will be displayed on LinkedIn with full source attribution and grounding data. Every claim must be verifiable, and the content should position the author as a thought leader in their industry.
        """
        
        return grounded_prompt.strip()
    
    def _process_grounded_response(self, response, content_type: str) -> Dict[str, Any]:
        """
        Process the Gemini response with grounding metadata.
        
        Args:
            response: Gemini API response
            content_type: Type of content generated
            
        Returns:
            Processed content with sources and citations
        """
        try:
            # Extract the main content
            content = ""
            if hasattr(response, 'text'):
                content = response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    # Extract text from content parts
                    text_parts = []
                    for part in candidate.content:
                        if hasattr(part, 'text'):
                            text_parts.append(part.text)
                    content = " ".join(text_parts)
            
            logger.info(f"Extracted content length: {len(content) if content else 0}")
            if not content:
                logger.warning("No content extracted from response")
                content = "Generated content about the requested topic."
            
            # Initialize result structure
            result = {
                'content': content,
                'sources': [],
                'citations': [],
                'search_queries': [],
                'grounding_metadata': {},
                'content_type': content_type,
                'generation_timestamp': datetime.now().isoformat()
            }
            
            # Debug: Log response structure
            logger.info(f"Response type: {type(response)}")
            logger.info(f"Response attributes: {dir(response)}")
            
            # Extract grounding metadata if available
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                logger.info(f"Candidate attributes: {dir(candidate)}")
                
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    grounding_metadata = candidate.grounding_metadata
                    result['grounding_metadata'] = grounding_metadata
                    logger.info(f"Grounding metadata attributes: {dir(grounding_metadata)}")
                    logger.info(f"Grounding metadata type: {type(grounding_metadata)}")
                    logger.info(f"Grounding metadata value: {grounding_metadata}")
                    
                    # Log all available attributes and their values
                    for attr in dir(grounding_metadata):
                        if not attr.startswith('_'):
                            try:
                                value = getattr(grounding_metadata, attr)
                                logger.info(f"  {attr}: {type(value)} = {value}")
                            except Exception as e:
                                logger.warning(f"  {attr}: Error accessing - {e}")
                    
                    # Extract search queries
                    if hasattr(grounding_metadata, 'web_search_queries'):
                        result['search_queries'] = grounding_metadata.web_search_queries
                        logger.info(f"Search queries: {grounding_metadata.web_search_queries}")
                    
                    # Extract sources from grounding chunks
                    if hasattr(grounding_metadata, 'grounding_chunks') and grounding_metadata.grounding_chunks:
                        sources = []
                        for i, chunk in enumerate(grounding_metadata.grounding_chunks):
                            logger.info(f"Chunk {i} attributes: {dir(chunk)}")
                            if hasattr(chunk, 'web'):
                                source = {
                                    'index': i,
                                    'title': getattr(chunk.web, 'title', f'Source {i+1}'),
                                    'url': getattr(chunk.web, 'uri', ''),
                                    'type': 'web'
                                }
                                sources.append(source)
                        result['sources'] = sources
                        logger.info(f"Extracted {len(sources)} sources")
                    else:
                        logger.error("❌ CRITICAL: No grounding chunks found in response")
                        logger.error(f"Grounding metadata structure: {dir(grounding_metadata)}")
                        if hasattr(grounding_metadata, 'grounding_chunks'):
                            logger.error(f"Grounding chunks type: {type(grounding_metadata.grounding_chunks)}")
                            logger.error(f"Grounding chunks value: {grounding_metadata.grounding_chunks}")
                        raise ValueError("No grounding chunks found - grounding is not working properly")
                    
                    # Extract citations from grounding supports
                    if hasattr(grounding_metadata, 'grounding_supports') and grounding_metadata.grounding_supports:
                        citations = []
                        for support in grounding_metadata.grounding_supports:
                            if hasattr(support, 'segment') and hasattr(support, 'grounding_chunk_indices'):
                                citation = {
                                    'type': 'inline',
                                    'start_index': getattr(support.segment, 'start_index', 0),
                                    'end_index': getattr(support.segment, 'end_index', 0),
                                    'text': getattr(support.segment, 'text', ''),
                                    'source_indices': support.grounding_chunk_indices,
                                    'reference': f"Source {support.grounding_chunk_indices[0] + 1}" if support.grounding_chunk_indices else "Unknown"
                                }
                                citations.append(citation)
                        result['citations'] = citations
                        logger.info(f"Extracted {len(citations)} citations")
                    else:
                        logger.error("❌ CRITICAL: No grounding supports found in response")
                        logger.error(f"Grounding metadata structure: {dir(grounding_metadata)}")
                        if hasattr(grounding_metadata, 'grounding_supports'):
                            logger.error(f"Grounding supports type: {type(grounding_metadata.grounding_supports)}")
                            logger.error(f"Grounding supports value: {grounding_metadata.grounding_supports}")
                        raise ValueError("No grounding supports found - grounding is not working properly")
                    
                    logger.info(f"✅ Successfully extracted {len(result['sources'])} sources and {len(result['citations'])} citations from grounding metadata")
                    logger.info(f"Sources: {result['sources']}")
                    logger.info(f"Citations: {result['citations']}")
                else:
                    logger.error("❌ CRITICAL: No grounding metadata found in response")
                    logger.error(f"Response structure: {dir(response)}")
                    logger.error(f"First candidate structure: {dir(candidates[0]) if candidates else 'No candidates'}")
                    raise ValueError("No grounding metadata found - grounding is not working properly")
            else:
                logger.error("❌ CRITICAL: No candidates found in response")
                logger.error(f"Response structure: {dir(response)}")
                raise ValueError("No candidates found in response - grounding is not working properly")
            
            # Add content-specific processing
            if content_type == "linkedin_post":
                result.update(self._process_post_content(content))
            elif content_type == "linkedin_article":
                result.update(self._process_article_content(content))
            elif content_type == "linkedin_carousel":
                result.update(self._process_carousel_content(content))
            elif content_type == "linkedin_video_script":
                result.update(self._process_video_script_content(content))
            
            return result
            
        except Exception as e:
            logger.error(f"❌ CRITICAL: Error processing grounded response: {str(e)}")
            logger.error(f"Exception type: {type(e)}")
            logger.error(f"Exception details: {e}")
            raise ValueError(f"Failed to process grounded response: {str(e)}")
    
    def _process_post_content(self, content: str) -> Dict[str, Any]:
        """Process LinkedIn post content for hashtags and engagement elements."""
        try:
            # Handle None content
            if content is None:
                content = ""
                logger.warning("Content is None, using empty string")
            
            # Extract hashtags
            hashtags = re.findall(r'#\w+', content)
            
            # Generate call-to-action if not present
            cta_patterns = [
                r'What do you think\?',
                r'Share your thoughts',
                r'Comment below',
                r'What\'s your experience\?',
                r'Let me know in the comments'
            ]
            
            has_cta = any(re.search(pattern, content, re.IGNORECASE) for pattern in cta_patterns)
            call_to_action = None
            if not has_cta:
                call_to_action = "What are your thoughts on this? Share in the comments!"
            
            return {
                'hashtags': [{'hashtag': tag, 'category': 'general', 'popularity_score': 0.8} for tag in hashtags],
                'call_to_action': call_to_action,
                'engagement_prediction': {
                    'estimated_likes': max(50, len(content) // 10),
                    'estimated_comments': max(5, len(content) // 100)
                }
            }
        except Exception as e:
            logger.error(f"Error processing post content: {str(e)}")
            return {}
    
    def _process_article_content(self, content: str) -> Dict[str, Any]:
        """Process LinkedIn article content for structure and SEO."""
        try:
            # Extract title (first line or first sentence)
            lines = content.split('\n')
            title = lines[0].strip() if lines else "Article Title"
            
            # Estimate word count
            word_count = len(content.split())
            
            # Generate sections based on content structure
            sections = []
            current_section = ""
            
            for line in lines:
                if line.strip().startswith('#') or line.strip().startswith('##'):
                    if current_section:
                        sections.append({'title': 'Section', 'content': current_section.strip()})
                        current_section = ""
                else:
                    current_section += line + "\n"
            
            if current_section:
                sections.append({'title': 'Content', 'content': current_section.strip()})
            
            return {
                'title': title,
                'word_count': word_count,
                'sections': sections,
                'reading_time': max(1, word_count // 200),  # 200 words per minute
                'seo_metadata': {
                    'meta_description': content[:160] + "..." if len(content) > 160 else content,
                    'keywords': self._extract_keywords(content)
                }
            }
        except Exception as e:
            logger.error(f"Error processing article content: {str(e)}")
            return {}
    
    def _process_carousel_content(self, content: str) -> Dict[str, Any]:
        """Process LinkedIn carousel content for slide structure."""
        try:
            # Split content into slides (basic implementation)
            slides = []
            content_parts = content.split('\n\n')
            
            for i, part in enumerate(content_parts[:10]):  # Max 10 slides
                if part.strip():
                    slides.append({
                        'slide_number': i + 1,
                        'title': f"Slide {i + 1}",
                        'content': part.strip(),
                        'visual_elements': [],
                        'design_notes': None
                    })
            
            return {
                'title': f"Carousel on {content[:50]}...",
                'slides': slides,
                'design_guidelines': {
                    'color_scheme': 'professional',
                    'typography': 'clean',
                    'layout': 'minimal'
                }
            }
        except Exception as e:
            logger.error(f"Error processing carousel content: {str(e)}")
            return {}
    
    def _process_video_script_content(self, content: str) -> Dict[str, Any]:
        """Process LinkedIn video script content for structure."""
        try:
            # Basic video script processing
            lines = content.split('\n')
            hook = ""
            main_content = []
            conclusion = ""
            
            # Extract hook (first few lines)
            hook_lines = []
            for line in lines[:3]:
                if line.strip() and not line.strip().startswith('#'):
                    hook_lines.append(line.strip())
                    if len(' '.join(hook_lines)) > 100:
                        break
            hook = ' '.join(hook_lines)
            
            # Extract conclusion (last few lines)
            conclusion_lines = []
            for line in lines[-3:]:
                if line.strip() and not line.strip().startswith('#'):
                    conclusion_lines.insert(0, line.strip())
                    if len(' '.join(conclusion_lines)) > 100:
                        break
            conclusion = ' '.join(conclusion_lines)
            
            # Main content (everything in between)
            main_content_text = content[len(hook):len(content)-len(conclusion)].strip()
            
            return {
                'hook': hook,
                'main_content': [{
                    'scene_number': 1,
                    'content': main_content_text,
                    'duration': 60,
                    'visual_notes': 'Professional presentation style'
                }],
                'conclusion': conclusion,
                'thumbnail_suggestions': ['Professional thumbnail', 'Industry-focused image'],
                'video_description': f"Professional insights on {content[:100]}..."
            }
        except Exception as e:
            logger.error(f"Error processing video script content: {str(e)}")
            return {}
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords from content."""
        try:
            # Simple keyword extraction (can be enhanced with NLP)
            words = re.findall(r'\b\w+\b', content.lower())
            word_freq = {}
            
            # Filter out common words
            stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an'}
            
            for word in words:
                if word not in stop_words and len(word) > 3:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Return top keywords
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_words[:10]]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    def add_citations(self, content: str, sources: List[Dict[str, Any]]) -> str:
        """
        Add inline citations to content based on grounding metadata.
        
        Args:
            content: The content to add citations to
            sources: List of sources from grounding metadata
            
        Returns:
            Content with inline citations
        """
        try:
            if not sources:
                return content
            
            # Create citation mapping
            citation_map = {}
            for source in sources:
                index = source.get('index', 0)
                citation_map[index] = f"[Source {index + 1}]({source.get('url', '')})"
            
            # Add citations at the end of sentences or paragraphs
            # This is a simplified approach - in practice, you'd use the groundingSupports data
            citation_text = "\n\n**Sources:**\n"
            for i, source in enumerate(sources):
                citation_text += f"{i+1}. **{source.get('title', f'Source {i+1}')}**\n   - URL: [{source.get('url', '')}]({source.get('url', '')})\n\n"
            
            return content + citation_text
            
        except Exception as e:
            logger.error(f"Error adding citations: {str(e)}")
            return content
    
    def extract_citations(self, content: str) -> List[Dict[str, Any]]:
        """
        Extract citations from content.
        
        Args:
            content: Content to extract citations from
            
        Returns:
            List of citation objects
        """
        try:
            citations = []
            # Look for citation patterns
            citation_patterns = [
                r'\[Source (\d+)\]',
                r'\[(\d+)\]',
                r'\(Source (\d+)\)'
            ]
            
            for pattern in citation_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    citations.append({
                        'type': 'inline',
                        'reference': match.group(0),
                        'position': match.start(),
                        'source_index': int(match.group(1)) - 1
                    })
            
            return citations
            
        except Exception as e:
            logger.error(f"Error extracting citations: {str(e)}")
            return []
    
    def assess_content_quality(self, content: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess the quality of generated content.
        
        Args:
            content: The generated content
            sources: List of sources used
            
        Returns:
            Quality metrics dictionary
        """
        try:
            # Basic quality metrics
            word_count = len(content.split())
            char_count = len(content)
            
            # Source coverage
            source_coverage = min(1.0, len(sources) / max(1, word_count / 100))
            
            # Professional tone indicators
            professional_indicators = ['research', 'analysis', 'insights', 'trends', 'industry', 'professional']
            unprofessional_indicators = ['awesome', 'amazing', 'incredible', 'mind-blowing']
            
            professional_score = sum(1 for indicator in professional_indicators if indicator.lower() in content.lower()) / len(professional_indicators)
            unprofessional_score = sum(1 for indicator in unprofessional_indicators if indicator.lower() in content.lower()) / len(unprofessional_indicators)
            
            tone_score = max(0, professional_score - unprofessional_score)
            
            # Overall quality score
            overall_score = (source_coverage * 0.4 + tone_score * 0.3 + min(1.0, word_count / 500) * 0.3)
            
            return {
                'overall_score': round(overall_score, 2),
                'source_coverage': round(source_coverage, 2),
                'tone_score': round(tone_score, 2),
                'word_count': word_count,
                'char_count': char_count,
                'sources_count': len(sources),
                'quality_level': 'high' if overall_score > 0.8 else 'medium' if overall_score > 0.6 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error assessing content quality: {str(e)}")
            return {
                'overall_score': 0.0,
                'error': str(e)
            }
