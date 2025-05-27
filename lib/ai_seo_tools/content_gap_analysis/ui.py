"""
Streamlit UI for Content Gap Analysis workflow.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
from .main import ContentGapAnalysis
from .keyword_researcher import KeywordResearcher
from .competitor_analyzer import CompetitorAnalyzer
from .website_analyzer import WebsiteAnalyzer
from .recommendation_engine import RecommendationEngine
from .utils.ai_processor import AIProcessor
from .navigation import show_content_gap_analysis_nav
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ContentGapAnalysisUI:
    """Streamlit UI for Content Gap Analysis workflow."""
    
    def __init__(self):
        """Initialize the UI components."""
        # Initialize session state for progress tracking
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
        if 'analysis_results' not in st.session_state:
            st.session_state.analysis_results = {}
        
        # Initialize analysis components
        self.analyzer = ContentGapAnalysis()
        self.keyword_researcher = KeywordResearcher()
        self.competitor_analyzer = CompetitorAnalyzer()
        self.website_analyzer = WebsiteAnalyzer()
        self.recommendation_engine = RecommendationEngine()
        self.ai_processor = AIProcessor()
    
    def run(self):
        """Run the Streamlit interface."""
        try:
            # Show navigation
            nav_option = show_content_gap_analysis_nav()
            
            # Main content area
            st.title("Content Gap Analysis")
            st.markdown("""
            This tool helps you identify content gaps and opportunities by analyzing your website,
            competitors, and market trends. Follow the steps below to get started.
            """)
            
            # Progress tracking
            self._show_progress()
            
            # Main workflow steps
            if nav_option == "Website Analysis" or st.session_state.current_step == 1:
                self._website_analysis_step()
            elif nav_option == "Competitor Analysis" or st.session_state.current_step == 2:
                self._competitor_analysis_step()
            elif nav_option == "Keyword Research" or st.session_state.current_step == 3:
                self._keyword_research_step()
            elif nav_option == "Recommendations" or st.session_state.current_step == 4:
                self._recommendations_step()
            else:
                self._export_results()
        except Exception as e:
            logger.error(f"Error in run method: {str(e)}", exc_info=True)
            st.error(f"An error occurred: {str(e)}")
    
    def _show_progress(self):
        """Display progress tracking."""
        steps = [
            "Website Analysis",
            "Competitor Analysis",
            "Keyword Research",
            "Recommendations",
            "Export Results"
        ]
        
        progress = st.session_state.current_step / len(steps)
        st.progress(progress)
        
        cols = st.columns(len(steps))
        for i, col in enumerate(cols):
            with col:
                if i + 1 < st.session_state.current_step:
                    st.success(f"✓ {steps[i]}")
                elif i + 1 == st.session_state.current_step:
                    st.info(f"→ {steps[i]}")
                else:
                    st.text(f"○ {steps[i]}")
    
    def _website_analysis_step(self):
        """Website analysis step UI."""
        try:
            st.header("Step 1: Website Analysis")
            
            # Display previous results if they exist
            if 'website' in st.session_state.analysis_results:
                st.info("Previous analysis results found. You can analyze a new website or proceed to the next step.")
                self._display_website_analysis(st.session_state.analysis_results['website'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Analyze New Website"):
                        st.session_state.analysis_results.pop('website', None)
                        st.rerun()
                with col2:
                    if st.button("Proceed to Competitor Analysis"):
                        st.session_state.current_step = 2
                        st.rerun()
                return
            
            # Create form for new analysis
            with st.form("website_analysis_form"):
                website_url = st.text_input("Enter your website URL")
                industry = st.text_input("Enter your industry/niche")
                
                submitted = st.form_submit_button("Analyze Website")
            
            # Handle form submission outside the form
            if submitted and website_url and industry:
                # Initialize progress tracking
                if 'analysis_progress' not in st.session_state:
                    st.session_state.analysis_progress = {
                        'status': 'initializing',
                        'current_step': 'Starting Analysis',
                        'progress': 0,
                        'details': 'Initializing analysis...'
                    }
                
                # Create progress container
                progress_container = st.empty()
                status_container = st.empty()
                details_container = st.empty()
                
                # Update progress display
                def update_progress_display():
                    progress = st.session_state.analysis_progress
                    
                    # Update progress bar
                    with progress_container:
                        st.progress(progress['progress'] / 100)
                    
                    # Update status
                    with status_container:
                        if progress['status'] == 'error':
                            st.error(f"Error: {progress['current_step']}")
                        elif progress['status'] == 'completed':
                            st.success(f"✓ {progress['current_step']}")
                        else:
                            st.info(f"→ {progress['current_step']}")
                    
                    # Update details
                    with details_container:
                        st.write(progress['details'])
                
                # Initial progress display
                update_progress_display()
                
                try:
                    # Get basic analysis
                    results = self.website_analyzer.analyze(website_url)
                    
                    # Update progress from analyzer
                    st.session_state.analysis_progress = self.website_analyzer.progress.get_progress()
                    update_progress_display()
                    
                    if isinstance(results, dict) and 'error' in results:
                        st.error(f"Error in website analysis: {results['error']}")
                        return
                    
                    # Get AI-enhanced analysis
                    st.session_state.analysis_progress.update({
                        'current_step': 'AI Analysis',
                        'progress': 95,
                        'details': 'Performing AI-enhanced analysis...'
                    })
                    update_progress_display()
                    
                    ai_analysis = self.ai_processor.analyze_content({
                        'url': website_url,
                        'industry': industry,
                        'content': results
                    })
                    
                    # Combine results
                    if isinstance(results, dict):
                        results.update(ai_analysis)
                    else:
                        results = {'error': 'Invalid analysis results format'}
                    
                    # Store results in session state
                    st.session_state.analysis_results['website'] = results
                    
                    # Update final progress
                    st.session_state.analysis_progress.update({
                        'status': 'completed',
                        'current_step': 'Analysis Complete',
                        'progress': 100,
                        'details': 'Analysis completed successfully!'
                    })
                    update_progress_display()
                    
                    # Display results
                    self._display_website_analysis(results)
                    
                except Exception as e:
                    logger.error(f"Error during website analysis: {str(e)}", exc_info=True)
                    st.session_state.analysis_progress.update({
                        'status': 'error',
                        'current_step': 'Analysis Failed',
                        'details': f"Error during website analysis: {str(e)}"
                    })
                    update_progress_display()
                    st.error(f"Error during website analysis: {str(e)}")
                    return
                        
        except Exception as e:
            logger.error(f"Error in website analysis step: {str(e)}", exc_info=True)
            st.error(f"Error in website analysis: {str(e)}")
    
    def _display_website_analysis(self, results: Dict[str, Any]):
        """Display website analysis results."""
        try:
            if not isinstance(results, dict):
                st.error("Invalid analysis results format")
                return
                
            if 'error' in results:
                st.error(f"Error in analysis: {results['error']}")
                return
            
            # Content Metrics
            st.subheader("Content Metrics")
            content_metrics = results.get('content_metrics', {})
            
            if content_metrics:
                # Basic metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Word Count", f"{content_metrics.get('word_count', 0):,}")
                with col2:
                    st.metric("Headings", f"{content_metrics.get('heading_count', 0):,}")
                with col3:
                    st.metric("Images", f"{content_metrics.get('image_count', 0):,}")
                with col4:
                    st.metric("Links", f"{content_metrics.get('link_count', 0):,}")
                
                # Content Structure Visualization
                st.write("Content Structure")
                heading_data = {
                    'Type': ['H1', 'H2', 'H3', 'Paragraphs'],
                    'Count': [
                        content_metrics.get('h1_count', 0),
                        content_metrics.get('h2_count', 0),
                        content_metrics.get('h3_count', 0),
                        content_metrics.get('paragraph_count', 0)
                    ]
                }
                fig = px.bar(
                    heading_data,
                    x='Type',
                    y='Count',
                    title="Content Structure Distribution",
                    color='Type',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Content Features
                st.write("Content Features")
                features = {
                    'Feature': ['Meta Description', 'Robots.txt', 'Sitemap'],
                    'Status': [
                        content_metrics.get('has_meta_description', False),
                        content_metrics.get('has_robots_txt', False),
                        content_metrics.get('has_sitemap', False)
                    ]
                }
                fig = px.bar(
                    features,
                    x='Feature',
                    y='Status',
                    title="Content Features Status",
                    color='Status',
                    color_discrete_sequence=['red', 'green']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # SEO Metrics
            st.subheader("SEO Metrics")
            seo_metrics = results.get('seo_metrics', {})
            
            if seo_metrics:
                # Basic metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Overall Score", f"{seo_metrics.get('overall_score', 0):.1f}%")
                with col2:
                    content_quality = seo_metrics.get('content', {}).get('content_quality_score', 0)
                    st.metric("Content Quality", f"{content_quality:.1f}%")
                with col3:
                    readability = seo_metrics.get('content', {}).get('readability_score', 0)
                    st.metric("Readability", f"{readability:.1f}%")
                with col4:
                    keyword_density = seo_metrics.get('content', {}).get('keyword_density', 0)
                    st.metric("Keyword Density", f"{keyword_density:.1f}%")
                
                # SEO Scores Radar Chart
                seo_scores = {
                    'Metric': ['Overall', 'Content Quality', 'Readability', 'Keyword Density'],
                    'Score': [
                        seo_metrics.get('overall_score', 0),
                        content_quality,
                        readability,
                        keyword_density
                    ]
                }
                fig = px.line_polar(
                    seo_scores,
                    r='Score',
                    theta='Metric',
                    line_close=True,
                    title="SEO Performance Overview"
                )
                fig.update_traces(fill='toself')
                st.plotly_chart(fig, use_container_width=True)
                
                # Meta Tags Analysis
                st.write("Meta Tags Analysis")
                meta_tags = seo_metrics.get('meta_tags', {})
                if meta_tags:
                    # Title Analysis
                    title = meta_tags.get('title', {})
                    st.write("Title Tag")
                    st.write(f"Status: {'✅' if title.get('status') == 'good' else '❌'}")
                    st.write(f"Value: {title.get('value', 'N/A')}")
                    st.write(f"Length: {title.get('length', 0)} characters")
                    st.write(f"Score: {title.get('score', 0)}%")
                    if title.get('recommendation'):
                        st.warning(title.get('recommendation'))
                    
                    # Description Analysis
                    desc = meta_tags.get('description', {})
                    st.write("Meta Description")
                    st.write(f"Status: {'✅' if desc.get('status') == 'good' else '❌'}")
                    st.write(f"Value: {desc.get('value', 'N/A')}")
                    st.write(f"Length: {desc.get('length', 0)} characters")
                    st.write(f"Score: {desc.get('score', 0)}%")
                    if desc.get('recommendation'):
                        st.warning(desc.get('recommendation'))
                    
                    # Keywords Analysis
                    keywords = meta_tags.get('keywords', {})
                    st.write("Meta Keywords")
                    st.write(f"Status: {'✅' if keywords.get('status') == 'good' else '❌'}")
                    st.write(f"Value: {keywords.get('value', 'N/A')}")
                    if keywords.get('recommendation'):
                        st.warning(keywords.get('recommendation'))
            
            # Technical Metrics
            st.subheader("Technical Metrics")
            technical_info = results.get('technical_info', {})
            
            if technical_info:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Basic Information")
                    st.metric("Status Code", technical_info.get('status_code', 'N/A'))
                    st.metric("Server", technical_info.get('server_info', {}).get('server', 'N/A'))
                    st.metric("Content Type", technical_info.get('server_info', {}).get('content_type', 'N/A'))
                with col2:
                    st.write("Security Information")
                    security_info = technical_info.get('security_info', {})
                    security_data = {
                        'Feature': ['SSL', 'HSTS', 'XSS Protection'],
                        'Status': [
                            security_info.get('ssl', False),
                            security_info.get('hsts', False),
                            security_info.get('xss_protection', False)
                        ]
                    }
                    fig = px.bar(
                        security_data,
                        x='Feature',
                        y='Status',
                        title="Security Features Status",
                        color='Status',
                        color_discrete_sequence=['red', 'green']
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Performance Metrics
            st.subheader("Performance Metrics")
            performance = results.get('performance', {})
            
            if performance:
                # Basic metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Load Time", f"{performance.get('load_time', 0):.2f}s")
                with col2:
                    st.metric("Page Size", f"{performance.get('page_size', 0):.1f} KB")
                with col3:
                    st.metric("Status Code", performance.get('status_code', 'N/A'))
                with col4:
                    st.metric("Response Time", f"{performance.get('response_time', 0):.2f}s")
            
            # Insights and Recommendations
            st.subheader("Insights and Recommendations")
            insights = results.get('insights', [])
            if insights:
                for insight in insights:
                    st.info(f"• {insight}")
            else:
                st.info("No specific insights available")
                
        except Exception as e:
            logger.error(f"Error displaying website analysis: {str(e)}", exc_info=True)
            st.error(f"Error displaying website analysis: {str(e)}")
    
    def _competitor_analysis_step(self):
        """Competitor analysis step UI."""
        try:
            st.header("Step 2: Competitor Analysis")
            
            with st.form("competitor_analysis_form"):
                competitors = st.text_area(
                    "Enter competitor URLs (one per line)",
                    help="Enter the URLs of your main competitors"
                )
                
                submitted = st.form_submit_button("Analyze Competitors")
                
                if submitted and competitors:
                    with st.spinner("Analyzing competitors..."):
                        competitor_urls = [url.strip() for url in competitors.split('\n') if url.strip()]
                        results = self.competitor_analyzer.analyze(competitor_urls)
                        
                        # Get AI-enhanced competitor analysis
                        ai_analysis = self.ai_processor.analyze_competitors({
                            'competitors': competitor_urls,
                            'analysis': results
                        })
                        
                        # Combine results
                        results.update(ai_analysis)
                        st.session_state.analysis_results['competitors'] = results
                        
                        # Display results
                        self._display_competitor_analysis(results)
                        
                        # Move to next step
                        st.session_state.current_step = 3
                        st.rerun()
        except Exception as e:
            logger.error(f"Error in competitor analysis step: {str(e)}", exc_info=True)
            st.error(f"Error in competitor analysis: {str(e)}")
    
    def _display_competitor_analysis(self, results: dict):
        """Display competitor analysis results."""
        st.subheader("Competitor Analysis Results")
        
        # Competitor comparison
        st.subheader("Competitor Comparison")
        comp_data = pd.DataFrame(results.get('comparison', []))
        if not comp_data.empty:
            fig = px.bar(
                comp_data,
                x='competitor',
                y='score',
                color='metric',
                title="Competitor Comparison"
            )
            st.plotly_chart(fig)
        
        # AI-Enhanced Competitor Analysis
        st.subheader("AI-Enhanced Competitor Analysis")
        
        # Competitor Trend Analysis
        trend_data = results.get('competitor_trends', {})
        if trend_data:
            fig = go.Figure()
            for competitor, trends in trend_data.items():
                fig.add_trace(go.Scatter(
                    x=trends.get('timeline', []),
                    y=trends.get('scores', []),
                    name=competitor,
                    mode='lines+markers'
                ))
            fig.update_layout(
                title="Competitor Performance Trends",
                xaxis_title="Timeline",
                yaxis_title="Score"
            )
            st.plotly_chart(fig)
        
        # Content gaps
        st.subheader("Content Gaps")
        gaps = results.get('content_gaps', [])
        for gap in gaps:
            st.info(f"• {gap}")
        
        # AI-Generated Competitive Insights
        st.subheader("Competitive Insights")
        insights = results.get('competitive_insights', {})
        if insights:
            for category, points in insights.items():
                with st.expander(f"{category.title()} Analysis"):
                    for point in points:
                        st.success(f"• {point}")
    
    def _keyword_research_step(self):
        """Keyword research step UI."""
        try:
            st.header("Step 3: Keyword Research")
            
            with st.form("keyword_research_form"):
                industry = st.text_input(
                    "Enter your industry/niche",
                    value=st.session_state.analysis_results.get('website', {}).get('industry', '')
                )
                
                submitted = st.form_submit_button("Research Keywords")
                
                if submitted and industry:
                    with st.spinner("Researching keywords..."):
                        results = self.keyword_researcher.research(industry)
                        
                        # Get AI-enhanced keyword analysis
                        ai_analysis = self.ai_processor.analyze_keywords({
                            'industry': industry,
                            'keywords': results
                        })
                        
                        # Combine results
                        results.update(ai_analysis)
                        st.session_state.analysis_results['keywords'] = results
                        
                        # Display results
                        self._display_keyword_research(results)
                        
                        # Move to next step
                        st.session_state.current_step = 4
                        st.rerun()
        except Exception as e:
            logger.error(f"Error in keyword research step: {str(e)}", exc_info=True)
            st.error(f"Error in keyword research: {str(e)}")
    
    def _display_keyword_research(self, results: dict):
        """Display keyword research results."""
        st.subheader("Keyword Research Results")
        
        # Keyword metrics
        st.subheader("Keyword Metrics")
        keyword_data = pd.DataFrame(results.get('keywords', []))
        if not keyword_data.empty:
            fig = px.scatter(
                keyword_data,
                x='search_volume',
                y='difficulty',
                size='relevance_score',
                hover_data=['keyword'],
                title="Keyword Opportunities"
            )
            st.plotly_chart(fig)
        
        # AI-Enhanced Keyword Analysis
        st.subheader("AI-Enhanced Keyword Analysis")
        
        # Keyword Trend Analysis
        trend_data = results.get('keyword_trends', {})
        if trend_data:
            fig = go.Figure()
            for keyword, trends in trend_data.items():
                fig.add_trace(go.Scatter(
                    x=trends.get('timeline', []),
                    y=trends.get('scores', []),
                    name=keyword,
                    mode='lines+markers'
                ))
            fig.update_layout(
                title="Keyword Trend Analysis",
                xaxis_title="Timeline",
                yaxis_title="Trend Score"
            )
            st.plotly_chart(fig)
        
        # Search intent distribution
        st.subheader("Search Intent Distribution")
        intent_data = pd.DataFrame(results.get('search_intent', {}).get('summary', {}))
        if not intent_data.empty:
            fig = px.pie(
                intent_data,
                values='count',
                names='intent',
                title="Search Intent Distribution"
            )
            st.plotly_chart(fig)
        
        # Content format suggestions
        st.subheader("Content Format Suggestions")
        formats = results.get('content_formats', [])
        for format in formats:
            st.info(f"• {format}")
        
        # AI-Generated Keyword Insights
        st.subheader("Keyword Insights")
        insights = results.get('keyword_insights', {})
        if insights:
            for category, points in insights.items():
                with st.expander(f"{category.title()} Insights"):
                    for point in points:
                        st.success(f"• {point}")
    
    def _recommendations_step(self):
        """Recommendations step UI."""
        try:
            st.header("Step 4: Content Recommendations")
            
            with st.spinner("Generating recommendations..."):
                results = self.recommendation_engine.generate_recommendations(
                    st.session_state.analysis_results
                )
                
                # Get AI-enhanced recommendations
                ai_recommendations = self.ai_processor.analyze_recommendations({
                    'recommendations': results,
                    'analysis': st.session_state.analysis_results
                })
                
                # Combine results
                results.update(ai_recommendations)
                st.session_state.analysis_results['recommendations'] = results
                
                # Display results
                self._display_recommendations(results)
                
                # Move to next step
                st.session_state.current_step = 5
                st.rerun()
        except Exception as e:
            logger.error(f"Error in recommendations step: {str(e)}", exc_info=True)
            st.error(f"Error in recommendations: {str(e)}")
    
    def _display_recommendations(self, results: dict):
        """Display content recommendations."""
        st.subheader("Content Recommendations")
        
        # Priority recommendations
        st.subheader("Priority Recommendations")
        priorities = results.get('priorities', [])
        for priority in priorities:
            st.success(f"• {priority}")
        
        # AI-Enhanced Recommendations
        st.subheader("AI-Enhanced Recommendations")
        
        # Recommendation Impact Analysis
        impact_data = results.get('impact_analysis', {})
        if impact_data:
            fig = go.Figure()
            for metric, values in impact_data.items():
                fig.add_trace(go.Bar(
                    name=metric,
                    x=values.get('categories', []),
                    y=values.get('scores', [])
                ))
            fig.update_layout(
                title="Recommendation Impact Analysis",
                xaxis_title="Categories",
                yaxis_title="Impact Score",
                barmode='group'
            )
            st.plotly_chart(fig)
        
        # Implementation timeline
        st.subheader("Implementation Timeline")
        timeline = results.get('timeline', [])
        for item in timeline:
            st.info(f"• {item}")
        
        # Expected impact
        st.subheader("Expected Impact")
        impact = results.get('impact', {})
        for metric, value in impact.items():
            st.metric(metric, value)
        
        # AI-Generated Strategic Insights
        st.subheader("Strategic Insights")
        insights = results.get('strategic_insights', {})
        if insights:
            for category, points in insights.items():
                with st.expander(f"{category.title()} Strategy"):
                    for point in points:
                        st.success(f"• {point}")
    
    def _export_results(self):
        """Export results step UI."""
        st.header("Step 5: Export Results")
        
        # Export options
        export_format = st.radio(
            "Choose export format",
            ["JSON", "CSV", "PDF"]
        )
        
        if st.button("Export Results"):
            if export_format == "JSON":
                self._export_json()
            elif export_format == "CSV":
                self._export_csv()
            else:
                st.info("PDF export coming soon!")
    
    def _export_json(self):
        """Export results as JSON."""
        results = st.session_state.analysis_results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_gap_analysis_{timestamp}.json"
        
        st.download_button(
            "Download JSON",
            data=json.dumps(results, indent=2),
            file_name=filename,
            mime="application/json"
        )
    
    def _export_csv(self):
        """Export results as CSV."""
        results = st.session_state.analysis_results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Convert results to CSV format
        csv_data = []
        for section, data in results.items():
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        item['section'] = section
                        csv_data.append(item)
            elif isinstance(data, dict):
                data['section'] = section
                csv_data.append(data)
        
        if csv_data:
            df = pd.DataFrame(csv_data)
            filename = f"content_gap_analysis_{timestamp}.csv"
            
            st.download_button(
                "Download CSV",
                data=df.to_csv(index=False),
                file_name=filename,
                mime="text/csv"
            )

def main():
    """Main entry point for the Streamlit app."""
    ui = ContentGapAnalysisUI()
    ui.run()

if __name__ == "__main__":
    main() 