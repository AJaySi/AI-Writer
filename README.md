# AI Blog Creation and Management Toolkit

## Introduction
This toolkit automates and enhances the process of blog creation, optimization, and management. Leveraging AI technologies, it assists content creators and digital marketers in generating, formatting, and uploading blog content efficiently. The toolkit integrates advanced AI models for text generation, image creation, and data analysis, streamlining the content creation pipeline.

## Features

### Blog Generation and Optimization
- **YouTube to Blog Conversion**: Converts YouTube videos into detailed blog posts by extracting and transcribing audio, then generating text-based content.
- **Online Research Integration**: Enhances blog content by integrating insights and information gathered from online research, ensuring the content is informative and up-to-date.
- **Image Generation and Processing**: Utilizes AI models like DALL-E 3 to create relevant images based on blog content. Offers features to process and optimize images for web usage.
- **SEO Optimization**: Employs AI to generate SEO-friendly blog titles, meta descriptions, tags, and categories. Ensures content is optimized for search engines.

### Speech-to-Text Conversion
- **Audio Transcription**: Converts speech from video content into text, facilitating the creation of blogs and articles from video sources.

### AI-Driven Content Creation
- **Text Generation with OpenAI ChatGPT**: Leverages OpenAI's ChatGPT for generating creative and relevant text for blogs.
- **Customizable AI Parameters**: Offers flexibility in adjusting AI parameters like model selection, temperature, and token limits to suit different content needs.

### Image Detail Extraction
- **Analyzing and Extracting Image Details**: Uses OpenAI's Vision API to analyze images and extract details such as alt text, descriptions, titles, and captions, enhancing the SEO of image content.


## Installation and Configuration
1. **Clone the Repository**: Clone the toolkit from the provided repository link.
2. **Install Dependencies**: Install necessary Python packages and libraries.


## Usage
The toolkit provides functions for generating blogs from YouTube videos, detailed blogs from provided keywords, and optimizing them for SEO and readability. It supports content uploading to WordPress and includes comprehensive error handling.

## Installation
- Requires Python 3.x.
- Install dependencies: `openai`, `nltk`, `tqdm`, `loguru`.
- Set up API keys and credentials for OpenAI and WordPress.

---

**Note**: This toolkit is designed for automated blog management and requires appropriate API keys and access credentials for full functionality.

----------------------------------

## How to use this tool

### Prerequisites: pip install requirements.txt

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

- Example:
python3 pseo_main.py --num_blogs "10" --keywords "Python, programming, data science" --niche True


-----------------------------------

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

