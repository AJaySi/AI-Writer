# AI Blog Creation and Management Toolkit

## Introduction
This toolkit automates and enhances the process of blog creation, optimization, and management. Leveraging AI technologies, it assists content creators and digital marketers in generating, formatting, and uploading blog content efficiently. The toolkit integrates advanced AI models for text generation, image creation, and data analysis, streamlining the content creation pipeline.

## Getting Started

To use this tool, follow these steps:

### Option 1: Local laptop Install: (I know what I am doing..)

Step 1. Clone this repository to your local machine (Take google's help, if this sentence makes less sense).

Step 2. Install the required dependencies using:<br>
On your local machine's command prompt, navigate to the folder where you completed Step 1.
Now Run the below command:<br>
`pip install -r requirements.txt`

Step 3. Run the script by executing `python alwrity.py`.
Step 4. Once the tools is running it will guide/ask for your APIs. It will provide you with links to sign for APIs.

---
### Option 2: Cloud install: (I just want to write blogs..)

Step 1). Make efforts to fork this present repo into your own accounts.

Step 2). Follow this guide: <br>
https://docs.replit.com/programming-ide/using-git-on-replit/running-github-repositories-replit

---
## Features

- **Online Research Integration**: Enhances blog content by integrating insights and information gathered from online research, ensuring the content is informative and up-to-date. This gives context for generating content. Tavily AI, Google search, serp and Vision AI is used to scrape web data for context augumentation. TBD: Include CrewAI for web research agents.

- **Image Generation and Processing**: Utilizes AI models like DALL-E 3, stable difffusion to create relevant images based on blog content. Offers features to process and optimize images for web usage. FIXME: Need more work with stable diffusion.

- **SEO Optimization**: Employs AI to generate SEO-friendly blog titles, meta descriptions, tags, and categories. Ensures content is optimized for search engines.

- **Wordpress, Jekyll Integration**: Implemented generating and uploading blog content, media to wordpress via its REST APIs. Most of the static website which can work with markdown style should work with little testing.
	

### AI-Driven Content Creation
- **Text Generation**: Leverages OpenAI's ChatGPT, Google Gemini Pro for generating text for blogs.
- **Customizable AI Parameters**: (FIXME) Offers flexibility in adjusting AI parameters like model selection, temperature, and token limits to suit different content needs.

### Image Detail Extraction
- **Analyzing and Extracting Image Details**: Uses OpenAI's Vision API, Google Gemini vision to analyze images and extract details such as alt text, descriptions, titles, and captions, enhancing the SEO of image content.

---
**Note**: This toolkit is designed for automated blog management and requires appropriate API keys and access credentials for full functionality.
---

### Web Research
- **Keyword Research**: Conduct in-depth keyword research by specifying search queries and time ranges.
- **Domain-Specific Searches**: Include specific URLs to confine searches to certain domains, such as Wikipedia or competitor websites.
- **Semantic Analysis**: Explore similar topics and technologies by providing a reference URL for semantic analysis.

### Competitor Analysis
- **Similar Company Discovery**: Analyze competitor websites to discover similar companies, startups, and technologies.
- **Industry Insights**: Gain insights into industry trends, market competitors, and emerging technologies.

### Blog Writing
- **Keyword-Based Blogs**: Generate blog content based on specified keywords, leveraging AI to produce engaging and informative articles.
- **Audio Blog Generation**: Convert audio from YouTube videos into blog posts, facilitating content creation from multimedia sources.
- **GitHub Repository Blogs**: Transform GitHub repositories or topics into blog posts, showcasing code examples and project insights.
- **Scholarly Research Blogs**: Generate blog content based on research papers, summarizing key findings and insights.

### Blogging Tools
- **Title and Meta Description Generation**: Generate catchy titles and meta descriptions for blog posts to improve SEO and user engagement.
- **Blog Outline Creation**: Generate outlines for blog posts, aiding in structuring content and organizing ideas.
- **FAQ Generation**: Automatically generate FAQs (Frequently Asked Questions) based on blog content, enhancing user engagement and SEO.
- **HTML and Markdown Conversion**: Convert blog posts between HTML and Markdown formats for easy integration with various platforms.
- **Blog Proofreading**: Proofread blog content for grammar, spelling, and readability, ensuring high-quality output.
- **Tag and Category Suggestions**: Generate tags and categories for blog posts based on content analysis, improving organization and discoverability.

### Interactive Mode
- **User-Friendly Interface**: Navigate tasks and options easily through an interactive command-line interface.
- **Menu-Driven Interaction**: Choose between various options, tasks, and tools using intuitive menus and prompts.
- **Task Guidance**: Receive guidance and instructions for each task, facilitating user interaction and decision-making.

## Packages, Tools, and APIs Used

- **Libraries**:
  - PyInquirer: For creating interactive command-line interfaces.
  - Typer: For building CLI applications with ease.
  - Tabulate: For formatting data in tabular form.
  - Requests: For making HTTP requests to web APIs.
  - python-dotenv: For loading environment variables from a .env file.

- **APIs**:
  - Metaphor API: Provides semantic search capabilities for finding similar topics and technologies.
  - Tavily API: Offers AI-powered web search functionality for conducting in-depth keyword research.
  - SerperDev API: Enables access to search engine results and competitor analysis data.
  - OpenAI API: Powers the Large Language Models (LLMs) for generating blog content and conducting research.
  - Gemini API: Another LLM provider for natural language processing tasks.
  - Ollama API (Work In Progress): An upcoming LLM provider for additional research and content generation capabilities.

---

Notes:

1). Focus is on writing/generating highly unique, SEO optimized blog content.
2). Models: Openai, gemini, ollama are interesting. Minstral API is also worth exploring. Cohere API is purpose made.
Focus is getting the prompts right. Shit in, shit out, irrespective of dollars and cutting edge models.
Pydantically speakng, Due to experimental nature of prompting, its getting expensive soon enough. Gemini is free for now.
3). Missing frontend: A smart backend will enable a good frontend. WIP, backend. So, frontend; coming soon.
4).Getting AI agents to 'brainstrom' blog ideas seems more pressing. CrewAI seems more straightforward than autogen.
5). Too Many APIs floating around: The implementation is using tools that dont depend on API keys and rather scrape them.
Duh, scraping wont scale, that is GPT vision based scraping will come in handy.
