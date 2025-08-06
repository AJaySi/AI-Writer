import { apiClient } from './client';

export interface UserData {
  website_url?: string;
  session?: {
    id: number;
    current_step: number;
    progress: number;
    started_at?: string;
    updated_at?: string;
  };
  website_analysis?: {
    website_url: string;
    industry: string;
    target_audience: string;
    content_goals: string[];
    brand_voice: string;
    content_style: string;
  };
  api_keys?: Array<{
    id: number;
    provider: string;
    description?: string;
  }>;
  research_preferences?: {
    target_keywords: string[];
    competitor_urls: string[];
    content_topics: string[];
  };
}

export const userDataAPI = {
  async getUserData(): Promise<UserData | null> {
    try {
      console.log('Fetching user data from backend...');
      const response = await apiClient.get('/api/user-data');
      console.log('User data received:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching user data:', error);
      return null;
    }
  },

  async getWebsiteURL(): Promise<string | null> {
    try {
      console.log('Fetching website URL...');
      const response = await apiClient.get('/api/user-data/website-url');
      console.log('Website URL received:', response.data);
      return response.data.website_url || null;
    } catch (error: any) {
      console.error('Error fetching website URL:', error);
      return null;
    }
  },

  async getOnboardingData(): Promise<any> {
    try {
      console.log('Fetching onboarding data...');
      const response = await apiClient.get('/api/user-data/onboarding');
      console.log('Onboarding data received:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching onboarding data:', error);
      return null;
    }
  }
}; 