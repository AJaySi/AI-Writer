"""
Comprehensive Technical SEO Crawler using Advertools Integration.

This module provides advanced site-wide technical SEO analysis using:
- adv.crawl: Complete website crawling and analysis
- adv.crawl_headers: HTTP headers and server analysis
- adv.crawl_images: Image optimization analysis
- adv.url_to_df: URL structure optimization
- AI-powered technical recommendations
"""

import streamlit as st
import pandas as pd
import advertools as adv
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse, urljoin
import tempfile
import os
from datetime import datetime
import json
from collections import Counter, defaultdict
from loguru import logger
import numpy as np

# Import existing modules
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.utils.website_analyzer.analyzer import WebsiteAnalyzer

class TechnicalSEOCrawler:
    """Comprehensive technical SEO crawler with advertools integration."""
    
    def __init__(self):
        """Initialize the technical SEO crawler."""
        self.temp_dir = tempfile.mkdtemp()
        logger.info("TechnicalSEOCrawler initialized")
    
    def analyze_website_technical_seo(self, website_url: str, crawl_depth: int = 3, 
                                    max_pages: int = 500) -> Dict[str, Any]:
        """
        Perform comprehensive technical SEO analysis.
        
        Args:
            website_url: Website URL to analyze
            crawl_depth: How deep to crawl (1-5)
            max_pages: Maximum pages to crawl (50-1000)
            
        Returns:
            Comprehensive technical SEO analysis results
        """
        try:
            st.info("🚀 Starting Comprehensive Technical SEO Crawl...")
            
            # Initialize results structure
            results = {
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'website_url': website_url,
                'crawl_settings': {
                    'depth': crawl_depth,
                    'max_pages': max_pages
                },
                'crawl_overview': {},
                'technical_issues': {},
                'performance_analysis': {},
                'content_analysis': {},
                'url_structure': {},
                'image_optimization': {},
                'security_headers': {},
                'mobile_seo': {},
                'structured_data': {},
                'ai_recommendations': {}
            }
            
            # Phase 1: Core Website Crawl
            with st.expander("🕷️ Website Crawling Progress", expanded=True):
                crawl_data = self._perform_comprehensive_crawl(website_url, crawl_depth, max_pages)
                results['crawl_overview'] = crawl_data
                st.success(f"✅ Crawled {crawl_data.get('pages_crawled', 0)} pages")
            
            # Phase 2: Technical Issues Detection
            with st.expander("🔍 Technical Issues Analysis", expanded=True):
                technical_issues = self._analyze_technical_issues(crawl_data)
                results['technical_issues'] = technical_issues
                st.success("✅ Identified technical SEO issues")
            
            # Phase 3: Performance Analysis
            with st.expander("⚡ Performance Analysis", expanded=True):
                performance = self._analyze_performance_metrics(crawl_data)
                results['performance_analysis'] = performance
                st.success("✅ Analyzed website performance metrics")
            
            # Phase 4: Content & Structure Analysis
            with st.expander("📊 Content Structure Analysis", expanded=True):
                content_analysis = self._analyze_content_structure(crawl_data)
                results['content_analysis'] = content_analysis
                st.success("✅ Analyzed content structure and optimization")
            
            # Phase 5: URL Structure Optimization
            with st.expander("🔗 URL Structure Analysis", expanded=True):
                url_analysis = self._analyze_url_structure(crawl_data)
                results['url_structure'] = url_analysis
                st.success("✅ Analyzed URL structure and patterns")
            
            # Phase 6: Image SEO Analysis
            with st.expander("🖼️ Image SEO Analysis", expanded=True):
                image_analysis = self._analyze_image_seo(website_url)
                results['image_optimization'] = image_analysis
                st.success("✅ Analyzed image optimization")
            
            # Phase 7: Security & Headers Analysis
            with st.expander("🛡️ Security Headers Analysis", expanded=True):
                security_analysis = self._analyze_security_headers(website_url)
                results['security_headers'] = security_analysis
                st.success("✅ Analyzed security headers")
            
            # Phase 8: Mobile SEO Analysis
            with st.expander("📱 Mobile SEO Analysis", expanded=True):
                mobile_analysis = self._analyze_mobile_seo(crawl_data)
                results['mobile_seo'] = mobile_analysis
                st.success("✅ Analyzed mobile SEO factors")
            
            # Phase 9: AI-Powered Recommendations
            with st.expander("🤖 AI Technical Recommendations", expanded=True):
                ai_recommendations = self._generate_technical_recommendations(results)
                results['ai_recommendations'] = ai_recommendations
                st.success("✅ Generated AI-powered technical recommendations")
            
            return results
            
        except Exception as e:
            error_msg = f"Error in technical SEO analysis: {str(e)}"
            logger.error(error_msg, exc_info=True)
            st.error(error_msg)
            return {'error': error_msg}
    
    def _perform_comprehensive_crawl(self, website_url: str, depth: int, max_pages: int) -> Dict[str, Any]:
        """Perform comprehensive website crawl using adv.crawl."""
        try:
            st.info("🕷️ Crawling website for comprehensive analysis...")
            
            # Create crawl output file
            crawl_file = os.path.join(self.temp_dir, "technical_crawl.jl")
            
            # Configure crawl settings for technical SEO
            custom_settings = {
                'DEPTH_LIMIT': depth,
                'CLOSESPIDER_PAGECOUNT': max_pages,
                'DOWNLOAD_DELAY': 0.5,  # Be respectful
                'CONCURRENT_REQUESTS': 8,
                'ROBOTSTXT_OBEY': True,
                'USER_AGENT': 'ALwrity-TechnicalSEO-Crawler/1.0',
                'COOKIES_ENABLED': False,
                'TELNETCONSOLE_ENABLED': False,
                'LOG_LEVEL': 'WARNING'
            }
            
            # Start crawl
            adv.crawl(
                url_list=[website_url],
                output_file=crawl_file,
                follow_links=True,
                custom_settings=custom_settings
            )
            
            # Read and process crawl results
            if os.path.exists(crawl_file):
                crawl_df = pd.read_json(crawl_file, lines=True)
                
                # Basic crawl statistics
                crawl_overview = {
                    'pages_crawled': len(crawl_df),
                    'status_codes': crawl_df['status'].value_counts().to_dict(),
                    'crawl_file_path': crawl_file,
                    'crawl_dataframe': crawl_df,
                    'domains_found': crawl_df['url'].apply(lambda x: urlparse(x).netloc).nunique(),
                    'avg_response_time': crawl_df.get('download_latency', pd.Series()).mean(),
                    'total_content_size': crawl_df.get('size', pd.Series()).sum()
                }
                
                return crawl_overview
            else:
                st.error("Crawl file not created")
                return {}
                
        except Exception as e:
            st.error(f"Error in website crawl: {str(e)}")
            return {}
    
    def _analyze_technical_issues(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical SEO issues from crawl data."""
        try:
            st.info("🔍 Detecting technical SEO issues...")
            
            if 'crawl_dataframe' not in crawl_data:
                return {}
            
            df = crawl_data['crawl_dataframe']
            
            technical_issues = {
                'http_errors': {},
                'redirect_issues': {},
                'duplicate_content': {},
                'missing_elements': {},
                'page_speed_issues': {},
                'crawlability_issues': {}
            }
            
            # HTTP Status Code Issues
            error_codes = df[df['status'] >= 400]['status'].value_counts().to_dict()
            technical_issues['http_errors'] = {
                'total_errors': len(df[df['status'] >= 400]),
                'error_breakdown': error_codes,
                'error_pages': df[df['status'] >= 400][['url', 'status']].to_dict('records')[:50]
            }
            
            # Redirect Analysis
            redirects = df[df['status'].isin([301, 302, 303, 307, 308])]
            technical_issues['redirect_issues'] = {
                'total_redirects': len(redirects),
                'redirect_chains': self._find_redirect_chains(redirects),
                'redirect_types': redirects['status'].value_counts().to_dict()
            }
            
            # Duplicate Content Detection
            if 'title' in df.columns:
                duplicate_titles = df['title'].value_counts()
                duplicate_titles = duplicate_titles[duplicate_titles > 1]
                
                technical_issues['duplicate_content'] = {
                    'duplicate_titles': len(duplicate_titles),
                    'duplicate_title_groups': duplicate_titles.to_dict(),
                    'pages_with_duplicate_titles': df[df['title'].isin(duplicate_titles.index)][['url', 'title']].to_dict('records')[:20]
                }
            
            # Missing Elements Analysis
            missing_elements = {
                'missing_titles': len(df[(df['title'].isna()) | (df['title'] == '')]) if 'title' in df.columns else 0,
                'missing_meta_desc': len(df[(df['meta_desc'].isna()) | (df['meta_desc'] == '')]) if 'meta_desc' in df.columns else 0,
                'missing_h1': len(df[(df['h1'].isna()) | (df['h1'] == '')]) if 'h1' in df.columns else 0
            }
            technical_issues['missing_elements'] = missing_elements
            
            # Page Speed Issues
            if 'download_latency' in df.columns:
                slow_pages = df[df['download_latency'] > 3.0]  # Pages taking >3s
                technical_issues['page_speed_issues'] = {
                    'slow_pages_count': len(slow_pages),
                    'avg_load_time': df['download_latency'].mean(),
                    'slowest_pages': slow_pages.nlargest(10, 'download_latency')[['url', 'download_latency']].to_dict('records')
                }
            
            return technical_issues
            
        except Exception as e:
            st.error(f"Error analyzing technical issues: {str(e)}")
            return {}
    
    def _analyze_performance_metrics(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze website performance metrics."""
        try:
            st.info("⚡ Analyzing performance metrics...")
            
            if 'crawl_dataframe' not in crawl_data:
                return {}
            
            df = crawl_data['crawl_dataframe']
            
            performance = {
                'load_time_analysis': {},
                'content_size_analysis': {},
                'server_performance': {},
                'optimization_opportunities': []
            }
            
            # Load Time Analysis
            if 'download_latency' in df.columns:
                load_times = df['download_latency'].dropna()
                performance['load_time_analysis'] = {
                    'avg_load_time': load_times.mean(),
                    'median_load_time': load_times.median(),
                    'p95_load_time': load_times.quantile(0.95),
                    'fastest_page': load_times.min(),
                    'slowest_page': load_times.max(),
                    'pages_over_3s': len(load_times[load_times > 3]),
                    'performance_distribution': {
                        'fast_pages': len(load_times[load_times <= 1]),
                        'moderate_pages': len(load_times[(load_times > 1) & (load_times <= 3)]),
                        'slow_pages': len(load_times[load_times > 3])
                    }
                }
            
            # Content Size Analysis
            if 'size' in df.columns:
                sizes = df['size'].dropna()
                performance['content_size_analysis'] = {
                    'avg_page_size': sizes.mean(),
                    'median_page_size': sizes.median(),
                    'largest_page': sizes.max(),
                    'smallest_page': sizes.min(),
                    'pages_over_1mb': len(sizes[sizes > 1048576]),  # 1MB
                    'total_content_size': sizes.sum()
                }
            
            # Server Performance
            status_codes = df['status'].value_counts()
            total_pages = len(df)
            performance['server_performance'] = {
                'success_rate': status_codes.get(200, 0) / total_pages * 100,
                'error_rate': sum(status_codes.get(code, 0) for code in range(400, 600)) / total_pages * 100,
                'redirect_rate': sum(status_codes.get(code, 0) for code in [301, 302, 303, 307, 308]) / total_pages * 100
            }
            
            return performance
            
        except Exception as e:
            st.error(f"Error analyzing performance: {str(e)}")
            return {}
    
    def _analyze_content_structure(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content structure and SEO elements."""
        try:
            st.info("📊 Analyzing content structure...")
            
            if 'crawl_dataframe' not in crawl_data:
                return {}
            
            df = crawl_data['crawl_dataframe']
            
            content_analysis = {
                'title_analysis': {},
                'meta_description_analysis': {},
                'heading_structure': {},
                'internal_linking': {},
                'content_optimization': {}
            }
            
            # Title Analysis
            if 'title' in df.columns:
                titles = df['title'].dropna()
                title_lengths = titles.str.len()
                
                content_analysis['title_analysis'] = {
                    'avg_title_length': title_lengths.mean(),
                    'title_length_distribution': {
                        'too_short': len(title_lengths[title_lengths < 30]),
                        'optimal': len(title_lengths[(title_lengths >= 30) & (title_lengths <= 60)]),
                        'too_long': len(title_lengths[title_lengths > 60])
                    },
                    'duplicate_titles': len(titles.value_counts()[titles.value_counts() > 1]),
                    'missing_titles': len(df) - len(titles)
                }
            
            # Meta Description Analysis
            if 'meta_desc' in df.columns:
                meta_descs = df['meta_desc'].dropna()
                meta_lengths = meta_descs.str.len()
                
                content_analysis['meta_description_analysis'] = {
                    'avg_meta_length': meta_lengths.mean(),
                    'meta_length_distribution': {
                        'too_short': len(meta_lengths[meta_lengths < 120]),
                        'optimal': len(meta_lengths[(meta_lengths >= 120) & (meta_lengths <= 160)]),
                        'too_long': len(meta_lengths[meta_lengths > 160])
                    },
                    'missing_meta_descriptions': len(df) - len(meta_descs)
                }
            
            # Heading Structure Analysis
            heading_cols = [col for col in df.columns if col.startswith('h') and col[1:].isdigit()]
            if heading_cols:
                heading_analysis = {}
                for col in heading_cols:
                    headings = df[col].dropna()
                    heading_analysis[f'{col}_usage'] = {
                        'pages_with_heading': len(headings),
                        'usage_rate': len(headings) / len(df) * 100,
                        'avg_length': headings.str.len().mean() if len(headings) > 0 else 0
                    }
                content_analysis['heading_structure'] = heading_analysis
            
            # Internal Linking Analysis
            if 'links_internal' in df.columns:
                internal_links = df['links_internal'].apply(lambda x: len(x) if isinstance(x, list) else 0)
                content_analysis['internal_linking'] = {
                    'avg_internal_links': internal_links.mean(),
                    'pages_with_no_internal_links': len(internal_links[internal_links == 0]),
                    'max_internal_links': internal_links.max(),
                    'internal_link_distribution': internal_links.describe().to_dict()
                }
            
            return content_analysis
            
        except Exception as e:
            st.error(f"Error analyzing content structure: {str(e)}")
            return {}
    
    def _analyze_url_structure(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze URL structure and optimization using adv.url_to_df."""
        try:
            st.info("🔗 Analyzing URL structure...")
            
            if 'crawl_dataframe' not in crawl_data:
                return {}
            
            df = crawl_data['crawl_dataframe']
            urls = df['url'].tolist()
            
            # Use advertools to analyze URL structure
            url_df = adv.url_to_df(urls)
            
            url_analysis = {
                'url_length_analysis': {},
                'url_structure_patterns': {},
                'url_optimization': {},
                'path_analysis': {}
            }
            
            # URL Length Analysis
            url_lengths = url_df['url'].str.len()
            url_analysis['url_length_analysis'] = {
                'avg_url_length': url_lengths.mean(),
                'max_url_length': url_lengths.max(),
                'long_urls_count': len(url_lengths[url_lengths > 100]),
                'url_length_distribution': url_lengths.describe().to_dict()
            }
            
            # Path Depth Analysis
            if 'dir_1' in url_df.columns:
                path_depths = url_df.apply(lambda row: sum(1 for i in range(1, 10) if f'dir_{i}' in row and pd.notna(row[f'dir_{i}'])), axis=1)
                url_analysis['path_analysis'] = {
                    'avg_path_depth': path_depths.mean(),
                    'max_path_depth': path_depths.max(),
                    'deep_paths_count': len(path_depths[path_depths > 4]),
                    'path_depth_distribution': path_depths.value_counts().to_dict()
                }
            
            # URL Structure Patterns
            domains = url_df['netloc'].value_counts()
            schemes = url_df['scheme'].value_counts()
            
            url_analysis['url_structure_patterns'] = {
                'domains_found': domains.to_dict(),
                'schemes_used': schemes.to_dict(),
                'subdomain_usage': len(url_df[url_df['netloc'].str.contains('\.', regex=True)]),
                'https_usage': schemes.get('https', 0) / len(url_df) * 100
            }
            
            # URL Optimization Issues
            optimization_issues = []
            
            # Check for non-HTTPS URLs
            if schemes.get('http', 0) > 0:
                optimization_issues.append(f"{schemes.get('http', 0)} pages not using HTTPS")
            
            # Check for long URLs
            long_urls = len(url_lengths[url_lengths > 100])
            if long_urls > 0:
                optimization_issues.append(f"{long_urls} URLs are too long (>100 characters)")
            
            # Check for deep paths
            if 'path_analysis' in url_analysis:
                deep_paths = url_analysis['path_analysis']['deep_paths_count']
                if deep_paths > 0:
                    optimization_issues.append(f"{deep_paths} URLs have deep path structures (>4 levels)")
            
            url_analysis['url_optimization'] = {
                'issues_found': len(optimization_issues),
                'optimization_recommendations': optimization_issues
            }
            
            return url_analysis
            
        except Exception as e:
            st.error(f"Error analyzing URL structure: {str(e)}")
            return {}
    
    def _analyze_image_seo(self, website_url: str) -> Dict[str, Any]:
        """Analyze image SEO using adv.crawl_images."""
        try:
            st.info("🖼️ Analyzing image SEO...")
            
            # Create image crawl output file
            image_file = os.path.join(self.temp_dir, "image_crawl.jl")
            
            # Crawl images
            adv.crawl_images(
                url_list=[website_url],
                output_file=image_file,
                custom_settings={
                    'DEPTH_LIMIT': 2,
                    'CLOSESPIDER_PAGECOUNT': 100,
                    'DOWNLOAD_DELAY': 1
                }
            )
            
            image_analysis = {
                'image_count': 0,
                'alt_text_analysis': {},
                'image_format_analysis': {},
                'image_size_analysis': {},
                'optimization_opportunities': []
            }
            
            if os.path.exists(image_file):
                image_df = pd.read_json(image_file, lines=True)
                
                image_analysis['image_count'] = len(image_df)
                
                # Alt text analysis
                if 'img_alt' in image_df.columns:
                    alt_texts = image_df['img_alt'].dropna()
                    missing_alt = len(image_df) - len(alt_texts)
                    
                    image_analysis['alt_text_analysis'] = {
                        'images_with_alt': len(alt_texts),
                        'images_missing_alt': missing_alt,
                        'alt_text_coverage': len(alt_texts) / len(image_df) * 100,
                        'avg_alt_length': alt_texts.str.len().mean() if len(alt_texts) > 0 else 0
                    }
                
                # Image format analysis
                if 'img_src' in image_df.columns:
                    # Extract file extensions
                    extensions = image_df['img_src'].str.extract(r'\.([a-zA-Z]{2,4})(?:\?|$)')
                    format_counts = extensions[0].value_counts()
                    
                    image_analysis['image_format_analysis'] = {
                        'format_distribution': format_counts.to_dict(),
                        'modern_format_usage': format_counts.get('webp', 0) + format_counts.get('avif', 0)
                    }
            
            return image_analysis
            
        except Exception as e:
            st.error(f"Error analyzing images: {str(e)}")
            return {}
    
    def _analyze_security_headers(self, website_url: str) -> Dict[str, Any]:
        """Analyze security headers using adv.crawl_headers."""
        try:
            st.info("🛡️ Analyzing security headers...")
            
            # Create headers output file
            headers_file = os.path.join(self.temp_dir, "security_headers.jl")
            
            # Crawl headers
            adv.crawl_headers([website_url], output_file=headers_file)
            
            security_analysis = {
                'security_headers_present': {},
                'security_score': 0,
                'security_recommendations': []
            }
            
            if os.path.exists(headers_file):
                headers_df = pd.read_json(headers_file, lines=True)
                
                # Check for important security headers
                security_headers = {
                    'X-Frame-Options': 'resp_headers_X-Frame-Options',
                    'X-Content-Type-Options': 'resp_headers_X-Content-Type-Options',
                    'X-XSS-Protection': 'resp_headers_X-XSS-Protection',
                    'Strict-Transport-Security': 'resp_headers_Strict-Transport-Security',
                    'Content-Security-Policy': 'resp_headers_Content-Security-Policy',
                    'Referrer-Policy': 'resp_headers_Referrer-Policy'
                }
                
                headers_present = {}
                for header_name, column_name in security_headers.items():
                    is_present = column_name in headers_df.columns and headers_df[column_name].notna().any()
                    headers_present[header_name] = is_present
                
                security_analysis['security_headers_present'] = headers_present
                
                # Calculate security score
                present_count = sum(headers_present.values())
                security_analysis['security_score'] = (present_count / len(security_headers)) * 100
                
                # Generate recommendations
                recommendations = []
                for header_name, is_present in headers_present.items():
                    if not is_present:
                        recommendations.append(f"Add {header_name} header for improved security")
                
                security_analysis['security_recommendations'] = recommendations
            
            return security_analysis
            
        except Exception as e:
            st.error(f"Error analyzing security headers: {str(e)}")
            return {}
    
    def _analyze_mobile_seo(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mobile SEO factors."""
        try:
            st.info("📱 Analyzing mobile SEO factors...")
            
            if 'crawl_dataframe' not in crawl_data:
                return {}
            
            df = crawl_data['crawl_dataframe']
            
            mobile_analysis = {
                'viewport_analysis': {},
                'mobile_optimization': {},
                'responsive_design_indicators': {}
            }
            
            # Viewport meta tag analysis
            if 'viewport' in df.columns:
                viewport_present = df['viewport'].notna().sum()
                mobile_analysis['viewport_analysis'] = {
                    'pages_with_viewport': viewport_present,
                    'viewport_coverage': viewport_present / len(df) * 100,
                    'pages_missing_viewport': len(df) - viewport_present
                }
            
            # Check for mobile-specific meta tags and indicators
            mobile_indicators = []
            
            # Check for touch icons
            if any('touch-icon' in col for col in df.columns):
                mobile_indicators.append("Touch icons configured")
            
            # Check for responsive design indicators in content
            # This is a simplified check - in practice, you'd analyze CSS and page structure
            mobile_analysis['mobile_optimization'] = {
                'mobile_indicators_found': len(mobile_indicators),
                'mobile_indicators': mobile_indicators
            }
            
            return mobile_analysis
            
        except Exception as e:
            st.error(f"Error analyzing mobile SEO: {str(e)}")
            return {}
    
    def _generate_technical_recommendations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered technical SEO recommendations."""
        try:
            st.info("🤖 Generating technical recommendations...")
            
            # Prepare technical analysis summary for AI
            technical_summary = {
                'website_url': results.get('website_url', ''),
                'pages_crawled': results.get('crawl_overview', {}).get('pages_crawled', 0),
                'error_count': results.get('technical_issues', {}).get('http_errors', {}).get('total_errors', 0),
                'avg_load_time': results.get('performance_analysis', {}).get('load_time_analysis', {}).get('avg_load_time', 0),
                'security_score': results.get('security_headers', {}).get('security_score', 0),
                'missing_titles': results.get('content_analysis', {}).get('title_analysis', {}).get('missing_titles', 0),
                'missing_meta_desc': results.get('content_analysis', {}).get('meta_description_analysis', {}).get('missing_meta_descriptions', 0)
            }
            
            # Generate AI recommendations
            prompt = f"""
            As a technical SEO expert, analyze this comprehensive website audit and provide prioritized recommendations:

            WEBSITE: {technical_summary['website_url']}
            PAGES ANALYZED: {technical_summary['pages_crawled']}
            
            TECHNICAL ISSUES:
            - HTTP Errors: {technical_summary['error_count']}
            - Average Load Time: {technical_summary['avg_load_time']:.2f}s
            - Security Score: {technical_summary['security_score']:.1f}%
            - Missing Titles: {technical_summary['missing_titles']}
            - Missing Meta Descriptions: {technical_summary['missing_meta_desc']}

            PROVIDE:
            1. Critical Issues (Fix Immediately)
            2. High Priority Optimizations
            3. Medium Priority Improvements
            4. Long-term Technical Strategy
            5. Specific Implementation Steps
            6. Expected Impact Assessment

            Format as JSON with clear priorities and actionable recommendations.
            """
            
            ai_response = llm_text_gen(
                prompt=prompt,
                system_prompt="You are a senior technical SEO specialist with expertise in website optimization, Core Web Vitals, and search engine best practices.",
                response_format="json_object"
            )
            
            if ai_response:
                return ai_response
            else:
                return {'recommendations': ['AI recommendations temporarily unavailable']}
                
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return {}
    
    def _find_redirect_chains(self, redirects_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Find redirect chains in the crawled data."""
        # Simplified redirect chain detection
        # In a full implementation, you'd trace the redirect paths
        redirect_chains = []
        
        if len(redirects_df) > 0:
            # Group redirects by status code
            for status_code in redirects_df['status'].unique():
                status_redirects = redirects_df[redirects_df['status'] == status_code]
                redirect_chains.append({
                    'status_code': int(status_code),
                    'count': len(status_redirects),
                    'examples': status_redirects['url'].head(5).tolist()
                })
        
        return redirect_chains 