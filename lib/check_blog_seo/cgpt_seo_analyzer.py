###################################################
#
# The script covers many SEO factors, including keyword presence, title length, 
# meta description, images, img alt text, headings, internal links, external links, 
# spelling errors, grammar errors, and readability.
#
##################################################

import re
from bs4 import BeautifulSoup
from textstat import flesch_reading_ease
import spellchecker

class SEOAnalyzer:
    def __init__(self, html_content, target_keywords):
        self.html_content = html_content
        self.target_keywords = target_keywords

    def analyze_html_content(self):
        try:
            soup = BeautifulSoup(self.html_content, 'html.parser')

            # Extract and clean text from HTML
            text = ' '.join(soup.stripped_strings)
            text = re.sub(r'\s+', ' ', text)

            # Calculate keyword density
            keyword_density = {}
            for keyword in self.target_keywords:
                keyword_density[keyword] = (text.lower().count(keyword.lower()) / len(text.split())) * 100

            # Check for the presence of keywords in the title
            title_tag = soup.find('title')
            title_text = title_tag.text.lower() if title_tag else ''
            keyword_presence_in_title = {keyword: keyword.lower() in title_text for keyword in self.target_keywords}

            # Check for the presence of images and keywords in image alt text
            images = soup.find_all('img')
            img_alt_text = [img.get('alt', '').lower() for img in images]
            keyword_presence_in_img_alt_text = {keyword: any(keyword.lower() in alt_text for alt_text in img_alt_text) for keyword in self.target_keywords}

            # Check for the presence of headings
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            headings_text = ' '.join(heading.text.lower() for heading in headings)

            # Check for the presence of internal and external links
            internal_links = len([link for link in soup.find_all('a') if '#' not in link.get('href', '')])
            external_links = len([link for link in soup.find_all('a') if 'http' in link.get('href', '')])

            # Calculate readability score
            readability_score = flesch_reading_ease(text)

            # Check for spelling and grammar errors
            spell = spellchecker.SpellChecker()
            spelling_errors = len(spell.unknown(text.split()))
            grammar_errors = len(spell.check_grammar(text))

            # Calculate SEO score
            seo_score = 0

            # Check for the presence of relevant keywords
            for keyword in self.target_keywords:
                if keyword in text.lower():
                    seo_score += 1

            # Check for title length
            title_length = len(title_text.split()) if title_text else 0
            recommended_title_length = (50, 70)

            if recommended_title_length[0] <= title_length <= recommended_title_length[1]:
                seo_score += 1

            # Generate suggestions for improvement
            suggestions = []
            if seo_score < 5:
                suggestions.append("Add more relevant keywords to your HTML content.")
                suggestions.append("Make sure your title contains keywords.")
                suggestions.append("Add keywords to image alt text.")
                suggestions.append("Add headings to your HTML content.")
                suggestions.append("Add internal links to your HTML content.")

            return {
                'Keyword Density': keyword_density,
                'Keyword Presence in Title': keyword_presence_in_title,
                'Keyword Presence in Image Alt Text': keyword_presence_in_img_alt_text,
                'Headings Text': headings_text,
                'Internal Links': internal_links,
                'External Links': external_links,
                'Readability Score': readability_score,
                'Spelling Errors': spelling_errors,
                'Grammar Errors': grammar_errors,
                'SEO Score': seo_score,
                'Suggestions': suggestions
            }
        except Exception as e:
            return {'error': str(e)}

# Example usage:
if __name__ == "__main__":
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SEO Analyzer - Sample Page</title>
        <meta name="description" content="This is a sample page for SEO analysis.">
    </head>
    <body>
        <h1>Welcome to the SEO Analyzer</h1>
        <p>This is a sample page with some sample content for SEO analysis. It mentions the target keywords SEO, keywords, and content.</p>
        <img src="image1.jpg" alt="SEO image">
        <img src="image2.jpg" alt="Keywords image">
    </body>
    </html>
    """

    keywords = ['SEO', 'keywords', 'content']  # Replace with your target keywords

    seo_analyzer = SEOAnalyzer(html_content, keywords)
    results = seo_analyzer.analyze_html_content()

    print("SEO Analysis Results:")
    print(f"Keyword Density: {results['Keyword Density']}")
    print(f"Keyword Presence in Title: {results['Keyword Presence in Title']}")
    print(f"Keyword Presence in Image Alt Text: {results['Keyword Presence in Image Alt Text']}")
    print(f"Headings Text: {results['Headings Text']}")
    print(f"Internal Links: {results['Internal Links']}")
    print(f"External Links: {results['External Links']}")
    print(f"Readability Score: {results['Readability Score']}")
    print(f"Spelling Errors: {results['Spelling Errors']}")
    print(f"Grammar Errors: {results['Grammar Errors']}")
    print(f"SEO Score: {results['SEO Score']}")
    print("Suggestions:")
    for suggestion in results['Suggestions']:
        print(suggestion)

