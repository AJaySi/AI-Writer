"""
Technical SEO Crawler UI with Comprehensive Analysis Dashboard.

This module provides a professional Streamlit interface for the Technical SEO Crawler
with detailed analysis results, visualization, and export capabilities.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List
import json
from datetime import datetime
import io
import base64
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .crawler import TechnicalSEOCrawler
from lib.alwrity_ui.dashboard_styles import apply_dashboard_style, render_dashboard_header

class TechnicalSEOCrawlerUI:
    """Professional UI for Technical SEO Crawler."""
    
    def __init__(self):
        """Initialize the Technical SEO Crawler UI."""
        self.crawler = TechnicalSEOCrawler()
        
        # Apply dashboard styling
        apply_dashboard_style()
    
    def render(self):
        """Render the Technical SEO Crawler interface."""
        
        # Enhanced dashboard header
        render_dashboard_header(
            "🔧 Technical SEO Crawler",
            "Comprehensive site-wide technical SEO analysis with AI-powered recommendations. Identify and fix technical issues that impact your search rankings."
        )
        
        # Main content area
        with st.container():
            # Analysis input form
            self._render_crawler_form()
        
        # Session state for results
        if 'technical_seo_results' in st.session_state and st.session_state.technical_seo_results:
            st.markdown("---")
            self._render_results_dashboard(st.session_state.technical_seo_results)
    
    def _render_crawler_form(self):
        """Render the crawler configuration form."""
        st.markdown("## 🚀 Configure Technical SEO Audit")
        
        with st.form("technical_seo_crawler_form"):
            # Website URL input
            col1, col2 = st.columns([3, 1])
            
            with col1:
                website_url = st.text_input(
                    "🌐 Website URL to Audit",
                    placeholder="https://yourwebsite.com",
                    help="Enter the website URL for comprehensive technical SEO analysis"
                )
            
            with col2:
                audit_type = st.selectbox(
                    "🎯 Audit Type",
                    options=["Standard", "Deep", "Quick"],
                    help="Choose the depth of analysis"
                )
            
            # Crawl configuration
            st.markdown("### ⚙️ Crawl Configuration")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if audit_type == "Quick":
                    crawl_depth = st.slider("Crawl Depth", 1, 2, 1)
                    max_pages = st.slider("Max Pages", 10, 100, 50)
                elif audit_type == "Deep":
                    crawl_depth = st.slider("Crawl Depth", 1, 5, 4)
                    max_pages = st.slider("Max Pages", 100, 1000, 500)
                else:  # Standard
                    crawl_depth = st.slider("Crawl Depth", 1, 4, 3)
                    max_pages = st.slider("Max Pages", 50, 500, 200)
            
            with col2:
                analyze_images = st.checkbox(
                    "🖼️ Analyze Images",
                    value=True,
                    help="Include image SEO analysis"
                )
                
                analyze_security = st.checkbox(
                    "🛡️ Security Headers",
                    value=True,
                    help="Analyze security headers"
                )
            
            with col3:
                analyze_mobile = st.checkbox(
                    "📱 Mobile SEO",
                    value=True,
                    help="Include mobile SEO analysis"
                )
                
                ai_recommendations = st.checkbox(
                    "🤖 AI Recommendations",
                    value=True,
                    help="Generate AI-powered recommendations"
                )
            
            # Analysis scope
            st.markdown("### 🎯 Analysis Scope")
            
            analysis_options = st.multiselect(
                "Select Analysis Components",
                options=[
                    "Technical Issues Detection",
                    "Performance Analysis", 
                    "Content Structure Analysis",
                    "URL Structure Optimization",
                    "Internal Linking Analysis",
                    "Duplicate Content Detection"
                ],
                default=[
                    "Technical Issues Detection",
                    "Performance Analysis", 
                    "Content Structure Analysis"
                ],
                help="Choose which analysis components to include"
            )
            
            # Submit button
            submitted = st.form_submit_button(
                "🚀 Start Technical SEO Audit",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                # Validate inputs
                if not website_url or not website_url.startswith(('http://', 'https://')):
                    st.error("❌ Please enter a valid website URL starting with http:// or https://")
                    return
                
                # Run technical SEO analysis
                self._run_technical_analysis(
                    website_url=website_url,
                    crawl_depth=crawl_depth,
                    max_pages=max_pages,
                    options={
                        'analyze_images': analyze_images,
                        'analyze_security': analyze_security,
                        'analyze_mobile': analyze_mobile,
                        'ai_recommendations': ai_recommendations,
                        'analysis_scope': analysis_options
                    }
                )
    
    def _run_technical_analysis(self, website_url: str, crawl_depth: int, 
                               max_pages: int, options: Dict[str, Any]):
        """Run the technical SEO analysis."""
        
        try:
            with st.spinner("🔄 Running Comprehensive Technical SEO Audit..."):
                
                # Initialize progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                progress_bar.progress(10)
                status_text.text("🚀 Initializing technical SEO crawler...")
                
                # Run comprehensive analysis
                results = self.crawler.analyze_website_technical_seo(
                    website_url=website_url,
                    crawl_depth=crawl_depth,
                    max_pages=max_pages
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Technical SEO audit complete!")
                
                # Store results in session state
                st.session_state.technical_seo_results = results
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                if 'error' in results:
                    st.error(f"❌ Analysis failed: {results['error']}")
                else:
                    st.success("🎉 Technical SEO Audit completed successfully!")
                    st.balloons()
                    
                    # Rerun to show results
                    st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error running technical analysis: {str(e)}")
    
    def _render_results_dashboard(self, results: Dict[str, Any]):
        """Render the comprehensive results dashboard."""
        
        if 'error' in results:
            st.error(f"❌ Analysis Error: {results['error']}")
            return
        
        # Results header
        st.markdown("## 📊 Technical SEO Audit Results")
        
        # Key metrics overview
        self._render_metrics_overview(results)
        
        # Detailed analysis tabs
        self._render_detailed_analysis(results)
        
        # Export functionality
        self._render_export_options(results)
    
    def _render_metrics_overview(self, results: Dict[str, Any]):
        """Render key metrics overview."""
        
        st.markdown("### 📈 Audit Overview")
        
        # Create metrics columns
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            pages_crawled = results.get('crawl_overview', {}).get('pages_crawled', 0)
            st.metric(
                "🕷️ Pages Crawled",
                pages_crawled,
                help="Total pages analyzed"
            )
        
        with col2:
            error_count = results.get('technical_issues', {}).get('http_errors', {}).get('total_errors', 0)
            st.metric(
                "❌ HTTP Errors",
                error_count,
                delta=f"-{error_count}" if error_count > 0 else None,
                help="Pages with HTTP errors (4xx, 5xx)"
            )
        
        with col3:
            avg_load_time = results.get('performance_analysis', {}).get('load_time_analysis', {}).get('avg_load_time', 0)
            st.metric(
                "⚡ Avg Load Time",
                f"{avg_load_time:.2f}s",
                delta=f"+{avg_load_time:.2f}s" if avg_load_time > 3 else None,
                help="Average page load time"
            )
        
        with col4:
            security_score = results.get('security_headers', {}).get('security_score', 0)
            st.metric(
                "🛡️ Security Score",
                f"{security_score:.0f}%",
                delta=f"{security_score:.0f}%" if security_score < 100 else None,
                help="Security headers implementation score"
            )
        
        with col5:
            missing_titles = results.get('content_analysis', {}).get('title_analysis', {}).get('missing_titles', 0)
            st.metric(
                "📝 Missing Titles",
                missing_titles,
                delta=f"-{missing_titles}" if missing_titles > 0 else None,
                help="Pages without title tags"
            )
        
        with col6:
            image_count = results.get('image_optimization', {}).get('image_count', 0)
            st.metric(
                "🖼️ Images Analyzed",
                image_count,
                help="Total images found and analyzed"
            )
        
        # Analysis timestamp
        if results.get('analysis_timestamp'):
            timestamp = datetime.fromisoformat(results['analysis_timestamp'].replace('Z', '+00:00'))
            st.caption(f"📅 Audit completed: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    def _render_detailed_analysis(self, results: Dict[str, Any]):
        """Render detailed analysis in tabs."""
        
        # Create main analysis tabs
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "🔍 Technical Issues",
            "⚡ Performance",
            "📊 Content Analysis", 
            "🔗 URL Structure",
            "🖼️ Image SEO",
            "🛡️ Security",
            "🤖 AI Recommendations"
        ])
        
        with tab1:
            self._render_technical_issues(results.get('technical_issues', {}))
        
        with tab2:
            self._render_performance_analysis(results.get('performance_analysis', {}))
        
        with tab3:
            self._render_content_analysis(results.get('content_analysis', {}))
        
        with tab4:
            self._render_url_structure(results.get('url_structure', {}))
        
        with tab5:
            self._render_image_analysis(results.get('image_optimization', {}))
        
        with tab6:
            self._render_security_analysis(results.get('security_headers', {}))
        
        with tab7:
            self._render_ai_recommendations(results.get('ai_recommendations', {}))
    
    def _render_technical_issues(self, technical_data: Dict[str, Any]):
        """Render technical issues analysis."""
        
        st.markdown("### 🔍 Technical SEO Issues")
        
        if not technical_data:
            st.info("No technical issues data available")
            return
        
        # HTTP Errors
        if technical_data.get('http_errors'):
            http_errors = technical_data['http_errors']
            
            st.markdown("#### ❌ HTTP Status Code Errors")
            
            if http_errors.get('total_errors', 0) > 0:
                st.error(f"Found {http_errors['total_errors']} pages with HTTP errors!")
                
                # Error breakdown chart
                if http_errors.get('error_breakdown'):
                    error_df = pd.DataFrame(
                        list(http_errors['error_breakdown'].items()),
                        columns=['Status Code', 'Count']
                    )
                    
                    fig = px.bar(error_df, x='Status Code', y='Count', 
                               title="HTTP Error Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Error pages table
                if http_errors.get('error_pages'):
                    st.markdown("**Pages with Errors:**")
                    error_pages_df = pd.DataFrame(http_errors['error_pages'])
                    st.dataframe(error_pages_df, use_container_width=True)
            else:
                st.success("✅ No HTTP errors found!")
        
        # Redirect Issues
        if technical_data.get('redirect_issues'):
            redirect_data = technical_data['redirect_issues']
            
            st.markdown("#### 🔄 Redirect Analysis")
            
            total_redirects = redirect_data.get('total_redirects', 0)
            
            if total_redirects > 0:
                st.warning(f"Found {total_redirects} redirect(s)")
                
                # Redirect types
                if redirect_data.get('redirect_types'):
                    redirect_df = pd.DataFrame(
                        list(redirect_data['redirect_types'].items()),
                        columns=['Redirect Type', 'Count']
                    )
                    st.bar_chart(redirect_df.set_index('Redirect Type'))
            else:
                st.success("✅ No redirects found")
        
        # Duplicate Content
        if technical_data.get('duplicate_content'):
            duplicate_data = technical_data['duplicate_content']
            
            st.markdown("#### 📋 Duplicate Content Issues")
            
            duplicate_titles = duplicate_data.get('duplicate_titles', 0)
            
            if duplicate_titles > 0:
                st.warning(f"Found {duplicate_titles} duplicate title(s)")
                
                # Show duplicate title groups
                if duplicate_data.get('pages_with_duplicate_titles'):
                    duplicate_df = pd.DataFrame(duplicate_data['pages_with_duplicate_titles'])
                    st.dataframe(duplicate_df, use_container_width=True)
            else:
                st.success("✅ No duplicate titles found")
        
        # Missing Elements
        if technical_data.get('missing_elements'):
            missing_data = technical_data['missing_elements']
            
            st.markdown("#### 📝 Missing SEO Elements")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                missing_titles = missing_data.get('missing_titles', 0)
                if missing_titles > 0:
                    st.error(f"Missing Titles: {missing_titles}")
                else:
                    st.success("All pages have titles ✅")
            
            with col2:
                missing_meta = missing_data.get('missing_meta_desc', 0)
                if missing_meta > 0:
                    st.error(f"Missing Meta Descriptions: {missing_meta}")
                else:
                    st.success("All pages have meta descriptions ✅")
            
            with col3:
                missing_h1 = missing_data.get('missing_h1', 0)
                if missing_h1 > 0:
                    st.error(f"Missing H1 tags: {missing_h1}")
                else:
                    st.success("All pages have H1 tags ✅")
    
    def _render_performance_analysis(self, performance_data: Dict[str, Any]):
        """Render performance analysis."""
        
        st.markdown("### ⚡ Website Performance Analysis")
        
        if not performance_data:
            st.info("No performance data available")
            return
        
        # Load Time Analysis
        if performance_data.get('load_time_analysis'):
            load_time_data = performance_data['load_time_analysis']
            
            st.markdown("#### 🚀 Page Load Time Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_load = load_time_data.get('avg_load_time', 0)
                st.metric("Average Load Time", f"{avg_load:.2f}s")
            
            with col2:
                median_load = load_time_data.get('median_load_time', 0)
                st.metric("Median Load Time", f"{median_load:.2f}s")
            
            with col3:
                p95_load = load_time_data.get('p95_load_time', 0)
                st.metric("95th Percentile", f"{p95_load:.2f}s")
            
            # Performance distribution
            if load_time_data.get('performance_distribution'):
                perf_dist = load_time_data['performance_distribution']
                
                # Create pie chart for performance distribution
                labels = ['Fast (≤1s)', 'Moderate (1-3s)', 'Slow (>3s)']
                values = [
                    perf_dist.get('fast_pages', 0),
                    perf_dist.get('moderate_pages', 0),
                    perf_dist.get('slow_pages', 0)
                ]
                
                fig = px.pie(values=values, names=labels, 
                           title="Page Load Time Distribution")
                st.plotly_chart(fig, use_container_width=True)
        
        # Content Size Analysis
        if performance_data.get('content_size_analysis'):
            size_data = performance_data['content_size_analysis']
            
            st.markdown("#### 📦 Content Size Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_size = size_data.get('avg_page_size', 0)
                st.metric("Average Page Size", f"{avg_size/1024:.1f} KB")
            
            with col2:
                largest_size = size_data.get('largest_page', 0)
                st.metric("Largest Page", f"{largest_size/1024:.1f} KB")
            
            with col3:
                large_pages = size_data.get('pages_over_1mb', 0)
                st.metric("Pages >1MB", large_pages)
        
        # Server Performance
        if performance_data.get('server_performance'):
            server_data = performance_data['server_performance']
            
            st.markdown("#### 🖥️ Server Performance")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                success_rate = server_data.get('success_rate', 0)
                st.metric("Success Rate", f"{success_rate:.1f}%")
            
            with col2:
                error_rate = server_data.get('error_rate', 0)
                st.metric("Error Rate", f"{error_rate:.1f}%")
            
            with col3:
                redirect_rate = server_data.get('redirect_rate', 0)
                st.metric("Redirect Rate", f"{redirect_rate:.1f}%")
    
    def _render_content_analysis(self, content_data: Dict[str, Any]):
        """Render content structure analysis."""
        
        st.markdown("### 📊 Content Structure Analysis")
        
        if not content_data:
            st.info("No content analysis data available")
            return
        
        # Title Analysis
        if content_data.get('title_analysis'):
            title_data = content_data['title_analysis']
            
            st.markdown("#### 📝 Title Tag Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                avg_title_length = title_data.get('avg_title_length', 0)
                st.metric("Average Title Length", f"{avg_title_length:.0f} chars")
                
                duplicate_titles = title_data.get('duplicate_titles', 0)
                st.metric("Duplicate Titles", duplicate_titles)
            
            with col2:
                # Title length distribution
                if title_data.get('title_length_distribution'):
                    length_dist = title_data['title_length_distribution']
                    
                    labels = ['Too Short (<30)', 'Optimal (30-60)', 'Too Long (>60)']
                    values = [
                        length_dist.get('too_short', 0),
                        length_dist.get('optimal', 0),
                        length_dist.get('too_long', 0)
                    ]
                    
                    fig = px.pie(values=values, names=labels, 
                               title="Title Length Distribution")
                    st.plotly_chart(fig, use_container_width=True)
        
        # Meta Description Analysis
        if content_data.get('meta_description_analysis'):
            meta_data = content_data['meta_description_analysis']
            
            st.markdown("#### 🏷️ Meta Description Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                avg_meta_length = meta_data.get('avg_meta_length', 0)
                st.metric("Average Meta Length", f"{avg_meta_length:.0f} chars")
                
                missing_meta = meta_data.get('missing_meta_descriptions', 0)
                st.metric("Missing Meta Descriptions", missing_meta)
            
            with col2:
                # Meta length distribution
                if meta_data.get('meta_length_distribution'):
                    meta_dist = meta_data['meta_length_distribution']
                    
                    labels = ['Too Short (<120)', 'Optimal (120-160)', 'Too Long (>160)']
                    values = [
                        meta_dist.get('too_short', 0),
                        meta_dist.get('optimal', 0),
                        meta_dist.get('too_long', 0)
                    ]
                    
                    fig = px.pie(values=values, names=labels, 
                               title="Meta Description Length Distribution")
                    st.plotly_chart(fig, use_container_width=True)
        
        # Heading Structure
        if content_data.get('heading_structure'):
            heading_data = content_data['heading_structure']
            
            st.markdown("#### 📋 Heading Structure Analysis")
            
            # Create heading usage chart
            heading_usage = []
            for heading_type, data in heading_data.items():
                heading_usage.append({
                    'Heading': heading_type.replace('_usage', '').upper(),
                    'Usage Rate': data.get('usage_rate', 0),
                    'Pages': data.get('pages_with_heading', 0)
                })
            
            if heading_usage:
                heading_df = pd.DataFrame(heading_usage)
                
                fig = px.bar(heading_df, x='Heading', y='Usage Rate',
                           title="Heading Tag Usage Rates")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(heading_df, use_container_width=True)
    
    def _render_url_structure(self, url_data: Dict[str, Any]):
        """Render URL structure analysis."""
        
        st.markdown("### 🔗 URL Structure Analysis")
        
        if not url_data:
            st.info("No URL structure data available")
            return
        
        # URL Length Analysis
        if url_data.get('url_length_analysis'):
            length_data = url_data['url_length_analysis']
            
            st.markdown("#### 📏 URL Length Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_length = length_data.get('avg_url_length', 0)
                st.metric("Average URL Length", f"{avg_length:.0f} chars")
            
            with col2:
                max_length = length_data.get('max_url_length', 0)
                st.metric("Longest URL", f"{max_length:.0f} chars")
            
            with col3:
                long_urls = length_data.get('long_urls_count', 0)
                st.metric("URLs >100 chars", long_urls)
        
        # URL Structure Patterns
        if url_data.get('url_structure_patterns'):
            pattern_data = url_data['url_structure_patterns']
            
            st.markdown("#### 🏗️ URL Structure Patterns")
            
            col1, col2 = st.columns(2)
            
            with col1:
                https_usage = pattern_data.get('https_usage', 0)
                st.metric("HTTPS Usage", f"{https_usage:.1f}%")
            
            with col2:
                subdomain_usage = pattern_data.get('subdomain_usage', 0)
                st.metric("Subdomains Found", subdomain_usage)
        
        # Path Analysis
        if url_data.get('path_analysis'):
            path_data = url_data['path_analysis']
            
            st.markdown("#### 📂 Path Depth Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_depth = path_data.get('avg_path_depth', 0)
                st.metric("Average Path Depth", f"{avg_depth:.1f}")
            
            with col2:
                max_depth = path_data.get('max_path_depth', 0)
                st.metric("Maximum Depth", max_depth)
            
            with col3:
                deep_paths = path_data.get('deep_paths_count', 0)
                st.metric("Deep Paths (>4)", deep_paths)
        
        # Optimization Issues
        if url_data.get('url_optimization'):
            opt_data = url_data['url_optimization']
            
            st.markdown("#### ⚠️ URL Optimization Issues")
            
            issues_found = opt_data.get('issues_found', 0)
            recommendations = opt_data.get('optimization_recommendations', [])
            
            if issues_found > 0:
                st.warning(f"Found {issues_found} URL optimization issue(s)")
                
                for rec in recommendations:
                    st.write(f"• {rec}")
            else:
                st.success("✅ No URL optimization issues found")
    
    def _render_image_analysis(self, image_data: Dict[str, Any]):
        """Render image SEO analysis."""
        
        st.markdown("### 🖼️ Image SEO Analysis")
        
        if not image_data:
            st.info("No image analysis data available")
            return
        
        # Image overview
        image_count = image_data.get('image_count', 0)
        st.metric("Total Images Found", image_count)
        
        if image_count > 0:
            # Alt text analysis
            if image_data.get('alt_text_analysis'):
                alt_data = image_data['alt_text_analysis']
                
                st.markdown("#### 📝 Alt Text Analysis")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    images_with_alt = alt_data.get('images_with_alt', 0)
                    st.metric("Images with Alt Text", images_with_alt)
                
                with col2:
                    images_missing_alt = alt_data.get('images_missing_alt', 0)
                    st.metric("Missing Alt Text", images_missing_alt)
                
                with col3:
                    alt_coverage = alt_data.get('alt_text_coverage', 0)
                    st.metric("Alt Text Coverage", f"{alt_coverage:.1f}%")
            
            # Image format analysis
            if image_data.get('image_format_analysis'):
                format_data = image_data['image_format_analysis']
                
                st.markdown("#### 🎨 Image Format Analysis")
                
                if format_data.get('format_distribution'):
                    format_dist = format_data['format_distribution']
                    
                    format_df = pd.DataFrame(
                        list(format_dist.items()),
                        columns=['Format', 'Count']
                    )
                    
                    fig = px.pie(format_df, values='Count', names='Format',
                               title="Image Format Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                modern_formats = format_data.get('modern_format_usage', 0)
                st.metric("Modern Formats (WebP/AVIF)", modern_formats)
        else:
            st.info("No images found to analyze")
    
    def _render_security_analysis(self, security_data: Dict[str, Any]):
        """Render security analysis."""
        
        st.markdown("### 🛡️ Security Headers Analysis")
        
        if not security_data:
            st.info("No security analysis data available")
            return
        
        # Security score
        security_score = security_data.get('security_score', 0)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Security Score", f"{security_score:.0f}%")
            
            if security_score >= 80:
                st.success("🔒 Good security posture")
            elif security_score >= 50:
                st.warning("⚠️ Moderate security")
            else:
                st.error("🚨 Poor security posture")
        
        with col2:
            # Security headers status
            if security_data.get('security_headers_present'):
                headers_status = security_data['security_headers_present']
                
                st.markdown("**Security Headers Status:**")
                
                for header, present in headers_status.items():
                    status = "✅" if present else "❌"
                    st.write(f"{status} {header}")
        
        # Security recommendations
        if security_data.get('security_recommendations'):
            recommendations = security_data['security_recommendations']
            
            if recommendations:
                st.markdown("#### 🔧 Security Recommendations")
                
                for rec in recommendations:
                    st.write(f"• {rec}")
            else:
                st.success("✅ All security headers properly configured")
    
    def _render_ai_recommendations(self, ai_data: Dict[str, Any]):
        """Render AI-generated recommendations."""
        
        st.markdown("### 🤖 AI-Powered Technical Recommendations")
        
        if not ai_data:
            st.info("No AI recommendations available")
            return
        
        # Critical Issues
        if ai_data.get('critical_issues'):
            st.markdown("#### 🚨 Critical Issues (Fix Immediately)")
            
            critical_issues = ai_data['critical_issues']
            for issue in critical_issues:
                st.error(f"🚨 {issue}")
        
        # High Priority
        if ai_data.get('high_priority'):
            st.markdown("#### 🔥 High Priority Optimizations")
            
            high_priority = ai_data['high_priority']
            for item in high_priority:
                st.warning(f"⚡ {item}")
        
        # Medium Priority
        if ai_data.get('medium_priority'):
            st.markdown("#### 📈 Medium Priority Improvements")
            
            medium_priority = ai_data['medium_priority']
            for item in medium_priority:
                st.info(f"📊 {item}")
        
        # Implementation Steps
        if ai_data.get('implementation_steps'):
            st.markdown("#### 🛠️ Implementation Steps")
            
            steps = ai_data['implementation_steps']
            for i, step in enumerate(steps, 1):
                st.write(f"{i}. {step}")
        
        # Expected Impact
        if ai_data.get('expected_impact'):
            st.markdown("#### 📈 Expected Impact Assessment")
            
            impact = ai_data['expected_impact']
            st.markdown(impact)
    
    def _render_export_options(self, results: Dict[str, Any]):
        """Render export options for analysis results."""
        
        st.markdown("---")
        st.markdown("### 📥 Export Technical SEO Audit")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # JSON export
            if st.button("📄 Export Full Report (JSON)", use_container_width=True):
                json_data = json.dumps(results, indent=2, default=str)
                
                st.download_button(
                    label="⬇️ Download JSON Report",
                    data=json_data,
                    file_name=f"technical_seo_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            # CSV export for issues
            if st.button("📊 Export Issues CSV", use_container_width=True):
                issues_data = self._prepare_issues_csv(results)
                
                if issues_data:
                    st.download_button(
                        label="⬇️ Download Issues CSV",
                        data=issues_data,
                        file_name=f"technical_issues_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.info("No issues found to export")
        
        with col3:
            # Executive summary
            if st.button("📋 Executive Summary", use_container_width=True):
                summary = self._generate_executive_summary(results)
                
                st.download_button(
                    label="⬇️ Download Summary",
                    data=summary,
                    file_name=f"technical_seo_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    def _prepare_issues_csv(self, results: Dict[str, Any]) -> str:
        """Prepare CSV data for technical issues."""
        
        issues_list = []
        
        # HTTP errors
        http_errors = results.get('technical_issues', {}).get('http_errors', {})
        if http_errors.get('error_pages'):
            for error in http_errors['error_pages']:
                issues_list.append({
                    'Issue Type': 'HTTP Error',
                    'Severity': 'High',
                    'URL': error.get('url', ''),
                    'Status Code': error.get('status', ''),
                    'Description': f"HTTP {error.get('status', '')} error"
                })
        
        # Missing elements
        missing_elements = results.get('technical_issues', {}).get('missing_elements', {})
        
        # Add more issue types as needed...
        
        if issues_list:
            issues_df = pd.DataFrame(issues_list)
            return issues_df.to_csv(index=False)
        
        return ""
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> str:
        """Generate executive summary report."""
        
        website_url = results.get('website_url', 'Unknown')
        timestamp = results.get('analysis_timestamp', datetime.now().isoformat())
        
        summary = f"""
TECHNICAL SEO AUDIT - EXECUTIVE SUMMARY
======================================

Website: {website_url}
Audit Date: {timestamp}

AUDIT OVERVIEW
--------------
Pages Crawled: {results.get('crawl_overview', {}).get('pages_crawled', 0)}
HTTP Errors: {results.get('technical_issues', {}).get('http_errors', {}).get('total_errors', 0)}
Average Load Time: {results.get('performance_analysis', {}).get('load_time_analysis', {}).get('avg_load_time', 0):.2f}s
Security Score: {results.get('security_headers', {}).get('security_score', 0):.0f}%

CRITICAL FINDINGS
-----------------
"""
        
        # Add critical findings
        error_count = results.get('technical_issues', {}).get('http_errors', {}).get('total_errors', 0)
        if error_count > 0:
            summary += f"• {error_count} pages have HTTP errors requiring immediate attention\n"
        
        avg_load_time = results.get('performance_analysis', {}).get('load_time_analysis', {}).get('avg_load_time', 0)
        if avg_load_time > 3:
            summary += f"• Page load times are slow (avg: {avg_load_time:.2f}s), impacting user experience\n"
        
        security_score = results.get('security_headers', {}).get('security_score', 0)
        if security_score < 80:
            summary += f"• Security headers need improvement (current score: {security_score:.0f}%)\n"
        
        summary += f"\n\nDetailed technical audit completed by ALwrity Technical SEO Crawler\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return summary

# Render function for integration with main dashboard
def render_technical_seo_crawler():
    """Render the Technical SEO Crawler UI."""
    ui = TechnicalSEOCrawlerUI()
    ui.render() 