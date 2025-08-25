# AI SEO Tools Services

## Overview
Professional-grade AI-powered SEO analysis tools converted from Streamlit apps to FastAPI services. Designed for content creators, digital marketers, and solopreneurs.

## Available Services

### 🎯 Meta Description Generator
- **Service**: `MetaDescriptionService`
- **Purpose**: Generate compelling, SEO-optimized meta descriptions
- **AI Features**: Context-aware generation, keyword optimization, tone adaptation

### ⚡ PageSpeed Analyzer  
- **Service**: `PageSpeedService`
- **Purpose**: Google PageSpeed Insights analysis with AI insights
- **AI Features**: Performance optimization recommendations, business impact analysis

### 🗺️ Sitemap Analyzer
- **Service**: `SitemapService` 
- **Purpose**: Website structure and content trend analysis
- **AI Features**: Content strategy insights, publishing pattern analysis

### 🖼️ Image Alt Text Generator
- **Service**: `ImageAltService`
- **Purpose**: AI-powered alt text generation for images
- **AI Features**: Vision-based analysis, SEO-optimized descriptions

### 📱 OpenGraph Generator
- **Service**: `OpenGraphService`
- **Purpose**: Social media optimization tags
- **AI Features**: Platform-specific optimization, content analysis

### 📄 On-Page SEO Analyzer
- **Service**: `OnPageSEOService`
- **Purpose**: Comprehensive on-page SEO analysis
- **AI Features**: Content quality analysis, keyword optimization insights

### 🔧 Technical SEO Analyzer
- **Service**: `TechnicalSEOService`
- **Purpose**: Website crawling and technical analysis
- **AI Features**: Issue prioritization, fix recommendations

### 🏢 Enterprise SEO Suite
- **Service**: `EnterpriseSEOService`
- **Purpose**: Complete SEO audit workflows
- **AI Features**: Competitive analysis, strategic recommendations

### 📊 Content Strategy Analyzer
- **Service**: `ContentStrategyService`
- **Purpose**: Content gap analysis and strategy planning
- **AI Features**: Topic opportunities, competitive positioning

## Key Features
- ✅ AI-enhanced analysis using Gemini
- ✅ Structured JSON responses
- ✅ Comprehensive error handling
- ✅ Intelligent logging and monitoring
- ✅ Business-focused insights
- ✅ Async/await support
- ✅ Health check endpoints

## Quick Start

```python
from services.seo_tools import MetaDescriptionService

# Initialize service
service = MetaDescriptionService()

# Generate meta descriptions
result = await service.generate_meta_description(
    keywords=["SEO", "content marketing"],
    tone="Professional",
    search_intent="Informational Intent"
)

print(result["meta_descriptions"])
```

## API Integration
All services are exposed via FastAPI endpoints at `/api/seo/*`. See the main documentation for complete API reference.

## Logging
All operations are logged with structured data to:
- `logs/seo_tools/operations.jsonl` - Successful operations  
- `logs/seo_tools/errors.jsonl` - Error logs
- `logs/seo_tools/ai_analysis.jsonl` - AI interactions

## Health Monitoring
Each service includes a `health_check()` method for monitoring:

```python
status = await service.health_check()
print(status["status"])  # "operational" or "error"
```

## Business Focus
All AI analysis is optimized for:
- **Content Creators**: User-friendly insights and actionable recommendations
- **Digital Marketers**: Performance metrics and ROI-focused suggestions  
- **Solopreneurs**: Cost-effective, comprehensive SEO analysis

---
For complete documentation, see `/backend/docs/SEO_TOOLS_MIGRATION.md`