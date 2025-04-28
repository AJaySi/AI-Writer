"""
AIDA Formula Module - Attention, Interest, Desire, Action

This module implements the AIDA copywriting formula for generating persuasive marketing copy.
"""

import streamlit as st
from typing import Dict, Any
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

def generate_aida_copy():
    """Generate copy using the AIDA (Attention, Interest, Desire, Action) formula."""
    
    # Create tabs for the input sections
    tab1, tab2, tab3 = st.tabs(["Basic Info", "Formula Details", "Advanced Options"])
    
    with tab1:
        # Basic information
        product_name = st.text_input("Product/Service Name", 
                                   placeholder="e.g., Social Media Management Tool")
        
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
        # AIDA-specific inputs
        st.subheader("AIDA Formula Components")
        
        attention_hook = st.selectbox("Attention Hook Type", [
            "Bold Claim", "Surprising Statistic", "Provocative Question",
            "Story Hook", "Pain Point", "Curiosity Gap", "Timely News"
        ])
        
        attention_details = st.text_area("Attention Details", 
                                       placeholder="Provide details for your attention hook (e.g., specific statistic, claim, or question)")
        
        interest_approach = st.selectbox("Interest Building Approach", [
            "Problem Elaboration", "Industry Trends", "Personal Relevance",
            "Social Proof", "Unique Mechanism", "Future Vision"
        ])
        
        desire_elements = st.multiselect("Desire Building Elements", [
            "Benefits List", "Success Stories", "Before/After Scenario",
            "Emotional Appeal", "Scarcity/Exclusivity", "Risk Reversal"
        ])
        
        action_type = st.selectbox("Call to Action Type", [
            "Direct Purchase", "Free Trial/Demo", "Learn More",
            "Subscribe", "Contact Sales", "Limited-Time Offer"
        ])
        
        action_text = st.text_input("Call to Action Text", 
                                  placeholder="e.g., Get Started Free, Buy Now, Schedule a Demo")
    
    with tab3:
        # Advanced options
        st.subheader("Content Preferences")
        
        content_length = st.select_slider("Content Length", 
                                        options=["Very Short", "Short", "Medium", "Long", "Very Long"],
                                        value="Medium")
        
        tone_options = ["Professional", "Conversational", "Enthusiastic", 
                       "Authoritative", "Empathetic", "Urgent", "Humorous"]
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
                "Professional/Corporate", "Creative/Artistic", 
                "Minimalist", "Bold/Dramatic", "Friendly/Approachable"
            ])
            
            image_focus = st.selectbox("Image Focus", [
                "Product Showcase", "Customer Using Product", 
                "Problem Being Solved", "Benefit Visualization",
                "Emotional Response", "Brand Elements"
            ])
    
    # Generate button
    if st.button("Generate AIDA Copy", type="primary"):
        if not product_name or not target_audience or not primary_benefit:
            st.error("Please fill in all required fields: Product Name, Target Audience, and Primary Benefit.")
            return
        
        with st.spinner("Generating your AIDA copy..."):
            # Build the prompt
            prompt = f"""
            Create persuasive marketing copy using the AIDA (Attention, Interest, Desire, Action) formula for {product_name} in the {industry} industry.
            
            TARGET AUDIENCE:
            {target_audience}
            
            PRIMARY BENEFIT:
            {primary_benefit}
            
            AIDA COMPONENTS:
            - Attention Hook Type: {attention_hook}
            - Attention Details: {attention_details}
            - Interest Building Approach: {interest_approach}
            - Desire Building Elements: {', '.join(desire_elements)}
            - Call to Action Type: {action_type}
            - Call to Action Text: {action_text}
            
            CONTENT PREFERENCES:
            - Length: {content_length}
            - Tone: {tone}
            - Format: {content_format}
            - Additional Elements: {', '.join(include_options)}
            
            Please structure the copy with clear sections for each part of the AIDA formula:
            1. ATTENTION: A compelling headline or opening that grabs attention using the specified hook type.
            2. INTEREST: Content that builds interest using the specified approach.
            3. DESIRE: Elements that create desire for the product/service using the specified elements.
            4. ACTION: A clear call to action based on the specified type and text.
            
            For each section, provide the actual marketing copy as well as a brief explanation of how it fulfills that part of the AIDA formula.
            """
            
            # Generate the copy
            generated_copy = llm_text_gen(prompt)
            
            if generated_copy:
                # Display the generated copy
                st.subheader("Generated AIDA Copy")
                
                # Create tabs for different views
                view_tab1, view_tab2, view_tab3 = st.tabs(["Formatted", "Plain Text", "Analysis"])
                
                with view_tab1:
                    st.markdown(generated_copy)
                
                with view_tab2:
                    st.text_area("Copy to clipboard", generated_copy, height=400)
                    st.button("Copy to Clipboard")
                
                with view_tab3:
                    # Analyze the copy for AIDA components
                    analysis_prompt = f"""
                    Analyze the following marketing copy and evaluate how well it implements the AIDA formula.
                    Provide a score from 1-10 for each component (Attention, Interest, Desire, Action) and suggestions for improvement.
                    
                    COPY:
                    {generated_copy}
                    
                    Format your response as:
                    
                    ## AIDA Analysis
                    
                    ### Attention: [Score]/10
                    [Analysis and suggestions]
                    
                    ### Interest: [Score]/10
                    [Analysis and suggestions]
                    
                    ### Desire: [Score]/10
                    [Analysis and suggestions]
                    
                    ### Action: [Score]/10
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
                    Create a detailed image prompt for a {image_style} style image that would complement AIDA marketing copy for {product_name}.
                    The image should focus on {image_focus} and align with the following target audience: {target_audience}.
                    The image should reinforce the primary benefit: {primary_benefit}.
                    
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
                                    file_name="aida_marketing_image.png",
                                    mime="image/png"
                                )
                
                # Download options
                st.download_button(
                    label="Download as Text",
                    data=generated_copy,
                    file_name=f"AIDA_copy_{product_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Failed to generate AIDA copy. Please try again.")