import { apiClient, aiApiClient } from '../api/client';

// Types
export interface ContentStrategyCreate {
  name: string;
  description: string;
  industry: string;
  target_audience: string;
  content_pillars: string[];
  user_id?: number;
}

export interface ContentStrategyUpdate {
  name?: string;
  description?: string;
  industry?: string;
  target_audience?: string;
  content_pillars?: string[];
}

export interface CalendarEventCreate {
  title: string;
  description: string;
  date: string;
  platform: string;
  content_type: string;
  status: 'draft' | 'scheduled' | 'published';
  strategy_id?: string;
  user_id?: number;
}

export interface CalendarEventUpdate {
  title?: string;
  description?: string;
  date?: string;
  platform?: string;
  content_type?: string;
  status?: 'draft' | 'scheduled' | 'published';
  strategy_id?: string;
}

export interface GapAnalysisCreate {
  website_url: string;
  competitors: string[];
  keywords: string[];
  user_id?: number;
}

export interface GapAnalysisUpdate {
  website_url?: string;
  competitors?: string[];
  keywords?: string[];
  gaps?: string[];
  recommendations?: any[];
}

export interface AIAnalyticsCreate {
  analysis_type: string;
  data: any;
  insights: any[];
  user_id?: number;
}

export interface AIAnalyticsUpdate {
  analysis_type?: string;
  data?: any;
  insights?: any[];
}

// New Calendar Generation Interfaces
export interface CalendarGenerationRequest {
  user_id: number;
  strategy_id?: number;
  calendar_type: string;
  industry?: string;
  business_size: string;
  force_refresh?: boolean;
}

export interface CalendarGenerationResponse {
  user_id: number;
  strategy_id?: number;
  calendar_type: string;
  industry: string;
  business_size: string;
  generated_at: string;
  content_pillars: string[];
  platform_strategies: any;
  content_mix: Record<string, number>;
  daily_schedule: any[];
  weekly_themes: any[];
  content_recommendations: any[];
  optimal_timing: any;
  performance_predictions: any;
  trending_topics: any[];
  repurposing_opportunities: any[];
  ai_insights: any[];
  competitor_analysis: any;
  gap_analysis_insights: any;
  strategy_insights: any;
  onboarding_insights: any;
  processing_time: number;
  ai_confidence: number;
}

export interface ContentOptimizationRequest {
  user_id: number;
  event_id?: number;
  title: string;
  description: string;
  content_type: string;
  target_platform: string;
  original_content?: any;
}

export interface ContentOptimizationResponse {
  user_id: number;
  event_id?: number;
  original_content: any;
  optimized_content: any;
  platform_adaptations: string[];
  visual_recommendations: string[];
  hashtag_suggestions: string[];
  keyword_optimization: any;
  tone_adjustments: any;
  length_optimization: any;
  performance_prediction: any;
  optimization_score: number;
  created_at: string;
}

export interface PerformancePredictionRequest {
  user_id: number;
  strategy_id?: number;
  content_type: string;
  platform: string;
  content_data: any;
}

export interface PerformancePredictionResponse {
  user_id: number;
  strategy_id?: number;
  content_type: string;
  platform: string;
  predicted_engagement_rate: number;
  predicted_reach: number;
  predicted_conversions: number;
  predicted_roi: number;
  confidence_score: number;
  recommendations: string[];
  created_at: string;
}

export interface ContentRepurposingRequest {
  user_id: number;
  strategy_id?: number;
  original_content: any;
  target_platforms: string[];
}

export interface ContentRepurposingResponse {
  user_id: number;
  strategy_id?: number;
  original_content: any;
  platform_adaptations: any[];
  transformations: any[];
  implementation_tips: string[];
  gap_addresses: string[];
  created_at: string;
}

export interface TrendingTopicsRequest {
  user_id: number;
  industry: string;
  limit?: number;
}

export interface TrendingTopicsResponse {
  user_id: number;
  industry: string;
  trending_topics: any[];
  gap_relevance_scores: Record<string, number>;
  audience_alignment_scores: Record<string, number>;
  created_at: string;
}

// Content Planning API Service
class ContentPlanningAPI {
  private baseURL = '/api/content-planning';

  // Content Strategy APIs
  async createStrategy(strategy: ContentStrategyCreate) {
    const response = await apiClient.post(`${this.baseURL}/strategies/`, strategy);
    return response.data?.data || response.data;
  }

  async getStrategies(userId?: number) {
    const params = userId ? { user_id: userId } : {};
    const response = await apiClient.get(`${this.baseURL}/enhanced-strategies`, { params });
    return response.data?.data || response.data;
  }

  async getStrategy(id: string) {
    const response = await apiClient.get(`${this.baseURL}/strategies/${id}`);
    return response.data?.data || response.data;
  }

  async updateStrategy(id: string, updates: ContentStrategyUpdate) {
    const response = await apiClient.put(`${this.baseURL}/strategies/${id}`, updates);
    return response.data?.data || response.data;
  }

  async deleteStrategy(id: string) {
    const response = await apiClient.delete(`${this.baseURL}/strategies/${id}`);
    return response.data?.data || response.data;
  }

  // Calendar Event APIs
  async createEvent(event: CalendarEventCreate) {
    const response = await apiClient.post(`${this.baseURL}/calendar-events/`, event);
    return response.data?.data || response.data;
  }

  async getEvents(userId?: number, filters?: any) {
    const params = { ...filters };
    if (userId) params.user_id = userId;
    const response = await apiClient.get(`${this.baseURL}/calendar-events/`, { params });
    return response.data?.data || response.data;
  }

  async getEvent(id: string) {
    const response = await apiClient.get(`${this.baseURL}/calendar-events/${id}`);
    return response.data?.data || response.data;
  }

  async updateEvent(id: string, updates: CalendarEventUpdate) {
    const response = await apiClient.put(`${this.baseURL}/calendar-events/${id}`, updates);
    return response.data?.data || response.data;
  }

  async deleteEvent(id: string) {
    const response = await apiClient.delete(`${this.baseURL}/calendar-events/${id}`);
    return response.data?.data || response.data;
  }

  // Gap Analysis APIs
  async createGapAnalysis(analysis: GapAnalysisCreate) {
    const response = await apiClient.post(`${this.baseURL}/gap-analysis/`, analysis);
    return response.data?.data || response.data;
  }

  async getGapAnalyses(userId?: number) {
    const params = userId ? { user_id: userId } : {};
    const response = await apiClient.get(`${this.baseURL}/gap-analysis/`, { params });
    return response.data?.data || response.data;
  }

  async getGapAnalysis(id: string) {
    const response = await apiClient.get(`${this.baseURL}/gap-analysis/${id}`);
    return response.data?.data || response.data;
  }

  async updateGapAnalysis(id: string, updates: GapAnalysisUpdate) {
    const response = await apiClient.put(`${this.baseURL}/gap-analysis/${id}`, updates);
    return response.data?.data || response.data;
  }

  async deleteGapAnalysis(id: string) {
    const response = await apiClient.delete(`${this.baseURL}/gap-analysis/${id}`);
    return response.data?.data || response.data;
  }

  // AI-Powered Gap Analysis - Using AI client for longer timeout
  async analyzeContentGaps(params: {
    website_url: string;
    competitors: string[];
    keywords: string[];
    user_id?: number;
  }) {
    const response = await aiApiClient.post(`${this.baseURL}/gap-analysis/analyze`, params);
    return response.data;
  }

  // AI Analytics APIs - Using AI client for longer timeout
  async createAIAnalytics(analytics: AIAnalyticsCreate) {
    const response = await aiApiClient.post(`${this.baseURL}/ai-analytics/`, analytics);
    return response.data;
  }

  async getAIAnalytics(userId?: number) {
    const params = userId ? { user_id: userId } : {};
    const response = await aiApiClient.get(`${this.baseURL}/ai-analytics/`, { params });
    return response.data;
  }

  async getAIAnalyticsById(id: string) {
    const response = await aiApiClient.get(`${this.baseURL}/ai-analytics/${id}`);
    return response.data;
  }

  async updateAIAnalytics(id: string, updates: AIAnalyticsUpdate) {
    const response = await aiApiClient.put(`${this.baseURL}/ai-analytics/${id}`, updates);
    return response.data;
  }

  async deleteAIAnalytics(id: string) {
    const response = await aiApiClient.delete(`${this.baseURL}/ai-analytics/${id}`);
    return response.data;
  }

  // AI Analytics with Server-Sent Events
  async streamAIAnalytics(
    onProgress: (data: any) => void,
    onComplete: (data: any) => void,
    onError: (error: any) => void,
    userId?: number
  ) {
    try {
      const params: Record<string, string> = {};
      if (userId) {
        params.user_id = userId.toString();
      }
      const queryString = new URLSearchParams(params).toString();
      const url = `${this.baseURL}/ai-analytics/stream?${queryString}`;
      
      const eventSource = new EventSource(url);
      
      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          switch (data.type) {
            case 'connected':
              onProgress({ message: data.message, progress: 0 });
              break;
            case 'progress':
              onProgress({ 
                message: data.message, 
                progress: data.progress,
                step: data.step 
              });
              break;
            case 'complete':
              onComplete(data);
              eventSource.close();
              break;
            case 'error':
              onError(new Error(data.message));
              eventSource.close();
              break;
          }
        } catch (parseError) {
          onError(new Error('Failed to parse server message'));
        }
      };
      
      eventSource.onerror = (error) => {
        onError(new Error('EventSource failed'));
        eventSource.close();
      };
      
      // Return cleanup function
      return () => {
        eventSource.close();
      };
    } catch (error: any) {
      onError(error);
    }
  }

  // Health Check APIs
  async checkHealth() {
    const response = await apiClient.get(`${this.baseURL}/health`);
    return response.data;
  }

  async checkBackendHealth() {
    const response = await apiClient.get(`${this.baseURL}/health/backend`);
    return response.data;
  }

  async checkAIHealth() {
    const response = await apiClient.get(`${this.baseURL}/health/ai`);
    return response.data;
  }

  async checkDatabaseHealth() {
    const response = await apiClient.get(`${this.baseURL}/database/health`);
    return response.data;
  }

  // Error handling wrapper with AI-specific error messages
  private async handleRequest<T>(request: () => Promise<T>, isAI: boolean = false): Promise<T> {
    try {
      return await request();
    } catch (error: any) {
      console.error('API Error:', error);
      
      if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
        if (isAI) {
          throw new Error('AI analysis is taking longer than expected. This is normal for complex AI operations. Please wait a moment and try again.');
        } else {
          throw new Error('Request timed out. Please check your connection and try again.');
        }
      } else if (error.response) {
        // Server responded with error status
        const message = error.response.data?.detail || error.response.data?.message || 'API request failed';
        throw new Error(message);
      } else if (error.request) {
        // Request was made but no response received
        if (isAI) {
          throw new Error('AI service is not responding. The AI analysis may be in progress. Please wait and try again.');
        } else {
          throw new Error('No response from server. Please check your connection.');
        }
      } else {
        // Something else happened
        throw new Error('An unexpected error occurred.');
      }
    }
  }

  // Wrapped methods with error handling
  async createStrategySafe(strategy: ContentStrategyCreate) {
    return this.handleRequest(() => this.createStrategy(strategy));
  }

  async getStrategiesSafe(userId?: number) {
    return this.handleRequest(() => this.getStrategies(userId));
  }

  async createEventSafe(event: CalendarEventCreate) {
    return this.handleRequest(() => this.createEvent(event));
  }

  async getEventsSafe(userId?: number, filters?: any) {
    return this.handleRequest(() => this.getEvents(userId, filters));
  }

  async createGapAnalysisSafe(analysis: GapAnalysisCreate) {
    return this.handleRequest(() => this.createGapAnalysis(analysis));
  }

  async getGapAnalysesSafe(userId?: number) {
    return this.handleRequest(() => this.getGapAnalyses(userId));
  }

  async analyzeContentGapsSafe(params: {
    website_url: string;
    competitors: string[];
    keywords: string[];
    user_id?: number;
  }) {
    return this.handleRequest(() => this.analyzeContentGaps(params), true);
  }

  async getAIAnalyticsSafe(userId?: number) {
    return this.handleRequest(() => this.getAIAnalytics(userId), true);
  }

  // Enhanced version with rate limit handling for AI analytics
  async getAIAnalyticsWithRetry(userId?: number, maxRetries: number = 2): Promise<any> {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const response = await apiClient.get(`${this.baseURL}/ai-analytics/`, { 
          params: { user_id: userId || 1 }
        });
        return response.data;
      } catch (error: any) {
        if (error.response?.status === 429 && attempt < maxRetries) {
          // Rate limit hit, wait and retry
          const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
          console.log(`🚫 Rate limit hit for AI analytics, waiting ${delay}ms before retry ${attempt + 1}/${maxRetries}`);
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
        throw error; // Re-throw if it's not a rate limit or we've exhausted retries
      }
    }
  }

  // AI Analytics with force refresh option
  async getAIAnalyticsWithRefresh(userId?: number, forceRefresh = false): Promise<any> {
    try {
      const params: any = { user_id: userId || 1 };
      if (forceRefresh) {
        params.force_refresh = true;
      }
      const response = await apiClient.get(`${this.baseURL}/ai-analytics/`, { params });
      return response.data;
    } catch (error) {
      console.error('Error getting AI analytics with refresh:', error);
      return { insights: [], recommendations: [], total_insights: 0, total_recommendations: 0 };
    }
  }

  async getGapAnalysesWithRefresh(userId?: number, forceRefresh = false): Promise<any> {
    try {
      const params: any = { user_id: userId || 1 };
      if (forceRefresh) {
        params.force_refresh = true;
      }
      const response = await apiClient.get(`${this.baseURL}/gap-analysis/`, { params });
      return response.data;
    } catch (error) {
      console.error('Error getting gap analyses with refresh:', error);
      return { gap_analyses: [], total_gaps: 0 };
    }
  }

  // New Calendar Generation APIs
  async generateCalendar(request: CalendarGenerationRequest): Promise<CalendarGenerationResponse> {
    const response = await apiClient.post(`${this.baseURL}/generate-calendar`, request);
    return response.data;
  }

  async optimizeContent(request: ContentOptimizationRequest): Promise<ContentOptimizationResponse> {
    const response = await apiClient.post(`${this.baseURL}/optimize-content`, request);
    return response.data;
  }

  async predictPerformance(request: PerformancePredictionRequest): Promise<PerformancePredictionResponse> {
    const response = await apiClient.post(`${this.baseURL}/performance-predictions`, request);
    return response.data;
  }

  async repurposeContent(request: ContentRepurposingRequest): Promise<ContentRepurposingResponse> {
    const response = await apiClient.post(`${this.baseURL}/repurpose-content`, request);
    return response.data;
  }

  async getTrendingTopics(request: TrendingTopicsRequest): Promise<TrendingTopicsResponse> {
    return this.handleRequest(async () => {
      const response = await apiClient.post(`${this.baseURL}/trending-topics`, request);
      return response.data;
    });
  }

  async getComprehensiveUserData(userId?: number): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/calendar-generation/comprehensive-user-data`, {
        params: { user_id: userId }
      });
      return response.data;
    });
  }

  async generateComprehensiveCalendar(config: any): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.post(`${this.baseURL}/generate-comprehensive-calendar`, config);
      return response.data;
    });
  }

  async checkCalendarGenerationHealth(): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/calendar-generation/health`);
      return response.data;
    });
  }

  // Enhanced Strategy API Methods
  async getEnhancedStrategies(userId?: number): Promise<any> {
    return this.handleRequest(async () => {
      const params: any = {};
      if (userId) params.user_id = userId;
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies`, { params });
      return response.data?.data || response.data;
    });
  }

  async getEnhancedStrategy(strategyId: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies/${strategyId}`);
      return response.data?.data || response.data;
    });
  }

  async createEnhancedStrategy(strategy: any): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.post(`${this.baseURL}/enhanced-strategies`, strategy);
      return response.data.data || response.data;
    });
  }

  async getEnhancedStrategyCompletion(strategyId: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies/${strategyId}/completion`);
      return response.data?.data || response.data;
    });
  }

  async getEnhancedStrategyTooltips(): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies/tooltips`);
      return response.data?.data || response.data;
    });
  }

  async getEnhancedStrategyDisclosureSteps(): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies/disclosure-steps`);
      return response.data?.data || response.data;
    });
  }

  // Clear enhanced strategy streaming/cache for a user (best-effort refresh)
  async clearEnhancedCache(userId?: number): Promise<any> {
    const params: any = {};
    if (userId) params.user_id = userId;
    const response = await apiClient.post(`${this.baseURL}/enhanced-strategies/cache/clear`, null, { params });
    return response.data?.data || response.data;
  }

  // Non-streaming autofill refresh method
  async refreshAutofill(userId?: number, useAI: boolean = true, aiOnly: boolean = false): Promise<any> {
    const params: any = { 
      use_ai: useAI, 
      ai_only: aiOnly,
      _t: Date.now() // 🚨 CRITICAL: Cache-busting timestamp to ensure fresh AI generation
    };
    if (userId) params.user_id = userId;
    const response = await apiClient.post(`${this.baseURL}/enhanced-strategies/autofill/refresh`, null, { params });
    
    // The backend returns ResponseBuilder format: { status, message, data, status_code, timestamp }
    // We need to return the actual payload from response.data.data
    const result = response.data?.data || response.data;
    
    return result;
  }

  // Enhanced Strategy CRUD Operations
  async updateEnhancedStrategy(id: string, updates: any): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.put(`${this.baseURL}/enhanced-strategies/${id}`, updates);
      return response.data.data || response.data;
    });
  }

  async deleteEnhancedStrategy(id: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.delete(`${this.baseURL}/enhanced-strategies/${id}`);
      return response.data.data || response.data;
    });
  }

  // Onboarding Data Methods
  async getOnboardingData(userId?: number): Promise<any> {
    return this.handleRequest(async () => {
      const params = userId ? { user_id: userId } : {};
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies/onboarding-data`, { params });
      return response.data?.data || response.data;
    });
  }

  async getOnboardingIntegration(strategyId: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies/${strategyId}/onboarding-integration`);
      return response.data?.data || response.data;
    });
  }

  // AI Analysis Methods
  async generateEnhancedAIRecommendations(strategyId: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.post(`${this.baseURL}/enhanced-strategies/${strategyId}/ai-recommendations`);
      return response.data.data || response.data;
    }, true);
  }

  async regenerateAIAnalysis(strategyId: string, analysisType: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.post(`${this.baseURL}/enhanced-strategies/${strategyId}/ai-analysis/regenerate`, {
        analysis_type: analysisType
      });
      return response.data;
    }, true);
  }

  async getEnhancedAIAnalyses(strategyId: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.get(`${this.baseURL}/enhanced-strategies/${strategyId}/ai-analyses`);
      return response.data;
    });
  }

  // SSE Methods (for Orchestrator - real-time updates needed)
  async streamStrategicIntelligence(userId?: number): Promise<EventSource> {
    const url = `${this.baseURL}/enhanced-strategies/stream/strategic-intelligence?user_id=${userId || 1}`;
    return new EventSource(url);
  }

  // Helper method to handle SSE data (for Orchestrator)
  handleSSEData(eventSource: EventSource, onData: (data: any) => void, onError?: (error: any) => void, onComplete?: () => void) {
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onData(data);
        
        // Close connection when we get a result or error
        if (data.type === 'result' || data.type === 'error') {
          eventSource.close();
          onComplete?.();
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
        onError?.(error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE Error:', error);
      onError?.(error);
      eventSource.close();
    };

    return eventSource;
  }

  // Polling and Status Methods
  async getLatestGeneratedStrategy(userId?: number): Promise<any> {
    return this.handleRequest(async () => {
      const params = userId ? { user_id: userId } : {};
      const response = await apiClient.get(`${this.baseURL}/content-strategy/ai-generation/latest-strategy`, { params });
      // Return the strategy data from the nested response structure
      const result = response.data?.data?.strategy;
      return result;
    });
  }

  // Enhanced version with rate limit handling
  async getLatestGeneratedStrategyWithRetry(userId?: number, maxRetries: number = 2): Promise<any> {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const params = userId ? { user_id: userId } : {};
        const response = await apiClient.get(`${this.baseURL}/content-strategy/ai-generation/latest-strategy`, { params });
        const result = response.data?.data?.strategy;
        return result;
      } catch (error: any) {
        if (error.response?.status === 429 && attempt < maxRetries) {
          // Rate limit hit, wait and retry
          const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
          console.log(`🚫 Rate limit hit, waiting ${delay}ms before retry ${attempt + 1}/${maxRetries}`);
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
        throw error; // Re-throw if it's not a rate limit or we've exhausted retries
      }
    }
  }

  async startStrategyGenerationPolling(userId: number, strategyName: string): Promise<any> {
    return this.handleRequest(async () => {
      const response = await apiClient.post(`${this.baseURL}/content-strategy/ai-generation/generate-comprehensive-strategy-polling`, {
        user_id: userId,
        strategy_name: strategyName,
        config: {
          include_competitive_analysis: true,
          include_content_calendar: true,
          include_performance_predictions: true,
          include_implementation_roadmap: true,
          include_risk_assessment: true,
          max_content_pieces: 50,
          timeline_months: 12
        }
      });
      return response.data;
    });
  }

  async pollStrategyGeneration(
    taskId: string,
    onProgress: (status: any) => void,
    onComplete: (strategy: any) => void,
    onError: (error: string) => void,
    interval: number = 5000,
    maxAttempts: number = 72
  ): Promise<void> {
    let attempts = 0;
    
    const poll = async () => {
      try {
        attempts++;
        console.log(`🔄 Polling attempt ${attempts}/${maxAttempts} for task ${taskId}`);
        
        const response = await apiClient.get(`${this.baseURL}/content-strategy/ai-generation/strategy-generation-status/${taskId}`);
        const responseData = response.data;
        
        console.log('📊 Polling response:', responseData);
        
        // Extract the actual task status from the response data
        const taskStatus = responseData?.data || responseData;
        console.log('📊 Task status:', taskStatus);
        console.log('📊 Task status type:', typeof taskStatus);
        console.log('📊 Task status keys:', Object.keys(taskStatus || {}));
        
        console.log('📊 Task status check:', {
          status: taskStatus.status,
          progress: taskStatus.progress,
          hasStrategy: !!taskStatus.strategy,
          hasError: !!taskStatus.error,
          step: taskStatus.step,
          message: taskStatus.message
        });

        console.log('🔍 Checking completion conditions:');
        console.log('  - taskStatus.status:', taskStatus.status);
        console.log('  - taskStatus.progress:', taskStatus.progress);
        console.log('  - hasStrategy:', !!taskStatus.strategy);
        console.log('  - status === "completed":', taskStatus.status === 'completed');
        console.log('  - hasStrategy condition:', !!taskStatus.strategy);
        console.log('  - Both conditions met:', taskStatus.status === 'completed' && !!taskStatus.strategy);

        if (taskStatus.status === 'completed' && taskStatus.strategy) {
          console.log('✅ Strategy generation completed!');
          console.log('📊 Final completion data:', {
            status: taskStatus.status,
            progress: taskStatus.progress,
            step: taskStatus.step,
            hasStrategy: !!taskStatus.strategy,
            strategyKeys: taskStatus.strategy ? Object.keys(taskStatus.strategy) : []
          });
          onComplete(taskStatus.strategy);
          return;
        } else if (taskStatus.status === 'failed' || taskStatus.error) {
          console.error('❌ Strategy generation failed:', taskStatus.error);
          onError(taskStatus.error || 'Strategy generation failed');
          return;
        } else {
          // Update progress for any non-completed, non-failed status
          console.log('📊 Updating progress for status:', taskStatus.status);
          onProgress(responseData); // Pass the full response to maintain structure
          
          // Continue polling if we haven't exceeded max attempts
          if (attempts < maxAttempts) {
            setTimeout(poll, interval);
          } else {
            console.error('⏰ Polling timeout reached');
            onError('Strategy generation timed out. Please try again.');
          }
        }
        
        // Additional check: If progress is 100% but status is not 'completed', 
        // we should still call onComplete to ensure the modal shows completion
        if (taskStatus.progress >= 100 && taskStatus.strategy && taskStatus.status !== 'failed') {
          console.log('🎯 Progress is 100% with strategy available - calling onComplete');
          onComplete(taskStatus.strategy);
          return;
        }
      } catch (error: any) {
        console.error('❌ Polling error:', error);
        onError(error.message || 'Polling failed');
      }
    };
    
    // Start polling
    poll();
  }

  // Additional SSE Methods (for other features that need real-time updates)
  async streamKeywordResearch(userId?: number): Promise<EventSource> {
    const url = `${this.baseURL}/enhanced-strategies/stream/keyword-research?user_id=${userId || 1}`;
    return new EventSource(url);
  }

  async streamAIGenerationStatus(strategyId: string | number): Promise<EventSource> {
    const url = `${this.baseURL}/enhanced-strategies/stream/ai-generation-status?strategy_id=${strategyId}`;
    return new EventSource(url);
  }
}

// Export singleton instance
export const contentPlanningApi = new ContentPlanningAPI(); 