// SEO CopilotKit Type Definitions
// This file contains all TypeScript interfaces and types for SEO CopilotKit integration

// SEO Analysis Data Types
export interface SEOAnalysisData {
  health_score: number;
  critical_issues: SEOIssue[];
  traffic_metrics: TrafficMetrics;
  ranking_data: RankingData;
  mobile_speed: SpeedMetrics;
  keyword_data: KeywordData;
  url: string;
  last_updated: string;
  status: 'pending' | 'completed' | 'failed';
}

export interface SEOIssue {
  id: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  category: 'technical' | 'content' | 'performance' | 'accessibility';
  impact: string;
  recommendation: string;
  effort: 'easy' | 'medium' | 'hard';
  priority: number;
}

export interface PageTraffic {
  url: string;
  traffic: number;
  growth: number;
}

export interface TrafficSource {
  source: string;
  traffic: number;
  percentage: number;
}

export interface TrafficMetrics {
  organic_traffic: number;
  traffic_growth: number;
  top_pages: PageTraffic[];
  traffic_sources: TrafficSource[];
}

export interface KeywordRanking {
  keyword: string;
  position: number;
  volume: number;
  difficulty: number;
}

export interface PositionChange {
  keyword: string;
  old_position: number;
  new_position: number;
  change: number;
}

export interface RankingData {
  average_position: number;
  ranking_keywords: KeywordRanking[];
  position_changes: PositionChange[];
}

export interface CoreWebVitals {
  lcp: number;
  fid: number;
  cls: number;
}

export interface SpeedMetrics {
  mobile_score: number;
  desktop_score: number;
  load_time: number;
  core_web_vitals: CoreWebVitals;
}

export interface KeywordOpportunity {
  keyword: string;
  volume: number;
  difficulty: number;
  opportunity_score: number;
  current_position?: number;
}

export interface KeywordData {
  total_keywords: number;
  ranking_keywords: number;
  keyword_opportunities: KeywordOpportunity[];
}

// User Context Types
export interface UserProfile {
  id: string;
  name: string;
  email: string;
  business_type: string;
  seo_experience: 'beginner' | 'intermediate' | 'advanced';
  seo_goals: string[];
  target_audience: string;
}

export interface PersonalizationData {
  user_profile: UserProfile;
  business_type: string;
  target_audience: string;
  seo_goals: string[];
  seo_experience: 'beginner' | 'intermediate' | 'advanced';
}

// CopilotKit Action Types
export interface CopilotActionParams {
  url?: string;
  keywords?: string[];
  tone?: string;
  searchIntent?: string;
  strategy?: 'DESKTOP' | 'MOBILE';
  categories?: string[];
  chartType?: string;
  timeRange?: string;
  metrics?: string[];
  focusArea?: string;
  focusAreas?: string[];
  layout?: string;
  hideSections?: string[];
  concept?: string;
  complexity?: 'simple' | 'detailed' | 'technical';
  businessContext?: string;
  category?: string;
  timeframe?: string;
  scenarios?: string[];
  priority?: 'critical' | 'high' | 'medium' | 'low';
  effort?: 'easy' | 'medium' | 'hard';
  targetKeywords?: string[];
  sitemapUrl?: string;
  analyzeContentTrends?: boolean;
  analyzePublishingPatterns?: boolean;
  imageUrl?: string;
  context?: string;
  titleHint?: string;
  descriptionHint?: string;
  platform?: string;
  analyzeImages?: boolean;
  analyzeContentQuality?: boolean;
  includeMobile?: boolean;
  competitorUrls?: string[];
  marketAnalysis?: boolean;
  contentType?: string;
  targetAudience?: string;
  auditType?: string;
  includeRecommendations?: boolean;
  contentFocus?: string;
  seoOptimization?: boolean;
  includeToolsStatus?: boolean;
  depth?: string;
}

export interface CopilotActionResponse {
  success: boolean;
  message: string;
  data?: any;
  error?: string;
  execution_time?: number;
}

// SEO Service Response Types
export interface MetaDescriptionResponse {
  meta_descriptions: string[];
  analysis: {
    keyword_density: number;
    length_optimal: boolean;
    seo_score: number;
  };
}

export interface PageSpeedResponse {
  performance_score: number;
  accessibility_score: number;
  best_practices_score: number;
  seo_score: number;
  recommendations: string[];
  opportunities: SpeedOpportunity[];
}

export interface SitemapIssue {
  url: string;
  issue: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  recommendation: string;
}

export interface SpeedOpportunity {
  metric: string;
  current_value: number;
  target_value: number;
  improvement: number;
  recommendation: string;
}

export interface SitemapResponse {
  total_urls: number;
  indexed_urls: number;
  issues: SitemapIssue[];
  recommendations: string[];
}

// Chart and Visualization Types
export interface ChartConfig {
  type: 'line' | 'bar' | 'pie' | 'radar';
  chartKey?: ChartType;
  data: any;
  options: any;
  timeRange?: string;
  metrics?: string[];
}

export interface DashboardLayout {
  focusArea: string;
  layout: 'overview' | 'detailed' | 'focused';
  hiddenSections: string[];
  chartConfigs: ChartConfig[];
}

// Store State Types
export interface SEOCopilotState {
  // Loading states
  isLoading: boolean;
  isAnalyzing: boolean;
  isGenerating: boolean;
  
  // Data states
  analysisData: SEOAnalysisData | null;
  personalizationData: PersonalizationData | null;
  
  // UI states
  activeChart: string | null;
  dashboardLayout: DashboardLayout;
  suggestions: CopilotSuggestion[];
  
  // Error states
  error: string | null;
  lastError: Error | null;
  
  // Actions
  setLoading: (loading: boolean) => void;
  setAnalyzing: (analyzing: boolean) => void;
  setGenerating: (generating: boolean) => void;
  setAnalysisData: (data: SEOAnalysisData | null) => void;
  setPersonalizationData: (data: PersonalizationData | null) => void;
  setActiveChart: (chart: string | null) => void;
  setDashboardLayout: (layout: DashboardLayout) => void;
  setSuggestions: (suggestions: CopilotSuggestion[]) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  
  // API integration methods
  loadPersonalizationData: () => Promise<void>;
  executeCopilotAction: (action: string, params: any) => Promise<any>;
  
  // Chart and visualization methods
  updateChart: (chartType: ChartType, timeRange?: TimeRange, metrics?: string[]) => void;
  
  // Utility methods
  generateContextualSuggestions: (analysisData: SEOAnalysisData) => CopilotSuggestion[];
  getHealthScoreColor: (score: number) => string;
  getSeverityColor: (severity: string) => string;
  getEffortColor: (effort: string) => string;
  
  // Reset methods
  resetAnalysis: () => void;
  resetAll: () => void;
}

// CopilotKit Suggestion Types
export interface CopilotSuggestion {
  id: string;
  title: string;
  message: string;
  icon: string;
  category: 'analysis' | 'optimization' | 'education' | 'monitoring';
  priority: 'high' | 'medium' | 'low';
  action: string;
  parameters?: CopilotActionParams;
}

// API Service Types
export interface SEOApiService {
  analyzeSEO: (url: string, options?: any) => Promise<SEOAnalysisData>;
  generateMetaDescriptions: (params: any) => Promise<MetaDescriptionResponse>;
  analyzePageSpeed: (url: string, strategy?: string) => Promise<PageSpeedResponse>;
  analyzeSitemap: (sitemapUrl: string) => Promise<SitemapResponse>;
  getPersonalizationData: () => Promise<PersonalizationData>;
  updateDashboardLayout: (layout: DashboardLayout) => Promise<void>;
}

// Error Types
export interface SEOActionError {
  action: string;
  error: string;
  timestamp: string;
  userContext: any;
  retryable: boolean;
}

// Utility Types
export type SEOCategory = 'technical' | 'content' | 'performance' | 'accessibility' | 'mobile' | 'local';
export type SEOExperienceLevel = 'beginner' | 'intermediate' | 'advanced';
export type BusinessType = 'ecommerce' | 'saas' | 'blog' | 'agency' | 'local' | 'enterprise';
export type TimeRange = '7d' | '30d' | '90d' | '1y' | 'all';
export type ChartType = 'traffic' | 'rankings' | 'speed' | 'keywords' | 'issues' | 'performance';
