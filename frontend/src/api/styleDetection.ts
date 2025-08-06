/** Style Detection API Integration */

export interface StyleAnalysisRequest {
  content: {
    main_content: string;
    title?: string;
    description?: string;
  };
  analysis_type?: 'comprehensive' | 'patterns';
}

export interface StyleAnalysisResponse {
  success: boolean;
  analysis?: any;
  patterns?: any;
  guidelines?: any;
  error?: string;
  timestamp: string;
}

export interface WebCrawlRequest {
  url?: string;
  text_sample?: string;
}

export interface WebCrawlResponse {
  success: boolean;
  content?: any;
  metrics?: any;
  error?: string;
  timestamp: string;
}

export interface StyleDetectionRequest {
  url?: string;
  text_sample?: string;
  include_patterns?: boolean;
  include_guidelines?: boolean;
}

export interface StyleDetectionResponse {
  success: boolean;
  crawl_result?: any;
  style_analysis?: any;
  style_patterns?: any;
  style_guidelines?: any;
  error?: string;
  warning?: string;
  timestamp: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Analyze content style using AI
 */
export const analyzeContentStyle = async (request: StyleAnalysisRequest): Promise<StyleAnalysisResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error analyzing content style:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString(),
    };
  }
};

/**
 * Crawl website content for style analysis
 */
export const crawlWebsiteContent = async (request: WebCrawlRequest): Promise<WebCrawlResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/crawl`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error crawling website content:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString(),
    };
  }
};

/**
 * Complete style detection workflow
 */
export const completeStyleDetection = async (request: StyleDetectionRequest): Promise<StyleDetectionResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/complete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error in complete style detection:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString(),
    };
  }
};

/**
 * Get style detection configuration options
 */
export const getStyleDetectionConfiguration = async (): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/configuration-options`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting style detection configuration:', error);
    return {
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

/**
 * Validate style detection request
 */
export const validateStyleDetectionRequest = (request: StyleDetectionRequest): { valid: boolean; errors: string[] } => {
  const errors: string[] = [];

  if (!request.url && !request.text_sample) {
    errors.push('Either URL or text sample is required');
  }

  if (request.url && !request.url.startsWith('http')) {
    errors.push('URL must start with http:// or https://');
  }

  if (request.text_sample && request.text_sample.length < 50) {
    errors.push('Text sample must be at least 50 characters');
  }

  if (request.text_sample && request.text_sample.length > 10000) {
    errors.push('Text sample is too long (max 10,000 characters)');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
};

/**
 * Check if analysis exists for a website URL
 */
export const checkExistingAnalysis = async (websiteUrl: string): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/check-existing/${encodeURIComponent(websiteUrl)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error checking existing analysis:', error);
    return {
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

/**
 * Get analysis by ID
 */
export const getAnalysisById = async (analysisId: number): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/analysis/${analysisId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting analysis by ID:', error);
    return {
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

/**
 * Get all analyses for the current session
 */
export const getSessionAnalyses = async (): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/session-analyses`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting session analyses:', error);
    return {
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

/**
 * Delete an analysis
 */
export const deleteAnalysis = async (analysisId: number): Promise<any> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/onboarding/style-detection/analysis/${analysisId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error deleting analysis:', error);
    return {
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}; 