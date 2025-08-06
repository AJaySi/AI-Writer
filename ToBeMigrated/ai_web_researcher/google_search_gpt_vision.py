import re #additional import for regex
import os
import json
import requests
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv('OPENAI-API-KEY')
)

# Target URL can be a website url or it can google search
query = "kedarkanta trek"
target_url = f"https://www.google.com/search?q={query}&gl=us"
response = requests.get(target_url)
print
html_text = response.text

# Remove unnecessary part to prevent HUGE TOKEN cost!
# Remove everything between <head> and </head>
html_text = re.sub(r'<head.*?>.*?</head>', '', html_text, flags=re.DOTALL)
# Remove all occurrences of content between <script> and </script>
html_text = re.sub(r'<script.*?>.*?</script>', '', html_text, flags=re.DOTALL)
# Remove all occurrences of content between <style> and </style>
html_text = re.sub(r'<style.*?>.*?</style>', '', html_text, flags=re.DOTALL)

completion = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[
    {"role": "system", "content": "You are a master at scraping Google results data. Scrape two things: 1st. Scrape top 10 organic results data and 2nd. Scrape people_also_ask section from Google search result page."},
    {"role": "user", "content": html_text}
  ],
  tools=[
          {
          "type": "function",
          "function": {
            "name": "parse_organic_results",
            "description": "Parse organic results from Google SERP raw HTML data nicely",
            "parameters": {
              'type': 'object',
              'properties': {
                  'data': {
                      'type': 'array',
                      'items': {
                          'type': 'object',
                          'properties': {
                              'title': {'type': 'string'},
                              'original_url': {'type': 'string'},
                              'snippet': {'type': 'string'},
                              'position': {'type': 'integer'}
                          }
                      }
                  }
              }
            }
          }
        },
          {
          "type": "function",
          "function": {
            "name": "parse_people_also_ask_section",
            "description": "Parse `people also ask` section from Google SERP raw HTML",
            "parameters": {
              'type': 'object',
              'properties': {
                  'data': {
                      'type': 'array',
                      'items': {
                          'type': 'object',
                          'properties': {
                              'question': {'type': 'string'},
                              'original_url': {'type': 'string'},
                              'answer': {'type': 'string'},
                          }
                      }
                  }
              }
            }
          }
        }
    ],
    tool_choice="auto"
)


# Organic_results
argument_str = completion.choices[0].message.tool_calls[0].function.arguments
argument_dict = json.loads(argument_str)
organic_results = argument_dict['data']

print('Organic results:')
for result in organic_results:
    print(f"Blog Title: {result['title']}")
    print(f"Blog URL: {result['original_url']}")
    print(f"Blog Snippet: {result['snippet']}")
    print(f"Blog Position: {result['position']}")
    print('---')

# People also ask
argument_str = completion.choices[0].message.tool_calls[1].function.arguments
argument_dict = json.loads(argument_str)
people_also_ask = argument_dict['data']

print('People also ask:')
for result in people_also_ask:
    print(f"People_Also_Ask: Question: {result['question']}")
    print(f"People_Also_Ask: URL: {result['original_url']}")
    print("People_Also_Ask: Answer: {result['answer']}")
    print('---')
