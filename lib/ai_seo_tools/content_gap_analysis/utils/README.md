# Content Gap Analysis Utils

This directory contains utility modules that power the Content Gap Analysis tool. These modules provide core functionality for data collection, processing, analysis, and storage.

## Directory Structure

```
utils/
├── README.md
├── ai_processor.py      # AI-powered content analysis and processing
├── content_parser.py    # Content structure parsing and analysis
├── data_collector.py    # Website data collection and processing
└── storage.py          # Analysis results storage and retrieval
```

## Module Descriptions

### 1. AI Processor (`ai_processor.py`)

The AI Processor module enhances content analysis using AI techniques. It provides intelligent analysis of website content, competitor data, and keyword research.

#### Key Features:
- Content quality assessment
- Topic analysis and clustering
- Performance metrics analysis
- Strategic recommendations generation
- Progress tracking for analysis tasks

#### Main Components:
- `AIProcessor`: Main class for AI-powered analysis
- `ProgressTracker`: Tracks analysis progress and status

#### Usage Example:
```python
from utils.ai_processor import AIProcessor

processor = AIProcessor()
analysis = processor.analyze_content({
    'url': 'https://example.com',
    'industry': 'technology',
    'content': content_data
})
```

### 2. Content Parser (`content_parser.py`)

The Content Parser module handles the parsing and analysis of website content structure. It provides detailed insights into content organization and quality.

#### Key Features:
- Content structure analysis
- Text statistics calculation
- Topic extraction
- Readability analysis
- Content hierarchy analysis

#### Main Components:
- `ContentParser`: Main class for content parsing and analysis

#### Usage Example:
```python
from utils.content_parser import ContentParser

parser = ContentParser()
structure = parser.parse_structure({
    'main_content': content,
    'html': html_content,
    'headings': headings_data
})
```

### 3. Data Collector (`data_collector.py`)

The Data Collector module is responsible for gathering website data for analysis. It handles web scraping and data extraction.

#### Key Features:
- Website content collection
- Meta data extraction
- Heading structure analysis
- Link and image extraction
- Error handling and retry logic

#### Main Components:
- `DataCollector`: Main class for data collection

#### Usage Example:
```python
from utils.data_collector import DataCollector

collector = DataCollector()
data = collector.collect('https://example.com')
```

### 4. Storage (`storage.py`)

The Storage module manages the persistence and retrieval of analysis results. It provides a robust database interface for storing and accessing analysis data.

#### Key Features:
- Analysis results storage
- Historical data management
- Recommendation tracking
- User-specific analysis storage
- Error handling and rollback support

#### Main Components:
- `ContentGapAnalysisStorage`: Main class for storage operations

#### Usage Example:
```python
from utils.storage import ContentGapAnalysisStorage

storage = ContentGapAnalysisStorage(db_session)
analysis_id = storage.save_analysis(
    user_id=1,
    website_url='https://example.com',
    industry='technology',
    results=analysis_results
)
```

## Integration Points

### 1. Website Analysis Integration
```python
from utils.data_collector import DataCollector
from utils.content_parser import ContentParser
from utils.ai_processor import AIProcessor

# Collect data
collector = DataCollector()
data = collector.collect(url)

# Parse content
parser = ContentParser()
structure = parser.parse_structure(data)

# Process with AI
processor = AIProcessor()
analysis = processor.analyze_content({
    'url': url,
    'content': structure
})
```

### 2. Storage Integration
```python
from utils.storage import ContentGapAnalysisStorage

# Store analysis results
storage = ContentGapAnalysisStorage(db_session)
analysis_id = storage.save_analysis(
    user_id=user_id,
    website_url=url,
    industry=industry,
    results=analysis_results
)

# Retrieve analysis
results = storage.get_analysis(analysis_id)
```

## Error Handling

All modules implement comprehensive error handling:

1. **Data Collection Errors**
   - Network timeouts
   - Invalid URLs
   - Access restrictions
   - Parsing errors

2. **Processing Errors**
   - Invalid data formats
   - AI processing failures
   - Resource limitations
   - Analysis timeouts

3. **Storage Errors**
   - Database connection issues
   - Transaction failures
   - Data validation errors
   - Concurrent access conflicts

## Best Practices

1. **Data Collection**
   - Implement rate limiting
   - Use proper user agents
   - Handle redirects
   - Validate input data

2. **Content Processing**
   - Clean and normalize data
   - Handle encoding issues
   - Implement fallback strategies
   - Cache processed results

3. **Storage Management**
   - Use transactions
   - Implement data validation
   - Handle concurrent access
   - Maintain data integrity

## Future Enhancements

1. **Performance Optimizations**
   - Implement parallel processing
   - Add caching layer
   - Optimize database queries
   - Enhance error recovery

2. **Feature Additions**
   - Content performance tracking
   - Automated content planning
   - Enhanced competitive intelligence
   - Advanced topic clustering

3. **Integration Improvements**
   - API endpoints
   - Export capabilities
   - Data visualization
   - Progress tracking

4. **UI/UX Enhancements**
   - Interactive visualizations
   - Real-time progress updates
   - Export interfaces
   - Customization options

## Contributing

When contributing to these utility modules:

1. Follow the existing code structure
2. Add comprehensive error handling
3. Include unit tests
4. Update documentation
5. Follow PEP 8 style guide

## Dependencies

- BeautifulSoup4: HTML parsing
- NLTK: Natural language processing
- SQLAlchemy: Database operations
- Streamlit: UI components
- Requests: HTTP requests

## License

This project is licensed under the MIT License - see the LICENSE file for details. 