import streamlit as st
import time
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

def generate_pas_copy():
    """Generate copy using the PAS (Problem, Agitation, Solution) formula."""
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Content Details", "Formula Structure", "Preview & Export"])
    
    with tab1:
        st.subheader("Content Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_service = st.text_input(
                "Product/Service Name",
                placeholder="e.g., Weight Loss Program",
                key="pas_product"
            )
            
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., Busy professionals trying to lose weight",
                key="pas_audience"
            )
            
            main_problem = st.text_area(
                "Main Problem Your Product Solves",
                placeholder="e.g., Lack of time for meal planning and exercise",
                key="pas_problem"
            )
            
            solution_benefits = st.text_area(
                "Key Benefits of Your Solution",
                placeholder="e.g., 15-minute workouts, ready-made meal plans",
                key="pas_benefits"
            )
        
        with col2:
            content_type = st.selectbox(
                "Content Type",
                ["Social Media Ad", "Email", "Landing Page", "Blog Intro", "Video Script"],
                key="pas_content_type"
            )
            
            tone = st.selectbox(
                "Tone",
                ["Empathetic", "Urgent", "Conversational", "Professional", "Dramatic"],
                key="pas_tone"
            )
            
            word_count = st.slider("Approximate Word Count", 50, 500, 200, key="pas_word_count")
            
            call_to_action = st.text_input(
                "Call to Action",
                placeholder="e.g., Join our program today",
                key="pas_cta"
            )
        
        # Advanced options
        with st.expander("Advanced Options"):
            agitation_intensity = st.slider(
                "Agitation Intensity", 
                1, 10, 7, 
                help="How strongly should we emphasize the pain points? (1=mild, 10=intense)",
                key="pas_intensity"
            )
            
            include_proof = st.checkbox(
                "Include social proof", 
                value=True,
                help="Add testimonials or statistics to support your claims",
                key="pas_proof"
            )
            
            include_urgency = st.checkbox(
                "Add urgency elements", 
                value=True,
                help="Include elements that create a sense of urgency",
                key="pas_urgency"
            )
            
            st.subheader("Visual Elements")
            generate_image_suggestion = st.checkbox("Generate image suggestions", value=True, key="pas_image_suggest")
    
    with tab2:
        st.subheader("PAS Formula Structure")
        
        st.markdown("""
        ### Problem
        Start by identifying a problem that your target audience faces. This should be specific, relatable, and something your product or service can solve.
        
        **Examples:**
        - "Struggling to find time for exercise in your busy schedule?"
        - "Is your website failing to convert visitors into customers?"
        - "Tired of complicated skincare routines that don't deliver results?"
        
        ### Agitation
        Amplify the problem by highlighting the negative consequences, pain points, and emotional impact. Make the reader feel the problem more deeply.
        
        **Examples:**
        - "Every day you put it off means another day of feeling exhausted, unhealthy, and disappointed in yourself."
        - "Those lost conversions aren't just statistics—they're real revenue walking away from your business."
        - "You've spent hundreds of dollars and countless hours on products that promised results but left you frustrated and still dealing with the same skin issues."
        
        ### Solution
        Present your product or service as the perfect solution to their problem, highlighting benefits and how it addresses their specific pain points.
        
        **Examples:**
        - "Our 15-minute workout program is designed specifically for busy professionals like you."
        - "Our conversion optimization service has helped businesses like yours increase sales by an average of 37%."
        - "Our 3-step skincare system is clinically proven to deliver visible results in just 14 days."
        """)
        
        st.info("The AI will generate content for each section of the PAS formula based on your inputs.")
    
    with tab3:
        st.subheader("Generate PAS Copy")
        
        if st.button("Generate PAS Content", type="primary", key="generate_pas"):
            if not product_service or not target_audience or not main_problem or not solution_benefits:
                st.error("Please fill in all required fields in the Content Details tab.")
            else:
                with st.spinner("Generating your PAS copy..."):
                    # Build the prompt
                    prompt = f"""
                    Create persuasive copy using the PAS (Problem, Agitation, Solution) formula for a {content_type} about {product_service}.
                    
                    Target audience: {target_audience}
                    Main problem: {main_problem}
                    Solution benefits: {solution_benefits}
                    Tone: {tone}
                    Approximate word count: {word_count}
                    Call to action: {call_to_action}
                    
                    Additional requirements:
                    - Agitation intensity: {agitation_intensity}/10
                    - Include social proof: {include_proof}
                    - Add urgency elements: {include_urgency}
                    
                    Please structure the content with clear sections for each part of the PAS formula:
                    1. Problem: Identify a specific problem that the target audience faces
                    2. Agitation: Amplify the problem by highlighting negative consequences and emotional impact
                    3. Solution: Present the product/service as the perfect solution, highlighting benefits
                    
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
                            st.button("Copy to Clipboard", key="copy_pas")
                        
                        # Download options
                        st.download_button(
                            label="Download as Text",
                            data=generated_copy,
                            file_name=f"PAS_copy_{int(time.time())}.txt",
                            mime="text/plain"
                        )
                        
                        # Generate image suggestions if selected
                        if generate_image_suggestion:
                            st.subheader("Image Suggestions")
                            with st.spinner("Generating image suggestions..."):
                                image_prompt = f"""
                                Create an image suggestion for a {content_type} about {product_service} targeting {target_audience}.
                                The image should complement the PAS copywriting formula by visually representing:
                                1. The problem: {main_problem}
                                2. The emotional impact of this problem
                                3. The solution or relief provided by {product_service}
                                
                                Provide a detailed description of what this image should contain and how it should be composed.
                                """
                                
                                image_suggestions = llm_text_gen(image_prompt)
                                st.markdown(image_suggestions)
                    else:
                        st.error("Error: Failed to generate PAS content.")