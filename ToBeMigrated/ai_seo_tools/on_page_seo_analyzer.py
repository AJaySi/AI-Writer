import os
import json
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential
import crawl4ai
from bs4 import BeautifulSoup
import requests
import csv
import time
from urllib.parse import urlparse, urljoin
import validators
import readability
import textstat
import re
from PIL import Image
import io
import advertools as adv
import pandas as pd
from collections import Counter
from ..gpt_providers.text_generation.main_text_generation import llm_text_gen

def fetch_and_parse_html(url):
    """
    Fetches HTML content from the given URL using crawl4ai and parses it with BeautifulSoup.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        BeautifulSoup: Parsed HTML content.
    """
    try:
        html = crawl4ai.get(url)
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except Exception as e:
        st.error(f"⚠️ Error fetching or parsing HTML: {e}")
        return None

def extract_meta_data(soup):
    """
    Extracts meta data like title, description, and robots directives from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Extracted meta data.
    """
    try:
        metatitle = soup.find('title').get_text() if soup.find('title') else "Title not found"
        metadescription = soup.find('meta', attrs={'name': 'description'})["content"] if soup.find('meta', attrs={'name': 'description'}) else "Description not found"
        robots_directives = [directive.strip() for directive in soup.find('meta', attrs={'name': 'robots'})["content"].split(",")] if soup.find('meta', attrs={'name': 'robots'}) else []
        viewport = soup.find('meta', attrs={'name': 'viewport'})["content"] if soup.find('meta', attrs={'name': 'viewport'}) else "Viewport not found"
        charset = soup.find('meta', attrs={'charset': True})["charset"] if soup.find('meta', attrs={'charset': True}) else "Charset not found"
        html_language = soup.find('html')["lang"] if soup.find('html') else "Language not found"
        
        title_length = len(metatitle) if metatitle != "Title not found" else 0
        description_length = len(metadescription) if metadescription != "Description not found" else 0
        title_message = "✅ Title length is good." if 30 <= title_length <= 60 else "⚠️ Title length should be between 30-60 characters."
        description_message = "✅ Meta description length is good." if 70 <= description_length <= 160 else "⚠️ Meta description should be between 70-160 characters."
        
        return {
            "metatitle": metatitle,
            "metadescription": metadescription,
            "robots_directives": robots_directives,
            "viewport": viewport,
            "charset": charset,
            "html_language": html_language,
            "title_message": title_message,
            "description_message": description_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error extracting meta data: {e}")
        return {}

def analyze_headings(soup):
    """
    Analyzes the headings on the webpage.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Count of each heading tag.
    """
    try:
        headings = {
            'h1': len(soup.find_all('h1')),
            'h2': len(soup.find_all('h2')),
            'h3': len(soup.find_all('h3')),
            'h4': len(soup.find_all('h4')),
            'h5': len(soup.find_all('h5')),
            'h6': len(soup.find_all('h6'))
        }
        return headings
    except Exception as e:
        st.warning(f"⚠️ Error analyzing headings: {e}")
        return {}

def check_readability(text):
    """
    Checks the readability score of the text.

    Args:
        text (str): The text content of the webpage.

    Returns:
        float: Readability score.
    """
    try:
        readability_score = textstat.flesch_reading_ease(text)
        return readability_score
    except Exception as e:
        st.warning(f"⚠️ Error checking readability: {e}")
        return None

def analyze_images(soup, url):
    """
    Analyzes the images on the webpage.

    Args:
        soup (BeautifulSoup): Parsed HTML content.
        url (str): The URL of the webpage.

    Returns:
        list: List of dictionaries containing image src and alt text.
    """
    try:
        images = soup.find_all('img')
        image_data = []
        for img in images:
            src = img.get('src')
            if not src:
                continue
            if not validators.url(src):
                src = urlparse(url).scheme + '://' + urlparse(url).netloc + src
            alt_text = img.get('alt', '')
            image_data.append({'src': src, 'alt': alt_text})
        return image_data
    except Exception as e:
        st.warning(f"⚠️ Error analyzing images: {e}")
        return []

def analyze_links(soup):
    """
    Analyzes the links on the webpage.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        list: List of broken links.
    """
    try:
        links = soup.find_all('a', href=True)
        broken_links = []
        for link in links:
            href = link['href']
            if not validators.url(href):
                continue
            try:
                response = requests.head(href, timeout=5, allow_redirects=True)
                if response.status_code >= 400:
                    broken_links.append(href)
            except requests.RequestException as e:
                # Log the exception for debugging purposes
                print(f"Error checking link {href}: {e}")
                broken_links.append(href)
        return broken_links
    except Exception as e:
        st.warning(f"⚠️ Error analyzing links: {e}")
        return []

def suggest_ctas(soup):
    """
    Suggests call-to-action phrases present on the webpage.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        list: List of found CTA phrases.
    """
    try:
        cta_keywords = ['buy now', 'subscribe', 'learn more', 'sign up', 'get started']
        text = soup.get_text().lower()
        ctas_found = [cta for cta in cta_keywords if cta in text]
        return ctas_found
    except Exception as e:
        st.warning(f"⚠️ Error suggesting CTAs: {e}")
        return []

def extract_alternates_and_canonicals(soup):
    """
    Extracts canonical URL, hreflangs, and mobile alternate links from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Extracted alternates and canonicals.
    """
    try:
        canonical = soup.find('link', attrs={'rel': 'canonical'})["href"] if soup.find('link', attrs={'rel': 'canonical'}) else "Canonical not found"
        list_hreflangs = [[a['href'], a["hreflang"]] for a in soup.find_all('link', href=True, hreflang=True)] if soup.find_all('link', href=True, hreflang=True) else []
        mobile_alternate = soup.find('link', attrs={'media': 'only screen and (max-width: 640px)'})["href"] if soup.find('link', attrs={'media': 'only screen and (max-width: 640px)'}) else "Mobile Alternate not found"
        
        canonical_message = "✅ Canonical tag found. Great! This helps avoid duplicate content issues." if canonical != "Canonical not found" else "⚠️ Consider adding a canonical tag."
        hreflangs_message = "✅ Hreflang tags are implemented. Good job!" if list_hreflangs else "⚠️ Consider implementing hreflang tags."
        
        return {
            "canonical": canonical,
            "hreflangs": list_hreflangs,
            "mobile_alternate": mobile_alternate,
            "canonical_message": canonical_message,
            "hreflangs_message": hreflangs_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error extracting alternates and canonicals: {e}")
        return {}

def extract_schema_markup(soup):
    """
    Extracts schema markup data from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Extracted schema markup data.
    """
    try:
        json_schema = soup.find('script', attrs={'type': 'application/ld+json'})
        if json_schema:
            json_file = json.loads(json_schema.get_text())
            schema_types = [x['@type'] for x in json_file.get("@graph", [])] if "@graph" in json_file else [json_file["@type"]]
            schema_message = "✅ Schema markup found. Wonderful!" if schema_types else "⚠️ No schema markup found."
            return {
                "schema_types": schema_types,
                "schema_message": schema_message
            }
        else:
            return {
                "schema_message": "⚠️ No schema markup found."
            }
    except Exception as e:
        st.warning(f"⚠️ Error extracting schema markup: {e}")
        return {}

def extract_content_data(soup, url):
    """
    Extracts content data such as text length, headers, and insights about images and links.

    Args:
        soup (BeautifulSoup): Parsed HTML content.
        url (str): The URL of the webpage.

    Returns:
        dict: Extracted content data.
    """
    try:
        paragraph = [a.get_text() for a in soup.find_all('p')]
        text_length = sum([len(a) for a in paragraph])
        h1 = [a.get_text() for a in soup.find_all('h1')]
        headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        list_headers = [[str(x)[1:3], x.get_text()] for x in headers]
        
        images = []
        for img in soup.find_all('img'):
            src = img.get("src", "No src attribute")
            alt_text = img.get("alt", "No alt text")
            images.append([src, alt_text])
        
        internal_links = []
        external_links = []
        domain = url.split("//")[-1].split("/")[0]
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if domain in href:
                internal_links.append(href)
            else:
                external_links.append(href)
        
        content_message = "✅ Content length is adequate." if text_length > 300 else "⚠️ Consider adding more content (minimum 300 words)."
        h1_message = "✅ H1 tag found. Good!" if h1 else "⚠️ Missing H1 tag."
        missing_alt_texts = sum([1 for img in images if img[1] == "No alt text"])
        alt_text_message = "✅ All images have alt text. Great!" if missing_alt_texts == 0 else f"⚠️ {missing_alt_texts} images are missing alt text."
        internal_links_message = f"✅ {len(internal_links)} internal links found."
        external_links_message = f"✅ {len(external_links)} external links found."

        link_insights = []
        if internal_links:
            link_insights.append("✅ Internal links are present.")
        if external_links:
            link_insights.append("✅ External links are present.")

        return {
            "text_length": text_length,
            "headers": list_headers,
            "images": images,
            "h1_message": h1_message,
            "content_message": content_message,
            "alt_text_message": alt_text_message,
            "internal_links_message": internal_links_message,
            "external_links_message": external_links_message,
            "link_insights": link_insights
        }
    except Exception as e:
        st.warning(f"⚠️ Error extracting content data: {e}")
        return {}

def extract_open_graph(soup):
    """
    Extracts Open Graph data from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Extracted Open Graph data.
    """
    try:
        open_graph = [[a["property"].replace("og:", ""), a["content"]] for a in soup.select("meta[property^=og]")]
        open_graph_message = "✅ Open Graph tags found. Awesome!" if open_graph else "⚠️ No Open Graph tags found."
        return {
            "open_graph": open_graph,
            "open_graph_message": open_graph_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error extracting Open Graph data: {e}")
        return {}

def extract_social_tags(soup):
    """
    Extracts Twitter Card and Facebook Open Graph data from the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Extracted social tags.
    """
    try:
        twitter_cards = [[a["name"].replace("twitter:", ""), a["content"]] for a in soup.select("meta[name^=twitter]")]
        facebook_open_graph = [[a["property"].replace("og:", ""), a["content"]] for a in soup.select("meta[property^=og]")]
        
        twitter_message = "✅ Twitter Card tags found." if twitter_cards else "⚠️ No Twitter Card tags found."
        facebook_message = "✅ Facebook Open Graph tags found." if facebook_open_graph else "⚠️ No Facebook Open Graph tags found."
        
        return {
            "twitter_cards": twitter_cards,
            "facebook_open_graph": facebook_open_graph,
            "twitter_message": twitter_message,
            "facebook_message": facebook_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error extracting social tags: {e}")
        return {}

def check_page_speed(url):
    """
    Fetches and analyzes page speed metrics using Google PageSpeed Insights API.

    Args:
        url (str): The URL of the webpage.

    Returns:
        dict: Page speed data.
    """
    try:
        api_key = "YOUR_GOOGLE_PAGESPEED_API_KEY"
        response = requests.get(f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}")
        data = response.json()
        score = data.get('overall_category_score', 'N/A')
        speed_message = f"Page Speed Score: {score}" if score != 'N/A' else "⚠️ Unable to retrieve page speed score."
        return {
            "speed_score": score,
            "speed_message": speed_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error fetching page speed data: {e}")
        return {}

def check_mobile_usability(soup):
    """
    Checks if the website is mobile-friendly based on viewport and other elements.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Mobile usability data.
    """
    try:
        viewport = soup.find('meta', attrs={'name': 'viewport'})["content"] if soup.find('meta', attrs={'name': 'viewport'}) else ""
        mobile_message = "✅ Mobile viewport is set." if viewport else "⚠️ Mobile viewport meta tag is missing."
        return {
            "mobile_message": mobile_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error checking mobile usability: {e}")
        return {}

def check_alt_text(soup):
    """
    Checks if all images have alt text.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        dict: Alt text data.
    """
    try:
        images = soup.find_all('img')
        missing_alt_texts = sum([1 for img in images if not img.get("alt")])
        alt_text_message = "✅ All images have alt text. Great!" if missing_alt_texts == 0 else f"⚠️ {missing_alt_texts} images are missing alt text."
        return {
            "alt_text_message": alt_text_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error checking alt text: {e}")
        return {}

def analyze_keyword_density(text, url=None):
    """
    Analyze keyword density and word frequency using advertools for comprehensive SEO insights.
    
    Args:
        text (str): The main content text from the webpage
        url (str): Optional URL for additional context
    
    Returns:
        dict: Comprehensive keyword density analysis
    """
    try:
        # Use advertools word_frequency for professional analysis
        word_freq_df = adv.word_frequency(text)
        
        if word_freq_df.empty:
            return {
                "word_frequency": [],
                "keyword_density": {},
                "top_keywords": [],
                "analysis_message": "⚠️ Unable to analyze content - no words found",
                "recommendations": []
            }
        
        # Get top 20 most frequent words (excluding very common words)
        # Filter out common stopwords and very short words
        common_stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'a', 'an', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        # Filter and process the word frequency data
        filtered_words = []
        total_words = len(text.split())
        
        for idx, row in word_freq_df.iterrows():
            word = row['word'].lower().strip()
            count = row['abs_freq']
            
            # Filter criteria
            if (len(word) >= 3 and 
                word not in common_stopwords and 
                word.isalpha() and 
                count >= 2):  # Minimum frequency of 2
                
                density = (count / total_words) * 100
                filtered_words.append({
                    'word': word,
                    'count': count,
                    'density': round(density, 2)
                })
        
        # Sort by frequency and take top 15
        top_keywords = sorted(filtered_words, key=lambda x: x['count'], reverse=True)[:15]
        
        # Calculate keyword density categories
        keyword_density = {
            'high_density': [kw for kw in top_keywords if kw['density'] > 3],
            'medium_density': [kw for kw in top_keywords if 1 <= kw['density'] <= 3],
            'low_density': [kw for kw in top_keywords if kw['density'] < 1]
        }
        
        # Generate analysis messages and recommendations
        analysis_messages = []
        recommendations = []
        
        if len(top_keywords) == 0:
            analysis_messages.append("⚠️ No significant keywords found in content")
            recommendations.append("Add more descriptive and relevant keywords to your content")
        else:
            analysis_messages.append(f"✅ Found {len(top_keywords)} significant keywords")
            
            # Check for keyword stuffing
            if keyword_density['high_density']:
                high_density_words = [kw['word'] for kw in keyword_density['high_density']]
                analysis_messages.append(f"⚠️ Potential keyword stuffing detected: {', '.join(high_density_words[:3])}")
                recommendations.append("Consider reducing frequency of over-optimized keywords (>3% density)")
            
            # Check for good keyword distribution
            if len(keyword_density['medium_density']) >= 3:
                analysis_messages.append("✅ Good keyword distribution found")
            else:
                recommendations.append("Consider adding more medium-density keywords (1-3% density)")
        
        # Check total word count
        if total_words < 300:
            recommendations.append("Content is quite short - consider expanding to at least 300 words")
        elif total_words > 2000:
            recommendations.append("Content is quite long - ensure it's well-structured with headings")
        
        return {
            "word_frequency": word_freq_df.to_dict('records') if not word_freq_df.empty else [],
            "keyword_density": keyword_density,
            "top_keywords": top_keywords,
            "total_words": total_words,
            "analysis_message": " | ".join(analysis_messages) if analysis_messages else "✅ Keyword analysis complete",
            "recommendations": recommendations
        }
        
    except Exception as e:
        st.warning(f"⚠️ Error in keyword density analysis: {e}")
        return {
            "word_frequency": [],
            "keyword_density": {},
            "top_keywords": [],
            "total_words": 0,
            "analysis_message": f"⚠️ Error analyzing keywords: {str(e)}",
            "recommendations": []
        }

def analyze_url_structure_with_advertools(text, url):
    """
    Analyze URL structure and extract URLs using advertools for comprehensive link analysis.
    
    Args:
        text (str): The main content text from the webpage
        url (str): The current webpage URL for context
    
    Returns:
        dict: Comprehensive URL analysis using advertools
    """
    try:
        # Use advertools extract_urls for professional URL extraction
        extracted_urls = adv.extract_urls(text)
        
        if not extracted_urls:
            return {
                "extracted_urls": [],
                "url_analysis": {},
                "link_insights": [],
                "recommendations": ["No URLs found in content text"]
            }
        
        # Convert to DataFrame for easier analysis
        urls_df = pd.DataFrame(extracted_urls, columns=['urls'])
        
        # Analyze URL patterns and structure
        current_domain = urlparse(url).netloc.lower()
        
        # Categorize URLs
        internal_urls = []
        external_urls = []
        social_urls = []
        email_urls = []
        file_urls = []
        
        # Social media domains for classification
        social_domains = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 
                         'youtube.com', 'pinterest.com', 'tiktok.com', 'snapchat.com']
        
        # File extensions to identify downloadable content
        file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', 
                          '.zip', '.rar', '.mp4', '.mp3', '.jpg', '.png', '.gif']
        
        for extracted_url in extracted_urls:
            url_lower = extracted_url.lower()
            parsed_url = urlparse(extracted_url)
            domain = parsed_url.netloc.lower()
            
            # Categorize URLs
            if extracted_url.startswith('mailto:'):
                email_urls.append(extracted_url)
            elif any(ext in url_lower for ext in file_extensions):
                file_urls.append(extracted_url)
            elif any(social in domain for social in social_domains):
                social_urls.append(extracted_url)
            elif current_domain in domain or domain == '':
                internal_urls.append(extracted_url)
            else:
                external_urls.append(extracted_url)
        
        # Generate insights and recommendations
        insights = []
        recommendations = []
        
        # URL distribution analysis
        total_urls = len(extracted_urls)
        if total_urls > 0:
            insights.append(f"✅ Found {total_urls} URLs in content")
            
            # Internal vs External ratio analysis
            internal_ratio = (len(internal_urls) / total_urls) * 100
            external_ratio = (len(external_urls) / total_urls) * 100
            
            if internal_ratio > 70:
                insights.append(f"✅ Good internal linking: {len(internal_urls)} internal URLs ({internal_ratio:.1f}%)")
            elif internal_ratio < 30:
                insights.append(f"⚠️ Low internal linking: {len(internal_urls)} internal URLs ({internal_ratio:.1f}%)")
                recommendations.append("Consider adding more internal links to improve site structure")
            else:
                insights.append(f"✅ Balanced linking: {len(internal_urls)} internal, {len(external_urls)} external URLs")
            
            # External links analysis
            if external_urls:
                insights.append(f"🔗 {len(external_urls)} external links found ({external_ratio:.1f}%)")
                if len(external_urls) > 10:
                    recommendations.append("Consider reviewing external links - too many might dilute page authority")
            else:
                recommendations.append("Consider adding relevant external links to authoritative sources")
            
            # Social media presence
            if social_urls:
                insights.append(f"📱 {len(social_urls)} social media links found")
            else:
                recommendations.append("Consider adding social media links for better engagement")
            
            # File downloads
            if file_urls:
                insights.append(f"📄 {len(file_urls)} downloadable files linked")
            
            # Email links
            if email_urls:
                insights.append(f"📧 {len(email_urls)} email links found")
        
        # URL quality analysis
        broken_or_suspicious = []
        for extracted_url in extracted_urls:
            # Check for common issues
            if extracted_url.count('http') > 1:
                broken_or_suspicious.append(f"Malformed URL: {extracted_url}")
            elif len(extracted_url) > 200:
                broken_or_suspicious.append(f"Very long URL: {extracted_url[:100]}...")
        
        if broken_or_suspicious:
            insights.append(f"⚠️ {len(broken_or_suspicious)} potentially problematic URLs found")
            recommendations.extend(broken_or_suspicious[:3])  # Show first 3
        
        # Performance insights
        if total_urls > 50:
            recommendations.append("High number of URLs - ensure they're all necessary for user experience")
        elif total_urls < 5:
            recommendations.append("Consider adding more relevant links to improve content value")
        
        return {
            "extracted_urls": extracted_urls,
            "url_analysis": {
                "total_urls": total_urls,
                "internal_urls": internal_urls,
                "external_urls": external_urls,
                "social_urls": social_urls,
                "email_urls": email_urls,
                "file_urls": file_urls,
                "internal_ratio": round((len(internal_urls) / total_urls) * 100, 1) if total_urls > 0 else 0,
                "external_ratio": round((len(external_urls) / total_urls) * 100, 1) if total_urls > 0 else 0
            },
            "link_insights": insights,
            "recommendations": recommendations,
            "problematic_urls": broken_or_suspicious
        }
        
    except Exception as e:
        st.warning(f"⚠️ Error in URL analysis: {e}")
        return {
            "extracted_urls": [],
            "url_analysis": {},
            "link_insights": [f"⚠️ Error analyzing URLs: {str(e)}"],
            "recommendations": []
        }

def enhanced_content_analysis(soup, url):
    """
    Enhanced content analysis that includes advertools word frequency and URL analysis.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
        url (str): The URL of the webpage
    
    Returns:
        dict: Enhanced content analysis data
    """
    try:
        # Get the main content text (excluding navigation, footers, etc.)
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        main_text = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in main_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Perform keyword density analysis
        keyword_analysis = analyze_keyword_density(clean_text, url)
        
        # Perform URL analysis using advertools
        url_analysis = analyze_url_structure_with_advertools(clean_text, url)
        
        # Get existing content data
        content_data = extract_content_data(soup, url)
        
        # Enhance with keyword and URL analysis
        content_data.update({
            "keyword_analysis": keyword_analysis,
            "url_analysis": url_analysis,
            "clean_text_length": len(clean_text),
            "clean_word_count": len(clean_text.split())
        })
        
        # Update link insights with advertools analysis
        if url_analysis.get('link_insights'):
            content_data['link_insights'] = url_analysis['link_insights']
        
        return content_data
        
    except Exception as e:
        st.warning(f"⚠️ Error in enhanced content analysis: {e}")
        return extract_content_data(soup, url)  # Fallback to original

def fetch_seo_data(url):
    """
    Fetches SEO-related data from the provided URL and returns a dictionary with results.

    Args:
        url (str): The URL of the webpage to analyze.

    Returns:
        dict: SEO data.
    """
    soup = fetch_and_parse_html(url)
    if not soup:
        return {}
    
    meta_data = extract_meta_data(soup)
    headings = analyze_headings(soup)
    text = soup.get_text()
    readability_score = check_readability(text)
    images = analyze_images(soup, url)
    broken_links = analyze_links(soup)
    ctas = suggest_ctas(soup)
    alternates_and_canonicals = extract_alternates_and_canonicals(soup)
    schema_markup = extract_schema_markup(soup)
    content_data = enhanced_content_analysis(soup, url)
    open_graph = extract_open_graph(soup)
    
    return {
        "meta_data": meta_data,
        "headings": headings,
        "readability_score": readability_score,
        "images": images,
        "broken_links": broken_links,
        "ctas": ctas,
        "alternates_and_canonicals": alternates_and_canonicals,
        "schema_markup": schema_markup,
        "content_data": content_data,
        "open_graph": open_graph
    }

def download_csv(data, filename='seo_data.csv'):
    """
    Downloads the data as a CSV file.

    Args:
        data (dict): SEO data to download.
        filename (str): Filename for the downloaded CSV file.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key] + value)
            else:
                writer.writerow([key, value])
    st.success(f"Data exported to {filename}")

def analyze_onpage_seo():
    """
    Main function to analyze on-page SEO using Streamlit.
    """
    st.title("🔍 ALwrity On-Page SEO Analyzer")
    st.write("Enhanced with AI-powered keyword density and URL analysis")
    
    url = st.text_input("Enter URL to Analyze", "")
    if st.button("🚀 Analyze"):
        if not url:
            st.error("⚠️ Please enter a URL.")
        else:
            with st.spinner("Fetching and analyzing data..."):
                results = fetch_seo_data(url)
                social_tags = extract_social_tags(fetch_and_parse_html(url))
                speed = check_page_speed(url)
                mobile_usability = check_mobile_usability(fetch_and_parse_html(url))
                alt_text = check_alt_text(fetch_and_parse_html(url))
                
            if results:
                # Create tabs for better organization
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📄 Meta & Content", 
                    "🔤 Keywords & Density", 
                    "🖼️ Media & Links", 
                    "📱 Technical", 
                    "📊 Performance"
                ])
                
                with tab1:
                    st.subheader("Meta Data")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Title:** {results['meta_data']['metatitle']}")
                        st.write(f"**Description:** {results['meta_data']['metadescription']}")
                        st.write(f"**Language:** {results['meta_data']['html_language']}")
                        st.write(results['meta_data']['title_message'])
                        st.write(results['meta_data']['description_message'])
                    
                    with col2:
                        st.write(f"**Robots Directives:** {', '.join(results['meta_data']['robots_directives'])}")
                        st.write(f"**Viewport:** {results['meta_data']['viewport']}")
                        st.write(f"**Charset:** {results['meta_data']['charset']}")

                    st.subheader("Content Overview")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Text Length", f"{results['content_data']['text_length']} chars")
                    with col2:
                        if 'clean_word_count' in results['content_data']:
                            st.metric("Word Count", results['content_data']['clean_word_count'])
                    with col3:
                        st.metric("Readability Score", f"{results['readability_score']:.1f}")
                    
                    st.write(results['content_data']['h1_message'])
                    st.write(results['content_data']['content_message'])

                    st.subheader("Headings Structure")
                    if results['headings']:
                        headings_df = pd.DataFrame(results['headings'])
                        st.dataframe(headings_df, use_container_width=True)
                    else:
                        st.write("No headings found")

                with tab2:
                    st.subheader("🎯 Keyword Density Analysis")
                    
                    if 'keyword_analysis' in results['content_data']:
                        keyword_data = results['content_data']['keyword_analysis']
                        
                        # Display analysis message
                        st.write(keyword_data['analysis_message'])
                        
                        # Show recommendations if any
                        if keyword_data['recommendations']:
                            st.write("**💡 Recommendations:**")
                            for rec in keyword_data['recommendations']:
                                st.write(f"• {rec}")
                        
                        # Display top keywords
                        if keyword_data['top_keywords']:
                            st.subheader("📈 Top Keywords")
                            
                            # Create a DataFrame for better visualization
                            keywords_df = pd.DataFrame(keyword_data['top_keywords'])
                            
                            # Color code by density
                            def highlight_density(val):
                                if val > 3:
                                    return 'background-color: #ffcccc'  # Light red for high density
                                elif val >= 1:
                                    return 'background-color: #ccffcc'  # Light green for good density
                                else:
                                    return 'background-color: #ffffcc'  # Light yellow for low density
                            
                            styled_df = keywords_df.style.applymap(highlight_density, subset=['density'])
                            st.dataframe(styled_df, use_container_width=True)
                            
                            # Keyword density categories
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write("**🔴 High Density (>3%)**")
                                if keyword_data['keyword_density']['high_density']:
                                    for kw in keyword_data['keyword_density']['high_density']:
                                        st.write(f"• {kw['word']}: {kw['density']}%")
                                else:
                                    st.write("None found ✅")
                            
                            with col2:
                                st.write("**🟢 Good Density (1-3%)**")
                                if keyword_data['keyword_density']['medium_density']:
                                    for kw in keyword_data['keyword_density']['medium_density'][:5]:
                                        st.write(f"• {kw['word']}: {kw['density']}%")
                                else:
                                    st.write("None found")
                            
                            with col3:
                                st.write("**🟡 Low Density (<1%)**")
                                if keyword_data['keyword_density']['low_density']:
                                    for kw in keyword_data['keyword_density']['low_density'][:5]:
                                        st.write(f"• {kw['word']}: {kw['density']}%")
                                else:
                                    st.write("None found")
                        
                        else:
                            st.warning("No significant keywords found in content")
                    else:
                        st.warning("Keyword analysis not available")

                with tab3:
                    st.subheader("Images Analysis")
                    st.write(results['content_data']['alt_text_message'])
                    
                    if results['images']:
                        st.write(f"**Total Images:** {len(results['images'])}")
                        with st.expander("View Image Details"):
                            for i, img in enumerate(results['images'][:10]):  # Show first 10
                                st.write(f"**Image {i+1}:** {img}")
                    
                    st.subheader("🔗 Advanced Link Analysis")
                    
                    # Display advertools URL analysis if available
                    if 'url_analysis' in results['content_data']:
                        url_data = results['content_data']['url_analysis']
                        
                        # URL Statistics
                        st.subheader("📊 URL Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total URLs", url_data['url_analysis'].get('total_urls', 0))
                        with col2:
                            st.metric("Internal Links", len(url_data['url_analysis'].get('internal_urls', [])))
                        with col3:
                            st.metric("External Links", len(url_data['url_analysis'].get('external_urls', [])))
                        with col4:
                            st.metric("Social Links", len(url_data['url_analysis'].get('social_urls', [])))
                        
                        # Link Distribution
                        if url_data['url_analysis'].get('total_urls', 0) > 0:
                            st.subheader("🎯 Link Distribution")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Internal vs External Ratio:**")
                                internal_ratio = url_data['url_analysis'].get('internal_ratio', 0)
                                external_ratio = url_data['url_analysis'].get('external_ratio', 0)
                                st.write(f"• Internal: {internal_ratio}%")
                                st.write(f"• External: {external_ratio}%")
                            
                            with col2:
                                st.write("**Link Categories:**")
                                if url_data['url_analysis'].get('email_urls'):
                                    st.write(f"• Email: {len(url_data['url_analysis']['email_urls'])}")
                                if url_data['url_analysis'].get('file_urls'):
                                    st.write(f"• Files: {len(url_data['url_analysis']['file_urls'])}")
                                if url_data['url_analysis'].get('social_urls'):
                                    st.write(f"• Social: {len(url_data['url_analysis']['social_urls'])}")
                        
                        # URL Insights and Recommendations
                        if url_data.get('link_insights'):
                            st.subheader("💡 Link Analysis Insights")
                            for insight in url_data['link_insights']:
                                st.write(f"• {insight}")
                        
                        if url_data.get('recommendations'):
                            st.subheader("🎯 Link Optimization Recommendations")
                            for rec in url_data['recommendations']:
                                st.write(f"• {rec}")
                        
                        # Show extracted URLs
                        if url_data.get('extracted_urls'):
                            with st.expander(f"📋 View All Extracted URLs ({len(url_data['extracted_urls'])})"):
                                # Categorize and display URLs
                                internal_urls = url_data['url_analysis'].get('internal_urls', [])
                                external_urls = url_data['url_analysis'].get('external_urls', [])
                                social_urls = url_data['url_analysis'].get('social_urls', [])
                                
                                if internal_urls:
                                    st.write("**🏠 Internal URLs:**")
                                    for url in internal_urls[:10]:  # Show first 10
                                        st.write(f"• {url}")
                                
                                if external_urls:
                                    st.write("**🌐 External URLs:**")
                                    for url in external_urls[:10]:  # Show first 10
                                        st.write(f"• {url}")
                                
                                if social_urls:
                                    st.write("**📱 Social Media URLs:**")
                                    for url in social_urls:
                                        st.write(f"• {url}")
                    
                    else:
                        # Fallback to original link analysis
                        st.subheader("Links Analysis")
                        for insight in results['content_data']['link_insights']: 
                            st.write(f"- {insight}")
                        
                        st.write(results['content_data']['internal_links_message'])
                        st.write(results['content_data']['external_links_message'])
                    
                    if results['broken_links']:
                        st.subheader("⚠️ Broken Links")
                        for link in results['broken_links'][:5]:  # Show first 5
                            st.write(f"• {link}")
                    else:
                        st.success("✅ No broken links detected")

                with tab4:
                    st.subheader("Schema Markup")
                    st.write(f"**Schema Types:** {results['schema_markup']['schema_types']}")
                    st.write(results['schema_markup']['schema_message'])
                    
                    st.subheader("Canonical and Hreflangs")
                    st.write(f"**Canonical:** {results['alternates_and_canonicals']['canonical']}")
                    st.write(f"**Hreflangs:** {results['alternates_and_canonicals']['hreflangs']}")
                    st.write(f"**Mobile Alternate:** {results['alternates_and_canonicals']['mobile_alternate']}")
                    st.write(results['alternates_and_canonicals']['canonical_message'])
                    st.write(results['alternates_and_canonicals']['hreflangs_message'])
                    
                    st.subheader("Open Graph & Social")
                    st.write(f"**Open Graph Tags:** {results['open_graph']['open_graph']}")
                    st.write(results['open_graph']['open_graph_message'])
                    
                    st.write(f"**Twitter Cards:** {social_tags['twitter_cards']}")
                    st.write(social_tags['twitter_message'])
                    st.write(f"**Facebook Open Graph:** {social_tags['facebook_open_graph']}")
                    st.write(social_tags['facebook_message'])

                with tab5:
                    st.subheader("Performance & Usability")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Page Speed**")
                        st.write(speed['speed_message'])
                        
                        st.write("**Mobile Usability**")
                        st.write(mobile_usability['mobile_message'])
                    
                    with col2:
                        st.write("**Accessibility**")
                        st.write(alt_text['alt_text_message'])
                        
                        st.write("**CTAs Found**")
                        if results['ctas']:
                            for cta in results['ctas']:
                                st.write(f"• {cta}")
                        else:
                            st.write("No common CTAs detected")
                
                # Export functionality
                st.subheader("📥 Export Data")
                if st.button("Download Complete Analysis as CSV"):
                    download_csv(results)
