# Hallucination Detection React UI Implementation Guide

This comprehensive guide provides everything you need to implement a React frontend for the Hallucination Detection API, recreating the demo experience described in the Exa.ai hallucination detector example.

## Table of Contents

1. [Overview](#overview)
2. [API Endpoints](#api-endpoints)
3. [React Components](#react-components)
4. [Implementation Steps](#implementation-steps)
5. [Advanced Features](#advanced-features)
6. [Styling and UX](#styling-and-ux)
7. [Error Handling](#error-handling)
8. [Testing](#testing)

## Overview

The Hallucination Detection UI provides an interface for users to:
- Input text for analysis
- View extracted claims
- See verification results with sources
- Understand confidence scores and explanations
- Perform batch analysis
- View demo examples

### Key Features

- **Real-time Analysis**: Analyze text as users type or on-demand
- **Visual Indicators**: Color-coded results (supported/refuted/uncertain)
- **Source Attribution**: Show supporting and refuting sources
- **Confidence Scoring**: Visual confidence indicators
- **Batch Processing**: Handle multiple texts simultaneously
- **Responsive Design**: Works on desktop and mobile devices

## API Endpoints

The backend provides these endpoints for the React frontend:

### Base URL
```
http://localhost:8000/api/hallucination-detection
```

### Available Endpoints

1. **Single Text Analysis**
   ```
   POST /analyze
   Content-Type: application/json
   
   {
     "text": "Your text to analyze",
     "search_depth": 5,
     "confidence_threshold": 0.7
   }
   ```

2. **Batch Analysis**
   ```
   POST /analyze-batch
   Content-Type: application/json
   
   {
     "texts": ["Text 1", "Text 2"],
     "search_depth": 5,
     "confidence_threshold": 0.7
   }
   ```

3. **Claim Extraction Only**
   ```
   POST /extract-claims
   Content-Type: application/json
   
   {
     "text": "Your text to analyze"
   }
   ```

4. **Single Claim Verification**
   ```
   POST /verify-claim?claim=Your%20claim&search_depth=5
   ```

5. **Demo Analysis**
   ```
   GET /demo
   ```

6. **Health Check**
   ```
   GET /health
   ```

## React Components

### 1. Main Hallucination Detector Component

```jsx
// components/HallucinationDetector.jsx
import React, { useState, useCallback } from 'react';
import axios from 'axios';
import TextInput from './TextInput';
import AnalysisResults from './AnalysisResults';
import LoadingSpinner from './LoadingSpinner';
import ErrorDisplay from './ErrorDisplay';
import './HallucinationDetector.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const HallucinationDetector = () => {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [settings, setSettings] = useState({
    searchDepth: 5,
    confidenceThreshold: 0.7
  });

  const analyzeText = useCallback(async () => {
    if (!text.trim()) {
      setError('Please enter text to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/hallucination-detection/analyze`, {
        text: text.trim(),
        search_depth: settings.searchDepth,
        confidence_threshold: settings.confidenceThreshold
      });

      setResults(response.data);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [text, settings]);

  const loadDemo = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/api/hallucination-detection/demo`);
      setResults(response.data);
      setText(response.data.original_text);
    } catch (err) {
      console.error('Demo load error:', err);
      setError('Failed to load demo. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="hallucination-detector">
      <div className="detector-header">
        <h1>AI Hallucination Detector</h1>
        <p>Analyze text for factual accuracy using AI-powered claim verification</p>
      </div>

      <div className="detector-main">
        <div className="input-section">
          <TextInput
            value={text}
            onChange={setText}
            onAnalyze={analyzeText}
            loading={loading}
            settings={settings}
            onSettingsChange={setSettings}
          />
          
          <div className="action-buttons">
            <button 
              onClick={analyzeText}
              disabled={loading || !text.trim()}
              className="analyze-btn primary"
            >
              {loading ? 'Analyzing...' : 'Analyze Text'}
            </button>
            
            <button 
              onClick={loadDemo}
              disabled={loading}
              className="demo-btn secondary"
            >
              Load Demo
            </button>
          </div>
        </div>

        <div className="results-section">
          {loading && <LoadingSpinner />}
          {error && <ErrorDisplay error={error} onDismiss={() => setError(null)} />}
          {results && <AnalysisResults results={results} />}
        </div>
      </div>
    </div>
  );
};

export default HallucinationDetector;
```

### 2. Text Input Component

```jsx
// components/TextInput.jsx
import React from 'react';
import SettingsPanel from './SettingsPanel';

const TextInput = ({ 
  value, 
  onChange, 
  onAnalyze, 
  loading, 
  settings, 
  onSettingsChange 
}) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      onAnalyze();
    }
  };

  return (
    <div className="text-input-container">
      <div className="input-header">
        <label htmlFor="text-input">Text to Analyze</label>
        <span className="char-count">{value.length} characters</span>
      </div>
      
      <textarea
        id="text-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Enter the text you want to analyze for potential hallucinations..."
        rows={8}
        disabled={loading}
        className="text-input"
      />
      
      <div className="input-footer">
        <span className="shortcut-hint">Press Ctrl+Enter to analyze</span>
        <SettingsPanel 
          settings={settings} 
          onSettingsChange={onSettingsChange}
          disabled={loading}
        />
      </div>
    </div>
  );
};

export default TextInput;
```

### 3. Analysis Results Component

```jsx
// components/AnalysisResults.jsx
import React, { useState } from 'react';
import ClaimCard from './ClaimCard';
import OverallAssessment from './OverallAssessment';
import SourcesList from './SourcesList';

const AnalysisResults = ({ results }) => {
  const [activeTab, setActiveTab] = useState('claims');
  const [selectedClaim, setSelectedClaim] = useState(null);

  const tabs = [
    { id: 'claims', label: 'Claims Analysis', count: results.total_claims },
    { id: 'overview', label: 'Overview' },
    { id: 'sources', label: 'All Sources' }
  ];

  return (
    <div className="analysis-results">
      <div className="results-header">
        <h2>Analysis Results</h2>
        <div className="processing-time">
          Processed in {results.processing_time?.toFixed(2)}s
        </div>
      </div>

      <div className="tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
          >
            {tab.label}
            {tab.count && <span className="tab-count">{tab.count}</span>}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {activeTab === 'claims' && (
          <div className="claims-list">
            {results.claims_analysis.map((claim, index) => (
              <ClaimCard
                key={index}
                claim={claim}
                index={index}
                isSelected={selectedClaim === index}
                onSelect={() => setSelectedClaim(
                  selectedClaim === index ? null : index
                )}
              />
            ))}
          </div>
        )}

        {activeTab === 'overview' && (
          <OverallAssessment assessment={results.overall_assessment} />
        )}

        {activeTab === 'sources' && (
          <SourcesList claims={results.claims_analysis} />
        )}
      </div>
    </div>
  );
};

export default AnalysisResults;
```

### 4. Claim Card Component

```jsx
// components/ClaimCard.jsx
import React from 'react';
import ConfidenceBar from './ConfidenceBar';
import SourcePreview from './SourcePreview';

const ClaimCard = ({ claim, index, isSelected, onSelect }) => {
  const getAssessmentColor = (assessment) => {
    switch (assessment) {
      case 'supported': return 'green';
      case 'refuted': return 'red';
      case 'partially_supported': return 'orange';
      default: return 'gray';
    }
  };

  const getAssessmentIcon = (assessment) => {
    switch (assessment) {
      case 'supported': return '✓';
      case 'refuted': return '✗';
      case 'partially_supported': return '~';
      default: return '?';
    }
  };

  return (
    <div className={`claim-card ${isSelected ? 'selected' : ''}`}>
      <div className="claim-header" onClick={onSelect}>
        <div className="claim-number">Claim {index + 1}</div>
        <div className={`assessment-badge ${getAssessmentColor(claim.assessment)}`}>
          <span className="assessment-icon">
            {getAssessmentIcon(claim.assessment)}
          </span>
          <span className="assessment-text">
            {claim.assessment.replace('_', ' ').toUpperCase()}
          </span>
        </div>
      </div>

      <div className="claim-text">
        "{claim.claim}"
      </div>

      <div className="claim-confidence">
        <label>Confidence Score</label>
        <ConfidenceBar score={claim.confidence_score} />
      </div>

      {isSelected && (
        <div className="claim-details">
          <div className="explanation">
            <h4>Analysis Explanation</h4>
            <p>{claim.explanation}</p>
          </div>

          {claim.supporting_sources.length > 0 && (
            <div className="sources-section">
              <h4>Supporting Sources ({claim.supporting_sources.length})</h4>
              {claim.supporting_sources.map((source, idx) => (
                <SourcePreview key={idx} source={source} type="supporting" />
              ))}
            </div>
          )}

          {claim.refuting_sources.length > 0 && (
            <div className="sources-section">
              <h4>Refuting Sources ({claim.refuting_sources.length})</h4>
              {claim.refuting_sources.map((source, idx) => (
                <SourcePreview key={idx} source={source} type="refuting" />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ClaimCard;
```

### 5. Settings Panel Component

```jsx
// components/SettingsPanel.jsx
import React, { useState } from 'react';

const SettingsPanel = ({ settings, onSettingsChange, disabled }) => {
  const [isOpen, setIsOpen] = useState(false);

  const updateSetting = (key, value) => {
    onSettingsChange({ ...settings, [key]: value });
  };

  return (
    <div className="settings-panel">
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled}
        className="settings-toggle"
      >
        ⚙️ Settings
      </button>

      {isOpen && (
        <div className="settings-dropdown">
          <div className="setting-group">
            <label>Search Depth</label>
            <input
              type="range"
              min="1"
              max="10"
              value={settings.searchDepth}
              onChange={(e) => updateSetting('searchDepth', parseInt(e.target.value))}
              disabled={disabled}
            />
            <span className="setting-value">{settings.searchDepth} sources</span>
          </div>

          <div className="setting-group">
            <label>Confidence Threshold</label>
            <input
              type="range"
              min="0.1"
              max="1.0"
              step="0.1"
              value={settings.confidenceThreshold}
              onChange={(e) => updateSetting('confidenceThreshold', parseFloat(e.target.value))}
              disabled={disabled}
            />
            <span className="setting-value">{(settings.confidenceThreshold * 100).toFixed(0)}%</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default SettingsPanel;
```

## Implementation Steps

### Step 1: Setup React Project

```bash
# Create new React app or add to existing project
npx create-react-app hallucination-detector-ui
cd hallucination-detector-ui

# Install dependencies
npm install axios react-router-dom
```

### Step 2: Project Structure

```
src/
├── components/
│   ├── HallucinationDetector.jsx
│   ├── TextInput.jsx
│   ├── AnalysisResults.jsx
│   ├── ClaimCard.jsx
│   ├── SettingsPanel.jsx
│   ├── ConfidenceBar.jsx
│   ├── SourcePreview.jsx
│   ├── OverallAssessment.jsx
│   ├── LoadingSpinner.jsx
│   └── ErrorDisplay.jsx
├── styles/
│   ├── HallucinationDetector.css
│   ├── components.css
│   └── animations.css
├── services/
│   └── api.js
├── hooks/
│   └── useHallucinationDetector.js
└── utils/
    └── helpers.js
```

### Step 3: API Service Layer

```jsx
// services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class HallucinationAPI {
  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/hallucination-detection`,
      timeout: 60000, // 60 seconds for analysis
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Add request interceptor for loading states
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  async analyzeText(text, options = {}) {
    const response = await this.client.post('/analyze', {
      text,
      search_depth: options.searchDepth || 5,
      confidence_threshold: options.confidenceThreshold || 0.7
    });
    return response.data;
  }

  async analyzeBatch(texts, options = {}) {
    const response = await this.client.post('/analyze-batch', {
      texts,
      search_depth: options.searchDepth || 5,
      confidence_threshold: options.confidenceThreshold || 0.7
    });
    return response.data;
  }

  async extractClaims(text) {
    const response = await this.client.post('/extract-claims', { text });
    return response.data;
  }

  async verifyClaim(claim, options = {}) {
    const params = new URLSearchParams({
      claim,
      search_depth: options.searchDepth || 5,
      confidence_threshold: options.confidenceThreshold || 0.7
    });
    
    const response = await this.client.post(`/verify-claim?${params}`);
    return response.data;
  }

  async getDemo() {
    const response = await this.client.get('/demo');
    return response.data;
  }

  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const hallucinationAPI = new HallucinationAPI();
```

### Step 4: Custom Hook

```jsx
// hooks/useHallucinationDetector.js
import { useState, useCallback } from 'react';
import { hallucinationAPI } from '../services/api';

export const useHallucinationDetector = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const analyzeText = useCallback(async (text, options) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await hallucinationAPI.analyzeText(text, options);
      setResults(results);
      return results;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Analysis failed';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const loadDemo = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const demo = await hallucinationAPI.getDemo();
      setResults(demo);
      return demo;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to load demo';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResults = useCallback(() => {
    setResults(null);
    setError(null);
  }, []);

  return {
    loading,
    error,
    results,
    analyzeText,
    loadDemo,
    clearResults
  };
};
```

## Advanced Features

### Real-time Analysis

```jsx
// hooks/useRealTimeAnalysis.js
import { useState, useEffect, useCallback } from 'react';
import { debounce } from 'lodash';
import { hallucinationAPI } from '../services/api';

export const useRealTimeAnalysis = (delay = 2000) => {
  const [text, setText] = useState('');
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(false);

  const debouncedExtractClaims = useCallback(
    debounce(async (text) => {
      if (text.length < 50) return; // Minimum text length
      
      setLoading(true);
      try {
        const result = await hallucinationAPI.extractClaims(text);
        setClaims(result.claims);
      } catch (error) {
        console.error('Real-time analysis error:', error);
      } finally {
        setLoading(false);
      }
    }, delay),
    [delay]
  );

  useEffect(() => {
    debouncedExtractClaims(text);
  }, [text, debouncedExtractClaims]);

  return { text, setText, claims, loading };
};
```

### Batch Analysis Component

```jsx
// components/BatchAnalysis.jsx
import React, { useState } from 'react';
import { hallucinationAPI } from '../services/api';

const BatchAnalysis = () => {
  const [texts, setTexts] = useState(['']);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const addTextInput = () => {
    setTexts([...texts, '']);
  };

  const removeTextInput = (index) => {
    setTexts(texts.filter((_, i) => i !== index));
  };

  const updateText = (index, value) => {
    const newTexts = [...texts];
    newTexts[index] = value;
    setTexts(newTexts);
  };

  const analyzeBatch = async () => {
    const validTexts = texts.filter(text => text.trim().length > 0);
    if (validTexts.length === 0) return;

    setLoading(true);
    try {
      const results = await hallucinationAPI.analyzeBatch(validTexts);
      setResults(results);
    } catch (error) {
      console.error('Batch analysis error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="batch-analysis">
      <h2>Batch Analysis</h2>
      
      <div className="text-inputs">
        {texts.map((text, index) => (
          <div key={index} className="batch-input">
            <textarea
              value={text}
              onChange={(e) => updateText(index, e.target.value)}
              placeholder={`Text ${index + 1}`}
              rows={3}
            />
            {texts.length > 1 && (
              <button onClick={() => removeTextInput(index)}>Remove</button>
            )}
          </div>
        ))}
      </div>

      <div className="batch-controls">
        <button onClick={addTextInput}>Add Text</button>
        <button onClick={analyzeBatch} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Batch'}
        </button>
      </div>

      {results && (
        <div className="batch-results">
          <h3>Batch Results</h3>
          <div className="batch-summary">
            <p>Processed {results.batch_summary.total_texts_processed} texts</p>
            <p>Found {results.batch_summary.texts_with_hallucinations} texts with potential hallucinations</p>
            <p>Average accuracy: {(results.batch_summary.average_accuracy_score * 100).toFixed(1)}%</p>
          </div>
          
          {results.results.map((result, index) => (
            <div key={index} className="batch-result-item">
              <h4>Text {index + 1}</h4>
              {/* Render individual results */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BatchAnalysis;
```

## Styling and UX

### CSS Variables and Theme

```css
/* styles/theme.css */
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-secondary: #64748b;
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-neutral: #6b7280;
  
  /* Assessment colors */
  --color-supported: #10b981;
  --color-refuted: #ef4444;
  --color-partially: #f59e0b;
  --color-insufficient: #9ca3af;
  
  /* Backgrounds */
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;
  
  /* Borders */
  --border-light: #e2e8f0;
  --border-medium: #cbd5e1;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  
  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  
  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --border-light: #334155;
    --border-medium: #475569;
  }
}
```

### Component Styles

```css
/* styles/HallucinationDetector.css */
.hallucination-detector {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl);
  font-family: var(--font-sans);
}

.detector-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.detector-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.detector-header p {
  font-size: 1.125rem;
  color: var(--color-secondary);
}

.detector-main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
  align-items: start;
}

@media (max-width: 768px) {
  .detector-main {
    grid-template-columns: 1fr;
  }
}

.input-section {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.text-input-container {
  margin-bottom: var(--spacing-lg);
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.input-header label {
  font-weight: 600;
  color: var(--color-primary);
}

.char-count {
  font-size: 0.875rem;
  color: var(--color-secondary);
}

.text-input {
  width: 100%;
  min-height: 200px;
  padding: var(--spacing-md);
  border: 2px solid var(--border-light);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.5;
  resize: vertical;
  transition: border-color 0.2s;
}

.text-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--spacing-sm);
  font-size: 0.875rem;
  color: var(--color-secondary);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
}

.analyze-btn, .demo-btn {
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.analyze-btn.primary {
  background: var(--color-primary);
  color: white;
}

.analyze-btn.primary:hover:not(:disabled) {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.demo-btn.secondary {
  background: var(--bg-secondary);
  color: var(--color-secondary);
  border: 1px solid var(--border-medium);
}

.demo-btn.secondary:hover:not(:disabled) {
  background: var(--bg-tertiary);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Claim Card Styles */
.claim-card {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-md);
  overflow: hidden;
  transition: all 0.2s;
}

.claim-card:hover {
  box-shadow: var(--shadow-md);
}

.claim-card.selected {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

.claim-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  cursor: pointer;
}

.claim-number {
  font-weight: 600;
  color: var(--color-primary);
}

.assessment-badge {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 600;
}

.assessment-badge.green {
  background: rgb(16 185 129 / 0.1);
  color: var(--color-supported);
}

.assessment-badge.red {
  background: rgb(239 68 68 / 0.1);
  color: var(--color-refuted);
}

.assessment-badge.orange {
  background: rgb(245 158 11 / 0.1);
  color: var(--color-partially);
}

.assessment-badge.gray {
  background: rgb(156 163 175 / 0.1);
  color: var(--color-insufficient);
}

.claim-text {
  padding: var(--spacing-md);
  font-style: italic;
  color: var(--color-secondary);
  border-left: 4px solid var(--color-primary);
  margin: var(--spacing-md);
  background: var(--bg-tertiary);
}

.confidence-bar {
  width: 100%;
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-error), var(--color-warning), var(--color-success));
  transition: width 0.3s ease;
}

/* Animation styles */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.analysis-results {
  animation: fadeIn 0.5s ease-out;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading-spinner {
  animation: pulse 1.5s ease-in-out infinite;
}
```

## Error Handling

### Error Boundary Component

```jsx
// components/ErrorBoundary.jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Hallucination Detector Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <p>The hallucination detector encountered an unexpected error.</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

### Error Display Component

```jsx
// components/ErrorDisplay.jsx
import React from 'react';

const ErrorDisplay = ({ error, onDismiss, onRetry }) => {
  return (
    <div className="error-display">
      <div className="error-icon">⚠️</div>
      <div className="error-content">
        <h3>Analysis Failed</h3>
        <p>{error}</p>
        <div className="error-actions">
          {onRetry && (
            <button onClick={onRetry} className="retry-btn">
              Try Again
            </button>
          )}
          <button onClick={onDismiss} className="dismiss-btn">
            Dismiss
          </button>
        </div>
      </div>
    </div>
  );
};

export default ErrorDisplay;
```

## Testing

### Unit Tests

```jsx
// __tests__/HallucinationDetector.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import HallucinationDetector from '../components/HallucinationDetector';
import { hallucinationAPI } from '../services/api';

// Mock the API
jest.mock('../services/api');

describe('HallucinationDetector', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders main components', () => {
    render(<HallucinationDetector />);
    
    expect(screen.getByText('AI Hallucination Detector')).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter the text you want to analyze/)).toBeInTheDocument();
    expect(screen.getByText('Analyze Text')).toBeInTheDocument();
    expect(screen.getByText('Load Demo')).toBeInTheDocument();
  });

  test('handles text input', () => {
    render(<HallucinationDetector />);
    
    const textInput = screen.getByPlaceholderText(/Enter the text you want to analyze/);
    fireEvent.change(textInput, { target: { value: 'Test text' } });
    
    expect(textInput.value).toBe('Test text');
  });

  test('calls API on analyze button click', async () => {
    const mockResponse = {
      original_text: 'Test text',
      total_claims: 1,
      claims_analysis: [],
      overall_assessment: {},
      processing_time: 1.5
    };
    
    hallucinationAPI.analyzeText.mockResolvedValue(mockResponse);
    
    render(<HallucinationDetector />);
    
    const textInput = screen.getByPlaceholderText(/Enter the text you want to analyze/);
    const analyzeBtn = screen.getByText('Analyze Text');
    
    fireEvent.change(textInput, { target: { value: 'Test text' } });
    fireEvent.click(analyzeBtn);
    
    await waitFor(() => {
      expect(hallucinationAPI.analyzeText).toHaveBeenCalledWith('Test text', {
        searchDepth: 5,
        confidenceThreshold: 0.7
      });
    });
  });

  test('loads demo data', async () => {
    const mockDemo = {
      original_text: 'Demo text',
      total_claims: 2,
      claims_analysis: [],
      overall_assessment: {}
    };
    
    hallucinationAPI.getDemo.mockResolvedValue(mockDemo);
    
    render(<HallucinationDetector />);
    
    const demoBtn = screen.getByText('Load Demo');
    fireEvent.click(demoBtn);
    
    await waitFor(() => {
      expect(hallucinationAPI.getDemo).toHaveBeenCalled();
    });
  });
});
```

### Integration Tests

```jsx
// __tests__/integration.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import HallucinationDetector from '../components/HallucinationDetector';

// Mock fetch for integration tests
global.fetch = jest.fn();

describe('Integration Tests', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('full analysis workflow', async () => {
    const mockResponse = {
      original_text: 'The sky is green.',
      total_claims: 1,
      claims_analysis: [{
        claim: 'The sky is green',
        assessment: 'refuted',
        confidence_score: 0.95,
        explanation: 'The sky is typically blue due to light scattering.',
        supporting_sources: [],
        refuting_sources: [{
          url: 'https://example.com',
          title: 'Why is the sky blue?',
          text: 'The sky appears blue due to Rayleigh scattering...',
          relevance_score: 0.9
        }]
      }],
      overall_assessment: {
        hallucination_detected: true,
        accuracy_score: 0.0,
        total_supported: 0,
        total_refuted: 1
      },
      processing_time: 2.3
    };

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    render(<HallucinationDetector />);

    // Input text
    const textInput = screen.getByPlaceholderText(/Enter the text you want to analyze/);
    fireEvent.change(textInput, { target: { value: 'The sky is green.' } });

    // Click analyze
    const analyzeBtn = screen.getByText('Analyze Text');
    fireEvent.click(analyzeBtn);

    // Wait for results
    await waitFor(() => {
      expect(screen.getByText('Analysis Results')).toBeInTheDocument();
    });

    // Check results display
    expect(screen.getByText('REFUTED')).toBeInTheDocument();
    expect(screen.getByText('The sky is green')).toBeInTheDocument();
  });
});
```

## Environment Configuration

### Environment Variables

```bash
# .env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENABLE_DEMO=true
REACT_APP_MAX_TEXT_LENGTH=10000
REACT_APP_DEFAULT_SEARCH_DEPTH=5
REACT_APP_DEFAULT_CONFIDENCE_THRESHOLD=0.7
```

### Configuration File

```jsx
// config/app.js
export const config = {
  api: {
    baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    timeout: 60000,
    retries: 3
  },
  features: {
    enableDemo: process.env.REACT_APP_ENABLE_DEMO === 'true',
    enableBatchAnalysis: true,
    enableRealTimeAnalysis: false
  },
  limits: {
    maxTextLength: parseInt(process.env.REACT_APP_MAX_TEXT_LENGTH) || 10000,
    maxBatchSize: 50,
    minTextLength: 10
  },
  defaults: {
    searchDepth: parseInt(process.env.REACT_APP_DEFAULT_SEARCH_DEPTH) || 5,
    confidenceThreshold: parseFloat(process.env.REACT_APP_DEFAULT_CONFIDENCE_THRESHOLD) || 0.7
  }
};
```

This comprehensive guide provides everything needed to implement a full-featured React UI for the Hallucination Detection API. The implementation includes modern React patterns, comprehensive error handling, responsive design, and thorough testing approaches.