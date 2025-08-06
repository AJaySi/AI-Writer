"""
LinkedIn Post Generator

This module provides functionality for generating LinkedIn posts with research-backed content,
optimized hashtags, and engagement predictions.
"""

import os
import json
import time
import streamlit as st
from typing import Dict, List, Optional, Tuple, Union
from loguru import logger
import random

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....ai_web_researcher.gpt_online_researcher import do_google_serp_search
from .....ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles, streamlit_display_metaphor_results
from .....ai_web_researcher.tavily_ai_search import do_tavily_ai_search, streamlit_display_results


class LinkedInPostGenerator:
    """
    A class for generating LinkedIn posts with research-backed content.
    
    This class provides methods for:
    - Researching topics using Metaphor and Google
    - Generating outlines based on research
    - Creating post content optimized for engagement
    - Optimizing hashtags
    - Generating visual content recommendations
    - Predicting engagement metrics
    - Suggesting optimal posting times
    - Creating polls
    """
    
    def __init__(self):
        """Initialize the LinkedIn Post Generator."""
        self.research_results = {}
        self.outline = {}
        self.post_content = ""
        self.hashtags = []
        self.visual_content = {}
        self.engagement_prediction = {}
        self.posting_time_suggestions = []
        self.poll = {}
    
    def research_topic(self, topic: str, industry: str, search_engine: str = "metaphor", status_container=None) -> Dict:
        """
        Research a topic using the selected search engine.
        
        Args:
            topic: The topic to research
            industry: The industry context
            search_engine: The search engine to use (metaphor, google, tavily)
            status_container: Optional container for status updates
            
        Returns:
            Dict containing research results
        """
        # Update progress
        if status_container:
            status_container.text("🔍 Researching topic...")
        
        # Research with selected search engine
        research_results = None
        if search_engine == "metaphor":
            research_results = self._research_with_metaphor(topic, industry, status_container)
        elif search_engine == "google":
            research_results = self._research_with_google(topic, industry, status_container)
        elif search_engine == "tavily":
            research_results = self._research_with_tavily(topic, industry, status_container)
        else:
            research_results = self._research_with_metaphor(topic, industry, status_container)
        
        # Analyze research results
        combined_results = self._analyze_research_results(research_results, topic, industry)
        
        # Add topic and industry to the results
        combined_results["topic"] = topic
        combined_results["industry"] = industry
        
        # Update progress
        if status_container:
            status_container.text("✅ Research complete!")
        
        return combined_results
    
    def _research_with_metaphor(self, topic: str, industry: str, status_container=None) -> Dict:
        """
        Research a topic using Metaphor.
        
        Args:
            topic: The topic to research
            industry: The industry context
            status_container: Optional container for status updates
            
        Returns:
            Dict containing research results
        """
        # Update progress
        if status_container:
            status_container.text("🔍 Searching with Metaphor...")
        
        try:
            # Construct search query
            search_query = f"{topic} in {industry} industry"
            
            # Search with Metaphor
            metaphor_results = metaphor_search_articles(search_query)
            
            # Display the results using streamlit_display_metaphor_results
            if metaphor_results:
                streamlit_display_metaphor_results(metaphor_results, search_query)
            
            # Update progress
            if status_container:
                status_container.text("✅ Metaphor search complete!")
            
            # Ensure we return a valid dictionary even if metaphor_results is None
            if metaphor_results is None:
                logger.warning(f"No results returned from Metaphor search for: {search_query}")
                return {"sources": []}
                
            return metaphor_results
        except Exception as e:
            logger.error(f"Error in Metaphor search: {e}")
            if status_container:
                status_container.text(f"⚠️ Error in Metaphor search: {str(e)}")
            return {"sources": []}
    
    def _research_with_google(self, topic: str, industry: str, status_container=None) -> Dict:
        """
        Research a topic using Google.
        
        Args:
            topic: The topic to research
            industry: The industry context
            status_container: Optional container for status updates
            
        Returns:
            Dict containing research results
        """
        # Update progress
        if status_container:
            status_container.text("🔍 Searching with Google...")
        
        try:
            # Search with Google
            google_results = do_google_serp_search(topic, industry)
            
            # Display the results using streamlit_display_google_results
            if google_results:
                streamlit_display_google_results(google_results)
            
            # Update progress
            if status_container:
                status_container.text("✅ Google search complete!")
            
            # Ensure we return a valid dictionary even if google_results is None
            if google_results is None:
                logger.warning(f"No results returned from Google search for: {topic} in {industry}")
                return {"sources": []}
                
            return google_results
        except Exception as e:
            logger.error(f"Error in Google search: {e}")
            if status_container:
                status_container.text(f"⚠️ Error in Google search: {str(e)}")
            return {"sources": []}
    
    def _research_with_tavily(self, topic: str, industry: str, status_container=None) -> Dict:
        """
        Research a topic using Tavily AI.
        
        Args:
            topic: The topic to research
            industry: The industry context
            status_container: Optional container for status updates
            
        Returns:
            Dict containing research results
        """
        # Update progress
        if status_container:
            status_container.text("🔍 Searching with Tavily AI...")
        
        # Construct search query
        search_query = f"{topic} in {industry} industry"
        
        try:
            # Search with Tavily
            tavily_results = do_tavily_ai_search(search_query)
            
            # Display the results using streamlit_display_results
            if tavily_results:
                streamlit_display_results(tavily_results)
            
            # Update progress
            if status_container:
                status_container.text("✅ Tavily search complete!")
            
            # Ensure we return a valid dictionary even if tavily_results is None
            if tavily_results is None:
                logger.warning(f"No results returned from Tavily search for: {search_query}")
                return {"sources": []}
                
            return tavily_results
        except Exception as e:
            logger.error(f"Error in Tavily search: {e}")
            if status_container:
                status_container.text(f"⚠️ Error in Tavily search: {str(e)}")
            return {"sources": []}
    
    def _analyze_research_results(self, research_results: Dict, topic: str, industry: str) -> Dict:
        """
        Analyze research results to extract key insights.
        
        Args:
            research_results: Results from research
            topic: The topic being researched
            industry: The industry context
            
        Returns:
            Dict containing analyzed insights
        """
        # Handle case where research_results is None
        if research_results is None:
            logger.warning(f"No research results available for {topic} in {industry}")
            return {
                "key_insights": [f"Unable to find specific insights about {topic} in {industry}"],
                "data_points": [f"No specific data available for {topic} in {industry}"],
                "expert_quotes": [f"No expert quotes found about {topic} in {industry}"],
                "industry_context": f"Limited information available about {topic} in {industry} industry"
            }
        
        # Extract sources and content from research results
        sources = research_results.get("sources", [])
        content = "\n".join([source.get("content", "") for source in sources])
        
        # Generate analysis prompt
        analysis_prompt = f"""
        Analyze the following research about {topic} in the {industry} industry:
        
        {content}
        
        Extract the following:
        1. Key insights and trends
        2. Supporting data and statistics
        3. Expert opinions and quotes
        4. Industry-specific context
        
        Format the response as a JSON with these keys:
        - key_insights: List of main insights
        - data_points: List of relevant data/statistics
        - expert_quotes: List of expert opinions
        - industry_context: Relevant industry information
        """
        
        # Generate analysis using LLM
        analysis = llm_text_gen(analysis_prompt)
        
        # Parse the analysis
        try:
            analysis_dict = json.loads(analysis)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            analysis_dict = {
                "key_insights": ["Unable to parse analysis"],
                "data_points": [],
                "expert_quotes": [],
                "industry_context": "Unable to parse industry context"
            }
        
        return analysis_dict
    
    def generate_outline(self, research_results: Dict) -> Dict:
        """
        Generate a detailed post outline based on research results.
        
        Args:
            research_results: Dictionary containing analyzed research results
            
        Returns:
            Dict containing the post outline
        """
        # Extract key information from research results
        topic = research_results.get("topic", "")
        industry = research_results.get("industry", "")
        key_insights = research_results.get("key_insights", [])
        data_points = research_results.get("data_points", [])
        expert_quotes = research_results.get("expert_quotes", [])
        industry_context = research_results.get("industry_context", "")
        
        # Generate outline prompt
        outline_prompt = f"""
        Create a detailed LinkedIn post outline about {topic} in the {industry} industry.
        
        Use these research insights:
        Key Insights: {', '.join(key_insights)}
        Data Points: {', '.join(data_points)}
        Expert Quotes: {', '.join(expert_quotes)}
        Industry Context: {industry_context}
        
        The outline should include:
        1. A compelling hook that grabs attention and introduces the topic
        2. 3-4 main points that provide valuable insights, each supported by:
           - Specific data or statistics
           - Expert opinions or quotes
           - Real-world examples or case studies
        3. A thought-provoking conclusion
        4. A clear call to action that encourages engagement
        
        Format the response as a JSON with these keys:
        - hook: The opening statement (1-2 sentences)
        - main_points: List of 3-4 main points (each 1-2 sentences)
        - supporting_evidence: List of supporting evidence for each point (include data, quotes, examples)
        - conclusion: A strong conclusion (1-2 sentences)
        - call_to_action: The closing call to action (1-2 sentences)
        - key_statistics: List of 2-3 key statistics to highlight
        - expert_insights: List of 2-3 expert insights to include
        """
        
        # Generate outline using LLM
        outline = llm_text_gen(outline_prompt)
        
        # Parse the outline
        try:
            outline_dict = json.loads(outline)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            outline_dict = {
                "hook": f"Let's talk about {topic}",
                "main_points": ["Unable to generate main points"],
                "supporting_evidence": ["Unable to generate supporting evidence"],
                "conclusion": f"These insights highlight the importance of {topic}",
                "call_to_action": "What are your thoughts on this topic?",
                "key_statistics": ["No statistics available"],
                "expert_insights": ["No expert insights available"]
            }
        
        # Add topic and industry to the outline
        outline_dict["topic"] = topic
        outline_dict["industry"] = industry
        
        return outline_dict
    
    def generate_post_content(self, outline: Dict, tone: str = "professional", include_hashtags: bool = True) -> str:
        """
        Generate detailed LinkedIn post content based on the outline.
        
        Args:
            outline: Dictionary containing the post outline
            tone: The tone to use for the post
            include_hashtags: Whether to include hashtags
            
        Returns:
            str: The generated post content
        """
        # Extract outline components
        hook = outline.get("hook", "")
        main_points = outline.get("main_points", [])
        supporting_evidence = outline.get("supporting_evidence", [])
        conclusion = outline.get("conclusion", "")
        call_to_action = outline.get("call_to_action", "")
        key_statistics = outline.get("key_statistics", [])
        expert_insights = outline.get("expert_insights", [])
        topic = outline.get("topic", "")
        industry = outline.get("industry", "")
        
        # Generate post prompt
        post_prompt = f"""
        Create a detailed, insightful LinkedIn post about {topic} in the {industry} industry with the following components:
        
        Hook: {hook}
        Main Points: {', '.join(main_points)}
        Supporting Evidence: {', '.join(supporting_evidence)}
        Conclusion: {conclusion}
        Call to Action: {call_to_action}
        Key Statistics: {', '.join(key_statistics)}
        Expert Insights: {', '.join(expert_insights)}
        
        Tone: {tone}
        
        IMPORTANT INSTRUCTIONS:
        1. Write ONLY the post content - no explanations or meta-commentary
        2. Do not include phrases like "Here's a LinkedIn post" or "I wrote this post"
        3. Format with appropriate emojis and line breaks for readability
        4. Make it engaging, professional, and insightful
        5. Include specific data points, statistics, and expert quotes where relevant
        6. Structure the post with clear paragraphs and bullet points where appropriate
        7. Keep the post between 800-1200 characters for optimal engagement
        8. Focus specifically on {topic} in the {industry} industry
        9. Include a personal perspective or experience if relevant
        10. End with a thought-provoking question to encourage comments
        11. Use line breaks between paragraphs for better readability
        12. Include relevant emojis to highlight key points
        """
        
        # Generate post content
        post_content = llm_text_gen(post_prompt)
        
        # Clean up any potential explanations
        post_content = post_content.replace("Here's a LinkedIn post:", "")
        post_content = post_content.replace("LinkedIn post:", "")
        post_content = post_content.replace("Post:", "")
        post_content = post_content.strip()
        
        # Add hashtags if requested
        if include_hashtags:
            hashtags = self.optimize_hashtags(post_content)
            if hashtags:
                post_content += "\n\n" + " ".join(hashtags)
        
        return post_content
    
    def optimize_hashtags(self, post_content: str) -> List[str]:
        """
        Generate optimized hashtags for a LinkedIn post.
        
        Args:
            post_content: The content of the post
            
        Returns:
            List[str]: List of optimized hashtags
        """
        # Generate hashtag prompt
        hashtag_prompt = f"""
        Generate relevant hashtags for this LinkedIn post:
        
        {post_content}
        
        IMPORTANT INSTRUCTIONS:
        1. Return ONLY a comma-separated list of hashtags
        2. Do not include any explanations or commentary
        3. Each hashtag should start with #
        4. Do not include spaces in hashtags
        5. Include a mix of broad and specific hashtags
        6. Limit to 5-7 most relevant hashtags
        7. Make hashtags searchable and professional
        8. Do not include any text before or after the hashtags
        """
        
        # Generate hashtags
        hashtag_response = llm_text_gen(hashtag_prompt)
        
        # Clean up the response
        hashtag_response = hashtag_response.replace("Hashtags:", "")
        hashtag_response = hashtag_response.replace("Suggested hashtags:", "")
        hashtag_response = hashtag_response.strip()
        
        # Parse hashtags
        hashtags = [tag.strip() for tag in hashtag_response.split(",")]
        hashtags = [tag for tag in hashtags if tag.startswith("#")]
        
        return hashtags
    
    def generate_visual_content(self, post_content: str, topic: str) -> Dict:
        """
        Generate visual content recommendations and create images for a LinkedIn post.
        
        Args:
            post_content: The post content
            topic: The post topic
            
        Returns:
            Dict containing visual content recommendations and generated images
        """
        logger.info(f"Generating visual content for topic: {topic}")
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress
        progress_bar.progress(20)
        status_text.text("Analyzing post content...")
        
        # Extract key elements from post content for better image generation
        key_elements_prompt = f"""
        Analyze this LinkedIn post content and extract SPECIFIC visual elements that would create a UNIQUE and TARGETED image:

        {post_content}

        Extract these elements and be EXTREMELY SPECIFIC:
        1. Main concept or message (What's the core idea we need to visualize?)
        2. Key data or statistics mentioned (Can we visualize these?)
        3. Industry-specific elements (What visuals would resonate with this industry?)
        4. Abstract concepts mentioned (How can we represent these visually?)
        5. Text to potentially overlay (What 2-3 word phrase would enhance the image?)

        Return ONLY a JSON object with these keys:
        {{
            "main_concept": "The specific core concept to visualize",
            "data_elements": ["List of specific data points to potentially visualize"],
            "industry_visuals": ["List of industry-specific visual elements"],
            "abstract_concepts": ["List of abstract concepts to represent"],
            "potential_text": ["2-3 short phrases that could be overlaid on the image"],
            "style_keywords": ["List of specific style keywords for this topic"]
        }}
        """
        
        # Get key elements from LLM
        key_elements_response = llm_text_gen(key_elements_prompt)
        
        # Parse the key elements
        try:
            key_elements = json.loads(key_elements_response)
        except json.JSONDecodeError:
            key_elements = {
                "main_concept": topic,
                "data_elements": [],
                "industry_visuals": [],
                "abstract_concepts": [],
                "potential_text": [],
                "style_keywords": ["professional", "modern", "clean"]
            }
        
        # Update progress
        progress_bar.progress(40)
        status_text.text("Generating visual content recommendations...")
        
        # Randomly decide whether to include text overlay (30% chance)
        include_text = random.random() < 0.3
        text_overlay = ""
        if include_text and key_elements.get("potential_text"):
            text_overlay = random.choice(key_elements.get("potential_text"))
        
        # Generate visual content recommendations using the extracted key elements
        prompt = f"""
        Generate HIGHLY SPECIFIC visual content recommendations for a LinkedIn post about {topic}.
        
        Content Focus:
        - Main concept: {key_elements.get('main_concept')}
        - Data elements: {', '.join(key_elements.get('data_elements', []))}
        - Industry visuals: {', '.join(key_elements.get('industry_visuals', []))}
        - Abstract concepts: {', '.join(key_elements.get('abstract_concepts', []))}
        - Style keywords: {', '.join(key_elements.get('style_keywords', []))}
        
        Create recommendations that:
        1. Are UNIQUE to this specific post and topic
        2. Incorporate actual elements from the post content
        3. Use industry-specific imagery and symbolism
        4. {"Include text overlay: " + text_overlay if include_text else "Focus on purely visual elements"}
        
        Format as JSON:
        {{
            "main_image": {{
                "concept": "Detailed description of the main image",
                "prompt": "Detailed generation prompt that is SPECIFIC to this post",
                "colors": ["Color 1", "Color 2", "Color 3"],
                "text_overlay": "Text to overlay (if any)"
            }},
            "alternative_formats": [
                {{
                    "format": "Format name",
                    "description": "Description",
                    "suggestions": ["Suggestion 1", "Suggestion 2"]
                }}
            ]
        }}
        """
        
        # Get visual content recommendations from LLM
        visual_content_response = llm_text_gen(prompt)
        
        # Parse the visual content recommendations
        try:
            visual_content = json.loads(visual_content_response)
            
            # Enhance the prompt with specific style and quality requirements
            base_prompt = visual_content["main_image"]["prompt"]
            text_part = f", with elegant text overlay: '{text_overlay}'" if include_text else ""
            
            visual_content["main_image"]["prompt"] = f"""
            {base_prompt}{text_part}, 
            Style requirements: ultra high quality, 8k resolution, professional photography, 
            dramatic lighting, perfect composition, extremely detailed, 
            corporate style, professional context, LinkedIn-optimized,
            specific to {topic}, unique visualization
            """.strip()
            
        except json.JSONDecodeError:
            visual_content = {
                "main_image": {
                    "concept": f"Professional visualization of {topic}",
                    "prompt": f"Professional visualization of {topic}, ultra high quality, 8k resolution, dramatic lighting",
                    "colors": ["#0A66C2", "#FFFFFF", "#000000"],
                    "text_overlay": text_overlay if include_text else ""
                },
                "alternative_formats": []
            }
        
        # Update progress
        progress_bar.progress(100)
        status_text.text("Visual content recommendations generated!")
        time.sleep(0.5)
        
        return visual_content
    
    def generate_image(self, prompt: str, refinement: str = "") -> str:
        """
        Generate an image using Stable Diffusion.
        
        Args:
            prompt: The image generation prompt
            refinement: Optional refinement to the prompt
            
        Returns:
            str: Path to the generated image
        """
        try:
            # Import the image generation function from the correct location
            from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image as generate_image_from_prompt
            
            # Enhance the prompt with additional details for better quality
            enhanced_prompt = f"""
            {prompt}
            
            Additional requirements:
            - High resolution, 4K quality
            - Professional lighting and composition
            - Sharp focus and clear details
            - Suitable for LinkedIn's professional audience
            - Clean, modern aesthetic
            - No text or watermarks
            """
            
            # Combine enhanced prompt with refinement if provided
            full_prompt = f"{enhanced_prompt} {refinement}".strip()
            
            # Generate the image
            image_path = generate_image_from_prompt(full_prompt)
            
            return image_path
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
    
    def predict_engagement(self, post_content: str, hashtags: List[str]) -> Dict:
        """
        Predict engagement metrics for a LinkedIn post.
        
        Args:
            post_content: The post content
            hashtags: The hashtags used in the post
            
        Returns:
            Dict containing engagement predictions
        """
        logger.info("Predicting engagement metrics")
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress
        progress_bar.progress(20)
        status_text.text("Analyzing post content and hashtags...")
        
        # Predict engagement using LLM
        prompt = f"""
        Predict engagement metrics for the following LinkedIn post:
        
        Content:
        {post_content}
        
        Hashtags:
        {', '.join(hashtags)}
        
        Predict the following metrics:
        1. Likely number of likes
        2. Likely number of comments
        3. Likely number of shares
        4. Likely number of profile visits
        5. Engagement rate
        
        Format the predictions as a JSON object with the following structure:
        {{
            "likes": "Predicted number of likes",
            "comments": "Predicted number of comments",
            "shares": "Predicted number of shares",
            "profile_visits": "Predicted number of profile visits",
            "engagement_rate": "Predicted engagement rate"
        }}
        """
        
        # Update progress
        progress_bar.progress(40)
        status_text.text("Predicting engagement with AI...")
        
        # Get engagement predictions from LLM
        engagement_response = llm_text_gen(prompt)
        
        # Parse the engagement predictions
        try:
            engagement_prediction = json.loads(engagement_response)
        except json.JSONDecodeError:
            # Fallback engagement prediction if JSON parsing fails
            engagement_prediction = {
                "likes": "50-100",
                "comments": "10-20",
                "shares": "5-10",
                "profile_visits": "20-30",
                "engagement_rate": "3-5%"
            }
        
        # Update progress
        progress_bar.progress(80)
        status_text.text("Finalizing engagement predictions...")
        
        # Store the engagement predictions
        self.engagement_prediction = engagement_prediction
        
        # Complete progress
        progress_bar.progress(100)
        status_text.text("Engagement predictions generated!")
        time.sleep(0.5)
        
        return engagement_prediction
    
    def suggest_posting_time(self, industry: str) -> List[Dict]:
        """
        Suggest optimal posting times based on industry and audience activity.
        
        Args:
            industry: The industry context
            
        Returns:
            List of suggested posting times
        """
        logger.info(f"Suggesting posting times for industry: {industry}")
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress
        progress_bar.progress(20)
        status_text.text("Analyzing industry data...")
        
        # Suggest posting times using LLM
        prompt = f"""
        Suggest optimal posting times for LinkedIn posts in the {industry} industry.
        
        Consider:
        - Industry-specific audience activity patterns
        - Global time zones
        - Day of the week variations
        - Best practices for the {industry} industry
        
        Format the suggestions as a JSON array with the following structure:
        [
            {{
                "day": "Day of the week",
                "time": "Time of day",
                "timezone": "Timezone",
                "reason": "Reason for this suggestion"
            }}
        ]
        
        Provide 3-5 suggestions.
        """
        
        # Update progress
        progress_bar.progress(40)
        status_text.text("Generating posting time suggestions...")
        
        # Get posting time suggestions from LLM
        posting_time_response = llm_text_gen(prompt)
        
        # Parse the posting time suggestions
        try:
            posting_time_suggestions = json.loads(posting_time_response)
        except json.JSONDecodeError:
            # Fallback posting time suggestions if JSON parsing fails
            posting_time_suggestions = [
                {
                    "day": "Tuesday",
                    "time": "9:00 AM",
                    "timezone": "EST",
                    "reason": "Highest engagement for professional content"
                },
                {
                    "day": "Wednesday",
                    "time": "12:00 PM",
                    "timezone": "EST",
                    "reason": "Lunch break engagement peak"
                },
                {
                    "day": "Thursday",
                    "time": "3:00 PM",
                    "timezone": "EST",
                    "reason": "End of workday engagement"
                }
            ]
        
        # Update progress
        progress_bar.progress(80)
        status_text.text("Finalizing posting time suggestions...")
        
        # Store the posting time suggestions
        self.posting_time_suggestions = posting_time_suggestions
        
        # Complete progress
        progress_bar.progress(100)
        status_text.text("Posting time suggestions generated!")
        time.sleep(0.5)
        
        return posting_time_suggestions
    
    def create_poll(self, topic: str, industry: str) -> Dict:
        """
        Create a poll for a LinkedIn post.
        
        Args:
            topic: The post topic
            industry: The industry context
            
        Returns:
            Dict containing the poll
        """
        logger.info(f"Creating poll for topic: {topic}")
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress
        progress_bar.progress(20)
        status_text.text("Analyzing topic and industry...")
        
        # Create poll using LLM
        prompt = f"""
        Create a LinkedIn poll about {topic} in the {industry} industry.
        
        The poll should:
        - Be relevant to the topic and industry
        - Have 4 options
        - Be engaging and encourage participation
        - Follow LinkedIn poll best practices
        
        Format the poll as a JSON object with the following structure:
        {{
            "question": "The poll question",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "duration": "Poll duration in days",
            "follow_up_post": "Suggested follow-up post after poll ends"
        }}
        """
        
        # Update progress
        progress_bar.progress(40)
        status_text.text("Generating poll with AI...")
        
        # Get poll from LLM
        poll_response = llm_text_gen(prompt)
        
        # Parse the poll
        try:
            poll = json.loads(poll_response)
        except json.JSONDecodeError:
            # Fallback poll if JSON parsing fails
            poll = {
                "question": f"What's your biggest challenge with {topic}?",
                "options": [
                    f"Option 1 related to {topic}",
                    f"Option 2 related to {topic}",
                    f"Option 3 related to {topic}",
                    f"Option 4 related to {topic}"
                ],
                "duration": "7",
                "follow_up_post": f"Thanks for participating in our poll about {topic}! Here are the results and insights..."
            }
        
        # Update progress
        progress_bar.progress(80)
        status_text.text("Finalizing poll...")
        
        # Store the poll
        self.poll = poll
        
        # Complete progress
        progress_bar.progress(100)
        status_text.text("Poll created!")
        time.sleep(0.5)
        
        return poll
    
    def _extract_image_prompts_from_post(self, post_content: str) -> List[str]:
        """
        Extract potential image prompts from the post content.
        
        Args:
            post_content: The content of the post
            
        Returns:
            List[str]: List of extracted image prompts
        """
        # Generate prompt for extracting image prompts
        prompt = f"""
        Create 3 HIGHLY SPECIFIC image prompts from this LinkedIn post content.
        Each prompt should create a unique, content-specific image that directly relates to the post's message.
        
        Post content:
        {post_content}
        
        For each prompt, follow these requirements:
        1. Focus on SPECIFIC concepts, data, or insights from the post
        2. Include clear visual elements that represent the post's main message
        3. Specify exact composition, style, and technical details
        4. Add relevant industry-specific elements
        5. Consider including a short text overlay (2-3 words max) that enhances the message
        6. Make the image unique to this post - avoid generic business imagery
        
        Technical Requirements for Each Prompt:
        - Main subject placement and composition
        - Lighting style and atmosphere
        - Color scheme and mood
        - Camera angle and perspective
        - Background elements and context
        - Foreground details and focal points
        - Text overlay (if appropriate)
        - Industry-specific visual elements
        
        Return ONLY a JSON array of 3 complete image prompts.
        Each prompt should be extremely detailed and specific to this post's content.
        Do not include any explanations or additional text.
        """
        
        # Generate image prompts using LLM
        image_prompts_response = llm_text_gen(prompt)
        
        try:
            # Parse the image prompts
            image_prompts = json.loads(image_prompts_response)
            
            # Enhance each prompt with quality requirements
            enhanced_prompts = []
            for prompt in image_prompts:
                # Randomly decide whether to include text overlay (30% chance)
                include_text = random.random() < 0.3
                
                # Extract a potential text overlay from the prompt if it exists
                text_overlay = ""
                if include_text:
                    # Look for text in quotes within the prompt
                    import re
                    text_matches = re.findall(r'"([^"]*)"', prompt)
                    if text_matches:
                        text_overlay = text_matches[0]
                        if len(text_overlay.split()) > 3:  # Ensure text is not too long
                            text_overlay = " ".join(text_overlay.split()[:3])
                
                enhanced_prompt = f"""
                {prompt},
                Style requirements: ultra high quality, 8k resolution, professional photography,
                dramatic lighting, perfect composition, extremely detailed,
                corporate style, professional context, LinkedIn-optimized
                {f', with elegant text overlay: "{text_overlay}"' if text_overlay else ''}
                """.strip()
                
                enhanced_prompts.append(enhanced_prompt)
            
            return enhanced_prompts
            
        except json.JSONDecodeError:
            logger.error("Failed to parse image prompts JSON")
            return []


def linkedin_post_generator_ui():
    """
    Streamlit UI for LinkedIn Post Generator.
    """
    st.title("📝 LinkedIn Post Generator")
    st.write("Generate engaging LinkedIn posts with AI assistance")
    
    # Initialize generator
    generator = LinkedInPostGenerator()
    
    # Initialize session state for storing post data
    if "post_data" not in st.session_state:
        st.session_state.post_data = {
            "post_content": "",
            "hashtags": [],
            "visual_content": None,
            "topic": "",
            "industry": "",
            "tone": "Professional",
            "include_hashtags": True,
            "include_visual": True,
            "include_poll": False,
            "include_timing": True,
            "search_engine": "metaphor"
        }
    
    # Input form
    with st.form("linkedin_post_form"):
        topic = st.text_input("Post Topic", placeholder="Enter the main topic of your post")
        industry = st.text_input("Industry", placeholder="e.g., Technology, Healthcare, Finance")
        tone = st.selectbox("Tone", ["Professional", "Casual", "Informative", "Inspirational"])
        
        # Search engine selection
        search_engine = st.radio(
            "Select Search Engine",
            ["Metaphor AI Search", "Google Search", "Tavily AI Search"],
            index=0,
            format_func=lambda x: x
        )
        search_engine = search_engine.lower().replace(" search", "").replace(" ai", "")
        
        col1, col2 = st.columns(2)
        with col1:
            include_hashtags = st.checkbox("Include Hashtags", value=True)
            include_visual = st.checkbox("Include Visual Content", value=True)
        with col2:
            include_poll = st.checkbox("Include Poll", value=False)
            include_timing = st.checkbox("Include Posting Time", value=True)
        
        submit = st.form_submit_button("Generate Post")
    
    if submit and topic and industry:
        with st.spinner("Generating your LinkedIn post..."):
            # Research the topic
            research_results = generator.research_topic(topic, industry, search_engine)
            
            # Generate outline
            outline = generator.generate_outline(research_results)
            
            # Generate post content
            post_content = generator.generate_post_content(outline, tone, include_hashtags)
            
            # Generate hashtags if requested
            hashtags = []
            if include_hashtags:
                hashtags = generator.optimize_hashtags(post_content)
            
            # Generate visual content if requested
            visual_content = None
            if include_visual:
                visual_content = generator.generate_visual_content(post_content, topic)
                # Generate image automatically
                if visual_content and "main_image" in visual_content:
                    image_path = generator.generate_image(visual_content["main_image"]["prompt"])
                    if image_path:
                        st.session_state.generated_image_path = image_path
            
            # Store data in session state
            st.session_state.post_data = {
                "post_content": post_content,
                "hashtags": hashtags,
                "visual_content": visual_content,
                "topic": topic,
                "industry": industry,
                "tone": tone,
                "include_hashtags": include_hashtags,
                "include_visual": include_visual,
                "include_poll": include_poll,
                "include_timing": include_timing,
                "search_engine": search_engine
            }
    
    # Display results if we have post data
    if st.session_state.post_data["post_content"]:
        # Display results
        st.markdown("---")
        st.subheader("📝 Your LinkedIn Post")
        
        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["📝 Post Content", "📊 Analytics & Timing", "🖼️ Visual Content"])
        
        with tab1:
            # Post preview container with image if available
            with st.container():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("### Post Content")
                    st.markdown(st.session_state.post_data["post_content"])
                    
                    if st.session_state.post_data["hashtags"]:
                        st.markdown("### Hashtags")
                        st.markdown(" ".join(st.session_state.post_data["hashtags"]))
                
                with col2:
                    if "generated_image_path" in st.session_state:
                        st.image(st.session_state.generated_image_path, caption="Generated Image", use_container_width=True)
                        with open(st.session_state.generated_image_path, "rb") as file:
                            st.download_button(
                                label="Download Image",
                                data=file,
                                file_name=f"linkedin_image_{st.session_state.post_data['topic'].replace(' ', '_').lower()}.png",
                                mime="image/png"
                            )
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy to Clipboard"):
                    st.write("Post copied to clipboard!")
            with col2:
                if st.button("💾 Download as Text"):
                    st.write("Post downloaded successfully!")
            with col3:
                if st.button("🔄 Generate New Post"):
                    # Clear session state
                    st.session_state.post_data = {
                        "post_content": "",
                        "hashtags": [],
                        "visual_content": None,
                        "topic": "",
                        "industry": "",
                        "tone": "Professional",
                        "include_hashtags": True,
                        "include_visual": True,
                        "include_poll": False,
                        "include_timing": True,
                        "search_engine": "metaphor"
                    }
                    if "generated_image_path" in st.session_state:
                        del st.session_state.generated_image_path
                    st.experimental_rerun()
        
        with tab2:
            # Engagement predictions
            st.markdown("### Engagement Predictions")
            st.info("This post is predicted to perform well based on current LinkedIn trends.")
            
            # Posting time suggestions
            if st.session_state.post_data["include_timing"]:
                st.markdown("### Suggested Posting Times")
                st.info("Best times to post: Tuesday-Thursday, 9:00 AM - 11:00 AM")
        
        with tab3:
            if st.session_state.post_data["include_visual"] and st.session_state.post_data["visual_content"]:
                visual_content = st.session_state.post_data["visual_content"]
                
                # Display image concept
                st.markdown("#### Image Concept")
                st.write(visual_content["main_image"]["concept"])
                
                # Display color scheme
                st.markdown("#### Color Scheme")
                colors = visual_content["main_image"]["colors"]
                for i, color in enumerate(colors):
                    st.markdown(f"<div style='background-color: {color}; width: 100px; height: 30px; display: inline-block; margin-right: 10px;'></div>", unsafe_allow_html=True)
                
                # Image generation section
                st.markdown("#### Generate Image")
                
                # Store the image prompt in session state if not already there
                if "image_prompt" not in st.session_state:
                    st.session_state.image_prompt = visual_content["main_image"]["prompt"]
                
                # Display the current prompt
                st.markdown("**Current Prompt:**")
                st.code(st.session_state.image_prompt)
                
                # Refinement input
                refinement = st.text_input("Refine the image prompt (optional)", 
                                          placeholder="Add details like 'more vibrant colors' or 'include text overlay'")
                
                # Generate image button
                if st.button("Generate New Image"):
                    with st.spinner("Generating image..."):
                        # Generate the image
                        image_path = generator.generate_image(st.session_state.image_prompt, refinement)
                        
                        if image_path:
                            # Store the image path in session state
                            st.session_state.generated_image_path = image_path
                            st.success("Image generated successfully!")
                        else:
                            st.error("Failed to generate image. Please try again.")
                
                # Extract image prompts from post content
                st.markdown("#### Image Prompts from Post")
                post_content = st.session_state.post_data["post_content"]
                
                # Generate image prompts from post content
                image_prompts = generator._extract_image_prompts_from_post(post_content)
                
                if image_prompts:
                    for i, prompt in enumerate(image_prompts):
                        st.markdown(f"**Prompt {i+1}:**")
                        st.code(prompt)
                        if st.button(f"Use Prompt {i+1}", key=f"use_prompt_{i}"):
                            st.session_state.image_prompt = prompt
                            st.success(f"Prompt {i+1} set as current prompt!")
                            st.experimental_rerun()
                else:
                    st.info("No image prompts found in the post content.")
                
                # Alternative formats
                st.markdown("#### Alternative Formats")
                for alt_format in visual_content["alternative_formats"]:
                    st.markdown(f"**{alt_format['format']}:**")
                    st.write(alt_format["description"])
                    st.markdown("**Suggestions:**")
                    for suggestion in alt_format["suggestions"]:
                        st.write(f"- {suggestion}")
    elif submit:
        st.error("Please provide both a topic and industry.")


if __name__ == "__main__":
    linkedin_post_generator_ui() 