import { useState } from 'react';
import { contentPlanningApi } from '../../../../../services/contentPlanningApi';
import { StrategyData } from '../types/strategy.types';

export const useStrategyActions = () => {
  const [strategyConfirmed, setStrategyConfirmed] = useState(false);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);

  const handleConfirmStrategy = () => {
    setShowConfirmDialog(true);
  };

  const confirmStrategy = async (strategyData: StrategyData | null) => {
    try {
      setStrategyConfirmed(true);
      setShowConfirmDialog(false);
      
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
      
      console.log('Strategy confirmed! Ready to generate content calendar.');
    } catch (error) {
      console.error('Error confirming strategy:', error);
      setStrategyConfirmed(false);
    }
  };

  const handleGenerateContentCalendar = async (strategyData: StrategyData | null) => {
    try {
      const userId = strategyData?.strategy_metadata?.user_id || strategyData?.metadata?.user_id;
      if (!userId) {
        console.error('No strategy data available for calendar generation');
        return;
      }
      
      // Generate content calendar based on confirmed strategy
      const calendarRequest = {
        user_id: userId,
        strategy_id: userId, // Using user_id as strategy_id for now
        calendar_type: 'comprehensive',
        industry: strategyData.base_strategy?.industry || 'technology',
        business_size: 'medium', // TODO: Get from strategy data
        force_refresh: false
      };
      
      console.log('Generating content calendar with request:', calendarRequest);
      
      // Call the calendar generation API
      const calendarResponse = await contentPlanningApi.generateCalendar(calendarRequest);
      
      console.log('Content calendar generated successfully:', calendarResponse);
      
      // TODO: Navigate to calendar tab or show success message
      // You could also store the calendar data in a global state
      
    } catch (error) {
      console.error('Error generating content calendar:', error);
      // Show error message to user
      throw new Error('Failed to generate content calendar. Please try again.');
    }
  };

  return {
    strategyConfirmed,
    showConfirmDialog,
    setShowConfirmDialog,
    handleConfirmStrategy,
    confirmStrategy,
    handleGenerateContentCalendar
  };
}; 