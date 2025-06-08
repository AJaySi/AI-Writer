"""
Enhanced UI for Content Gap Analysis with Advertools Integration.

This module provides a comprehensive Streamlit interface for content gap analysis
using the EnhancedContentGapAnalyzer with advertools and AI insights.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List
import json
from datetime import datetime
import io
import base64

from .enhanced_analyzer import EnhancedContentGapAnalyzer
from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header

class EnhancedContentGapAnalysisUI:
    """Enhanced UI for content gap analysis."""
    
    def __init__(self):
        """Initialize the enhanced UI."""
        self.analyzer = EnhancedContentGapAnalyzer()
        
        # Apply dashboard styling
        apply_dashboard_style()
    
    def render(self):
        """Render the enhanced content gap analysis interface."""
        
        # Enhanced dashboard header
        render_dashboard_header(
            "🎯 Enhanced Content Gap Analysis",
            "Discover content opportunities with AI-powered insights using advertools, SERP analysis, competitor crawling, and strategic recommendations."
        )
        
        # Main content area
        with st.container():
            # Analysis input form
            self._render_analysis_form()
        
        # Session state for results
        if 'gap_analysis_results' in st.session_state and st.session_state.gap_analysis_results:
            st.markdown("---")
            self._render_results_dashboard(st.session_state.gap_analysis_results)
    
    def _render_analysis_form(self):
        """Render the analysis input form."""
        st.markdown("## 🚀 Setup Your Content Gap Analysis")
        
        with st.form("enhanced_gap_analysis_form"):
            # Target website input
            col1, col2 = st.columns([2, 1])
            
            with col1:
                target_url = st.text_input(
                    "🎯 Your Website URL",
                    placeholder="https://yourwebsite.com",
                    help="Enter your website URL to analyze"
                )
            
            with col2:
                industry = st.selectbox(
                    "🏭 Industry",
                    options=[
                        "general", "technology", "healthcare", "finance", 
                        "ecommerce", "education", "real estate", "travel",
                        "food", "fitness", "marketing", "consulting"
                    ],
                    help="Select your industry for better analysis context"
                )
            
            # Competitor URLs
            st.markdown("### 🏆 Competitor Analysis")
            competitor_urls_text = st.text_area(
                "Competitor URLs (one per line, max 5)",
                placeholder="https://competitor1.com\nhttps://competitor2.com\nhttps://competitor3.com",
                height=120,
                help="Enter up to 5 competitor URLs for comprehensive analysis"
            )
            
            # Target keywords
            st.markdown("### 🎯 Keyword Focus")
            target_keywords_text = st.text_input(
                "Primary Keywords (comma-separated)",
                placeholder="seo, content marketing, digital marketing",
                help="Enter your main keywords to analyze and expand"
            )
            
            # Analysis options
            st.markdown("### ⚙️ Analysis Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                enable_serp = st.checkbox(
                    "🔍 SERP Analysis",
                    value=True,
                    help="Analyze competitor positions in search results"
                )
            
            with col2:
                enable_crawling = st.checkbox(
                    "🕷️ Deep Crawling",
                    value=True,
                    help="Perform comprehensive competitor content crawling"
                )
            
            with col3:
                enable_ai_insights = st.checkbox(
                    "🤖 AI Insights",
                    value=True,
                    help="Generate AI-powered strategic recommendations"
                )
            
            # Submit button
            submitted = st.form_submit_button(
                "🚀 Start Enhanced Analysis",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                # Validate inputs
                if not target_url or not target_url.startswith(('http://', 'https://')):
                    st.error("❌ Please enter a valid target URL starting with http:// or https://")
                    return
                
                if not target_keywords_text.strip():
                    st.error("❌ Please enter at least one target keyword")
                    return
                
                # Process inputs
                competitor_urls = [
                    url.strip() for url in competitor_urls_text.split('\n') 
                    if url.strip() and url.strip().startswith(('http://', 'https://'))
                ]
                
                if not competitor_urls:
                    st.error("❌ Please enter at least one valid competitor URL")
                    return
                
                target_keywords = [
                    kw.strip() for kw in target_keywords_text.split(',') 
                    if kw.strip()
                ]
                
                # Run analysis
                self._run_enhanced_analysis(
                    target_url=target_url,
                    competitor_urls=competitor_urls,
                    target_keywords=target_keywords,
                    industry=industry,
                    options={
                        'enable_serp': enable_serp,
                        'enable_crawling': enable_crawling,
                        'enable_ai_insights': enable_ai_insights
                    }
                )
    
    def _run_enhanced_analysis(self, target_url: str, competitor_urls: List[str], 
                              target_keywords: List[str], industry: str, options: Dict[str, bool]):
        """Run the enhanced content gap analysis."""
        
        try:
            with st.spinner("🔄 Running Enhanced Content Gap Analysis..."):
                
                # Initialize progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                progress_bar.progress(10)
                status_text.text("🚀 Initializing analysis...")
                
                # Run comprehensive analysis
                results = self.analyzer.analyze_comprehensive_gap(
                    target_url=target_url,
                    competitor_urls=competitor_urls,
                    target_keywords=target_keywords,
                    industry=industry
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Store results in session state
                st.session_state.gap_analysis_results = results
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                if 'error' in results:
                    st.error(f"❌ Analysis failed: {results['error']}")
                else:
                    st.success("🎉 Enhanced Content Gap Analysis completed successfully!")
                    st.balloons()
                    
                    # Rerun to show results
                    st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error running analysis: {str(e)}")
    
    def _render_results_dashboard(self, results: Dict[str, Any]):
        """Render the comprehensive results dashboard."""
        
        if 'error' in results:
            st.error(f"❌ Analysis Error: {results['error']}")
            return
        
        # Results header
        st.markdown("## 📊 Enhanced Content Gap Analysis Results")
        
        # Key metrics overview
        self._render_metrics_overview(results)
        
        # Detailed analysis tabs
        self._render_detailed_analysis(results)
        
        # Export functionality
        self._render_export_options(results)
    
    def _render_metrics_overview(self, results: Dict[str, Any]):
        """Render key metrics overview."""
        
        st.markdown("### 📈 Analysis Overview")
        
        # Create metrics columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "🎯 Keywords Analyzed",
                len(results.get('target_keywords', [])),
                help="Number of primary keywords analyzed"
            )
        
        with col2:
            st.metric(
                "🏆 Competitors Crawled",
                len(results.get('competitor_urls', [])),
                help="Number of competitor websites analyzed"
            )
        
        with col3:
            expanded_keywords = results.get('keyword_expansion', {}).get('expanded_keywords', [])
            st.metric(
                "🔍 Keywords Discovered",
                len(expanded_keywords),
                help="Additional keywords discovered through expansion"
            )
        
        with col4:
            ranking_opportunities = results.get('serp_analysis', {}).get('ranking_opportunities', [])
            st.metric(
                "🚀 SERP Opportunities",
                len(ranking_opportunities),
                help="Keywords with ranking opportunities identified"
            )
        
        with col5:
            recommendations = results.get('recommendations', [])
            st.metric(
                "💡 AI Recommendations",
                len(recommendations),
                help="AI-generated strategic recommendations"
            )
        
        # Analysis timestamp
        if results.get('analysis_timestamp'):
            timestamp = datetime.fromisoformat(results['analysis_timestamp'].replace('Z', '+00:00'))
            st.caption(f"📅 Analysis completed: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    def _render_detailed_analysis(self, results: Dict[str, Any]):
        """Render detailed analysis in tabs."""
        
        # Create main analysis tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🔍 SERP Analysis",
            "🎯 Keyword Research", 
            "🕷️ Competitor Intelligence",
            "📊 Content Themes",
            "🤖 AI Strategic Insights",
            "📋 Action Plan"
        ])
        
        with tab1:
            self._render_serp_analysis(results.get('serp_analysis', {}))
        
        with tab2:
            self._render_keyword_research(results.get('keyword_expansion', {}))
        
        with tab3:
            self._render_competitor_intelligence(results.get('competitor_content', {}))
        
        with tab4:
            self._render_content_themes(results.get('content_themes', {}))
        
        with tab5:
            self._render_ai_insights(results.get('ai_insights', {}))
        
        with tab6:
            self._render_action_plan(results)
    
    def _render_serp_analysis(self, serp_data: Dict[str, Any]):
        """Render SERP analysis results."""
        
        st.markdown("### 🔍 Search Engine Results Analysis")
        
        if not serp_data:
            st.info("No SERP analysis data available")
            return
        
        # Competitor SERP presence
        if serp_data.get('competitor_presence'):
            st.markdown("#### 🏆 Competitor SERP Dominance")
            
            presence_data = serp_data['competitor_presence']
            presence_df = pd.DataFrame(
                list(presence_data.items()),
                columns=['Domain', 'Keywords Ranking']
            )
            
            # Display as chart
            st.bar_chart(presence_df.set_index('Domain'))
            
            # Top performers
            st.markdown("**🥇 Top Performing Competitors:**")
            for domain, count in list(presence_data.items())[:3]:
                st.write(f"• **{domain}**: Ranking for {count} keywords")
        
        # Ranking opportunities
        if serp_data.get('ranking_opportunities'):
            st.markdown("#### 🚀 Ranking Opportunities")
            
            opportunities = serp_data['ranking_opportunities']
            
            if opportunities:
                opp_df = pd.DataFrame(opportunities)
                st.dataframe(opp_df, use_container_width=True)
                
                st.info(f"💡 Found {len(opportunities)} keywords where you're not ranking in top 10!")
            else:
                st.success("🎉 You're already ranking well for your target keywords!")
        
        # SERP features analysis
        if serp_data.get('keyword_rankings'):
            st.markdown("#### 🎯 SERP Features Opportunities")
            
            all_features = []
            for keyword_data in serp_data['keyword_rankings'].values():
                all_features.extend(keyword_data.get('serp_features', []))
            
            if all_features:
                feature_counts = pd.Series(all_features).value_counts()
                st.bar_chart(feature_counts)
                
                st.markdown("**🎯 Focus on these SERP features:**")
                for feature, count in feature_counts.head(3).items():
                    st.write(f"• **{feature.replace('_', ' ').title()}**: Appears in {count} keyword searches")
    
    def _render_keyword_research(self, keyword_data: Dict[str, Any]):
        """Render keyword research results."""
        
        st.markdown("### 🎯 Advanced Keyword Research")
        
        if not keyword_data:
            st.info("No keyword expansion data available")
            return
        
        # Seed vs expanded keywords
        seed_keywords = keyword_data.get('seed_keywords', [])
        expanded_keywords = keyword_data.get('expanded_keywords', [])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🌱 Seed Keywords", len(seed_keywords))
            if seed_keywords:
                for kw in seed_keywords:
                    st.write(f"• {kw}")
        
        with col2:
            st.metric("🔍 Expanded Keywords", len(expanded_keywords))
            st.write(f"**Expansion Factor:** {len(expanded_keywords) / len(seed_keywords) if seed_keywords else 0:.1f}x")
        
        # Search intent categorization
        if keyword_data.get('keyword_categories'):
            st.markdown("#### 🧠 Search Intent Analysis")
            
            categories = keyword_data['keyword_categories']
            
            # Create intent distribution chart
            intent_counts = {intent: len(keywords) for intent, keywords in categories.items() if keywords}
            
            if intent_counts:
                intent_df = pd.DataFrame(
                    list(intent_counts.items()),
                    columns=['Search Intent', 'Keywords']
                )
                st.bar_chart(intent_df.set_index('Search Intent'))
                
                # Detailed breakdown
                for intent, keywords in categories.items():
                    if keywords:
                        with st.expander(f"📂 {intent.title()} Keywords ({len(keywords)})"):
                            for kw in keywords[:20]:  # Show first 20
                                st.write(f"• {kw}")
        
        # Long-tail opportunities
        if keyword_data.get('long_tail_opportunities'):
            st.markdown("#### 🎣 Long-tail Keyword Opportunities")
            
            long_tail = keyword_data['long_tail_opportunities']
            
            if long_tail:
                st.info(f"🎯 Found {len(long_tail)} long-tail opportunities with lower competition!")
                
                # Display in expandable format
                with st.expander("View Long-tail Keywords"):
                    for i, kw in enumerate(long_tail, 1):
                        st.write(f"{i}. {kw}")
            else:
                st.warning("No long-tail opportunities identified")
    
    def _render_competitor_intelligence(self, competitor_data: Dict[str, Any]):
        """Render competitor intelligence results."""
        
        st.markdown("### 🕷️ Competitive Intelligence")
        
        if not competitor_data.get('crawl_results'):
            st.info("No competitor crawl data available")
            return
        
        # Crawl summary
        crawl_results = competitor_data['crawl_results']
        
        st.markdown("#### 📊 Competitor Content Overview")
        
        # Create summary table
        summary_data = []
        for domain, data in crawl_results.items():
            summary_data.append({
                'Competitor': domain,
                'Pages Crawled': data.get('total_pages', 0),
                'Avg Content Length': f"{data.get('content_length_stats', {}).get('mean', 0):,.0f} chars",
                'Success Rate': f"{data.get('status_codes', {}).get(200, 0) / data.get('total_pages', 1) * 100:.1f}%"
            })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
        
        # Page type analysis
        st.markdown("#### 📄 Content Type Distribution")
        
        for domain, data in crawl_results.items():
            page_types = data.get('page_types', {})
            
            if page_types:
                with st.expander(f"📊 {domain} Content Types"):
                    
                    # Create chart data
                    types_df = pd.DataFrame(
                        list(page_types.items()),
                        columns=['Page Type', 'Count']
                    )
                    
                    if not types_df.empty:
                        st.bar_chart(types_df.set_index('Page Type'))
                        
                        # Key insights
                        total_pages = sum(page_types.values())
                        if total_pages > 0:
                            blog_ratio = page_types.get('blog_posts', 0) / total_pages * 100
                            product_ratio = page_types.get('product_pages', 0) / total_pages * 100
                            
                            st.write("**Content Strategy Insights:**")
                            st.write(f"• Blog content: {blog_ratio:.1f}% of pages")
                            st.write(f"• Product focus: {product_ratio:.1f}% of pages")
        
        # Content structure insights
        if competitor_data.get('content_structure'):
            st.markdown("#### 🏗️ Content Structure Analysis")
            
            structure_data = competitor_data['content_structure']
            
            for domain, structure in structure_data.items():
                with st.expander(f"🔍 {domain} Structure Analysis"):
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Avg Title Length", f"{structure.get('avg_title_length', 0):.0f} chars")
                        st.metric("H1 Usage", f"{structure.get('h1_usage', 0):.1f}%")
                    
                    with col2:
                        st.metric("Avg Meta Desc Length", f"{structure.get('avg_meta_desc_length', 0):.0f} chars")
                        st.metric("Internal Links", f"{structure.get('internal_links_avg', 0):.1f} avg")
    
    def _render_content_themes(self, theme_data: Dict[str, Any]):
        """Render content theme analysis."""
        
        st.markdown("### 📊 Content Theme Intelligence")
        
        if not theme_data:
            st.info("No content theme data available")
            return
        
        # Dominant themes
        if theme_data.get('dominant_themes'):
            st.markdown("#### 🎯 Dominant Content Themes")
            
            themes = theme_data['dominant_themes']
            
            if themes:
                themes_df = pd.DataFrame(themes)
                st.dataframe(themes_df, use_container_width=True)
                
                # Top themes highlight
                st.markdown("**🔥 Top Content Themes:**")
                for i, theme in enumerate(themes[:5], 1):
                    word = theme.get('word', theme.get('text', 'Unknown'))
                    freq = theme.get('freq', theme.get('frequency', 0))
                    st.write(f"{i}. **{word}** (appears {freq} times)")
        
        # Content clusters
        if theme_data.get('content_clusters'):
            st.markdown("#### 🗂️ Topic Cluster Analysis")
            
            clusters = theme_data['content_clusters']
            
            # Cluster distribution
            cluster_counts = {name: len(themes) for name, themes in clusters.items() if themes}
            
            if cluster_counts:
                cluster_df = pd.DataFrame(
                    list(cluster_counts.items()),
                    columns=['Topic Cluster', 'Theme Count']
                )
                st.bar_chart(cluster_df.set_index('Topic Cluster'))
                
                # Detailed cluster view
                for cluster_name, themes in clusters.items():
                    if themes:
                        with st.expander(f"📂 {cluster_name.replace('_', ' ').title()} ({len(themes)} themes)"):
                            for theme in themes[:15]:  # Show first 15
                                st.write(f"• {theme}")
        
        # Content gaps and opportunities
        if theme_data.get('content_opportunities'):
            st.markdown("#### 🎯 Content Gap Opportunities")
            
            opportunities = theme_data['content_opportunities']
            
            if opportunities:
                for opp in opportunities:
                    st.write(f"🎯 **{opp}**")
            else:
                st.info("No specific content opportunities identified in theme analysis")
    
    def _render_ai_insights(self, ai_data: Dict[str, Any]):
        """Render AI-generated strategic insights."""
        
        st.markdown("### 🤖 AI-Powered Strategic Insights")
        
        if not ai_data:
            st.info("No AI insights available")
            return
        
        # Strategic recommendations
        if ai_data.get('recommendations'):
            st.markdown("#### 🎯 Priority Strategic Recommendations")
            
            recommendations = ai_data['recommendations']
            
            for i, rec in enumerate(recommendations[:5], 1):
                with st.expander(f"🎯 Recommendation {i}"):
                    st.markdown(rec)
        
        # Competitive positioning
        if ai_data.get('competitive_positioning'):
            st.markdown("#### 🏆 Competitive Positioning Insights")
            st.markdown(ai_data['competitive_positioning'])
        
        # Content strategy insights
        if ai_data.get('content_strategy'):
            st.markdown("#### 📝 Content Strategy Recommendations")
            st.markdown(ai_data['content_strategy'])
        
        # Implementation timeline
        if ai_data.get('implementation_timeline'):
            st.markdown("#### 📅 Implementation Roadmap")
            
            timeline = ai_data['implementation_timeline']
            
            for period, tasks in timeline.items():
                with st.expander(f"📅 {period.replace('_', ' ').title()} Plan"):
                    for task in tasks:
                        st.write(f"• {task}")
        
        # Technical SEO opportunities
        if ai_data.get('technical_opportunities'):
            st.markdown("#### ⚙️ Technical SEO Opportunities")
            
            tech_opps = ai_data['technical_opportunities']
            
            for opp in tech_opps:
                st.write(f"⚙️ {opp}")
    
    def _render_action_plan(self, results: Dict[str, Any]):
        """Render actionable implementation plan."""
        
        st.markdown("### 📋 Your Content Gap Action Plan")
        
        # Quick wins section
        st.markdown("#### 🚀 Quick Wins (Week 1-2)")
        
        quick_wins = []
        
        # SERP opportunities
        serp_opportunities = results.get('serp_analysis', {}).get('ranking_opportunities', [])
        if serp_opportunities:
            quick_wins.append(f"🎯 Target {len(serp_opportunities)} keywords where you're not ranking")
        
        # Long-tail keywords
        long_tail = results.get('keyword_expansion', {}).get('long_tail_opportunities', [])
        if long_tail:
            quick_wins.append(f"🎣 Create content for {min(5, len(long_tail))} high-potential long-tail keywords")
        
        # Content themes
        themes = results.get('content_themes', {}).get('dominant_themes', [])
        if themes:
            top_theme = themes[0].get('word', 'top theme') if themes else 'content optimization'
            quick_wins.append(f"📊 Optimize existing content around '{top_theme}' theme")
        
        for i, win in enumerate(quick_wins, 1):
            st.write(f"{i}. {win}")
        
        # Medium-term strategy
        st.markdown("#### 📈 Medium-term Strategy (Month 1-3)")
        
        medium_term = [
            "🕷️ Conduct regular competitor content audits",
            "🎯 Develop content calendar based on keyword gaps",
            "📊 Implement content theme clusters",
            "🤖 Set up automated SERP monitoring"
        ]
        
        for i, strategy in enumerate(medium_term, 1):
            st.write(f"{i}. {strategy}")
        
        # Long-term vision
        st.markdown("#### 🎯 Long-term Vision (Quarter 2+)")
        
        long_term = [
            "🏆 Establish thought leadership in identified content gaps",
            "🌐 Build comprehensive content hub around dominant themes",
            "📈 Scale content production based on proven gaps",
            "🤝 Develop strategic partnerships for content collaboration"
        ]
        
        for i, vision in enumerate(long_term, 1):
            st.write(f"{i}. {vision}")
        
        # Success metrics
        st.markdown("#### 📊 Success Metrics to Track")
        
        metrics = [
            "🎯 Keyword ranking improvements for target terms",
            "📈 Organic traffic growth from new content",
            "🔍 SERP feature acquisitions (featured snippets, etc.)",
            "🏆 Competitive ranking gains in content themes",
            "📊 Content engagement metrics and user behavior"
        ]
        
        for metric in metrics:
            st.write(f"• {metric}")
    
    def _render_export_options(self, results: Dict[str, Any]):
        """Render export options for analysis results."""
        
        st.markdown("---")
        st.markdown("### 📥 Export Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # JSON export
            if st.button("📄 Export as JSON", use_container_width=True):
                json_data = json.dumps(results, indent=2, default=str)
                
                st.download_button(
                    label="⬇️ Download JSON Report",
                    data=json_data,
                    file_name=f"content_gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            # CSV export for keywords
            if st.button("📊 Export Keywords CSV", use_container_width=True):
                expanded_keywords = results.get('keyword_expansion', {}).get('expanded_keywords', [])
                
                if expanded_keywords:
                    keywords_df = pd.DataFrame(expanded_keywords, columns=['Keyword'])
                    csv_data = keywords_df.to_csv(index=False)
                    
                    st.download_button(
                        label="⬇️ Download Keywords CSV",
                        data=csv_data,
                        file_name=f"discovered_keywords_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.warning("No keywords available for export")
        
        with col3:
            # Summary report
            if st.button("📋 Generate Summary Report", use_container_width=True):
                summary = self._generate_summary_report(results)
                
                st.download_button(
                    label="⬇️ Download Summary Report",
                    data=summary,
                    file_name=f"content_gap_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    def _generate_summary_report(self, results: Dict[str, Any]) -> str:
        """Generate a text summary report."""
        
        target_url = results.get('target_url', 'Unknown')
        timestamp = results.get('analysis_timestamp', datetime.now().isoformat())
        
        summary = f"""
ENHANCED CONTENT GAP ANALYSIS REPORT
=====================================

Target Website: {target_url}
Analysis Date: {timestamp}
Industry: {results.get('industry', 'General')}

EXECUTIVE SUMMARY
-----------------
Keywords Analyzed: {len(results.get('target_keywords', []))}
Competitors Analyzed: {len(results.get('competitor_urls', []))}
Keywords Discovered: {len(results.get('keyword_expansion', {}).get('expanded_keywords', []))}
SERP Opportunities: {len(results.get('serp_analysis', {}).get('ranking_opportunities', []))}

RANKING OPPORTUNITIES
---------------------
"""
        
        # Add ranking opportunities
        opportunities = results.get('serp_analysis', {}).get('ranking_opportunities', [])
        for i, opp in enumerate(opportunities[:10], 1):
            summary += f"{i}. {opp.get('keyword', 'Unknown keyword')}\n"
        
        # Add top keywords discovered
        summary += "\nTOP DISCOVERED KEYWORDS\n-----------------------\n"
        expanded_keywords = results.get('keyword_expansion', {}).get('expanded_keywords', [])
        for i, kw in enumerate(expanded_keywords[:20], 1):
            summary += f"{i}. {kw}\n"
        
        # Add AI recommendations
        recommendations = results.get('ai_insights', {}).get('recommendations', [])
        if recommendations:
            summary += "\nAI STRATEGIC RECOMMENDATIONS\n----------------------------\n"
            for i, rec in enumerate(recommendations[:5], 1):
                summary += f"{i}. {rec}\n"
        
        summary += f"\n\nReport generated by ALwrity Enhanced Content Gap Analysis\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return summary

# Render function for integration with main dashboard
def render_enhanced_content_gap_analysis():
    """Render the enhanced content gap analysis UI."""
    ui = EnhancedContentGapAnalysisUI()
    ui.render() 