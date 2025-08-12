import React from 'react';
import {
  Box,
  Button,
  Tooltip as MuiTooltip
} from '@mui/material';
import {
  AutoAwesome as AutoAwesomeIcon,
  Save as SaveIcon
} from '@mui/icons-material';
import { ActionButtonsProps, ActionButtonsBusinessLogicProps } from '../types/contentStrategy.types';

// Business Logic Hook
export const useActionButtonsBusinessLogic = ({
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
}: ActionButtonsBusinessLogicProps) => {
  
  const handleCreateStrategy = async () => {
    try {
      setAIGenerating(true);
      setError(null);
      
      console.log('Starting strategy creation...');
      console.log('Current formData:', formData);
      console.log('FormData ID:', formData.id);

      // If we have a saved strategy, use its ID
      if (formData.id) {
        console.log('Using existing strategy ID:', formData.id);
        await generateAIRecommendations(formData.id);
      } else {
        console.log('No strategy ID found, creating new strategy...');
        // If no strategy is saved yet, save it first, then generate AI insights
        const isValid = validateAllFields();
        console.log('Form validation result:', isValid);
      
        if (isValid) {
          const completionStats = getCompletionStats();
          const strategyData = {
            ...formData,
            completion_percentage: completionStats.completion_percentage,
            user_id: 1, // This would come from auth context
            name: formData.name || 'Enhanced Content Strategy',
            industry: formData.industry || 'General'
          };

          console.log('Attempting to create strategy with data:', strategyData);
          
          // Use SSE streaming endpoint for strategy generation with educational content
          await generateStrategyWithPolling(strategyData);
        } else {
          setError('Please fill in all required fields before generating AI insights.');
          console.error('Form validation failed. Cannot generate AI insights.');
        }
      }
    } catch (err: any) {
      setError(`Error generating AI recommendations: ${err.message || 'Unknown error'}`);
      console.error('Error in handleCreateStrategy:', err);
    } finally {
      setAIGenerating(false);
    }
  };

  const generateStrategyWithPolling = async (strategyData: any) => {
    try {
      console.log('🚀 Starting polling-based strategy generation...');
      
      // Initialize progress and educational content
      setGenerationProgress(0);
      setEducationalContent({
        title: '🤖 AI-Powered Strategy Generation',
        description: 'Initializing AI analysis and preparing educational content...',
        details: [
          '🔧 Setting up AI services',
          '📊 Loading user context',
          '🎯 Preparing strategy framework',
          '📚 Generating educational content'
        ],
        insight: 'We\'re getting everything ready for your personalized AI strategy generation.',
        estimated_time: '2-3 minutes total'
      });
      
      // Show educational modal
      setShowEducationalModal(true);

      // Start polling-based strategy generation directly (no basic strategy creation)
      const generationResult = await contentPlanningApi.startStrategyGenerationPolling(1, 'Enhanced Content Strategy');
      console.log('Strategy generation started:', generationResult);
      
      if (generationResult && generationResult.task_id) {
        const taskId = generationResult.task_id;
        console.log('Task ID received:', taskId);
        
        // Start polling for status updates
        contentPlanningApi.pollStrategyGeneration(
          taskId,
          // onProgress callback
          (status: any) => {
            console.log('📊 Progress update:', status);
            
            // Update progress
            if (status.progress !== undefined) {
              setGenerationProgress(status.progress);
            }
            
            // Update educational content
            if (status.educational_content) {
              console.log('📚 Updating educational content:', status.educational_content);
              setEducationalContent(status.educational_content);
            }
            
            // Update message
            if (status.message) {
              console.log('📝 Status message:', status.message);
            }
          },
          // onComplete callback
          (strategy: any) => {
            console.log('✅ Strategy generation completed successfully!');
            setCurrentStrategy(strategy);
            setShowEducationalModal(false);
            setError('Strategy created successfully! Check the Strategic Intelligence tab for detailed insights.');
          },
          // onError callback
          (error: string) => {
            console.error('❌ Strategy generation failed:', error);
            setError(`Strategy generation failed: ${error}`);
            setShowEducationalModal(false);
          },
          5000, // 5 second polling interval for faster updates
          72 // 6 minutes max (72 * 5 seconds)
        );
        
      } else {
        setError('Failed to start strategy generation. No task ID received.');
        setShowEducationalModal(false);
      }
    } catch (error: any) {
      console.error('Error in polling-based strategy generation:', error);
      setError(`Error in strategy generation: ${error.message || 'Unknown error'}`);
      setShowEducationalModal(false);
    }
  };

  const handleSaveStrategy = async () => {
    try {
      setSaving(true);
      setError(null);
      
      const completionStats = getCompletionStats();
      const strategyData = {
        ...formData,
        completion_percentage: completionStats.completion_percentage,
        user_id: 1,
        name: formData.name || 'Enhanced Content Strategy',
        industry: formData.industry || 'General'
      };
      
      const newStrategy = await createEnhancedStrategy(strategyData);
      setCurrentStrategy(newStrategy);
      setError('Strategy saved successfully!');
    } catch (err: any) {
      setError(`Error saving strategy: ${err.message || 'Unknown error'}`);
    } finally {
      setSaving(false);
    }
  };

  return {
    handleCreateStrategy,
    handleSaveStrategy
  };
};

// UI Component
const ActionButtons: React.FC<ActionButtonsProps> = ({
  aiGenerating,
  saving,
  reviewProgressPercentage,
  onCreateStrategy,
  onSaveStrategy
}) => {
  return (
    <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
      <MuiTooltip 
        title={reviewProgressPercentage < 20 ? `Complete at least 20% of the form (currently ${Math.round(reviewProgressPercentage)}%)` : 'Create a comprehensive content strategy with AI insights'}
        placement="top"
      >
        <span>
          <Button
            variant="outlined"
            startIcon={<AutoAwesomeIcon />}
            onClick={onCreateStrategy}
            disabled={aiGenerating || reviewProgressPercentage < 20}
          >
            {aiGenerating ? 'Creating...' : 'Create Strategy'}
          </Button>
        </span>
      </MuiTooltip>
      
      <Button
        variant="contained"
        startIcon={<SaveIcon />}
        onClick={onSaveStrategy}
        disabled={saving || reviewProgressPercentage < 30}
      >
        {saving ? 'Saving...' : 'Save Strategy'}
      </Button>
    </Box>
  );
};

export default ActionButtons; 