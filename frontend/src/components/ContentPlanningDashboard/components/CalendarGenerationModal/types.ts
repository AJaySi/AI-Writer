// Calendar Generation Modal Types

export interface CalendarGenerationModalProps {
  open: boolean;
  onClose: () => void;
  sessionId: string;
  initialConfig: CalendarConfig;
  onComplete: (results: CalendarGenerationResults) => void;
  onError: (error: string) => void;
}

export interface CalendarConfig {
  userId: string;
  strategyId: string;
  calendarType: 'monthly' | 'quarterly' | 'yearly';
  platforms: string[];
  duration: number;
  postingFrequency: 'daily' | 'weekly' | 'biweekly';
}

export interface CalendarGenerationResults {
  calendar: CalendarData;
  qualityScores: QualityScores;
  insights: GenerationInsights;
  recommendations: Recommendations;
  exportData: ExportData;
}

export interface CalendarData {
  id: string;
  title: string;
  description: string;
  startDate: string;
  endDate: string;
  content: CalendarContent[];
  themes: Theme[];
  platforms: Platform[];
}

export interface CalendarContent {
  id: string;
  title: string;
  description: string;
  contentType: string;
  platform: string;
  scheduledDate: string;
  theme: string;
  keywords: string[];
}

export interface Theme {
  id: string;
  name: string;
  description: string;
  weekNumber: number;
  contentTypes: string[];
}

export interface Platform {
  id: string;
  name: string;
  contentCount: number;
  postingSchedule: PostingSchedule[];
}

export interface PostingSchedule {
  day: string;
  time: string;
  contentType: string;
}

export interface QualityScores {
  overall: number;
  step1: number;
  step2: number;
  step3: number;
  step4: number;
  step5: number;
  step6: number;
  step7: number;
  step8: number;
  step9: number;
  step10: number;
  step11: number;
  step12: number;
}

export interface GenerationInsights {
  contentGaps: ContentGap[];
  keywordOpportunities: KeywordOpportunity[];
  audienceInsights: AudienceInsight[];
  platformPerformance: PlatformPerformance[];
}

export interface ContentGap {
  id: string;
  title: string;
  description: string;
  impact: number;
  priority: 'high' | 'medium' | 'low';
  estimatedTraffic: number;
}

export interface KeywordOpportunity {
  id: string;
  keyword: string;
  searchVolume: number;
  competition: number;
  relevance: number;
  estimatedTraffic: number;
}

export interface AudienceInsight {
  id: string;
  segment: string;
  demographics: string[];
  preferences: string[];
  engagementRate: number;
  bestTimes: string[];
}

export interface PlatformPerformance {
  id: string;
  platform: string;
  engagementRate: number;
  reach: number;
  conversionRate: number;
  bestContentTypes: string[];
}

export interface Recommendations {
  contentMix: ContentMixRecommendation;
  postingSchedule: PostingScheduleRecommendation;
  platformStrategy: PlatformStrategyRecommendation;
  optimizationTips: string[];
}

export interface ContentMixRecommendation {
  educational: number;
  thoughtLeadership: number;
  engagement: number;
  promotional: number;
  reasoning: string;
}

export interface PostingScheduleRecommendation {
  bestDays: string[];
  bestTimes: string[];
  frequency: string;
  reasoning: string;
}

export interface PlatformStrategyRecommendation {
  primaryPlatforms: string[];
  contentDistribution: Record<string, number>;
  crossPlatformStrategy: string;
}

export interface ExportData {
  calendarJson: string;
  insightsCsv: string;
  recommendationsPdf: string;
  qualityReport: string;
}

export interface CalendarGenerationProgress {
  status: 'initializing' | 'step1' | 'step2' | 'step3' | 'completed' | 'error';
  currentStep: number;
  stepProgress: number;
  overallProgress: number;
  stepResults: Record<number, StepResult>;
  qualityScores: QualityScores;
  transparencyMessages: string[];
  educationalContent: EducationalContent[];
  errors: ErrorInfo[];
  warnings: WarningInfo[];
}

export interface StepResult {
  stepNumber: number;
  stepName: string;
  results: any;
  qualityScore: number;
  executionTime: string;
  dataSourcesUsed: string[];
  insights: string[];
  recommendations: string[];
}

export interface EducationalContent {
  title: string;
  description: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  category: 'strategy' | 'analysis' | 'optimization' | 'quality';
  tips: string[];
  examples: string[];
  relatedConcepts: string[];
  nextSteps: string[];
}

export interface ErrorInfo {
  id: string;
  message: string;
  step: number;
  timestamp: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export interface WarningInfo {
  id: string;
  message: string;
  step: number;
  timestamp: string;
  severity: 'low' | 'medium' | 'high';
}

export interface DataSourceAttribution {
  id: string;
  name: string;
  type: 'strategy' | 'onboarding' | 'gap_analysis' | 'ai_analysis' | 'performance' | 'competitor';
  confidence: number;
  lastUpdated: string;
  dataPoints: DataPoint[];
}

export interface DataPoint {
  id: string;
  name: string;
  value: any;
  confidence: number;
  source: string;
  timestamp: string;
}

export interface QualityGateResult {
  id: string;
  name: string;
  status: 'passed' | 'failed' | 'warning';
  score: number;
  threshold: number;
  details: string;
  recommendations: string[];
}

export interface UserPreferences {
  transparencyLevel: 'basic' | 'detailed' | 'expert';
  educationalLevel: 'beginner' | 'intermediate' | 'advanced';
  autoExpandResults: boolean;
  showQualityDetails: boolean;
  enableNotifications: boolean;
}
