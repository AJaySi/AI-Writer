import { create } from 'zustand';
import { contentPlanningApi } from '../services/contentPlanningApi';

// Global flag to prevent multiple simultaneous auto-population calls
let isAutoPopulating = false;

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

// Strategy Builder Store Interface
interface StrategyBuilderStore {
  // Strategy State
  strategies: EnhancedStrategy[];
  currentStrategy: EnhancedStrategy | null;
  
  // Form State
  formData: Record<string, any>;
  formErrors: Record<string, string>;
  
  // Auto-Population State
  autoPopulatedFields: Record<string, any>;
  dataSources: Record<string, string>;
  inputDataPoints: Record<string, any>; // Detailed input data points from backend
  personalizationData: Record<string, any>; // Personalization data for each field
  confidenceScores: Record<string, number>; // Confidence scores for each field
  autoPopulationBlocked: boolean;
  
  // UI State
  loading: boolean;
  error: string | null;
  saving: boolean;
  
  // Strategy Actions
  createStrategy: (strategy: Partial<EnhancedStrategy>) => Promise<EnhancedStrategy>;
  updateStrategy: (id: string, updates: Partial<EnhancedStrategy>) => Promise<void>;
  deleteStrategy: (id: string) => Promise<void>;
  setCurrentStrategy: (strategy: EnhancedStrategy | null) => void;
  loadStrategies: () => Promise<void>;
  
  // Form Actions
  updateFormField: (fieldId: string, value: any) => void;
  validateFormField: (fieldId: string) => boolean;
  validateAllFields: () => boolean;
  resetForm: () => void;
  setFormData: (data: Record<string, any>) => void;
  setFormErrors: (errors: Record<string, string>) => void;
  
  // Auto-Population Actions
  autoPopulateFromOnboarding: (forceRefresh?: boolean) => Promise<void>;
  updateAutoPopulatedField: (fieldId: string, value: any, source: string) => void;
  overrideAutoPopulatedField: (fieldId: string, value: any) => void;
  
  // UI Actions
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setSaving: (saving: boolean) => void;
  
  // Completion Tracking
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
    description: 'Current market position and share',
    tooltip: 'Indicate your current market share and position. This helps tailor content strategy to either defend your position or gain market share.',
    type: 'text',
    required: false,
    placeholder: 'Enter your market share'
  },
  {
    id: 'competitive_position',
    category: 'business_context',
    label: 'Competitive Position',
    description: 'Position relative to competitors',
    tooltip: 'Describe your competitive position in the market. Are you a leader, challenger, follower, or niche player?',
    type: 'select',
    required: false,
    options: ['Market Leader', 'Challenger', 'Follower', 'Niche Player']
  },
  {
    id: 'performance_metrics',
    category: 'business_context',
    label: 'Performance Metrics',
    description: 'Current performance indicators',
    tooltip: 'Document your current performance metrics to establish a baseline for measuring strategy success.',
    type: 'json',
    required: false,
    placeholder: 'Enter current performance metrics'
  },
  
  // Audience Intelligence
  {
    id: 'content_preferences',
    category: 'audience_intelligence',
    label: 'Content Preferences',
    description: 'Preferred content types and formats',
    tooltip: 'Identify what types of content your audience prefers. Consider formats like blog posts, videos, infographics, podcasts, etc.',
    type: 'multiselect',
    required: true,
    options: ['Blog Posts', 'Videos', 'Infographics', 'Podcasts', 'Webinars', 'Case Studies', 'Whitepapers', 'Social Media Posts']
  },
  {
    id: 'consumption_patterns',
    category: 'audience_intelligence',
    label: 'Consumption Patterns',
    description: 'How and when audience consumes content',
    tooltip: 'Understand when and how your audience consumes content. This helps optimize publishing schedules and content formats.',
    type: 'json',
    required: false,
    placeholder: 'Describe consumption patterns'
  },
  {
    id: 'audience_pain_points',
    category: 'audience_intelligence',
    label: 'Audience Pain Points',
    description: 'Key challenges and problems',
    tooltip: 'Identify the main challenges and pain points your audience faces. This helps create content that addresses real needs.',
    type: 'multiselect',
    required: true,
    options: ['Lack of Time', 'Information Overload', 'Budget Constraints', 'Technical Complexity', 'Decision Paralysis', 'Quality Concerns']
  },
  {
    id: 'buying_journey',
    category: 'audience_intelligence',
    label: 'Buying Journey',
    description: 'Customer journey stages and touchpoints',
    tooltip: 'Map out your customer journey stages and identify key touchpoints where content can influence decisions.',
    type: 'json',
    required: false,
    placeholder: 'Describe buying journey'
  },
  {
    id: 'seasonal_trends',
    category: 'audience_intelligence',
    label: 'Seasonal Trends',
    description: 'Seasonal patterns and trends',
    tooltip: 'Identify seasonal patterns in your industry or audience behavior that should influence content planning.',
    type: 'multiselect',
    required: false,
    options: ['Q1 Planning', 'Q2 Execution', 'Q3 Optimization', 'Q4 Review', 'Holiday Season', 'Back to School', 'Summer Slowdown']
  },
  {
    id: 'engagement_metrics',
    category: 'audience_intelligence',
    label: 'Engagement Metrics',
    description: 'Current engagement performance',
    tooltip: 'Document current engagement metrics to understand what content resonates with your audience.',
    type: 'json',
    required: false,
    placeholder: 'Enter engagement metrics'
  },
  
  // Competitive Intelligence
  {
    id: 'top_competitors',
    category: 'competitive_intelligence',
    label: 'Top Competitors',
    description: 'Main competitors in your market',
    tooltip: 'Identify your main competitors and analyze their strengths and weaknesses.',
    type: 'multiselect',
    required: true,
    placeholder: 'Enter competitor names'
  },
  {
    id: 'competitor_content_strategies',
    category: 'competitive_intelligence',
    label: 'Competitor Content Strategies',
    description: 'Content strategies of competitors',
    tooltip: 'Analyze what content strategies your competitors are using and their effectiveness.',
    type: 'json',
    required: false,
    placeholder: 'Describe competitor content strategies'
  },
  {
    id: 'market_gaps',
    category: 'competitive_intelligence',
    label: 'Market Gaps',
    description: 'Unfilled market opportunities',
    tooltip: 'Identify gaps in the market that your content can address.',
    type: 'multiselect',
    required: false,
    options: ['Underserved Audience', 'Content Format Gap', 'Topic Gap', 'Channel Gap', 'Timing Gap']
  },
  {
    id: 'industry_trends',
    category: 'competitive_intelligence',
    label: 'Industry Trends',
    description: 'Current industry trends and patterns',
    tooltip: 'Stay updated on current trends in your industry that should influence content strategy.',
    type: 'multiselect',
    required: false,
    options: ['Digital Transformation', 'AI Integration', 'Sustainability', 'Remote Work', 'E-commerce Growth', 'Video Content', 'Personalization']
  },
  {
    id: 'emerging_trends',
    category: 'competitive_intelligence',
    label: 'Emerging Trends',
    description: 'New and emerging market trends',
    tooltip: 'Identify emerging trends that could impact your content strategy in the future.',
    type: 'json',
    required: false,
    placeholder: 'Describe emerging trends'
  },
  
  // Content Strategy
  {
    id: 'preferred_formats',
    category: 'content_strategy',
    label: 'Preferred Formats',
    description: 'Content formats to focus on',
    tooltip: 'Choose the content formats that align with your audience preferences and business goals.',
    type: 'multiselect',
    required: true,
    options: ['Blog Posts', 'Videos', 'Infographics', 'Podcasts', 'Webinars', 'Case Studies', 'Whitepapers', 'Social Media Posts', 'Email Newsletters', 'Interactive Content']
  },
  {
    id: 'content_mix',
    category: 'content_strategy',
    label: 'Content Mix',
    description: 'Distribution of content types',
    tooltip: 'Define the ideal mix of content types for your strategy (e.g., 40% educational, 30% promotional, 30% entertaining).',
    type: 'json',
    required: false,
    placeholder: 'Define content mix percentages'
  },
  {
    id: 'content_frequency',
    category: 'content_strategy',
    label: 'Content Frequency',
    description: 'How often to publish content',
    tooltip: 'Determine how frequently you will publish content across different channels.',
    type: 'select',
    required: true,
    options: ['Daily', '2-3 times per week', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly']
  },
  {
    id: 'optimal_timing',
    category: 'content_strategy',
    label: 'Optimal Timing',
    description: 'Best times to publish content',
    tooltip: 'Identify the optimal times to publish content for maximum engagement.',
    type: 'multiselect',
    required: false,
    options: ['Monday Morning', 'Tuesday Midday', 'Wednesday Afternoon', 'Thursday Evening', 'Friday Morning', 'Weekend']
  },
  {
    id: 'quality_metrics',
    category: 'content_strategy',
    label: 'Quality Metrics',
    description: 'Standards for content quality',
    tooltip: 'Define the quality standards and metrics for your content.',
    type: 'json',
    required: false,
    placeholder: 'Define quality metrics'
  },
  {
    id: 'editorial_guidelines',
    category: 'content_strategy',
    label: 'Editorial Guidelines',
    description: 'Content creation guidelines',
    tooltip: 'Establish editorial guidelines to maintain consistency across all content.',
    type: 'json',
    required: false,
    placeholder: 'Define editorial guidelines'
  },
  {
    id: 'brand_voice',
    category: 'content_strategy',
    label: 'Brand Voice',
    description: 'Tone and style for content',
    tooltip: 'Define your brand voice and tone to ensure consistent messaging.',
    type: 'select',
    required: true,
    options: ['Professional', 'Casual', 'Friendly', 'Authoritative', 'Humorous', 'Inspirational', 'Educational']
  },
  
  // Performance & Analytics
  {
    id: 'traffic_sources',
    category: 'performance_analytics',
    label: 'Traffic Sources',
    description: 'Primary sources of website traffic',
    tooltip: 'Identify your main traffic sources to optimize content distribution.',
    type: 'multiselect',
    required: false,
    options: ['Organic Search', 'Social Media', 'Email Marketing', 'Direct Traffic', 'Referral Traffic', 'Paid Advertising']
  },
  {
    id: 'conversion_rates',
    category: 'performance_analytics',
    label: 'Conversion Rates',
    description: 'Current conversion performance',
    tooltip: 'Track your current conversion rates to set realistic improvement targets.',
    type: 'json',
    required: false,
    placeholder: 'Enter conversion rates'
  },
  {
    id: 'content_roi_targets',
    category: 'performance_analytics',
    label: 'Content ROI Targets',
    description: 'Target return on investment for content',
    tooltip: 'Set realistic ROI targets for your content marketing efforts.',
    type: 'json',
    required: false,
    placeholder: 'Define ROI targets'
  },
  {
    id: 'ab_testing_capabilities',
    category: 'performance_analytics',
    label: 'A/B Testing Capabilities',
    description: 'Ability to test content variations',
    tooltip: 'Indicate whether you have the capability to conduct A/B testing on your content.',
    type: 'boolean',
    required: false
  }
];

// Strategy Builder Store Implementation
export const useStrategyBuilderStore = create<StrategyBuilderStore>((set, get) => ({
  // Initial State
  strategies: [],
  currentStrategy: null,
  
  // Form State
  formData: {},
  formErrors: {},
  
  // Auto-Population State
  autoPopulatedFields: {},
  dataSources: {},
  inputDataPoints: {},
  personalizationData: {},
  confidenceScores: {},
  autoPopulationBlocked: false,
  
  // UI State
  loading: false,
  error: null,
  saving: false,
  
  // Strategy Actions
  createStrategy: async (strategy) => {
    set({ saving: true, error: null });
    try {
      const newStrategy = await contentPlanningApi.createEnhancedStrategy(strategy);
      set((state) => ({
        strategies: [...state.strategies, newStrategy],
        saving: false,
      }));
      return newStrategy;
    } catch (error: any) {
      set({ error: error.message || 'Failed to create strategy', saving: false });
      throw error;
    }
  },
  
  updateStrategy: async (id, updates) => {
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
      set({ error: error.message || 'Failed to update strategy', saving: false });
    }
  },
  
  deleteStrategy: async (id) => {
    set({ saving: true, error: null });
    try {
      await contentPlanningApi.deleteEnhancedStrategy(id);
      set((state) => ({
        strategies: state.strategies.filter((strategy) => strategy.id !== id),
        saving: false,
      }));
    } catch (error: any) {
      set({ error: error.message || 'Failed to delete strategy', saving: false });
    }
  },
  
  setCurrentStrategy: (strategy) => {
    set({ currentStrategy: strategy });
  },
  
  loadStrategies: async () => {
    set({ loading: true, error: null });
    try {
      const response = await contentPlanningApi.getEnhancedStrategies();
      set({ strategies: response.strategies || [], loading: false });
    } catch (error: any) {
      set({ error: error.message || 'Failed to load strategies', loading: false });
    }
  },
  
  // Form Actions
  updateFormField: (fieldId, value) => {
    set((state) => ({
      formData: { ...state.formData, [fieldId]: value },
      formErrors: { ...state.formErrors, [fieldId]: '' } // Clear error when field is updated
    }));
  },
  
  validateFormField: (fieldId) => {
    const field = STRATEGIC_INPUT_FIELDS.find(f => f.id === fieldId);
    if (!field) return true;
    
    const value = get().formData[fieldId];
    let isValid = true;
    let errorMessage = '';
    
    if (field.required && (!value || (Array.isArray(value) && value.length === 0))) {
      isValid = false;
      errorMessage = `${field.label} is required`;
    }
    
    set((state) => ({
      formErrors: { ...state.formErrors, [fieldId]: errorMessage }
    }));
    
    return isValid;
  },
  
  validateAllFields: () => {
    const formData = get().formData;
    const errors: Record<string, string> = {};
    let allValid = true;
    
    STRATEGIC_INPUT_FIELDS.forEach(field => {
      const value = formData[field.id];
      if (field.required && (!value || (Array.isArray(value) && value.length === 0))) {
        errors[field.id] = `${field.label} is required`;
        allValid = false;
      }
    });
    
    set({ formErrors: errors });
    return allValid;
  },
  
  resetForm: () => {
    set({ formData: {}, formErrors: {} });
  },
  
  setFormData: (data) => {
    set({ formData: data });
  },
  
  setFormErrors: (errors) => {
    set({ formErrors: errors });
  },
  
  // Auto-Population Actions
  autoPopulateFromOnboarding: async (forceRefresh: boolean = false) => {
    // Global protection against multiple simultaneous calls
    if (isAutoPopulating) {
      console.log('⏸️ Auto-population skipped - already running globally');
      return;
    }
    
    isAutoPopulating = true;
    
    try {
      // Skip if already loading
      if (get().loading) {
        console.log('⏸️ Auto-population skipped - already loading');
        return;
      }

      // Skip if already populated and not forcing refresh
      if (!forceRefresh && Object.keys(get().autoPopulatedFields).length > 0) {
        console.log('⏸️ Auto-population skipped - already populated');
        return;
      }

      // Skip if there was a recent error
      const lastError = get().error;
      if (lastError && (lastError.includes('No response from server') || lastError.includes('Too many requests'))) {
        console.log('⏸️ Auto-population skipped - recent server error');
        return;
      }

      // Skip if auto-population is blocked
      if (get().autoPopulationBlocked) {
        console.log('⏸️ Auto-population skipped - blocked due to previous errors');
        return;
      }

      // Add a longer delay to prevent rate limiting
      await new Promise(resolve => setTimeout(resolve, 500));

      set({ loading: true });
      
      console.log('🔄 Starting auto-population from onboarding data...');
      
      // Optionally clear backend caches to force fresh values
      if (forceRefresh) {
        try {
          await contentPlanningApi.clearEnhancedCache(1);
          console.log('♻️ Cleared enhanced strategy cache for fresh onboarding data');
        } catch (e) {
          console.warn('Cache clear failed (non-blocking):', e);
        }
      }

      // Fetch onboarding data to auto-populate fields
      const response = await contentPlanningApi.getOnboardingData();
      console.log('📡 Backend response:', response);
      
      // Extract field values and sources from the new backend format
      const fields = response.data?.fields || {};
      const sources = response.data?.sources || {};
      const inputDataPoints = response.data?.input_data_points || {};
      
      console.log('📋 Extracted fields:', fields);
      console.log('🔗 Data sources:', sources);
      console.log('📝 Input data points:', inputDataPoints);
      
      // Transform the fields object to extract values for formData
      const fieldValues: Record<string, any> = {};
      const autoPopulatedFields: Record<string, any> = {};
      const personalizationData: Record<string, any> = {};
      const confidenceScores: Record<string, number> = {};
      
      // Check if fields is empty and provide fallback
      if (Object.keys(fields).length === 0) {
        console.log('⚠️ No fields found in onboarding data, using default values');
        
        // Set default values for strategy builder
        const defaultFields: Record<string, any> = {
          industry: 'Technology',
          business_objectives: 'Increase brand awareness and drive sales',
          target_metrics: { traffic: 10000, conversion_rate: 2.5 },
          content_budget: 5000,
          team_size: 3,
          content_preferences: ['Blog posts', 'Social media', 'Email marketing'],
          preferred_formats: ['Blog posts', 'Whitepapers', 'Videos'],
          content_mix: { blog_posts: 40, whitepapers: 20, videos: 15, social_media: 25 }
        };
        
        Object.keys(defaultFields).forEach(fieldId => {
          fieldValues[fieldId] = defaultFields[fieldId];
          autoPopulatedFields[fieldId] = defaultFields[fieldId];
          confidenceScores[fieldId] = 0.7; // Medium confidence for defaults
          console.log(`✅ Set default value for ${fieldId}:`, defaultFields[fieldId]);
        });
      } else {
        // Process actual fields from backend
        Object.keys(fields).forEach(fieldId => {
          const fieldData = fields[fieldId];
          console.log(`🔍 Processing field ${fieldId}:`, fieldData);
          
          if (fieldData && typeof fieldData === 'object' && 'value' in fieldData) {
            fieldValues[fieldId] = fieldData.value;
            autoPopulatedFields[fieldId] = fieldData.value;
            
            // Extract personalization data if available
            if (fieldData.personalization_data) {
              personalizationData[fieldId] = fieldData.personalization_data;
              console.log(`🎯 Personalization data for ${fieldId}:`, fieldData.personalization_data);
            }
            
            // Extract confidence score if available
            if (fieldData.confidence_score) {
              confidenceScores[fieldId] = fieldData.confidence_score;
              console.log(`💯 Confidence score for ${fieldId}:`, fieldData.confidence_score);
            }
            
            console.log(`✅ Auto-populated ${fieldId}:`, fieldData.value);
          } else {
            console.log(`❌ Skipping ${fieldId} - invalid data structure`);
          }
        });
      }
      
      console.log('📝 Final field values:', fieldValues);
      console.log('🔄 Final auto-populated fields:', autoPopulatedFields);
      console.log('🎯 Personalization data:', personalizationData);
      console.log('💯 Confidence scores:', confidenceScores);
      
      set((state) => ({
        autoPopulatedFields,
        dataSources: sources,
        inputDataPoints,
        personalizationData,
        confidenceScores,
        formData: { ...state.formData, ...fieldValues }
      }));
      
      console.log('✅ Auto-population completed successfully');
    } catch (error: any) {
      console.error('❌ Auto-population error:', error);
      const errorMessage = error.message || 'Failed to auto-populate from onboarding';
      set({ 
        error: errorMessage,
        loading: false 
      });
      
      // If it's a rate limit error, set a flag to prevent further attempts
      if (errorMessage.includes('Too many requests') || errorMessage.includes('No response from server')) {
        set({ autoPopulationBlocked: true });
      }
    } finally {
      set({ loading: false });
      isAutoPopulating = false; // Reset global flag
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
  
  // UI Actions
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  setSaving: (saving) => set({ saving }),
  
  // Completion Tracking
  calculateCompletionPercentage: () => {
    const formData = get().formData;
    const requiredFields = STRATEGIC_INPUT_FIELDS.filter(field => field.required);
    const filledRequiredFields = requiredFields.filter(field => {
      const value = formData[field.id];
      return value && (Array.isArray(value) ? value.length > 0 : true);
    });
    
    return requiredFields.length > 0 ? (filledRequiredFields.length / requiredFields.length) * 100 : 0;
  },
  
  getCompletionStats: () => {
    const formData = get().formData;
    const totalFields = STRATEGIC_INPUT_FIELDS.length;
    const filledFields = STRATEGIC_INPUT_FIELDS.filter(field => {
      const value = formData[field.id];
      return value && (Array.isArray(value) ? value.length > 0 : true);
    }).length;
    
    const completionPercentage = totalFields > 0 ? (filledFields / totalFields) * 100 : 0;
    
    // Calculate completion by category
    const categoryCompletion: Record<string, number> = {};
    const categories = Array.from(new Set(STRATEGIC_INPUT_FIELDS.map(field => field.category)));
    
    categories.forEach(category => {
      const categoryFields = STRATEGIC_INPUT_FIELDS.filter(field => field.category === category);
      const filledCategoryFields = categoryFields.filter(field => {
        const value = formData[field.id];
        return value && (Array.isArray(value) ? value.length > 0 : true);
      }).length;
      
      categoryCompletion[category] = categoryFields.length > 0 ? (filledCategoryFields / categoryFields.length) * 100 : 0;
    });
    
    return {
      total_fields: totalFields,
      filled_fields: filledFields,
      completion_percentage: completionPercentage,
      category_completion: categoryCompletion
    };
  }
}));
