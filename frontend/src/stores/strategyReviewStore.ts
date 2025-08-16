import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export type ReviewStatus = 'not_reviewed' | 'in_review' | 'reviewed';

export interface StrategyComponent {
  id: string;
  title: string;
  subtitle: string;
  status: ReviewStatus;
  reviewedAt?: Date;
  reviewedBy?: string;
  notes?: string;
}

export interface ReviewState {
  // Review state
  components: StrategyComponent[];
  isReviewing: boolean;
  reviewProgress: number;
  
  // Actions
  initializeComponents: (components: Omit<StrategyComponent, 'status' | 'reviewedAt' | 'reviewedBy' | 'notes'>[]) => void;
  startReview: (componentId: string) => void;
  completeReview: (componentId: string, notes?: string) => void;
  resetReview: (componentId: string) => void;
  resetAllReviews: () => void;
  updateReviewProgress: () => void;
  getReviewProgress: () => number;
  isAllReviewed: () => boolean;
  getUnreviewedComponents: () => StrategyComponent[];
  getReviewedComponents: () => StrategyComponent[];
}

const STRATEGY_COMPONENTS = [
  {
    id: 'strategic_insights',
    title: 'Strategic Insights',
    subtitle: 'AI-powered market analysis'
  },
  {
    id: 'competitive_analysis',
    title: 'Competitive Analysis',
    subtitle: 'Market positioning insights'
  },
  {
    id: 'performance_predictions',
    title: 'Performance Predictions',
    subtitle: 'ROI and success metrics'
  },
  {
    id: 'implementation_roadmap',
    title: 'Implementation Roadmap',
    subtitle: 'Project timeline and phases'
  },
  {
    id: 'risk_assessment',
    title: 'Risk Assessment',
    subtitle: 'Risk analysis and mitigation'
  }
];

export const useStrategyReviewStore = create<ReviewState>()(
  devtools(
    (set, get) => ({
      // Initial state
      components: [],
      isReviewing: false,
      reviewProgress: 0,

      // Initialize components with default review status
      initializeComponents: (components) => {
        const initializedComponents = components.map(component => ({
          ...component,
          status: 'not_reviewed' as ReviewStatus
        }));
        
        set({ components: initializedComponents });
        get().updateReviewProgress();
      },

      // Start reviewing a component
      startReview: (componentId: string) => {
        set(state => ({
          isReviewing: true,
          components: state.components.map(comp =>
            comp.id === componentId
              ? { ...comp, status: 'in_review' as ReviewStatus }
              : comp
          )
        }));
      },

      // Complete review for a component
      completeReview: (componentId: string, notes?: string) => {
        set(state => ({
          isReviewing: false,
          components: state.components.map(comp =>
            comp.id === componentId
              ? {
                  ...comp,
                  status: 'reviewed' as ReviewStatus,
                  reviewedAt: new Date(),
                  reviewedBy: 'current_user', // In real app, get from auth
                  notes
                }
              : comp
          )
        }));
        
        get().updateReviewProgress();
      },

      // Reset review for a component
      resetReview: (componentId: string) => {
        set(state => ({
          components: state.components.map(comp =>
            comp.id === componentId
              ? {
                  ...comp,
                  status: 'not_reviewed' as ReviewStatus,
                  reviewedAt: undefined,
                  reviewedBy: undefined,
                  notes: undefined
                }
              : comp
          )
        }));
        
        get().updateReviewProgress();
      },

      // Reset all reviews
      resetAllReviews: () => {
        set(state => ({
          components: state.components.map(comp => ({
            ...comp,
            status: 'not_reviewed' as ReviewStatus,
            reviewedAt: undefined,
            reviewedBy: undefined,
            notes: undefined
          }))
        }));
        
        get().updateReviewProgress();
      },

      // Update review progress
      updateReviewProgress: () => {
        const { components } = get();
        const reviewedCount = components.filter(comp => comp.status === 'reviewed').length;
        const totalCount = components.length;
        const progress = totalCount > 0 ? (reviewedCount / totalCount) * 100 : 0;
        
        set({ reviewProgress: progress });
      },

      // Get review progress percentage
      getReviewProgress: () => {
        return get().reviewProgress;
      },

      // Check if all components are reviewed
      isAllReviewed: () => {
        const { components } = get();
        return components.every(comp => comp.status === 'reviewed');
      },

      // Get unreviewed components
      getUnreviewedComponents: () => {
        const { components } = get();
        return components.filter(comp => comp.status !== 'reviewed');
      },

      // Get reviewed components
      getReviewedComponents: () => {
        const { components } = get();
        return components.filter(comp => comp.status === 'reviewed');
      }
    }),
    {
      name: 'strategy-review-store',
      enabled: process.env.NODE_ENV === 'development'
    }
  )
);

// Initialize components when store is created
useStrategyReviewStore.getState().initializeComponents(STRATEGY_COMPONENTS);
