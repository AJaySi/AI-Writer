// Component Logic API integration
import { AxiosResponse } from 'axios';
import { apiClient } from './client';

// AI Research Interfaces
export interface UserInfoRequest {
  full_name: string;
  email: string;
  company: string;
  role: string;
}

export interface UserInfoResponse {
  valid: boolean;
  user_info?: any;
  errors: string[];
}

export interface ResearchPreferencesRequest {
  research_depth: string;
  content_types: string[];
  auto_research: boolean;
  factual_content: boolean;
}

export interface ResearchPreferencesResponse {
  valid: boolean;
  preferences?: any;
  errors: string[];
}

export interface ResearchRequest {
  topic: string;
  preferences: ResearchPreferencesRequest;
}

export interface ResearchResponse {
  success: boolean;
  topic: string;
  results?: any;
  error?: string;
}

// Personalization Interfaces
export interface ContentStyleRequest {
  writing_style: string;
  tone: string;
  content_length: string;
}

export interface ContentStyleResponse {
  valid: boolean;
  style_config?: any;
  errors: string[];
}

export interface BrandVoiceRequest {
  personality_traits: string[];
  voice_description?: string;
  keywords?: string;
}

export interface BrandVoiceResponse {
  valid: boolean;
  brand_config?: any;
  errors: string[];
}

export interface AdvancedSettingsRequest {
  seo_optimization: boolean;
  readability_level: string;
  content_structure: string[];
}

export interface PersonalizationSettingsRequest {
  content_style: ContentStyleRequest;
  brand_voice: BrandVoiceRequest;
  advanced_settings: AdvancedSettingsRequest;
}

export interface PersonalizationSettingsResponse {
  valid: boolean;
  settings?: any;
  errors: string[];
}

// Research Utilities Interfaces
export interface ResearchTopicRequest {
  topic: string;
  api_keys: Record<string, string>;
}

export interface ResearchResultResponse {
  success: boolean;
  topic: string;
  data?: any;
  error?: string;
  metadata?: any;
}

// AI Research API Functions
export async function validateUserInfo(request: UserInfoRequest): Promise<UserInfoResponse> {
  const res: AxiosResponse<UserInfoResponse> = await apiClient.post('/api/onboarding/ai-research/validate-user', request);
  return res.data;
}

export async function configureResearchPreferences(request: ResearchPreferencesRequest): Promise<ResearchPreferencesResponse> {
  const res: AxiosResponse<ResearchPreferencesResponse> = await apiClient.post('/api/onboarding/ai-research/configure-preferences', request);
  return res.data;
}

export async function processResearchRequest(request: ResearchRequest): Promise<ResearchResponse> {
  const res: AxiosResponse<ResearchResponse> = await apiClient.post('/api/onboarding/ai-research/process-research', request);
  return res.data;
}

export async function getResearchConfigurationOptions(): Promise<any> {
  const res: AxiosResponse<any> = await apiClient.get('/api/onboarding/ai-research/configuration-options');
  return res.data;
}

export async function getResearchPreferences(): Promise<ResearchPreferencesResponse> {
  const res: AxiosResponse<ResearchPreferencesResponse> = await apiClient.get('/api/onboarding/ai-research/preferences');
  return res.data;
}

// Personalization API Functions
export async function validateContentStyle(request: ContentStyleRequest): Promise<ContentStyleResponse> {
  const res: AxiosResponse<ContentStyleResponse> = await apiClient.post('/api/onboarding/personalization/validate-style', request);
  return res.data;
}

export async function configureBrandVoice(request: BrandVoiceRequest): Promise<BrandVoiceResponse> {
  const res: AxiosResponse<BrandVoiceResponse> = await apiClient.post('/api/onboarding/personalization/configure-brand', request);
  return res.data;
}

export async function processPersonalizationSettings(request: PersonalizationSettingsRequest): Promise<PersonalizationSettingsResponse> {
  const res: AxiosResponse<PersonalizationSettingsResponse> = await apiClient.post('/api/onboarding/personalization/process-settings', request);
  return res.data;
}

export async function getPersonalizationConfigurationOptions(): Promise<any> {
  const res: AxiosResponse<any> = await apiClient.get('/api/onboarding/personalization/configuration-options');
  return res.data;
}

export async function generateContentGuidelines(settings: any): Promise<any> {
  const res: AxiosResponse<any> = await apiClient.post('/api/onboarding/personalization/generate-guidelines', settings);
  return res.data;
}

// Research Utilities API Functions
export async function processResearchTopic(request: ResearchTopicRequest): Promise<ResearchResultResponse> {
  const res: AxiosResponse<ResearchResultResponse> = await apiClient.post('/api/onboarding/research/process-topic', request);
  return res.data;
}

export async function processResearchResults(results: any): Promise<any> {
  const res: AxiosResponse<any> = await apiClient.post('/api/onboarding/research/process-results', results);
  return res.data;
}

export async function validateResearchRequest(topic: string, api_keys: Record<string, string>): Promise<any> {
  const res: AxiosResponse<any> = await apiClient.post('/api/onboarding/research/validate-request', { topic, api_keys });
  return res.data;
}

export async function getResearchProvidersInfo(): Promise<any> {
  const res: AxiosResponse<any> = await apiClient.get('/api/onboarding/research/providers-info');
  return res.data;
}

export async function generateResearchReport(results: any): Promise<any> {
  const res: AxiosResponse<any> = await apiClient.post('/api/onboarding/research/generate-report', results);
  return res.data;
} 