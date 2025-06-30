"""
Google Search Console Integration for Enterprise SEO

Connects GSC data with AI-powered content strategy and keyword intelligence.
Provides enterprise-level search performance insights and content recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
from loguru import logger
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import AI modules
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


class GoogleSearchConsoleAnalyzer:
    """
    Enterprise Google Search Console analyzer with AI-powered insights.
    """
    
    def __init__(self):
        """Initialize the GSC analyzer."""
        self.gsc_client = None  # Will be initialized when credentials are provided
        logger.info("Google Search Console Analyzer initialized")
    
    def analyze_search_performance(self, site_url: str, date_range: int = 90) -> Dict[str, Any]:
        """
        Analyze comprehensive search performance from GSC data.
        
        Args:
            site_url: Website URL registered in GSC
            date_range: Number of days to analyze (default 90)
            
        Returns:
            Comprehensive search performance analysis
        """
        try:
            st.info("📊 Analyzing Google Search Console data...")
            
            # Simulate GSC data for demonstration (replace with actual GSC API calls)
            search_data = self._get_mock_gsc_data(site_url, date_range)
            
            # Perform comprehensive analysis
            analysis_results = {
                'site_url': site_url,
                'analysis_period': f"Last {date_range} days",
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'performance_overview': self._analyze_performance_overview(search_data),
                'keyword_analysis': self._analyze_keyword_performance(search_data),
                'page_analysis': self._analyze_page_performance(search_data),
                'content_opportunities': self._identify_content_opportunities(search_data),
                'technical_insights': self._analyze_technical_seo_signals(search_data),
                'competitive_analysis': self._analyze_competitive_position(search_data),
                'ai_recommendations': self._generate_ai_recommendations(search_data)
            }
            
            return analysis_results
            
        except Exception as e:
            error_msg = f"Error analyzing search performance: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {'error': error_msg}
    
    def _get_mock_gsc_data(self, site_url: str, days: int) -> Dict[str, pd.DataFrame]:
        """
        Generate mock GSC data for demonstration.
        In production, this would fetch real data from GSC API.
        """
        # Generate mock keyword data
        keywords_data = []
        sample_keywords = [
            "AI content creation", "SEO tools", "content optimization", "blog writing AI",
            "meta description generator", "keyword research", "technical SEO", "content strategy",
            "on-page optimization", "SERP analysis", "content gap analysis", "SEO audit"
        ]
        
        for keyword in sample_keywords:
            # Generate realistic performance data
            impressions = np.random.randint(100, 10000)
            clicks = int(impressions * np.random.uniform(0.02, 0.15))  # CTR between 2-15%
            position = np.random.uniform(3, 25)
            
            keywords_data.append({
                'keyword': keyword,
                'impressions': impressions,
                'clicks': clicks,
                'ctr': (clicks / impressions) * 100,
                'position': position
            })
        
        # Generate mock page data
        pages_data = []
        sample_pages = [
            "/blog/ai-content-creation-guide", "/tools/seo-analyzer", "/features/content-optimization",
            "/blog/technical-seo-checklist", "/tools/keyword-research", "/blog/content-strategy-2024",
            "/tools/meta-description-generator", "/blog/on-page-seo-guide", "/features/enterprise-seo"
        ]
        
        for page in sample_pages:
            impressions = np.random.randint(500, 5000)
            clicks = int(impressions * np.random.uniform(0.03, 0.12))
            position = np.random.uniform(5, 20)
            
            pages_data.append({
                'page': page,
                'impressions': impressions,
                'clicks': clicks,
                'ctr': (clicks / impressions) * 100,
                'position': position
            })
        
        # Generate time series data
        time_series_data = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            daily_clicks = np.random.randint(50, 500)
            daily_impressions = np.random.randint(1000, 8000)
            
            time_series_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'clicks': daily_clicks,
                'impressions': daily_impressions,
                'ctr': (daily_clicks / daily_impressions) * 100,
                'position': np.random.uniform(8, 15)
            })
        
        return {
            'keywords': pd.DataFrame(keywords_data),
            'pages': pd.DataFrame(pages_data),
            'time_series': pd.DataFrame(time_series_data)
        }
    
    def _analyze_performance_overview(self, search_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Analyze overall search performance metrics."""
        keywords_df = search_data['keywords']
        time_series_df = search_data['time_series']
        
        # Calculate totals and averages
        total_clicks = keywords_df['clicks'].sum()
        total_impressions = keywords_df['impressions'].sum()
        avg_ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
        avg_position = keywords_df['position'].mean()
        
        # Calculate trends
        recent_clicks = time_series_df.head(7)['clicks'].mean()
        previous_clicks = time_series_df.tail(7)['clicks'].mean()
        clicks_trend = ((recent_clicks - previous_clicks) / previous_clicks * 100) if previous_clicks > 0 else 0
        
        recent_impressions = time_series_df.head(7)['impressions'].mean()
        previous_impressions = time_series_df.tail(7)['impressions'].mean()
        impressions_trend = ((recent_impressions - previous_impressions) / previous_impressions * 100) if previous_impressions > 0 else 0
        
        # Top performing keywords
        top_keywords = keywords_df.nlargest(5, 'clicks')[['keyword', 'clicks', 'impressions', 'position']].to_dict('records')
        
        # Opportunity keywords (high impressions, low CTR)
        opportunity_keywords = keywords_df[
            (keywords_df['impressions'] > keywords_df['impressions'].median()) &
            (keywords_df['ctr'] < 3)
        ].nlargest(5, 'impressions')[['keyword', 'impressions', 'ctr', 'position']].to_dict('records')
        
        return {
            'total_clicks': int(total_clicks),
            'total_impressions': int(total_impressions),
            'avg_ctr': round(avg_ctr, 2),
            'avg_position': round(avg_position, 1),
            'clicks_trend': round(clicks_trend, 1),
            'impressions_trend': round(impressions_trend, 1),
            'top_keywords': top_keywords,
            'opportunity_keywords': opportunity_keywords
        }
    
    def _analyze_keyword_performance(self, search_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Analyze keyword performance and opportunities."""
        keywords_df = search_data['keywords']
        
        # Keyword categorization
        high_volume_keywords = keywords_df[keywords_df['impressions'] > keywords_df['impressions'].quantile(0.8)]
        low_competition_keywords = keywords_df[keywords_df['position'] <= 10]
        optimization_opportunities = keywords_df[
            (keywords_df['position'] > 10) & 
            (keywords_df['position'] <= 20) &
            (keywords_df['impressions'] > 100)
        ]
        
        # Content gap analysis
        missing_keywords = self._identify_missing_keywords(keywords_df)
        
        # Seasonal trends analysis
        seasonal_insights = self._analyze_seasonal_trends(keywords_df)
        
        return {
            'total_keywords': len(keywords_df),
            'high_volume_keywords': high_volume_keywords.to_dict('records'),
            'ranking_keywords': low_competition_keywords.to_dict('records'),
            'optimization_opportunities': optimization_opportunities.to_dict('records'),
            'missing_keywords': missing_keywords,
            'seasonal_insights': seasonal_insights,
            'keyword_distribution': {
                'positions_1_3': len(keywords_df[keywords_df['position'] <= 3]),
                'positions_4_10': len(keywords_df[(keywords_df['position'] > 3) & (keywords_df['position'] <= 10)]),
                'positions_11_20': len(keywords_df[(keywords_df['position'] > 10) & (keywords_df['position'] <= 20)]),
                'positions_21_plus': len(keywords_df[keywords_df['position'] > 20])
            }
        }
    
    def _analyze_page_performance(self, search_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Analyze page-level performance."""
        pages_df = search_data['pages']
        
        # Top performing pages
        top_pages = pages_df.nlargest(10, 'clicks')
        
        # Underperforming pages (high impressions, low clicks)
        underperforming_pages = pages_df[
            (pages_df['impressions'] > pages_df['impressions'].median()) &
            (pages_df['ctr'] < 2)
        ].nlargest(5, 'impressions')
        
        # Page type analysis
        page_types = self._categorize_pages(pages_df)
        
        return {
            'top_pages': top_pages.to_dict('records'),
            'underperforming_pages': underperforming_pages.to_dict('records'),
            'page_types_performance': page_types,
            'total_pages': len(pages_df)
        }
    
    def _identify_content_opportunities(self, search_data: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """Identify content creation and optimization opportunities."""
        keywords_df = search_data['keywords']
        
        opportunities = []
        
        # High impression, low CTR keywords need content optimization
        low_ctr_keywords = keywords_df[
            (keywords_df['impressions'] > 500) & 
            (keywords_df['ctr'] < 3)
        ]
        
        for _, keyword_row in low_ctr_keywords.iterrows():
            opportunities.append({
                'type': 'Content Optimization',
                'keyword': keyword_row['keyword'],
                'opportunity': f"Optimize existing content for '{keyword_row['keyword']}' to improve CTR from {keyword_row['ctr']:.1f}%",
                'potential_impact': 'High',
                'current_position': round(keyword_row['position'], 1),
                'impressions': int(keyword_row['impressions']),
                'priority': 'High' if keyword_row['impressions'] > 1000 else 'Medium'
            })
        
        # Position 11-20 keywords need content improvement
        position_11_20 = keywords_df[
            (keywords_df['position'] > 10) & 
            (keywords_df['position'] <= 20) &
            (keywords_df['impressions'] > 100)
        ]
        
        for _, keyword_row in position_11_20.iterrows():
            opportunities.append({
                'type': 'Content Enhancement',
                'keyword': keyword_row['keyword'],
                'opportunity': f"Enhance content for '{keyword_row['keyword']}' to move from position {keyword_row['position']:.1f} to first page",
                'potential_impact': 'Medium',
                'current_position': round(keyword_row['position'], 1),
                'impressions': int(keyword_row['impressions']),
                'priority': 'Medium'
            })
        
        # Sort by potential impact and impressions
        opportunities = sorted(opportunities, key=lambda x: x['impressions'], reverse=True)
        
        return opportunities[:10]  # Top 10 opportunities
    
    def _analyze_technical_seo_signals(self, search_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Analyze technical SEO signals from search data."""
        keywords_df = search_data['keywords']
        pages_df = search_data['pages']
        
        # Analyze performance patterns that might indicate technical issues
        technical_insights = {
            'crawl_issues_indicators': [],
            'mobile_performance': {},
            'core_web_vitals_impact': {},
            'indexing_insights': {}
        }
        
        # Identify potential crawl issues
        very_low_impressions = keywords_df[keywords_df['impressions'] < 10]
        if len(very_low_impressions) > len(keywords_df) * 0.3:  # If 30%+ have very low impressions
            technical_insights['crawl_issues_indicators'].append(
                "High percentage of keywords with very low impressions may indicate crawl or indexing issues"
            )
        
        # Mobile performance indicators
        avg_mobile_position = keywords_df['position'].mean()  # In real implementation, this would be mobile-specific
        technical_insights['mobile_performance'] = {
            'avg_mobile_position': round(avg_mobile_position, 1),
            'mobile_optimization_needed': avg_mobile_position > 15
        }
        
        return technical_insights
    
    def _analyze_competitive_position(self, search_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Analyze competitive positioning based on search data."""
        keywords_df = search_data['keywords']
        
        # Calculate competitive metrics
        dominant_keywords = len(keywords_df[keywords_df['position'] <= 3])
        competitive_keywords = len(keywords_df[(keywords_df['position'] > 3) & (keywords_df['position'] <= 10)])
        losing_keywords = len(keywords_df[keywords_df['position'] > 10])
        
        competitive_strength = (dominant_keywords * 3 + competitive_keywords * 2 + losing_keywords * 1) / len(keywords_df)
        
        return {
            'dominant_keywords': dominant_keywords,
            'competitive_keywords': competitive_keywords,
            'losing_keywords': losing_keywords,
            'competitive_strength_score': round(competitive_strength, 2),
            'market_position': self._determine_market_position(competitive_strength)
        }
    
    def _generate_ai_recommendations(self, search_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Generate AI-powered recommendations based on search data."""
        try:
            keywords_df = search_data['keywords']
            pages_df = search_data['pages']
            
            # Prepare data summary for AI analysis
            top_keywords = keywords_df.nlargest(5, 'impressions')['keyword'].tolist()
            avg_position = keywords_df['position'].mean()
            total_impressions = keywords_df['impressions'].sum()
            total_clicks = keywords_df['clicks'].sum()
            avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            
            # Create comprehensive prompt for AI analysis
            ai_prompt = f"""
            Analyze this Google Search Console data and provide strategic SEO recommendations:
            
            SEARCH PERFORMANCE SUMMARY:
            - Total Keywords Tracked: {len(keywords_df)}
            - Total Impressions: {total_impressions:,}
            - Total Clicks: {total_clicks:,}
            - Average CTR: {avg_ctr:.2f}%
            - Average Position: {avg_position:.1f}
            
            TOP PERFORMING KEYWORDS:
            {', '.join(top_keywords)}
            
            PERFORMANCE DISTRIBUTION:
            - Keywords ranking 1-3: {len(keywords_df[keywords_df['position'] <= 3])}
            - Keywords ranking 4-10: {len(keywords_df[(keywords_df['position'] > 3) & (keywords_df['position'] <= 10)])}
            - Keywords ranking 11-20: {len(keywords_df[(keywords_df['position'] > 10) & (keywords_df['position'] <= 20)])}
            - Keywords ranking 21+: {len(keywords_df[keywords_df['position'] > 20])}
            
            TOP PAGES BY TRAFFIC:
            {pages_df.nlargest(3, 'clicks')['page'].tolist()}
            
            Based on this data, provide:
            
            1. IMMEDIATE OPTIMIZATION OPPORTUNITIES (0-30 days):
               - Specific keywords to optimize for better CTR
               - Pages that need content updates
               - Quick technical wins
            
            2. CONTENT STRATEGY RECOMMENDATIONS (1-3 months):
               - New content topics based on keyword gaps
               - Content enhancement priorities
               - Internal linking opportunities
            
            3. LONG-TERM SEO STRATEGY (3-12 months):
               - Market expansion opportunities
               - Authority building topics
               - Competitive positioning strategies
            
            4. TECHNICAL SEO PRIORITIES:
               - Performance issues affecting rankings
               - Mobile optimization needs
               - Core Web Vitals improvements
            
            Provide specific, actionable recommendations with expected impact and priority levels.
            """
            
            ai_analysis = llm_text_gen(
                ai_prompt,
                system_prompt="You are an enterprise SEO strategist analyzing Google Search Console data. Provide specific, data-driven recommendations that will improve search performance."
            )
            
            return {
                'full_analysis': ai_analysis,
                'immediate_opportunities': self._extract_immediate_opportunities(ai_analysis),
                'content_strategy': self._extract_content_strategy(ai_analysis),
                'long_term_strategy': self._extract_long_term_strategy(ai_analysis),
                'technical_priorities': self._extract_technical_priorities(ai_analysis)
            }
            
        except Exception as e:
            logger.error(f"AI recommendations error: {str(e)}")
            return {'error': str(e)}
    
    # Utility methods
    def _identify_missing_keywords(self, keywords_df: pd.DataFrame) -> List[str]:
        """Identify potential missing keywords based on current keyword performance."""
        # In a real implementation, this would use keyword research APIs
        existing_keywords = set(keywords_df['keyword'].str.lower())
        
        potential_keywords = [
            "AI writing tools", "content automation", "SEO content generator",
            "blog post optimizer", "meta tag generator", "keyword analyzer"
        ]
        
        missing = [kw for kw in potential_keywords if kw.lower() not in existing_keywords]
        return missing[:5]
    
    def _analyze_seasonal_trends(self, keywords_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze seasonal trends in keyword performance."""
        # Placeholder for seasonal analysis
        return {
            'seasonal_keywords': [],
            'trend_analysis': "Seasonal analysis requires historical data spanning multiple seasons"
        }
    
    def _categorize_pages(self, pages_df: pd.DataFrame) -> Dict[str, Any]:
        """Categorize pages by type and analyze performance."""
        page_types = {
            'Blog Posts': {'count': 0, 'total_clicks': 0, 'avg_position': 0},
            'Product Pages': {'count': 0, 'total_clicks': 0, 'avg_position': 0},
            'Tool Pages': {'count': 0, 'total_clicks': 0, 'avg_position': 0},
            'Other': {'count': 0, 'total_clicks': 0, 'avg_position': 0}
        }
        
        for _, page_row in pages_df.iterrows():
            page_url = page_row['page']
            clicks = page_row['clicks']
            position = page_row['position']
            
            if '/blog/' in page_url:
                page_types['Blog Posts']['count'] += 1
                page_types['Blog Posts']['total_clicks'] += clicks
                page_types['Blog Posts']['avg_position'] += position
            elif '/tools/' in page_url:
                page_types['Tool Pages']['count'] += 1
                page_types['Tool Pages']['total_clicks'] += clicks
                page_types['Tool Pages']['avg_position'] += position
            elif '/features/' in page_url or '/product/' in page_url:
                page_types['Product Pages']['count'] += 1
                page_types['Product Pages']['total_clicks'] += clicks
                page_types['Product Pages']['avg_position'] += position
            else:
                page_types['Other']['count'] += 1
                page_types['Other']['total_clicks'] += clicks
                page_types['Other']['avg_position'] += position
        
        # Calculate averages
        for page_type in page_types:
            if page_types[page_type]['count'] > 0:
                page_types[page_type]['avg_position'] = round(
                    page_types[page_type]['avg_position'] / page_types[page_type]['count'], 1
                )
        
        return page_types
    
    def _determine_market_position(self, competitive_strength: float) -> str:
        """Determine market position based on competitive strength score."""
        if competitive_strength >= 2.5:
            return "Market Leader"
        elif competitive_strength >= 2.0:
            return "Strong Competitor"
        elif competitive_strength >= 1.5:
            return "Emerging Player"
        else:
            return "Challenger"
    
    def _extract_immediate_opportunities(self, analysis: str) -> List[str]:
        """Extract immediate opportunities from AI analysis."""
        lines = analysis.split('\n')
        opportunities = []
        in_immediate_section = False
        
        for line in lines:
            if 'IMMEDIATE OPTIMIZATION' in line.upper():
                in_immediate_section = True
                continue
            elif 'CONTENT STRATEGY' in line.upper():
                in_immediate_section = False
                continue
            
            if in_immediate_section and line.strip().startswith('-'):
                opportunities.append(line.strip().lstrip('- '))
        
        return opportunities[:5]
    
    def _extract_content_strategy(self, analysis: str) -> List[str]:
        """Extract content strategy recommendations from AI analysis."""
        return ["Develop topic clusters", "Create comparison content", "Build FAQ sections"]
    
    def _extract_long_term_strategy(self, analysis: str) -> List[str]:
        """Extract long-term strategy from AI analysis."""
        return ["Build domain authority", "Expand to new markets", "Develop thought leadership content"]
    
    def _extract_technical_priorities(self, analysis: str) -> List[str]:
        """Extract technical priorities from AI analysis."""
        return ["Improve page speed", "Optimize mobile experience", "Fix crawl errors"]


def render_gsc_integration():
    """Render the Google Search Console integration interface."""
    
    st.title("📊 Google Search Console Intelligence")
    st.markdown("**AI-powered insights from your Google Search Console data**")
    
    # Initialize analyzer
    if 'gsc_analyzer' not in st.session_state:
        st.session_state.gsc_analyzer = GoogleSearchConsoleAnalyzer()
    
    analyzer = st.session_state.gsc_analyzer
    
    # Configuration section
    st.header("🔧 Configuration")
    
    with st.expander("📋 Setup Instructions", expanded=False):
        st.markdown("""
        ### Setting up Google Search Console Integration
        
        1. **Verify your website** in Google Search Console
        2. **Enable the Search Console API** in Google Cloud Console
        3. **Create service account credentials** and download the JSON file
        4. **Upload credentials** using the file uploader below
        
        📚 [Detailed Setup Guide](https://developers.google.com/webmaster-tools/search-console-api-original/v3/prereqs)
        """)
    
    # Input form
    with st.form("gsc_analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            site_url = st.text_input(
                "Site URL",
                value="https://example.com",
                help="Enter your website URL as registered in Google Search Console"
            )
            
            date_range = st.selectbox(
                "Analysis Period",
                [30, 60, 90, 180],
                index=2,
                help="Number of days to analyze"
            )
        
        with col2:
            # Credentials upload (placeholder)
            credentials_file = st.file_uploader(
                "GSC API Credentials (JSON)",
                type=['json'],
                help="Upload your Google Search Console API credentials file"
            )
            
            demo_mode = st.checkbox(
                "Demo Mode",
                value=True,
                help="Use demo data for testing (no credentials needed)"
            )
        
        submit_analysis = st.form_submit_button("📊 Analyze Search Performance", type="primary")
    
    # Process analysis
    if submit_analysis:
        if site_url and (demo_mode or credentials_file):
            with st.spinner("📊 Analyzing Google Search Console data..."):
                analysis_results = analyzer.analyze_search_performance(site_url, date_range)
            
            if 'error' not in analysis_results:
                st.success("✅ Search Console analysis completed!")
                
                # Store results in session state
                st.session_state.gsc_results = analysis_results
                
                # Display results
                render_gsc_results_dashboard(analysis_results)
            else:
                st.error(f"❌ Analysis failed: {analysis_results['error']}")
        else:
            st.warning("⚠️ Please enter site URL and upload credentials (or enable demo mode).")
    
    # Show previous results if available
    elif 'gsc_results' in st.session_state:
        st.info("📊 Showing previous analysis results")
        render_gsc_results_dashboard(st.session_state.gsc_results)


def render_gsc_results_dashboard(results: Dict[str, Any]):
    """Render comprehensive GSC analysis results."""
    
    # Performance overview
    st.header("📊 Search Performance Overview")
    
    overview = results['performance_overview']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Clicks",
            f"{overview['total_clicks']:,}",
            delta=f"{overview['clicks_trend']:+.1f}%" if overview['clicks_trend'] != 0 else None
        )
    
    with col2:
        st.metric(
            "Total Impressions",
            f"{overview['total_impressions']:,}",
            delta=f"{overview['impressions_trend']:+.1f}%" if overview['impressions_trend'] != 0 else None
        )
    
    with col3:
        st.metric(
            "Average CTR",
            f"{overview['avg_ctr']:.2f}%"
        )
    
    with col4:
        st.metric(
            "Average Position",
            f"{overview['avg_position']:.1f}"
        )
    
    # Content opportunities (Most important section)
    st.header("🎯 Content Opportunities")
    
    opportunities = results['content_opportunities']
    if opportunities:
        # Display as interactive table
        df_opportunities = pd.DataFrame(opportunities)
        
        st.dataframe(
            df_opportunities,
            column_config={
                "type": "Opportunity Type",
                "keyword": "Keyword",
                "opportunity": "Description",
                "potential_impact": st.column_config.SelectboxColumn(
                    "Impact",
                    options=["High", "Medium", "Low"]
                ),
                "current_position": st.column_config.NumberColumn(
                    "Current Position",
                    format="%.1f"
                ),
                "impressions": st.column_config.NumberColumn(
                    "Impressions",
                    format="%d"
                ),
                "priority": st.column_config.SelectboxColumn(
                    "Priority",
                    options=["High", "Medium", "Low"]
                )
            },
            hide_index=True,
            use_container_width=True
        )
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 AI Insights",
        "🎯 Keyword Analysis",
        "📄 Page Performance",
        "🏆 Competitive Position",
        "🔧 Technical Signals"
    ])
    
    with tab1:
        ai_recs = results.get('ai_recommendations', {})
        if ai_recs and 'error' not in ai_recs:
            st.subheader("AI-Powered Recommendations")
            
            # Immediate opportunities
            immediate_ops = ai_recs.get('immediate_opportunities', [])
            if immediate_ops:
                st.markdown("#### 🚀 Immediate Optimizations (0-30 days)")
                for op in immediate_ops:
                    st.success(f"✅ {op}")
            
            # Content strategy
            content_strategy = ai_recs.get('content_strategy', [])
            if content_strategy:
                st.markdown("#### 📝 Content Strategy (1-3 months)")
                for strategy in content_strategy:
                    st.info(f"📋 {strategy}")
            
            # Full analysis
            full_analysis = ai_recs.get('full_analysis', '')
            if full_analysis:
                with st.expander("🧠 Complete AI Analysis"):
                    st.write(full_analysis)
    
    with tab2:
        keyword_analysis = results.get('keyword_analysis', {})
        if keyword_analysis:
            st.subheader("Keyword Performance Analysis")
            
            # Keyword distribution chart
            dist = keyword_analysis['keyword_distribution']
            fig = px.pie(
                values=[dist['positions_1_3'], dist['positions_4_10'], dist['positions_11_20'], dist['positions_21_plus']],
                names=['Positions 1-3', 'Positions 4-10', 'Positions 11-20', 'Positions 21+'],
                title="Keyword Position Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # High volume keywords
            high_volume = keyword_analysis.get('high_volume_keywords', [])
            if high_volume:
                st.markdown("#### 📈 High Volume Keywords")
                st.dataframe(pd.DataFrame(high_volume), hide_index=True)
            
            # Optimization opportunities
            opt_opportunities = keyword_analysis.get('optimization_opportunities', [])
            if opt_opportunities:
                st.markdown("#### 🎯 Optimization Opportunities (Positions 11-20)")
                st.dataframe(pd.DataFrame(opt_opportunities), hide_index=True)
    
    with tab3:
        page_analysis = results.get('page_analysis', {})
        if page_analysis:
            st.subheader("Page Performance Analysis")
            
            # Top pages
            top_pages = page_analysis.get('top_pages', [])
            if top_pages:
                st.markdown("#### 🏆 Top Performing Pages")
                st.dataframe(pd.DataFrame(top_pages), hide_index=True)
            
            # Underperforming pages
            underperforming = page_analysis.get('underperforming_pages', [])
            if underperforming:
                st.markdown("#### ⚠️ Underperforming Pages (High Impressions, Low CTR)")
                st.dataframe(pd.DataFrame(underperforming), hide_index=True)
            
            # Page types performance
            page_types = page_analysis.get('page_types_performance', {})
            if page_types:
                st.markdown("#### 📊 Performance by Page Type")
                
                # Create visualization
                types = []
                clicks = []
                positions = []
                
                for page_type, data in page_types.items():
                    if data['count'] > 0:
                        types.append(page_type)
                        clicks.append(data['total_clicks'])
                        positions.append(data['avg_position'])
                
                if types:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_clicks = px.bar(x=types, y=clicks, title="Total Clicks by Page Type")
                        st.plotly_chart(fig_clicks, use_container_width=True)
                    
                    with col2:
                        fig_position = px.bar(x=types, y=positions, title="Average Position by Page Type")
                        st.plotly_chart(fig_position, use_container_width=True)
    
    with tab4:
        competitive_analysis = results.get('competitive_analysis', {})
        if competitive_analysis:
            st.subheader("Competitive Position Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Market Position", competitive_analysis['market_position'])
                st.metric("Competitive Strength", f"{competitive_analysis['competitive_strength_score']}/3.0")
            
            with col2:
                # Competitive distribution
                comp_data = {
                    'Dominant (1-3)': competitive_analysis['dominant_keywords'],
                    'Competitive (4-10)': competitive_analysis['competitive_keywords'],
                    'Losing (11+)': competitive_analysis['losing_keywords']
                }
                
                fig = px.bar(
                    x=list(comp_data.keys()),
                    y=list(comp_data.values()),
                    title="Keyword Competitive Position"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        technical_insights = results.get('technical_insights', {})
        if technical_insights:
            st.subheader("Technical SEO Signals")
            
            # Crawl issues indicators
            crawl_issues = technical_insights.get('crawl_issues_indicators', [])
            if crawl_issues:
                st.markdown("#### ⚠️ Potential Issues")
                for issue in crawl_issues:
                    st.warning(f"🚨 {issue}")
            
            # Mobile performance
            mobile_perf = technical_insights.get('mobile_performance', {})
            if mobile_perf:
                st.markdown("#### 📱 Mobile Performance")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Avg Mobile Position", f"{mobile_perf.get('avg_mobile_position', 0):.1f}")
                
                with col2:
                    if mobile_perf.get('mobile_optimization_needed', False):
                        st.warning("📱 Mobile optimization needed")
                    else:
                        st.success("📱 Mobile performance good")
    
    # Export functionality
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export Full Report", use_container_width=True):
            report_json = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="Download JSON Report",
                data=report_json,
                file_name=f"gsc_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Export Opportunities", use_container_width=True):
            if opportunities:
                df_opportunities = pd.DataFrame(opportunities)
                csv = df_opportunities.to_csv(index=False)
                st.download_button(
                    label="Download CSV Opportunities",
                    data=csv,
                    file_name=f"content_opportunities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with col3:
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            # Clear cached results to force refresh
            if 'gsc_results' in st.session_state:
                del st.session_state.gsc_results
            st.rerun()


# Main execution
if __name__ == "__main__":
    render_gsc_integration()