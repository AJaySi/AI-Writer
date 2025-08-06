"""
LinkedIn Company Page Content Generator

This module provides the core functionality for generating and optimizing LinkedIn company page content.
"""

import json
from typing import Dict, List, Optional, Union
from loguru import logger

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....ai_web_researcher.gpt_online_researcher import do_google_serp_search
from .....ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles
from .....ai_web_researcher.tavily_ai_search import do_tavily_ai_search
from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

class LinkedInCompanyPageGenerator:
    """Main class for generating LinkedIn company page content."""
    
    def __init__(self):
        """Initialize the LinkedIn Company Page Generator."""
        self.company_info = {}
        self.brand_voice = {}
        self.content_history = []
    
    async def optimize_company_profile(
        self,
        company_name: str,
        industry: str,
        target_audience: List[str],
        brand_voice: str,
        key_products: List[str],
        company_size: str,
        company_description: str
    ) -> Dict[str, str]:
        """
        Optimize the company profile content for LinkedIn.
        
        Args:
            company_name: Name of the company
            industry: Industry sector
            target_audience: List of target audience segments
            brand_voice: Desired brand voice/tone
            key_products: List of key products/services
            company_size: Size of the company
            company_description: Current company description
            
        Returns:
            Dict containing optimized profile sections
        """
        try:
            # Store company info for future content generation
            self.company_info = {
                "name": company_name,
                "industry": industry,
                "target_audience": target_audience,
                "brand_voice": brand_voice,
                "key_products": key_products,
                "size": company_size,
                "description": company_description
            }
            
            # Create the prompt for profile optimization
            prompt = f"""
            Optimize the LinkedIn company profile for {company_name}, a {company_size} company in the {industry} industry.
            
            Current Description:
            {company_description}
            
            Key Products/Services:
            {', '.join(key_products)}
            
            Target Audience:
            {', '.join(target_audience)}
            
            Brand Voice:
            {brand_voice}
            
            Generate a comprehensive LinkedIn company profile with the following sections:
            1. Company Overview
            2. Mission Statement
            3. Value Proposition
            4. Industry Expertise
            5. Company Culture
            6. Products/Services Overview
            
            Ensure the content:
            - Maintains the specified brand voice
            - Targets the identified audience segments
            - Highlights key products/services
            - Optimizes for LinkedIn's algorithm
            - Includes relevant industry keywords
            - Maintains professional tone
            """
            
            # Define the JSON structure for the response
            json_struct = {
                "company_overview": "string",
                "mission_statement": "string",
                "value_proposition": "string",
                "industry_expertise": "string",
                "company_culture": "string",
                "products_services_overview": "string",
                "recommended_hashtags": ["string"],
                "seo_keywords": ["string"]
            }
            
            # Generate the optimized profile content
            response = await llm_text_gen(
                prompt=prompt,
                json_struct=json_struct,
                temperature=0.7
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error optimizing company profile: {str(e)}")
            raise
    
    async def generate_company_update(
        self,
        update_type: str,
        topic: str,
        target_audience: Optional[List[str]] = None,
        include_hashtags: bool = True,
        include_cta: bool = True
    ) -> Dict[str, str]:
        """
        Generate a company update post for LinkedIn.
        
        Args:
            update_type: Type of update (product_launch, milestone, news, etc.)
            topic: Main topic or focus of the update
            target_audience: Optional list of target audience segments
            include_hashtags: Whether to include hashtags
            include_cta: Whether to include a call-to-action
            
        Returns:
            Dict containing the generated update content
        """
        try:
            # Use company info if target audience not specified
            if not target_audience:
                target_audience = self.company_info.get("target_audience", [])
            
            # Create the prompt for update generation
            prompt = f"""
            Generate a LinkedIn company update post for {self.company_info['name']} about {topic}.
            
            Update Type: {update_type}
            Target Audience: {', '.join(target_audience)}
            Brand Voice: {self.company_info['brand_voice']}
            
            The post should:
            - Be engaging and professional
            - Include relevant industry context
            - Highlight the company's expertise
            - Drive meaningful engagement
            - Be optimized for LinkedIn's algorithm
            """
            
            if include_hashtags:
                prompt += "\n- Include 3-5 relevant hashtags"
            
            if include_cta:
                prompt += "\n- Include a clear call-to-action"
            
            # Define the JSON structure for the response
            json_struct = {
                "post_content": "string",
                "hashtags": ["string"],
                "call_to_action": "string",
                "suggested_image_prompt": "string",
                "engagement_tips": ["string"]
            }
            
            # Generate the update content
            response = await llm_text_gen(
                prompt=prompt,
                json_struct=json_struct,
                temperature=0.7
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating company update: {str(e)}")
            raise
    
    async def generate_employee_spotlight(
        self,
        employee_name: str,
        role: str,
        achievements: List[str],
        spotlight_type: str = "general"
    ) -> Dict[str, str]:
        """
        Generate an employee spotlight post for LinkedIn.
        
        Args:
            employee_name: Name of the employee
            role: Employee's role
            achievements: List of key achievements
            spotlight_type: Type of spotlight (general, leadership, innovation, etc.)
            
        Returns:
            Dict containing the generated spotlight content
        """
        try:
            # Create the prompt for spotlight generation
            prompt = f"""
            Generate a LinkedIn employee spotlight post for {employee_name}, {role} at {self.company_info['name']}.
            
            Spotlight Type: {spotlight_type}
            Key Achievements:
            {chr(10).join(f'- {achievement}' for achievement in achievements)}
            
            Company Context:
            Industry: {self.company_info['industry']}
            Brand Voice: {self.company_info['brand_voice']}
            
            The post should:
            - Highlight the employee's contributions
            - Showcase company culture
            - Be engaging and professional
            - Include relevant industry context
            - Drive meaningful engagement
            """
            
            # Define the JSON structure for the response
            json_struct = {
                "spotlight_content": "string",
                "hashtags": ["string"],
                "call_to_action": "string",
                "suggested_image_prompt": "string",
                "engagement_tips": ["string"]
            }
            
            # Generate the spotlight content
            response = await llm_text_gen(
                prompt=prompt,
                json_struct=json_struct,
                temperature=0.7
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating employee spotlight: {str(e)}")
            raise
    
    async def generate_industry_content(
        self,
        content_type: str,
        topic: str,
        target_audience: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Generate industry-focused content for LinkedIn.
        
        Args:
            content_type: Type of content (insight, trend, analysis, etc.)
            topic: Main topic or focus
            target_audience: Optional list of target audience segments
            
        Returns:
            Dict containing the generated content
        """
        try:
            # Use company info if target audience not specified
            if not target_audience:
                target_audience = self.company_info.get("target_audience", [])
            
            # Research industry trends and insights
            research_results = await do_tavily_ai_search(
                query=f"{topic} in {self.company_info['industry']} industry trends insights",
                search_depth="advanced"
            )
            
            # Create the prompt for content generation
            prompt = f"""
            Generate LinkedIn industry content for {self.company_info['name']} about {topic}.
            
            Content Type: {content_type}
            Target Audience: {', '.join(target_audience)}
            Industry: {self.company_info['industry']}
            Brand Voice: {self.company_info['brand_voice']}
            
            Research Context:
            {research_results}
            
            The content should:
            - Provide valuable industry insights
            - Position the company as a thought leader
            - Be data-driven and professional
            - Drive meaningful engagement
            - Include relevant examples and context
            """
            
            # Define the JSON structure for the response
            json_struct = {
                "content": "string",
                "hashtags": ["string"],
                "call_to_action": "string",
                "suggested_image_prompt": "string",
                "engagement_tips": ["string"],
                "key_insights": ["string"]
            }
            
            # Generate the industry content
            response = await llm_text_gen(
                prompt=prompt,
                json_struct=json_struct,
                temperature=0.7
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating industry content: {str(e)}")
            raise 