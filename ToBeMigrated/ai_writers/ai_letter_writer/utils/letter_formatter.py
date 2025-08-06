"""
Letter Formatter Module

This module provides utilities for formatting letters and generating HTML
previews in different styles (Personal, Formal, Business, Cover).
The formatting functions here are primarily focused on generating HTML
for preview purposes, applying standard layout conventions for each letter type
using inline CSS styles.
"""

import re
from typing import Dict, Any

def format_letter(content: str, metadata: Dict[str, Any], letter_type: str = "personal") -> str:
    """
    Format a letter with basic structure (paragraphs).

    Args:
        content: The raw letter content (string).
        metadata: Dictionary containing metadata (currently not used for formatting in this placeholder).
        letter_type: Type of letter (personal, formal, business, cover).

    Returns:
        Formatted letter content (currently just returns the input content).
        This is a placeholder and would be expanded to apply specific
        formatting rules (e.g., indentation, spacing) based on letter type
        and metadata in a full implementation before generating HTML.
        For this module, we primarily rely on the HTML generation functions
        to handle the visual formatting.
    """
    # This is a basic placeholder. In a real implementation, this function
    # might process the raw text content to add indentation, adjust line breaks,
    # or handle specific markdown-like syntax before it's passed to the
    # HTML generation functions.
    # For now, we assume the input `content` uses double newlines for paragraphs.
    return content

def get_letter_preview_html(content: str, metadata: Dict[str, Any], letter_type: str = "personal") -> str:
    """
    Generate HTML for letter preview based on letter type and metadata.
    This function acts as a dispatcher to the specific HTML generation functions.

    Args:
        content: The letter content string.
        metadata: Dictionary containing metadata like sender/recipient info, date, etc.
        letter_type: Type of letter ("personal", "formal", "business", "cover").
                     Defaults to "personal".

    Returns:
        HTML string for letter preview, styled appropriately for the type.
        Includes basic styling for a printable letter appearance.
    """
    # Dispatch to the appropriate HTML generation function based on letter type
    # Pass the content and metadata to the specific functions
    if letter_type == "personal":
        return get_personal_letter_html(content, metadata)
    elif letter_type == "formal":
        return get_formal_letter_html(content, metadata)
    elif letter_type == "business":
        return get_business_letter_html(content, metadata)
    elif letter_type == "cover":
        return get_cover_letter_html(content, metadata)
    else:
        # Fallback for unrecognized types, displaying raw content in a styled box
        return f"""
        <div style="max-width: 800px; margin: 20px auto; padding: 20px; border: 1px solid #ccc; font-family: sans-serif; line-height: 1.6; background-color: #fff8f8; color: #333; border-radius: 8px;">
            <h3 style="color: #e53935; margin-top: 0;">Preview Unavailable for Unknown Letter Type</h3>
            <p>The letter type '{letter_type}' is not recognized. Displaying raw content:</p>
            <pre style="white-space: pre-wrap; word-wrap: break-word; background-color: #f8f8f8; padding: 15px; border: 1px solid #ddd; border-radius: 4px; overflow-x: auto;">{content}</pre>
        </div>
        """

def get_personal_letter_html(content: str, metadata: Dict[str, Any]) -> str:
    """
    Generate HTML for personal letter preview with basic styling.
    Uses a more informal layout and font style.

    Args:
        content: The letter content string.
        metadata: Dictionary containing personal letter metadata (sender_name, date).

    Returns:
        HTML string for personal letter preview.
    """
    # Extract metadata with default empty strings for robustness
    sender_name = metadata.get("sender_name", "")
    # recipient_name = metadata.get("recipient_name", "") # Less common in personal body, but could be used in greeting
    date = metadata.get("date", "")

    # Split content into paragraphs based on double newlines
    # Use list comprehension to strip whitespace and filter out empty strings
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    # Format paragraphs as HTML <p> tags with bottom margin
    formatted_paragraphs = "".join(f"<p style='margin-bottom: 1em;'>{paragraph}</p>" for paragraph in paragraphs)

    # Basic HTML structure with inline styles for a personal letter feel
    # Styles aim for a warm, readable appearance
    html = f"""
    <div style="max-width: 700px; margin: 20px auto; padding: 30px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #ffffff; font-family: 'Georgia', serif; line-height: 1.7; color: #333; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="text-align: right; margin-bottom: 30px; font-size: 0.9em; color: #555;">
            {date if date else "[Date]"}
        </div>

        <div style="margin-bottom: 30px;">
             {formatted_paragraphs if formatted_paragraphs else "<p style='color: #888;'>Letter content goes here...</p>"}
        </div>

        <div style="margin-top: 40px;">
            <p style="margin-bottom: 0.5em;">Sincerely,</p>
            <p style="font-weight: bold; margin-top: 0;">{sender_name if sender_name else "[Sender Name]"}</p>
        </div>
    </div>
    """
    return html

def get_formal_letter_html(content: str, metadata: Dict[str, Any]) -> str:
    """
    Generate HTML for formal letter preview with standard formal structure and styling.
    Uses a more professional layout and font style (Arial/sans-serif).

    Args:
        content: The letter content string.
        metadata: Dictionary containing formal letter metadata.

    Returns:
        HTML string for formal letter preview.
    """
    # Extract metadata with default empty strings
    sender_name = metadata.get("sender_name", "")
    sender_title = metadata.get("sender_title", "")
    sender_organization = metadata.get("sender_organization", "")
    # Replace newlines in address for HTML display
    sender_address = metadata.get("sender_address", "").replace("\n", "<br>")
    sender_phone = metadata.get("sender_phone", "")
    sender_email = metadata.get("sender_email", "")

    recipient_name = metadata.get("recipient_name", "")
    recipient_title = metadata.get("recipient_title", "")
    recipient_organization = metadata.get("recipient_organization", "")
    # Replace newlines in address for HTML display
    recipient_address = metadata.get("recipient_address", "").replace("\n", "<br>")

    date = metadata.get("date", "")
    subject = metadata.get("subject", "") # Added subject line
    salutation = metadata.get("salutation", "Dear Sir/Madam,") # Added salutation
    complimentary_close = metadata.get("complimentary_close", "Sincerely,") # Added close

    # Determine alignment based on letter format (simplified)
    # Full Block: All aligned left
    # Modified Block: Sender address block, date, closing, and signature are right-aligned
    letter_format = metadata.get("letter_format", "Full Block")
    sender_address_align = "left"
    date_align = "left"
    closing_align = "left"

    if letter_format == "Modified Block":
        sender_address_align = "right"
        date_align = "right"
        closing_align = "right"

    # Split content into paragraphs based on double newlines
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    # Format paragraphs as HTML <p> tags with bottom margin
    formatted_paragraphs = "".join(f"<p style='margin-bottom: 1em;'>{paragraph}</p>" for paragraph in paragraphs)

    # Basic HTML structure with inline styles for a formal letter
    html = f"""
    <div style="max-width: 800px; margin: 20px auto; padding: 30px; border: 1px solid #d0d0d0; border-radius: 8px; background-color: #ffffff; font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">

        <div style="text-align: {sender_address_align}; margin-bottom: 20px; font-size: 0.9em;">
            <p style="margin: 0;">{sender_name if sender_name else "[Sender Name]"}{', ' + sender_title if sender_title else ''}</p>
            <p style="margin: 0;">{sender_organization if sender_organization else "[Sender Organization]"}</p>
            <p style="margin: 0;">{sender_address if sender_address else "[Sender Address]"}</p>
            <p style="margin: 0;">{sender_phone}</p>
            <p style="margin: 0;">{sender_email}</p>
        </div>

        <div style="text-align: {date_align}; margin-bottom: 20px;">
            <p style="margin: 0;">{date if date else "[Date]"}</p>
        </div>

        <div style="margin-bottom: 20px; font-size: 0.9em;">
            <p style="margin: 0;">{recipient_name if recipient_name else "[Recipient Name]"}{', ' + recipient_title if recipient_title else ''}</p>
            <p style="margin: 0;">{recipient_organization if recipient_organization else "[Recipient Organization]"}</p>
            <p style="margin: 0;">{recipient_address if recipient_address else "[Recipient Address]"}</p>
        </div>

        <div style="margin-bottom: 20px;">
            <p style="margin: 0; font-weight: bold;">Subject: {subject if subject else "[Subject Line]"}</p>
        </div>

        <div style="margin-bottom: 20px;">
            <p style="margin: 0;">{salutation}</p>
        </div>

        <div style="margin-bottom: 20px;">
            {formatted_paragraphs if formatted_paragraphs else "<p style='color: #888;'>Letter content goes here...</p>"}
        </div>

        <div style="margin-top: 40px; text-align: {closing_align};">
            <p style="margin-bottom: 0.5em;">{complimentary_close}</p>
            <p style="font-weight: bold; margin: 0;">{sender_name}</p>
            <p style="margin: 0; font-size: 0.9em;">{sender_title}</p>
            <p style="margin: 0; font-size: 0.9em;">{sender_organization}</p>
        </div>
    </div>
    """
    return html

def get_business_letter_html(content: str, metadata: Dict[str, Any]) -> str:
    """
    Generate HTML for business letter preview with standard business structure and styling.
    Includes optional letterhead.

    Args:
        content: The letter content string.
        metadata: Dictionary containing business letter metadata.

    Returns:
        HTML string for business letter preview.
    """
    # Extract metadata with default empty strings
    sender_company = metadata.get("sender_company", "")
    sender_name = metadata.get("sender_name", "")
    sender_title = metadata.get("sender_title", "")
    sender_address = metadata.get("sender_address", "").replace("\n", "<br>")
    sender_phone = metadata.get("sender_phone", "")
    sender_email = metadata.get("sender_email", "")
    sender_website = metadata.get("sender_website", "")

    recipient_company = metadata.get("recipient_company", "")
    recipient_name = metadata.get("recipient_name", "")
    recipient_title = metadata.get("recipient_title", "")
    recipient_address = metadata.get("recipient_address", "").replace("\n", "<br>")

    date = metadata.get("date", "")
    subject = metadata.get("subject", "") # Added subject line
    salutation = metadata.get("salutation", "Dear Sir/Madam,") # Added salutation
    complimentary_close = metadata.get("complimentary_close", "Sincerely,") # Added close

    # Determine alignment based on letter format (simplified)
    letter_format = metadata.get("letter_format", "Full Block")
    sender_info_align = "left"
    date_align = "left"
    closing_align = "left"

    if letter_format == "Modified Block":
        sender_info_align = "right"
        date_align = "right"
        closing_align = "right"

    # Include letterhead logic
    include_letterhead = metadata.get("include_letterhead", True)

    # Split content into paragraphs based on double newlines
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    # Format paragraphs as HTML <p> tags with bottom margin
    formatted_paragraphs = "".join(f"<p style='margin-bottom: 1em;'>{paragraph}</p>" for paragraph in paragraphs)

    # Create letterhead HTML if included and company name is provided
    letterhead_html = ""
    if include_letterhead and sender_company:
        letterhead_html = f"""
        <div style="padding-bottom: 15px; margin-bottom: 20px; border-bottom: 1px solid #eee;">
            <h2 style="margin: 0; color: #333; font-size: 1.5em;">{sender_company}</h2>
            <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #555;">
                {sender_address.replace('<br>', ', ') if sender_address else ''}
                {' | ' + sender_phone if sender_phone else ''}
                {' | ' + sender_email if sender_email else ''}
                {' | ' + sender_website if sender_website else ''}
            </p>
        </div>
        """

    # Basic HTML structure with inline styles for a business letter
    html = f"""
    <div style="max-width: 800px; margin: 20px auto; padding: 30px; border: 1px solid #d0d0d0; border-radius: 8px; background-color: #ffffff; font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        {letterhead_html}

        <div style="text-align: {date_align}; margin-bottom: 20px;">
            <p style="margin: 0;">{date if date else "[Date]"}</p>
        </div>

        <div style="margin-bottom: 20px; font-size: 0.9em;">
            <p style="margin: 0;">{recipient_name if recipient_name else "[Recipient Name]"}{', ' + recipient_title if recipient_title else ''}</p>
            <p style="margin: 0;">{recipient_company if recipient_company else "[Recipient Company]"}</p>
            <p style="margin: 0;">{recipient_address if recipient_address else "[Recipient Address]"}</p>
        </div>

        <div style="margin-bottom: 20px;">
            <p style="margin: 0; font-weight: bold;">Subject: {subject if subject else "[Subject Line]"}</p>
        </div>

        <div style="margin-bottom: 20px;">
            <p style="margin: 0;">{salutation}</p>
        </div>

        <div style="margin-bottom: 20px;">
            {formatted_paragraphs if formatted_paragraphs else "<p style='color: #888;'>Letter content goes here...</p>"}
        </div>

        <div style="margin-top: 40px; text-align: {closing_align};">
            <p style="margin-bottom: 0.5em;">{complimentary_close}</p>
            <p style="font-weight: bold; margin: 0;">{sender_name if sender_name else "[Sender Name]"}</p>
            <p style="margin: 0; font-size: 0.9em;">{sender_title}</p>
            <p style="margin: 0; font-size: 0.9em;">{sender_company}</p>
        </div>
    </div>
    """
    return html

def get_cover_letter_html(content: str, metadata: Dict[str, Any]) -> str:
    """
    Generate HTML for cover letter preview with standard cover letter structure and styling.
    Includes sender contact block and optional online links.

    Args:
        content: The letter content string.
        metadata: Dictionary containing cover letter metadata.

    Returns:
        HTML string for cover letter preview.
    """
    # Extract metadata with default empty strings
    sender_name = metadata.get("sender_name", "")
    sender_email = metadata.get("sender_email", "")
    sender_phone = metadata.get("sender_phone", "")
    sender_location = metadata.get("sender_location", "")
    sender_linkedin = metadata.get("sender_linkedin", "")
    sender_portfolio = metadata.get("sender_portfolio", "")

    recipient_name = metadata.get("recipient_name", "")
    recipient_title = metadata.get("recipient_title", "") # Added recipient title
    recipient_company = metadata.get("recipient_company", "")
    recipient_department = metadata.get("recipient_department", "") # Added department
    recipient_address = metadata.get("recipient_address", "").replace("\n", "<br>") # Added recipient address

    date = metadata.get("date", "")
    job_title = metadata.get("job_title", "") # Added job title for subject
    salutation = metadata.get("salutation", "Dear Hiring Manager,") # Added salutation
    complimentary_close = metadata.get("complimentary_close", "Sincerely,") # Added close


    # Split content into paragraphs based on double newlines
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    # Format paragraphs as HTML <p> tags with bottom margin
    formatted_paragraphs = "".join(f"<p style='margin-bottom: 1em;'>{paragraph}</p>" for paragraph in paragraphs)

    # Construct sender contact line, only including fields that have values
    sender_contact_parts = [sender_location, sender_phone, sender_email]
    sender_contact_line = " | ".join(filter(None, sender_contact_parts))

    # Construct sender online links line, only including fields that have values
    sender_online_parts = []
    if sender_linkedin:
        # Add basic styling for links
        sender_online_parts.append(f'<a href="{sender_linkedin}" style="color: #0077b5; text-decoration: none;">LinkedIn</a>')
    if sender_portfolio:
         # Add basic styling for links
         sender_online_parts.append(f'<a href="{sender_portfolio}" style="color: #0077b5; text-decoration: none;">Portfolio</a>')

    sender_online_line = " | ".join(filter(None, sender_online_parts))


    # Basic HTML structure with inline styles for a cover letter
    # Styles aim for a clean, professional look
    html = f"""
    <div style="max-width: 800px; margin: 20px auto; padding: 30px; border: 1px solid #d0d0d0; border-radius: 8px; background-color: #ffffff; font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">

        <div style="text-align: left; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid #eee;">
            <h2 style="margin: 0; color: #333; font-size: 1.5em;">{sender_name if sender_name else "[Your Name]"}</h2>
            {'<p style="margin: 5px 0 0 0; font-size: 0.9em; color: #555;">' + sender_contact_line + '</p>' if sender_contact_line else ''}
            {'<p style="margin: 2px 0 0 0; font-size: 0.9em;">' + sender_online_line + '</p>' if sender_online_line else ''}
        </div>

        <div style="margin-bottom: 20px;">
            <p style="margin: 0;">{date if date else "[Date]"}</p>
        </div>

        <div style="margin-bottom: 20px; font-size: 0.9em;">
            <p style="margin: 0;">{recipient_name if recipient_name else "[Recipient Name]"}{', ' + recipient_title if recipient_title else ''}</p>
            <p style="margin: 0;">{recipient_department}</p>
            <p style="margin: 0;">{recipient_company if recipient_company else "[Recipient Company]"}</p>
            <p style="margin: 0;">{recipient_address if recipient_address else "[Recipient Address]"}</p>
        </div>

        <div style="margin-bottom: 20px;">
            <p style="margin: 0; font-weight: bold;">Subject: Application for {job_title if job_title else '[Job Title]'} Position</p>
        </div>

        <div style="margin-bottom: 20px;">
            <p style="margin: 0;">{salutation}</p>
        </div>

        <div style="margin-bottom: 20px;">
             {formatted_paragraphs if formatted_paragraphs else "<p style='color: #888;'>Letter content goes here...</p>"}
        </div>

        <div style="margin-top: 40px;">
            <p style="margin-bottom: 0.5em;">{complimentary_close}</p>
            <p style="font-weight: bold; margin: 0;">{sender_name}</p>
        </div>
    </div>
    """
    return html

# Example usage (for testing purposes)
if __name__ == '__main__':
    sample_personal_content = """
    Hi Sarah,

    Hope you're doing well!

    Just wanted to send a quick note to say how much I enjoyed catching up last week. It was great hearing about your trip to Italy.

    Let's try to do it again soon!

    Best,
    Emily
    """
    sample_personal_metadata = {
        "sender_name": "Emily Davis",
        "recipient_name": "Sarah Johnson",
        "date": "November 5, 2023"
    }

    sample_formal_content = """
    I am writing to formally request a copy of my academic transcript.

    I require this document for a graduate school application. The deadline for submission is December 15, 2023.

    Please let me know if there are any fees associated with this request or if any further information is needed from my end.

    Thank you for your time and assistance.
    """
    sample_formal_metadata_full_block = {
        "sender_name": "John Smith",
        "sender_title": "Student",
        "sender_organization": "University of Example",
        "sender_address": "123 University Ave\nAnytown, CA 91234",
        "sender_phone": "(555) 123-4567",
        "sender_email": "john.smith@example.com",
        "recipient_name": "Registrar's Office",
        "recipient_organization": "University of Example",
        "recipient_address": "456 Admin Building\nAnytown, CA 91234",
        "date": "November 5, 2023",
        "subject": "Request for Academic Transcript",
        "salutation": "To the Registrar's Office,",
        "complimentary_close": "Sincerely,",
        "letter_format": "Full Block"
    }

    sample_formal_metadata_modified_block = sample_formal_metadata_full_block.copy()
    sample_formal_metadata_modified_block["letter_format"] = "Modified Block"


    sample_business_content = """
    This letter confirms the details of Purchase Order #PO-7890.

    We are ordering 50 units of Model X widgets at the agreed-upon price of $100 per unit, totaling $5,000.

    Please ensure delivery to our warehouse by November 20, 2023. Payment will be made within 30 days of receipt of invoice.

    Thank you for your prompt processing of this order.
    """
    sample_business_metadata_full_block = {
        "sender_company": "Acme Corp",
        "sender_name": "Alice Brown",
        "sender_title": "Procurement Manager",
        "sender_address": "789 Business Rd\nMetropolis, NY 10001",
        "sender_phone": "(555) 987-6543",
        "sender_email": "alice.brown@acmecorp.com",
        "sender_website": "www.acmecorp.com",
        "recipient_company": "Supplier Co.",
        "recipient_name": "Sales Department",
        "recipient_title": "",
        "recipient_address": "101 Vendor Lane\nIndustriatown, TX 75001",
        "date": "November 5, 2023",
        "subject": "Purchase Order Confirmation - PO-7890",
        "salutation": "To the Sales Department,",
        "complimentary_close": "Sincerely,",
        "letter_format": "Full Block",
        "include_letterhead": True
    }

    sample_business_metadata_modified_block = sample_business_metadata_full_block.copy()
    sample_business_metadata_modified_block["letter_format"] = "Modified Block"
    sample_business_metadata_no_letterhead = sample_business_metadata_full_block.copy()
    sample_business_metadata_no_letterhead["include_letterhead"] = False


    sample_cover_letter_content = """
    I am writing to express my enthusiastic interest in the Marketing Specialist position advertised on LinkedIn.

    With three years of experience in digital marketing and a proven track record in content creation and social media management, I am confident in my ability to contribute to your team. My skills in [Specific Skill 1] and [Specific Skill 2] align perfectly with the requirements outlined in the job description.

    In my previous role at [Previous Company], I successfully managed social media campaigns that resulted in a 25% increase in engagement. I am particularly drawn to [Company Name]'s innovative approach to [Industry Trend] and believe my creative problem-solving skills would be a valuable asset.

    Thank you for considering my application. I have attached my resume for your review and welcome the opportunity to discuss how my background and skills can benefit [Company Name].
    """
    sample_cover_letter_metadata = {
        "sender_name": "Jane Doe",
        "sender_email": "jane.doe@email.com",
        "sender_phone": "(123) 456-7890",
        "sender_location": "San Francisco, CA",
        "sender_linkedin": "https://linkedin.com/in/janedoe",
        "sender_portfolio": "https://janedoeportfolio.com",
        "recipient_name": "Hiring Manager",
        "recipient_title": "", # Example with no recipient title
        "recipient_company": "Innovative Solutions Inc.",
        "recipient_department": "Marketing Department",
        "recipient_address": "456 Tech Way\nSilicon Valley, CA 95001",
        "date": "November 5, 2023",
        "job_title": "Marketing Specialist",
        "salutation": "Dear Hiring Manager,",
        "complimentary_close": "Sincerely,"
    }

    print("--- Personal Letter HTML Preview ---")
    print(get_letter_preview_html(sample_personal_content, sample_personal_metadata, letter_type="personal"))

    print("\n--- Formal Letter HTML Preview (Full Block) ---")
    print(get_letter_preview_html(sample_formal_content, sample_formal_metadata_full_block, letter_type="formal"))

    print("\n--- Formal Letter HTML Preview (Modified Block) ---")
    print(get_letter_preview_html(sample_formal_content, sample_formal_metadata_modified_block, letter_type="formal"))

    print("\n--- Business Letter HTML Preview (Full Block, with Letterhead) ---")
    print(get_letter_preview_html(sample_business_content, sample_business_metadata_full_block, letter_type="business"))

    print("\n--- Business Letter HTML Preview (Modified Block, with Letterhead) ---")
    print(get_letter_preview_html(sample_business_content, sample_business_metadata_modified_block, letter_type="business"))

    print("\n--- Business Letter HTML Preview (Full Block, no Letterhead) ---")
    print(get_letter_preview_html(sample_business_content, sample_business_metadata_no_letterhead, letter_type="business"))

    print("\n--- Cover Letter HTML Preview ---")
    print(get_letter_preview_html(sample_cover_letter_content, sample_cover_letter_metadata, letter_type="cover"))

    print("\n--- Unknown Type HTML Preview ---")
    print(get_letter_preview_html("Some random content.", {}, letter_type="unknown"))
