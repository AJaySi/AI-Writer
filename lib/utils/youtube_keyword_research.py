"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import os
import sys

import google.generativeai as genai

def research_yt(keywords):
    """ Research top youtube videos for given keywords """
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    except Exception as err:
        print("Google Gemini Error: {err}")

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

    prompt_parts = [f"Research 5 latest youtube urls on {keywords}, released this week. Check the number of views and also get the references from youtube video description. REMEMBER to make sure, your response urls are available and valid. For each result, visit their webpages to write detailed quickstart code samples, preferably in python. Your response urls should consist of trending topics on latest {keywords}. Your response should be in json format, so that i can easily parse all the fields. For consistency, always use json key names as Title, URL, Views, References and Quickstart_Code."]

    try:
        response = model.generate_content(prompt_parts)
    except Exception as err:
        print(f"Failed to get response from Gemini Pro.{response}")
        sys.exit(1)

    return response.text
