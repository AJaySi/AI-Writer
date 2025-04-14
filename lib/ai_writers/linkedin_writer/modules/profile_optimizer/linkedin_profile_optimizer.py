"""
LinkedIn Profile Optimizer

This module provides AI-powered optimization for LinkedIn profiles to improve visibility
and professional appeal.
"""

import json
from typing import Dict, List, Optional
from loguru import logger

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....ai_web_researcher.gpt_online_researcher import do_google_serp_search
from .....ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles
from .....ai_web_researcher.tavily_ai_search import do_tavily_ai_search

class LinkedInProfileOptimizer:
    """
    AI-powered LinkedIn Profile Optimizer that enhances profiles for better visibility
    and professional appeal.
    """
    
    def __init__(self):
        """Initialize the LinkedIn Profile Optimizer."""
        self.industry_keywords = {}
        self.seo_patterns = {}
        self.profile_sections = [
            "headline",
            "about",
            "experience",
            "skills",
            "projects",
            "endorsements",
            "summary",
            "custom_url"
        ]
    
    async def optimize_headline(self, current_headline: str, industry: str, role: str) -> Dict:
        """
        Optimize the LinkedIn headline for better visibility and impact.
        
        Args:
            current_headline: Current LinkedIn headline
            industry: User's industry
            role: User's current or target role
            
        Returns:
            Dict containing optimized headline and explanation
        """
        prompt = f"""
        As an expert LinkedIn profile optimizer, enhance this headline for maximum impact and visibility:
        Current Headline: {current_headline}
        Industry: {industry}
        Role: {role}
        
        Consider:
        - Including relevant keywords for {industry}
        - Highlighting unique value proposition
        - Using industry-standard titles
        - Incorporating achievements or specialties
        - Keeping it under LinkedIn's character limit
        
        Return a JSON with:
        - optimized_headline: The enhanced headline
        - explanation: Why changes were made
        - keywords_used: Key terms included
        """
        
        response = await llm_text_gen(prompt)
        return json.loads(response)
    
    async def generate_about_section(self, 
        current_about: str,
        experience: List[Dict],
        achievements: List[str],
        target_audience: str
    ) -> Dict:
        """
        Generate an optimized About section.
        
        Args:
            current_about: Current About section content
            experience: List of work experiences
            achievements: List of key achievements
            target_audience: Intended profile visitors
            
        Returns:
            Dict containing new About section and explanation
        """
        prompt = f"""
        As an expert LinkedIn profile writer, create an engaging About section that showcases professional value:
        
        Current About: {current_about}
        Key Experiences: {json.dumps(experience)}
        Achievements: {json.dumps(achievements)}
        Target Audience: {target_audience}
        
        Consider:
        - Strong opening hook
        - Professional journey narrative
        - Key achievements and impact
        - Industry expertise
        - Call to action
        - Proper formatting and structure
        
        Return a JSON with:
        - about_section: The optimized content
        - structure_explanation: Section breakdown
        - impact_factors: Key elements that drive engagement
        """
        
        response = await llm_text_gen(prompt)
        return json.loads(response)
    
    async def enhance_experience_descriptions(self,
        experiences: List[Dict]
    ) -> List[Dict]:
        """
        Enhance work experience descriptions for better impact.
        
        Args:
            experiences: List of work experiences with roles and descriptions
            
        Returns:
            List of enhanced experience descriptions
        """
        enhanced_experiences = []
        
        for exp in experiences:
            prompt = f"""
            As an expert LinkedIn profile writer, enhance this work experience description:
            
            Role: {exp.get('role')}
            Company: {exp.get('company')}
            Current Description: {exp.get('description')}
            
            Enhance the description to:
            - Lead with strong action verbs
            - Include quantifiable achievements
            - Highlight key responsibilities
            - Incorporate relevant keywords
            - Use proper formatting
            
            Return a JSON with:
            - enhanced_description: The improved description
            - achievements_highlighted: Key accomplishments
            - keywords_used: Industry terms included
            """
            
            response = await llm_text_gen(prompt)
            enhanced_exp = json.loads(response)
            enhanced_experiences.append({
                **exp,
                'enhanced_description': enhanced_exp['enhanced_description'],
                'achievements': enhanced_exp['achievements_highlighted'],
                'keywords': enhanced_exp['keywords_used']
            })
        
        return enhanced_experiences
    
    async def recommend_skills(self,
        current_skills: List[str],
        industry: str,
        role: str
    ) -> Dict:
        """
        Recommend relevant skills based on industry and role.
        
        Args:
            current_skills: List of current skills
            industry: User's industry
            role: User's role
            
        Returns:
            Dict containing skill recommendations
        """
        # Research trending skills in the industry
        industry_research = await do_tavily_ai_search(
            f"most in-demand skills for {role} in {industry} LinkedIn 2024"
        )
        
        prompt = f"""
        As a LinkedIn profile optimization expert, recommend skills based on:
        
        Current Skills: {json.dumps(current_skills)}
        Industry: {industry}
        Role: {role}
        Industry Research: {json.dumps(industry_research)}
        
        Provide:
        - Must-have technical skills
        - Important soft skills
        - Trending skills in the industry
        - Skills to remove (if any)
        
        Return a JSON with:
        - recommended_skills: New skills to add
        - skills_to_remove: Skills to consider removing
        - skill_categories: Grouping of skills by category
        - trending_skills: Currently popular skills
        """
        
        response = await llm_text_gen(prompt)
        return json.loads(response)
    
    async def analyze_profile_strength(self,
        profile_data: Dict
    ) -> Dict:
        """
        Analyze overall profile strength and provide improvement recommendations.
        
        Args:
            profile_data: Complete profile information
            
        Returns:
            Dict containing analysis and recommendations
        """
        prompt = f"""
        As a LinkedIn profile optimization expert, analyze this profile:
        
        Profile Data: {json.dumps(profile_data)}
        
        Provide a comprehensive analysis including:
        - Overall profile strength score
        - Section-by-section analysis
        - Missing elements
        - Improvement opportunities
        - SEO optimization suggestions
        - Engagement potential
        
        Return a JSON with:
        - strength_score: 0-100 rating
        - section_scores: Individual section ratings
        - missing_elements: Key missing components
        - priority_improvements: Ordered list of suggestions
        - seo_recommendations: Keyword and optimization tips
        """
        
        response = await llm_text_gen(prompt)
        return json.loads(response) 