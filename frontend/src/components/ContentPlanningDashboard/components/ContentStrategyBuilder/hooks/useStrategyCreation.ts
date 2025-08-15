import { useActionButtonsBusinessLogic } from '../components/ActionButtons';

interface UseStrategyCreationProps {
  formData: any;
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
  createEnhancedStrategy: (data: any) => Promise<any>;
  contentPlanningApi: any;
}

export const useStrategyCreation = ({
  formData,
  error,
  currentStrategy,
  setAIGenerating,
  setError,
  setCurrentStrategy,
  setSaving,
  setGenerationProgress,
  setEducationalContent,
  setShowEducationalModal,
  validateAllFields,
  getCompletionStats,
  generateAIRecommendations,
  createEnhancedStrategy,
  contentPlanningApi
}: UseStrategyCreationProps) => {
  // Use ActionButtons business logic hook
  const { handleCreateStrategy: originalHandleCreateStrategy, handleSaveStrategy } = useActionButtonsBusinessLogic({
    formData,
    error,
    currentStrategy,
    setAIGenerating,
    setError,
    setCurrentStrategy,
    setSaving,
    setGenerationProgress,
    setEducationalContent,
    setShowEducationalModal,
    validateAllFields,
    getCompletionStats,
    generateAIRecommendations,
    createEnhancedStrategy,
    contentPlanningApi
  });

  return {
    originalHandleCreateStrategy: () => originalHandleCreateStrategy(),
    handleSaveStrategy: () => handleSaveStrategy()
  };
};
