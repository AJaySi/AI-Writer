"""
BAB Formula Module - Before, After, Bridge

This module implements the BAB copywriting formula for generating persuasive marketing copy.
"""

import streamlit as st
from typing import Dict, Any
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

def generate_bab_copy():
    """Generate copy using the BAB (Before, After, Bridge) formula."""
    
    # Create tabs for the input sections
    tab1, tab2, tab3 = st.tabs(["Basic Info", "Formula Details", "Advanced Options"])
    
    with tab1:
        # Basic information
        product_name = st.text_input("Product/Service Name", 
                                   placeholder="e.g., Fitness Coaching Program")
        
        industry = st.selectbox("Industry", [
            "E-commerce", "SaaS/Technology", "Health & Wellness", 
            "Finance", "Education", "Real Estate", "Travel",
            "Food & Beverage", "Fashion", "Entertainment", "Other"
        ])
        
        target_audience = st.text_area("Target Audience", 
                                     placeholder="Describe your ideal customer (age, interests, pain points, etc.)")
        
        primary_benefit = st.text_input("Primary Benefit", 
                                      placeholder="The main benefit your product/service provides")
    
    with tab2:
        # BAB-specific inputs
        st.subheader("BAB Formula Components")
        
        # Before section
        st.markdown("### Before")
        before_focus = st.selectbox("Before Focus", [
            "Current Struggle", "Inefficiency", "Frustration",
            "Limitation", "Risk", "Missed Opportunity", "Status Quo"
        ])
        
        before_description = st.text_area("Before Description", 
                                        placeholder="Describe the current state or situation before using your product/service")
        
        # After section
        st.markdown("### After")
        after_focus = st.selectbox("After Focus", [
            "Desired Outcome", "Ideal State", "Relief",
            "Achievement", "Transformation", "New Capability", "Freedom"
        ])
        
        after_description = st.text_area("After Description", 
                                       placeholder="Describe the ideal state or situation after using your product/service")
        
        # Bridge section
        st.markdown("### Bridge")
        bridge_approach = st.selectbox("Bridge Approach", [
            "Process Explanation", "Features Showcase", "Unique Mechanism",
            "Simple Steps", "Testimonial Bridge", "Guarantee", "Case Study"
        ])
        
        bridge_elements = st.multiselect("Bridge Elements", [
            "How-to Steps", "Key Features", "Unique Selling Points",
            "Social Proof", "Risk Reversal", "Timeline", "Support Details"
        ])
        
        call_to_action = st.text_input("Call to Action", 
                                     placeholder="e.g., Start Your Transformation, Begin Your Journey")
    
    with tab3:
        # Advanced options
        st.subheader("Content Preferences")
        
        content_length = st.select_slider("Content Length", 
                                        options=["Very Short", "Short", "Medium", "Long", "Very Long"],
                                        value="Medium")
        
        tone_options = ["Inspirational", "Conversational", "Empathetic", 
                       "Motivational", "Professional", "Friendly", "Direct"]
        tone = st.selectbox("Tone of Voice", tone_options)
        
        format_options = ["Landing Page Copy", "Email", "Social Media Ad", 
                         "Product Description", "Sales Letter", "Video Script"]
        content_format = st.selectbox("Content Format", format_options)
        
        include_options = st.multiselect("Additional Elements to Include", [
            "Testimonial Placeholders", "Statistics/Data Points",
            "Objection Handling", "Guarantee", "Pricing Information",
            "Bullet Points", "Subheadings"
        ])
        
        # Visual elements
        st.subheader("Visual Elements")
        generate_image_prompt = st.checkbox("Generate Image Prompt", value=False)
        
        if generate_image_prompt:
            image_style = st.selectbox("Image Style", [
                "Before/After Comparison", "Transformation Journey", 
                "Process Visualization", "Result Showcase", "Emotional Contrast"
            ])
            
            image_focus = st.selectbox("Image Focus", [
                "Before State", "After State", 
                "Transformation Process", "Customer Journey", "Results"
            ])
    
    # Generate button
    if st.button("Generate BAB Copy", type="primary"):
        if not product_name or not target_audience or not before_description or not after_description:
            st.error("Please fill in all required fields: Product Name, Target Audience, Before Description, and After Description.")
            return
        
        with st.spinner("Generating your BAB copy..."):
            # Build the prompt
            prompt = f"""
            Create persuasive marketing copy using the BAB (Before, After, Bridge) formula for {product_name} in the {industry} industry.
            
            TARGET AUDIENCE:
            {target_audience}
            
            PRIMARY BENEFIT:
            {primary_benefit}
            
            BAB COMPONENTS:
            - Before Focus: {before_focus}
            - Before Description: {before_description}
            - After Focus: {after_focus}
            - After Description: {after_description}
            - Bridge Approach: {bridge_approach}
            - Bridge Elements: {', '.join(bridge_elements)}
            - Call to Action: {call_to_action}
            
            CONTENT PREFERENCES:
            - Length: {content_length}
            - Tone: {tone}
            - Format: {content_format}
            - Additional Elements: {', '.join(include_options)}
            
            Please structure the copy with clear sections for each part of the BAB formula:
            1. BEFORE: Paint a picture of the current state, challenges, or pain points.
            2. AFTER: Create a vision of the ideal state or outcome after the problem is solved.
            3. BRIDGE: Explain how your product/service bridges the gap between before and after.
            
            For each section, provide the actual marketing copy as well as a brief explanation of how it fulfills that part of the BAB formula.
            """
            
            # Generate the copy
            generated_copy = llm_text_gen(prompt)
            
            if generated_copy:
                # Display the generated copy
                st.subheader("Generated BAB Copy")
                
                # Create tabs for different views
                view_tab1, view_tab2, view_tab3 = st.tabs(["Formatted", "Plain Text", "Analysis"])
                
                with view_tab1:
                    st.markdown(generated_copy)
                
                with view_tab2:
                    st.text_area("Copy to clipboard", generated_copy, height=400)
                    st.button("Copy to Clipboard")
                
                with view_tab3:
                    # Analyze the copy for BAB components
                    analysis_prompt = f"""
                    Analyze the following marketing copy and evaluate how well it implements the BAB (Before, After, Bridge) formula.
                    Provide a score from 1-10 for each component and suggestions for improvement.
                    
                    COPY:
                    {generated_copy}
                    
                    Format your response as:
                    
                    ## BAB Analysis
                    
                    ### Before: [Score]/10
                    [Analysis and suggestions]
                    
                    ### After: [Score]/10
                    [Analysis and suggestions]
                    
                    ### Bridge: [Score]/10
                    [Analysis and suggestions]
                    
                    ### Overall Score: [Average Score]/10
                    [Summary and key improvement opportunities]
                    """
                    
                    analysis = llm_text_gen(analysis_prompt)
                    st.markdown(analysis)
                
                # Generate image prompt if requested
                if generate_image_prompt:
                    st.subheader("Complementary Image Prompt")
                    
                    image_prompt_request = f"""
                    Create a detailed image prompt for a {image_style} style image that would complement BAB marketing copy for {product_name}.
                    The image should focus on {image_focus} and align with the following target audience: {target_audience}.
                    The image should contrast the before state: {before_description} with the after state: {after_description}.
                    
                    Provide a detailed description that could be used with an AI image generator, including:
                    - Subject matter
                    - Style and mood
                    - Colors and lighting
                    - Composition
                    - Any text overlays (if appropriate)
                    
                    Format your response as a single, detailed paragraph that could be directly input into an image generation AI.
                    """
                    
                    image_prompt = llm_text_gen(image_prompt_request)
                    st.text_area("Image Generation Prompt", image_prompt, height=150)
                    
                    if st.button("Generate Image"):
                        with st.spinner("Generating image..."):
                            image_path = generate_image(image_prompt)
                            if image_path:
                                st.image(image_path)
                                st.download_button(
                                    label="Download Image",
                                    data=open(image_path, "rb").read(),
                                    file_name="bab_marketing_image.png",
                                    mime="image/png"
                                )
                
                # Download options
                st.download_button(
                    label="Download as Text",
                    data=generated_copy,
                    file_name=f"BAB_copy_{product_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Failed to generate BAB copy. Please try again.")