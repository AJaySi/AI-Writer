import streamlit as st
import cloudscraper
from bs4 import BeautifulSoup
import json
import requests
import csv
import time

def fetch_and_parse_html(url):
    """Fetches HTML content from the given URL using CloudScraper and parses it with BeautifulSoup."""
    try:
        scraper = cloudscraper.create_scraper()
        html = scraper.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup
    except Exception as e:
        st.error(f"⚠️ Error fetching or parsing HTML: {e}")
        return None

def extract_meta_data(soup):
    """Extracts meta data like title, description, and robots directives from the parsed HTML."""
    try:
        metatitle = soup.find('title').get_text() if soup.find('title') else "Title not found"
        metadescription = soup.find('meta', attrs={'name': 'description'})["content"] if soup.find('meta', attrs={'name': 'description'}) else "Description not found"
        robots_directives = [directive.strip() for directive in soup.find('meta', attrs={'name': 'robots'})["content"].split(",")] if soup.find('meta', attrs={'name': 'robots'}) else []
        viewport = soup.find('meta', attrs={'name': 'viewport'})["content"] if soup.find('meta', attrs={'name': 'viewport'}) else "Viewport not found"
        charset = soup.find('meta', attrs={'charset': True})["charset"] if soup.find('meta', attrs={'charset': True}) else "Charset not found"
        html_language = soup.find('html')["lang"] if soup.find('html') else "Language not found"
        
        # Check for missing or long title/meta description
        title_length = len(metatitle) if metatitle != "Title not found" else 0
        description_length = len(metadescription) if metadescription != "Description not found" else 0
        title_message = "✅ Title length is good." if 30 <= title_length <= 60 else "⚠️ Title length should be between 30-60 characters. Aim for clear and concise titles that accurately reflect your page's content."
        description_message = "✅ Meta description length is good." if 70 <= description_length <= 160 else "⚠️ Meta description should be between 70-160 characters. Craft compelling descriptions that entice users to click your link."
        
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

def extract_alternates_and_canonicals(soup):
    """Extracts canonical URL, hreflangs, and mobile alternate links from the parsed HTML."""
    try:
        canonical = soup.find('link', attrs={'rel': 'canonical'})["href"] if soup.find('link', attrs={'rel': 'canonical'}) else "Canonical not found"
        list_hreflangs = [[a['href'], a["hreflang"]] for a in soup.find_all('link', href=True, hreflang=True)] if soup.find_all('link', href=True, hreflang=True) else []
        mobile_alternate = soup.find('link', attrs={'media': 'only screen and (max-width: 640px)'})["href"] if soup.find('link', attrs={'media': 'only screen and (max-width: 640px)'}) else "Mobile Alternate not found"
        
        # Provide user-friendly insights
        canonical_message = "✅ Canonical tag found. Great! This helps avoid duplicate content issues." if canonical != "Canonical not found" else "⚠️ Consider adding a canonical tag to tell search engines which version of your page is the main one, preventing confusion and potential duplicate content penalties."
        hreflangs_message = "✅ Hreflang tags are implemented. Good job! This is crucial for international audiences." if list_hreflangs else "⚠️ Consider implementing hreflang tags to help search engines understand the language variations of your site. This is essential for international SEO and can lead to better search rankings in different regions."
        
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
    """Extracts schema markup data from the parsed HTML."""
    try:
        json_schema = soup.find('script', attrs={'type': 'application/ld+json'})
        if json_schema:
            json_file = json.loads(json_schema.get_text())
            schema_types = [x['@type'] for x in json_file.get("@graph", [])] if "@graph" in json_file else [json_file["@type"]]
            schema_message = "✅ Schema markup found. Wonderful! This helps search engines better understand your content." if schema_types else "⚠️ No schema markup found. Consider adding structured data (like JSON-LD schema) to your pages. It can enhance search results by giving search engines more context about your content, potentially leading to richer snippets and improved visibility."
            return {
                "schema_types": schema_types,
                "schema_message": schema_message
            }
        else:
            return {
                "schema_message": "⚠️ No schema markup found. Consider adding structured data (like JSON-LD schema) to your pages. It can enhance search results by giving search engines more context about your content, potentially leading to richer snippets and improved visibility."
            }
    except Exception as e:
        st.warning(f"⚠️ Error extracting schema markup: {e}")
        return {}

def extract_content_data(soup, url):
    """Extracts content data such as text length, headers, and insights about images and links."""
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
        
        # Content length evaluation
        content_message = "✅ Content length is adequate." if text_length > 300 else "⚠️ Consider adding more content (minimum 300 words). Aim for thorough and engaging content that provides value to your audience. Longer content often ranks higher in search results."
        
        # Header evaluation
        h1_message = "✅ H1 tag found. Good! It helps structure your content." if h1 else "⚠️ Missing H1 tag.  An H1 tag (the most important heading) is crucial for content structure and SEO. Add an H1 tag clearly defining your page's main topic."

        # Image alt text check
        missing_alt_texts = sum([1 for img in images if img[1] == "No alt text"])
        alt_text_message = "✅ All images have alt text. Great! This helps accessibility and SEO." if missing_alt_texts == 0 else f"⚠️ {missing_alt_texts} images are missing alt text. Consider adding descriptive alt text descriptions to all images. Alt text helps users with visual impairments understand the images, and search engines use it to better understand the context of the page."
        
        # Links evaluation
        internal_links_message = f"✅ {len(internal_links)} internal links found. Good practice for website structure."
        external_links_message = f"✅ {len(external_links)} external links found. Links to high-quality external sources add value."

        # Link Insights
        link_insights = []
        if internal_links:
            link_insights.append("✅  Internal links are present.")
        if external_links:
            link_insights.append("✅  External links are present.")

        return {
            "text_length": text_length,
            "headers": list_headers,
            "images": images,
            "h1_message": h1_message,
            "content_message": content_message,
            "alt_text_message": alt_text_message,
            "internal_links_message": internal_links_message,
            "external_links_message": external_links_message,
            "link_insights": link_insights  # Added new key for link insights
        }
    except Exception as e:
        st.warning(f"⚠️ Error extracting content data: {e}")
        return {}

def extract_open_graph(soup):
    """Extracts Open Graph data from the parsed HTML."""
    try:
        open_graph = [[a["property"].replace("og:", ""), a["content"]] for a in soup.select("meta[property^=og]")]
        open_graph_message = "✅ Open Graph tags found. Awesome! These improve your social media sharing." if open_graph else "⚠️ No Open Graph tags found. Consider adding Open Graph tags. They help your content appear better when shared on social media, with clearer titles, descriptions, and images."
        return {
            "open_graph": open_graph,
            "open_graph_message": open_graph_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error extracting Open Graph data: {e}")
        return {}

def extract_social_tags(soup):
    """Extracts Twitter Card and Facebook Open Graph data from the parsed HTML."""
    try:
        twitter_cards = [[a["name"].replace("twitter:", ""), a["content"]] for a in soup.select("meta[name^=twitter]")]
        facebook_open_graph = [[a["property"].replace("og:", ""), a["content"]] for a in soup.select("meta[property^=og]")]
        
        twitter_message = "✅ Twitter Card tags found." if twitter_cards else "⚠️ No Twitter Card tags found. Consider adding them for better visibility on Twitter."
        facebook_message = "✅ Facebook Open Graph tags found." if facebook_open_graph else "⚠️ No Facebook Open Graph tags found. Consider adding them for better sharing on Facebook."
        
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
    """Fetches and analyzes page speed metrics using Google PageSpeed Insights API."""
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
    """Checks if the website is mobile-friendly based on viewport and other elements."""
    try:
        viewport = soup.find('meta', attrs={'name': 'viewport'})["content"] if soup.find('meta', attrs={'name': 'viewport'}) else ""
        mobile_message = "✅ Mobile viewport is set. Great! This indicates the site is designed to be responsive on different devices." if viewport else "⚠️ Mobile viewport meta tag is missing.  Ensure your site is designed to work well on all devices, especially mobile.  This is essential for a great user experience and improved SEO."
        return {
            "mobile_message": mobile_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error checking mobile usability: {e}")
        return {}

def check_alt_text(soup):
    """Checks if all images have alt text."""
    try:
        images = soup.find_all('img')
        missing_alt_texts = sum([1 for img in images if not img.get("alt")])
        alt_text_message = "✅ All images have alt text. Great! This helps accessibility and SEO." if missing_alt_texts == 0 else f"⚠️ {missing_alt_texts} images are missing alt text. Consider adding descriptive alt text for better accessibility.  Alt text helps users with visual impairments understand images and improves SEO."
        return {
            "alt_text_message": alt_text_message
        }
    except Exception as e:
        st.warning(f"⚠️ Error checking alt text: {e}")
        return {}

def fetch_seo_data(url):
    """Fetches SEO-related data from the provided URL and returns a dictionary with results."""
    soup = fetch_and_parse_html(url)
    if not soup:
        return {}
    
    meta_data = extract_meta_data(soup)
    alternates_and_canonicals = extract_alternates_and_canonicals(soup)
    schema_markup = extract_schema_markup(soup)
    content_data = extract_content_data(soup, url)
    open_graph = extract_open_graph(soup)
    
    return {
        "meta_data": meta_data,
        "alternates_and_canonicals": alternates_and_canonicals,
        "schema_markup": schema_markup,
        "content_data": content_data,
        "open_graph": open_graph
    }

def download_csv(data, filename='seo_data.csv'):
    """Downloads the data as a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            if isinstance(value, list):
                writer.writerow([key] + value)
            else:
                writer.writerow([key, value])
    st.success(f"Data exported to {filename}")

def analyze_onpage_seo():
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
                
                # Display link insights in a bullet point format
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
                
                # Option to download results
                if st.button("Download CSV"):
                    download_csv(results)
