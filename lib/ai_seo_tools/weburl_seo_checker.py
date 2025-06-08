import streamlit as st
import advertools as adv
import pandas as pd
from urllib.parse import urlparse
import requests
from datetime import datetime
import tempfile
import os


# Title and introduction
def show_title_and_intro():
    st.title("🌟 URL SEO Checkup: Your Link's Health Report 🌟")
    st.write("""
        Welcome to the URL SEO Checkup! This tool is like a doctor for your website links. 
        Just paste your URL, and we'll check if it's healthy and ready to climb the search engine ladder.
    """)


# Basic HTTPS Check
def check_https(url):
    st.subheader("The Basics - Are We Looking Good?")
    st.write("---")
    
    if url.startswith("https://"):
        st.success("✨ You're using HTTPS! This adds extra security, and Google rewards that with better rankings. Keep it up! ✨")
    else:
        st.warning("🚧 Heads Up! Your URL doesn't use 'https://'. This is a red flag for Google.")
        st.info("🔧 **How to fix:** Contact your hosting provider or website developer to install an SSL certificate. This will secure your site with HTTPS.")


# URL Length Check
def check_url_length(path):
    st.subheader("The Length Test - Keep it Short and Sweet!")
    st.write("---")
    
    if len(path) <= 50:
        st.success("🏆 Great! Your URL is short and user-friendly. Google loves short URLs! 🏆")
    else:
        st.warning("🧭 Tip: Try shortening your URL. Shorter URLs are easier to remember and better for SEO.")
        st.info("🔧 **How to fix:** Consider removing unnecessary words or folders in the URL. Aim for concise, descriptive URLs that are easy for users to read.")


# Hyphen Check
def check_hyphens(path):
    st.subheader("The Hyphen Check - Use Hyphens for Clear Separation!")
    st.write("---")
    
    if "-" in path:
        st.success("😎 You're on the right track! Using hyphens makes your URL more readable for both users and Google. 😎")
    else:
        st.warning("❓ Did you know? Using hyphens between words (like 'shoes-for-sale') helps Google understand your URL better!")
        st.info("🔧 **How to fix:** Update your URL to use hyphens (-) instead of spaces or underscores (_). For example, 'shoes-for-sale' instead of 'shoes_for_sale'.")


# File Extension Check
def check_file_extension(path):
    st.subheader("File Extension Check - Showing Your Files With Pride!")
    st.write("---")
    
    if "." in path:
        st.success("🥳 File Extension Check: Your URL includes a file extension like '.html', which helps Google categorize your page. Nice job! 🥳")
    else:
        st.warning("🤔 Your URL seems to be missing a file extension like '.html' or '.php'.")
        st.info("🔧 **How to fix:** While file extensions are not always required, adding them to static pages (like .html or .php) can improve clarity for search engines.")


# Keyword Insights
def show_keyword_insights(netloc, path):
    st.subheader("Bonus Insight - Let's Talk Keywords")
    st.write("---")
    
    st.info("Keywords are the words people use to search for information online. Your goal is to help Google understand what your page is about by using the right keywords in your URL!")
    
    st.markdown(f"""
        **Your Domain:** {netloc}  
        **Your URL Path:** {path}
        
        **Suggestion:** Consider adding a primary keyword to your URL if it aligns with your page content. But don't overdo it – too many keywords can hurt your SEO. Keep it natural!
    """)


# Enhanced HTTP Headers Analysis using advertools
def analyze_http_headers(url):
    """Analyze HTTP headers using advertools for comprehensive SEO insights."""
    st.subheader("🔍 Advanced HTTP Headers Analysis")
    st.write("---")
    
    try:
        with st.spinner("Analyzing HTTP headers..."):
            # Create a temporary file for output
            with tempfile.NamedTemporaryFile(mode='w', suffix='.jl', delete=False) as tmp_file:
                temp_filename = tmp_file.name
            
            # Use advertools to crawl headers
            adv.crawl_headers([url], temp_filename)
            
            # Read the results
            headers_df = pd.read_json(temp_filename, lines=True)
            
            # Clean up temp file
            os.unlink(temp_filename)
        
        if not headers_df.empty:
            # Display key SEO-relevant headers
            st.success("✅ Successfully analyzed HTTP headers!")
            
            # Create tabs for different header categories
            tab1, tab2, tab3, tab4 = st.tabs(["🔒 Security", "📈 SEO Headers", "⚡ Performance", "📊 Technical Details"])
            
            with tab1:
                st.write("### Security Headers Analysis")
                security_headers = {
                    'resp_headers_X-Frame-Options': 'X-Frame-Options',
                    'resp_headers_X-Content-Type-Options': 'X-Content-Type-Options',
                    'resp_headers_X-XSS-Protection': 'X-XSS-Protection',
                    'resp_headers_Strict-Transport-Security': 'Strict-Transport-Security',
                    'resp_headers_Content-Security-Policy': 'Content-Security-Policy',
                    'resp_headers_Referrer-Policy': 'Referrer-Policy'
                }
                
                for header_key, header_name in security_headers.items():
                    if header_key in headers_df.columns and not pd.isna(headers_df[header_key].iloc[0]):
                        st.success(f"✅ **{header_name}**: Present")
                        with st.expander(f"View {header_name} Details"):
                            st.code(headers_df[header_key].iloc[0])
                    else:
                        st.warning(f"⚠️ **{header_name}**: Missing")
                        st.info(f"💡 **Recommendation**: Add {header_name} header for better security")
            
            with tab2:
                st.write("### SEO-Related Headers")
                seo_headers = {
                    'resp_headers_Content-Type': 'Content-Type',
                    'resp_headers_Content-Language': 'Content-Language',
                    'resp_headers_Cache-Control': 'Cache-Control',
                    'resp_headers_Expires': 'Expires',
                    'resp_headers_Last-Modified': 'Last-Modified',
                    'resp_headers_ETag': 'ETag'
                }
                
                for header_key, header_name in seo_headers.items():
                    if header_key in headers_df.columns and not pd.isna(headers_df[header_key].iloc[0]):
                        st.success(f"✅ **{header_name}**: {headers_df[header_key].iloc[0]}")
                    else:
                        st.info(f"ℹ️ **{header_name}**: Not set or not detected")
                
                # Special handling for content-type
                if 'resp_headers_Content-Type' in headers_df.columns:
                    content_type = headers_df['resp_headers_Content-Type'].iloc[0]
                    if 'text/html' in str(content_type):
                        st.success("🎯 **Content-Type**: Properly set for HTML content")
                    if 'charset=utf-8' in str(content_type):
                        st.success("🌍 **Character Encoding**: UTF-8 detected - Great for international SEO!")
            
            with tab3:
                st.write("### Performance Headers")
                perf_headers = {
                    'resp_headers_Server': 'Server',
                    'resp_headers_X-Powered-By': 'X-Powered-By',
                    'resp_headers_Connection': 'Connection',
                    'resp_headers_Transfer-Encoding': 'Transfer-Encoding',
                    'resp_headers_Content-Encoding': 'Content-Encoding',
                    'resp_headers_Content-Length': 'Content-Length'
                }
                
                for header_key, header_name in perf_headers.items():
                    if header_key in headers_df.columns and not pd.isna(headers_df[header_key].iloc[0]):
                        st.info(f"📊 **{header_name}**: {headers_df[header_key].iloc[0]}")
                
                # Check for compression
                if 'resp_headers_Content-Encoding' in headers_df.columns:
                    encoding = headers_df['resp_headers_Content-Encoding'].iloc[0]
                    if 'gzip' in str(encoding) or 'br' in str(encoding):
                        st.success("🚀 **Compression**: Enabled - Great for page speed!")
                    else:
                        st.warning("⚠️ **Compression**: Consider enabling GZIP or Brotli compression")
                else:
                    st.warning("⚠️ **Compression**: Not detected - Consider enabling compression")
                
                # Check status code
                if 'status' in headers_df.columns:
                    status = headers_df['status'].iloc[0]
                    if status == 200:
                        st.success(f"✅ **HTTP Status**: {status} OK")
                    else:
                        st.warning(f"⚠️ **HTTP Status**: {status}")
            
            with tab4:
                st.write("### Complete Headers Analysis")
                
                # Show response headers only (more relevant for SEO)
                response_headers = {col: col.replace('resp_headers_', '') for col in headers_df.columns if col.startswith('resp_headers_')}
                if response_headers:
                    st.write("**Response Headers:**")
                    for col, display_name in response_headers.items():
                        if not pd.isna(headers_df[col].iloc[0]):
                            st.write(f"**{display_name}**: `{headers_df[col].iloc[0]}`")
                
                # Show crawl metadata
                st.write("**Crawl Information:**")
                metadata_cols = ['url', 'status', 'crawl_time', 'download_latency']
                for col in metadata_cols:
                    if col in headers_df.columns:
                        st.write(f"**{col.replace('_', ' ').title()}**: `{headers_df[col].iloc[0]}`")
                
                # Download option
                csv = headers_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Complete Headers Data as CSV",
                    data=csv,
                    file_name=f"headers_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        else:
            st.error("❌ Could not retrieve headers data")
            
    except Exception as e:
        st.error(f"❌ Error analyzing headers: {str(e)}")
        st.info("💡 **Tip**: Make sure the URL is accessible and try again")


# Enhanced robots.txt and sitemap detection
def check_robots_and_sitemap(url):
    """Check for robots.txt and sitemap files."""
    st.subheader("🤖 Robots.txt & Sitemap Detection")
    st.write("---")
    
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Check robots.txt
    try:
        robots_url = f"{base_url}/robots.txt"
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            st.success(f"✅ **Robots.txt found**: {robots_url}")
            with st.expander("View robots.txt content"):
                st.code(response.text[:1000])  # Show first 1000 characters
        else:
            st.warning(f"⚠️ **Robots.txt not found**: Consider creating one at {robots_url}")
    except:
        st.error("❌ Could not check robots.txt")
    
    # Check common sitemap locations
    sitemap_locations = [
        f"{base_url}/sitemap.xml",
        f"{base_url}/sitemap_index.xml",
        f"{base_url}/sitemaps.xml"
    ]
    
    sitemap_found = False
    for sitemap_url in sitemap_locations:
        try:
            response = requests.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                st.success(f"✅ **Sitemap found**: {sitemap_url}")
                sitemap_found = True
                break
        except:
            continue
    
    if not sitemap_found:
        st.warning("⚠️ **Sitemap not found**: Consider creating an XML sitemap")
        st.info("💡 **Recommendation**: Submit your sitemap to Google Search Console")


# Enhanced URL structure analysis
def enhanced_url_analysis(url):
    """Provide enhanced URL structure analysis."""
    st.subheader("🔗 Enhanced URL Structure Analysis")
    st.write("---")
    
    parsed_url = urlparse(url)
    
    # URL components analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**URL Components:**")
        st.info(f"**Protocol**: {parsed_url.scheme}")
        st.info(f"**Domain**: {parsed_url.netloc}")
        st.info(f"**Path**: {parsed_url.path}")
        if parsed_url.query:
            st.info(f"**Query**: {parsed_url.query}")
        if parsed_url.fragment:
            st.info(f"**Fragment**: {parsed_url.fragment}")
    
    with col2:
        st.write("**SEO Analysis:**")
        
        # URL length analysis
        url_length = len(url)
        if url_length <= 60:
            st.success(f"✅ **URL Length**: {url_length} characters (Excellent)")
        elif url_length <= 100:
            st.warning(f"⚠️ **URL Length**: {url_length} characters (Good, but could be shorter)")
        else:
            st.error(f"❌ **URL Length**: {url_length} characters (Too long)")
        
        # Path depth analysis
        path_segments = [seg for seg in parsed_url.path.split('/') if seg]
        depth = len(path_segments)
        if depth <= 3:
            st.success(f"✅ **URL Depth**: {depth} levels (Good)")
        else:
            st.warning(f"⚠️ **URL Depth**: {depth} levels (Consider flattening)")
        
        # Special characters check
        special_chars = set(url) - set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~:/?#[]@!$&\'()*+,;=')
        if not special_chars:
            st.success("✅ **Special Characters**: Clean URL structure")
        else:
            st.warning(f"⚠️ **Special Characters**: Found {len(special_chars)} special characters")


# Enhanced main function to run the analysis
def run_analysis(url):
    # Parse the URL
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc  # Domain name
    path = parsed_url.path  # Path after the domain

    # Run existing checks
    check_https(url)
    check_url_length(path)
    check_hyphens(path)
    check_file_extension(path)
    
    # Add new enhanced analyses
    enhanced_url_analysis(url)
    analyze_http_headers(url)
    check_robots_and_sitemap(url)
    
    # Keep existing keyword insights
    show_keyword_insights(netloc, path)
    
    # Add summary section
    st.subheader("📋 Analysis Summary & Recommendations")
    st.write("---")
    st.success("🎉 **Analysis Complete!** Review the findings above and implement the recommendations for better SEO performance.")
    
    recommendations = [
        "✅ Ensure HTTPS is enabled for security and SEO benefits",
        "🔗 Keep URLs short, descriptive, and user-friendly",
        "🔒 Implement security headers to protect your site",
        "🤖 Create and maintain robots.txt and XML sitemaps",
        "⚡ Enable compression and optimize HTTP headers for performance",
        "📊 Monitor your URL structure and avoid excessive depth"
    ]
    
    st.write("**Key Recommendations:**")
    for rec in recommendations:
        st.write(rec)


# Display the app
def url_seo_checker():
    show_title_and_intro()

    # User input for URL
    url_input = st.text_input("Paste your URL here:", "https://www.example.com/")
    st.write(" ")  # Add spacing

    # When the analyze button is clicked
    if st.button("Let's Analyze!"):
        with st.spinner('Checking your link...'):
            url = url_input.strip()  # Clean up the input

            # Validate URL format
            if not url.startswith(("http://", "https://")):
                st.error("Oops! It seems like your URL needs 'http://' or 'https://' at the beginning. Please add it!")
                st.stop()

            # Run the analysis
            run_analysis(url)
