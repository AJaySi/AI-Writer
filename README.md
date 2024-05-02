# How to Use AI Content Generation Toolkit - Alwrity

1). [Visit alwrity.com](https://www.alwrity.com/ai-writing-tools), You will find AI content writing tools, which are Free & No-Signup.
**Note:** Although, this is limited, as is our wallet & Resources.

2). **For complete AI content creation toolkit**, alwrity offers a commandline App. Its a BYOK model(Bring Your Own Key).
**Note:** (🗯️ commandline, byok and shit) ... Now, before you run away 🏃💨   

If you have 💻 Laptop + 🛜 Internet + 20 minutes, you will be generating blogs, articles etc with just few words.

### [Step-By-Step: Getting Started for Absolute Begginers](https://www.alwrity.com/post/getting-started-with-alwrity-ai-writer)

### [Getting started for Developers](https://github.com/AJaySi/AI-Writer/wiki/Alwrity--%E2%80%90-Get-started)

**If you still Get stuck, Open a issue here & say pretty please** :: https://github.com/AJaySi/AI-Writer/issues

---
# AI Content Generation Toolkit - Alwrity
![](https://github.com/AJaySi/AI-Writer/blob/main/lib/workspace/keyword_blog.gif)

## Introduction

Alwrity automates and enhances the process of blog creation, optimization, and management(Really ?). 
Leveraging AI technologies, it assists content creators and digital marketers in generating, formatting, 
and uploading blog content efficiently(Hmmmm, OK...). 
The toolkit integrates advanced AI models for text generation, image creation, 
and data analysis, streamlining the content creation pipeline(Who reads introductions, right!).

## [Read Alwrity Configuration Options](https://www.alwrity.com/post/know-powerful-alwrity-ai-writer-configuration):
Use the [main_config](https://github.com/AJaySi/AI-Writer/blob/main/main_config) file to modify Alwrity behavior for your content needs.

---

## Under the hood:

### Tech-Stack on the shoulders of Giants - (Credits):
- **APIs**:
  - [Exa API](https://exa.ai/): Provides semantic search capabilities for finding similar topics and technologies.
  - [Tavily API](https://tavily.com/): Offers AI-powered web search functionality for conducting in-depth keyword research.
  - [SerperDev API](https://serper.dev/): Enables access to search engine results and competitor analysis data.
  - [YOU.com](https://you.com/): You.com enhances web search, writing, coding, digital art creation, and solving complex problems.
  - [Stability AI](https://stability.ai/): Activating humanity's potential through generative AI. 
    Open models in every modality, for everyone, everywhere.
  - [OpenAI API](https://openai.com/): Powers the Large Language Models (LLMs) for generating blog content and conducting research.
  - [Gemini API](https://gemini.google.com/app): Google powered LLM for natural language processing tasks.
  - [Ollama](https://ollama.com/) : Local, Privacy focused, LLM provider for research and content generation capabilities.
  - [CrewAI](https://www.crewai.com/): Collaborative AI agents framework.
---

## Features

- **Online Research Integration**: Enhances blog content by integrating insights and information gathered from online research(SERP, Tavily, Metaphor), ensuring the content is informative and up-to-date. 
This gives context for generating content. Tavily AI, Google search, serp and Vision AI is used to scrape web data for context augumentation. CrewAI for web research agents.

- **Long Form Content Generation**: Write Essay, Story, Long form Blogs with web researched context.

- **AI Content planning & Calender**: Writer's block, Alwrity will provide you with months worth of blog titles.

- **Multilingual**: Write Content in your language, web research in your language and country(main_config).

- **Prevents AI Hallucinations**: Web researched context generates factual content.

- **Text-To-Text, Speech-To-Text, Text-To-Image, Image-To-Text**: Multimodal content generatiom suite.

- **Agentic Content Team**: Crewai content team for you company. Define persona, roles, goals, task for your AI content team(Beta). 

- **Image Generation and Processing**: Utilizes AI models like DALL-E 3, stable difffusion to create relevant images based on blog content. Offers features to process and optimize images for web usage. FIXME: Need more work with stable diffusion.

- **SEO Optimization**: Employs AI to generate SEO-friendly blog titles, meta descriptions, tags, and categories. Ensures content is optimized for search engines.

- **Wordpress, Jekyll Integration**: Implemented generating and uploading blog content, media to wordpress via its REST APIs. Most of the static website which can work with markdown style should work with little testing.
	

### AI-Driven Content Creation

- **Text Generation**: Leverages OpenAI's ChatGPT, Google Gemini Pro for generating text for blogs.
- [**Customizable AI Parameters**](https://github.com/AJaySi/AI-Writer/blob/main/main_config): Offers flexibility in adjusting AI parameters like model selection, temperature, and token limits to suit different content needs.

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


---

Notes from underground:

1). Focus is on writing/generating highly unique, SEO optimized blog content.
2). Models: Openai, gemini, ollama are interesting. Minstral API is also worth exploring. Cohere API is purpose made.
Focus is getting the prompts right. Shit in, shit out, irrespective of dollars and cutting edge models.
Pydantically speakng, Due to experimental nature of prompting, its getting expensive soon enough. Gemini is free for now.
3). Missing frontend: A smart backend will enable a good frontend. WIP, backend. So, frontend; coming soon.
4).Getting AI agents to 'brainstrom' blog ideas seems more pressing. CrewAI seems more straightforward than autogen.
5). Too Many APIs floating around: The implementation is using tools that dont depend on API keys and rather scrape them.
Duh, scraping wont scale, that is GPT vision based scraping will come in handy.
