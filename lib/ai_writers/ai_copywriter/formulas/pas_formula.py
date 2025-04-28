"""
PAS Formula Module - Problem, Agitation, Solution

This module implements the PAS copywriting formula for generating persuasive marketing copy.
"""

import streamlit as st
from typing import Dict, Any
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

def generate_pas_copy():
    """Generate copy using the PAS (Problem, Agitation, Solution) formula."""
    
    # Create tabs for the input sections
    tab1, tab2, tab3 = st.tabs(["Basic Info", "Formula Details", "Advanced Options"])
    
    with tab1:
        # Basic information
        product_name = st.text_input("Product/Service Name", 
                                   placeholder="e.g., Home Security System")
        
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
        # PAS-specific inputs
        st.subheader("PAS Formula Components")
        
        # Problem section
        st.markdown("### Problem")
        problem_focus = st.selectbox("Problem Focus", [
            "Pain Point", "Fear", "Frustration", "Obstacle",
            "Challenge", "Risk", "Inefficiency"
        ])
        
        problem_description = st.text_area("Problem Description", 
                                         placeholder="Describe the main problem your product/service solves")
        
        # Agitation section
        st.markdown("### Agitation")
        agitation_approach = st.selectbox("Agitation Approach", [
            "Consequences", "Emotional Impact", "Lost Opportunities",
            "Future Risks", "Comparison", "Statistics", "Scenarios"
        ])
        
        agitation_intensity = st.slider("Agitation Intensity", 1, 10, 7, 
                                      help="How strongly should the copy emphasize the pain points? (1=Mild, 10=Intense)")
        
        # Solution section
        st.markdown("### Solution")
        solution_framing = st.selectbox("Solution Framing", [
            "Hero/Savior", "Tool/Resource", "Process/Method",
            "Partnership/Guide", "Transformation", "Protection"
        ])
        
        solution_proof = st.multiselect("Solution Proof Elements", [
            "Testimonials", "Case Studies", "Statistics",
            "Guarantees", "Before/After", "Social Proof", "Demonstrations"
        ])
        
        call_to_action = st.text_input("Call to Action", 
                                     placeholder="e.g., Get Protected Today, Start Your Free Trial")
    
    with tab3:
        # Advanced options
        st.subheader("Content Preferences")
        
        content_length = st.select_slider("Content Length", 
                                        options=["Very Short", "Short", "Medium", "Long", "Very Long"],
                                        value="Medium")
        
        tone_options = ["Professional", "Conversational", "Empathetic", 
                       "Urgent", "Authoritative", "Reassuring", "Direct"]
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
                "Problem Visualization", "Emotional Impact", 
                "Solution Showcase", "Before/After", "Relief/Resolution"
            ])
            
            image_focus = st.selectbox("Image Focus", [
                "Problem Scenario", "Emotional Expression", 
                "Product in Action", "Transformation", "Customer Relief"
            ])
    
    # Generate button
    if st.button("Generate PAS Copy", type="primary"):
        if not product_name or not target_audience or not problem_description:
            st.error("Please fill in all required fields: Product Name, Target Audience, and Problem Description.")
            return
        
        with st.spinner("Generating your PAS copy..."):
            # Build the prompt
            prompt = f"""
            Create persuasive marketing copy using the PAS (Problem, Agitation, Solution) formula for {product_name} in the {industry} industry.
            
            TARGET AUDIENCE:
            {target_audience}
            
            PRIMARY BENEFIT:
            {primary_benefit}
            
            PAS COMPONENTS:
            - Problem Focus: {problem_focus}
            - Problem Description: {problem_description}
            - Agitation Approach: {agitation_approach}
            - Agitation Intensity: {agitation_intensity}/10
            - Solution Framing: {solution_framing}
            - Solution Proof Elements: {', '.join(solution_proof)}
            - Call to Action: {call_to_action}
            
            CONTENT PREFERENCES:
            - Length: {content_length}
            - Tone: {tone}
            - Format: {content_format}
            - Additional Elements: {', '.join(include_options)}
            
            Please structure the copy with clear sections for each part of the PAS formula:
            1. PROBLEM: Clearly identify the problem that resonates with the target audience.
            2. AGITATION: Amplify the pain points and consequences of not solving the problem.
            3. SOLUTION: Present the product/service as the ideal solution with proof elements.
            
            For each section, provide the actual marketing copy as well as a brief explanation of how it fulfills that part of the PAS formula.
            """
            
            # Generate the copy
            generated_copy = llm_text_gen(prompt)
            
            if generated_copy:
                # Display the generated copy
                st.subheader("Generated PAS Copy")
                
                # Create tabs for different views
                view_tab1, view_tab2, view_tab3 = st.tabs(["Formatted", "Plain Text", "Analysis"])
                
                with view_tab1:
                    st.markdown(generated_copy)
                
                with view_tab2:
                    st.text_area("Copy to clipboard", generated_copy, height=400)
                    st.button("Copy to Clipboard")
                
                with view_tab3:
                    # Analyze the copy for PAS components
                    analysis_prompt = f"""
                    Analyze the following marketing copy and evaluate how well it implements the PAS (Problem, Agitation, Solution) formula.
                    Provide a score from 1-10 for each component and suggestions for improvement.
                    
                    COPY:
                    {generated_copy}
                    
                    Format your response as:
                    
                    ## PAS Analysis
                    
                    ### Problem: [Score]/10
                    [Analysis and suggestions]
                    
                    ### Agitation: [Score]/10
                    [Analysis and suggestions]
                    
                    ### Solution: [Score]/10
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
                    Create a detailed image prompt for a {image_style} style image that would complement PAS marketing copy for {product_name}.
                    The image should focus on {image_focus} and align with the following target audience: {target_audience}.
                    The image should reinforce the problem: {problem_description} and the solution benefit: {primary_benefit}.
                    
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
                                    file_name="pas_marketing_image.png",
                                    mime="image/png"
                                )
                
                # Download options
                st.download_button(
                    label="Download as Text",
                    data=generated_copy,
                    file_name=f"PAS_copy_{product_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Failed to generate PAS copy. Please try again.")