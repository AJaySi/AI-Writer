"""
Module for displaying Google Trends data in the Streamlit UI.

This module provides functions for visualizing Google Trends data, including:
- Interest over time
- Regional interest
- Related queries
- Related topics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging

# Set up logging
logger = logging.getLogger(__name__)

def display_google_trends_data(trends_data, search_keyword):
    """
    Display Google Trends data in a structured format with tabs for different sections.
    
    Args:
        trends_data (dict): Dictionary containing Google Trends data
        search_keyword (str): The search keyword used for the analysis
    """
    if not trends_data:
        st.warning("No Google Trends data available for this search.")
        return
        
    st.subheader(f"Google Trends Analysis for '{search_keyword}'")
    
    # Add an informative message about Google Trends
    with st.expander("ℹ️ About Google Trends Data", expanded=False):
        st.markdown("""
        **What is Google Trends?**
        
        Google Trends is a public web facility that shows how often a particular search-term is entered relative to the total search-volume across various regions of the world, and in various languages.
        
        **What data is shown here?**
        
        - **Related Keywords**: Terms that are frequently searched together with your keyword
        - **Interest Over Time**: How interest in your keyword has changed over the past 12 months
        - **Regional Interest**: Where in the world your keyword is most popular
        - **Related Queries**: What people search for before and after searching for your keyword
        - **Related Topics**: Topics that are closely related to your keyword
        
        **How to interpret the data:**
        
        - Interest values range from 0 to 100, where 100 is the peak popularity for the term
        - A value of 50 means the term is half as popular as the peak
        - A value of 0 means there was not enough data for this term
        """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Related Keywords", 
        "Interest Over Time", 
        "Regional Interest", 
        "Related Queries", 
        "Related Topics"
    ])
    
    with tab1:
        display_keywords_section(trends_data.get('related_keywords', []))
        
    with tab2:
        display_interest_over_time(trends_data.get('interest_over_time', pd.DataFrame()))
        
    with tab3:
        display_regional_interest(trends_data.get('regional_interest', pd.DataFrame()))
        
    with tab4:
        display_related_queries(trends_data.get('related_queries', pd.DataFrame()))
        
    with tab5:
        display_related_topics(trends_data.get('related_topics', pd.DataFrame()))
        
    # Add a footer with data source information
    st.markdown("---")
    st.caption("Data source: Google Trends | Last updated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))

def display_keywords_section(keywords):
    """Display related keywords from Google Trends in a table format."""
    if not keywords:
        st.info("No related keywords data available.")
        return
        
    st.subheader("Related Keywords")
    st.write("Keywords related to your search:")
    
    # Add explanation about related keywords
    with st.expander("ℹ️ About Related Keywords", expanded=False):
        st.markdown("""
        **What are Related Keywords?**
        
        Related keywords are terms that are frequently searched together with your main keyword. 
        These keywords can help you understand what topics are associated with your search term 
        and can be valuable for content planning and SEO strategies.
        
        **How to use this data:**
        
        - Use these keywords to expand your content strategy
        - Identify gaps in your content that you could fill
        - Understand what your audience is interested in
        - Improve your SEO by incorporating these terms naturally in your content
        """)
    
    # Create a DataFrame for better display
    df = pd.DataFrame(keywords, columns=['Keyword'])
    st.dataframe(df, use_container_width=True)
    
    # Add a note about the number of keywords
    st.caption(f"Found {len(keywords)} related keywords")

def display_interest_over_time(interest_df):
    """Display a chart showing interest over time for a given search keyword."""
    if interest_df.empty:
        st.info("No interest over time data available.")
        return
        
    st.subheader("Interest Over Time")
    
    # Add explanation about interest over time
    with st.expander("ℹ️ About Interest Over Time", expanded=False):
        st.markdown("""
        **What is Interest Over Time?**
        
        Interest Over Time shows how interest in your search term has changed over the past 12 months.
        The data is normalized and presented on a scale from 0 to 100, where 100 is the peak popularity 
        for the term, 50 means the term is half as popular, and 0 means there was not enough data.
        
        **How to interpret this chart:**
        
        - Look for peaks and valleys to identify trends
        - Compare with seasonal patterns or events
        - Identify if interest is growing, declining, or stable
        - Use this data to time your content releases for maximum impact
        """)
    
    try:
        # Ensure we have the required columns
        if 'date' not in interest_df.columns:
            st.error("Interest over time data is missing the 'date' column.")
            return
            
        if 'interest' not in interest_df.columns:
            st.error("Interest over time data is missing the 'interest' column.")
            return
            
        # Create the chart
        fig = px.line(
            interest_df, 
            x='date', 
            y='interest',
            title='Interest Over Time',
            labels={'date': 'Date', 'interest': 'Interest'},
            line_shape='spline'
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Interest",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics
        if not interest_df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Interest", f"{interest_df['interest'].mean():.1f}")
            with col2:
                st.metric("Peak Interest", f"{interest_df['interest'].max():.1f}")
            with col3:
                st.metric("Lowest Interest", f"{interest_df['interest'].min():.1f}")
        
    except Exception as e:
        st.error(f"Error displaying interest over time chart: {str(e)}")
        logger.error(f"Error in display_interest_over_time: {e}")

def display_regional_interest(regional_df):
    """Display a chart showing interest by region for the search keyword."""
    if regional_df.empty:
        st.info("No regional interest data available.")
        return
        
    st.subheader("Regional Interest")
    
    # Add explanation about regional interest
    with st.expander("ℹ️ About Regional Interest", expanded=False):
        st.markdown("""
        **What is Regional Interest?**
        
        Regional Interest shows how interest in your search term varies across different countries.
        The data is normalized and presented on a scale from 0 to 100, where 100 is the peak popularity 
        for the term in that region, 50 means the term is half as popular, and 0 means there was not enough data.
        
        **How to interpret this map:**
        
        - Darker colors indicate higher interest in that region
        - Lighter colors indicate lower interest
        - Hover over a country to see the exact interest value
        - Use this data to target your content to specific regions
        """)
    
    try:
        # Ensure we have the required columns
        if 'country_code' not in regional_df.columns:
            st.error("Regional interest data is missing the 'country_code' column.")
            return
            
        if 'interest' not in regional_df.columns:
            st.error("Regional interest data is missing the 'interest' column.")
            return
            
        # Create the choropleth map
        fig = go.Figure(data=go.Choropleth(
            locations=regional_df['country_code'],
            z=regional_df['interest'],
            text=regional_df['country_code'],  # This will show in the hover text
            colorscale='Viridis',
            colorbar_title="Interest Level",
            zmin=0,
            zmax=100,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            showscale=True,
            colorbar=dict(
                title="Interest Level",
                tickformat=".0f",
                tickmode="linear",
                tick0=0,
                dtick=20
            )
        ))
        
        # Update the layout for better visualization
        fig.update_layout(
            title=dict(
                text='Regional Interest Distribution',
                x=0.5,
                xanchor='center'
            ),
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                showland=True,
                landcolor='lightgray',
                showocean=True,
                oceancolor='aliceblue',
                showcountries=True,
                countrycolor='darkgray'
            ),
            width=800,
            height=500,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        # Display the map
        st.plotly_chart(fig, use_container_width=True)
        
        # Display top 5 countries with highest interest
        if not regional_df.empty:
            st.subheader("Top Regions by Interest")
            top_regions = regional_df.sort_values('interest', ascending=False).head(5)
            
            # Create a more visually appealing bar chart for top regions
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=top_regions['country_code'],
                    y=top_regions['interest'],
                    text=top_regions['interest'].round(1),
                    textposition='auto',
                    marker_color='rgb(55, 83, 109)'
                )
            ])
            
            fig_bar.update_layout(
                title='Top 5 Regions by Interest Level',
                xaxis_title='Region',
                yaxis_title='Interest Level',
                yaxis_range=[0, 100],
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying regional interest chart: {str(e)}")
        logger.error(f"Error in display_regional_interest: {e}")

def display_related_queries(queries_df):
    """Display related queries in a structured format."""
    if queries_df.empty:
        st.info("No related queries data available.")
        return
        
    st.subheader("Related Queries")
    
    # Add explanation about related queries
    with st.expander("ℹ️ About Related Queries", expanded=False):
        st.markdown("""
        **What are Related Queries?**
        
        Related Queries show what people search for before and after searching for your keyword.
        These queries can help you understand the search intent and context around your keyword.
        
        **How to interpret this data:**
        
        - The 'value' column shows the relative interest compared to your main keyword
        - Higher values indicate stronger association with your keyword
        - Use these queries to expand your content strategy
        - Identify what questions your audience is trying to answer
        """)
    
    try:
        # Ensure we have the required columns
        if 'query' not in queries_df.columns:
            st.error("Related queries data is missing the 'query' column.")
            return
            
        if 'value' not in queries_df.columns:
            st.error("Related queries data is missing the 'value' column.")
            return
            
        # Sort by value in descending order
        queries_df = queries_df.sort_values('value', ascending=False)
        
        # Display as a table
        st.dataframe(queries_df, use_container_width=True)
        
        # Add a note about the number of queries
        st.caption(f"Found {len(queries_df)} related queries")
        
    except Exception as e:
        st.error(f"Error displaying related queries: {str(e)}")
        logger.error(f"Error in display_related_queries: {e}")

def display_trending_searches(trending_df):
    """Display trending searches in the UI."""
    if trending_df.empty:
        st.info("No trending searches data available.")
        return
        
    st.subheader("📊 Trending Searches")
    
    # Display as numbered list with emojis
    for idx, search in enumerate(trending_df[0].head(10), 1):
        st.write(f"{idx}. 🔍 {search}")

def display_realtime_trends(trends_df):
    """Display realtime trending searches in the UI."""
    if trends_df.empty:
        st.info("No realtime trends data available.")
        return
        
    st.subheader("⚡ Realtime Trends")
    
    # Create tabs for different categories
    if not trends_df.empty:
        # Display top 5 trends with their titles and articles
        for _, row in trends_df.head(5).iterrows():
            with st.expander(f"🔥 {row.get('title', 'Trending Topic')}"):
                st.write(f"**Traffic:** {row.get('traffic', 'N/A')}")
                if 'articles' in row:
                    st.write("📰 Related Articles:")
                    for article in row['articles'][:3]:  # Show top 3 articles
                        st.write(f"- {article['title']}")



def display_related_topics(topics_df):
    """Display related topics in a structured format."""
    if topics_df.empty:
        st.info("No related topics data available.")
        return
        
    st.subheader("Related Topics")
    
    # Add explanation about related topics
    with st.expander("ℹ️ About Related Topics", expanded=False):
        st.markdown("""
        **What are Related Topics?**
        
        Related Topics show broader topics that are associated with your search term.
        These topics can help you understand the broader context and themes related to your keyword.
        
        **How to interpret this data:**
        
        - The 'value' column shows the relative interest compared to your main keyword
        - Higher values indicate stronger association with your keyword
        - Use these topics to understand the broader context of your keyword
        - Identify themes that might be relevant to your content strategy
        """)
    
    try:
        # Ensure we have the required columns
        if 'topic' not in topics_df.columns:
            st.error("Related topics data is missing the 'topic' column.")
            return
            
        if 'value' not in topics_df.columns:
            st.error("Related topics data is missing the 'value' column.")
            return
            
        # Sort by value in descending order
        topics_df = topics_df.sort_values('value', ascending=False)
        
        # Display as a table
        st.dataframe(topics_df, use_container_width=True)
        
        # Add a note about the number of topics
        st.caption(f"Found {len(topics_df)} related topics")
        
    except Exception as e:
        st.error(f"Error displaying related topics: {str(e)}")
        logger.error(f"Error in display_related_topics: {e}")

def process_trends_data(trends_data):
    """
    Process and format Google Trends data for display.
    
    Args:
        trends_data (dict): Raw Google Trends data
        
    Returns:
        dict: Formatted data ready for display
    """
    if not trends_data:
        return {}
        
    processed_data = {}
    
    # Process related keywords
    if 'related_keywords' in trends_data:
        processed_data['related_keywords'] = trends_data['related_keywords']
        
    # Process interest over time
    if 'interest_over_time' in trends_data and not trends_data['interest_over_time'].empty:
        processed_data['interest_over_time'] = trends_data['interest_over_time']
        
    # Process regional interest
    if 'regional_interest' in trends_data and not trends_data['regional_interest'].empty:
        processed_data['regional_interest'] = trends_data['regional_interest']
        
    # Process related queries
    if 'related_queries' in trends_data and not trends_data['related_queries'].empty:
        processed_data['related_queries'] = trends_data['related_queries']
        
    # Process related topics
    if 'related_topics' in trends_data and not trends_data['related_topics'].empty:
        processed_data['related_topics'] = trends_data['related_topics']
        
    return processed_data 