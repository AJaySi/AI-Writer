// Educational Content Types
export interface EducationalContent {
  title?: string;
  description?: string;
  details?: string[];
  insight?: string;
  estimated_time?: string;
  achievement?: string;
  next_step?: string;
  ai_prompt_preview?: string;
  summary?: Record<string, string>;
}

// Educational Modal Props
export interface EducationalModalProps {
  open: boolean;
  onClose: () => void;
  educationalContent: EducationalContent | null;
  generationProgress: number;
}

// Category Detail View Types
export interface CategoryDetailViewProps {
  activeCategory: string | null;
  formData: Record<string, any>;
  formErrors: Record<string, any>;
  autoPopulatedFields: Record<string, any>;
  dataSources: Record<string, any>;
  inputDataPoints: Record<string, any>;
  personalizationData: Record<string, any>;
  completionStats: any;
  reviewedCategories: Set<string>;
  isMarkingReviewed: boolean;
  showEducationalInfo: string | null;
  STRATEGIC_INPUT_FIELDS: any[];
  onUpdateFormField: (fieldId: string, value: any) => void;
  onValidateFormField: (fieldId: string) => boolean;
  onShowTooltip: (fieldId: string) => void;
  onViewDataSource: (fieldId?: string) => void;
  onConfirmCategoryReview: () => void;
  onSetActiveCategory: (category: string | null) => void;
  onSetShowEducationalInfo: (categoryId: string | null) => void;
  getCategoryIcon: (category: string) => React.ReactNode;
  getCategoryColor: (category: string) => string;
  getEducationalContent: (categoryId: string) => any;
}

// Educational Info Dialog Types
export interface EducationalInfoDialogProps {
  open: boolean;
  onClose: () => void;
  categoryId: string | null;
  getEducationalContent: (categoryId: string) => any;
}

// Action Buttons Types
export interface ActionButtonsProps {
  aiGenerating: boolean;
  saving: boolean;
  reviewProgressPercentage: number;
  onCreateStrategy: () => void;
  onSaveStrategy: () => void;
}

// Action Buttons Business Logic Types
export interface ActionButtonsBusinessLogicProps {
  formData: Record<string, any>;
  error: string | null;
  currentStrategy: any;
  setAIGenerating: (generating: boolean) => void;
  setError: (error: string | null) => void;
  setCurrentStrategy: (strategy: any) => void;
  setSaving: (saving: boolean) => void;
  setGenerationProgress: (progress: number) => void;
  setEducationalContent: (content: any) => void;
  setShowEducationalModal: (show: boolean) => void;
  validateAllFields: () => boolean;
  getCompletionStats: () => any;
  generateAIRecommendations: (strategyId: string) => Promise<void>;
  createEnhancedStrategy: (strategyData: any) => Promise<any>;
  contentPlanningApi: any;
}

// Strategy Generation Types
export interface StrategyGenerationStatus {
  progress?: number;
  message?: string;
  educational_content?: EducationalContent;
  error?: string;
}

export interface StrategyGenerationCallbacks {
  onProgress: (status: StrategyGenerationStatus) => void;
  onComplete: (strategy: any) => void;
  onError: (error: string) => void;
}

// Category Navigation Types
export interface CategoryNavigationProps {
  activeCategory: string | null;
  onCategorySelect: (category: string | null) => void;
  completionStats: any;
  reviewedCategories: Set<string>;
}

// Strategy Display Types
export interface StrategyDisplayProps {
  currentStrategy: any;
  error: string | null;
  categoryCompletionMessage: string | null;
  onViewStrategicIntelligence: () => void;
}

// Error Alert Types
export interface ErrorAlertProps {
  error: string | null;
  onRetry: () => void;
  onShowDataSourceTransparency: () => void;
}

// Success Alert Types
export interface SuccessAlertProps {
  currentStrategy: any;
  categoryCompletionMessage: string | null;
} 