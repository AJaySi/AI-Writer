"""
LinkedIn Video Script Generator

This module provides functionality for generating professional video scripts
for LinkedIn content with AI-powered optimization and engagement features.
"""

import streamlit as st
import json
from typing import Dict, List, Optional, Union
from loguru import logger

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....ai_web_researcher.gpt_online_researcher import do_google_serp_search
from .....ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles
from .....ai_web_researcher.tavily_ai_search import do_tavily_ai_search


class LinkedInVideoScriptGenerator:
    """
    AI-powered LinkedIn video script generator that creates engaging scripts with
    hooks, story structure, and visual suggestions.
    """
    
    def __init__(self):
        """Initialize the LinkedIn Video Script Generator."""
        self.video_types = {
            "thought_leadership": "Thought Leadership",
            "tutorial": "Tutorial/How-to",
            "product_demo": "Product Demo",
            "company_culture": "Company Culture",
            "industry_insights": "Industry Insights",
            "event_highlights": "Event Highlights",
            "customer_story": "Customer Story",
            "behind_scenes": "Behind the Scenes"
        }
        
        self.video_lengths = {
            "short": "Short (< 1 minute)",
            "medium": "Medium (1-3 minutes)",
            "long": "Long (3-5 minutes)",
            "extended": "Extended (5+ minutes)"
        }
        
        self.tone_options = {
            "professional": "Professional & Authoritative",
            "conversational": "Conversational & Friendly",
            "educational": "Educational & Informative",
            "inspirational": "Inspirational & Motivational",
            "storytelling": "Storytelling & Narrative"
        }
        
        self.target_audiences = {
            "professionals": "Industry Professionals",
            "decision_makers": "Decision Makers",
            "job_seekers": "Job Seekers",
            "students": "Students & Early Career",
            "entrepreneurs": "Entrepreneurs & Business Owners",
            "general": "General Professional Network"
        }

    def research_topic(self, topic: str, industry: str, search_engine: str = "metaphor") -> Dict:
        """
        Research a topic to gather insights for video content.
        
        Args:
            topic: The main topic for the video
            industry: The target industry
            search_engine: The search engine to use (metaphor, google, tavily)
            
        Returns:
            Dict containing research results and insights
        """
        try:
            search_query = f"{topic} {industry} trends insights best practices"
            
            if search_engine == "metaphor":
                articles = metaphor_search_articles(search_query)
            elif search_engine == "google":
                articles = do_google_serp_search(search_query)
            elif search_engine == "tavily":
                articles = do_tavily_ai_search(search_query)
            else:
                raise ValueError(f"Unsupported search engine: {search_engine}")
            
            insights, trends = self._extract_insights_and_trends(articles)
            
            return {
                "articles": articles,
                "insights": insights,
                "trends": trends
            }
            
        except Exception as e:
            logger.error(f"Error researching topic: {str(e)}")
            return {
                "articles": [],
                "insights": [],
                "trends": []
            }

    def _extract_insights_and_trends(self, articles: List[Dict]) -> tuple[List[str], List[str]]:
        """Extract key insights and trends from research articles."""
        try:
            prompt = f"""
            Based on the following articles, extract:
            1. Key insights relevant for a video script
            2. Current trends in the industry
            
            Articles:
            {json.dumps(articles, indent=2)}
            
            Return a JSON with two lists: 'insights' and 'trends'
            """
            
            response = llm_text_gen(prompt)
            result = json.loads(response)
            
            return result.get("insights", []), result.get("trends", [])
            
        except Exception as e:
            logger.error(f"Error extracting insights and trends: {str(e)}")
            return [], []

    def generate_hook(self, topic: str, video_type: str, target_audience: str, tone: str) -> str:
        """
        Generate an attention-grabbing hook for the video.
        
        Args:
            topic: The main topic of the video
            video_type: Type of video content
            target_audience: Target audience for the video
            tone: Desired tone of the hook
            
        Returns:
            str: The generated hook
        """
        try:
            prompt = f"""
            Create an attention-grabbing hook for a LinkedIn video with:
            - Topic: {topic}
            - Video Type: {self.video_types[video_type]}
            - Target Audience: {self.target_audiences[target_audience]}
            - Tone: {self.tone_options[tone]}
            
            The hook should be:
            1. Under 15 seconds when spoken
            2. Immediately capture attention
            3. Clear value proposition
            4. Professional and engaging
            
            Return only the hook text.
            """
            
            return llm_text_gen(prompt)
            
        except Exception as e:
            logger.error(f"Error generating hook: {str(e)}")
            return ""

    def generate_story_structure(self, topic: str, video_type: str, length: str, insights: List[str]) -> Dict:
        """
        Generate a structured outline for the video.
        
        Args:
            topic: Main topic of the video
            video_type: Type of video content
            length: Target video length
            insights: Research insights to incorporate
            
        Returns:
            Dict containing the story structure
        """
        try:
            prompt = f"""
            Create a professional video script structure for LinkedIn with:
            - Topic: {topic}
            - Video Type: {self.video_types[video_type]}
            - Length: {self.video_lengths[length]}
            - Key Insights: {json.dumps(insights)}
            
            Return a JSON with:
            1. sections: List of sections with timing and content
            2. transitions: List of smooth transitions
            3. key_points: Main points to emphasize
            4. pacing_notes: Guidance on pacing and delivery
            """
            
            response = llm_text_gen(prompt)
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Error generating story structure: {str(e)}")
            return {
                "sections": [],
                "transitions": [],
                "key_points": [],
                "pacing_notes": []
            }

    def generate_visual_cues(self, script_sections: List[Dict]) -> List[Dict]:
        """
        Generate visual suggestions for each section of the script.
        
        Args:
            script_sections: List of script sections
            
        Returns:
            List of visual cue suggestions
        """
        try:
            prompt = f"""
            For each section of the LinkedIn video script, suggest visual elements:
            
            Script Sections:
            {json.dumps(script_sections, indent=2)}
            
            For each section, provide:
            1. Visual type (b-roll, graphics, text overlay, etc.)
            2. Description of visual content
            3. Timing and duration
            4. Visual transitions
            
            Return a JSON array of visual suggestions.
            """
            
            response = llm_text_gen(prompt)
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Error generating visual cues: {str(e)}")
            return []

    def generate_full_script(self, topic: str, video_type: str, length: str, 
                           target_audience: str, tone: str, insights: List[str]) -> Dict:
        """
        Generate a complete video script with all components.
        
        Args:
            topic: Main topic of the video
            video_type: Type of video content
            length: Target video length
            target_audience: Target audience
            tone: Desired tone
            insights: Research insights
            
        Returns:
            Dict containing the complete script
        """
        try:
            # Generate hook
            hook = self.generate_hook(topic, video_type, target_audience, tone)
            
            # Generate story structure
            structure = self.generate_story_structure(topic, video_type, length, insights)
            
            # Generate visual cues
            visuals = self.generate_visual_cues(structure["sections"])
            
            # Generate call-to-action
            cta = self.generate_cta(topic, video_type, target_audience)
            
            # Combine all components
            script = {
                "metadata": {
                    "topic": topic,
                    "video_type": video_type,
                    "length": length,
                    "target_audience": target_audience,
                    "tone": tone
                },
                "hook": hook,
                "structure": structure,
                "visuals": visuals,
                "cta": cta
            }
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating full script: {str(e)}")
            return {}

    def generate_cta(self, topic: str, video_type: str, target_audience: str) -> Dict:
        """Generate an effective call-to-action."""
        try:
            prompt = f"""
            Create an effective call-to-action for a LinkedIn video:
            - Topic: {topic}
            - Video Type: {self.video_types[video_type]}
            - Target Audience: {self.target_audiences[target_audience]}
            
            Return a JSON with:
            1. primary_cta: Main call-to-action text
            2. secondary_cta: Optional follow-up action
            3. engagement_prompts: Questions or prompts for comments
            """
            
            response = llm_text_gen(prompt)
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Error generating CTA: {str(e)}")
            return {}

def linkedin_video_script_generator_ui():
    """Streamlit UI for the LinkedIn Video Script Generator."""
    
    st.title("LinkedIn Video Script Generator")
    st.markdown("""
    Create professional video scripts for LinkedIn that drive engagement and showcase your expertise.
    """)
    
    # Initialize the video script generator
    generator = LinkedInVideoScriptGenerator()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Script Details", "Research & Insights", "Generated Script"])
    
    with tab1:
        st.header("Video Script Details")
        
        # Basic information
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input("Topic", placeholder="e.g., AI in Healthcare, Remote Work Best Practices")
            industry = st.text_input("Industry", placeholder="e.g., Technology, Healthcare, Finance")
        
        with col2:
            video_type = st.selectbox(
                "Video Type",
                options=list(generator.video_types.keys()),
                format_func=lambda x: generator.video_types[x]
            )
            length = st.selectbox(
                "Video Length",
                options=list(generator.video_lengths.keys()),
                format_func=lambda x: generator.video_lengths[x]
            )
        
        # Advanced options
        with st.expander("Advanced Options"):
            col3, col4 = st.columns(2)
            with col3:
                target_audience = st.selectbox(
                    "Target Audience",
                    options=list(generator.target_audiences.keys()),
                    format_func=lambda x: generator.target_audiences[x]
                )
            
            with col4:
                tone = st.selectbox(
                    "Tone",
                    options=list(generator.tone_options.keys()),
                    format_func=lambda x: generator.tone_options[x]
                )
    
    with tab2:
        st.header("Research & Insights")
        
        if topic and industry:
            # Research options
            search_engine = st.selectbox(
                "Research Source",
                options=["metaphor", "google", "tavily"],
                format_func=lambda x: x.title()
            )
            
            if st.button("Research Topic"):
                with st.spinner("Researching topic..."):
                    research_results = generator.research_topic(topic, industry, search_engine)
                    
                    if research_results["insights"] or research_results["trends"]:
                        # Store results in session state
                        st.session_state.research_results = research_results
                        
                        # Display insights
                        st.subheader("Key Insights")
                        for insight in research_results["insights"]:
                            st.markdown(f"- {insight}")
                        
                        # Display trends
                        st.subheader("Current Trends")
                        for trend in research_results["trends"]:
                            st.markdown(f"- {trend}")
                    else:
                        st.warning("No insights found. Try adjusting your topic or using a different research source.")
        else:
            st.info("Please enter a topic and industry in the Script Details tab to research insights.")
    
    with tab3:
        st.header("Generated Script")
        
        if all([topic, industry, video_type, length, target_audience, tone]):
            if st.button("Generate Script"):
                with st.spinner("Generating video script..."):
                    # Get insights from research if available
                    insights = []
                    if hasattr(st.session_state, 'research_results'):
                        insights = st.session_state.research_results.get("insights", [])
                    
                    # Generate full script
                    script = generator.generate_full_script(
                        topic=topic,
                        video_type=video_type,
                        length=length,
                        target_audience=target_audience,
                        tone=tone,
                        insights=insights
                    )
                    
                    if script:
                        # Display hook
                        st.subheader("Hook")
                        st.write(script["hook"])
                        
                        # Display structure
                        st.subheader("Script Structure")
                        for i, section in enumerate(script["structure"]["sections"], 1):
                            with st.expander(f"Section {i}"):
                                st.write(f"**Timing:** {section.get('timing', 'N/A')}")
                                st.write(f"**Content:** {section.get('content', 'N/A')}")
                                
                                # Display visual cues for this section
                                if script["visuals"]:
                                    visual = next((v for v in script["visuals"] if v.get("section") == i), None)
                                    if visual:
                                        st.write("**Visual Elements:**")
                                        st.write(f"- Type: {visual.get('type', 'N/A')}")
                                        st.write(f"- Description: {visual.get('description', 'N/A')}")
                                        st.write(f"- Duration: {visual.get('duration', 'N/A')}")
                        
                        # Display transitions
                        st.subheader("Transitions")
                        for transition in script["structure"]["transitions"]:
                            st.markdown(f"- {transition}")
                        
                        # Display key points
                        st.subheader("Key Points to Emphasize")
                        for point in script["structure"]["key_points"]:
                            st.markdown(f"- {point}")
                        
                        # Display CTA
                        st.subheader("Call-to-Action")
                        st.write(f"**Primary CTA:** {script['cta'].get('primary_cta', 'N/A')}")
                        if script['cta'].get('secondary_cta'):
                            st.write(f"**Secondary CTA:** {script['cta']['secondary_cta']}")
                        
                        # Display engagement prompts
                        if script['cta'].get('engagement_prompts'):
                            st.subheader("Engagement Prompts")
                            for prompt in script['cta']['engagement_prompts']:
                                st.markdown(f"- {prompt}")
                        
                        # Display pacing notes
                        st.subheader("Pacing & Delivery Notes")
                        for note in script["structure"]["pacing_notes"]:
                            st.markdown(f"- {note}")
                    else:
                        st.error("Failed to generate script. Please try again.")
        else:
            st.info("Please fill in all required fields in the Script Details tab to generate a script.") 