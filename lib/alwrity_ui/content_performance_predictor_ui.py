"""
Streamlit UI for Content Performance Predictor
Interactive interface for predicting and optimizing content performance
"""

import streamlit as st
import asyncio
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Any, Optional
import logging

# Import the predictor
try:
    from lib.content_performance_predictor.content_performance_predictor import (
        ContentPerformancePredictor, 
        ContentType, 
        predict_content_performance
    )
except ImportError:
    st.error("Content Performance Predictor module not found. Please check the installation.")

logger = logging.getLogger(__name__)

class ContentPerformancePredictorUI:
    """Streamlit UI for Content Performance Predictor"""
    
    def __init__(self):
        self.predictor = None
        self.initialize_predictor()
    
    def initialize_predictor(self):
        """Initialize the predictor with error handling"""
        try:
            self.predictor = ContentPerformancePredictor()
        except Exception as e:
            st.error(f"Failed to initialize predictor: {str(e)}")
            self.predictor = None
    
    def render_main_interface(self):
        """Render the main Content Performance Predictor interface"""
        st.title("🎯 Content Performance Predictor")
        st.markdown("### Predict content success before you publish!")
        
        # Create tabs for different features
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Predict Performance", 
            "📈 Batch Analysis", 
            "🔧 Optimization Tools", 
            "📚 Performance History"
        ])
        
        with tab1:
            self.render_single_prediction_tab()
        
        with tab2:
            self.render_batch_analysis_tab()
        
        with tab3:
            self.render_optimization_tab()
        
        with tab4:
            self.render_history_tab()
    
    def render_single_prediction_tab(self):
        """Render single content prediction interface"""
        st.header("Single Content Analysis")
        
        # Input section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Content input
            content_input = st.text_area(
                "Enter your content:",
                height=200,
                placeholder="Paste your content here...\n\nExample:\n🚀 Just discovered an amazing AI writing tool that's changing the game!\n\n#AIWriting #ContentCreation"
            )
            
            # Target keywords
            keywords_input = st.text_input(
                "Target Keywords (optional):",
                placeholder="AI writing, content creation, SEO"
            )
        
        with col2:
            # Content type selection
            content_type = st.selectbox(
                "Content Type:",
                ["twitter", "linkedin", "facebook", "instagram", "blog_post", "email", "youtube"],
                help="Select the platform where you plan to publish"
            )
            
            # Analysis options
            st.subheader("Analysis Options")
            
            include_seo = st.checkbox("Include SEO Analysis", value=True)
            include_trends = st.checkbox("Include Trend Analysis", value=True)
            include_competitor = st.checkbox("Include Competitor Analysis", value=False)
            
            # Advanced settings
            with st.expander("Advanced Settings"):
                target_audience = st.selectbox(
                    "Target Audience:",
                    ["General", "Business", "Tech", "Marketing", "Education", "Entertainment"]
                )
                
                urgency_level = st.slider(
                    "Content Urgency:",
                    0.0, 1.0, 0.5,
                    help="How time-sensitive is this content?"
                )
        
        # Predict button
        if st.button("🎯 Predict Performance", type="primary", use_container_width=True):
            if not content_input.strip():
                st.error("Please enter content to analyze")
                return
            
            # Process keywords
            keywords = [k.strip() for k in keywords_input.split(",")] if keywords_input else None
            
            # Show loading spinner
            with st.spinner("Analyzing content performance..."):
                # Run prediction
                prediction_result = self.run_prediction(
                    content_input,
                    content_type,
                    keywords,
                    include_seo,
                    include_trends,
                    include_competitor
                )
            
            if prediction_result:
                self.display_prediction_results(prediction_result)
            else:
                st.error("Failed to analyze content. Please try again.")
    
    def run_prediction(
        self, 
        content: str, 
        content_type: str, 
        keywords: Optional[List[str]], 
        include_seo: bool,
        include_trends: bool,
        include_competitor: bool
    ) -> Optional[Dict[str, Any]]:
        """Run the content performance prediction"""
        try:
            # Run async prediction
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(
                predict_content_performance(
                    content=content,
                    content_type=content_type,
                    target_keywords=keywords
                )
            )
            
            loop.close()
            return result
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            st.error(f"Prediction failed: {str(e)}")
            return None
    
    def display_prediction_results(self, result: Dict[str, Any]):
        """Display the prediction results with visualizations"""
        st.success("✅ Analysis Complete!")
        
        # Overall score section
        st.subheader("📊 Overall Performance Score")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Overall score gauge
            score = result.get("overall_score", 0)
            self.render_score_gauge(score, "Overall Score")
        
        with col2:
            # Success probability
            prob = result.get("success_probability", 0) * 100
            self.render_score_gauge(prob, "Success Probability")
        
        with col3:
            # Performance rating
            rating = self.get_performance_rating(score)
            st.metric(
                "Performance Rating",
                rating["label"],
                help=rating["description"]
            )
        
        # Detailed scores breakdown
        st.subheader("🔍 Detailed Score Breakdown")
        scores = result.get("individual_scores", {})
        if scores:
            self.render_scores_breakdown(scores)
        
        # Recommendations section
        st.subheader("💡 Optimization Recommendations")
        recommendations = result.get("recommendations", [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
        else:
            st.info("No specific recommendations available")
        
        # Predicted metrics
        st.subheader("📊 Predicted Performance Metrics")
        metrics = result.get("predicted_metrics", {})
        if metrics:
            self.render_predicted_metrics(metrics)
        
        # Content analysis details
        st.subheader("📝 Content Analysis Details")
        analysis = result.get("content_analysis", {})
        if analysis:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Word Count", analysis.get("word_count", 0))
            with col2:
                st.metric("Character Count", analysis.get("character_count", 0))
            with col3:
                st.metric("Hashtags", analysis.get("hashtag_count", 0))
            with col4:
                st.metric("Readability", f"{analysis.get('readability_score', 0):.1f}")
        
        # Export options
        st.subheader("📤 Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate Report"):
                report = self.generate_text_report(result)
                st.text_area("Report:", value=report, height=200)
        
        with col2:
            if st.button("📊 Download JSON"):
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"content_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    def render_score_gauge(self, score: float, title: str):
        """Render a gauge chart for scores"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "green"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_scores_breakdown(self, scores: Dict[str, float]):
        """Render radar chart for score breakdown"""
        categories = list(scores.keys())
        values = list(scores.values())
        
        # Close the radar chart
        categories.append(categories[0])
        values.append(values[0])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Performance Scores'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Performance Score Breakdown"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display scores as metrics
        cols = st.columns(len(scores))
        for i, (category, score) in enumerate(scores.items()):
            with cols[i]:
                st.metric(category.title(), f"{score:.1f}")
    
    def render_predicted_metrics(self, metrics: Dict[str, Any]):
        """Render predicted performance metrics"""
        cols = st.columns(len(metrics))
        
        for i, (metric, value) in enumerate(metrics.items()):
            with cols[i]:
                # Format metric name
                display_name = metric.replace("predicted_", "").replace("_", " ").title()
                st.metric(display_name, f"{value:,}")
    
    def get_performance_rating(self, score: float) -> Dict[str, str]:
        """Get performance rating based on score"""
        if score >= 80:
            return {"label": "Excellent", "description": "High chance of success"}
        elif score >= 60:
            return {"label": "Good", "description": "Solid performance expected"}
        elif score >= 40:
            return {"label": "Average", "description": "Room for improvement"}
        else:
            return {"label": "Needs Work", "description": "Optimization recommended"}
    
    def render_batch_analysis_tab(self):
        """Render batch analysis interface"""
        st.header("Batch Content Analysis")
        st.info("Analyze multiple pieces of content at once")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload CSV with content",
            type=['csv'],
            help="CSV should have columns: 'content', 'content_type', 'keywords' (optional)"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_cols = ['content', 'content_type']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"Missing required columns: {', '.join(missing_cols)}")
                    return
                
                st.success(f"✅ Loaded {len(df)} content items")
                
                # Preview data
                with st.expander("Preview Data"):
                    st.dataframe(df.head())
                
                # Analysis options
                col1, col2 = st.columns(2)
                
                with col1:
                    max_items = st.number_input(
                        "Max items to analyze:",
                        min_value=1,
                        max_value=100,
                        value=min(10, len(df))
                    )
                
                with col2:
                    export_format = st.selectbox(
                        "Export format:",
                        ["CSV", "JSON", "Excel"]
                    )
                
                # Run batch analysis
                if st.button("🚀 Run Batch Analysis", type="primary"):
                    with st.spinner(f"Analyzing {max_items} content items..."):
                        batch_df = df.head(max_items)
                        results = self.run_batch_analysis(batch_df)
                    
                    if results:
                        self.display_batch_results(results)
                    else:
                        st.error("Batch analysis failed")
                        
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    def run_batch_analysis(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Run batch analysis on multiple content items"""
        results = []
        progress = st.progress(0)
        
        for i, row in df.iterrows():
            try:
                content = row['content']
                content_type = row['content_type']
                keywords = row.get('keywords', '').split(',') if row.get('keywords') else None
                
                result = self.run_prediction(content, content_type, keywords, True, True, False)
                if result:
                    result['original_content'] = content
                    result['content_type'] = content_type
                    results.append(result)
                
                progress.progress((i + 1) / len(df))
                
            except Exception as e:
                st.warning(f"Error analyzing row {i}: {str(e)}")
                continue
        
        return results
    
    def display_batch_results(self, results: List[Dict[str, Any]]):
        """Display batch analysis results"""
        st.success(f"✅ Analyzed {len(results)} content items")
        
        # Summary statistics
        st.subheader("📊 Batch Summary")
        
        scores = [r.get('overall_score', 0) for r in results]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Score", f"{avg_score:.1f}")
        with col2:
            st.metric("Best Score", f"{max(scores):.1f}" if scores else "0")
        with col3:
            st.metric("Worst Score", f"{min(scores):.1f}" if scores else "0")
        with col4:
            good_content = len([s for s in scores if s >= 60])
            st.metric("Good Content", f"{good_content}/{len(scores)}")
        
        # Results table
        st.subheader("📋 Detailed Results")
        
        # Create summary DataFrame
        summary_data = []
        for i, result in enumerate(results):
            summary_data.append({
                "Content": result['original_content'][:50] + "..." if len(result['original_content']) > 50 else result['original_content'],
                "Type": result['content_type'],
                "Overall Score": result.get('overall_score', 0),
                "Success Probability": result.get('success_probability', 0) * 100,
                "Engagement": result.get('individual_scores', {}).get('engagement', 0),
                "SEO": result.get('individual_scores', {}).get('seo', 0),
                "Virality": result.get('individual_scores', {}).get('virality', 0)
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
        
        # Download results
        if st.button("📥 Download Results"):
            csv = summary_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    def render_optimization_tab(self):
        """Render content optimization tools"""
        st.header("🔧 Content Optimization Tools")
        
        # A/B Testing section
        st.subheader("🧪 A/B Content Testing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Version A**")
            content_a = st.text_area(
                "Content A:",
                height=150,
                key="content_a",
                placeholder="Enter first version of your content..."
            )
            
        with col2:
            st.markdown("**Version B**")
            content_b = st.text_area(
                "Content B:",
                height=150,
                key="content_b",
                placeholder="Enter second version of your content..."
            )
        
        # Common settings
        content_type = st.selectbox(
            "Content Type for both:",
            ["twitter", "linkedin", "facebook", "instagram", "blog_post", "email", "youtube"],
            key="ab_content_type"
        )
        
        if st.button("⚡ Compare Versions", type="primary"):
            if not content_a.strip() or not content_b.strip():
                st.error("Please enter both versions of content")
                return
            
            with st.spinner("Comparing content versions..."):
                result_a = self.run_prediction(content_a, content_type, None, True, True, False)
                result_b = self.run_prediction(content_b, content_type, None, True, True, False)
            
            if result_a and result_b:
                self.display_ab_comparison(result_a, result_b)
        
        # Optimization suggestions
        st.subheader("💡 Optimization Suggestions")
        
        optimization_content = st.text_area(
            "Content to optimize:",
            height=150,
            placeholder="Enter content for optimization suggestions..."
        )
        
        if st.button("🚀 Get Suggestions") and optimization_content.strip():
            with st.spinner("Generating optimization suggestions..."):
                suggestions = self.generate_optimization_suggestions(optimization_content)
            
            if suggestions:
                st.success("✅ Optimization suggestions generated!")
                for i, suggestion in enumerate(suggestions, 1):
                    st.markdown(f"**{i}.** {suggestion}")
    
    def display_ab_comparison(self, result_a: Dict[str, Any], result_b: Dict[str, Any]):
        """Display A/B test comparison results"""
        st.success("✅ A/B Comparison Complete!")
        
        # Overall comparison
        col1, col2, col3 = st.columns(3)
        
        score_a = result_a.get('overall_score', 0)
        score_b = result_b.get('overall_score', 0)
        winner = "A" if score_a > score_b else "B" if score_b > score_a else "Tie"
        
        with col1:
            st.metric("Version A Score", f"{score_a:.1f}")
        with col2:
            st.metric("Version B Score", f"{score_b:.1f}")
        with col3:
            st.metric("Winner", winner, delta=f"{abs(score_a - score_b):.1f} point difference")
        
        # Detailed comparison chart
        scores_a = result_a.get('individual_scores', {})
        scores_b = result_b.get('individual_scores', {})
        
        categories = list(scores_a.keys())
        values_a = list(scores_a.values())
        values_b = list(scores_b.values())
        
        # Create comparison bar chart
        fig = go.Figure(data=[
            go.Bar(name='Version A', x=categories, y=values_a),
            go.Bar(name='Version B', x=categories, y=values_b)
        ])
        
        fig.update_layout(
            barmode='group',
            title="Detailed Score Comparison",
            yaxis_title="Score",
            xaxis_title="Category"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations comparison
        st.subheader("📋 Recommendations Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Version A Recommendations:**")
            recs_a = result_a.get('recommendations', [])
            for rec in recs_a[:5]:
                st.markdown(f"• {rec}")
        
        with col2:
            st.markdown("**Version B Recommendations:**")
            recs_b = result_b.get('recommendations', [])
            for rec in recs_b[:5]:
                st.markdown(f"• {rec}")
    
    def generate_optimization_suggestions(self, content: str) -> List[str]:
        """Generate optimization suggestions for content"""
        suggestions = []
        
        # Basic content analysis
        word_count = len(content.split())
        char_count = len(content)
        hashtag_count = content.count('#')
        
        # Length optimization
        if word_count < 10:
            suggestions.append("Consider adding more detail to your content for better engagement")
        elif word_count > 50:
            suggestions.append("Consider shortening your content for better social media performance")
        
        # Hashtag optimization
        if hashtag_count == 0:
            suggestions.append("Add relevant hashtags to increase discoverability")
        elif hashtag_count > 5:
            suggestions.append("Reduce the number of hashtags for better readability")
        
        # Engagement optimization
        if '?' not in content:
            suggestions.append("Consider adding a question to encourage engagement")
        
        if '!' not in content and '.' in content:
            suggestions.append("Add some excitement with exclamation marks")
        
        # Call to action
        cta_words = ['click', 'share', 'comment', 'like', 'follow', 'subscribe']
        has_cta = any(word in content.lower() for word in cta_words)
        if not has_cta:
            suggestions.append("Include a clear call-to-action (like, share, comment)")
        
        # Emoji usage
        emoji_count = len([char for char in content if ord(char) > 127])
        if emoji_count == 0:
            suggestions.append("Consider adding relevant emojis to make content more engaging")
        
        return suggestions[:5]  # Limit to top 5 suggestions
    
    def render_history_tab(self):
        """Render performance history interface"""
        st.header("📚 Performance History")
        st.info("Performance history tracking coming soon!")
        st.markdown("This feature will allow you to:")
        st.markdown("• Track your content performance over time")
        st.markdown("• Compare predicted vs actual performance")
        st.markdown("• Identify your best-performing content patterns")
        st.markdown("• Generate performance reports")
    
    def generate_text_report(self, result: Dict[str, Any]) -> str:
        """Generate a text report of the analysis"""
        report = f"""
CONTENT PERFORMANCE ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL PERFORMANCE
Overall Score: {result.get('overall_score', 0):.1f}/100
Success Probability: {result.get('success_probability', 0)*100:.1f}%
Performance Rating: {self.get_performance_rating(result.get('overall_score', 0))['label']}

DETAILED SCORES
"""
        
        scores = result.get('individual_scores', {})
        for category, score in scores.items():
            report += f"{category.title()}: {score:.1f}/100\n"
        
        report += "\nCONTENT ANALYSIS\n"
        analysis = result.get('content_analysis', {})
        for key, value in analysis.items():
            report += f"{key.replace('_', ' ').title()}: {value}\n"
        
        report += "\nRECOMMENDATIONS\n"
        recommendations = result.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        return report

def render_content_performance_predictor():
    """Main function to render the Content Performance Predictor UI"""
    ui = ContentPerformancePredictorUI()
    ui.render_main_interface()

if __name__ == "__main__":
    render_content_performance_predictor() 