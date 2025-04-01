import os
import json
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential
import crawl4ai
from bs4 import BeautifulSoup
import requests
import csv
import time
from urllib.parse import urlparse
import validators
import readability
import textstat
import re
from PIL import Image
import io
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
                response = requests.head(href, timeout=5)
                if response.status_code >= 400:
                    broken_links.append(href)
            except requests.RequestException:
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
    content_data = extract_content_data(soup, url)
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
    st.title("ALwrity On Page SEO Analyzer")
    
    url = st.text_input("Enter URL to Analyze", "")
    if st.button("Analyze"):
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
                st.subheader("Meta Data")
                st.write(f"**Title:** {results['meta_data']['metatitle']}")
                st.write(f"**Description:** {results['meta_data']['metadescription']}")
                st.write(f"**Robots Directives:** {', '.join(results['meta_data']['robots_directives'])}")
                st.write(f"**Viewport:** {results['meta_data']['viewport']}")
                st.write(f"**Charset:** {results['meta_data']['charset']}")
                st.write(f"**Language:** {results['meta_data']['html_language']}")
                st.write(results['meta_data']['title_message'])
                st.write(results['meta_data']['description_message'])

                st.subheader("Headings")
                st.write(results['headings'])

                st.subheader("Readability Score")
                st.write(f"**Readability Score:** {results['readability_score']}")

                st.subheader("Images")
                st.write(results['images'])

                st.subheader("Broken Links")
                st.write(results['broken_links'])

                st.subheader("Suggested CTAs")
                st.write(results['ctas'])
                
                st.subheader("Canonical and Hreflangs")
                st.write(f"**Canonical:** {results['alternates_and_canonicals']['canonical']}")
                st.write(f"**Hreflangs:** {results['alternates_and_canonicals']['hreflangs']}")
                st.write(f"**Mobile Alternate:** {results['alternates_and_canonicals']['mobile_alternate']}")
                st.write(results['alternates_and_canonicals']['canonical_message'])
                st.write(results['alternates_and_canonicals']['hreflangs_message'])
                
                st.subheader("Schema Markup")
                st.write(f"**Schema Types:** {results['schema_markup']['schema_types']}")
                st.write(results['schema_markup']['schema_message'])
                
                st.subheader("Content Data")
                st.write(f"**Text Length:** {results['content_data']['text_length']} characters")
                st.write(results['content_data']['h1_message'])
                st.write(results['content_data']['content_message'])
                st.write(results['content_data']['alt_text_message'])
                
                for insight in results['content_data']['link_insights']: 
                    st.write(f"- {insight}") 
                
                st.write(results['content_data']['internal_links_message'])
                st.write(results['content_data']['external_links_message'])
                
                st.subheader("Open Graph Data")
                st.write(f"**Open Graph Tags:** {results['open_graph']['open_graph']}")
                st.write(results['open_graph']['open_graph_message'])
                
                st.subheader("Social Tags")
                st.write(f"**Twitter Cards:** {social_tags['twitter_cards']}")
                st.write(social_tags['twitter_message'])
                st.write(f"**Facebook Open Graph:** {social_tags['facebook_open_graph']}")
                st.write(social_tags['facebook_message'])
                
                st.subheader("Performance Metrics")
                st.write(speed['speed_message'])
                
                st.subheader("Mobile Usability")
                st.write(mobile_usability['mobile_message'])
                
                st.subheader("Accessibility")
                st.write(alt_text['alt_text_message'])
                
                if st.button("Download CSV"):
                    download_csv(results)
