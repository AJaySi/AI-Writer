"""
Letter Templates Module

This module provides structured templates and guidance for generating
different types and subtypes of letters.
Templates are defined as a nested dictionary containing 'structure' (list of sections)
and 'guidance' (a string) for each letter type and subtype.
"""

from typing import Dict, Any, List

# Define letter templates using a nested dictionary structure for better organization and lookup.
# The structure is {letter_type: {subtype: {template_details}}}
# 'default' subtype is used as a fallback if a specific subtype isn't found for a given type.
TEMPLATES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "personal": {
        "congratulations": {
            "structure": [
                "Greeting",
                "Express congratulations",
                "Acknowledge the achievement",
                "Share personal thoughts/memory (optional)",
                "Look to the future/well wishes",
                "Closing"
            ],
            "guidance": "Be warm, sincere, and specific about the achievement. Express genuine happiness for the recipient. Keep the tone personal and friendly."
        },
        "thank_you": {
            "structure": [
                "Greeting",
                "Express gratitude clearly",
                "Specify what you are thankful for",
                "Explain the impact or how you used it (optional)",
                "Share a personal thought or memory (optional)",
                "Offer reciprocation or look to the future",
                "Closing"
            ],
            "guidance": "Be specific about what you're thankful for and how it affected you. Express sincere appreciation. Personalize the message."
        },
        "sympathy": {
            "structure": [
                "Greeting",
                "Express sympathy for the loss",
                "Acknowledge the significance of the person/situation",
                "Share a positive memory or quality (optional)",
                "Offer specific support (optional)",
                "Closing with comforting words"
            ],
            "guidance": "Be gentle, compassionate, and sincere. Avoid clichés. Focus on offering genuine comfort and acknowledging the recipient's feelings."
        },
        "apology": {
            "structure": [
                "Greeting",
                "Clearly state your apology",
                "Acknowledge the specific mistake or action",
                "Express understanding of the impact on the other person",
                "Explain (briefly, without making excuses) what happened (optional)",
                "Offer amends or suggest how to make things right",
                "Assure it won't happen again",
                "Closing"
            ],
            "guidance": "Be sincere, take full responsibility for your actions, and focus on making things right. Avoid making excuses or blaming others."
        },
        "invitation": {
            "structure": [
                "Greeting",
                "Clearly state the invitation",
                "Provide full event details (What, When, Where)",
                "Explain the significance or purpose (optional)",
                "Mention who else might be there (optional)",
                "Request RSVP (date and contact method)",
                "Express anticipation",
                "Closing"
            ],
            "guidance": "Be clear and specific about the details (what, when, where, why). Make it easy for the person to respond."
        },
        "friendship": {
            "structure": [
                "Greeting",
                "Express appreciation for the friendship",
                "Share a recent memory or anecdote",
                "Acknowledge the value of the relationship",
                "Check in on them or share updates",
                "Look to the future (getting together, etc.)",
                "Closing"
            ],
            "guidance": "Be warm, personal, and specific about what you value in the friendship. Share updates and show genuine interest."
        },
        "love": {
            "structure": [
                "Greeting (Terms of endearment)",
                "Express depth of feelings",
                "Share a cherished memory or moment",
                "Describe specific qualities you love and appreciate",
                "Reaffirm commitment or future hopes",
                "Closing (Terms of endearment)"
            ],
            "guidance": "Be sincere, personal, and specific about your feelings. Use sensory details and emotional language appropriate for your relationship."
        },
        "encouragement": {
            "structure": [
                "Greeting",
                "Acknowledge the situation or challenge they face",
                "Express belief in their abilities/strength",
                "Offer specific words of encouragement or support",
                "Remind them of past successes (optional)",
                "Offer practical help (optional)",
                "Look to the future with hope",
                "Closing with support"
            ],
            "guidance": "Be positive, supportive, and specific about the person's strengths and abilities. Offer genuine encouragement and belief in them."
        },
        "farewell": {
            "structure": [
                "Greeting",
                "State the purpose (saying goodbye)",
                "Express feelings about their departure (sadness, happiness for them)",
                "Share a positive memory or highlight their contribution",
                "Express good wishes for their future endeavors",
                "Look to staying in touch (optional)",
                "Closing"
            ],
            "guidance": "Be warm, reflective, and forward-looking. Focus on positive memories and express genuine good wishes for their next steps."
        },
         # Default personal letter template if subtype is not found
        "default": {
            "structure": [
                "Greeting",
                "Introduction",
                "Main content paragraphs",
                "Closing thoughts",
                "Signature"
            ],
            "guidance": "Be personal, authentic, and appropriate for your relationship with the recipient. The tone is typically informal to semi-formal."
        }
    },
    "formal": {
        "application": {
            "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information (if known)",
                "Subject line (Clear and concise)",
                "Salutation (Formal)",
                "Introduction (State position applied for and where you saw it)",
                "Body paragraphs (Highlight relevant skills and experience)",
                "Closing paragraph (Reiterate interest, mention enclosed resume, call to action)",
                "Complimentary close (Formal)",
                "Signature (Typed name)",
                "Enclosures (Mention if attaching resume/portfolio)"
            ],
            "guidance": "Be professional, concise, and specific about your qualifications and genuine interest in the position. Tailor it to the specific job description."
        },
        "complaint": {
            "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information",
                "Subject line (Clearly state it's a complaint)",
                "Salutation (Formal)",
                "Introduction (State the purpose: complaint about X service/product)",
                "Problem description (Provide specific details: date, time, location, product details, names if applicable)",
                "Impact statement (Explain how the problem affected you)",
                "Requested resolution (Clearly state what you want: refund, replacement, action)",
                "Closing paragraph (Reference attached documents, state expectation for response)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Be clear, factual, and specific about the issue and your desired resolution. Maintain a respectful but firm tone. Include all relevant details."
        },
        "request": {
            "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information",
                "Subject line (Clearly state the request)",
                "Salutation (Formal)",
                "Introduction (State the purpose: making a request)",
                "Request details (Clearly explain what you are requesting)",
                "Justification (Explain why the request is necessary or beneficial)",
                "Provide supporting information (optional)",
                "Closing paragraph (Express gratitude for consideration, reiterate call to action)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Be clear, specific, and courteous about your request. Explain why it's important or beneficial to the recipient or organization."
        },
        "recommendation": {
            "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information",
                "Subject line (Letter of Recommendation for [Name])",
                "Salutation (Formal)",
                "Introduction (State your name, title, relationship to the recommendee, and for what purpose the letter is written)",
                "Body paragraphs (Describe the recommendee's qualifications, skills, and achievements with specific examples)",
                "Highlight relevant experiences and contributions",
                "Closing recommendation (Summarize endorsement, strongly recommend the person)",
                "Complimentary close (Formal)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be specific, positive, and credible. Use concrete examples and anecdotes to support your recommendation. Tailor it to the specific role/opportunity."
        },
        "resignation": {
            "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information (Immediate supervisor/HR)",
                "Subject line (Letter of Resignation - [Your Name])",
                "Salutation (Formal)",
                "Statement of resignation (Clearly state you are resigning)",
                "Last day of employment (Specify the date)",
                "Gratitude and reflection (Optional: Express thanks for the opportunity/experience)",
                "Transition plan/Offer of assistance (Optional: Suggest how to ensure a smooth handover)",
                "Closing paragraph (Express good wishes for the company's future)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Be professional, positive (if possible), and clear about your departure and last day. Maintain a good relationship."
        },
        "inquiry": {
            "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information",
                "Subject line (Clearly state the nature of the inquiry)",
                "Salutation (Formal)",
                "Introduction (State your purpose for writing - making an inquiry)",
                "Inquiry details (Provide necessary context or background)",
                "Specific questions (List your questions clearly, perhaps numbered)",
                "Closing paragraph (Express gratitude for assistance, indicate when you need a response)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Be clear, specific, and courteous about your inquiry. Organize your questions logically for easy answering."
        },
        "authorization": {
            "structure": [
                "Sender's contact information (The grantor of authority)",
                "Date",
                "Recipient's contact information (The person/entity receiving the letter)",
                "Subject line (Letter of Authorization)",
                "Salutation (Formal)",
                "Statement of authorization (Clearly state who is authorized)",
                "Authorized person's details (Full name, ID if applicable)",
                "Scope of authority (Precisely define what they are authorized to do)",
                "Limitations (Specify any restrictions or conditions)",
                "Duration of authorization (Start and end dates, if applicable)",
                "Closing paragraph (State responsibility, express confidence)",
                "Complimentary close (Formal)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be clear, specific, and precise about who is authorized, what they can do, for how long, and under what conditions. This is a legal document."
        },
        "appeal": {
            "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information (Appeals committee/relevant authority)",
                "Subject line (Letter of Appeal - [Your Name] - [Subject of Appeal])",
                "Salutation (Formal)",
                "Introduction (State your name, the decision being appealed, and the date of the decision)",
                "Grounds for appeal (Clearly state the reasons why you believe the decision is incorrect)",
                "Provide supporting evidence (Reference attached documents: records, photos, etc.)",
                "Explain mitigating circumstances (Optional)",
                "Requested outcome (Clearly state what resolution you seek)",
                "Closing paragraph (Express hope for reconsideration, gratitude for time)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Be respectful, factual, and persuasive. Focus on valid grounds for appeal and provide clear, supporting evidence. Maintain a formal tone."
        },
        "introduction": {
             "structure": [
                "Sender's contact information",
                "Date",
                "Recipient's contact information",
                "Subject line (Introduction - [Your Name])",
                "Salutation (Formal)",
                "Introduction (Introduce yourself and the purpose of the letter)",
                "Background information (Briefly describe your relevant background or expertise)",
                "Reason for reaching out (Explain why you are introducing yourself to this specific person/entity)",
                "Potential areas of collaboration or shared interest (Optional)",
                "Call to action (Suggest a meeting, call, or further communication)",
                "Closing paragraph (Express enthusiasm for potential connection)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Be professional, informative, and engaging. Clearly explain who you are, your expertise, and why you're reaching out to them specifically."
        },
        # Default formal letter template if subtype is not found
        "default": {
            "structure": [
                "Sender's address",
                "Date",
                "Recipient's address",
                "Subject line",
                "Salutation",
                "Introduction",
                "Body paragraphs",
                "Closing paragraph",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Be professional, clear, and concise. Use formal language and structure. The tone is typically formal."
        }
    },
    "business": {
        "sales": {
            "structure": [
                "Letterhead",
                "Date",
                "Recipient's address",
                "Subject line (Benefit-oriented)",
                "Salutation",
                "Attention-grabbing opening (Address a pain point or introduce a benefit)",
                "Problem statement (Briefly describe the challenge the recipient faces)",
                "Solution presentation (Introduce your product/service as the solution)",
                "Benefits and features (Explain how your solution helps, focusing on benefits)",
                "Social proof (Optional: Testimonials, case studies, data)",
                "Call to action (Clearly state what you want them to do next)",
                "Closing paragraph (Reiterate benefit, create urgency/incentive)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)",
                "Enclosures (Optional: Brochure, pricing)"
            ],
            "guidance": "Be persuasive, customer-focused, and clear about the value proposition. Focus on benefits, not just features. Make the call to action obvious."
        },
        "proposal": {
            "structure": [
                "Letterhead",
                "Date",
                "Recipient's address",
                "Subject line (Clear and descriptive)",
                "Salutation",
                "Introduction (State purpose: submitting a proposal)",
                "Problem statement/Needs assessment (Demonstrate understanding of client's needs)",
                "Proposed solution (Describe your solution in detail)",
                "Implementation plan (Outline steps and timeline)",
                "Costs and investment (Clearly state pricing and payment terms)",
                "Benefits and ROI (Explain the value the client will receive)",
                "Call to action (Suggest next steps: meeting, discussion)",
                "Closing paragraph (Express enthusiasm, availability for questions)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)",
                "Enclosures (Proposal document, appendix)"
            ],
            "guidance": "Be clear, specific, and persuasive about your solution. Focus on the client's needs and the value you provide. Structure it logically."
        },
        "order": {
            "structure": [
                "Letterhead (Your company)",
                "Date",
                "Recipient's address (Supplier)",
                "Subject line (Purchase Order - [PO Number])",
                "Salutation",
                "Introduction (Reference quote/agreement, state purpose: placing an order)",
                "Order details (Item list with quantities, descriptions, unit prices, total)",
                "Delivery requirements (Shipping address, requested delivery date, shipping method)",
                "Payment terms (Reference agreed terms)",
                "Closing paragraph (Express expectation for timely delivery)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be clear, specific, and detailed about what you're ordering, quantities, delivery requirements, and payment terms. Include a purchase order number."
        },
        "quotation": {
            "structure": [
                "Letterhead (Your company)",
                "Date",
                "Recipient's address (Customer)",
                "Subject line (Quotation for [Product/Service])",
                "Salutation",
                "Introduction (Reference inquiry, state purpose: providing a quotation)",
                "Quotation details (List items/services, descriptions, unit prices, quantities, line totals)",
                "Pricing breakdown (Mention taxes, discounts, fees separately)",
                "Terms and conditions (Payment terms, delivery terms, warranty)",
                "Validity period (State how long the quote is valid)",
                "Next steps (How they can place an order)",
                "Closing paragraph (Express hope to do business, offer further assistance)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be clear, specific, and transparent about pricing, terms, and what's included or excluded. Make it easy for the customer to understand and accept."
        },
        "acknowledgment": {
             "structure": [
                "Letterhead",
                "Date",
                "Recipient's address",
                "Subject line (Acknowledgment of [Received Item/Request])",
                "Salutation",
                "Acknowledgment statement (Clearly state what you have received or are acknowledging)",
                "Details of what's being acknowledged (Reference number, date, brief description)",
                "Confirm understanding (Optional: Briefly restate the request/issue to show understanding)",
                "Next steps (Outline what will happen next, e.g., processing order, investigating issue)",
                "Timeline (Provide an estimated timeframe if possible)",
                "Closing paragraph (Express gratitude, offer further assistance)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be prompt, clear, and specific about what you're acknowledging. Set clear expectations for next steps and timelines."
        },
         "collection": {
            "structure": [
                "Letterhead",
                "Date",
                "Recipient's address",
                "Subject line (Invoice [Invoice Number] - Payment Due)",
                "Salutation",
                "Introduction (Reference invoice number and due date)",
                "Account status (Clearly state the outstanding amount)",
                "Payment request (Politely request payment)",
                "Payment options (Remind them how to pay)",
                "Consequences of non-payment (Optional: Briefly mention late fees or further action, depending on letter stage)",
                "Call to action (Request payment by a specific date)",
                "Closing paragraph (Express hope for prompt payment, offer to discuss)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be firm but professional. Clearly state the amount due, due date, and payment options. The tone may vary depending on how overdue the payment is."
        },
         "adjustment": {
            "structure": [
                "Letterhead",
                "Date",
                "Recipient's address (Customer who made a complaint)",
                "Subject line (Response to your inquiry - [Reference Number])",
                "Salutation",
                "Acknowledgment of complaint (Reference their communication and the issue)",
                "Investigation findings (Explain the outcome of your investigation)",
                "Adjustment offered (Clearly state the resolution: refund, replacement, credit, etc.)",
                "Apology (Optional: Express regret for the inconvenience)",
                "Preventive measures (Optional: Explain steps taken to prevent recurrence)",
                "Closing paragraph (Express hope for continued business, offer further assistance)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be responsive, empathetic, and solution-oriented. Clearly explain the adjustment and any preventive measures taken."
        },
        "credit": {
            "structure": [
                "Letterhead",
                "Date",
                "Recipient's address (Applicant)",
                "Subject line (Credit Application Status - [Applicant Name])",
                "Salutation",
                "Introduction (Reference their credit application and the purpose of the letter)",
                "Credit decision (Clearly state if credit is approved or denied)",
                "If approved: Credit terms (Credit limit, payment terms, interest rates)",
                "If denied: Reason for decision (Provide specific, compliant reasons)",
                "Requirements (If approved: any further steps or documents needed)",
                "Closing paragraph (If approved: Express welcome; If denied: Offer alternative options or appeals process)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be clear, specific, and transparent about the credit decision, terms, limits, or reasons for denial. Ensure compliance with regulations if denying credit."
        },
        "follow_up": {
            "structure": [
                "Letterhead",
                "Date",
                "Recipient's address",
                "Subject line (Following up on [Previous Communication/Meeting])",
                "Salutation",
                "Reference to previous communication (Mention date, topic, or meeting)",
                "Purpose of follow-up (Clearly state why you are writing again)",
                "Action items/Next steps (Remind of agreed-upon actions or propose next steps)",
                "Provide additional information (Optional)",
                "Call to action (If applicable, e.g., request a response, schedule a meeting)",
                "Closing paragraph (Reiterate interest, express anticipation)",
                "Complimentary close (Professional)",
                "Signature (Typed name and title)"
            ],
            "guidance": "Be clear, specific, and action-oriented. Reference previous communication and clearly state the purpose of your follow-up and desired outcome."
        },
         # Default business letter template if subtype is not found
        "default": {
            "structure": [
                "Letterhead",
                "Date",
                "Recipient's address",
                "Subject line",
                "Salutation",
                "Introduction",
                "Body paragraphs",
                "Closing paragraph",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Be professional, clear, and concise. Focus on the business purpose of your letter. The tone is typically formal to semi-formal."
        }
    },
     "cover": {
        "standard": {
            "structure": [
                "Your contact information",
                "Date",
                "Hiring Manager contact information (if known)",
                "Subject line (Job Application - [Your Name] - [Job Title])",
                "Salutation (Formal)",
                "Introduction (State the position you are applying for, where you saw the advertisement, and a brief statement of enthusiasm)",
                "Body paragraph 1 (Highlight skills and experience directly relevant to the job description - often 1-2 key qualifications)",
                "Body paragraph 2 (Provide a specific example or anecdote demonstrating your abilities)",
                "Body paragraph 3 (Connect your passion/goals to the company's mission/values - optional but effective)",
                "Closing paragraph (Reiterate interest, mention enclosed resume, call to action)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Be professional, specific about your most relevant qualifications, and clear about your interest in the position. Tailor every cover letter to the specific job and company."
        },
        "career_change": {
            "structure": [
                "Your contact information",
                "Date",
                "Hiring Manager contact information",
                "Subject line (Job Application - [Your Name] - [Job Title])",
                "Salutation",
                "Introduction (State the position and acknowledge your career transition)",
                "Body paragraph 1 (Highlight transferable skills from previous roles)",
                "Body paragraph 2 (Explain your motivation for the career change and how your skills apply)",
                "Body paragraph 3 (Demonstrate understanding of the new industry/role)",
                "Closing paragraph (Reiterate enthusiasm, mention enclosed resume, call to action)",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Focus on transferable skills and explain your career transition. Connect your past experience and new skills directly to the requirements of the target role."
        },
        "entry_level": {
            "structure": [
                "Your contact information",
                "Date",
                "Hiring Manager contact information",
                "Subject line (Job Application - [Your Name] - [Job Title])",
                "Salutation",
                "Introduction (State the position and your enthusiasm for the opportunity as a recent graduate/entrant)",
                "Body paragraph 1 (Highlight relevant education, coursework, GPA if strong)",
                "Body paragraph 2 (Describe relevant internships, projects, or volunteer experience)",
                "Body paragraph 3 (Showcase soft skills: teamwork, communication, eagerness to learn)",
                "Closing paragraph (Reiterate interest, mention attached resume, express availability for interview)",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Emphasize education, relevant internships/projects, and transferable skills gained through academic or extracurricular activities. Show strong potential and enthusiasm."
        },
        "executive": {
            "structure": [
                "Your contact information",
                "Date",
                "Recipient's contact information (Senior Executive/Board Member)",
                "Subject line (Executive Application - [Your Name] - [Position])",
                "Salutation (Formal)",
                "Introduction (State position applying for, brief summary of executive profile)",
                "Body paragraph 1 (Highlight strategic leadership experience and key achievements)",
                "Body paragraph 2 (Discuss relevant industry expertise and market insights)",
                "Body paragraph 3 (Describe experience in driving growth, managing teams, achieving results)",
                "Closing paragraph (Reiterate interest, express desire to discuss contribution to the organization)",
                "Complimentary close (Formal)",
                "Signature"
            ],
            "guidance": "Emphasize strategic leadership experience, significant achievements with measurable results, and industry expertise. Use a confident, authoritative, and forward-looking tone."
        },
        "creative": {
            "structure": [
                "Your contact information",
                "Date",
                "Hiring Manager contact information",
                "Subject line (Application - [Your Name] - [Creative Role])",
                "Salutation",
                "Creative introduction (Engaging hook related to the role or your passion)",
                "Body paragraph 1 (Highlight relevant creative experience and skills)",
                "Body paragraph 2 (Reference specific portfolio pieces or projects that showcase your style/abilities)",
                "Body paragraph 3 (Describe your creative process or approach)",
                "Closing paragraph (Reiterate enthusiasm, mention attached resume/portfolio link, call to action)",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Use a more engaging and expressive style appropriate for a creative role while maintaining professionalism. Highlight specific creative achievements and link to your portfolio."
        },
        "technical": {
            "structure": [
                "Your contact information",
                "Date",
                "Hiring Manager contact information",
                "Subject line (Application - [Your Name] - [Technical Role])",
                "Salutation (Formal)",
                "Introduction (State position, source, and brief technical interest)",
                "Body paragraph 1 (Highlight specific technical skills and proficiencies relevant to the job description)",
                "Body paragraph 2 (Describe relevant technical projects or challenges you've solved)",
                "Body paragraph 3 (Discuss problem-solving abilities and experience with relevant technologies)",
                "Closing paragraph (Reiterate interest, mention attached resume, express availability for technical discussion/interview)",
                "Complimentary close (Formal)",
                "Signature"
            ],
            "guidance": "Focus on technical skills, relevant projects, and problem-solving abilities. Use appropriate technical terminology accurately."
        },
         "academic": {
            "structure": [
                "Your contact information",
                "Date",
                "Recipient's contact information (Search Committee Chair)",
                "Subject line (Application for [Position] - [Your Name])",
                "Salutation (Formal)",
                "Introduction (State the position, the department, and express your strong interest)",
                "Body paragraph 1 (Discuss your research experience, focus on key projects and contributions)",
                "Body paragraph 2 (Describe your teaching philosophy and relevant teaching experience)",
                "Body paragraph 3 (Mention publications, presentations, grants, and other scholarly contributions)",
                "Closing paragraph (Reiterate enthusiasm for joining the faculty, express availability for interview/presentation)",
                "Complimentary close (Formal)",
                "Signature (Typed name)"
            ],
            "guidance": "Focus on research experience, teaching philosophy, publications, and contributions to the field. Use a scholarly and professional tone suitable for academia."
        },
        "remote": {
             "structure": [
                "Your contact information",
                "Date",
                "Hiring Manager contact information",
                "Subject line (Remote Application - [Your Name] - [Job Title])",
                "Salutation",
                "Introduction (State the remote position, source, and enthusiasm for remote work)",
                "Body paragraph 1 (Highlight experience working remotely or independently)",
                "Body paragraph 2 (Emphasize self-management, time management, and organizational skills required for remote work)",
                "Body paragraph 3 (Describe strong written and verbal communication skills, essential for remote collaboration)",
                "Closing paragraph (Reiterate interest in the remote role, mention attached resume, express availability for video interview)",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Emphasize self-motivation, excellent communication skills (especially written), time management, and any prior experience working independently or in remote teams."
        },
        "referral": {
            "structure": [
                "Your contact information",
                "Date",
                "Hiring Manager contact information",
                "Subject line (Referral Application - [Your Name] - [Job Title] - Referred by [Referrer's Name])",
                "Salutation",
                "Referral introduction (Immediately state who referred you and for what position)",
                "Body paragraph 1 (Briefly explain your connection to the referrer and how you learned about the role)",
                "Body paragraph 2 (Highlight key qualifications relevant to the job description)",
                "Body paragraph 3 (Express strong interest in the position and the company)",
                "Closing paragraph (Reiterate enthusiasm, mention attached resume, express availability for interview)",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Mention the referral prominently and early. Explain your connection to the referrer and how it aligns with your interest in the role. Still, ensure you highlight your own qualifications."
        },
        # Default cover letter template if subtype is not found
        "default": {
            "structure": [
                "Contact information",
                "Date",
                "Recipient's information",
                "Salutation",
                "Introduction",
                "Body paragraphs",
                "Closing paragraph",
                "Complimentary close",
                "Signature"
            ],
            "guidance": "Be professional, specific about your qualifications, and clear about your interest in the position. Tailor your letter to the specific job and company."
        }
     },
     # Overall default template if letter type is not recognized
    "default": {
        "structure": [
            "Introduction",
            "Body",
            "Conclusion"
        ],
        "guidance": "Be clear, concise, and appropriate for your audience and purpose. This is a generic structure."
    }
}


def get_template_by_type(letter_type: str, subtype: str = "default") -> Dict[str, Any]:
    """
    Get a template for a specific letter type and subtype using a dictionary lookup.

    Args:
        letter_type: Type of letter (e.g., "personal", "formal", "business", "cover").
        subtype: Subtype of letter (e.g., "congratulations", "application", "sales").
                 Defaults to "default" if no subtype is specified.

    Returns:
        Template dictionary with 'structure' (List[str]) and 'guidance' (str).
        Returns the default template if the letter type or subtype is not found,
        ensuring the return structure is always consistent.
    """
    # Get templates for the specific letter type, or the overall default templates
    # .get() method is used for safe dictionary access with a default fallback
    type_templates = TEMPLATES.get(letter_type, TEMPLATES["default"])

    # Get the template for the specific subtype, or the default for that letter type
    # Chain .get() calls to handle cases where subtype or the type's default is missing
    template = type_templates.get(subtype, type_templates.get("default", TEMPLATES["default"]))

    # Ensure the returned template always has 'structure' (as a list) and 'guidance' (as a string) keys.
    # This adds robustness in case a template definition is incomplete.
    if "structure" not in template or not isinstance(template["structure"], list):
         # Fallback structure if missing or incorrect type
         template["structure"] = ["Introduction", "Body", "Conclusion"]
         # Update guidance to reflect that the structure was defaulted
         template["guidance"] = "Generic template structure applied due to missing or invalid definition."

    if "guidance" not in template or not isinstance(template["guidance"], str):
         # Fallback guidance if missing or incorrect type
         template["guidance"] = "Generic guidance applied due to missing or invalid definition."


    return template

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Test cases to demonstrate functionality and default handling
    print("--- Testing Letter Templates Module ---")

    # Test a known personal letter subtype
    personal_congrats = get_template_by_type("personal", "congratulations")
    print("\nPersonal Congratulations Template:")
    print(f"Structure: {personal_congrats['structure']}")
    print(f"Guidance: {personal_congrats['guidance']}")

    # Test a known formal letter subtype
    formal_complaint = get_template_by_type("formal", "complaint")
    print("\nFormal Complaint Template:")
    print(f"Structure: {formal_complaint['structure']}")
    print(f"Guidance: {formal_complaint['guidance']}")

    # Test a known business letter subtype
    business_sales = get_template_by_type("business", "sales")
    print("\nBusiness Sales Template:")
    print(f"Structure: {business_sales['structure']}")
    print(f"Guidance: {business_sales['guidance']}")

    # Test a known cover letter subtype
    cover_entry_level = get_template_by_type("cover", "entry_level")
    print("\nCover Entry Level Template:")
    print(f"Structure: {cover_entry_level['structure']}")
    print(f"Guidance: {cover_entry_level['guidance']}")

    # Test an unknown letter type (should fallback to overall default)
    unknown_type = get_template_by_type("unknown_type", "some_subtype")
    print("\nUnknown Type Template (Should be Overall Default):")
    print(f"Structure: {unknown_type['structure']}")
    print(f"Guidance: {unknown_type['guidance']}")

    # Test a known letter type but unknown subtype (should fallback to type's default)
    personal_unknown_subtype = get_template_by_type("personal", "unknown_subtype")
    print("\nPersonal Unknown Subtype Template (Should be Personal Default):")
    print(f"Structure: {personal_unknown_subtype['structure']}")
    print(f"Guidance: {personal_unknown_subtype['guidance']}")

    # Test with only letter type (should use type's default)
    formal_default = get_template_by_type("formal")
    print("\nFormal Default Template (No Subtype Specified):")
    print(f"Structure: {formal_default['structure']}")
    print(f"Guidance: {formal_default['guidance']}")
