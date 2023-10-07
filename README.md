## Introduction

Given high level domain keywords like "Fishing baits online" Or any 2-3 main key words that describe, broadly, your business.
This tool will produce a SEO optimized blogs. This tool will suggest most popular blog topics, divide them in sub topics and write content for each sub topic. For each of the paragraphs, we summarise it and pass the line for text to image.
Thus, the generated blog will have text and relevant images.

(TBD) Provide the blog output as plain text, markdown Or HTML.

Presently, wordpress and WIX integration is present for uploading the generated blog, but needs testing.

### This is based on openai gpt models for content generation, google bard for keyword research and some basic tools for plagiarism checker, SEO audit and suggestions to improve the generated content.
As prompts are the important ingredients to get the best result, they are stored in prompts folder. Edit these prompts to produce results as per your likings.

### API based blog generation are much cheaper, almost 10x, but difficult to use for everyone. We use bard for search related prompts and chatgpt for generative requirements.

### Check TBD for features currently under development.

### Amazon affiliate links are also supported. Given, affiliate tag, your affiliate product links will included in the blogs.
To use the module, simply create an instance of the AmazonAffiliateImages class, passing in your Amazon affiliate tag. 
Then, you can use the get_image_url() or get_image_html() methods to get the Amazon affiliate image URL or HTML 
for a product, passing in either the product ASIN or the product URL.

----------------------------------

## How to use this tool

*Prerequisites: pip install requirements.txt

This is in active development and needs ironing out. The main concern is make it general purpose, for all. 
Usuability and extendibility are major concerns. This section will be updated soon. 

python3 pseo_main.py -h
usage: pseo_main.py [-h] [--num_blogs NUM_BLOGS] --keywords KEYWORDS [--niche NICHE]

Accepts user input for the number of blogs, keywords, and niche.

options:
  -h, --help            show this help message and exit
  --num_blogs NUM_BLOGS
                        The number of blogs (default: 1).
  --keywords KEYWORDS   The keywords.
  --niche NICHE         Whether the blog is a niche blog (default: False).

*Example:
python3 pseo_main.py --num_blogs "10" --keywords Python, programming, data science --niche True

----------------------------------

# The detailed SEO checks are as follows:

- Keyword Density
- Keyword Presence in Title
- Keyword Presence in Image Alt Text
- Headings Text
- Internal Links
- External Links
- Readability Score
- Spelling Errors
- Grammar Errors
- SEO Score
- SEO Suggestions to improve generated content

-----------------------------------

# What to write on ?

This is basically keyword research for a specific domain, narrowed down by blog topics.
We can craft prompts to get an idea on what to generate blogs on. Divide them in topic and write for most searched ones, as below:

#[Prompts]
For more details on prompts used to get blog topics and SEO keyword research, check file blog_ideas.prompts in prompts folder.

