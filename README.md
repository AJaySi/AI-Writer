# How to Alwrity - Getting Started

Alwrity assists content creators and digital marketers in keyword web research, AI website & Social media content generation & AI Copywriting.
Our toolkit integrates **(OpenAI, Gemini, Anthropic)** AI models for text generation, image creation **(Stability.ai), STT(whisper, AssemblyAI)** and Web or local data analysis, streamlining your content creation pipeline and ensuring high-quality output with minimal effort.

Prompting is abstracted to get going sooner. Focus on your content quality, rather than AI tooling around it.
Alwrity gives hyper content personalization, factual web researched & SEO optimized content and tools for automating content & digital marketing.

AI will help achieve Content Hyper-Personalization.
![](https://github.com/AJaySi/AI-Writer/blob/main/lib/workspace/keyword_blog.gif)
---
1). [Visit alwrity.com](https://www.alwrity.com/ai-writing-tools), You will find AI content writing tools, which are Free & No-Signup.
**Note:** Although, this is limited, as is our wallet & Resources.

2). **For complete AI content creation toolkit**, alwrity offers a local streamlit UI App. Its a BYOK model(Bring Your Own Key).
**Note:** 🗯️ Now, before you run away 🏃💨   
If you have 💻 Laptop + 🛜 Internet + 10 minutes, you will be generating blogs, articles etc with just few words.

### [Step-By-Step: Getting Started for Absolute Begginers](https://www.alwrity.com/post/getting-started-with-alwrity-ai-writer)

---
### [Getting started for Developers](https://github.com/AJaySi/AI-Writer/wiki/Alwrity--%E2%80%90-Get-started)
```
1). git clone https://github.com/AJaySi/AI-Writer.git
2). pip install -r -U requirements.txt
3). streamlit run alwrity.py

4). Visit Alwrity UI in a Browser & Start generation AI personalized content.
```
---
### Updating to latest Code: (Existing users)
```
1). Git pull
2). pip install -U -r requirements.txt
3). streamlit run alwrity.py
```
---
**Still stuck, [Open issue here](https://github.com/AJaySi/AI-Writer/issues) & Someone will bail you out.**
---

![](https://github.com/AJaySi/AI-Writer/blob/main/lib/workspace/structured_data_seo.mp4)

### AI Tools & Features of Alwrity:
| No. | Alwrity Tool                       | Description                                                                    |
|-----|------------------------------------|--------------------------------------------------------------------------------|
| 1   | AI Blog Writer                     | Generates blog content based on the latest web research on given keywords.     |
| 2   | AI YouTube to Content Writer       | Transforms content from provided YouTube URLs into written form.               |
| 3   | AI Long Form Content               | Creates extensive and detailed articles.                                       |
| 4   | AI Essay Writer                    | Produces lengthy essays on various topics, with room for improvement.          |
| 5   | AI Story Writer                    | Constructs narratives and stories based on provided backstories and characters.|
| 6   | AI Email Writer                    | Generates various types of professional letters.                               |
| 7   | AI Letter Writer                   | Crafts business letters for formal communication.                              |
| 8   | AI LinkedIn Blog Post Generator    | Develops blog posts optimized for sharing on LinkedIn.                         |
| 9   | AI Instagram Caption Generation    | Creates engaging captions for Instagram posts.                                 |
| 10  | AI Content Outline Generator       | Generates outlines based on keywords gathered from web research.               |
| 11  | AI Web Researcher                  | Conducts comprehensive web research and analysis using various methods.        |
| 12  | AI Content Planning & Calendar     | Assists in planning and organizing content with a comprehensive calendar.      |
| 13  | Create Blog Images                 | Generates images to complement blog content using Stable Diffusion.            |
| 14  | Agentic Content Creation           | Explores innovative content creation methods with CrewAI.                      |
| 15  | AI Finance Writer                  | Uses ufinance & padnas_ta to write TA report for given stock symbol            |
| 16  | AI Agents Team                     | Easily create AI Agents team for Content creation & Digital marketing          |
| 17  | Talk to your Docs (WIP)            | Write content from your local documents of any type(multi-modal)               |
| 18  | Wordpress API integration          | Programmatically upload blogs to wordpress website with API keys               |
| 19  | Talk to your website               | Crawl Crawl your entire website & write content based on its content, Or Not   |
| 20  | Content From URLs                  | Provide any URL to create an original, unique content from                     |
| 21  | SEO Structured Data                | Feature: AI SEO - Generate rich snippet from url                               |

---

# AI Content Generation Toolkit - Alwrity
![](https://github.com/AJaySi/AI-Writer/blob/main/lib/workspace/alwrity_ai_writer.png)

## Introduction

Alwrity automates and enhances the process of content creation, optimization, and management(Really ?). 
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
  - [firecrawl](https://www.firecrawl.dev/): Turn websites into LLM-ready data
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

#### Notes from underground:

1). Focus is on writing/generating highly unique, SEO optimized blog content.
2). Models: Openai, gemini, ollama are interesting. Minstral API is also worth exploring. Cohere API is purpose made.
Focus is getting the prompts right. Shit in, shit out, irrespective of dollars and cutting edge models.
Pydantically speakng, Due to experimental nature of prompting, its getting expensive soon enough. Gemini is free for now.
3). Missing frontend: A smart backend will enable a good frontend. WIP, backend. So, frontend; coming soon.
4).Getting AI agents to 'brainstrom' blog ideas seems more pressing. CrewAI seems more straightforward than autogen.
5). Too Many APIs floating around: The implementation is using tools that dont depend on API keys and rather scrape them.
Duh, scraping wont scale, that is GPT vision based scraping will come in handy.
6). firecrawl is interesting, gpt-researcher is providing local docsqa.
7). Had to provide streamlit UI as Alwrity's audience arent comfortable with commandline.
8). Local folder RAG and Chat with your content, website is on the cards.
9). AI models are better, not sure until when 'Free' APIs will be "Free".
10). The code is always a mess, lot of changes happening.. 
11). Focus is to stop making any more AI content tools, but rather revisit & improve user experience & content quality.
12). To Err is Human & AI....

---
LICENE
---
MIT License

Copyright (c) 2024 Alwrity

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
