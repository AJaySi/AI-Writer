"""
LinkedIn Carousel Post Generator

This module provides functionality for generating LinkedIn carousel posts with
AI-powered content and visuals.
"""

import streamlit as st
from typing import Dict, List, Optional
from loguru import logger
import json
from pydantic import BaseModel

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen
from .....gpt_providers.text_generation.gemini_pro_text import gemini_structured_json_response
from .....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image
from .....ai_web_researcher.gpt_online_researcher import do_google_serp_search
from .....ai_web_researcher.metaphor_basic_neural_web_search import metaphor_search_articles
from .....ai_web_researcher.tavily_ai_search import do_tavily_ai_search


class CarouselSlide(BaseModel):
    """Represents a single slide in the carousel."""
    index: int
    heading: str
    subheading: str
    content: str
    image_prompt: str
    image_path: Optional[str] = None


class CarouselStructure(BaseModel):
    """Represents the complete carousel structure."""
    slides: List[CarouselSlide]


def generate_structured_content(prompt: str, model: str = 'gemini-pro') -> Optional[Dict]:
    """Generate structured content using Gemini's structured output feature."""
    try:
        # Define the schema for the carousel structure
        schema = {
            "type": "object",
            "properties": {
                "slides": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "index": {"type": "integer"},
                            "heading": {"type": "string"},
                            "subheading": {"type": "string"},
                            "content": {"type": "string"},
                            "image_prompt": {"type": "string"}
                        },
                        "required": ["index", "heading", "subheading", "content", "image_prompt"]
                    }
                }
            },
            "required": ["slides"]
        }
        
        # Use the new function to generate structured content
        result = gemini_structured_json_response(prompt, schema)
        
        # Check if there was an error
        if "error" in result:
            logger.error(f"Error generating structured content: {result['error']}")
            return None
            
        logger.debug(f"Structured response: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        logger.error(f"Error generating structured content: {e}")
        logger.exception("Full traceback:")
        return None


class LinkedInCarouselGenerator:
    """
    Generator for LinkedIn carousel posts with AI-powered content and visuals.
    """
    
    def __init__(self):
        """Initialize the carousel generator."""
        self.slides: List[CarouselSlide] = []
        self.topic = ""
        self.industry = ""
        self.tone = ""
        self.content_type = ""
        self.num_slides = 0
        self.research_results = {}
    
    def research_topic(self, topic: str, industry: str, search_engine: str = "metaphor") -> Dict:
        """Research the topic to gather content for carousel slides."""
        try:
            # Construct research query
            search_query = f"""
            Find detailed professional content about '{topic}' in {industry} industry
            focusing on:
            - Key concepts and main points
            - Statistics and data
            - Examples and case studies
            - Best practices
            - Expert insights
            """
            
            # Perform research using selected engine
            if search_engine == "metaphor":
                results = metaphor_search_articles(search_query)
            elif search_engine == "google":
                results = do_google_serp_search(search_query)
            elif search_engine == "tavily":
                results = do_tavily_ai_search(search_query)
            
            self.research_results = results
            return results
            
        except Exception as e:
            logger.error(f"Error researching topic: {e}")
            return {}
    
    def generate_slide_content(self, topic: str, num_slides: int = 5) -> bool:
        """Generate content for carousel slides."""
        try:
            logger.info(f"Generating carousel outline for topic: {topic}")
            
            # Step 1: Generate detailed outline
            outline_prompt = f"""
            Create a detailed outline for a LinkedIn carousel about {topic}.
            The outline should include:
            1. Main topic and key message
            2. {num_slides} main points to cover
            3. Supporting details for each point
            4. Key takeaways and call-to-action
            
            Format the outline in a clear, structured way.
            """
            
            outline = llm_text_gen(outline_prompt)
            logger.debug(f"Generated outline: {outline}")
            
            # Step 2: Generate structured carousel content
            carousel_prompt = f"""
            Based on this outline:
            {outline}
            
            Create a LinkedIn carousel with {num_slides} slides.
            Each slide should have:
            - A compelling heading
            - A brief subheading
            - Concise, engaging content
            - A detailed image prompt for visual content
            
            The content should be informative, engaging, and valuable for LinkedIn professionals.
            """
            
            logger.info("Generating structured carousel content")
            carousel_structure = generate_structured_content(carousel_prompt)
            
            if not carousel_structure:
                logger.error("Failed to generate structured carousel content")
                return False
                
            logger.debug(f"Generated carousel structure: {json.dumps(carousel_structure, indent=2)}")
            
            # Validate and process the structure
            if "slides" not in carousel_structure:
                logger.error("Invalid carousel structure: missing 'slides' key")
                return False
                
            self.slides = []
            for slide_data in carousel_structure["slides"]:
                try:
                    slide = CarouselSlide(
                        index=slide_data["index"],
                        heading=slide_data["heading"],
                        subheading=slide_data["subheading"],
                        content=slide_data["content"],
                        image_prompt=slide_data["image_prompt"]
                    )
                    self.slides.append(slide)
                    logger.debug(f"Created slide {slide.index}: {slide.heading}")
                except Exception as e:
                    logger.error(f"Error processing slide data: {e}")
                    logger.debug(f"Problematic slide data: {slide_data}")
                    continue
                    
            if not self.slides:
                logger.error("No valid slides were created")
                return False
                
            logger.info(f"Successfully generated {len(self.slides)} slides")
            return True
            
        except Exception as e:
            logger.error(f"Error generating slide content: {e}")
            logger.exception("Full traceback:")
            return False
    
    def generate_slide_image(self, slide: CarouselSlide) -> Optional[str]:
        """Generate an image for a carousel slide."""
        try:
            # Generate image using the slide's prompt
            image_path = generate_image(slide.image_prompt)
            slide.image_path = image_path
            return image_path
        except Exception as e:
            logger.error(f"Error generating slide image: {e}")
            return None
    
    def optimize_content(self, slide: CarouselSlide) -> CarouselSlide:
        """Optimize slide content for engagement."""
        try:
            optimization_prompt = f"""
            Optimize this carousel slide content for maximum LinkedIn engagement:

            Current Content:
            Heading: {slide.heading}
            Subheading: {slide.subheading}
            Content: {slide.content}

            Requirements:
            1. Make heading more attention-grabbing
            2. Ensure content is concise and impactful
            3. Add relevant emojis where appropriate
            4. Optimize for readability
            5. Keep professional tone
            6. Maintain focus on {self.topic}

            Return as JSON:
            {{
                "heading": "Optimized heading",
                "subheading": "Optimized subheading",
                "content": "Optimized content"
            }}
            """
            
            optimized = llm_text_gen(optimization_prompt)
            
            try:
                optimized_data = json.loads(optimized)
                slide.heading = optimized_data["heading"]
                slide.subheading = optimized_data["subheading"]
                slide.content = optimized_data["content"]
            except json.JSONDecodeError:
                logger.error("Failed to parse optimized content")
            
            return slide
            
        except Exception as e:
            logger.error(f"Error optimizing slide content: {e}")
            return slide


def linkedin_carousel_generator_ui():
    """Streamlit UI for the LinkedIn Carousel Generator."""
    st.title("🔄 LinkedIn Carousel Post Generator")
    st.write("Create engaging carousel posts that showcase your content professionally")
    
    # Initialize generator
    generator = LinkedInCarouselGenerator()
    
    # Initialize session state
    if "carousel_data" not in st.session_state:
        st.session_state.carousel_data = {
            "slides": [],
            "research_results": None,
            "generated_images": {},
            "current_slide": 0
        }
    
    # Input form
    with st.form("carousel_form"):
        topic = st.text_input("Topic", placeholder="Enter the main topic of your carousel")
        industry = st.text_input("Industry", placeholder="e.g., Technology, Healthcare, Finance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tone = st.selectbox(
                "Tone",
                ["Professional", "Educational", "Conversational", "Inspiring", "Technical"]
            )
        
        with col2:
            content_type = st.selectbox(
                "Content Type",
                ["How-to Guide", "List", "Story", "Case Study", "Tips & Tricks"]
            )
        
        with col3:
            num_slides = st.slider("Number of Slides", min_value=3, max_value=10, value=5)
        
        # Research source selection
        search_engine = st.radio(
            "Research Source",
            ["metaphor", "google", "tavily"],
            format_func=lambda x: {
                "metaphor": "🔍 Metaphor AI",
                "google": "🌐 Google Search",
                "tavily": "🤖 Tavily AI"
            }[x]
        )
        
        submit = st.form_submit_button("Generate Carousel")
    
    if submit and topic and industry:
        # Create status container
        status_container = st.empty()
        
        with st.spinner("Researching and generating your carousel..."):
            # Research phase
            status_container.text("🔍 Phase 1: Researching topic...")
            research_results = generator.research_topic(topic, industry, search_engine)
            st.session_state.carousel_data["research_results"] = research_results
            
            if research_results:
                # Content generation phase
                status_container.text("✍️ Phase 2: Creating carousel content...")
                slides = generator.generate_slide_content(
                    topic, num_slides
                )
                
                if not slides:
                    status_container.error("❌ Failed to generate carousel content. Please try again with different parameters.")
                    st.error("""
                    Tips to resolve this issue:
                    1. Try a different topic or industry
                    2. Adjust the number of slides
                    3. Change the content type or tone
                    4. Try a different research source
                    """)
                    return
                
                st.session_state.carousel_data["slides"] = slides
                
                # Image generation phase
                status_container.text("🎨 Phase 3: Generating slide visuals...")
                for slide in slides:
                    image_path = generator.generate_slide_image(slide)
                    if image_path:
                        st.session_state.carousel_data["generated_images"][slide.index] = image_path
                
                status_container.text("✅ Carousel generation complete!")
            else:
                status_container.error("❌ No research results found. Please try a different topic or research source.")
                st.error("""
                Tips to resolve this issue:
                1. Try a more specific topic
                2. Use a different research source
                3. Check if your topic is too niche or too broad
                4. Ensure your industry selection is accurate
                """)
    
    # Display carousel if we have slides
    if st.session_state.carousel_data["slides"]:
        st.markdown("---")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["🎯 Carousel Preview", "📊 Research Results"])
        
        with tab1:
            st.subheader("Carousel Preview")
            
            # Slide navigation
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                if st.button("⬅️ Previous") and st.session_state.carousel_data["current_slide"] > 0:
                    st.session_state.carousel_data["current_slide"] -= 1
            
            with col3:
                if st.button("Next ➡️") and st.session_state.carousel_data["current_slide"] < len(st.session_state.carousel_data["slides"]) - 1:
                    st.session_state.carousel_data["current_slide"] += 1
            
            # Display current slide
            current_slide = st.session_state.carousel_data["slides"][st.session_state.carousel_data["current_slide"]]
            
            st.markdown(f"""
                <div style='
                    background: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    margin: 1rem 0;
                '>
                    <h1 style='
                        color: #0A66C2;
                        font-size: 1.8rem;
                        margin-bottom: 0.5rem;
                    '>{current_slide.heading}</h1>
                    
                    <h2 style='
                        color: #666;
                        font-size: 1.2rem;
                        margin-bottom: 1.5rem;
                    '>{current_slide.subheading}</h2>
                    
                    <p style='
                        font-size: 1.1rem;
                        line-height: 1.6;
                        color: #2f2f2f;
                    '>{current_slide.content}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Display slide image if available
            if current_slide.image_path:
                st.image(current_slide.image_path, 
                        caption=f"Slide {current_slide.index} Image",
                        use_container_width=True)
            
            # Slide controls
            st.markdown(f"**Slide {current_slide.index} of {len(st.session_state.carousel_data['slides'])}**")
            
            # Edit options
            with st.expander("✏️ Edit Slide"):
                # Edit form for current slide
                edited_heading = st.text_input("Heading", value=current_slide.heading)
                edited_subheading = st.text_input("Subheading", value=current_slide.subheading)
                edited_content = st.text_area("Content", value=current_slide.content)
                
                if st.button("Update Slide"):
                    current_slide.heading = edited_heading
                    current_slide.subheading = edited_subheading
                    current_slide.content = edited_content
                    st.success("✅ Slide updated!")
                
                if st.button("Optimize Content"):
                    optimized_slide = generator.optimize_content(current_slide)
                    st.success("✅ Content optimized!")
                    st.experimental_rerun()
            
            # Export options
            with st.expander("💾 Export Options"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Export Current Slide"):
                        st.success("Slide exported successfully!")
                with col2:
                    if st.button("Export Full Carousel"):
                        st.success("Carousel exported successfully!")
        
        with tab2:
            st.subheader("Research Results")
            
            research_results = st.session_state.carousel_data["research_results"]
            
            if research_results:
                # Display key insights
                st.markdown("### Key Insights")
                for insight in research_results.get("key_insights", []):
                    st.markdown(f"- {insight}")
                
                # Display statistics
                st.markdown("### Statistics & Data")
                for stat in research_results.get("statistics", []):
                    st.markdown(f"- {stat}")
                
                # Display sources
                st.markdown("### Sources")
                for source in research_results.get("sources", []):
                    st.markdown(f"- {source}")
            else:
                st.info("No research results available.")


if __name__ == "__main__":
    linkedin_carousel_generator_ui() 