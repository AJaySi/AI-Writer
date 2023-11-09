import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def gen_ecomm_product_desc(product_name):
    """Given a product name, generate relevant content for blogging.
    """

    product_desc = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
            "content": """Act as an expert E-commerce copywriter specializing in content optimization for SEO. As an E-commerce SEO expert who writes compelling product descriptions for users looking to buy online. I am going to provide the title of one e-commerce product and I want you to come up with a minimum of three distinct content sections for the product description, each section about a unique subset of keywords relating to the product I provide you. Make sure that each of the unique content sections are labeled with an informative and eye-catching subheading describing the main focus of the content section. The main point of these commands is for you to developing a new keyword-rich, informative, and captivating product summary/description that is less than 1000 words. The purpose of product description is marketing the products to users looking to buy. Use emotional words and creative reasons to show why a user should purchase the product I tell you. After you generate the new product summary, please generate a bulleted list of 5 possible H1 headings for this product page, and make each H1 less than 7 words each. Please also include bulleted list of broad match keywords that were used to accomplish writing the product summary. Write a persuasive and professional sounding Meta Title and Description that integrates similar language present in the new product summary text. Make sure to include a numerical aspect in the Meta Title. Do not echo my prompt. Do not remind me what I asked you for. Do not apologize. Do not self-reference."""
            },
            {
                "role": "user",
                "content": f"""Craft blog content for following e commerce product.
                Product: {product_name}""",
            },
        ],
        max_tokens=4096,
        temperature=1,
    )

  if "choices" in product_desc and len(product_desc["choices"]) > 0:
    return product_desc["choices"][0]["message"]["content"]
  else:
    return None
