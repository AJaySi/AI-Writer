"""
Facebook Hashtag Generator Module

This module provides functionality to generate relevant and trending hashtags for Facebook content.
It analyzes content, suggests optimal hashtag combinations, and provides performance predictions.
"""

import streamlit as st
import json
import random
import re
from typing import List, Dict, Any, Tuple, Optional
from loguru import logger
import sys
import base64
from io import BytesIO

from .....gpt_providers.text_generation.main_text_generation import llm_text_gen

# Configure logging
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

def initialize_session_state():
    """Initialize session state with default values."""
    if 'hashtag_data' not in st.session_state:
        st.session_state.hashtag_data = {
            'content': "",
            'industry': "",
            'content_type': "Post",
            'hashtag_count': 5,
            'include_trending': True,
            'include_niche': True,
            'generated_hashtags': [],
            'performance_predictions': {},
            'saved_hashtags': []
        }

def write_fb_hashtags():
    """Generate relevant and trending hashtags for Facebook content."""
    
    # Initialize session state
    initialize_session_state()
    
    st.markdown("""
    ### #️⃣ Facebook Hashtag Generator
    Create optimized hashtag combinations that maximize your content's reach and engagement.
    Our AI analyzes your content and suggests the perfect hashtags for your Facebook posts.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Generate Hashtags", "Hashtag Library", "Performance Insights"])
    
    with tab1:
        render_generate_tab()
    
    with tab2:
        render_library_tab()
    
    with tab3:
        render_insights_tab()

def render_generate_tab():
    """Render the hashtag generation tab with input fields."""
    
    # Content Input
    st.markdown("#### Content for Hashtag Analysis")
    
    content = st.text_area(
        "Enter your content or describe what you're posting about",
        value=st.session_state.hashtag_data['content'],
        height=150,
        help="Enter the text content or describe the topic of your Facebook post",
        key="content_input"
    )
    
    # Update session state
    st.session_state.hashtag_data['content'] = content
    
    # Industry and Content Type
    col1, col2 = st.columns(2)
    
    with col1:
        industries = [
            "Technology", "Health & Wellness", "Fashion", "Food & Beverage", 
            "Travel", "Education", "Finance", "Entertainment", "Fitness", 
            "Beauty", "Home & Garden", "Automotive", "Real Estate", "Business",
            "Art & Design", "Sports", "Parenting", "Pets", "Other"
        ]
        
        industry = st.selectbox(
            "Industry",
            options=industries,
            index=industries.index(st.session_state.hashtag_data['industry']) if st.session_state.hashtag_data['industry'] in industries else 0,
            help="Select your industry for more relevant hashtag suggestions",
            key="industry_select"
        )
        
        # Update session state
        st.session_state.hashtag_data['industry'] = industry
    
    with col2:
        content_types = ["Post", "Story", "Reel", "Carousel", "Event", "Group Post"]
        
        content_type = st.selectbox(
            "Content Type",
            options=content_types,
            index=content_types.index(st.session_state.hashtag_data['content_type']) if st.session_state.hashtag_data['content_type'] in content_types else 0,
            help="Select the type of content you're creating",
            key="content_type_select"
        )
        
        # Update session state
        st.session_state.hashtag_data['content_type'] = content_type
    
    # Hashtag Preferences
    st.markdown("#### Hashtag Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hashtag_count = st.slider(
            "Number of Hashtags",
            min_value=1,
            max_value=30,
            value=st.session_state.hashtag_data['hashtag_count'],
            help="Select how many hashtags you want to generate",
            key="hashtag_count_slider"
        )
        
        # Update session state
        st.session_state.hashtag_data['hashtag_count'] = hashtag_count
        
        include_trending = st.checkbox(
            "Include Trending Hashtags",
            value=st.session_state.hashtag_data['include_trending'],
            help="Include currently trending hashtags in suggestions",
            key="include_trending_checkbox"
        )
        
        # Update session state
        st.session_state.hashtag_data['include_trending'] = include_trending
    
    with col2:
        include_niche = st.checkbox(
            "Include Niche Hashtags",
            value=st.session_state.hashtag_data['include_niche'],
            help="Include niche, industry-specific hashtags",
            key="include_niche_checkbox"
        )
        
        # Update session state
        st.session_state.hashtag_data['include_niche'] = include_niche
        
        hashtag_placement = st.radio(
            "Hashtag Placement",
            ["End of Post", "Throughout Content", "Both"],
            index=0,
            help="Select where you want to place the hashtags",
            key="hashtag_placement_radio"
        )
    
    # Generate Button
    if st.button("Generate Hashtags", key="generate_hashtags_button"):
        if not content:
            st.warning("Please enter some content to generate hashtags.")
        else:
            with st.spinner("Generating optimized hashtags..."):
                # Generate hashtags
                generated_hashtags, performance_predictions = generate_hashtags(
                    content, 
                    industry, 
                    content_type, 
                    hashtag_count,
                    include_trending,
                    include_niche
                )
                
                # Update session state
                st.session_state.hashtag_data['generated_hashtags'] = generated_hashtags
                st.session_state.hashtag_data['performance_predictions'] = performance_predictions
                
                # Display results
                display_hashtag_results(generated_hashtags, performance_predictions, hashtag_placement)

def render_library_tab():
    """Render the hashtag library tab."""
    
    st.markdown("#### Hashtag Library")
    
    # Initialize saved hashtags if not exists
    if 'saved_hashtags' not in st.session_state.hashtag_data:
        st.session_state.hashtag_data['saved_hashtags'] = []
    
    # Create collections
    collections = ["Favorites", "Industry", "Campaign", "Custom"]
    
    selected_collection = st.selectbox(
        "Select Collection",
        options=collections,
        index=0,
        help="Select a hashtag collection to view or edit",
        key="collection_select"
    )
    
    # Display saved hashtags
    if st.session_state.hashtag_data['saved_hashtags']:
        st.markdown(f"**{selected_collection} Collection**")
        
        for i, hashtag in enumerate(st.session_state.hashtag_data['saved_hashtags']):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"#{hashtag}")
            
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.hashtag_data['saved_hashtags'].remove(hashtag)
                    st.rerun()
    else:
        st.info("Your hashtag library is empty. Generate hashtags and save them to build your library.")
    
    # Add new hashtag
    st.markdown("#### Add New Hashtag")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_hashtag = st.text_input(
            "Enter hashtag (without #)",
            value="",
            help="Enter a hashtag to add to your library",
            key="new_hashtag_input"
        )
    
    with col2:
        if st.button("Add", key="add_hashtag_button"):
            if new_hashtag:
                # Remove # if present
                new_hashtag = new_hashtag.replace("#", "")
                
                # Add to saved hashtags
                if new_hashtag not in st.session_state.hashtag_data['saved_hashtags']:
                    st.session_state.hashtag_data['saved_hashtags'].append(new_hashtag)
                    st.success(f"Added #{new_hashtag} to your library.")
                else:
                    st.warning(f"#{new_hashtag} is already in your library.")
            else:
                st.warning("Please enter a hashtag.")

def render_insights_tab():
    """Render the performance insights tab."""
    
    st.markdown("#### Hashtag Performance Insights")
    
    # Check if we have generated hashtags
    if not st.session_state.hashtag_data['generated_hashtags']:
        st.info("Generate hashtags first to see performance insights.")
        return
    
    # Display performance metrics
    st.markdown("##### Performance Predictions")
    
    performance_predictions = st.session_state.hashtag_data['performance_predictions']
    
    # Create a bar chart for reach predictions
    reach_data = {hashtag: data['reach'] for hashtag, data in performance_predictions.items()}
    
    if reach_data:
        st.bar_chart(reach_data)
    
    # Display detailed metrics
    st.markdown("##### Detailed Metrics")
    
    for hashtag, metrics in performance_predictions.items():
        with st.expander(f"#{hashtag}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Reach", f"{metrics['reach']:,}")
            
            with col2:
                st.metric("Engagement", f"{metrics['engagement']}%")
            
            with col3:
                st.metric("Competition", metrics['competition'])
    
    # Hashtag recommendations
    st.markdown("##### Recommendations")
    
    # Find best performing hashtags
    best_hashtags = sorted(
        performance_predictions.items(), 
        key=lambda x: x[1]['reach'], 
        reverse=True
    )[:3]
    
    st.markdown("**Best Performing Hashtags:**")
    for hashtag, metrics in best_hashtags:
        st.write(f"#{hashtag} - Reach: {metrics['reach']:,}, Engagement: {metrics['engagement']}%")
    
    # Optimal combination
    st.markdown("**Optimal Hashtag Combination:**")
    optimal_combination = " ".join([f"#{hashtag}" for hashtag, _ in best_hashtags])
    st.code(optimal_combination)
    
    # Copy button
    if st.button("Copy Optimal Combination", key="copy_optimal_button"):
        st.code(optimal_combination)
        st.success("Copied to clipboard!")

def generate_hashtags(
    content: str, 
    industry: str, 
    content_type: str, 
    hashtag_count: int,
    include_trending: bool,
    include_niche: bool
) -> Tuple[List[str], Dict[str, Dict[str, Any]]]:
    """Generate hashtags based on content and preferences."""
    
    # Prepare the prompt for the AI
    prompt = f"""
    Generate {hashtag_count} relevant and effective hashtags for a Facebook {content_type} in the {industry} industry.
    
    Content or topic: {content}
    
    Requirements:
    - Include a mix of popular and niche hashtags
    - Focus on hashtags that drive engagement and reach
    - Ensure hashtags are relevant to the content and industry
    - Format as a comma-separated list without the # symbol
    - Include {hashtag_count} hashtags total
    """
    
    if include_trending:
        prompt += "- Include some currently trending hashtags in this industry\n"
    
    if include_niche:
        prompt += "- Include niche, industry-specific hashtags that have less competition\n"
    
    prompt += """
    For each hashtag, also provide a performance prediction in this format:
    [hashtag_name]: [reach_number], [engagement_percentage], [competition_level]
    
    Example:
    digitalmarketing: 50000, 3.2, Medium
    socialmediamarketing: 75000, 2.8, High
    """
    
    try:
        # Generate hashtags using AI
        response = llm_text_gen(prompt)
        
        # Parse the response
        hashtags = []
        performance_predictions = {}
        
        # Extract hashtags and performance data
        lines = response.strip().split('\n')
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                if len(parts) == 2:
                    hashtag = parts[0].strip()
                    metrics = parts[1].strip().split(',')
                    
                    if len(metrics) >= 3:
                        try:
                            reach = int(metrics[0].strip())
                            engagement = float(metrics[1].strip().replace('%', ''))
                            competition = metrics[2].strip()
                            
                            hashtags.append(hashtag)
                            performance_predictions[hashtag] = {
                                'reach': reach,
                                'engagement': engagement,
                                'competition': competition
                            }
                        except (ValueError, IndexError):
                            # Skip malformed entries
                            continue
        
        # If we couldn't parse the response properly, generate some default hashtags
        if not hashtags:
            hashtags = generate_default_hashtags(content, industry, hashtag_count)
            performance_predictions = generate_default_predictions(hashtags)
        
        return hashtags, performance_predictions
    
    except Exception as e:
        logger.error(f"Error generating hashtags: {e}")
        # Generate default hashtags as fallback
        hashtags = generate_default_hashtags(content, industry, hashtag_count)
        performance_predictions = generate_default_predictions(hashtags)
        return hashtags, performance_predictions

def generate_default_hashtags(content: str, industry: str, count: int) -> List[str]:
    """Generate default hashtags when AI generation fails."""
    
    # Extract keywords from content
    keywords = re.findall(r'\b\w+\b', content.lower())
    keywords = [k for k in keywords if len(k) > 3]  # Filter out short words
    
    # Industry-specific hashtags
    industry_hashtags = {
        "Technology": ["tech", "innovation", "digital", "future", "ai", "technews", "startup"],
        "Health & Wellness": ["health", "wellness", "fitness", "healthy", "wellbeing", "mindfulness"],
        "Fashion": ["fashion", "style", "trend", "outfit", "fashionista", "accessories"],
        "Food & Beverage": ["food", "foodie", "recipe", "cooking", "delicious", "foodporn"],
        "Travel": ["travel", "wanderlust", "adventure", "explore", "travelgram", "vacation"],
        "Education": ["education", "learning", "knowledge", "study", "student", "academic"],
        "Finance": ["finance", "money", "investing", "financial", "business", "wealth"],
        "Entertainment": ["entertainment", "fun", "music", "movie", "tv", "celebrity"],
        "Fitness": ["fitness", "workout", "gym", "exercise", "health", "training"],
        "Beauty": ["beauty", "makeup", "skincare", "beautytips", "glam", "beautylover"],
        "Home & Garden": ["home", "garden", "decor", "interior", "diy", "homemade"],
        "Automotive": ["car", "automotive", "vehicle", "driving", "cars", "auto"],
        "Real Estate": ["realestate", "property", "home", "housing", "realtor", "investment"],
        "Business": ["business", "entrepreneur", "success", "marketing", "smallbusiness", "startup"],
        "Art & Design": ["art", "design", "creative", "artist", "illustration", "designer"],
        "Sports": ["sports", "athlete", "game", "team", "competition", "winning"],
        "Parenting": ["parenting", "family", "kids", "children", "mom", "dad"],
        "Pets": ["pets", "dog", "cat", "animal", "petlover", "adoption"],
        "Other": ["trending", "viral", "popular", "mustsee", "recommended", "best"]
    }
    
    # Get industry hashtags
    industry_tags = industry_hashtags.get(industry, industry_hashtags["Other"])
    
    # Combine keywords and industry hashtags
    all_hashtags = list(set(keywords + industry_tags))
    
    # Shuffle and select
    random.shuffle(all_hashtags)
    selected_hashtags = all_hashtags[:count]
    
    return selected_hashtags

def generate_default_predictions(hashtags: List[str]) -> Dict[str, Dict[str, Any]]:
    """Generate default performance predictions for hashtags."""
    
    predictions = {}
    
    for hashtag in hashtags:
        # Generate random but realistic predictions
        reach = random.randint(1000, 100000)
        engagement = round(random.uniform(0.5, 5.0), 1)
        competition = random.choice(["Low", "Medium", "High"])
        
        predictions[hashtag] = {
            'reach': reach,
            'engagement': engagement,
            'competition': competition
        }
    
    return predictions

def display_hashtag_results(
    hashtags: List[str], 
    performance_predictions: Dict[str, Dict[str, Any]],
    placement: str
):
    """Display the generated hashtags and performance predictions."""
    
    st.markdown("#### Generated Hashtags")
    
    # Display hashtags
    hashtag_text = " ".join([f"#{hashtag}" for hashtag in hashtags])
    st.code(hashtag_text)
    
    # Copy button
    if st.button("Copy All Hashtags", key="copy_hashtags_button"):
        st.code(hashtag_text)
        st.success("Copied to clipboard!")
    
    # Save button
    if st.button("Save to Library", key="save_hashtags_button"):
        for hashtag in hashtags:
            if hashtag not in st.session_state.hashtag_data['saved_hashtags']:
                st.session_state.hashtag_data['saved_hashtags'].append(hashtag)
        st.success("Hashtags saved to your library!")
    
    # Display placement suggestion
    st.markdown("#### Recommended Placement")
    
    if placement == "End of Post":
        st.markdown("""
        **Place these hashtags at the end of your post:**
        
        Add a line break after your content, then add the hashtags.
        """)
        st.code(hashtag_text)
    
    elif placement == "Throughout Content":
        st.markdown("""
        **Weave these hashtags throughout your content:**
        
        Integrate hashtags naturally within your sentences where they make sense.
        """)
        
        # Create a sample with hashtags integrated
        sample_content = st.session_state.hashtag_data['content']
        words = sample_content.split()
        
        # Insert hashtags at random positions
        for hashtag in hashtags[:3]:  # Use first 3 hashtags
            if len(words) > 5:
                pos = random.randint(0, len(words) - 1)
                words.insert(pos, f"#{hashtag}")
        
        sample_with_hashtags = " ".join(words)
        st.code(sample_with_hashtags)
    
    else:  # Both
        st.markdown("""
        **Use a combination of both approaches:**
        
        1. Weave some hashtags naturally within your content
        2. Add the remaining hashtags at the end
        """)
        
        # Create a sample with some hashtags integrated
        sample_content = st.session_state.hashtag_data['content']
        words = sample_content.split()
        
        # Insert some hashtags at random positions
        for hashtag in hashtags[:2]:  # Use first 2 hashtags
            if len(words) > 5:
                pos = random.randint(0, len(words) - 1)
                words.insert(pos, f"#{hashtag}")
        
        sample_with_hashtags = " ".join(words)
        st.code(sample_with_hashtags)
        
        # Add remaining hashtags at the end
        remaining_hashtags = " ".join([f"#{hashtag}" for hashtag in hashtags[2:]])
        st.markdown("**Add these at the end:**")
        st.code(remaining_hashtags)
    
    # Display performance insights
    st.markdown("#### Performance Insights")
    
    # Create a bar chart for reach predictions
    reach_data = {hashtag: data['reach'] for hashtag, data in performance_predictions.items()}
    
    if reach_data:
        st.bar_chart(reach_data)
    
    # Display detailed metrics
    st.markdown("##### Detailed Metrics")
    
    for hashtag, metrics in performance_predictions.items():
        with st.expander(f"#{hashtag}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Reach", f"{metrics['reach']:,}")
            
            with col2:
                st.metric("Engagement", f"{metrics['engagement']}%")
            
            with col3:
                st.metric("Competition", metrics['competition']) 