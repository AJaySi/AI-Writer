import streamlit as st
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from tenacity import retry, wait_random_exponential, stop_after_attempt

def input_section():
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h2 style='color: #1E88E5;'>🎯 AIDPPC Copywriting Generator</h2>
        <p>Create compelling copy that follows the AIDPPC (Attention-Interest-Description-Persuasion-Proof-Close) framework to drive conversions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Educational content about AIDPPC copywriting
    with st.expander("📚 What is AIDPPC Copywriting?", expanded=False):
        st.markdown("""
        ### Understanding the AIDPPC Copywriting Framework
        
        AIDPPC is an acronym for Attention-Interest-Description-Persuasion-Proof-Close. It's a comprehensive copywriting framework that guides your audience through a complete journey:
        
        - **Attention**: Capturing the audience's attention with a compelling headline or hook
        - **Interest**: Generating interest by highlighting benefits or addressing pain points
        - **Description**: Describing your product or service in detail
        - **Persuasion**: Presenting compelling arguments or incentives to persuade
        - **Proof**: Providing social proof, testimonials, or guarantees to build credibility
        - **Close**: Prompting the audience to take action with a strong call to action
        
        ### Why AIDPPC Copywriting Works
        
        The AIDPPC framework works because it:
        
        - Follows the natural decision-making process of consumers
        - Addresses all key elements needed for conversion
        - Builds credibility through multiple stages
        - Creates a complete journey from awareness to action
        - Balances emotional and rational appeals
        
        ### When to Use AIDPPC Copywriting
        
        The AIDPPC framework is particularly effective for:
        
        - Landing pages and sales pages
        - Email marketing campaigns
        - Product descriptions
        - Direct response advertising
        - Content that needs to drive specific actions
        - Marketing materials that need to address objections
        """)
    
    # Main input form
    with st.expander("✍️ Create Your AIDPPC Copy", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            brand_name = st.text_input('**🏢 Brand/Company Name**', 
                                      placeholder="e.g., Alwrity",
                                      help="Enter the name of your brand or company.")
            
            target_audience = st.text_input('**👥 Target Audience**', 
                                          placeholder="e.g., Small business owners, Tech professionals",
                                          help="Who is your ideal customer? Be specific about demographics and psychographics.")
            
            attention = st.text_area('**🔔 Attention-Grabbing Hook**', 
                                   placeholder="e.g., Tired of spending hours writing content that doesn't convert?",
                                   help="Create a compelling headline or hook that captures attention.")
            
            interest = st.text_area('**💡 Generate Interest**', 
                                  placeholder="e.g., Imagine creating high-quality content in minutes instead of hours...",
                                  help="Highlight benefits or address pain points to generate interest.")
            
        with col2:
            description = st.text_input('**📝 Brand Description** (In 2-3 words)', 
                                      placeholder="e.g., AI writing tools",
                                      help="Describe your product or service briefly.")
            
            unique_selling_point = st.text_input('**💎 Unique Selling Point**', 
                                               placeholder="e.g., 10x faster content creation",
                                               help="What makes your product/service different from competitors?")
            
            persuasion = st.text_area('**💪 Persuasive Arguments**', 
                                    placeholder="e.g., Our AI analyzes top-performing content to ensure your copy resonates with your target audience...",
                                    help="Present compelling arguments or incentives to persuade your audience.")
            
            proof = st.text_area('**✅ Social Proof**', 
                                placeholder="e.g., Join 10,000+ satisfied customers who have transformed their content strategy...",
                                help="Provide testimonials, statistics, or guarantees to build credibility.")
            
            close = st.text_area('**🚀 Call to Action**', 
                                placeholder="e.g., Start creating converting content today with our 14-day free trial...",
                                help="Prompt your audience to take action with a strong call to action.")
        
        tone_style = st.selectbox(
            '**🎭 Copy Tone & Style**',
            options=['Professional', 'Conversational', 'Humorous', 'Authoritative', 'Empathetic', 'Aspirational'],
            help="Select the tone and style for your copy."
        )
        
        if st.button('**🚀 Generate AIDPPC Copy**', type="primary"):
            if not brand_name or not description or not attention or not interest or not persuasion or not proof or not close:
                st.error("⚠️ Please fill in all required fields (Brand Name, Description, and all AIDPPC elements)!")
            else:
                with st.spinner("✨ Crafting compelling AIDPPC copy..."):
                    aidppc_copy = generate_aidppc_copy(
                        brand_name, 
                        description, 
                        attention,
                        interest,
                        persuasion,
                        proof,
                        close,
                        target_audience,
                        unique_selling_point,
                        tone_style
                    )
                    
                    if aidppc_copy:
                        st.markdown("""
                        <div style='background-color: #e6f7ff; padding: 20px; border-radius: 10px; margin-top: 20px;'>
                            <h3 style='color: #0066cc;'>🎯 Your AIDPPC Copy</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display the copy with a nice format
                        st.markdown(aidppc_copy)
                        
                        # Add copy button
                        st.markdown("""
                        <div style='margin-top: 20px;'>
                            <button style='background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>
                                Copy to Clipboard
                            </button>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add tips for using the copy
                        with st.expander("💡 Tips for Using Your AIDPPC Copy", expanded=False):
                            st.markdown("""
                            ### How to Use Your AIDPPC Copy Effectively
                            
                            1. **Follow the sequence**: The AIDPPC framework creates a natural progression - make sure your copy maintains this flow
                            
                            2. **Test different hooks**: A/B test different attention-grabbing headlines to see which resonates most with your audience
                            
                            3. **Pair with visuals**: Combine your copy with images that reinforce each stage of the AIDPPC journey
                            
                            4. **Consider the context**: Adapt the copy based on where it will appear (landing page, email, social media, etc.)
                            
                            5. **Measure results**: Track conversion metrics to see how your AIDPPC copy performs
                            
                            6. **Refine over time**: Continuously improve your copy based on audience feedback and performance data
                            """)
                    else:
                        st.error("💥 **Failed to generate AIDPPC Copy. Please try again!**")


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_aidppc_copy(brand_name, description, attention, interest, persuasion, proof, close, 
                        target_audience, unique_selling_point, tone_style):
    system_prompt = """You are an expert copywriter specializing in the AIDPPC (Attention-Interest-Description-Persuasion-Proof-Close) framework. 
    Your expertise is in creating compelling, conversion-focused marketing copy that guides readers through a complete journey from awareness to action. 
    Your copy is authentic, specific to the brand, and focused on driving measurable results."""
    
    prompt = f"""Create 3 different marketing campaigns for {brand_name}, which is a {description}.

    TARGET AUDIENCE: {target_audience}
    UNIQUE SELLING POINT: {unique_selling_point}
    TONE & STYLE: {tone_style}
    
    Use the AIDPPC framework with these elements:
    - **Attention**: {attention}
    - **Interest**: {interest}
    - **Persuasion**: {persuasion}
    - **Proof**: {proof}
    - **Close**: {close}

    For each campaign:
    1. Start with the attention-grabbing hook to capture the audience's attention
    2. Generate interest by highlighting benefits or addressing pain points
    3. Describe your product or service in detail
    4. Present persuasive arguments or incentives
    5. Provide social proof, testimonials, or guarantees
    6. End with a strong call to action

    Format each campaign clearly with "CAMPAIGN 1:", "CAMPAIGN 2:", etc. as headers.
    Make the copy authentic, specific to the brand, and focused on the target audience's needs and desires.
    """
    
    try:
        return llm_text_gen(prompt, system_prompt=system_prompt)
    except Exception as e:
        st.error(f"Error generating copy: {str(e)}")
        return None