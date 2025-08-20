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
import { useContentPlanningStore } from '../../../../../stores/contentPlanningStore';

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
  
  // Get the content planning store to cache the latest generated strategy
  const { setLatestGeneratedStrategy } = useContentPlanningStore();
  
  const handleCreateStrategy = async () => {
    try {
      setAIGenerating(true);
      setError(null);
      
      // Clear any previous cached strategy when starting new generation
      setLatestGeneratedStrategy(null);
      console.log('🧹 Cleared previous cached strategy for new generation');
      
      console.log('Starting strategy creation...');
      console.log('Current formData:', formData);
      console.log('FormData ID:', formData.id);

      // Always use the polling-based strategy generation for consistency
      console.log('Using polling-based strategy generation...');
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
        
        // Use polling-based strategy generation with educational content
        await generateStrategyWithPolling(strategyData);
      } else {
        setError('Please fill in all required fields before generating AI insights.');
        console.error('Form validation failed. Cannot generate AI insights.');
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

      // Start polling-based strategy generation with actual strategy data
      const generationResult = await contentPlanningApi.startStrategyGenerationPolling(
        strategyData.user_id || 1, 
        strategyData.name || 'Enhanced Content Strategy'
      );
      console.log('Strategy generation started:', generationResult);
      console.log('Generation result structure:', generationResult);
      console.log('Generation result.data:', generationResult?.data);
      console.log('Generation result.data.task_id:', generationResult?.data?.task_id);
      
      // Check for task_id in the correct location based on backend response structure
      const taskId = generationResult?.data?.task_id || generationResult?.task_id;
      console.log('Task ID extracted:', taskId);
      
      if (taskId) {
        console.log('Task ID received:', taskId);
        
        // Start polling for status updates
        console.log('🎯 Starting polling for task ID:', taskId);
        contentPlanningApi.pollStrategyGeneration(
          taskId,
          // onProgress callback
          (status: any) => {
            console.log('📊 Progress update:', status);
            console.log('📊 Status structure:', status);
            
            // Extract the actual task status from the response data
            const taskStatus = status?.data || status;
            console.log('📊 Task status:', taskStatus);
            
            // Update progress
            if (taskStatus.progress !== undefined) {
              console.log('📊 Setting progress:', taskStatus.progress);
              setGenerationProgress(taskStatus.progress);
              
              // Debug: Check if progress reached 100%
              if (taskStatus.progress >= 100) {
                console.log('🎯 Progress reached 100% - modal should show "Next" button');
              }
            }
            
            // Update educational content
            if (taskStatus.educational_content) {
              console.log('📚 Updating educational content:', taskStatus.educational_content);
              setEducationalContent(taskStatus.educational_content);
            }
            
            // Update message
            if (taskStatus.message) {
              console.log('📝 Status message:', taskStatus.message);
            }
            
            // Update phase if available
            if (taskStatus.step) {
              console.log('📊 Current step:', taskStatus.step);
            }
          },
          // onComplete callback
          (strategy: any) => {
            console.log('✅ Strategy generation completed successfully!');
            setCurrentStrategy(strategy);
            
            // Cache the latest generated strategy in the content planning store
            console.log('💾 Attempting to cache strategy:', {
              strategyId: strategy?.id || strategy?.strategy_id,
              strategyName: strategy?.name || strategy?.strategy_name,
              hasStrategicInsights: !!strategy?.strategic_insights,
              hasCompetitiveAnalysis: !!strategy?.competitive_analysis,
              hasPerformancePredictions: !!strategy?.performance_predictions,
              hasImplementationRoadmap: !!strategy?.implementation_roadmap,
              hasRiskAssessment: !!strategy?.risk_assessment
            });
            setLatestGeneratedStrategy(strategy);
            console.log('💾 Cached latest generated strategy in store');
            
            // Set progress to 100% when completion is detected
            setGenerationProgress(100);
            console.log('🎯 Setting progress to 100% in onComplete callback');
            // Don't close the modal automatically - let user click the button
            // setShowEducationalModal(false); // REMOVED - let user control modal closure
            console.log('🎯 Strategy generation complete - modal should stay open for user to click "Next" button');
          },
          // onError callback
          (error: string) => {
            console.error('❌ Strategy generation failed:', error);
            setError(`Strategy generation failed: ${error}`);
            setShowEducationalModal(false); // Only close on error
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
      
      // Update the cache with the saved strategy
      setLatestGeneratedStrategy(newStrategy);
      console.log('💾 Updated cache with saved strategy');
      
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