// SEO CopilotKit Store
// Zustand store for managing SEO CopilotKit state and actions

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { 
  SEOCopilotState, 
  SEOAnalysisData, 
  PersonalizationData, 
  DashboardLayout, 
  CopilotSuggestion,
  TimeRange,
  ChartType
} from '../types/seoCopilotTypes';
import { seoApiService } from '../services/seoApiService';

// Default dashboard layout
const defaultDashboardLayout: DashboardLayout = {
  focusArea: 'overview',
  layout: 'overview',
  hiddenSections: [],
  chartConfigs: []
};

// Default suggestions
const defaultSuggestions: CopilotSuggestion[] = [
  {
    id: 'analyze-seo',
    title: '🔍 Analyze my SEO health',
    message: 'perform a comprehensive SEO analysis and identify priority issues',
    icon: '🔍',
    category: 'analysis',
    priority: 'high',
    action: 'analyzeSEOComprehensive'
  },
  {
    id: 'generate-meta',
    title: '📝 Generate meta descriptions',
    message: 'create optimized meta descriptions for my website pages',
    icon: '📝',
    category: 'optimization',
    priority: 'medium',
    action: 'generateMetaDescriptions'
  },
  {
    id: 'analyze-speed',
    title: '⚡ Check page speed',
    message: 'analyze my website performance and get optimization recommendations',
    icon: '⚡',
    category: 'analysis',
    priority: 'high',
    action: 'analyzePageSpeed'
  },
  {
    id: 'explain-seo',
    title: '🎓 Learn SEO basics',
    message: 'explain SEO concepts and best practices for my business',
    icon: '🎓',
    category: 'education',
    priority: 'medium',
    action: 'explainSEOConcept'
  }
];

// Create the store
export const useSEOCopilotStore = create<SEOCopilotState>()(
  devtools(
    (set, get) => ({
      // Initial state
      isLoading: false,
      isAnalyzing: false,
      isGenerating: false,
      analysisData: null,
      personalizationData: null,
      activeChart: null,
      dashboardLayout: defaultDashboardLayout,
      suggestions: defaultSuggestions,
      error: null,
      lastError: null,

      // Actions
      setLoading: (loading: boolean) => set({ isLoading: loading }),
      setAnalyzing: (analyzing: boolean) => set({ isAnalyzing: analyzing }),
      setGenerating: (generating: boolean) => set({ isGenerating: generating }),
      
      setAnalysisData: (data: SEOAnalysisData | null) => {
        set({ analysisData: data });
        
        // Update suggestions based on analysis data
        if (data) {
          const newSuggestions = get().generateContextualSuggestions(data);
          set({ suggestions: newSuggestions });
        }
      },
      
      setPersonalizationData: (data: PersonalizationData | null) => set({ personalizationData: data }),
      setActiveChart: (chart: string | null) => set({ activeChart: chart }),
      
      setDashboardLayout: (layout: DashboardLayout) => {
        set({ dashboardLayout: layout });
        // Save layout to backend
        seoApiService.updateDashboardLayout(layout).catch(console.error);
      },
      
      setSuggestions: (suggestions: CopilotSuggestion[]) => set({ suggestions }),
      setError: (error: string | null) => set({ error, lastError: error ? new Error(error) : null }),
      clearError: () => set({ error: null, lastError: null }),

      // Additional helper methods
      generateContextualSuggestions: (analysisData: SEOAnalysisData): CopilotSuggestion[] => {
        const suggestions: CopilotSuggestion[] = [...defaultSuggestions];
        
        // Add contextual suggestions based on analysis data (defensive checks)
        const criticalCount = (analysisData as any)?.critical_issues?.length || 0;
        if (criticalCount > 0) {
          suggestions.unshift({
            id: 'fix-critical-issues',
            title: `🚨 Fix ${criticalCount} critical issues`,
            message: `generate action plans for my ${criticalCount} critical SEO issues`,
            icon: '🚨',
            category: 'optimization',
            priority: 'high',
            action: 'identifySEOOpportunities'
          });
        }

        const healthScore = (analysisData as any)?.health_score ?? (analysisData as any)?.overall_score;
        if (typeof healthScore === 'number' && healthScore < 70) {
          suggestions.unshift({
            id: 'improve-score',
            title: '⚠️ Improve SEO score',
            message: 'help me improve my SEO health score with specific recommendations',
            icon: '⚠️',
            category: 'optimization',
            priority: 'high',
            action: 'analyzeSEOComprehensive'
          });
        }

        // Mobile performance fallback paths
        const mobileScore = (analysisData as any)?.mobile_speed?.mobile_score
          ?? (analysisData as any)?.data?.mobile_speed?.mobile_score
          ?? (analysisData as any)?.performance?.mobile_score
          ?? (analysisData as any)?.data?.performance?.mobile_score;

        if (typeof mobileScore === 'number' && mobileScore < 80) {
          suggestions.push({
            id: 'optimize-mobile',
            title: '📱 Optimize mobile performance',
            message: 'focus on mobile SEO performance and optimization opportunities',
            icon: '📱',
            category: 'optimization',
            priority: 'medium',
            action: 'analyzePageSpeed'
          });
        }

        return suggestions;
      },

      // API integration methods
      loadPersonalizationData: async () => {
        try {
          set({ isLoading: true, error: null });
          const data = await seoApiService.getPersonalizationData();
          set({ personalizationData: data, isLoading: false });
        } catch (error: any) {
          set({ 
            error: `Failed to load personalization data: ${error.message}`, 
            isLoading: false 
          });
        }
      },

      executeCopilotAction: async (action: string, params: any) => {
        try {
          set({ isGenerating: true, error: null });
          
          const response = await seoApiService.executeCopilotAction(action, params);
          
          if (response.success) {
            // Update analysis data if it's an analysis action
            if (action.includes('analyze') && response.data) {
              set({ analysisData: response.data });
            }
            
            set({ isGenerating: false });
            return response;
          } else {
            set({ 
              error: response.message, 
              isGenerating: false 
            });
            return response;
          }
        } catch (error: any) {
          set({ 
            error: `Failed to execute ${action}: ${error.message}`, 
            isGenerating: false 
          });
          throw error;
        }
      },

      // Chart and visualization methods
      updateChart: (chartType: ChartType, timeRange?: TimeRange, metrics?: string[]) => {
        const currentLayout = get().dashboardLayout;
        const updatedConfigs = currentLayout.chartConfigs.map(config => {
          if (config.chartKey === chartType) {
            return {
              ...config,
              timeRange: timeRange || config.timeRange,
              metrics: metrics || config.metrics
            };
          }
          return config;
        });

        set({
          dashboardLayout: {
            ...currentLayout,
            chartConfigs: updatedConfigs
          }
        });
      },

      // Utility methods
      getHealthScoreColor: (score: number): string => {
        if (score >= 90) return '#4CAF50'; // Green
        if (score >= 70) return '#FF9800'; // Orange
        return '#F44336'; // Red
      },

      getSeverityColor: (severity: string): string => {
        switch (severity) {
          case 'critical': return '#F44336';
          case 'high': return '#FF9800';
          case 'medium': return '#FFC107';
          case 'low': return '#4CAF50';
          default: return '#9E9E9E';
        }
      },

      getEffortColor: (effort: string): string => {
        switch (effort) {
          case 'easy': return '#4CAF50';
          case 'medium': return '#FF9800';
          case 'hard': return '#F44336';
          default: return '#9E9E9E';
        }
      },

      // Reset methods
      resetAnalysis: () => {
        set({ 
          analysisData: null, 
          suggestions: defaultSuggestions,
          error: null 
        });
      },

      resetAll: () => {
        set({
          isLoading: false,
          isAnalyzing: false,
          isGenerating: false,
          analysisData: null,
          personalizationData: null,
          activeChart: null,
          dashboardLayout: defaultDashboardLayout,
          suggestions: defaultSuggestions,
          error: null,
          lastError: null
        });
      }
    }),
    {
      name: 'seo-copilot-store',
      enabled: process.env.NODE_ENV === 'development'
    }
  )
);

// Export store hooks for specific use cases
export const useSEOCopilotAnalysis = () => useSEOCopilotStore(state => ({
  analysisData: state.analysisData,
  isAnalyzing: state.isAnalyzing,
  error: state.error,
  executeCopilotAction: state.executeCopilotAction
}));

export const useSEOCopilotSuggestions = () => useSEOCopilotStore(state => (
  state.suggestions
));

export const useSEOCopilotDashboard = () => useSEOCopilotStore(state => ({
  dashboardLayout: state.dashboardLayout,
  setDashboardLayout: state.setDashboardLayout,
  updateChart: state.updateChart
}));

export default useSEOCopilotStore;
