import { create } from 'zustand';
import { contentPlanningApi } from '../services/contentPlanningApi';

// Enhanced Strategy Types
export interface EnhancedStrategy {
  id: string;
  user_id: number;
  name: string;
  industry: string;
  
  // Business Context (8 inputs)
  business_objectives?: any;
  target_metrics?: any;
  content_budget?: number;
  team_size?: number;
  implementation_timeline?: string;
  market_share?: string;
  competitive_position?: string;
  performance_metrics?: any;
  
  // Audience Intelligence (6 inputs)
  content_preferences?: any;
  consumption_patterns?: any;
  audience_pain_points?: any;
  buying_journey?: any;
  seasonal_trends?: any;
  engagement_metrics?: any;
  
  // Competitive Intelligence (5 inputs)
  top_competitors?: any;
  competitor_content_strategies?: any;
  market_gaps?: any;
  industry_trends?: any;
  emerging_trends?: any;
  
  // Content Strategy (7 inputs)
  preferred_formats?: any;
  content_mix?: any;
  content_frequency?: string;
  optimal_timing?: any;
  quality_metrics?: any;
  editorial_guidelines?: any;
  brand_voice?: any;
  
  // Performance & Analytics (4 inputs)
  traffic_sources?: any;
  conversion_rates?: any;
  content_roi_targets?: any;
  ab_testing_capabilities?: boolean;
  
  // Enhanced AI Analysis
  comprehensive_ai_analysis?: any;
  onboarding_data_used?: any;
  strategic_scores?: any;
  market_positioning?: any;
  competitive_advantages?: any;
  strategic_risks?: any;
  opportunity_analysis?: any;
  
  // Metadata
  created_at: string;
  updated_at: string;
  completion_percentage: number;
  data_source_transparency?: any;
}

export interface EnhancedAIAnalysis {
  id: string;
  user_id: number;
  strategy_id: string;
  analysis_type: string;
  comprehensive_insights?: any;
  audience_intelligence?: any;
  competitive_intelligence?: any;
  performance_optimization?: any;
  content_calendar_optimization?: any;
  onboarding_data_used?: any;
  data_confidence_scores?: any;
  recommendation_quality_scores?: any;
  processing_time?: number;
  ai_service_status: string;
  prompt_version?: string;
  created_at: string;
  updated_at: string;
}

export interface OnboardingIntegration {
  id: string;
  user_id: number;
  strategy_id: string;
  website_analysis_data?: any;
  research_preferences_data?: any;
  api_keys_data?: any;
  field_mappings?: any;
  auto_populated_fields?: any;
  user_overrides?: any;
  data_quality_scores?: any;
  confidence_levels?: any;
  data_freshness?: any;
  created_at: string;
  updated_at: string;
}

export interface StrategicInputField {
  id: string;
  category: string;
  label: string;
  description: string;
  tooltip: string;
  type: 'text' | 'number' | 'select' | 'multiselect' | 'json' | 'boolean';
  required: boolean;
  options?: string[];
  placeholder?: string;
  validation?: any;
  auto_populated?: boolean;
  data_source?: string;
  confidence_level?: number;
}

export interface ProgressiveDisclosureStep {
  id: string;
  title: string;
  description: string;
  fields: string[];
  is_complete: boolean;
  is_visible: boolean;
  dependencies: string[];
}

export interface TooltipData {
  field_id: string;
  title: string;
  description: string;
  examples: string[];
  best_practices: string[];
  data_source?: string;
  confidence_level?: number;
}

// Store interface
interface EnhancedStrategyStore {
  // State
  strategies: EnhancedStrategy[];
  currentStrategy: EnhancedStrategy | null;
  aiAnalyses: EnhancedAIAnalysis[];
  onboardingIntegrations: OnboardingIntegration[];
  
  // Progressive Disclosure
  disclosureSteps: ProgressiveDisclosureStep[];
  currentStep: number;
  completedSteps: string[];
  
  // Tooltips
  tooltips: Record<string, TooltipData>;
  
  // Form State
  formData: Record<string, any>;
  formErrors: Record<string, string>;
  autoPopulatedFields: Record<string, any>;
  dataSources: Record<string, string>;
  
  // UI State
  loading: boolean;
  error: string | null;
  saving: boolean;
  aiGenerating: boolean;
  
  // Actions
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setSaving: (saving: boolean) => void;
  setAIGenerating: (generating: boolean) => void;
  
  // Strategy actions
  createEnhancedStrategy: (strategy: Partial<EnhancedStrategy>) => Promise<EnhancedStrategy>;
  updateEnhancedStrategy: (id: string, updates: Partial<EnhancedStrategy>) => Promise<void>;
  deleteEnhancedStrategy: (id: string) => Promise<void>;
  setCurrentStrategy: (strategy: EnhancedStrategy | null) => void;
  
  // Form actions
  updateFormField: (fieldId: string, value: any) => void;
  validateFormField: (fieldId: string) => boolean;
  validateAllFields: () => boolean;
  resetForm: () => void;
  
  // Progressive disclosure actions
  setCurrentStep: (step: number) => void;
  completeStep: (stepId: string) => void;
  canProceedToStep: (stepId: string) => boolean;
  getNextStep: () => ProgressiveDisclosureStep | null;
  getPreviousStep: () => ProgressiveDisclosureStep | null;
  
  // Auto-population actions
  autoPopulateFromOnboarding: () => Promise<void>;
  updateAutoPopulatedField: (fieldId: string, value: any, source: string) => void;
  overrideAutoPopulatedField: (fieldId: string, value: any) => void;
  
  // AI Analysis actions
  generateAIRecommendations: (strategyId: string) => Promise<void>;
  regenerateAIAnalysis: (strategyId: string, analysisType: string) => Promise<void>;
  
  // Data loading
  loadEnhancedStrategies: () => Promise<void>;
  loadAIAnalyses: (strategyId: string) => Promise<void>;
  loadOnboardingIntegration: (strategyId: string) => Promise<void>;
  
  // Tooltip actions
  getTooltipData: (fieldId: string) => TooltipData | null;
  updateTooltipData: (fieldId: string, data: TooltipData) => void;
  
  // Completion tracking
  calculateCompletionPercentage: () => number;
  getCompletionStats: () => {
    total_fields: number;
    filled_fields: number;
    completion_percentage: number;
    category_completion: Record<string, number>;
  };
}

// Strategic input fields configuration
export const STRATEGIC_INPUT_FIELDS: StrategicInputField[] = [
  // Business Context
  {
    id: 'business_objectives',
    category: 'business_context',
    label: 'Business Objectives',
    description: 'Primary and secondary business goals for content strategy',
    tooltip: 'Define your main business goals that content will support. Include both primary objectives (e.g., brand awareness) and secondary objectives (e.g., lead generation).',
    type: 'json',
    required: true,
    placeholder: 'Enter your business objectives'
  },
  {
    id: 'target_metrics',
    category: 'business_context',
    label: 'Target Metrics',
    description: 'KPIs and success metrics for content performance',
    tooltip: 'Specify the key performance indicators (KPIs) that will measure the success of your content strategy. Include metrics like traffic growth, engagement rates, and conversion rates.',
    type: 'json',
    required: true,
    placeholder: 'Define your target metrics'
  },
  {
    id: 'content_budget',
    category: 'business_context',
    label: 'Content Budget',
    description: 'Monthly or annual budget for content creation',
    tooltip: 'Set your content marketing budget. This helps determine the scope and scale of your content strategy, including team size, tools, and content production capabilities.',
    type: 'number',
    required: false,
    placeholder: 'Enter your content budget'
  },
  {
    id: 'team_size',
    category: 'business_context',
    label: 'Team Size',
    description: 'Number of people working on content',
    tooltip: 'Specify the size of your content team. This affects content production capacity and helps determine realistic content frequency and volume.',
    type: 'number',
    required: false,
    placeholder: 'Enter team size'
  },
  {
    id: 'implementation_timeline',
    category: 'business_context',
    label: 'Implementation Timeline',
    description: 'Timeline for strategy implementation',
    tooltip: 'Define how long you plan to implement this content strategy. Common timelines include 3 months, 6 months, or 1 year.',
    type: 'select',
    required: false,
    options: ['3 months', '6 months', '1 year', '2 years', 'Ongoing']
  },
  {
    id: 'market_share',
    category: 'business_context',
    label: 'Market Share',
    description: 'Current market share percentage',
    tooltip: 'Your current market share helps determine your competitive position and content strategy approach. Leaders focus on thought leadership, while challengers focus on differentiation.',
    type: 'text',
    required: false,
    placeholder: 'Enter market share percentage'
  },
  {
    id: 'competitive_position',
    category: 'business_context',
    label: 'Competitive Position',
    description: 'Market position relative to competitors',
    tooltip: 'Define your competitive position in the market. Options include Leader, Challenger, Niche, or Emerging. This influences your content strategy approach.',
    type: 'select',
    required: false,
    options: ['Leader', 'Challenger', 'Niche', 'Emerging']
  },
  {
    id: 'performance_metrics',
    category: 'business_context',
    label: 'Current Performance Metrics',
    description: 'Existing performance data and benchmarks',
    tooltip: 'Provide your current content performance metrics as a baseline. This helps measure improvement and set realistic targets.',
    type: 'json',
    required: false,
    placeholder: 'Enter current performance data'
  },
  
  // Audience Intelligence
  {
    id: 'content_preferences',
    category: 'audience_intelligence',
    label: 'Content Preferences',
    description: 'Preferred content formats and topics',
    tooltip: 'Identify what types of content your audience prefers. Consider formats (blog posts, videos, infographics) and topics that resonate most.',
    type: 'json',
    required: true,
    placeholder: 'Define content preferences'
  },
  {
    id: 'consumption_patterns',
    category: 'audience_intelligence',
    label: 'Consumption Patterns',
    description: 'When and how audience consumes content',
    tooltip: 'Understand when and how your audience consumes content. This includes peak times, preferred devices, and consumption channels.',
    type: 'json',
    required: false,
    placeholder: 'Describe consumption patterns'
  },
  {
    id: 'audience_pain_points',
    category: 'audience_intelligence',
    label: 'Audience Pain Points',
    description: 'Key challenges and pain points',
    tooltip: 'Identify the main challenges and pain points your audience faces. This helps create content that addresses real needs and provides value.',
    type: 'json',
    required: false,
    placeholder: 'List audience pain points'
  },
  {
    id: 'buying_journey',
    category: 'audience_intelligence',
    label: 'Buying Journey',
    description: 'Customer journey stages and touchpoints',
    tooltip: 'Map your audience\'s buying journey stages and the content touchpoints that influence their decisions.',
    type: 'json',
    required: false,
    placeholder: 'Define buying journey stages'
  },
  {
    id: 'seasonal_trends',
    category: 'audience_intelligence',
    label: 'Seasonal Trends',
    description: 'Seasonal content opportunities',
    tooltip: 'Identify seasonal trends and opportunities that affect your audience\'s content consumption and needs.',
    type: 'json',
    required: false,
    placeholder: 'Define seasonal trends'
  },
  {
    id: 'engagement_metrics',
    category: 'audience_intelligence',
    label: 'Engagement Metrics',
    description: 'Current engagement data',
    tooltip: 'Provide current engagement metrics to understand what content resonates with your audience.',
    type: 'json',
    required: false,
    placeholder: 'Enter engagement metrics'
  },
  
  // Competitive Intelligence
  {
    id: 'top_competitors',
    category: 'competitive_intelligence',
    label: 'Top Competitors',
    description: 'List of main competitors',
    tooltip: 'Identify your main competitors in the market. This helps understand competitive landscape and identify content opportunities.',
    type: 'json',
    required: false,
    placeholder: 'List top competitors'
  },
  {
    id: 'competitor_content_strategies',
    category: 'competitive_intelligence',
    label: 'Competitor Content Strategies',
    description: 'Analysis of competitor approaches',
    tooltip: 'Analyze your competitors\' content strategies to identify gaps, opportunities, and differentiation possibilities.',
    type: 'json',
    required: false,
    placeholder: 'Analyze competitor strategies'
  },
  {
    id: 'market_gaps',
    category: 'competitive_intelligence',
    label: 'Market Gaps',
    description: 'Identified market opportunities',
    tooltip: 'Identify gaps in the market that your content can address. These are opportunities where competitors are not providing adequate content.',
    type: 'json',
    required: false,
    placeholder: 'Identify market gaps'
  },
  {
    id: 'industry_trends',
    category: 'competitive_intelligence',
    label: 'Industry Trends',
    description: 'Current industry trends',
    tooltip: 'Stay current with industry trends that affect your audience and content strategy.',
    type: 'json',
    required: false,
    placeholder: 'List industry trends'
  },
  {
    id: 'emerging_trends',
    category: 'competitive_intelligence',
    label: 'Emerging Trends',
    description: 'Upcoming trends and opportunities',
    tooltip: 'Identify emerging trends that could provide early-mover advantages in content creation.',
    type: 'json',
    required: false,
    placeholder: 'Identify emerging trends'
  },
  
  // Content Strategy
  {
    id: 'preferred_formats',
    category: 'content_strategy',
    label: 'Preferred Formats',
    description: 'Content formats to focus on',
    tooltip: 'Choose the content formats that align with your audience preferences and business objectives.',
    type: 'multiselect',
    required: true,
    options: ['Blog Posts', 'Videos', 'Infographics', 'Webinars', 'Podcasts', 'Case Studies', 'Whitepapers', 'Social Media Posts']
  },
  {
    id: 'content_mix',
    category: 'content_strategy',
    label: 'Content Mix',
    description: 'Distribution of content types',
    tooltip: 'Define the percentage distribution of different content types in your strategy.',
    type: 'json',
    required: false,
    placeholder: 'Define content mix percentages'
  },
  {
    id: 'content_frequency',
    category: 'content_strategy',
    label: 'Content Frequency',
    description: 'How often to publish content',
    tooltip: 'Set realistic content publishing frequency based on your team capacity and audience expectations.',
    type: 'select',
    required: true,
    options: ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly']
  },
  {
    id: 'optimal_timing',
    category: 'content_strategy',
    label: 'Optimal Timing',
    description: 'Best times for publishing',
    tooltip: 'Identify the optimal times for publishing different types of content to maximize engagement.',
    type: 'json',
    required: false,
    placeholder: 'Define optimal publishing times'
  },
  {
    id: 'quality_metrics',
    category: 'content_strategy',
    label: 'Quality Metrics',
    description: 'Content quality standards',
    tooltip: 'Define the quality standards and metrics that will ensure your content meets your audience\'s expectations.',
    type: 'json',
    required: false,
    placeholder: 'Define quality standards'
  },
  {
    id: 'editorial_guidelines',
    category: 'content_strategy',
    label: 'Editorial Guidelines',
    description: 'Style and tone guidelines',
    tooltip: 'Establish editorial guidelines for consistent brand voice, tone, and style across all content.',
    type: 'json',
    required: false,
    placeholder: 'Define editorial guidelines'
  },
  {
    id: 'brand_voice',
    category: 'content_strategy',
    label: 'Brand Voice',
    description: 'Brand personality and voice',
    tooltip: 'Define your brand\'s personality and voice characteristics to ensure consistent messaging.',
    type: 'json',
    required: false,
    placeholder: 'Define brand voice'
  },
  
  // Performance & Analytics
  {
    id: 'traffic_sources',
    category: 'performance_analytics',
    label: 'Traffic Sources',
    description: 'Primary traffic sources',
    tooltip: 'Identify your main traffic sources to understand where your audience comes from and optimize accordingly.',
    type: 'json',
    required: false,
    placeholder: 'Define traffic sources'
  },
  {
    id: 'conversion_rates',
    category: 'performance_analytics',
    label: 'Conversion Rates',
    description: 'Current conversion data',
    tooltip: 'Track conversion rates across different content types and channels to identify what drives results.',
    type: 'json',
    required: false,
    placeholder: 'Enter conversion data'
  },
  {
    id: 'content_roi_targets',
    category: 'performance_analytics',
    label: 'Content ROI Targets',
    description: 'ROI goals and targets',
    tooltip: 'Set realistic ROI targets for your content marketing efforts to measure return on investment.',
    type: 'json',
    required: false,
    placeholder: 'Define ROI targets'
  },
  {
    id: 'ab_testing_capabilities',
    category: 'performance_analytics',
    label: 'A/B Testing Capabilities',
    description: 'A/B testing availability',
    tooltip: 'Indicate whether you have A/B testing capabilities to optimize content performance.',
    type: 'boolean',
    required: false
  }
];

// Progressive disclosure steps
const PROGRESSIVE_DISCLOSURE_STEPS: ProgressiveDisclosureStep[] = [
  {
    id: 'business_context',
    title: 'Business Context',
    description: 'Define your business objectives and context',
    fields: ['business_objectives', 'target_metrics', 'content_budget', 'team_size', 'implementation_timeline', 'market_share', 'competitive_position', 'performance_metrics'],
    is_complete: false,
    is_visible: true,
    dependencies: []
  },
  {
    id: 'audience_intelligence',
    title: 'Audience Intelligence',
    description: 'Understand your target audience',
    fields: ['content_preferences', 'consumption_patterns', 'audience_pain_points', 'buying_journey', 'seasonal_trends', 'engagement_metrics'],
    is_complete: false,
    is_visible: false,
    dependencies: ['business_context']
  },
  {
    id: 'competitive_intelligence',
    title: 'Competitive Intelligence',
    description: 'Analyze your competitive landscape',
    fields: ['top_competitors', 'competitor_content_strategies', 'market_gaps', 'industry_trends', 'emerging_trends'],
    is_complete: false,
    is_visible: false,
    dependencies: ['audience_intelligence']
  },
  {
    id: 'content_strategy',
    title: 'Content Strategy',
    description: 'Define your content approach',
    fields: ['preferred_formats', 'content_mix', 'content_frequency', 'optimal_timing', 'quality_metrics', 'editorial_guidelines', 'brand_voice'],
    is_complete: false,
    is_visible: false,
    dependencies: ['competitive_intelligence']
  },
  {
    id: 'performance_analytics',
    title: 'Performance & Analytics',
    description: 'Set up measurement and optimization',
    fields: ['traffic_sources', 'conversion_rates', 'content_roi_targets', 'ab_testing_capabilities'],
    is_complete: false,
    is_visible: false,
    dependencies: ['content_strategy']
  }
];

// Store implementation
export const useEnhancedStrategyStore = create<EnhancedStrategyStore>((set, get) => ({
  // Initial state
  strategies: [],
  currentStrategy: null,
  aiAnalyses: [],
  onboardingIntegrations: [],
  
  // Progressive Disclosure
  disclosureSteps: PROGRESSIVE_DISCLOSURE_STEPS,
  currentStep: 0,
  completedSteps: [],
  
  // Tooltips
  tooltips: {},
  
  // Form State
  formData: {},
  formErrors: {},
  autoPopulatedFields: {},
  dataSources: {},
  
  // UI State
  loading: false,
  error: null,
  saving: false,
  aiGenerating: false,
  
  // Actions
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  setSaving: (saving) => set({ saving }),
  setAIGenerating: (generating) => set({ aiGenerating: generating }),
  
  // Strategy actions
  createEnhancedStrategy: async (strategy) => {
    set({ saving: true, error: null });
    try {
      const newStrategy = await contentPlanningApi.createEnhancedStrategy(strategy);
      set((state) => ({
        strategies: [...state.strategies, newStrategy],
        saving: false,
      }));
      return newStrategy; // Return the created strategy
    } catch (error: any) {
      set({ error: error.message || 'Failed to create enhanced strategy', saving: false });
      throw error; // Re-throw the error so the calling function can handle it
    }
  },
  
  updateEnhancedStrategy: async (id, updates) => {
    set({ saving: true, error: null });
    try {
      const updatedStrategy = await contentPlanningApi.updateEnhancedStrategy(id, updates);
      set((state) => ({
        strategies: state.strategies.map((strategy) =>
          strategy.id === id ? updatedStrategy : strategy
        ),
        saving: false,
      }));
    } catch (error: any) {
      set({ error: error.message || 'Failed to update enhanced strategy', saving: false });
    }
  },
  
  deleteEnhancedStrategy: async (id) => {
    set({ saving: true, error: null });
    try {
      await contentPlanningApi.deleteEnhancedStrategy(id);
      set((state) => ({
        strategies: state.strategies.filter((strategy) => strategy.id !== id),
        saving: false,
      }));
    } catch (error: any) {
      set({ error: error.message || 'Failed to delete enhanced strategy', saving: false });
    }
  },
  
  setCurrentStrategy: (strategy) => set({ currentStrategy: strategy }),
  
  // Form actions
  updateFormField: (fieldId, value) => {
    set((state) => ({
      formData: { ...state.formData, [fieldId]: value },
      formErrors: { ...state.formErrors, [fieldId]: '' }
    }));
  },
  
  validateFormField: (fieldId) => {
    const field = STRATEGIC_INPUT_FIELDS.find(f => f.id === fieldId);
    if (!field) return true;
    
    const value = get().formData[fieldId];
    
    if (field.required && (!value || (Array.isArray(value) && value.length === 0))) {
      set((state) => ({
        formErrors: { ...state.formErrors, [fieldId]: `${field.label} is required` }
      }));
      return false;
    }
    
    return true;
  },
  
  validateAllFields: () => {
    const { formData } = get();
    let isValid = true;
    const errors: Record<string, string> = {};
    
    STRATEGIC_INPUT_FIELDS.forEach(field => {
      const value = formData[field.id];
      
      if (field.required && (!value || (Array.isArray(value) && value.length === 0))) {
        errors[field.id] = `${field.label} is required`;
        isValid = false;
      }
    });
    
    set({ formErrors: errors });
    return isValid;
  },
  
  resetForm: () => {
    set({
      formData: {},
      formErrors: {},
      autoPopulatedFields: {},
      dataSources: {},
      currentStep: 0,
      completedSteps: []
    });
  },
  
  // Progressive disclosure actions
  setCurrentStep: (step) => set({ currentStep: step }),
  
  completeStep: (stepId) => {
    set((state) => ({
      completedSteps: [...state.completedSteps, stepId],
      disclosureSteps: state.disclosureSteps.map(step => 
        step.id === stepId ? { ...step, is_complete: true } : step
      )
    }));
  },
  
  canProceedToStep: (stepId) => {
    const { disclosureSteps, completedSteps } = get();
    const step = disclosureSteps.find(s => s.id === stepId);
    if (!step) return false;
    
    return step.dependencies.every(dep => completedSteps.includes(dep));
  },
  
  getNextStep: () => {
    const { disclosureSteps, currentStep } = get();
    const nextStep = disclosureSteps[currentStep + 1];
    return nextStep && get().canProceedToStep(nextStep.id) ? nextStep : null;
  },
  
  getPreviousStep: () => {
    const { disclosureSteps, currentStep } = get();
    return currentStep > 0 ? disclosureSteps[currentStep - 1] : null;
  },
  
  // Auto-population actions
  autoPopulateFromOnboarding: async () => {
    set({ loading: true });
    try {
      console.log('🔄 Starting auto-population from onboarding data...');
      
      // This would call the backend to get onboarding data and auto-populate fields
      const response = await contentPlanningApi.getOnboardingData();
      console.log('📡 Backend response:', response);
      
      // Extract field values and sources from the new backend format
      const fields = response.data?.fields || {};
      const sources = response.data?.sources || {};
      
      console.log('📋 Extracted fields:', fields);
      console.log('🔗 Data sources:', sources);
      
      // Transform the fields object to extract values for formData
      const fieldValues: Record<string, any> = {};
      const autoPopulatedFields: Record<string, any> = {};
      
      Object.keys(fields).forEach(fieldId => {
        const fieldData = fields[fieldId];
        console.log(`🔍 Processing field ${fieldId}:`, fieldData);
        
        if (fieldData && typeof fieldData === 'object' && 'value' in fieldData) {
          fieldValues[fieldId] = fieldData.value;
          autoPopulatedFields[fieldId] = fieldData.value;
          console.log(`✅ Auto-populated ${fieldId}:`, fieldData.value);
        } else {
          console.log(`❌ Skipping ${fieldId} - invalid data structure`);
        }
      });
      
      console.log('📝 Final field values:', fieldValues);
      console.log('🔄 Final auto-populated fields:', autoPopulatedFields);
      
      set((state) => ({
        autoPopulatedFields,
        dataSources: sources,
        formData: { ...state.formData, ...fieldValues }
      }));
      
      console.log('✅ Auto-population completed successfully');
    } catch (error: any) {
      console.error('❌ Auto-population error:', error);
      set({ error: error.message || 'Failed to auto-populate from onboarding' });
    } finally {
      set({ loading: false });
    }
  },
  
  updateAutoPopulatedField: (fieldId, value, source) => {
    set((state) => ({
      autoPopulatedFields: { ...state.autoPopulatedFields, [fieldId]: value },
      dataSources: { ...state.dataSources, [fieldId]: source }
    }));
  },
  
  overrideAutoPopulatedField: (fieldId, value) => {
    set((state) => ({
      formData: { ...state.formData, [fieldId]: value },
      autoPopulatedFields: { ...state.autoPopulatedFields, [fieldId]: value }
    }));
  },
  
  // AI Analysis actions
  generateAIRecommendations: async (strategyId) => {
    set({ aiGenerating: true, error: null });
    try {
      const aiAnalysis = await contentPlanningApi.generateEnhancedAIRecommendations(strategyId);
      set((state) => ({
        aiAnalyses: [...state.aiAnalyses, aiAnalysis],
        aiGenerating: false
      }));
    } catch (error: any) {
      set({ error: error.message || 'Failed to generate AI recommendations', aiGenerating: false });
    }
  },
  
  regenerateAIAnalysis: async (strategyId: string, analysisType: string) => {
    set({ aiGenerating: true, error: null });
    try {
      const aiAnalysis = await contentPlanningApi.regenerateAIAnalysis(strategyId, analysisType);
      set((state) => ({
        aiAnalyses: state.aiAnalyses.map(analysis =>
          analysis.strategy_id === strategyId && analysis.analysis_type === analysisType
            ? { ...analysis, ...aiAnalysis }
            : analysis
        ),
        aiGenerating: false
      }));
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to regenerate AI analysis',
        aiGenerating: false 
      });
    }
  },
  
  // Data loading
  loadEnhancedStrategies: async () => {
    set({ loading: true, error: null });
    try {
      const strategies = await contentPlanningApi.getEnhancedStrategies();
      set({ strategies, loading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to load enhanced strategies', loading: false });
    }
  },
  
  loadAIAnalyses: async (strategyId) => {
    set({ loading: true, error: null });
    try {
      const analyses = await contentPlanningApi.getEnhancedAIAnalyses(strategyId);
      set({ aiAnalyses: analyses, loading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to load AI analyses', loading: false });
    }
  },
  
  loadOnboardingIntegration: async (strategyId) => {
    set({ loading: true, error: null });
    try {
      const integration = await contentPlanningApi.getOnboardingIntegration(strategyId);
      set({ onboardingIntegrations: [integration], loading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to load onboarding integration', loading: false });
    }
  },
  
  // Tooltip actions
  getTooltipData: (fieldId) => {
    const field = STRATEGIC_INPUT_FIELDS.find(f => f.id === fieldId);
    if (!field) return null;
    
    const state = get();
    const autoPopulatedFields = state.autoPopulatedFields || {};
    const dataSources = state.dataSources || {};
    
    return {
      field_id: fieldId,
      title: field.label,
      description: field.tooltip,
      examples: [],
      best_practices: [],
      data_source: dataSources[fieldId],
      confidence_level: autoPopulatedFields[fieldId] ? 0.8 : undefined
    };
  },
  
  updateTooltipData: (fieldId, data) => {
    set((state) => ({
      tooltips: { ...state.tooltips, [fieldId]: data }
    }));
  },
  
  // Completion tracking
  calculateCompletionPercentage: () => {
    const { formData } = get();
    const requiredFields = STRATEGIC_INPUT_FIELDS.filter(field => field.required);
    const filledRequiredFields = requiredFields.filter(field => 
      formData[field.id] && 
      (typeof formData[field.id] === 'string' ? formData[field.id].trim() !== '' : true)
    );
    
    return (filledRequiredFields.length / requiredFields.length) * 100;
  },
  
  getCompletionStats: () => {
    const { formData } = get();
    const categories = ['business_context', 'audience_intelligence', 'competitive_intelligence', 'content_strategy', 'performance_analytics'];
    
    const category_completion: Record<string, number> = {};
    
    categories.forEach(category => {
      const categoryFields = STRATEGIC_INPUT_FIELDS.filter(field => field.category === category);
      const filledFields = categoryFields.filter(field => 
        formData[field.id] && 
        (typeof formData[field.id] === 'string' ? formData[field.id].trim() !== '' : true)
      );
      
      category_completion[category] = (filledFields.length / categoryFields.length) * 100;
    });
    
    const total_fields = STRATEGIC_INPUT_FIELDS.length;
    const filled_fields = STRATEGIC_INPUT_FIELDS.filter(field => 
      formData[field.id] && 
      (typeof formData[field.id] === 'string' ? formData[field.id].trim() !== '' : true)
    ).length;
    
    return {
      total_fields,
      filled_fields,
      completion_percentage: (filled_fields / total_fields) * 100,
      category_completion
    };
  }
})); 