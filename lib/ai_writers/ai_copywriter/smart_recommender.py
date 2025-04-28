"""
Smart Formula Recommender

This module provides AI-powered recommendations for copywriting formulas
based on user inputs and brief requirements.
"""

import streamlit as st
from typing import Dict, List, Any
from ...gpt_providers.text_generation.main_text_generation import llm_text_gen

def analyze_brief(brief_text: str) -> Dict[str, Any]:
    """
    Analyze a marketing brief and recommend appropriate copywriting formulas.
    
    Args:
        brief_text: The marketing brief text to analyze
        
    Returns:
        Dictionary containing analysis results and recommendations
    """
    
    # Create a system prompt for the analysis
    system_prompt = """
    You are an expert copywriting consultant specializing in analyzing marketing briefs and recommending the most appropriate copywriting formulas.
    Your task is to analyze the provided marketing brief and recommend the best copywriting formulas for the situation.
    
    For your analysis, consider:
    1. The marketing objective (awareness, consideration, conversion)
    2. The target audience and their level of awareness
    3. The product/service complexity
    4. The marketing channel or format
    5. The emotional vs. logical appeal needed
    
    Provide your recommendations in a structured JSON format with the following keys:
    - objective: The identified marketing objective
    - audience_awareness: Level of audience awareness (problem aware, solution aware, product aware, etc.)
    - complexity: Product/service complexity (low, medium, high)
    - channel: Identified marketing channel or format
    - appeal_type: Whether emotional or logical appeal would be more effective
    - primary_formula: The most recommended copywriting formula
    - primary_formula_reason: Why this formula is recommended
    - alternative_formulas: List of 2 alternative formulas that could work
    - alternative_formulas_reasons: List of reasons for each alternative formula
    - extracted_key_points: Key points extracted from the brief (product benefits, target audience, etc.)
    """
    
    # Create the user prompt
    user_prompt = f"""
    Please analyze the following marketing brief and recommend the most appropriate copywriting formulas:
    
    ---
    {brief_text}
    ---
    
    Based on this brief, what copywriting formulas would you recommend and why?
    """
    
    try:
        # Get the analysis from the LLM
        response = llm_text_gen(user_prompt, system_prompt=system_prompt, response_format="json")
        
        # Parse the response
        import json
        analysis = json.loads(response)
        return analysis
    except Exception as e:
        st.error(f"Error analyzing brief: {str(e)}")
        return {
            "objective": "Unknown",
            "audience_awareness": "Unknown",
            "complexity": "Unknown",
            "channel": "Unknown",
            "appeal_type": "Unknown",
            "primary_formula": "AIDA",
            "primary_formula_reason": "Could not analyze brief. AIDA is recommended as a versatile default formula.",
            "alternative_formulas": ["PAS", "BAB"],
            "alternative_formulas_reasons": [
                "PAS is effective for problem-solution scenarios.",
                "BAB is good for showing transformation."
            ],
            "extracted_key_points": []
        }

def write_smart_recommender():
    """Display the smart formula recommender interface."""
    st.title("Smart Formula Recommender")
    st.write("Let AI analyze your marketing brief and recommend the best copywriting formula.")
    
    # Brief input
    st.subheader("Your Marketing Brief")
    brief_text = st.text_area(
        "Enter your marketing brief or project description",
        height=200,
        placeholder="Describe your marketing project, including:\\n- Product/service details\\n- Target audience\\n- Marketing objectives\\n- Where the copy will be used\\n- Any specific requirements or constraints"
    )
    
    # Example briefs
    with st.expander("Need inspiration? Try an example brief"):
        example_briefs = {
            "SaaS Product Launch": """
            We're launching a new project management SaaS tool called TaskMaster that helps remote teams collaborate more effectively.
            Our target audience is tech-savvy team leaders (30-45 years old) who manage remote teams of 5-20 people.
            The main pain points we solve are miscommunication, missed deadlines, and lack of visibility into project progress.
            Key features include real-time collaboration, automated task dependencies, and AI-powered workload balancing.
            We need copy for our product launch landing page that will encourage visitors to sign up for a 14-day free trial.
            Our brand voice is professional but friendly, and we want to emphasize productivity gains and team harmony.
            """,
            
            "Health Product Email Campaign": """
            We sell a premium plant-based protein powder called NatureFuel that's organic, non-GMO, and contains no artificial ingredients.
            Our target customers are health-conscious individuals aged 25-40 who exercise regularly and follow a plant-based or flexitarian diet.
            We want to create an email sequence to nurture leads who downloaded our "Plant Protein Guide" but haven't made a purchase yet.
            The main objections we need to overcome are price sensitivity (our product is premium-priced) and skepticism about the taste.
            We have strong testimonials from athletes and nutritionists, and clinical data showing our absorption rate is 28% higher than competitors.
            The goal is to convert these leads into first-time customers with a limited-time 15% discount offer.
            """,
            
            "Local Business Social Media": """
            I own a local bakery called Sweet Traditions that specializes in artisanal sourdough bread and pastries made with traditional methods.
            We're located in a mid-sized town and have been open for 3 years with a loyal but small customer base.
            We want to create social media ads to reach more local customers within a 10-mile radius and increase foot traffic on weekdays, which are currently slow.
            Our target customers are foodies, health-conscious individuals who care about ingredients, and families looking for special treats.
            We pride ourselves on using organic, locally-sourced ingredients and traditional baking methods passed down for generations.
            We want to highlight our weekday special (buy one loaf, get a pastry free) without coming across as too promotional.
            """
        }
        
        selected_example = st.selectbox("Select an example brief", list(example_briefs.keys()))
        if st.button("Use this example"):
            brief_text = example_briefs[selected_example]
            st.session_state.brief_text = brief_text
            st.rerun()
    
    # Store brief in session state if provided
    if brief_text:
        st.session_state.brief_text = brief_text
    
    # Analyze button
    if st.button("Analyze Brief & Recommend Formulas", type="primary"):
        if not st.session_state.get("brief_text"):
            st.error("Please enter a marketing brief to analyze.")
            return
        
        with st.spinner("Analyzing your brief and generating recommendations..."):
            # Analyze the brief
            analysis = analyze_brief(st.session_state.brief_text)
            
            # Store analysis in session state
            st.session_state.analysis = analysis
            
            # Display results
            st.success("Analysis complete! Here are your formula recommendations:")
            
            # Display the analysis
            st.subheader("Brief Analysis")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Marketing Objective", analysis["objective"])
            with col2:
                st.metric("Audience Awareness", analysis["audience_awareness"])
            with col3:
                st.metric("Appeal Type", analysis["appeal_type"])
            
            # Primary recommendation
            st.subheader("Primary Recommendation")
            st.markdown(f"""
            ### {analysis["primary_formula"]}
            
            **Why this formula works for you:**
            {analysis["primary_formula_reason"]}
            """)
            
            if st.button("Use This Formula"):
                st.session_state.selected_formula = analysis["primary_formula"]
                st.rerun()
            
            # Alternative recommendations
            st.subheader("Alternative Options")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                ### {analysis["alternative_formulas"][0]}
                
                **Why consider this:**
                {analysis["alternative_formulas_reasons"][0]}
                """)
                
                if st.button(f"Use {analysis['alternative_formulas'][0]}", key="alt1"):
                    st.session_state.selected_formula = analysis["alternative_formulas"][0]
                    st.rerun()
            
            with col2:
                st.markdown(f"""
                ### {analysis["alternative_formulas"][1]}
                
                **Why consider this:**
                {analysis["alternative_formulas_reasons"][1]}
                """)
                
                if st.button(f"Use {analysis['alternative_formulas'][1]}", key="alt2"):
                    st.session_state.selected_formula = analysis["alternative_formulas"][1]
                    st.rerun()
            
            # Extracted key points
            st.subheader("Key Points Extracted From Your Brief")
            for point in analysis["extracted_key_points"]:
                st.markdown(f"- {point}")
    
    # Display previous analysis if available
    elif "analysis" in st.session_state:
        analysis = st.session_state.analysis
        
        st.success("Here are your formula recommendations:")
        
        # Display the analysis
        st.subheader("Brief Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Marketing Objective", analysis["objective"])
        with col2:
            st.metric("Audience Awareness", analysis["audience_awareness"])
        with col3:
            st.metric("Appeal Type", analysis["appeal_type"])
        
        # Primary recommendation
        st.subheader("Primary Recommendation")
        st.markdown(f"""
        ### {analysis["primary_formula"]}
        
        **Why this formula works for you:**
        {analysis["primary_formula_reason"]}
        """)
        
        if st.button("Use This Formula"):
            st.session_state.selected_formula = analysis["primary_formula"]
            st.rerun()
        
        # Alternative recommendations
        st.subheader("Alternative Options")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            ### {analysis["alternative_formulas"][0]}
            
            **Why consider this:**
            {analysis["alternative_formulas_reasons"][0]}
            """)
            
            if st.button(f"Use {analysis['alternative_formulas'][0]}", key="alt1"):
                st.session_state.selected_formula = analysis["alternative_formulas"][0]
                st.rerun()
        
        with col2:
            st.markdown(f"""
            ### {analysis["alternative_formulas"][1]}
            
            **Why consider this:**
            {analysis["alternative_formulas_reasons"][1]}
            """)
            
            if st.button(f"Use {analysis['alternative_formulas'][1]}", key="alt2"):
                st.session_state.selected_formula = analysis["alternative_formulas"][1]
                st.rerun()
        
        # Extracted key points
        st.subheader("Key Points Extracted From Your Brief")
        for point in analysis["extracted_key_points"]:
            st.markdown(f"- {point}")