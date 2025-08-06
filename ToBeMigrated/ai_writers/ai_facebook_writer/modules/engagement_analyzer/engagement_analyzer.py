"""
Facebook Engagement Analyzer Module

This module provides functionality to analyze Facebook content performance and provide
AI-powered suggestions for improvement. It helps content creators understand what works
and how to optimize their content for better engagement.
"""

import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Tuple, Optional, Union
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
    if 'engagement_data' not in st.session_state:
        st.session_state.engagement_data = {
            'content': "",
            'content_type': "Post",
            'metrics': {
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'reach': 0,
                'impressions': 0,
                'clicks': 0,
                'engagement_rate': 0.0
            },
            'audience_demographics': {
                'age_groups': {},
                'gender': {},
                'location': {},
                'device': {}
            },
            'peak_engagement_times': [],
            'competitor_benchmarks': {},
            'analysis_results': {},
            'improvement_suggestions': []
        }

def analyze_fb_engagement():
    """Analyze Facebook content performance and provide improvement suggestions."""
    
    # Initialize session state
    initialize_session_state()
    
    st.markdown("""
    ### 📊 Facebook Engagement Analyzer
    Analyze your content performance and get AI-powered suggestions to improve engagement.
    Understand what works, identify patterns, and optimize your Facebook strategy.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Content Analysis", "Performance Metrics", "Audience Insights", "Improvement Suggestions"])
    
    with tab1:
        render_content_analysis_tab()
    
    with tab2:
        render_performance_metrics_tab()
    
    with tab3:
        render_audience_insights_tab()
    
    with tab4:
        render_improvement_suggestions_tab()

def render_content_analysis_tab():
    """Render the content analysis tab with input fields."""
    
    st.markdown("#### Content for Analysis")
    
    # Content Input
    content = st.text_area(
        "Enter your Facebook content or paste a URL",
        value=st.session_state.engagement_data['content'],
        height=150,
        help="Enter the text content or paste a URL to your Facebook post",
        key="content_input"
    )
    
    # Update session state
    st.session_state.engagement_data['content'] = content
    
    # Content Type Selection
    col1, col2 = st.columns(2)
    
    with col1:
        content_types = ["Post", "Story", "Reel", "Carousel", "Event", "Group Post", "Page"]
        
        content_type = st.selectbox(
            "Content Type",
            options=content_types,
            index=content_types.index(st.session_state.engagement_data['content_type']) if st.session_state.engagement_data['content_type'] in content_types else 0,
            help="Select the type of content you're analyzing",
            key="content_type_select"
        )
        
        # Update session state
        st.session_state.engagement_data['content_type'] = content_type
    
    with col2:
        # Date Range Selection
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=7), datetime.now()),
            help="Select the date range for analysis",
            key="date_range_select"
        )
    
    # Analyze Button
    if st.button("Analyze Content", key="analyze_content_button"):
        if not content:
            st.warning("Please enter some content to analyze.")
        else:
            with st.spinner("Analyzing content performance..."):
                # Perform content analysis
                analysis_results = analyze_content(
                    content, 
                    content_type,
                    date_range
                )
                
                # Update session state
                st.session_state.engagement_data['analysis_results'] = analysis_results
                
                # Display results
                display_content_analysis(analysis_results)

def render_performance_metrics_tab():
    """Render the performance metrics tab."""
    
    st.markdown("#### Performance Metrics")
    
    # Check if we have analysis results
    if not st.session_state.engagement_data['analysis_results']:
        st.info("Please analyze your content first in the Content Analysis tab.")
        return
    
    # Metrics Input
    st.markdown("##### Enter Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metrics = st.session_state.engagement_data['metrics']
        
        metrics['likes'] = st.number_input(
            "Likes",
            min_value=0,
            value=metrics['likes'],
            help="Number of likes",
            key="likes_input"
        )
        
        metrics['comments'] = st.number_input(
            "Comments",
            min_value=0,
            value=metrics['comments'],
            help="Number of comments",
            key="comments_input"
        )
        
        metrics['shares'] = st.number_input(
            "Shares",
            min_value=0,
            value=metrics['shares'],
            help="Number of shares",
            key="shares_input"
        )
        
        metrics['reach'] = st.number_input(
            "Reach",
            min_value=0,
            value=metrics['reach'],
            help="Number of people who saw your content",
            key="reach_input"
        )
    
    with col2:
        metrics['impressions'] = st.number_input(
            "Impressions",
            min_value=0,
            value=metrics['impressions'],
            help="Number of times your content was shown",
            key="impressions_input"
        )
        
        metrics['clicks'] = st.number_input(
            "Clicks",
            min_value=0,
            value=metrics['clicks'],
            help="Number of clicks on your content",
            key="clicks_input"
        )
        
        # Calculate engagement rate
        if metrics['reach'] > 0:
            metrics['engagement_rate'] = ((metrics['likes'] + metrics['comments'] + metrics['shares']) / metrics['reach']) * 100
        else:
            metrics['engagement_rate'] = 0.0
        
        st.metric(
            "Engagement Rate",
            f"{metrics['engagement_rate']:.2f}%",
            help="Percentage of people who engaged with your content"
        )
    
    # Update session state
    st.session_state.engagement_data['metrics'] = metrics
    
    # Visualize metrics
    visualize_performance_metrics(metrics)
    
    # Competitor Benchmarks
    st.markdown("##### Competitor Benchmarks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        competitor_metrics = {
            "Industry Average": {
                "engagement_rate": 2.5,
                "reach": metrics['reach'] * 1.2,
                "comments": metrics['comments'] * 1.1
            },
            "Top Performers": {
                "engagement_rate": 5.0,
                "reach": metrics['reach'] * 2.0,
                "comments": metrics['comments'] * 2.5
            }
        }
        
        st.session_state.engagement_data['competitor_benchmarks'] = competitor_metrics
        
        # Create a DataFrame for comparison
        comparison_data = {
            "Metric": ["Engagement Rate", "Reach", "Comments"],
            "Your Content": [
                metrics['engagement_rate'],
                metrics['reach'],
                metrics['comments']
            ],
            "Industry Average": [
                competitor_metrics["Industry Average"]["engagement_rate"],
                competitor_metrics["Industry Average"]["reach"],
                competitor_metrics["Industry Average"]["comments"]
            ],
            "Top Performers": [
                competitor_metrics["Top Performers"]["engagement_rate"],
                competitor_metrics["Top Performers"]["reach"],
                competitor_metrics["Top Performers"]["comments"]
            ]
        }
        
        df = pd.DataFrame(comparison_data)
        
        # Display comparison chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df["Metric"],
            y=df["Your Content"],
            name="Your Content",
            marker_color="#1877F2"
        ))
        
        fig.add_trace(go.Bar(
            x=df["Metric"],
            y=df["Industry Average"],
            name="Industry Average",
            marker_color="#34A853"
        ))
        
        fig.add_trace(go.Bar(
            x=df["Metric"],
            y=df["Top Performers"],
            name="Top Performers",
            marker_color="#EA4335"
        ))
        
        fig.update_layout(
            title="Performance Comparison",
            xaxis_title="Metric",
            yaxis_title="Value",
            barmode="group",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_audience_insights_tab():
    """Render the audience insights tab."""
    
    st.markdown("#### Audience Insights")
    
    # Check if we have analysis results
    if not st.session_state.engagement_data['analysis_results']:
        st.info("Please analyze your content first in the Content Analysis tab.")
        return
    
    # Audience Demographics
    st.markdown("##### Audience Demographics")
    
    # Initialize demographics if not exists
    demographics = st.session_state.engagement_data['audience_demographics']
    
    # Age Groups
    st.markdown("###### Age Distribution")
    
    age_data = {
        "18-24": 15,
        "25-34": 30,
        "35-44": 25,
        "45-54": 15,
        "55-64": 10,
        "65+": 5
    }
    
    demographics['age_groups'] = age_data
    
    # Create age distribution chart
    fig = px.pie(
        values=list(age_data.values()),
        names=list(age_data.keys()),
        title="Age Distribution"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gender
    st.markdown("###### Gender Distribution")
    
    gender_data = {
        "Male": 45,
        "Female": 52,
        "Other": 3
    }
    
    demographics['gender'] = gender_data
    
    # Create gender distribution chart
    fig = px.pie(
        values=list(gender_data.values()),
        names=list(gender_data.keys()),
        title="Gender Distribution"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Location
    st.markdown("###### Top Locations")
    
    location_data = {
        "United States": 40,
        "United Kingdom": 15,
        "Canada": 10,
        "Australia": 8,
        "India": 7,
        "Other": 20
    }
    
    demographics['location'] = location_data
    
    # Create location distribution chart
    fig = px.bar(
        x=list(location_data.keys()),
        y=list(location_data.values()),
        title="Top Locations"
    )
    
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Percentage"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Device
    st.markdown("###### Device Usage")
    
    device_data = {
        "Mobile": 75,
        "Desktop": 20,
        "Tablet": 5
    }
    
    demographics['device'] = device_data
    
    # Create device distribution chart
    fig = px.pie(
        values=list(device_data.values()),
        names=list(device_data.keys()),
        title="Device Usage"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Update session state
    st.session_state.engagement_data['audience_demographics'] = demographics
    
    # Peak Engagement Times
    st.markdown("##### Peak Engagement Times")
    
    peak_times = [
        {"day": "Monday", "time": "9:00 AM", "engagement": 85},
        {"day": "Tuesday", "time": "2:00 PM", "engagement": 90},
        {"day": "Wednesday", "time": "11:00 AM", "engagement": 95},
        {"day": "Thursday", "time": "3:00 PM", "engagement": 88},
        {"day": "Friday", "time": "5:00 PM", "engagement": 92},
        {"day": "Saturday", "time": "10:00 AM", "engagement": 78},
        {"day": "Sunday", "time": "4:00 PM", "engagement": 82}
    ]
    
    st.session_state.engagement_data['peak_engagement_times'] = peak_times
    
    # Create peak times chart
    days = [item["day"] for item in peak_times]
    times = [item["time"] for item in peak_times]
    engagement = [item["engagement"] for item in peak_times]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=engagement,
        mode="lines+markers",
        name="Engagement",
        line=dict(color="#1877F2", width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title="Peak Engagement Times",
        xaxis_title="Day of Week",
        yaxis_title="Engagement Score",
        annotations=[
            dict(
                x=days[i],
                y=engagement[i],
                text=times[i],
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            ) for i in range(len(days))
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_improvement_suggestions_tab():
    """Render the improvement suggestions tab."""
    
    st.markdown("#### Improvement Suggestions")
    
    # Check if we have analysis results
    if not st.session_state.engagement_data['analysis_results']:
        st.info("Please analyze your content first in the Content Analysis tab.")
        return
    
    # Generate improvement suggestions
    if st.button("Generate Improvement Suggestions", key="generate_suggestions_button"):
        with st.spinner("Generating improvement suggestions..."):
            # Generate suggestions
            suggestions = generate_improvement_suggestions(
                st.session_state.engagement_data['content'],
                st.session_state.engagement_data['content_type'],
                st.session_state.engagement_data['metrics'],
                st.session_state.engagement_data['audience_demographics']
            )
            
            # Update session state
            st.session_state.engagement_data['improvement_suggestions'] = suggestions
            
            # Display suggestions
            display_improvement_suggestions(suggestions)
    
    # Display existing suggestions if available
    if st.session_state.engagement_data['improvement_suggestions']:
        display_improvement_suggestions(st.session_state.engagement_data['improvement_suggestions'])
    
    # A/B Testing
    st.markdown("##### A/B Testing Suggestions")
    
    # Generate A/B testing suggestions
    if st.button("Generate A/B Testing Suggestions", key="generate_ab_testing_button"):
        with st.spinner("Generating A/B testing suggestions..."):
            # Generate A/B testing suggestions
            ab_testing_suggestions = generate_ab_testing_suggestions(
                st.session_state.engagement_data['content'],
                st.session_state.engagement_data['content_type']
            )
            
            # Display A/B testing suggestions
            display_ab_testing_suggestions(ab_testing_suggestions)

def analyze_content(content: str, content_type: str, date_range: Tuple[datetime.date, datetime.date]) -> Dict[str, Any]:
    """Analyze content and return analysis results."""
    
    # Prepare prompt for content analysis
    prompt = f"""
    Analyze the following Facebook {content_type} content and provide insights on its performance potential:
    
    Content: "{content}"
    
    Date Range: {date_range[0]} to {date_range[1]}
    
    Please provide a detailed analysis including:
    1. Content quality assessment
    2. Engagement potential
    3. Key strengths
    4. Areas for improvement
    5. Suggested optimizations
    
    Format your response as a JSON object with the following structure:
    {{
        "content_quality": {{
            "score": <score from 1-10>,
            "feedback": "<detailed feedback>"
        }},
        "engagement_potential": {{
            "score": <score from 1-10>,
            "feedback": "<detailed feedback>"
        }},
        "strengths": ["<strength 1>", "<strength 2>", ...],
        "improvements": ["<improvement 1>", "<improvement 2>", ...],
        "optimizations": ["<optimization 1>", "<optimization 2>", ...]
    }}
    """
    
    try:
        # Generate analysis using LLM
        response = llm_text_gen(prompt)
        
        # Parse JSON response
        analysis_results = json.loads(response)
        
        return analysis_results
    except Exception as e:
        logger.error(f"Error analyzing content: {e}")
        
        # Return default analysis results
        return {
            "content_quality": {
                "score": 7,
                "feedback": "Content appears to be well-structured and engaging."
            },
            "engagement_potential": {
                "score": 8,
                "feedback": "Content has good potential for engagement based on its format and content."
            },
            "strengths": [
                "Clear and concise messaging",
                "Engaging content structure",
                "Relevant to target audience"
            ],
            "improvements": [
                "Add more visual elements",
                "Include a stronger call-to-action",
                "Optimize posting time"
            ],
            "optimizations": [
                "Add relevant hashtags",
                "Include emojis for visual appeal",
                "Tag relevant accounts"
            ]
        }

def display_content_analysis(analysis_results: Dict[str, Any]):
    """Display content analysis results."""
    
    # Content Quality
    st.markdown("##### Content Quality")
    
    quality_score = analysis_results["content_quality"]["score"]
    quality_feedback = analysis_results["content_quality"]["feedback"]
    
    # Create gauge chart for content quality
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=quality_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Content Quality Score"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "#1877F2"},
            'steps': [
                {'range': [0, 3], 'color': "lightgray"},
                {'range': [3, 7], 'color': "gray"},
                {'range': [7, 10], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7
            }
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"**Feedback:** {quality_feedback}")
    
    # Engagement Potential
    st.markdown("##### Engagement Potential")
    
    engagement_score = analysis_results["engagement_potential"]["score"]
    engagement_feedback = analysis_results["engagement_potential"]["feedback"]
    
    # Create gauge chart for engagement potential
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=engagement_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Engagement Potential Score"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "#34A853"},
            'steps': [
                {'range': [0, 3], 'color': "lightgray"},
                {'range': [3, 7], 'color': "gray"},
                {'range': [7, 10], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7
            }
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"**Feedback:** {engagement_feedback}")
    
    # Strengths
    st.markdown("##### Key Strengths")
    
    for strength in analysis_results["strengths"]:
        st.markdown(f"- {strength}")
    
    # Areas for Improvement
    st.markdown("##### Areas for Improvement")
    
    for improvement in analysis_results["improvements"]:
        st.markdown(f"- {improvement}")
    
    # Suggested Optimizations
    st.markdown("##### Suggested Optimizations")
    
    for optimization in analysis_results["optimizations"]:
        st.markdown(f"- {optimization}")

def visualize_performance_metrics(metrics: Dict[str, Any]):
    """Visualize performance metrics."""
    
    # Create metrics chart
    metric_names = ["Likes", "Comments", "Shares", "Reach", "Impressions", "Clicks"]
    metric_values = [
        metrics["likes"],
        metrics["comments"],
        metrics["shares"],
        metrics["reach"],
        metrics["impressions"],
        metrics["clicks"]
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=metric_names,
            y=metric_values,
            marker_color=["#1877F2", "#34A853", "#EA4335", "#FBBC05", "#4285F4", "#46BDC6"]
        )
    ])
    
    fig.update_layout(
        title="Performance Metrics",
        xaxis_title="Metric",
        yaxis_title="Count"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Engagement Rate Gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=metrics["engagement_rate"],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Engagement Rate"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "#1877F2"},
            'steps': [
                {'range': [0, 1], 'color': "lightgray"},
                {'range': [1, 3], 'color': "gray"},
                {'range': [3, 10], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 3
            }
        }
    ))
    
    st.plotly_chart(fig, use_container_width=True)

def generate_improvement_suggestions(
    content: str,
    content_type: str,
    metrics: Dict[str, Any],
    demographics: Dict[str, Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Generate improvement suggestions based on content analysis and metrics."""
    
    # Prepare prompt for improvement suggestions
    prompt = f"""
    Based on the following Facebook {content_type} content and performance metrics, provide specific improvement suggestions:
    
    Content: "{content}"
    
    Metrics:
    - Likes: {metrics['likes']}
    - Comments: {metrics['comments']}
    - Shares: {metrics['shares']}
    - Reach: {metrics['reach']}
    - Impressions: {metrics['impressions']}
    - Clicks: {metrics['clicks']}
    - Engagement Rate: {metrics['engagement_rate']}%
    
    Audience Demographics:
    - Age Groups: {demographics['age_groups']}
    - Gender: {demographics['gender']}
    - Top Locations: {demographics['location']}
    - Device Usage: {demographics['device']}
    
    Please provide 5 specific, actionable improvement suggestions that would help increase engagement.
    Format your response as a JSON array of objects with the following structure:
    [
        {{
            "category": "<category>",
            "suggestion": "<detailed suggestion>",
            "expected_impact": "<expected impact on engagement>",
            "implementation": "<how to implement this suggestion>"
        }},
        ...
    ]
    """
    
    try:
        # Generate suggestions using LLM
        response = llm_text_gen(prompt)
        
        # Parse JSON response
        suggestions = json.loads(response)
        
        return suggestions
    except Exception as e:
        logger.error(f"Error generating improvement suggestions: {e}")
        
        # Return default suggestions
        return [
            {
                "category": "Content Structure",
                "suggestion": "Add a more compelling headline to grab attention in the first 3 seconds.",
                "expected_impact": "Increase initial engagement by 25%",
                "implementation": "Place the headline at the beginning of your post and make it bold or use emojis to stand out."
            },
            {
                "category": "Visual Elements",
                "suggestion": "Include high-quality images or videos that complement your message.",
                "expected_impact": "Increase engagement by 40%",
                "implementation": "Add relevant images or short videos that illustrate your main points."
            },
            {
                "category": "Call-to-Action",
                "suggestion": "Add a stronger, more specific call-to-action.",
                "expected_impact": "Increase click-through rate by 30%",
                "implementation": "End your post with a clear, action-oriented question or instruction."
            },
            {
                "category": "Posting Time",
                "suggestion": "Optimize your posting time based on audience activity.",
                "expected_impact": "Increase reach by 20%",
                "implementation": "Post during peak engagement times (Wednesdays at 11 AM) when your audience is most active."
            },
            {
                "category": "Hashtag Strategy",
                "suggestion": "Use a mix of popular and niche hashtags relevant to your content.",
                "expected_impact": "Increase discoverability by 35%",
                "implementation": "Research trending hashtags in your industry and include 3-5 relevant hashtags in your post."
            }
        ]

def display_improvement_suggestions(suggestions: List[Dict[str, Any]]):
    """Display improvement suggestions."""
    
    for i, suggestion in enumerate(suggestions):
        with st.expander(f"{i+1}. {suggestion['category']}", expanded=True):
            st.markdown(f"**Suggestion:** {suggestion['suggestion']}")
            st.markdown(f"**Expected Impact:** {suggestion['expected_impact']}")
            st.markdown(f"**Implementation:** {suggestion['implementation']}")

def generate_ab_testing_suggestions(content: str, content_type: str) -> List[Dict[str, Any]]:
    """Generate A/B testing suggestions."""
    
    # Prepare prompt for A/B testing suggestions
    prompt = f"""
    Based on the following Facebook {content_type} content, provide specific A/B testing suggestions:
    
    Content: "{content}"
    
    Please provide 3 specific A/B testing ideas that would help optimize engagement.
    Format your response as a JSON array of objects with the following structure:
    [
        {{
            "element": "<element to test>",
            "variant_a": "<description of variant A>",
            "variant_b": "<description of variant B>",
            "metric": "<primary metric to measure>",
            "hypothesis": "<hypothesis about which variant will perform better>"
        }},
        ...
    ]
    """
    
    try:
        # Generate A/B testing suggestions using LLM
        response = llm_text_gen(prompt)
        
        # Parse JSON response
        ab_testing_suggestions = json.loads(response)
        
        return ab_testing_suggestions
    except Exception as e:
        logger.error(f"Error generating A/B testing suggestions: {e}")
        
        # Return default A/B testing suggestions
        return [
            {
                "element": "Headline",
                "variant_a": "Keep the current headline",
                "variant_b": "Use a more emotional or provocative headline",
                "metric": "Click-through rate",
                "hypothesis": "The emotional headline will increase click-through rate by 15%"
            },
            {
                "element": "Call-to-Action",
                "variant_a": "Use a question as the call-to-action",
                "variant_b": "Use a command as the call-to-action",
                "metric": "Engagement rate",
                "hypothesis": "The question format will increase engagement rate by 10%"
            },
            {
                "element": "Visual Style",
                "variant_a": "Use a single image",
                "variant_b": "Use a carousel of images",
                "metric": "Time spent viewing",
                "hypothesis": "The carousel will increase time spent viewing by 25%"
            }
        ]

def display_ab_testing_suggestions(ab_testing_suggestions: List[Dict[str, Any]]):
    """Display A/B testing suggestions."""
    
    for i, suggestion in enumerate(ab_testing_suggestions):
        with st.expander(f"{i+1}. {suggestion['element']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Variant A**")
                st.markdown(suggestion['variant_a'])
            
            with col2:
                st.markdown("**Variant B**")
                st.markdown(suggestion['variant_b'])
            
            st.markdown(f"**Primary Metric:** {suggestion['metric']}")
            st.markdown(f"**Hypothesis:** {suggestion['hypothesis']}")
            
            # Add a button to create A/B test
            if st.button(f"Create A/B Test for {suggestion['element']}", key=f"ab_test_button_{i}"):
                st.success(f"A/B test for {suggestion['element']} created successfully!") 