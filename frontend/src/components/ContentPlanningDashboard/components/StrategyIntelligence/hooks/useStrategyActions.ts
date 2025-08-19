import { useState } from 'react';
import { contentPlanningApi } from '../../../../../services/contentPlanningApi';
import { StrategyData } from '../types/strategy.types';
import { useStrategyReviewStore } from '../../../../../stores/strategyReviewStore';

export const useStrategyActions = () => {
  const [strategyConfirmed, setStrategyConfirmed] = useState(false);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [isActivating, setIsActivating] = useState(false);
  
  // Get the activateStrategy method from the review store
  const { activateStrategy } = useStrategyReviewStore();

  const handleConfirmStrategy = () => {
    setShowConfirmDialog(true);
  };

  const confirmStrategy = async (strategyData: StrategyData | null): Promise<void> => {
    if (isActivating) {
      throw new Error('Strategy activation already in progress');
    }

    setIsActivating(true);
    
    try {
      // Save confirmation status to backend
      const userId = strategyData?.strategy_metadata?.user_id || strategyData?.metadata?.user_id;
      if (userId) {
        try {
          // Update the strategy with confirmation status
          await contentPlanningApi.updateEnhancedStrategy(
            userId.toString(),
            { confirmed: true, confirmed_at: new Date().toISOString() }
          );
          console.log('Strategy confirmation saved to backend');
        } catch (updateError) {
          console.warn('Could not save confirmation to backend:', updateError);
          // Don't fail the confirmation if backend update fails
        }
      }
      
      // Set local state
      setStrategyConfirmed(true);
      setShowConfirmDialog(false);
      
      // Activate strategy in the review store
      activateStrategy();
      
      console.log('Strategy confirmed and activated! Ready to generate content calendar.');
    } catch (error) {
      console.error('Error confirming strategy:', error);
      setStrategyConfirmed(false);
      throw error; // Re-throw to let the calling component handle the error
    } finally {
      setIsActivating(false);
    }
  };

  const handleGenerateContentCalendar = async (strategyData: StrategyData | null) => {
    try {
      const userId = strategyData?.strategy_metadata?.user_id || strategyData?.metadata?.user_id;
      if (!userId) {
        console.error('No strategy data available for calendar generation');
        return;
      }
      
      console.log('🎯 Strategy Actions: Generating content calendar for strategy:', strategyData);
      
      // For now, we'll just log that the function was called
      // The actual navigation is handled by the ReviewProgressHeader component
      // which uses the NavigationOrchestrator to navigate to the calendar wizard
      
      console.log('🎯 Strategy Actions: Calendar generation request prepared');
      
      // TODO: In the future, this could be enhanced to:
      // 1. Call the calendar generation API directly
      // 2. Store the generated calendar data
      // 3. Navigate to the calendar view with the generated data
      
    } catch (error) {
      console.error('Error in handleGenerateContentCalendar:', error);
      throw new Error('Failed to prepare calendar generation. Please try again.');
    }
  };

  return {
    strategyConfirmed,
    showConfirmDialog,
    setShowConfirmDialog,
    isActivating,
    handleConfirmStrategy,
    confirmStrategy,
    handleGenerateContentCalendar
  };
}; 