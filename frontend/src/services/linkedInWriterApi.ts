import { apiClient } from '../api/client';

// LinkedIn-specific enums
export enum LinkedInPostType {
  PROFESSIONAL = 'professional',
  THOUGHT_LEADERSHIP = 'thought_leadership',
  INDUSTRY_NEWS = 'industry_news',
  PERSONAL_STORY = 'personal_story',
  COMPANY_UPDATE = 'company_update',
  POLL = 'poll'
}

export enum LinkedInTone {
  PROFESSIONAL = 'professional',
  CONVERSATIONAL = 'conversational',
  AUTHORITATIVE = 'authoritative',
  INSPIRATIONAL = 'inspirational',
  EDUCATIONAL = 'educational',
  FRIENDLY = 'friendly'
}

export enum SearchEngine {
  METAPHOR = 'metaphor',
  GOOGLE = 'google',
  TAVILY = 'tavily'
}

// Request interfaces
export interface LinkedInPostRequest {
  topic: string;
  industry: string;
  post_type?: LinkedInPostType;
  tone?: LinkedInTone;
  target_audience?: string;
  key_points?: string[];
  include_hashtags?: boolean;
  include_call_to_action?: boolean;
  research_enabled?: boolean;
  search_engine?: SearchEngine;
  max_length?: number;
}

export interface LinkedInArticleRequest {
  topic: string;
  industry: string;
  tone?: LinkedInTone;
  target_audience?: string;
  key_sections?: string[];
  include_images?: boolean;
  seo_optimization?: boolean;
  research_enabled?: boolean;
  search_engine?: SearchEngine;
  word_count?: number;
}

export interface LinkedInCarouselRequest {
  topic: string;
  industry: string;
  slide_count?: number;
  tone?: LinkedInTone;
  target_audience?: string;
  key_takeaways?: string[];
  include_cover_slide?: boolean;
  include_cta_slide?: boolean;
  visual_style?: string;
}

export interface LinkedInVideoScriptRequest {
  topic: string;
  industry: string;
  video_length?: number;
  tone?: LinkedInTone;
  target_audience?: string;
  key_messages?: string[];
  include_hook?: boolean;
  include_captions?: boolean;
}

export interface LinkedInCommentResponseRequest {
  original_post: string;
  comment: string;
  response_type?: 'professional' | 'appreciative' | 'clarifying' | 'disagreement' | 'value_add';
  tone?: LinkedInTone;
  include_question?: boolean;
  brand_voice?: string;
}

// Response interfaces
export interface ResearchSource {
  title: string;
  url: string;
  content: string;
  relevance_score?: number;
}

export interface HashtagSuggestion {
  hashtag: string;
  category: string;
  popularity_score?: number;
}

export interface ImageSuggestion {
  description: string;
  alt_text: string;
  style?: string;
  placement?: string;
}

export interface PostContent {
  content: string;
  character_count: number;
  hashtags: HashtagSuggestion[];
  call_to_action?: string;
  engagement_prediction?: Record<string, any>;
}

export interface ArticleContent {
  title: string;
  content: string;
  word_count: number;
  sections: Array<Record<string, string>>;
  seo_metadata?: Record<string, any>;
  image_suggestions: ImageSuggestion[];
  reading_time?: number;
}

export interface CarouselSlide {
  slide_number: number;
  title: string;
  content: string;
  visual_elements: string[];
  design_notes?: string;
}

export interface CarouselContent {
  title: string;
  slides: CarouselSlide[];
  cover_slide?: CarouselSlide;
  cta_slide?: CarouselSlide;
  design_guidelines: Record<string, string>;
}

export interface VideoScript {
  hook: string;
  main_content: Array<Record<string, string>>;
  conclusion: string;
  captions?: string[];
  thumbnail_suggestions: string[];
  video_description: string;
}

export interface LinkedInPostResponse {
  success: boolean;
  data?: PostContent;
  research_sources: ResearchSource[];
  generation_metadata: Record<string, any>;
  error?: string;
}

export interface LinkedInArticleResponse {
  success: boolean;
  data?: ArticleContent;
  research_sources: ResearchSource[];
  generation_metadata: Record<string, any>;
  error?: string;
}

export interface LinkedInCarouselResponse {
  success: boolean;
  data?: CarouselContent;
  generation_metadata: Record<string, any>;
  error?: string;
}

export interface LinkedInVideoScriptResponse {
  success: boolean;
  data?: VideoScript;
  generation_metadata: Record<string, any>;
  error?: string;
}

export interface LinkedInCommentResponseResult {
  success: boolean;
  response?: string;
  alternative_responses: string[];
  tone_analysis?: Record<string, any>;
  generation_metadata: Record<string, any>;
  error?: string;
}

// API client
export const linkedInWriterApi = {
  async health(): Promise<any> {
    const { data } = await apiClient.get('/api/linkedin/health');
    return data;
  },

  async generatePost(request: LinkedInPostRequest): Promise<LinkedInPostResponse> {
    const { data } = await apiClient.post('/api/linkedin/generate-post', request);
    return data;
  },

  async generateArticle(request: LinkedInArticleRequest): Promise<LinkedInArticleResponse> {
    const { data } = await apiClient.post('/api/linkedin/generate-article', request);
    return data;
  },

  async generateCarousel(request: LinkedInCarouselRequest): Promise<LinkedInCarouselResponse> {
    const { data } = await apiClient.post('/api/linkedin/generate-carousel', request);
    return data;
  },

  async generateVideoScript(request: LinkedInVideoScriptRequest): Promise<LinkedInVideoScriptResponse> {
    const { data } = await apiClient.post('/api/linkedin/generate-video-script', request);
    return data;
  },

  async generateCommentResponse(request: LinkedInCommentResponseRequest): Promise<LinkedInCommentResponseResult> {
    const { data } = await apiClient.post('/api/linkedin/generate-comment-response', request);
    return data;
  },

  async optimizeProfile(request: any): Promise<any> {
    const { data } = await apiClient.post('/api/linkedin/optimize-profile', request);
    return data;
  },

  async generatePoll(request: any): Promise<any> {
    const { data } = await apiClient.post('/api/linkedin/generate-poll', request);
    return data;
  },

  async generateCompanyUpdate(request: any): Promise<any> {
    const { data } = await apiClient.post('/api/linkedin/generate-company-update', request);
    return data;
  }
};
