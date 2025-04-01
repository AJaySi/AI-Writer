# Website Analyzer Module

A comprehensive website analysis toolkit that provides detailed insights into website performance, SEO metrics, and content quality. This module combines traditional web analysis techniques with AI-powered content evaluation to deliver actionable recommendations.

## Features

### 1. Comprehensive Website Analysis
- Basic website information extraction
- SSL/TLS certificate validation
- DNS record analysis
- WHOIS information retrieval
- Content analysis and structure evaluation
- Performance metrics assessment

### 2. Advanced SEO Analysis
- Meta tag optimization analysis
- Content quality evaluation
- Keyword density analysis
- Readability scoring
- Heading structure analysis
- AI-powered content recommendations

### 3. Technical Infrastructure
- Asynchronous web crawling
- Multi-threaded analysis
- Robust error handling
- Comprehensive logging
- Type-safe data models

## Module Structure

### 1. `analyzer.py`
The main analysis engine that provides comprehensive website analysis.

#### Key Components:
- `WebsiteAnalyzer` class
  - URL validation
  - Basic website information extraction
  - SSL/TLS certificate checking
  - DNS record analysis
  - WHOIS information retrieval
  - Content analysis
  - Performance metrics assessment

#### Features:
- Concurrent analysis using ThreadPoolExecutor
- Robust error handling and logging
- User-agent simulation for reliable scraping
- Timeout handling for requests
- Comprehensive result formatting

### 2. `seo_analyzer.py`
Specialized SEO analysis module with AI integration.

#### Key Components:
- `extract_content()`: Fetches and parses webpage content
- `analyze_meta_tags()`: Evaluates meta tags and SEO elements
- `analyze_content_with_ai()`: AI-powered content analysis
- `analyze_seo()`: Main SEO analysis function

#### Features:
- Meta tag optimization analysis
- Content quality scoring
- Keyword density analysis
- Readability evaluation
- AI-powered recommendations
- Weighted scoring system

### 3. `models.py`
Data models for structured analysis results.

#### Key Components:
- `SEORecommendation`: Individual SEO recommendations
- `MetaTagAnalysis`: Meta tag analysis results
- `ContentAnalysis`: Content analysis metrics
- `SEOAnalysisResult`: Complete analysis results

#### Features:
- Type-safe data structures
- Clear data organization
- Easy serialization/deserialization
- Comprehensive documentation

## Usage Examples

### Basic Website Analysis
```python
from website_analyzer import analyze_website

# Analyze a website
results = analyze_website("https://example.com")

# Access analysis results
if results["success"]:
    data = results["data"]
    print(f"Domain: {data['domain']}")
    print(f"SSL Info: {data['analysis']['ssl_info']}")
    print(f"Content Info: {data['analysis']['content_info']}")
```

### SEO Analysis
```python
from website_analyzer.seo_analyzer import analyze_seo

# Perform SEO analysis
seo_results = analyze_seo("https://example.com", "your-openai-api-key")

# Access SEO results
if seo_results.success:
    print(f"Overall Score: {seo_results.overall_score}")
    print(f"Meta Tags: {seo_results.meta_tags}")
    print(f"Content Analysis: {seo_results.content}")
    print(f"Recommendations: {seo_results.recommendations}")
```

## Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `python-whois`: WHOIS information
- `dnspython`: DNS record analysis
- `openai`: AI-powered analysis
- `loguru`: Logging
- `typing`: Type hints
- `dataclasses`: Data models

## Error Handling

The module implements comprehensive error handling:
- URL validation
- Request timeouts
- Connection errors
- Parsing errors
- API errors
- DNS resolution errors
- SSL/TLS errors

All errors are logged and returned in a structured format for easy handling.

## Logging

The module uses `loguru` for logging with the following features:
- File rotation (500 MB)
- 10-day retention
- Debug level logging
- Structured log format
- Both file and stdout output

## Best Practices

1. **API Key Management**
   - Store API keys securely
   - Use environment variables
   - Implement rate limiting

2. **Error Handling**
   - Always check success status
   - Handle errors gracefully
   - Log errors appropriately

3. **Performance**
   - Use concurrent analysis
   - Implement timeouts
   - Cache results when possible

4. **Rate Limiting**
   - Respect website robots.txt
   - Implement delays between requests
   - Use appropriate user agents

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This module is part of the ALwrity project and is licensed under the MIT License.