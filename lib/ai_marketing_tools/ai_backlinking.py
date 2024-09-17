#Problem:
#
#Finding websites for guest posts is manual, tedious, and time-consuming. Communicating with webmasters, maintaining conversations, and keeping track of backlinking opportunities is difficult to scale. Content creators and marketers struggle with discovering new websites and consistently getting backlinks.
#Solution:
#
#An AI-powered backlinking app that automates web research, scrapes websites, extracts contact information, and sends personalized outreach emails to webmasters. This would simplify the entire process, allowing marketers to scale their backlinking strategy with minimal manual intervention.
#Core Workflow:
#
#    User Input:
#        Keyword Search: The user inputs a keyword (e.g., "AI writers").
#        Search Queries: Your app will append various search strings to this keyword to find backlinking opportunities (e.g., "AI writers + 'Write for Us'").
#
#    Web Research:
#
#        Use search engines or web scraping to run multiple queries:
#            Keyword + "Guest Contributor"
#            Keyword + "Add Guest Post"
#            Keyword + "Write for Us", etc.
#
#        Collect URLs of websites that have pages or posts related to guest post opportunities.
#
#    Scrape Website Data:
#        Contact Information Extraction:
#            Scrape the website for contact details (email addresses, contact forms, etc.).
#            Use natural language processing (NLP) to understand the type of content on the website and who the contact person might be (webmaster, editor, or guest post manager).
#        Website Content Understanding:
#            Scrape a summary of each website’s content (e.g., their blog topics, categories, and tone) to personalize the email based on the site's focus.
#
#    Personalized Outreach:
#        AI Email Composition:
#            Compose personalized outreach emails based on:
#                The scraped data (website content, topic focus, etc.).
#                The user's input (what kind of guest post or content they want to contribute).
#            Example: “Hi [Webmaster Name], I noticed that your site [Site Name] features high-quality content about [Topic]. I would love to contribute a guest post on [Proposed Topic] in exchange for a backlink.”
#
#    Automated Email Sending:
#        Review Emails (Optional HITL):
#            Let users review and approve the personalized emails before they are sent, or allow full automation.
#        Send Emails:
#            Automate email dispatch through an integrated SMTP or API (e.g., Gmail API, SendGrid).
#            Keep track of which emails were sent, bounced, or received replies.
#
#    Scaling the Search:
#        Repeat for Multiple Keywords:
#            Run the same scraping and outreach process for a list of relevant keywords, either automatically suggested or uploaded by the user.
#        Keep Track of Sent Emails:
#            Maintain a log of all sent emails, responses, and follow-up reminders to avoid repetition or forgotten leads.
#
#    Tracking Responses and Follow-ups:
#        Automated Responses:
#            If a website replies positively, AI can respond with predefined follow-up emails (e.g., proposing topics, confirming submission deadlines).
#        Follow-up Reminders:
#            If there’s no reply, the system can send polite follow-up reminders at pre-set intervals.
#
#Key Features:
#
#    Automated Web Scraping:
#        Scrape websites for guest post opportunities using a predefined set of search queries based on user input.
#        Extract key information like email addresses, names, and submission guidelines.
#
#    Personalized Email Writing:
#        Leverage AI to create personalized emails using the scraped website information.
#        Tailor each email to the tone, content style, and focus of the website.
#
#    Email Sending Automation:
#        Integrate with email platforms (e.g., Gmail, SendGrid, or custom SMTP).
#        Send automated outreach emails with the ability for users to review first (HITL - Human-in-the-loop) or automate completely.
#
#    Customizable Email Templates:
#        Allow users to customize or choose from a set of email templates for different types of outreach (e.g., guest post requests, follow-up emails, submission offers).
#
#    Lead Tracking and Management:
#        Track all emails sent, monitor replies, and keep track of successful backlinks.
#        Log each lead’s status (e.g., emailed, responded, no reply) to manage future interactions.
#
#    Multiple Keywords/Queries:
#        Allow users to run the same process for a batch of keywords, automatically generating relevant search queries for each.
#
#    AI-Driven Follow-Up:
#        Schedule follow-up emails if there is no response after a specified period.
#
#    Reports and Analytics:
#        Provide users with reports on how many emails were sent, opened, replied to, and successful backlink placements.
#
#Advanced Features (for Scaling and Optimization):
#
#    Domain Authority Filtering:
#        Use SEO APIs (e.g., Moz, Ahrefs) to filter websites based on their domain authority or backlink strength.
#        Prioritize high-authority websites to maximize the impact of backlinks.
#
#    Spam Detection:
#        Use AI to detect and avoid spammy or low-quality websites that might harm the user’s SEO.
#
#    Contact Form Auto-Fill:
#        If the site only offers a contact form (without email), automatically fill and submit the form with AI-generated content.
#
#    Dynamic Content Suggestions:
#        Suggest guest post topics based on the website’s focus, using NLP to analyze the site's existing content.
#
#    Bulk Email Support:
#        Allow users to bulk-send outreach emails while still personalizing each message for scalability.
#
#    AI Copy Optimization:
#        Use copywriting AI to optimize email content, adjusting tone and CTA based on the target audience.
#
#Challenges and Considerations:
#
#    Legal Compliance:
#        Ensure compliance with anti-spam laws (e.g., CAN-SPAM, GDPR) by including unsubscribe options or manual email approval.
#
#    Scraping Limits:
#        Be mindful of scraping limits on certain websites and employ smart throttling or use API-based scraping for better reliability.
#
#    Deliverability:
#        Ensure emails are delivered properly without landing in spam folders by integrating proper email authentication (SPF, DKIM) and using high-reputation SMTP servers.
#
#    Maintaining Email Personalization:
#        Striking the balance between automating the email process and keeping each message personal enough to avoid being flagged as spam.
#
#Technology Stack:
#
#    Web Scraping: BeautifulSoup, Scrapy, or Puppeteer for scraping guest post opportunities and contact information.
#    Email Automation: Integrate with Gmail API, SendGrid, or Mailgun for sending emails.
#    NLP for Personalization: GPT-based models for email generation and web content understanding.
#    Frontend: React or Vue for the user interface.
#    Backend: Python/Node.js with Flask or Express for the API and automation logic.
#    Database: MongoDB or PostgreSQL to track leads, emails, and responses.
#
#This solution will significantly streamline the backlinking process by automating the most tedious tasks, from finding sites to personalizing outreach, enabling marketers to focus on content creation and high-level strategies.

from lib.ai_web_researcher.firecrawl_web_crawler import scrape_website
from lib.gpt_providers.text_generation.main_text_generation import llm_text_gen
from lib.ai_web_researcher.firecrawl_web_crawler import scrape_url


def generate_search_queries(keyword):
    """
    Generate a list of search queries for finding guest post opportunities.
    
    Args:
        keyword (str): The keyword to base the search queries on.
    
    Returns:
        list: A list of search queries.
    """
    search_queries = [
        f"{keyword} + 'Guest Contributor'",
        f"{keyword} + 'Add Guest Post'",
        f"{keyword} + 'Guest Bloggers Wanted'",
        f"{keyword} + 'Guest Posts Roundup'",
        f"{keyword} + 'Write for Us'",
        f"{keyword} + 'Submit Guest Post'",
        f"{keyword} + 'Submit a Guest Article'",
        f"{keyword} + 'Guest Bloggers Wanted'",
        f"{keyword} + 'Submit an article'",
        f"{keyword} + 'Suggest a guest post'",
        f"{keyword} + 'Send a guest post'",
        f"{keyword} + 'Become a Guest Blogger'",
        f"{keyword} + 'guest post opportunities'",
        f"{keyword} + 'this is a guest post by'",
        f"{keyword} + 'This post was written by'",
        f"{keyword} + 'guest post courtesy of'",
        f"{keyword} + 'submit article'"
    ]
    return search_queries

def find_backlink_opportunities(keyword):
    """
    Find backlink opportunities by scraping websites based on search queries.
    
    Args:
        keyword (str): The keyword to search for backlink opportunities.
    
    Returns:
        list: A list of results from the scraped websites.
    """
    search_queries = generate_search_queries(keyword)
    results = []
    for query in search_queries:
        # Placeholder for a function to search and get URLs
        urls = search_for_urls(query)
        for url in urls:
            website_data = scrape_website(url)
            if website_data:
                contact_info = extract_contact_info(url)
                # Construct a prompt for the LLM
                prompt = f"""
                Analyze the following website content and provide insights:
                Content: {website_data.get("content_summary", "")}

                Please provide:
                1. A brief summary of what the website is about.
                2. Guidelines to follow for guest posting.
                3. Suggested topics to write on.
                4. Any other insights to help make a highly personalized reach out and decision making.
                """

                insights = llm_text_gen(prompt)

                detailed_result = {
                    "url": url,
                    "metadata": {
                        "title": website_data.get("metadata", {}).get("title", ""),
                        "description": website_data.get("metadata", {}).get("description", ""),
                        "keywords": website_data.get("metadata", {}).get("keywords", []),
                        "author": website_data.get("metadata", {}).get("author", ""),
                    },
                    "content_summary": website_data.get("content_summary", ""),
                    "contact_info": contact_info,
                    "insights": insights,
                    "backlink_opportunity": {
                        "query": query,
                        "context": "Guest post opportunity"
                    }
                }
                results.append(detailed_result)
    return results



def search_for_urls(query):
    """
    Search for URLs based on a query using Firecrawl.

    Args:
        query (str): The search query.

    Returns:
        list: A list of URLs.
    """
    # Use Firecrawl to perform the search
    result = scrape_url(query)
    if result and 'urls' in result:
        return result['urls']
    return []


from lib.ai_web_researcher.firecrawl_web_crawler import extract_data

def extract_contact_info(url):
    """
    Extract contact information from a website using Firecrawl's LLM Extract feature.
    
    Args:
        url (str): The URL of the website to extract contact information from.
    
    Returns:
        dict: Extracted contact information.
    """
    schema = {
        "type": "object",
        "properties": {
            "emails": {
                "type": "array",
                "items": {
                    "type": "string",
                    "format": "email"
                }
            },
            "contact_forms": {
                "type": "array",
                "items": {
                    "type": "string",
                    "format": "uri"
                }
            }
        },
        "required": ["emails", "contact_forms"]
    }
    
    result = extract_data(url, schema)
    if result and 'extract' in result:
        return result['extract']
    return {}
