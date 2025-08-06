"""
LinkedIn Company Page Generator UI

This module provides the Streamlit UI for the LinkedIn Company Page Generator.
"""

import streamlit as st
import json
from typing import Dict, List, Optional
from loguru import logger

from .linkedin_company_page_generator import LinkedInCompanyPageGenerator

async def linkedin_company_page_generator_ui():
    """Main UI function for the LinkedIn Company Page Generator."""
    
    st.title("🏢 LinkedIn Company Page Content Generator")
    st.markdown("""
    Create engaging and professional content for your LinkedIn company page. 
    This tool helps you generate optimized company profiles, updates, employee spotlights, and industry content.
    """)
    
    # Initialize the generator
    generator = LinkedInCompanyPageGenerator()
    
    # Create tabs for different content types
    tab1, tab2, tab3, tab4 = st.tabs([
        "Company Profile",
        "Company Updates",
        "Employee Spotlights",
        "Industry Content"
    ])
    
    # Company Profile Tab
    with tab1:
        st.header("Optimize Your Company Profile")
        st.markdown("Generate an optimized LinkedIn company profile that highlights your brand and drives engagement.")
        
        # Company Information Form
        with st.form("company_profile_form"):
            company_name = st.text_input("Company Name", placeholder="Enter your company name")
            industry = st.text_input("Industry", placeholder="e.g., Technology, Healthcare, Finance")
            company_size = st.selectbox(
                "Company Size",
                ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]
            )
            target_audience = st.multiselect(
                "Target Audience",
                ["Job Seekers", "Customers", "Partners", "Investors", "Industry Professionals", "Media"],
                default=["Job Seekers", "Customers"]
            )
            brand_voice = st.selectbox(
                "Brand Voice",
                ["Professional", "Innovative", "Friendly", "Authoritative", "Casual", "Technical"]
            )
            key_products = st.text_area(
                "Key Products/Services",
                placeholder="Enter your key products or services, one per line"
            ).split("\n")
            company_description = st.text_area(
                "Current Company Description",
                placeholder="Enter your current company description"
            )
            
            submit_profile = st.form_submit_button("Generate Optimized Profile")
            
            if submit_profile:
                if not all([company_name, industry, target_audience, brand_voice, key_products, company_description]):
                    st.error("Please fill in all required fields.")
                else:
                    with st.spinner("Generating optimized company profile..."):
                        try:
                            profile_content = await generator.optimize_company_profile(
                                company_name=company_name,
                                industry=industry,
                                target_audience=target_audience,
                                brand_voice=brand_voice,
                                key_products=key_products,
                                company_size=company_size,
                                company_description=company_description
                            )
                            
                            # Display the results
                            st.success("Profile generated successfully!")
                            
                            # Company Overview
                            st.subheader("Company Overview")
                            st.write(profile_content["company_overview"])
                            
                            # Mission Statement
                            st.subheader("Mission Statement")
                            st.write(profile_content["mission_statement"])
                            
                            # Value Proposition
                            st.subheader("Value Proposition")
                            st.write(profile_content["value_proposition"])
                            
                            # Industry Expertise
                            st.subheader("Industry Expertise")
                            st.write(profile_content["industry_expertise"])
                            
                            # Company Culture
                            st.subheader("Company Culture")
                            st.write(profile_content["company_culture"])
                            
                            # Products/Services Overview
                            st.subheader("Products/Services Overview")
                            st.write(profile_content["products_services_overview"])
                            
                            # SEO Keywords
                            st.subheader("Recommended SEO Keywords")
                            st.write(", ".join(profile_content["seo_keywords"]))
                            
                            # Hashtags
                            st.subheader("Recommended Hashtags")
                            st.write(" ".join([f"#{tag}" for tag in profile_content["recommended_hashtags"]]))
                            
                        except Exception as e:
                            st.error(f"Error generating profile: {str(e)}")
    
    # Company Updates Tab
    with tab2:
        st.header("Generate Company Updates")
        st.markdown("Create engaging company updates for your LinkedIn page.")
        
        # Update Generation Form
        with st.form("company_update_form"):
            update_type = st.selectbox(
                "Update Type",
                ["Product Launch", "Company Milestone", "Industry News", "Company News", "Event Announcement"]
            )
            topic = st.text_input("Topic", placeholder="Enter the main topic of your update")
            target_audience = st.multiselect(
                "Target Audience",
                ["Job Seekers", "Customers", "Partners", "Investors", "Industry Professionals", "Media"],
                default=["Customers", "Industry Professionals"]
            )
            include_hashtags = st.checkbox("Include Hashtags", value=True)
            include_cta = st.checkbox("Include Call-to-Action", value=True)
            
            submit_update = st.form_submit_button("Generate Update")
            
            if submit_update:
                if not topic:
                    st.error("Please enter a topic for your update.")
                else:
                    with st.spinner("Generating company update..."):
                        try:
                            update_content = await generator.generate_company_update(
                                update_type=update_type,
                                topic=topic,
                                target_audience=target_audience,
                                include_hashtags=include_hashtags,
                                include_cta=include_cta
                            )
                            
                            # Display the results
                            st.success("Update generated successfully!")
                            
                            # Post Content
                            st.subheader("Generated Post")
                            st.write(update_content["post_content"])
                            
                            # Hashtags
                            if include_hashtags:
                                st.subheader("Recommended Hashtags")
                                st.write(" ".join([f"#{tag}" for tag in update_content["hashtags"]]))
                            
                            # Call-to-Action
                            if include_cta:
                                st.subheader("Call-to-Action")
                                st.write(update_content["call_to_action"])
                            
                            # Engagement Tips
                            st.subheader("Engagement Tips")
                            for tip in update_content["engagement_tips"]:
                                st.write(f"• {tip}")
                            
                            # Image Prompt
                            st.subheader("Suggested Image Prompt")
                            st.write(update_content["suggested_image_prompt"])
                            
                        except Exception as e:
                            st.error(f"Error generating update: {str(e)}")
    
    # Employee Spotlights Tab
    with tab3:
        st.header("Generate Employee Spotlights")
        st.markdown("Create engaging employee spotlight posts to showcase your team.")
        
        # Spotlight Generation Form
        with st.form("employee_spotlight_form"):
            employee_name = st.text_input("Employee Name", placeholder="Enter employee's name")
            role = st.text_input("Role", placeholder="Enter employee's role")
            achievements = st.text_area(
                "Key Achievements",
                placeholder="Enter key achievements, one per line"
            ).split("\n")
            spotlight_type = st.selectbox(
                "Spotlight Type",
                ["General", "Leadership", "Innovation", "Team Player", "Career Growth"]
            )
            
            submit_spotlight = st.form_submit_button("Generate Spotlight")
            
            if submit_spotlight:
                if not all([employee_name, role, achievements]):
                    st.error("Please fill in all required fields.")
                else:
                    with st.spinner("Generating employee spotlight..."):
                        try:
                            spotlight_content = await generator.generate_employee_spotlight(
                                employee_name=employee_name,
                                role=role,
                                achievements=achievements,
                                spotlight_type=spotlight_type
                            )
                            
                            # Display the results
                            st.success("Spotlight generated successfully!")
                            
                            # Spotlight Content
                            st.subheader("Generated Spotlight")
                            st.write(spotlight_content["spotlight_content"])
                            
                            # Hashtags
                            st.subheader("Recommended Hashtags")
                            st.write(" ".join([f"#{tag}" for tag in spotlight_content["hashtags"]]))
                            
                            # Call-to-Action
                            st.subheader("Call-to-Action")
                            st.write(spotlight_content["call_to_action"])
                            
                            # Engagement Tips
                            st.subheader("Engagement Tips")
                            for tip in spotlight_content["engagement_tips"]:
                                st.write(f"• {tip}")
                            
                            # Image Prompt
                            st.subheader("Suggested Image Prompt")
                            st.write(spotlight_content["suggested_image_prompt"])
                            
                        except Exception as e:
                            st.error(f"Error generating spotlight: {str(e)}")
    
    # Industry Content Tab
    with tab4:
        st.header("Generate Industry Content")
        st.markdown("Create thought leadership content to position your company as an industry expert.")
        
        # Industry Content Generation Form
        with st.form("industry_content_form"):
            content_type = st.selectbox(
                "Content Type",
                ["Industry Insight", "Trend Analysis", "Best Practices", "Case Study", "Market Update"]
            )
            topic = st.text_input("Topic", placeholder="Enter the main topic of your content")
            target_audience = st.multiselect(
                "Target Audience",
                ["Job Seekers", "Customers", "Partners", "Investors", "Industry Professionals", "Media"],
                default=["Industry Professionals", "Customers"]
            )
            
            submit_content = st.form_submit_button("Generate Content")
            
            if submit_content:
                if not topic:
                    st.error("Please enter a topic for your content.")
                else:
                    with st.spinner("Generating industry content..."):
                        try:
                            content = await generator.generate_industry_content(
                                content_type=content_type,
                                topic=topic,
                                target_audience=target_audience
                            )
                            
                            # Display the results
                            st.success("Content generated successfully!")
                            
                            # Content
                            st.subheader("Generated Content")
                            st.write(content["content"])
                            
                            # Key Insights
                            st.subheader("Key Insights")
                            for insight in content["key_insights"]:
                                st.write(f"• {insight}")
                            
                            # Hashtags
                            st.subheader("Recommended Hashtags")
                            st.write(" ".join([f"#{tag}" for tag in content["hashtags"]]))
                            
                            # Call-to-Action
                            st.subheader("Call-to-Action")
                            st.write(content["call_to_action"])
                            
                            # Engagement Tips
                            st.subheader("Engagement Tips")
                            for tip in content["engagement_tips"]:
                                st.write(f"• {tip}")
                            
                            # Image Prompt
                            st.subheader("Suggested Image Prompt")
                            st.write(content["suggested_image_prompt"])
                            
                        except Exception as e:
                            st.error(f"Error generating content: {str(e)}")
    
    # Add a footer with tips
    st.markdown("---")
    st.markdown("""
    ### Tips for Effective LinkedIn Company Page Content:
    
    - **Consistency**: Maintain a consistent posting schedule and brand voice
    - **Engagement**: Encourage comments and discussions on your posts
    - **Visuals**: Use high-quality images and videos to increase engagement
    - **Hashtags**: Use relevant industry hashtags to increase visibility
    - **Analytics**: Monitor your content performance and adjust your strategy
    - **Employee Advocacy**: Encourage employees to share and engage with company content
    """) 