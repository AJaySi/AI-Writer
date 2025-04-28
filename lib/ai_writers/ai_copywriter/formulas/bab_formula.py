import streamlit as st
import time
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

def generate_bab_copy():
    """Generate copy using the BAB (Before, After, Bridge) formula."""
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Content Details", "Formula Structure", "Preview & Export"])
    
    with tab1:
        st.subheader("Content Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_service = st.text_input(
                "Product/Service Name",
                placeholder="e.g., Project Management Software",
                key="bab_product"
            )
            
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., Remote teams struggling with collaboration",
                key="bab_audience"
            )
            
            before_state = st.text_area(
                "Before State (Current Situation)",
                placeholder="e.g., Missed deadlines, communication gaps, unclear priorities",
                key="bab_before"
            )
            
            after_state = st.text_area(
                "After State (Desired Outcome)",
                placeholder="e.g., Streamlined workflows, clear communication, on-time delivery",
                key="bab_after"
            )
        
        with col2:
            content_type = st.selectbox(
                "Content Type",
                ["Case Study", "Testimonial", "Email", "Landing Page", "Video Script"],
                key="bab_content_type"
            )
            
            tone = st.selectbox(
                "Tone",
                ["Conversational", "Professional", "Inspirational", "Empathetic", "Authoritative"],
                key="bab_tone"
            )
            
            word_count = st.slider("Approximate Word Count", 100, 800, 300, key="bab_word_count")
            
            call_to_action = st.text_input(
                "Call to Action",
                placeholder="e.g., Schedule a demo today",
                key="bab_cta"
            )
        
        # Advanced options
        with st.expander("Advanced Options"):
            include_customer_story = st.checkbox(
                "Include customer story example", 
                value=True,
                help="Add a brief customer story to illustrate the transformation",
                key="bab_story"
            )
            
            include_statistics = st.checkbox(
                "Include statistics/data", 
                value=True,
                help="Add relevant statistics to support your claims",
                key="bab_stats"
            )
            
            focus_on_emotion = st.slider(
                "Emotional Focus", 
                1, 10, 7, 
                help="How much to focus on emotional benefits vs. practical benefits (1=practical, 10=emotional)",
                key="bab_emotion"
            )
            
            st.subheader("Visual Elements")
            generate_image_suggestion = st.checkbox("Generate image suggestions", value=True, key="bab_image_suggest")
            
            if generate_image_suggestion:
                image_style = st.selectbox(
                    "Image Style",
                    ["Before/After Comparison", "Transformation Journey", "Result Focused", "Process Illustration"],
                    key="bab_image_style"
                )
    
    with tab2:
        st.subheader("BAB Formula Structure")
        
        st.markdown("""
        ### Before
        Describe the current state or situation that your target audience is experiencing. Focus on pain points, challenges, and frustrations.
        
        **Examples:**
        - "Managing remote teams used to mean endless email chains, missed deadlines, and late-night emergency calls."
        - "Remember when creating content meant juggling multiple tools, spreadsheets, and communication platforms?"
        - "You've been trying to lose weight with crash diets and intense workout programs that leave you exhausted and discouraged."
        
        ### After
        Paint a picture of the ideal state—what life looks like after using your product or service. Focus on benefits and positive outcomes.
        
        **Examples:**
        - "Imagine your team collaborating seamlessly, meeting every deadline, and having complete visibility into project progress."
        - "Picture having all your content planned, created, and scheduled from a single dashboard, with real-time performance analytics at your fingertips."
        - "Envision yourself feeling energetic, confident, and proud of your sustainable fitness journey, enjoying foods you love while still reaching your goals."
        
        ### Bridge
        Explain how your product or service bridges the gap between the "Before" and "After" states. This is where you introduce your solution.
        
        **Examples:**
        - "Our project management platform is the bridge that takes you from chaos to clarity, with features specifically designed for remote teams."
        - "That's exactly what our all-in-one content platform delivers—the seamless connection between your content strategy and execution."
        - "Our personalized nutrition program is the missing link between your current struggles and your fitness goals."
        """)
        
        st.info("The AI will generate content for each section of the BAB formula based on your inputs.")
    
    with tab3:
        st.subheader("Generate BAB Copy")
        
        if st.button("Generate BAB Content", type="primary", key="generate_bab"):
            if not product_service or not target_audience or not before_state or not after_state:
                st.error("Please fill in all required fields in the Content Details tab.")
            else:
                with st.spinner("Generating your BAB copy..."):
                    # Build the prompt
                    prompt = f"""
                    Create persuasive copy using the BAB (Before, After, Bridge) formula for a {content_type} about {product_service}.
                    
                    Target audience: {target_audience}
                    Before state (current situation): {before_state}
                    After state (desired outcome): {after_state}
                    Tone: {tone}
                    Approximate word count: {word_count}
                    Call to action: {call_to_action}
                    
                    Additional requirements:
                    - Include customer story example: {include_customer_story}
                    - Include statistics/data: {include_statistics}
                    - Emotional focus level: {focus_on_emotion}/10 (higher means more emotional, lower means more practical)
                    
                    Please structure the content with clear sections for each part of the BAB formula:
                    1. Before: Describe the current state or situation that the target audience is experiencing
                    2. After: Paint a picture of the ideal state—what life looks like after using the product/service
                    3. Bridge: Explain how the product/service bridges the gap between the "Before" and "After" states
                    
                    For each section, provide the actual content as well as a brief explanation of how it fulfills that part of the formula.
                    """
                    
                    generated_copy = llm_text_gen(prompt)
                    
                    if generated_copy:
                        # Display tabs for different views
                        view_tab1, view_tab2 = st.tabs(["Formatted", "Plain Text"])
                        
                        with view_tab1:
                            st.markdown(generated_copy)
                        
                        with view_tab2:
                            st.text_area("Copy to clipboard", generated_copy, height=400)
                            st.button("Copy to Clipboard", key="copy_bab")
                        
                        # Download options
                        st.download_button(
                            label="Download as Text",
                            data=generated_copy,
                            file_name=f"BAB_copy_{int(time.time())}.txt",
                            mime="text/plain"
                        )
                        
                        # Generate image suggestions if selected
                        if generate_image_suggestion:
                            st.subheader("Image Suggestions")
                            with st.spinner("Generating image suggestions..."):
                                image_prompt = f"""
                                Create an image suggestion for a {content_type} about {product_service} targeting {target_audience}.
                                The image should use a {image_style} approach to visually represent:
                                1. Before state: {before_state}
                                2. After state: {after_state}
                                3. The transformation enabled by {product_service}
                                
                                Provide a detailed description of what this image should contain, how it should be composed, and what elements should be included to effectively communicate the before/after contrast.
                                """
                                
                                image_suggestions = llm_text_gen(image_prompt)
                                st.markdown(image_suggestions)
                    else:
                        st.error("Error: Failed to generate BAB content.")