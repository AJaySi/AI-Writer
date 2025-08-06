import streamlit as st
import json

from ..gpt_providers.text_generation.main_text_generation import llm_text_gen


def generate_product_description(title, details, audience, tone, length, keywords):
    """
    Generates a product description using OpenAI's API.

    Args:
        title (str): The title of the product.
        details (list): A list of product details (features, benefits, etc.).
        audience (list): A list of target audience segments.
        tone (str): The desired tone of the description (e.g., "Formal", "Informal").
        length (str): The desired length of the description (e.g., "short", "medium", "long").
        keywords (str): Keywords related to the product (comma-separated).

    Returns:
        str: The generated product description.
    """
    prompt = f"""
        Write a compelling product description for {title}.

        Highlight these key features: {', '.join(details)} 

        Emphasize the benefits of these features for the target audience ({audience}). 
        Maintain a {tone} tone and aim for a length of approximately {length} words.

        Use these keywords naturally throughout the description: {', '.join(keywords)}.

        Remember to be persuasive and focus on the value proposition.
    """
    
    try:
        response = llm_text_gen(prompt)
        return response
    except Exception as err:
        logger.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)


def display_inputs():
    st.title("📝 AI Product Description Writer 🚀")
    st.markdown("**Generate compelling and accurate product descriptions with AI.**")

    col1, col2 = st.columns(2)

    with col1:
        product_title = st.text_input("🏷️ **Product Title**", placeholder="Enter the product title (e.g., Wireless Bluetooth Headphones)")
    with col2:
        product_details = st.text_area("📄 **Product Details**", placeholder="Enter features, benefits, specifications, materials, etc. (e.g., Noise Cancellation, Long Battery Life, Water Resistant, Comfortable Design)")

    col3, col4 = st.columns(2)

    with col3:
        keywords = st.text_input("🔑 **Keywords**", placeholder="Enter keywords, comma-separated (e.g., wireless headphones, noise cancelling, Bluetooth 5.0)")
    with col4:
        target_audience = st.multiselect(
            "🎯 **Target Audience**",
            ["Teens", "Adults", "Seniors", "Music Lovers", "Fitness Enthusiasts", "Tech Savvy", "Busy Professionals", "Travelers", "Casual Users"],
            placeholder="Select target audience (optional)"
        )

    col5, col6 = st.columns(2)

    with col5:
        description_length = st.selectbox(
            "📏 **Desired Description Length**",
            ["Short (1-2 sentences)", "Medium (3-5 sentences)", "Long (6+ sentences)"],
            help="Select the desired length of the product description"
        )
    with col6:
        brand_tone = st.selectbox(
            "🎨 **Brand Tone**",
            ["Formal", "Informal", "Fun & Energetic"],
            help="Select the desired tone for the description"
        )

    return product_title, product_details, target_audience, brand_tone, description_length, keywords


def display_output(description):
    if description:
        st.subheader("✨ Generated Product Description:")
        st.write(description)

        json_ld = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": product_title,
            "description": description,
            "audience": target_audience,
            "brand": {
                "@type": "Brand",
                "name": "Your Brand Name"
            },
            "keywords": keywords.split(", ")
        }


def write_ai_prod_desc():
    product_title, product_details, target_audience, brand_tone, description_length, keywords = display_inputs()

    if st.button("Generate Product Description 🚀"):
        with st.spinner("Generating description..."):
            description = generate_product_description(
                product_title,
                product_details.split(", "),  # Split details into a list
                target_audience,
                brand_tone,
                description_length.split(" ")[0].lower(),  # Extract length from selectbox
                keywords
            )
            display_output(description)
