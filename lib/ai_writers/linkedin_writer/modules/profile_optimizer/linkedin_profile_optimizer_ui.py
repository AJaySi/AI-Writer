"""
LinkedIn Profile Optimizer UI

This module provides the Streamlit UI for the LinkedIn Profile Optimizer.
"""

import streamlit as st
import json
from typing import Dict, List
from .linkedin_profile_optimizer import LinkedInProfileOptimizer

async def linkedin_profile_optimizer_ui():
    """
    Streamlit UI for the LinkedIn Profile Optimizer.
    """
    # Initialize the profile optimizer
    optimizer = LinkedInProfileOptimizer()
    
    # Create tabs for different optimization sections
    tabs = st.tabs([
        "Profile Analysis",
        "Headline Optimizer",
        "About Section",
        "Experience Enhancer",
        "Skills Recommender"
    ])
    
    # Profile Analysis Tab
    with tabs[0]:
        st.header("Profile Strength Analysis")
        st.info("Upload your profile information for a comprehensive analysis")
        
        # Profile Data Input
        with st.expander("Enter Profile Information", expanded=True):
            profile_data = {
                "headline": st.text_input("Current Headline"),
                "about": st.text_area("About Section"),
                "industry": st.text_input("Industry"),
                "current_role": st.text_input("Current Role"),
                "experience": [],
                "skills": st.text_area("Current Skills (one per line)").split("\n"),
                "education": st.text_area("Education (one per line)").split("\n")
            }
            
            # Experience Input
            st.subheader("Work Experience")
            num_experiences = st.number_input("Number of experiences to add", min_value=0, max_value=10, value=1)
            
            for i in range(num_experiences):
                with st.expander(f"Experience {i+1}"):
                    exp = {
                        "role": st.text_input(f"Role {i+1}"),
                        "company": st.text_input(f"Company {i+1}"),
                        "description": st.text_area(f"Description {i+1}")
                    }
                    profile_data["experience"].append(exp)
        
        if st.button("Analyze Profile"):
            with st.spinner("Analyzing your profile..."):
                analysis = await optimizer.analyze_profile_strength(profile_data)
                
                # Display Analysis Results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Profile Strength Score", f"{analysis['strength_score']}/100")
                    
                    st.subheader("Section Scores")
                    for section, score in analysis['section_scores'].items():
                        st.progress(score/100, text=f"{section}: {score}%")
                
                with col2:
                    st.subheader("Priority Improvements")
                    for improvement in analysis['priority_improvements']:
                        st.warning(improvement)
                
                st.subheader("SEO Recommendations")
                for rec in analysis['seo_recommendations']:
                    st.info(rec)
    
    # Headline Optimizer Tab
    with tabs[1]:
        st.header("Headline Optimizer")
        st.info("Optimize your headline for better visibility and impact")
        
        current_headline = st.text_input("Current Headline")
        industry = st.text_input("Industry")
        role = st.text_input("Current/Target Role")
        
        if st.button("Optimize Headline"):
            with st.spinner("Generating optimized headline..."):
                headline_optimization = await optimizer.optimize_headline(
                    current_headline,
                    industry,
                    role
                )
                
                st.subheader("Optimized Headline")
                st.success(headline_optimization['optimized_headline'])
                
                st.subheader("Optimization Explanation")
                st.write(headline_optimization['explanation'])
                
                st.subheader("Keywords Used")
                for keyword in headline_optimization['keywords_used']:
                    st.info(keyword)
    
    # About Section Tab
    with tabs[2]:
        st.header("About Section Generator")
        st.info("Create an engaging and professional About section")
        
        current_about = st.text_area("Current About Section")
        achievements = st.text_area("Key Achievements (one per line)").split("\n")
        target_audience = st.text_input("Target Audience")
        
        if st.button("Generate About Section"):
            with st.spinner("Generating optimized About section..."):
                about_optimization = await optimizer.generate_about_section(
                    current_about,
                    profile_data.get("experience", []),
                    achievements,
                    target_audience
                )
                
                st.subheader("Optimized About Section")
                st.markdown(about_optimization['about_section'])
                
                st.subheader("Section Structure")
                for section, explanation in about_optimization['structure_explanation'].items():
                    with st.expander(section):
                        st.write(explanation)
                
                st.subheader("Impact Factors")
                for factor in about_optimization['impact_factors']:
                    st.success(factor)
    
    # Experience Enhancer Tab
    with tabs[3]:
        st.header("Experience Description Enhancer")
        st.info("Enhance your work experience descriptions for maximum impact")
        
        experiences = []
        num_exp = st.number_input("Number of experiences to enhance", min_value=1, max_value=10, value=1)
        
        for i in range(num_exp):
            with st.expander(f"Experience {i+1}"):
                exp = {
                    "role": st.text_input(f"Role {i+1}"),
                    "company": st.text_input(f"Company {i+1}"),
                    "description": st.text_area(f"Current Description {i+1}")
                }
                experiences.append(exp)
        
        if st.button("Enhance Experiences"):
            with st.spinner("Enhancing experience descriptions..."):
                enhanced_experiences = await optimizer.enhance_experience_descriptions(experiences)
                
                for i, exp in enumerate(enhanced_experiences):
                    with st.expander(f"Enhanced Experience {i+1}"):
                        st.subheader(f"{exp['role']} at {exp['company']}")
                        st.markdown(exp['enhanced_description'])
                        
                        st.subheader("Key Achievements")
                        for achievement in exp['achievements']:
                            st.success(achievement)
                        
                        st.subheader("Keywords Used")
                        for keyword in exp['keywords']:
                            st.info(keyword)
    
    # Skills Recommender Tab
    with tabs[4]:
        st.header("Skills Recommender")
        st.info("Get personalized skill recommendations for your profile")
        
        current_skills = st.text_area("Current Skills (one per line)").split("\n")
        industry = st.text_input("Industry (for skills)")
        role = st.text_input("Role (for skills)")
        
        if st.button("Get Skill Recommendations"):
            with st.spinner("Analyzing and recommending skills..."):
                skill_recommendations = await optimizer.recommend_skills(
                    current_skills,
                    industry,
                    role
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Recommended Skills to Add")
                    for skill in skill_recommendations['recommended_skills']:
                        st.success(skill)
                    
                    st.subheader("Consider Removing")
                    for skill in skill_recommendations['skills_to_remove']:
                        st.warning(skill)
                
                with col2:
                    st.subheader("Trending Skills")
                    for skill in skill_recommendations['trending_skills']:
                        st.info(skill)
                
                st.subheader("Skill Categories")
                for category, skills in skill_recommendations['skill_categories'].items():
                    with st.expander(category):
                        for skill in skills:
                            st.write(f"- {skill}") 