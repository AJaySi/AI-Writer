"""
LinkedIn Article Generator

This module provides functionality for generating LinkedIn articles with research-backed content,
AI-generated images, and SEO optimization.
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


class LinkedInArticleGenerator:
    """
    A class for generating LinkedIn articles with research-backed content.
    
    This class provides methods for:
    - Researching topics using multiple search engines (Metaphor, Google, Tavily)
    - Generating detailed article outlines
    - Creating comprehensive article content
    - Generating section-specific images
    - Adding SEO optimization
    - Suggesting engagement strategies
    """
    
    def __init__(self):
        """Initialize the LinkedIn Article Generator."""
        self.research_results = {}
        self.outline = {}
        self.article_content = ""
        self.seo_metadata = {}
        self.section_images = []
        self.engagement_strategy = {}
    
    def research_topic(self, topic: str, industry: str, search_engine: str = "metaphor", status_container=None) -> Dict:
        """
        Research a topic using the selected search engine.
        """
        # Update progress
        if status_container:
            status_container.text(f"🔍 Researching {topic} in {industry} using {search_engine.title()}...")
        
        # Construct focused search query
        search_query = f"""
        Find detailed professional articles about '{topic}' in the {industry} industry.
        Focus on:
        - Latest industry developments
        - Expert insights and analysis
        - Real-world case studies
        - Practical applications
        - Industry-specific statistics
        - Best practices and strategies
        """
        
        # Research with selected search engine
        research_results = None
        
        # Create tabs for displaying results
        search_tabs = st.tabs([
            "🔍 Research Results",
            "📊 Topic Analysis",
            "📝 Key Insights"
        ])
        
        with search_tabs[0]:
            st.markdown(f"### Research on: {topic}")
            st.markdown(f"*Industry Context: {industry}*")
            
            if search_engine == "metaphor":
                research_results = self._research_with_metaphor(search_query, industry, status_container)
            elif search_engine == "google":
                research_results = self._research_with_google(search_query, industry, status_container)
            elif search_engine == "tavily":
                research_results = self._research_with_tavily(search_query, industry, status_container)
        
        # Analyze research results with topic focus
        with search_tabs[1]:
            st.markdown("### Topic Analysis")
            combined_results = self._analyze_research_results(research_results, topic, industry)
            
            # Display analysis in an organized way
            if combined_results:
                # Topic relevance verification
                relevance_prompt = f"""
                Verify the relevance of these research findings to the topic: '{topic}' in {industry} industry.
                
                Key Insights: {combined_results.get('key_insights', [])}
                Statistics: {combined_results.get('statistics', [])}
                Expert Opinions: {combined_results.get('expert_opinions', [])}
                
                Return only the most relevant insights that directly relate to {topic}.
                Remove any generic or tangential information.
                """
                
                verified_results = llm_text_gen(relevance_prompt)
                
                try:
                    verified_data = json.loads(verified_results)
                    combined_results.update(verified_data)
                except:
                    logger.warning("Failed to parse verified results")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"#### Key Insights about {topic}")
                    for insight in combined_results.get("key_insights", []):
                        st.markdown(f"- {insight}")
                    
                    st.markdown("#### Industry-Specific Statistics")
                    for stat in combined_results.get("statistics", []):
                        st.markdown(f"- {stat}")
                
                with col2:
                    st.markdown("#### Expert Perspectives")
                    for opinion in combined_results.get("expert_opinions", []):
                        st.markdown(f"> {opinion}")
                    
                    st.markdown("#### Current Trends")
                    for trend in combined_results.get("trends", []):
                        st.markdown(f"- {trend}")
        
        with search_tabs[2]:
            st.markdown(f"### Key Takeaways for {topic}")
            if combined_results:
                # Topic-focused insights
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Best Practices")
                    for practice in combined_results.get("best_practices", []):
                        st.markdown(f"- {practice}")
                
                with col2:
                    st.markdown("#### Practical Solutions")
                    for solution in combined_results.get("solutions", []):
                        st.markdown(f"- {solution}")
                
                # Industry context
                st.markdown(f"#### {industry} Industry Context")
                st.markdown(combined_results.get("industry_context", ""))
                
                # Verified sources
                st.markdown("#### Expert Sources")
                sources = combined_results.get("sources", [])
                filtered_sources = [s for s in sources if topic.lower() in s.lower()]
                for source in filtered_sources:
                    st.markdown(f"- {source}")
        
        # Update progress
        if status_container:
            status_container.text("✅ Topic research complete!")
        
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
        try:
            # Construct search query
            search_query = f"{topic} in {industry} industry comprehensive article"
            
            # Update progress
            if status_container:
                status_container.text("🔍 Searching with Metaphor...")
            
            # Search with Metaphor
            search_options = {
                "num_results": 15,  # More results for comprehensive research
                "use_autoprompt": True,
                "time_range": "past_year"  # Recent but comprehensive results
            }
            
            metaphor_results = metaphor_search_articles(search_query, search_options)
            
            # Display the results
            if metaphor_results:
                streamlit_display_metaphor_results(metaphor_results, search_query)
            
            # Update progress
            if status_container:
                status_container.text("✅ Metaphor search complete!")
            
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
        try:
            # Update progress
            if status_container:
                status_container.text("🔍 Searching with Google...")
            
            # Search with Google
            google_results = do_google_serp_search(
                f"{topic} {industry} industry comprehensive guide article",
                num_results=15
            )
            
            # Update progress
            if status_container:
                status_container.text("✅ Google search complete!")
            
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
        try:
            # Update progress
            if status_container:
                status_container.text("🔍 Searching with Tavily AI...")
            
            # Search with Tavily
            search_query = f"{topic} in {industry} industry comprehensive guide"
            tavily_results = do_tavily_ai_search(search_query)
            
            # Display results
            if tavily_results:
                streamlit_display_results(tavily_results)
            
            # Update progress
            if status_container:
                status_container.text("✅ Tavily search complete!")
            
            return tavily_results
            
        except Exception as e:
            logger.error(f"Error in Tavily search: {e}")
            if status_container:
                status_container.text(f"⚠️ Error in Tavily search: {str(e)}")
            return {"sources": []}
    
    def _analyze_research_results(self, research_results: Dict, topic: str, industry: str) -> Dict:
        """
        Analyze research results to extract key insights for article creation.
        
        Args:
            research_results: Results from research
            topic: The topic being researched
            industry: The industry context
            
        Returns:
            Dict containing analyzed insights
        """
        if not research_results:
            logger.warning(f"No research results available for {topic} in {industry}")
            return {
                "key_insights": [],
                "expert_opinions": [],
                "statistics": [],
                "case_studies": [],
                "trends": [],
                "challenges": [],
                "solutions": [],
                "best_practices": [],
                "industry_context": "",
                "sources": []
            }
        
        # Extract content from research results
        sources = []
        content = ""
        
        if isinstance(research_results, dict):
            if "data" in research_results and "results" in research_results["data"]:
                sources = research_results["data"]["results"]
                content = "\n\n".join([
                    f"Title: {source.get('title', '')}\n"
                    f"Content: {source.get('text', '')}\n"
                    f"Summary: {source.get('summary', '')}"
                    for source in sources
                ])
        
        # Generate analysis prompt
        analysis_prompt = f"""
        Analyze this research about {topic} in the {industry} industry for writing a comprehensive LinkedIn article:

        {content}

        Extract and organize the following elements:
        1. Key insights and main arguments
        2. Expert opinions and quotes
        3. Statistics and data points
        4. Case studies and examples
        5. Current trends and future predictions
        6. Common challenges and pain points
        7. Solutions and strategies
        8. Best practices and recommendations
        9. Industry-specific context and implications

        Format as JSON with these keys:
        {{
            "key_insights": ["List of main insights"],
            "expert_opinions": ["List of expert quotes with sources"],
            "statistics": ["List of statistics with sources"],
            "case_studies": ["List of relevant case studies"],
            "trends": ["List of current and emerging trends"],
            "challenges": ["List of common challenges"],
            "solutions": ["List of solutions and strategies"],
            "best_practices": ["List of best practices"],
            "industry_context": "Summary of industry context",
            "sources": ["List of source URLs"]
        }}
        """
        
        # Generate analysis using LLM
        analysis = llm_text_gen(analysis_prompt)
        
        try:
            analysis_dict = json.loads(analysis)
        except json.JSONDecodeError:
            logger.error("Failed to parse analysis JSON")
            analysis_dict = {
                "key_insights": [],
                "expert_opinions": [],
                "statistics": [],
                "case_studies": [],
                "trends": [],
                "challenges": [],
                "solutions": [],
                "best_practices": [],
                "industry_context": "",
                "sources": []
            }
        
        return analysis_dict
    
    def generate_outline(self, research_results: Dict) -> Dict:
        """
        Generate a detailed article outline based on research results.
        """
        # Extract key information from research results
        key_insights = research_results.get("key_insights", [])
        expert_opinions = research_results.get("expert_opinions", [])
        statistics = research_results.get("statistics", [])
        case_studies = research_results.get("case_studies", [])
        trends = research_results.get("trends", [])
        challenges = research_results.get("challenges", [])
        solutions = research_results.get("solutions", [])
        best_practices = research_results.get("best_practices", [])
        industry_context = research_results.get("industry_context", "")
        
        # Generate outline prompt
        outline_prompt = f"""
        Create a professional LinkedIn article outline focused on the exact topic and industry provided.
        
        Research Data:
        Key Insights: {key_insights}
        Expert Opinions: {expert_opinions}
        Statistics: {statistics}
        Case Studies: {case_studies}
        Trends: {trends}
        Challenges: {challenges}
        Solutions: {solutions}
        Best Practices: {best_practices}
        Industry Context: {industry_context}

        Requirements:
        1. Stay strictly focused on the topic without any AI explanations
        2. Create a compelling headline that clearly states the topic's value
        3. Structure 4-5 main sections that logically develop the topic
        4. Include specific places for statistics and expert quotes
        5. Focus on practical insights and actionable takeaways
        6. Maintain professional tone throughout
        7. Ensure each section directly relates to the main topic
        8. Include specific examples and case studies where relevant

        Format as JSON:
        {{
            "headline": "Clear, topic-focused headline",
            "subheadline": "Supporting subheadline that elaborates on the value",
            "introduction": {{
                "hook": "Attention-grabbing opening relevant to topic",
                "context": "Topic-specific background",
                "thesis": "Clear main argument or point"
            }},
            "sections": [
                {{
                    "title": "Section title",
                    "key_points": ["Specific, topic-focused points"],
                    "supporting_evidence": ["Relevant statistics or quotes"],
                    "visual_suggestions": ["Topic-specific visual ideas"]
                }}
            ],
            "conclusion": {{
                "key_takeaways": ["Practical, actionable takeaways"],
                "call_to_action": "Relevant next steps for readers"
            }},
            "seo_keywords": ["Topic-specific keywords"]
        }}
        """
        
        # Generate outline using LLM
        outline = llm_text_gen(outline_prompt)
        
        try:
            outline_dict = json.loads(outline)
        except json.JSONDecodeError:
            logger.error("Failed to parse outline JSON")
            outline_dict = {
                "headline": "",
                "subheadline": "",
                "introduction": {
                    "hook": "",
                    "context": "",
                    "thesis": ""
                },
                "sections": [],
                "conclusion": {
                    "key_takeaways": [],
                    "call_to_action": ""
                },
                "seo_keywords": []
            }
        
        return outline_dict

    def generate_article_content(self, outline: Dict, topic: str, industry: str, tone: str = "professional") -> str:
        """
        Generate comprehensive article content based on the outline.
        """
        # Generate focused article prompt
        article_prompt = f"""
        Write a professional LinkedIn article about '{topic}' in the {industry} industry.
        Follow this outline exactly and stay focused on the specific topic.

        Title: {outline['headline']}
        Subheadline: {outline['subheadline']}

        Introduction:
        Hook: {outline['introduction']['hook']}
        Context: {outline['introduction']['context']}
        Thesis: {outline['introduction']['thesis']}

        Sections:
        {json.dumps(outline['sections'], indent=2)}

        Conclusion:
        Key Takeaways: {outline['conclusion']['key_takeaways']}
        Call to Action: {outline['conclusion']['call_to_action']}

        Critical Requirements:
        1. Write in a {tone} tone appropriate for LinkedIn
        2. Focus EXCLUSIVELY on {topic} - no deviations or tangents
        3. Every paragraph must directly discuss {topic}
        4. Use concrete examples and real-world applications specific to {topic}
        5. Include relevant statistics and expert quotes that directly relate to {topic}
        6. Use clear transitions that maintain focus on {topic}
        7. Provide actionable insights specific to {topic}
        8. Write as an industry expert discussing {topic}
        9. NO meta-commentary, AI explanations, or generic content
        10. Use proper HTML formatting for structure
        11. Every section must explicitly connect to {topic}

        Return ONLY the final article in clean HTML format, ready to publish on LinkedIn.
        The article must read as if written by a {industry} expert focusing solely on {topic}.
        """
        
        # Generate initial article content
        article_content = llm_text_gen(article_prompt)
        
        # Verify topic focus
        verification_prompt = f"""
        Verify this article maintains strict focus on '{topic}' in the {industry} industry.
        
        Requirements:
        1. Every paragraph must explicitly discuss {topic}
        2. Remove any content not directly related to {topic}
        3. Remove any AI explanations or meta-commentary
        4. Ensure all examples and insights are specific to {topic}
        5. Maintain professional {tone} tone
        6. Keep all relevant statistics and expert quotes about {topic}
        
        Return only the verified and cleaned article content.
        """
        
        # Verify and clean the content
        verified_content = llm_text_gen(verification_prompt + "\n\nArticle:\n" + article_content)
        
        # Final topic focus check
        final_check_prompt = f"""
        Perform a final check on this article about '{topic}'.
        
        If you find ANY content that:
        1. Isn't directly about {topic}
        2. Contains AI explanations
        3. Includes meta-commentary
        4. Uses generic examples
        
        Remove or replace it with topic-specific content about {topic}.
        Return only the final, topic-focused article.
        """
        
        final_content = llm_text_gen(final_check_prompt + "\n\nArticle:\n" + verified_content)
        
        return final_content

    def _generate_image_prompt(self, topic: str, article_content: str, industry: str) -> str:
        """
        Generate a detailed image prompt based on the article topic and content.
        """
        prompt_generation = f"""
        Create a specific, detailed image generation prompt for a LinkedIn article about "{topic}" in the {industry} industry.
        
        Article excerpt:
        {article_content[:500]}...
        
        Requirements:
        1. Focus on key concepts and themes from the article
        2. Specify exact visual elements that represent the topic
        3. Include industry-specific imagery and symbols
        4. Define a professional color scheme that matches the topic
        5. Describe specific composition and layout
        6. Include relevant metaphors or visual concepts
        7. Ensure the image will be immediately recognizable as related to {topic}
        8. Avoid generic business imagery
        
        Format:
        1. Main subject/focus
        2. Style and composition
        3. Colors and lighting
        4. Specific elements to include
        5. Industry-specific details
        6. Mood and atmosphere
        
        Return a detailed, topic-specific image generation prompt.
        """
        
        return llm_text_gen(prompt_generation)

    def _suggest_image_variations(self, topic: str, industry: str) -> List[str]:
        """
        Generate alternative image prompt suggestions.
        
        Args:
            topic: The article topic
            industry: The industry context
            
        Returns:
            List[str]: List of alternative image prompts
        """
        variation_prompt = f"""
        Generate 3 different image prompt variations for a LinkedIn article about "{topic}" in the {industry} industry.
        Each prompt should be unique and professional:
        1. A metaphorical/conceptual approach
        2. A data-driven/analytical visualization
        3. A human-centered/storytelling perspective

        Return only the 3 prompts, one per line, no explanations.
        """
        
        variations = llm_text_gen(variation_prompt).strip().split('\n')
        return [v.strip() for v in variations if v.strip()]

    def generate_section_images(self, outline: Dict, article_content: str, topic: str, industry: str) -> List[Dict]:
        """
        Generate image prompts for each section of the article.
        
        Args:
            outline: The article outline
            article_content: The generated article content
            topic: The article topic
            industry: The industry context
            
        Returns:
            List[Dict]: List of image generation prompts for each section
        """
        section_images = []
        
        # Generate main image prompt
        main_prompt = self._generate_image_prompt(topic, article_content, industry)
        alternative_prompts = self._suggest_image_variations(topic, industry)
        
        header_image = {
            "section": "header",
            "main_prompt": main_prompt,
            "alternative_prompts": alternative_prompts
        }
        section_images.append(header_image)
        
        # Generate image prompts for each section
        for section in outline['sections']:
            section_content = section.get('title', '') + ' ' + ' '.join(section.get('key_points', []))
            section_prompt = self._generate_image_prompt(section['title'], section_content, industry)
            
            section_image = {
                "section": section['title'],
                "main_prompt": section_prompt,
                "alternative_prompts": self._suggest_image_variations(section['title'], industry)
            }
            section_images.append(section_image)
        
        return section_images
    
    def generate_seo_metadata(self, article_content: str, outline: Dict) -> Dict:
        """
        Generate SEO metadata for the LinkedIn article.
        
        Args:
            article_content: The generated article content
            outline: The article outline
            
        Returns:
            Dict: SEO metadata including keywords, description, and tags
        """
        seo_prompt = f"""
        Generate SEO metadata for this LinkedIn article:

        Title: {outline['headline']}
        Content: {article_content[:500]}...

        Return a JSON object with:
        1. Focus keyword
        2. Secondary keywords (5-7)
        3. Meta description (150-160 characters)
        4. Article tags (5-7)
        5. Social sharing description
        """
        
        seo_response = llm_text_gen(seo_prompt)
        
        try:
            seo_metadata = json.loads(seo_response)
        except json.JSONDecodeError:
            logger.error("Failed to parse SEO metadata JSON")
            seo_metadata = {
                "focus_keyword": outline['headline'],
                "secondary_keywords": outline.get('seo_keywords', []),
                "meta_description": outline['subheadline'],
                "article_tags": [],
                "social_description": outline['subheadline']
            }
        
        return seo_metadata


def linkedin_article_generator_ui():
    """
    Streamlit UI for LinkedIn Article Generator.
    """
    st.title("📝 LinkedIn Article Generator")
    st.write("Generate comprehensive LinkedIn articles with AI assistance")
    
    # Initialize generator
    generator = LinkedInArticleGenerator()
    
    # Initialize session state
    if "article_data" not in st.session_state:
        st.session_state.article_data = {
            "research_results": None,
            "outline": None,
            "article_content": "",
            "section_images": [],
            "seo_metadata": None,
            "generated_images": {},
            "topic_image": None
        }
    
    # Input form
    with st.form("linkedin_article_form"):
        topic = st.text_input("Article Topic", placeholder="Enter the main topic of your article")
        industry = st.text_input("Industry", placeholder="e.g., Technology, Healthcare, Finance")
        
        col1, col2 = st.columns(2)
        with col1:
            tone = st.selectbox(
                "Writing Tone",
                ["Professional", "Analytical", "Conversational", "Technical", "Thought Leadership"]
            )
        with col2:
            search_engine = st.radio(
                "Research Source",
                ["metaphor", "google", "tavily"],
                format_func=lambda x: {
                    "metaphor": "🔍 Metaphor AI",
                    "google": "🌐 Google Search",
                    "tavily": "🤖 Tavily AI"
                }[x]
            )
        
        # Add option for topic image
        generate_topic_image = st.checkbox("Generate Topic Image", value=True, help="Generate an AI image related to your article topic")
        
        submit = st.form_submit_button("Generate Article")
    
    if submit and topic and industry:
        # Create a status container
        status_container = st.empty()
        
        with st.spinner(f"Researching and generating your article using {search_engine.title()}..."):
            # Generate topic image if requested
            if generate_topic_image:
                status_container.text("🎨 Generating topic image...")
                try:
                    # Generate image prompt
                    image_prompt = f"""Create a professional, LinkedIn-appropriate image for an article about {topic} in the {industry} industry.
                    The image should be:
                    - Professional and business-appropriate
                    - Visually engaging
                    - Relevant to both the topic and industry
                    - Suitable as a LinkedIn article header
                    """
                    
                    # Import the image generation function
                    from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
                    
                    # Generate the image
                    image_path = generate_image(image_prompt)
                    if image_path:
                        st.session_state.article_data["topic_image"] = image_path
                        status_container.success("✅ Topic image generated!")
                except Exception as e:
                    logger.error(f"Error generating topic image: {e}")
                    status_container.error("⚠️ Could not generate topic image. Proceeding with article generation.")
            
            # Research phase
            status_container.text(f"🔍 Phase 1: Researching topic with {search_engine.title()}...")
            research_results = generator.research_topic(topic, industry, search_engine, status_container)
            st.session_state.article_data["research_results"] = research_results
            
            if research_results:
                # Outline phase
                status_container.text("📋 Phase 2: Creating article outline...")
                outline = generator.generate_outline(research_results)
                st.session_state.article_data["outline"] = outline
                
                # Content generation phase
                status_container.text("✍️ Phase 3: Writing article content...")
                article_content = generator.generate_article_content(outline, topic, industry, tone.lower())
                st.session_state.article_data["article_content"] = article_content
                
                # Image generation phase
                status_container.text("🎨 Phase 4: Generating section images...")
                section_images = generator.generate_section_images(outline, article_content, topic, industry)
                st.session_state.article_data["section_images"] = section_images
                
                # SEO optimization phase
                status_container.text("🎯 Phase 5: Optimizing SEO...")
                seo_metadata = generator.generate_seo_metadata(article_content, outline)
                st.session_state.article_data["seo_metadata"] = seo_metadata
                
                status_container.text("✅ Article generation complete!")
            else:
                status_container.error(f"❌ No results found from {search_engine.title()}. Please try a different research source or modify your topic.")
    
    # Display results if we have article data
    if st.session_state.article_data["article_content"]:
        st.markdown("---")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Article Content",
            "🎨 Images & Visuals",
            "🎯 SEO & Metadata",
            "📊 Research Results"
        ])
        
        with tab1:
            # Article preview
            st.subheader("Article Preview")
            
            # Display topic image if available
            if st.session_state.article_data.get("topic_image"):
                st.image(st.session_state.article_data["topic_image"], 
                        caption="Generated Topic Image", 
                        use_container_width=True)
            
            # Add styling for the article container
            st.markdown("""
                <style>
                    .article-container {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                        line-height: 1.6;
                    }
                    .article-container h1 {
                        color: #0A66C2;
                        font-size: 2.5rem;
                        margin-bottom: 1rem;
                    }
                    .article-container h2 {
                        color: #333;
                        font-size: 2rem;
                        margin: 2rem 0 1rem;
                    }
                    .article-container h3 {
                        color: #444;
                        font-size: 1.5rem;
                        margin: 1.5rem 0 1rem;
                    }
                    .article-container p {
                        margin-bottom: 1.2rem;
                        font-size: 1.1rem;
                        color: #2f2f2f;
                    }
                    .article-container ul, .article-container ol {
                        margin: 1rem 0;
                        padding-left: 2rem;
                    }
                    .article-container li {
                        margin-bottom: 0.5rem;
                    }
                    .article-container blockquote {
                        border-left: 4px solid #0A66C2;
                        padding-left: 1rem;
                        margin: 1.5rem 0;
                        color: #555;
                        font-style: italic;
                    }
                </style>
            """, unsafe_allow_html=True)
            
            # Display the article in the styled container
            outline = st.session_state.article_data["outline"]
            st.markdown(f"""
                <div class="article-container">
                    <h1>{outline['headline']}</h1>
                    <h2 style="color: #666; font-size: 1.5rem; margin-bottom: 2rem;">
                        {outline['subheadline']}
                    </h2>
                    {st.session_state.article_data["article_content"]}
                </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy to Clipboard", key="copy_article"):
                    st.success("Article copied to clipboard!")
            with col2:
                if st.button("💾 Download as HTML", key="download_article"):
                    st.success("Article downloaded successfully!")
            with col3:
                if st.button("🔄 Generate New Article", key="new_article"):
                    st.session_state.article_data = {
                        "research_results": None,
                        "outline": None,
                        "article_content": "",
                        "section_images": [],
                        "seo_metadata": None,
                        "generated_images": {},
                        "topic_image": None
                    }
                    st.experimental_rerun()
        
        with tab2:
            st.subheader("Article Images")
            
            # Topic image section
            st.markdown("### 🎨 Main Article Image")
            
            # Display current topic image if available
            if st.session_state.article_data.get("topic_image"):
                st.image(st.session_state.article_data["topic_image"], 
                        caption="Current Article Image", 
                        use_container_width=True)
            
            # Image prompt selection and refinement
            if st.session_state.article_data.get("section_images"):
                header_image = st.session_state.article_data["section_images"][0]
                
                # Display main prompt
                st.markdown("#### Current Image Prompt")
                current_prompt = st.text_area(
                    "Edit prompt if needed:",
                    value=header_image["main_prompt"],
                    height=100,
                    key="main_image_prompt"
                )
                
                # Display alternative prompts
                st.markdown("#### Alternative Prompt Suggestions")
                selected_prompt = st.radio(
                    "Select an alternative prompt or use the current one:",
                    ["Current Prompt"] + header_image["alternative_prompts"],
                    key="prompt_selection"
                )
                
                # Custom prompt input
                custom_prompt = st.text_area(
                    "Or write your own prompt:",
                    value="",
                    height=100,
                    key="custom_image_prompt",
                    help="Write your own custom image prompt based on the article topic"
                )
                
                # Generate image button
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🎨 Generate New Image", key="generate_new_image"):
                        try:
                            # Determine which prompt to use
                            final_prompt = custom_prompt if custom_prompt else (
                                current_prompt if selected_prompt == "Current Prompt"
                                else selected_prompt
                            )
                            
                            # Generate new image
                            from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
                            image_path = generate_image(final_prompt)
                            
                            if image_path:
                                st.session_state.article_data["topic_image"] = image_path
                                st.success("✅ New image generated successfully!")
                                st.experimental_rerun()
                        except Exception as e:
                            st.error(f"⚠️ Error generating image: {str(e)}")
                
                with col2:
                    if st.button("🔄 Generate More Prompt Suggestions", key="generate_more_prompts"):
                        # Generate new variations
                        new_variations = generator._suggest_image_variations(
                            topic,
                            industry
                        )
                        header_image["alternative_prompts"].extend(new_variations)
                        st.success("✅ New prompt suggestions added!")
                        st.experimental_rerun()
            
            # Section images
            st.markdown("### 📑 Section Images")
            if st.session_state.article_data.get("section_images"):
                for section_image in st.session_state.article_data["section_images"][1:]:  # Skip header image
                    with st.expander(f"🖼️ {section_image['section']} Image"):
                        # Display current section image if available
                        if section_image["section"] in st.session_state.article_data["generated_images"]:
                            st.image(
                                st.session_state.article_data["generated_images"][section_image["section"]],
                                caption=f"Current image for {section_image['section']}",
                                use_container_width=True
                            )
                        
                        # Section image prompt and generation
                        section_prompt = st.text_area(
                            "Image prompt:",
                            value=section_image["main_prompt"],
                            height=100,
                            key=f"prompt_{section_image['section']}"
                        )
                        
                        if st.button("Generate Image", key=f"gen_img_{section_image['section']}"):
                            try:
                                from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
                                image_path = generate_image(section_prompt)
                                
                                if image_path:
                                    st.session_state.article_data["generated_images"][section_image["section"]] = image_path
                                    st.success(f"✅ Image generated for {section_image['section']}!")
                                    st.experimental_rerun()
                            except Exception as e:
                                st.error(f"⚠️ Error generating image: {str(e)}")
        
        with tab3:
            st.subheader("SEO Optimization")
            
            seo_metadata = st.session_state.article_data["seo_metadata"]
            
            # Display SEO metadata
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Focus Keyword")
                st.code(seo_metadata["focus_keyword"])
                
                st.markdown("### Secondary Keywords")
                for keyword in seo_metadata["secondary_keywords"]:
                    st.markdown(f"- {keyword}")
            
            with col2:
                st.markdown("### Meta Description")
                st.text_area(
                    label="Meta Description",
                    value=seo_metadata["meta_description"],
                    height=100,
                    disabled=True,
                    key="meta_description_area",
                    label_visibility="collapsed"
                )
                
                st.markdown("### Article Tags")
                for tag in seo_metadata["article_tags"]:
                    st.markdown(f"- {tag}")
            
            st.markdown("### Social Sharing Description")
            st.text_area(
                label="Social Sharing Description",
                value=seo_metadata["social_description"],
                height=100,
                disabled=True,
                key="social_description_area",
                label_visibility="collapsed"
            )
        
        with tab4:
            st.subheader("Research Results")
            
            research_results = st.session_state.article_data["research_results"]
            
            # Display key insights
            st.markdown("### Key Insights")
            for insight in research_results["key_insights"]:
                st.markdown(f"- {insight}")
            
            # Display statistics
            st.markdown("### Statistics & Data Points")
            for stat in research_results["statistics"]:
                st.markdown(f"- {stat}")
            
            # Display expert opinions
            st.markdown("### Expert Opinions")
            for opinion in research_results["expert_opinions"]:
                st.markdown(f"> {opinion}")
            
            # Display sources
            st.markdown("### Sources")
            for source in research_results["sources"]:
                st.markdown(f"- {source}")


if __name__ == "__main__":
    linkedin_article_generator_ui() 