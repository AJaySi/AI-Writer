# AI Blog Rewriter & Updater

A powerful AI-powered tool for rewriting and updating existing blog content with improved quality, factual accuracy, and SEO optimization.

## Features

### 1. Content Import
- **URL Import**: Automatically extract content from any blog URL
- **Manual Input**: Paste content directly with title, meta description, and author information
- **Smart Content Extraction**: Preserves structure, headings, images, and metadata

### 2. Content Analysis
- **Metrics Analysis**:
  - Word count
  - Sentence count
  - Paragraph count
  - Average words per sentence
  - Average sentences per paragraph
- **Structure Analysis**:
  - Heading hierarchy
  - Content organization
  - Image analysis
- **Age Analysis**:
  - Content age calculation
  - Publication date detection

### 3. Web Research
- **Topic Extraction**: Automatically identifies key topics for fact-checking
- **Multi-Source Research**: Gathers information from various sources
- **Research Depth Control**: Choose between low, medium, and high research depth
- **Source Organization**: Categorizes research by topic with source details

### 4. Rewriting Modes
- **Standard Rewrite**: Improve clarity and flow while maintaining core message
- **SEO Optimization**: Enhance content for search engines with targeted keywords
- **Simplification**: Make complex content more accessible
- **Expansion**: Add more details and examples
- **Fact Check**: Update outdated information
- **Tone Shift**: Change writing style while preserving content
- **Modernization**: Update with current information and trends

### 5. Customization Options
- **Tone Selection**:
  - Professional
  - Conversational
  - Academic
  - Enthusiastic
  - Authoritative
  - Friendly
  - Technical
  - Inspirational
- **Length Control**:
  - Maintain original length
  - Create shorter version
  - Create longer version
  - Custom word count
- **SEO Features**:
  - Focus keyword optimization
  - Meta description generation
  - Title optimization
- **Special Instructions**: Add custom requirements for the rewrite

### 6. Image Generation
- **AI Image Suggestions**: Get recommendations for relevant images
- **Custom Image Generation**: Create images based on content
- **Style Options**:
  - Realistic
  - Artistic
  - Cartoon
  - 3D Render
- **Image Placement**: Suggested optimal placement within content

### 7. Export Options
- **Preview Mode**: View formatted content
- **Markdown Export**: Get clean markdown version
- **Image Integration**: Include generated images with captions
- **Meta Information**: Export with optimized title and meta description

## Usage

1. **Import Content**
   - Choose between URL import or manual content entry
   - Provide necessary metadata (title, author, etc.)

2. **Analysis & Research**
   - Review content analysis metrics
   - Examine research findings
   - Identify areas for improvement

3. **Configure Rewrite Settings**
   - Select rewrite mode
   - Choose target tone
   - Set content length
   - Add focus keywords
   - Provide special instructions

4. **Review & Export**
   - Preview rewritten content
   - Generate suggested images
   - Export in desired format

## Technical Details

### Dependencies
- Streamlit for UI
- BeautifulSoup for content extraction
- GPT providers for text generation
- Image generation capabilities
- Web research APIs (Exa, Tavily)

### Key Components
- `BlogRewriter` class: Core functionality
- Content extraction and analysis
- Research integration
- AI-powered rewriting
- Image generation
- Export capabilities

### Error Handling
- Robust error handling for URL extraction
- Fallback mechanisms for content parsing
- Graceful degradation for API failures
- User-friendly error messages

## Best Practices

1. **Content Import**
   - Use clean, well-structured URLs
   - Provide complete metadata for manual entry
   - Ensure content is properly formatted

2. **Research Settings**
   - Choose appropriate research depth
   - Review research findings carefully
   - Verify source credibility

3. **Rewrite Configuration**
   - Select appropriate tone for audience
   - Use relevant focus keywords
   - Provide clear special instructions

4. **Image Generation**
   - Use descriptive prompts
   - Choose appropriate style
   - Consider image placement

## Limitations

- Maximum content length for processing
- API rate limits for research
- Image generation constraints
- Language support limitations

## Future Enhancements

- Multi-language support
- Advanced SEO analysis
- Content structure templates
- Collaborative editing
- Integration with CMS platforms
- Custom AI model selection
- Advanced image editing
- Content versioning 