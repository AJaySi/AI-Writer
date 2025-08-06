"""
LinkedIn Comment Response Generator UI

This module provides the Streamlit UI for the LinkedIn Comment Response Generator.
"""

import streamlit as st
import json
from typing import Dict, List
from .linkedin_comment_response_generator import LinkedInCommentResponseGenerator

async def linkedin_comment_response_generator_ui():
    """
    Streamlit UI for the LinkedIn Comment Response Generator.
    """
    # Initialize the generator
    generator = LinkedInCommentResponseGenerator()
    
    st.title("LinkedIn Comment Response Generator")
    
    # Create tabs for different response scenarios
    tabs = st.tabs([
        "General Response",
        "Handle Disagreement",
        "Value-Add Response",
        "Resource Suggestions",
        "Follow-up Questions"
    ])
    
    # General Response Tab
    with tabs[0]:
        st.header("Generate Professional Response")
        st.info("Generate an engaging and professional response to a LinkedIn comment")
        
        comment = st.text_area("Comment to Respond to", height=100)
        post_context = st.text_area("Original Post Context", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            brand_voice = st.selectbox(
                "Brand Voice",
                ["Professional", "Friendly", "Expert", "Supportive", "Diplomatic", "Appreciative"]
            )
        
        with col2:
            engagement_goal = st.selectbox(
                "Engagement Goal",
                ["Continue Discussion", "Share Knowledge", "Build Relationship", "Address Concern", "Encourage Action"]
            )
        
        if st.button("Generate Response", key="general_response"):
            with st.spinner("Generating response..."):
                # First analyze the comment
                analysis = await generator.analyze_comment(comment)
                
                # Display analysis
                with st.expander("Comment Analysis", expanded=True):
                    st.json(analysis)
                
                # Generate response
                response = await generator.generate_response(
                    comment,
                    post_context,
                    brand_voice.lower(),
                    engagement_goal
                )
                
                # Display response
                st.subheader("Generated Response")
                st.success(response['response'])
                
                # Display strategy
                with st.expander("Response Strategy"):
                    st.write("**Tone Used:**", response['tone_used'])
                    
                    st.write("**Key Points Addressed:**")
                    for point in response['key_points_addressed']:
                        st.write(f"- {point}")
                    
                    st.write("**Engagement Hooks:**")
                    for hook in response['engagement_hooks']:
                        st.write(f"- {hook}")
                    
                    st.write("**Value Adds:**")
                    for value in response['value_adds']:
                        st.write(f"- {value}")
                    
                    st.write("**Follow-up Suggestions:**")
                    for suggestion in response['follow_up_suggestions']:
                        st.write(f"- {suggestion}")
    
    # Handle Disagreement Tab
    with tabs[1]:
        st.header("Handle Disagreement")
        st.info("Generate a diplomatic response to a disagreeing comment")
        
        disagreement_comment = st.text_area("Disagreeing Comment", height=100, key="disagreement_comment")
        disagreement_context = st.text_area("Post Context", height=100, key="disagreement_context")
        disagreement_voice = st.selectbox(
            "Brand Voice",
            ["Diplomatic", "Professional", "Expert", "Supportive"],
            key="disagreement_voice"
        )
        
        if st.button("Generate Diplomatic Response"):
            with st.spinner("Generating diplomatic response..."):
                response = await generator.handle_disagreement(
                    disagreement_comment,
                    disagreement_context,
                    disagreement_voice.lower()
                )
                
                st.subheader("Diplomatic Response")
                st.success(response['response'])
                
                with st.expander("Response Strategy"):
                    st.write("**Acknowledgment:**", response['acknowledgment'])
                    
                    st.write("**Supporting Evidence:**")
                    for point in response['evidence']:
                        st.write(f"- {point}")
                    
                    st.write("**Common Ground:**")
                    for point in response['common_ground']:
                        st.write(f"- {point}")
                    
                    st.write("**Dialogue Continuation:**")
                    for hook in response['dialogue_hooks']:
                        st.write(f"- {hook}")
    
    # Value-Add Response Tab
    with tabs[2]:
        st.header("Value-Add Response")
        st.info("Generate a response that provides significant value")
        
        value_comment = st.text_area("Comment", height=100, key="value_comment")
        industry = st.text_input("Industry")
        expertise_areas = st.text_area(
            "Areas of Expertise (one per line)",
            height=100
        ).split("\n")
        
        if st.button("Generate Value-Add Response"):
            with st.spinner("Researching and generating response..."):
                response = await generator.generate_value_add_response(
                    value_comment,
                    industry,
                    expertise_areas
                )
                
                st.subheader("Value-Adding Response")
                st.success(response['response'])
                
                with st.expander("Value Components"):
                    st.write("**Key Insights:**")
                    for insight in response['insights_shared']:
                        st.write(f"- {insight}")
                    
                    st.write("**Action Items:**")
                    for item in response['action_items']:
                        st.write(f"- {item}")
                    
                    st.write("**Sources:**")
                    for source in response['sources']:
                        st.write(f"- {source}")
                    
                    st.write("**Expertise Demonstrated:**")
                    st.write(response['expertise_demonstrated'])
                    
                    st.write("**Engagement Hooks:**")
                    for hook in response['engagement_hooks']:
                        st.write(f"- {hook}")
    
    # Resource Suggestions Tab
    with tabs[3]:
        st.header("Resource Suggestions")
        st.info("Suggest helpful resources in response to a comment")
        
        resource_comment = st.text_area("Comment", height=100, key="resource_comment")
        topic = st.text_input("Topic")
        expertise_level = st.select_slider(
            "Expertise Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
        
        if st.button("Generate Resource Suggestions"):
            with st.spinner("Researching and compiling resources..."):
                response = await generator.suggest_resources(
                    resource_comment,
                    topic,
                    expertise_level.lower()
                )
                
                st.subheader("Resource Suggestion Response")
                st.success(response['response'])
                
                with st.expander("Resource Details"):
                    st.write("**Recommended Resources:**")
                    for resource in response['recommended_resources']:
                        st.write(f"- {resource}")
                    
                    st.write("**Learning Path:**")
                    for step in response['learning_path']:
                        st.write(f"- {step}")
                    
                    st.write("**Application Tips:**")
                    for tip in response['application_tips']:
                        st.write(f"- {tip}")
                    
                    st.write("**Follow-up Support:**")
                    st.write(response['follow_up_support'])
    
    # Follow-up Questions Tab
    with tabs[4]:
        st.header("Follow-up Questions")
        st.info("Generate engaging follow-up questions to continue the discussion")
        
        question_comment = st.text_area("Comment", height=100, key="question_comment")
        discussion_context = st.text_area("Discussion Context", height=100, key="question_context")
        
        if st.button("Generate Follow-up Questions"):
            with st.spinner("Generating questions..."):
                response = await generator.generate_follow_up_questions(
                    question_comment,
                    discussion_context
                )
                
                st.subheader("Primary Follow-up Question")
                st.success(response['primary_question'])
                
                st.subheader("Secondary Questions")
                for question in response['secondary_questions']:
                    st.info(question)
                
                with st.expander("Discussion Strategy"):
                    st.write("**Discussion Angles:**")
                    for angle in response['discussion_angles']:
                        st.write(f"- {angle}")
                    
                    st.write("**Engagement Prompts:**")
                    for prompt in response['engagement_prompts']:
                        st.write(f"- {prompt}")
                    
                    st.write("**Value Exploration:**")
                    for area in response['value_exploration']:
                        st.write(f"- {area}")
    
    # Add tone optimization section at the bottom
    st.divider()
    st.subheader("Response Tone Optimization")
    st.info("Optimize the tone of any generated response")
    
    response_to_optimize = st.text_area("Response to Optimize", height=100)
    col1, col2 = st.columns(2)
    
    with col1:
        target_tone = st.selectbox(
            "Target Tone",
            generator.response_tones
        )
    
    with col2:
        audience = st.text_input("Target Audience")
    
    if st.button("Optimize Tone"):
        with st.spinner("Optimizing response tone..."):
            optimized = await generator.optimize_response_tone(
                response_to_optimize,
                target_tone,
                audience
            )
            
            st.subheader("Tone-Optimized Response")
            st.success(optimized['optimized_response'])
            
            with st.expander("Optimization Details"):
                st.write("**Tone Adjustments:**")
                for adjustment in optimized['tone_adjustments']:
                    st.write(f"- {adjustment}")
                
                st.write("**Audience Alignment:**", optimized['audience_alignment'])
                st.write("**Engagement Potential:**", optimized['engagement_potential'])
                st.write("**Relationship Building:**", optimized['relationship_building']) 