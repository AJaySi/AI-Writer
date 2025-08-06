"""
AI-Powered Content Performance Predictor

This module uses AI (LLM) to predict content performance instead of traditional ML models.
Perfect for solo developers who want competitive intelligence without expensive ML infrastructure.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from loguru import logger
import streamlit as st

# Import existing Alwrity modules
from lib.database.twitter_service import TwitterDatabaseService
from lib.ai_web_researcher.google_trends_researcher import do_google_trends_analysis
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen


class AIContentPerformancePredictor:
    """
    AI-powered content performance predictor using LLM intelligence.
    No ML training required - uses AI's existing knowledge of content patterns.
    """
    
    def __init__(self):
        """Initialize the AI predictor."""
        self.twitter_service = TwitterDatabaseService()
        self.platform_configs = {
            'twitter': {
                'optimal_length': 120,
                'hashtag_range': (1, 3),
                'best_times': [9, 12, 15, 18, 21],
                'engagement_factors': ['questions', 'hashtags', 'mentions', 'visuals']
            },
            'linkedin': {
                'optimal_length': 1500,
                'hashtag_range': (3, 7),
                'best_times': [8, 12, 17],
                'engagement_factors': ['professional_insights', 'industry_expertise', 'networking']
            },
            'facebook': {
                'optimal_length': 200,
                'hashtag_range': (1, 5),
                'best_times': [12, 15, 18],
                'engagement_factors': ['visual_content', 'community_building', 'emotional_connection']
            },
            'instagram': {
                'optimal_length': 150,
                'hashtag_range': (5, 15),
                'best_times': [11, 13, 17, 19],
                'engagement_factors': ['visual_appeal', 'storytelling', 'trending_hashtags']
            }
        }
        
        logger.info("AI Content Performance Predictor initialized")
    
    async def predict_content_performance(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict content performance using AI analysis.
        
        Args:
            content_data: Dictionary containing content and metadata
            
        Returns:
            AI-powered performance prediction with insights
        """
        try:
            st.info("🧠 AI is analyzing your content...")
            
            # Extract content details
            content = content_data.get('content', '')
            platform = content_data.get('platform', 'twitter')
            hashtags = content_data.get('hashtags', [])
            posting_time = content_data.get('posting_time', datetime.now())
            
            # Get current trends for context
            trending_context = await self._get_trending_context(platform)
            
            # Create comprehensive AI prompt for prediction
            prediction_prompt = self._create_prediction_prompt(
                content, platform, hashtags, posting_time, trending_context
            )
            
            # Get AI prediction
            ai_response = llm_text_gen(
                prediction_prompt,
                system_prompt="You are an expert social media analyst with deep knowledge of content performance patterns across all platforms. Provide specific, actionable predictions."
            )
            
            # Parse AI response into structured prediction
            structured_prediction = self._parse_ai_prediction(ai_response, content_data)
            
            # Add platform-specific insights
            platform_insights = self._get_platform_insights(content_data, platform)
            
            # Generate actionable recommendations
            recommendations = await self._generate_ai_recommendations(content_data, structured_prediction)
            
            return {
                'success': True,
                'content_analyzed': content[:100] + "..." if len(content) > 100 else content,
                'platform': platform,
                'ai_prediction': structured_prediction,
                'platform_insights': platform_insights,
                'recommendations': recommendations,
                'trending_context': trending_context,
                'analysis_timestamp': datetime.now().isoformat(),
                'confidence_level': self._calculate_confidence_level(content_data)
            }
            
        except Exception as e:
            error_msg = f"Error in AI prediction: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'error': error_msg}
    
    def _create_prediction_prompt(
        self, 
        content: str, 
        platform: str, 
        hashtags: List[str], 
        posting_time: datetime,
        trending_context: Dict[str, Any]
    ) -> str:
        """Create a comprehensive prompt for AI prediction."""
        
        config = self.platform_configs.get(platform, {})
        
        prompt = f"""
        Analyze this {platform} content and predict its performance:

        CONTENT TO ANALYZE:
        "{content}"

        METADATA:
        - Platform: {platform}
        - Hashtags: {hashtags}
        - Posting Time: {posting_time.strftime('%A %I:%M %p')}
        - Content Length: {len(content)} characters
        - Word Count: {len(content.split())} words

        PLATFORM CONTEXT:
        - Optimal Length: {config.get('optimal_length', 'N/A')} characters
        - Recommended Hashtags: {config.get('hashtag_range', 'N/A')}
        - Best Posting Times: {config.get('best_times', 'N/A')}

        CURRENT TRENDS:
        {json.dumps(trending_context, indent=2)}

        PREDICTION REQUIREMENTS:
        Please provide a detailed analysis with these specific predictions:

        1. ENGAGEMENT PREDICTION:
           - Estimated engagement rate (0-10%)
           - Estimated likes (number)
           - Estimated shares/retweets (number)
           - Estimated comments (number)

        2. PERFORMANCE ANALYSIS:
           - Strengths of this content
           - Weaknesses to address
           - Viral potential (Low/Medium/High)
           - Audience appeal rating (1-10)

        3. OPTIMIZATION OPPORTUNITIES:
           - How to improve engagement potential
           - Better hashtag suggestions
           - Content format improvements
           - Timing optimization

        4. COMPETITIVE ASSESSMENT:
           - How this compares to typical content in this niche
           - Unique elements that stand out
           - Missing elements competitors usually include

        Format your response as a detailed analysis with specific numbers and actionable insights.
        Be realistic but optimistic in your predictions.
        """
        
        return prompt
    
    async def _get_trending_context(self, platform: str) -> Dict[str, Any]:
        """Get current trending context for better predictions."""
        try:
            # Use existing Twitter integration if available
            if platform == 'twitter' and hasattr(self.twitter_service, 'get_trending_topics'):
                trending_topics = self.twitter_service.get_trending_topics()
            else:
                # Fallback to general trends
                trending_topics = [
                    'AI and technology',
                    'Content creation',
                    'Social media marketing',
                    'Digital transformation',
                    'Remote work'
                ]
            
            return {
                'trending_topics': trending_topics[:5],
                'platform': platform,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting trending context: {str(e)}")
            return {
                'trending_topics': ['General content', 'Engagement tips'],
                'platform': platform,
                'analysis_date': datetime.now().isoformat()
            }
    
    def _parse_ai_prediction(self, ai_response: str, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response into structured prediction data."""
        try:
            # Extract numerical predictions using simple parsing
            # This is a simplified version - in production, you might want more sophisticated parsing
            
            prediction = {
                'engagement_rate': self._extract_percentage(ai_response, 'engagement rate'),
                'estimated_likes': self._extract_number(ai_response, 'likes'),
                'estimated_shares': self._extract_number(ai_response, ['shares', 'retweets']),
                'estimated_comments': self._extract_number(ai_response, 'comments'),
                'viral_potential': self._extract_rating(ai_response, 'viral potential'),
                'audience_appeal': self._extract_rating(ai_response, 'audience appeal'),
                'strengths': self._extract_list_items(ai_response, 'strengths'),
                'weaknesses': self._extract_list_items(ai_response, 'weaknesses'),
                'full_analysis': ai_response
            }
            
            return prediction
            
        except Exception as e:
            logger.error(f"Error parsing AI prediction: {str(e)}")
            return {
                'engagement_rate': 2.5,  # Default reasonable prediction
                'estimated_likes': 50,
                'estimated_shares': 10,
                'estimated_comments': 5,
                'viral_potential': 'Medium',
                'audience_appeal': 7,
                'full_analysis': ai_response
            }
    
    def _get_platform_insights(self, content_data: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """Get platform-specific insights."""
        config = self.platform_configs.get(platform, {})
        content = content_data.get('content', '')
        hashtags = content_data.get('hashtags', [])
        
        insights = {
            'platform_optimization': [],
            'timing_analysis': {},
            'format_analysis': {},
            'hashtag_analysis': {}
        }
        
        # Length analysis
        optimal_length = config.get('optimal_length', 200)
        current_length = len(content)
        
        if abs(current_length - optimal_length) > 50:
            insights['platform_optimization'].append(
                f"Content length ({current_length}) differs from optimal ({optimal_length}) for {platform}"
            )
        else:
            insights['platform_optimization'].append(
                f"Content length is well-optimized for {platform}"
            )
        
        # Hashtag analysis
        hashtag_range = config.get('hashtag_range', (1, 5))
        hashtag_count = len(hashtags)
        
        if hashtag_count < hashtag_range[0]:
            insights['hashtag_analysis']['recommendation'] = f"Add more hashtags (optimal: {hashtag_range[0]}-{hashtag_range[1]})"
        elif hashtag_count > hashtag_range[1]:
            insights['hashtag_analysis']['recommendation'] = f"Consider reducing hashtags (optimal: {hashtag_range[0]}-{hashtag_range[1]})"
        else:
            insights['hashtag_analysis']['recommendation'] = "Hashtag count is optimal"
        
        # Timing analysis
        best_times = config.get('best_times', [])
        current_hour = datetime.now().hour
        
        insights['timing_analysis'] = {
            'best_times': best_times,
            'current_timing': 'Optimal' if current_hour in best_times else 'Suboptimal',
            'suggestion': f"Consider posting at {best_times} for better engagement" if current_hour not in best_times else "Current timing is optimal"
        }
        
        return insights
    
    async def _generate_ai_recommendations(
        self, 
        content_data: Dict[str, Any], 
        prediction: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate AI-powered recommendations for improvement."""
        
        recommendations_prompt = f"""
        Based on this content analysis, provide specific improvement recommendations:

        CONTENT: "{content_data.get('content', '')[:200]}..."
        PLATFORM: {content_data.get('platform', 'twitter')}
        PREDICTED ENGAGEMENT: {prediction.get('engagement_rate', 'N/A')}%
        VIRAL POTENTIAL: {prediction.get('viral_potential', 'N/A')}

        Provide 5-7 specific, actionable recommendations to improve this content's performance:

        1. Content optimization suggestions
        2. Hashtag improvements
        3. Timing recommendations
        4. Format enhancements
        5. Engagement boosters
        6. Audience targeting tips
        7. Platform-specific optimizations

        Format each recommendation as:
        - Category: [category]
        - Action: [specific action to take]
        - Expected Impact: [what improvement to expect]
        - Priority: [High/Medium/Low]

        Focus on quick wins and high-impact changes.
        """
        
        try:
            ai_recommendations = llm_text_gen(
                recommendations_prompt,
                system_prompt="You are a content optimization expert. Provide specific, actionable recommendations that can be implemented immediately."
            )
            
            # Parse recommendations into structured format
            return self._parse_recommendations(ai_recommendations)
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {str(e)}")
            return [
                {
                    'category': 'Content Enhancement',
                    'action': 'Add more engaging elements like questions or calls-to-action',
                    'expected_impact': 'Increase engagement by 20-30%',
                    'priority': 'High'
                },
                {
                    'category': 'Hashtag Optimization',
                    'action': 'Research and add 2-3 trending relevant hashtags',
                    'expected_impact': 'Improve discoverability',
                    'priority': 'Medium'
                }
            ]
    
    def _extract_percentage(self, text: str, keyword: str) -> float:
        """Extract percentage value from AI response."""
        import re
        patterns = [
            rf'{keyword}.*?(\d+\.?\d*)%',
            rf'(\d+\.?\d*)%.*?{keyword}',
            rf'{keyword}.*?(\d+\.?\d*) percent'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return 2.5  # Default reasonable engagement rate
    
    def _extract_number(self, text: str, keywords: List[str]) -> int:
        """Extract number from AI response."""
        import re
        
        if isinstance(keywords, str):
            keywords = [keywords]
        
        for keyword in keywords:
            patterns = [
                rf'{keyword}.*?(\d+)',
                rf'(\d+).*?{keyword}'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
        
        return 25  # Default reasonable number
    
    def _extract_rating(self, text: str, keyword: str) -> str:
        """Extract rating (High/Medium/Low) from AI response."""
        import re
        
        pattern = rf'{keyword}.*?(High|Medium|Low)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1).capitalize()
        
        return 'Medium'  # Default
    
    def _extract_list_items(self, text: str, section: str) -> List[str]:
        """Extract list items from a section of AI response."""
        import re
        
        # Find the section
        section_pattern = rf'{section}:?\s*(.*?)(?=\n\n|\d\.|[A-Z]+:|$)'
        match = re.search(section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            section_text = match.group(1)
            # Extract bullet points or numbered items
            items = re.findall(r'[-•]\s*(.+)', section_text)
            if not items:
                items = re.findall(r'\d+\.\s*(.+)', section_text)
            
            return [item.strip() for item in items[:3]]  # Return first 3 items
        
        return []
    
    def _parse_recommendations(self, ai_recommendations: str) -> List[Dict[str, str]]:
        """Parse AI recommendations into structured format."""
        recommendations = []
        
        try:
            # Simple parsing - split by numbers or bullet points
            import re
            sections = re.split(r'\d+\.|[-•]', ai_recommendations)
            
            for section in sections[1:6]:  # Take first 5 recommendations
                if len(section.strip()) > 10:  # Only substantial recommendations
                    recommendations.append({
                        'category': 'AI Recommendation',
                        'action': section.strip()[:200],  # Limit length
                        'expected_impact': 'Improved engagement',
                        'priority': 'Medium'
                    })
            
        except Exception as e:
            logger.error(f"Error parsing recommendations: {str(e)}")
        
        # Ensure we have at least a few recommendations
        if len(recommendations) < 3:
            recommendations.extend([
                {
                    'category': 'Engagement',
                    'action': 'Add questions to encourage audience interaction',
                    'expected_impact': '20-30% more engagement',
                    'priority': 'High'
                },
                {
                    'category': 'Visibility',
                    'action': 'Use trending hashtags relevant to your niche',
                    'expected_impact': 'Better discoverability',
                    'priority': 'Medium'
                },
                {
                    'category': 'Timing',
                    'action': 'Post during peak engagement hours for your audience',
                    'expected_impact': '15-25% more reach',
                    'priority': 'Medium'
                }
            ])
        
        return recommendations[:7]  # Return max 7 recommendations
    
    def _calculate_confidence_level(self, content_data: Dict[str, Any]) -> str:
        """Calculate confidence level of prediction."""
        confidence_factors = 0
        
        # More complete data = higher confidence
        if content_data.get('content'):
            confidence_factors += 1
        if content_data.get('hashtags'):
            confidence_factors += 1
        if content_data.get('platform'):
            confidence_factors += 1
        if content_data.get('posting_time'):
            confidence_factors += 1
        
        if confidence_factors >= 4:
            return 'High'
        elif confidence_factors >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    async def analyze_content_batch(self, content_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple pieces of content."""
        results = []
        
        for i, content_data in enumerate(content_list):
            st.write(f"🔍 Analyzing content {i+1}/{len(content_list)}")
            result = await self.predict_content_performance(content_data)
            results.append(result)
        
        return results
    
    def get_platform_best_practices(self, platform: str) -> Dict[str, Any]:
        """Get best practices for a specific platform."""
        config = self.platform_configs.get(platform, {})
        
        return {
            'platform': platform,
            'optimal_length': config.get('optimal_length'),
            'hashtag_range': config.get('hashtag_range'),
            'best_posting_times': config.get('best_times'),
            'engagement_factors': config.get('engagement_factors', []),
            'tips': [
                f"Keep content around {config.get('optimal_length', 200)} characters",
                f"Use {config.get('hashtag_range', (1, 5))[0]}-{config.get('hashtag_range', (1, 5))[1]} relevant hashtags",
                f"Post during peak hours: {config.get('best_times', [])}",
                "Include engaging elements like questions or calls-to-action",
                "Use visuals when possible to increase engagement"
            ]
        }


# Usage example and Streamlit interface
def render_ai_predictor_ui():
    """Render the AI content performance predictor interface."""
    st.title("🎯 AI Content Performance Predictor")
    st.markdown("Get AI-powered predictions for your content performance - no ML training required!")
    
    # Initialize predictor
    if 'ai_predictor' not in st.session_state:
        st.session_state.ai_predictor = AIContentPerformancePredictor()
    
    predictor = st.session_state.ai_predictor
    
    # Input section
    st.header("📝 Content Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["twitter", "linkedin", "facebook", "instagram"],
            help="Choose your target platform"
        )
        
        posting_time = st.time_input("Posting Time", value=datetime.now().time())
    
    with col2:
        hashtags_input = st.text_input(
            "Hashtags (comma-separated)",
            value="AI, ContentCreation, Marketing",
            help="Enter hashtags without # symbol"
        )
    
    content = st.text_area(
        "Content to Analyze",
        value="Discover how AI is revolutionizing content creation! What's your experience with AI tools? Share your thoughts below! 🚀",
        height=150,
        help="Enter the content you want to analyze"
    )
    
    # Process hashtags
    hashtags = [tag.strip() for tag in hashtags_input.split(',') if tag.strip()]
    
    if st.button("🧠 Analyze Content Performance", type="primary"):
        if content:
            # Prepare content data
            content_data = {
                'content': content,
                'platform': platform,
                'hashtags': hashtags,
                'posting_time': datetime.combine(datetime.now().date(), posting_time)
            }
            
            # Run AI analysis
            with st.spinner("🤖 AI is analyzing your content..."):
                results = asyncio.run(predictor.predict_content_performance(content_data))
            
            if results.get('success'):
                st.success("✅ Analysis Complete!")
                
                # Display predictions
                st.header("📊 AI Performance Prediction")
                
                prediction = results.get('ai_prediction', {})
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Engagement Rate", 
                        f"{prediction.get('engagement_rate', 0):.1f}%"
                    )
                
                with col2:
                    st.metric(
                        "Est. Likes", 
                        f"{prediction.get('estimated_likes', 0):,}"
                    )
                
                with col3:
                    st.metric(
                        "Est. Shares", 
                        f"{prediction.get('estimated_shares', 0):,}"
                    )
                
                with col4:
                    st.metric(
                        "Viral Potential", 
                        prediction.get('viral_potential', 'Medium')
                    )
                
                # Platform insights
                platform_insights = results.get('platform_insights', {})
                if platform_insights:
                    st.subheader("🎯 Platform Optimization")
                    
                    for insight in platform_insights.get('platform_optimization', []):
                        st.info(f"💡 {insight}")
                    
                    # Timing analysis
                    timing = platform_insights.get('timing_analysis', {})
                    if timing:
                        st.write(f"**Timing Analysis:** {timing.get('suggestion', 'N/A')}")
                    
                    # Hashtag analysis
                    hashtag_analysis = platform_insights.get('hashtag_analysis', {})
                    if hashtag_analysis:
                        st.write(f"**Hashtag Recommendation:** {hashtag_analysis.get('recommendation', 'N/A')}")
                
                # AI Recommendations
                recommendations = results.get('recommendations', [])
                if recommendations:
                    st.subheader("🚀 AI Recommendations")
                    
                    for i, rec in enumerate(recommendations):
                        with st.expander(f"💡 {rec.get('category', 'Recommendation')} - {rec.get('priority', 'Medium')} Priority"):
                            st.write(f"**Action:** {rec.get('action', 'N/A')}")
                            st.write(f"**Expected Impact:** {rec.get('expected_impact', 'N/A')}")
                
                # Full AI Analysis
                if prediction.get('full_analysis'):
                    with st.expander("🤖 Complete AI Analysis"):
                        st.write(prediction['full_analysis'])
                
            else:
                st.error(f"❌ Analysis failed: {results.get('error')}")
        else:
            st.warning("⚠️ Please enter content to analyze")
    
    # Platform best practices
    st.sidebar.header("📚 Platform Best Practices")
    selected_platform = st.sidebar.selectbox("Get tips for:", ["twitter", "linkedin", "facebook", "instagram"])
    
    best_practices = predictor.get_platform_best_practices(selected_platform)
    
    st.sidebar.write(f"**{selected_platform.title()} Best Practices:**")
    for tip in best_practices.get('tips', []):
        st.sidebar.write(f"• {tip}")


# Main execution
if __name__ == "__main__":
    render_ai_predictor_ui() 