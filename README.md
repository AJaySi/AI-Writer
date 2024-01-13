# AI Blog Creation and Management Toolkit

## Introduction
This toolkit automates and enhances the process of blog creation, optimization, and management. Leveraging AI technologies, it assists content creators and digital marketers in generating, formatting, and uploading blog content efficiently. The toolkit integrates advanced AI models for text generation, image creation, and data analysis, streamlining the content creation pipeline.

## Features

### Blog Generation and Optimization
- **YouTube to Blog Conversion**: Converts YouTube videos into detailed blog posts by extracting and transcribing audio, then generating text-based content. TBD: Audio to blog.

- **Online Research Integration**: Enhances blog content by integrating insights and information gathered from online research, ensuring the content is informative and up-to-date. This gives context for generating content. Tavily AI, Google search, serp and Vision AI is used to scrape web data for context augumentation. TBD: Include CrewAI for web research agents.

- **Image Generation and Processing**: Utilizes AI models like DALL-E 3, stable difffusion to create relevant images based on blog content. Offers features to process and optimize images for web usage. FIXME: Need more work with stable diffusion.

- **Write Scholarly Article**: Does search for given keywords, arxiv IDs and write review or blog on research papers. Basically, PDF to Blog.

- **Write blogs from PDFs**: TBD . The code is there, need to abstract/extract it. There is RAG with llamaindex for 'n' pdfs.
- **
- **SEO Optimization**: Employs AI to generate SEO-friendly blog titles, meta descriptions, tags, and categories. Ensures content is optimized for search engines.

- **Blog Output formats**: For easy upload to website, blogs output format can be in plaintext, HTML, Mardown/MLA format.

- **Wordpress Integration**: Implemented generating and uploading blog content, media to wordpress via its REST APIs. Most of the static website which can work with markdown style should work with little testing.
	

### Speech-to-Text Conversion
- **Audio Transcription**: Converts speech from video content into text, facilitating the creation of blogs and articles from video sources. 
- **AI models used**: OpenAI whisper model, (TBD) AssemblyAI

### AI-Driven Content Creation
- **Text Generation**: Leverages OpenAI's ChatGPT, Google Gemini Pro for generating text for blogs.
- **Customizable AI Parameters**: (FIXME) Offers flexibility in adjusting AI parameters like model selection, temperature, and token limits to suit different content needs.

### Image Detail Extraction
- **Analyzing and Extracting Image Details**: Uses OpenAI's Vision API, Google Gemini vision to analyze images and extract details such as alt text, descriptions, titles, and captions, enhancing the SEO of image content.

---

## Installation and Configuration
1. **Clone the Repository**: Clone the toolkit from the provided repository link.
2. **Install Dependencies**: Install necessary Python packages and libraries.


## Installation
---

**Note**: This toolkit is designed for automated blog management and requires appropriate API keys and access credentials for full functionality.

### 1). Prerequisites: pip install requirements.txt
```
pip install -r requirements.txt
```
---

### 2). OpenAI, Gemini API keys
Create a file .env in the present directory and include OpenAI keys.
FIXME: The code is little messed up here.

---

This is in active development and needs ironing out. The main concern is make it general purpose, for all. 
Usuability and extendibility are major concerns. This section will be updated soon. 

usage: pseo_main.py [-h] [--csv CSV] [--keywords KEYWORDS] [--youtube_urls YOUTUBE_URLS] [--scholar SCHOLAR] [--niche] [--wordpress]
                    [--output_format {plaintext,markdown,html}]

options:
  -h, --help            show this help message and exit
  --csv CSV             Provide path csv file. Check the template csv for example.
  --keywords KEYWORDS   Keywords for blog generation.
  --youtube_urls YOUTUBE_URLS
                        Comma-separated YouTube URLs for blog generation.
  --scholar SCHOLAR     Write blog from latest research papers on given keywords. Use 'arxiv_papers_url' to provide a file arxiv url
                        list.
  --niche               Flag to generate niche blogs (default: False).
  --wordpress           Flag to upload blogs to WordPress (default: False).
  --output_format {plaintext,markdown,html}
                        Output format of the blogs (default: plaintext).

---

**Example Usage:**
- **Keyword usage**: 
```
python pseo_main.py --keywords "Writesonic AI SEO-optimized blog writing,PepperType AI virtual content assistant,Copysmith AI enterprise eCommerce content,Copy AI artificial intelligence content generator,Jasper AI creative content platform,Contents generative AI content strategy"
```
**YouTube usage**: 
```
python pseo_main.py --youtube https://www.youtube.com/watch?v=yu27PWzJI_Y,https://www.youtube.com/watch?v=WGzoBD-xthI,https://www.youtube.com/watch?v=zizonToFXDs
```
**Scholar usage**: 
```
python pseo_main.py --scholar "GPT-4 Technical Report"
```

---

Notes:

1). Focus is on writing/generating highly unique, SEO optimized blog content.
2). Models: Openai, gemini, ollama are interesting. Minstral API is also worth exploring. Cohere API is purpose made.
Focus is getting the prompts right. Shit in, shit out, irrespective of dollars and cutting edge models.
Pydantically speakng, Due to experimental nature of prompting, its getting expensive soon enough. Gemini is free for now.
3). Missing frontend: A smart backend will enable a good frontend. WIP, backend. So, frontend; coming soon.
4).Getting AI agents to 'brainstrom' blog ideas seems more pressing. CrewAI seems more straightforward than autogen.
