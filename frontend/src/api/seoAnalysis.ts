import { longRunningApiClient } from './client';
import { SEOAnalysisData } from '../components/shared/types';

// SEO Analysis API functions
export const seoAnalysisAPI = {
  async analyzeURL(url: string, targetKeywords?: string[]): Promise<SEOAnalysisData | null> {
    try {
      console.log(`Starting SEO analysis for URL: ${url}`);
      console.log(`Target keywords:`, targetKeywords);
      
      const requestData = {
        url,
        target_keywords: targetKeywords
      };
      console.log('Request data:', requestData);
      
      const response = await longRunningApiClient.post('/api/seo-dashboard/analyze-comprehensive', requestData);
      console.log('Response received:', response);
      console.log('Response data:', response.data);
      
      if (response.data.success) {
        console.log(`SEO analysis completed for ${url}`);
        console.log('Analysis result:', response.data);
        return response.data;
      } else {
        console.error('Analysis failed:', response.data.message);
        throw new Error(response.data.message || 'Analysis failed');
      }
    } catch (error: any) {
      console.error('Error analyzing URL:', error);
      console.error('Error details:', {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data
      });
      throw error;
    }
  },

  async getDetailedMetrics(url: string): Promise<any> {
    try {
      console.log(`Getting detailed metrics for URL: ${url}`);
      const response = await longRunningApiClient.get(`/api/seo-dashboard/metrics/${encodeURIComponent(url)}`);
      console.log(`Detailed metrics retrieved for ${url}`);
      return response.data;
    } catch (error) {
      console.error('Error getting detailed metrics:', error);
      throw error;
    }
  },

  async getAnalysisSummary(): Promise<any> {
    try {
      console.log('Getting analysis summary');
      const response = await longRunningApiClient.get('/api/seo-dashboard/summary');
      console.log('Analysis summary retrieved');
      return response.data;
    } catch (error) {
      console.error('Error getting analysis summary:', error);
      throw error;
    }
  },

  async batchAnalyzeURLs(urls: string[]): Promise<any[]> {
    try {
      console.log(`Starting batch analysis for ${urls.length} URLs`);
      const response = await longRunningApiClient.post('/api/seo-dashboard/batch-analyze', { urls });
      console.log(`Batch analysis completed for ${urls.length} URLs`);
      return response.data;
    } catch (error) {
      console.error('Error in batch analysis:', error);
      throw error;
    }
  },

  async healthCheck(): Promise<boolean> {
    try {
      const response = await longRunningApiClient.get('/api/seo-dashboard/health');
      return response.status === 200;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}; 