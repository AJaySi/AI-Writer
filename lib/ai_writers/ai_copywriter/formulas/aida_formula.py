import streamlit as st
import time
from ....gpt_providers.text_generation.main_text_generation import llm_text_gen
from ....gpt_providers.text_to_image_generation.main_generate_image_from_prompt import generate_image

def generate_aida_copy():
    """Generate copy using the AIDA (Attention, Interest, Desire, Action) formula."""
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Content Details", "Formula Structure", "Preview & Export"])
    
    with tab1:
        st.subheader("Content Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_service = st.text_input(
                "Product/Service Name",
                placeholder="e.g., Social Media Management Tool",
                key="aida_product"
            )
            
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., Small business owners aged 30-45",
                key="aida_audience"
            )
            
            primary_benefit = st.text_input(
                "Primary Benefit",
                placeholder="e.g., Save 10 hours per week on social media tasks",
                key="aida_benefit"
            )
            
            unique_selling_point = st.text_input(
                "Unique Selling Point",
                placeholder="e.g., AI-powered content suggestions",
                key="aida_usp"
            )
        
        with col2:
            content_type = st.selectbox(
                "Content Type",
                ["Landing Page", "Email", "Ad Copy", "Social Media Post", "Product Description"],
                key="aida_content_type"
            )
            
            tone = st.selectbox(
                "Tone",
                ["Professional", "Conversational", "Enthusiastic", "Authoritative", "Empathetic"],
                key="aida_tone"
            )
            
            word_count = st.slider("Approximate Word Count", 50, 500, 200, key="aida_word_count")
            
            call_to_action = st.text_input(
                "Call to Action",
                placeholder="e.g., Sign up for a free trial",
                key="aida_cta"
            )
        
        # Advanced options
        with st.expander("Advanced Options"):
            include_testimonial = st.checkbox("Include testimonial placeholder", value=False, key="aida_testimonial")
            include_statistics = st.checkbox("Include data/statistics placeholders", value=True, key="aida_stats")
            include_objection_handling = st.checkbox("Include objection handling", value=False, key="aida_objections")
            
            st.subheader("Visual Elements")
            generate_image_suggestion = st.checkbox("Generate image suggestions", value=True, key="aida_image_suggest")
    
    with tab2:
        st.subheader("AIDA Formula Structure")
        
        st.markdown("""
        ### Attention
        The first step is to grab the reader's attention with a bold claim, surprising statistic, provocative question, or compelling headline.
        
        **Examples:**
        - "What if you could double your sales in 30 days?"
        - "73% of businesses are wasting money on ineffective marketing."
        - "Stop losing customers to your competitors."
        
        ### Interest
        Once you have their attention, build interest by explaining how your product/service relates to them and their needs.
        
        **Examples:**
        - "For business owners like you, time is the most valuable resource."
        - "You've worked hard to build your business, but scaling requires a different approach."
        - "Every day you don't optimize your workflow costs you potential revenue."
        
        ### Desire
        Create desire by highlighting benefits, features, and painting a picture of how their life/business will improve.
        
        **Examples:**
        - "Imagine completing in minutes what used to take hours."
        - "Our clients report an average 43% increase in productivity within the first month."
        - "You'll join over 10,000 successful businesses who have transformed their operations."
        
        ### Action
        End with a clear, compelling call to action that tells the reader exactly what to do next.
        
        **Examples:**
        - "Click the button below to start your free trial today."
        - "Schedule your consultation now – spaces are limited."
        - "Join thousands of satisfied customers – sign up now and save 20%."
        """)
        
        st.info("The AI will generate content for each section of the AIDA formula based on your inputs.")
    
    with tab3:
        st.subheader("Generate AIDA Copy")
        
        if st.button("Generate AIDA Content", type="primary", key="generate_aida"):
            if not product_service or not target_audience or not primary_benefit:
                st.error("Please fill in all required fields in the Content Details tab.")
            else:
                with st.spinner("Generating your AIDA copy..."):
                    # Build the prompt
                    prompt = f"""
                    Create persuasive copy using the AIDA (Attention, Interest, Desire, Action) formula for a {content_type} about {product_service}.
                    
                    Target audience: {target_audience}
                    Primary benefit: {primary_benefit}
                    Unique selling point: {unique_selling_point}
                    Tone: {tone}
                    Approximate word count: {word_count}
                    Call to action: {call_to_action}
                    
                    Additional requirements:
                    - Include testimonial placeholder: {include_testimonial}
                    - Include statistics/data: {include_statistics}
                    - Include objection handling: {include_objection_handling}
                    
                    Please structure the content with clear sections for each part of the AIDA formula:
                    1. Attention: A compelling headline or opening that grabs attention
                    2. Interest: Information that builds interest by relating to the audience's needs
                    3. Desire: Content that creates desire by highlighting benefits and painting a picture of improvement
                    4. Action: A clear call to action that tells the reader what to do next
                    
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
                            st.button("Copy to Clipboard", key="copy_aida")
                        
                        # Download options
                        st.download_button(
                            label="Download as Text",
                            data=generated_copy,
                            file_name=f"AIDA_copy_{int(time.time())}.txt",
                            mime="text/plain"
                        )
                        
                        # Generate image suggestions if selected
                        if generate_image_suggestion:
                            st.subheader("Image Suggestions")
                            with st.spinner("Generating image suggestions..."):
                                image_prompt = f"""
                                Create an image suggestion for a {content_type} about {product_service} targeting {target_audience}.
                                The image should complement the AIDA copywriting formula and highlight the primary benefit: {primary_benefit}.
                                Focus on creating a visual that would grab attention and support the copy.
                                """
                                
                                image_suggestions = llm_text_gen(image_prompt)
                                st.markdown(image_suggestions)
                    else:
                        st.error("Error: Failed to generate AIDA content.")