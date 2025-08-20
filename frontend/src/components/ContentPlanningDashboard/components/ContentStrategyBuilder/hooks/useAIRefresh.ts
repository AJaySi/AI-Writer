import { useState } from 'react';
import { contentPlanningApi } from '../../../../../services/contentPlanningApi';
import { useStrategyBuilderStore } from '../../../../../stores/strategyBuilderStore';

interface UseAIRefreshProps {
  setTransparencyModalOpen: (open: boolean) => void;
  setIsGenerating: (generating: boolean) => void;
  setStoreGenerationProgress: (progress: number) => void;
  setCurrentPhase: (phase: string) => void;
  clearTransparencyMessages: () => void;
  addTransparencyMessage: (message: string) => void;
  setAIGenerating: (generating: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAIRefresh = ({
  setTransparencyModalOpen,
  setIsGenerating,
  setStoreGenerationProgress,
  setCurrentPhase,
  clearTransparencyMessages,
  addTransparencyMessage,
  setAIGenerating,
  setError
}: UseAIRefreshProps) => {
  const [refreshMessage, setRefreshMessage] = useState<string | null>(null);
  const [refreshProgress, setRefreshProgress] = useState<number>(0);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [refreshError, setRefreshError] = useState<string | null>(null);

  const handleAIRefresh = async () => {
    try {
      // 🚀 POLLING-BASED AI REFRESH (No SSE)
      // We switched from SSE to polling for better reliability
      // This approach uses direct HTTP calls with visual feedback
      
      // Open transparency modal and initialize transparency state
      setTransparencyModalOpen(true);
      setIsGenerating(true);
      setStoreGenerationProgress(0);
      setCurrentPhase('autofill_initialization');
      clearTransparencyMessages();
      addTransparencyMessage('Starting strategy inputs generation process...');
      
      setAIGenerating(true);
      setIsRefreshing(true);
      setRefreshError(null);
      setRefreshMessage('Initializing AI refresh…');
      setRefreshProgress(5);

      // Start transparency message polling for visual feedback
      const transparencyMessages = [
        { type: 'autofill_initialization', message: 'Starting strategy inputs generation process...', progress: 5 },
        { type: 'autofill_data_collection', message: 'Collecting and analyzing data sources...', progress: 15 },
        { type: 'autofill_data_quality', message: 'Assessing data quality and completeness...', progress: 25 },
        { type: 'autofill_context_analysis', message: 'Analyzing business context and strategic framework...', progress: 35 },
        { type: 'autofill_strategy_generation', message: 'Generating strategic insights and recommendations...', progress: 45 },
        { type: 'autofill_field_generation', message: 'Generating individual strategy input fields...', progress: 55 },
        { type: 'autofill_quality_validation', message: 'Validating generated strategy inputs...', progress: 65 },
        { type: 'autofill_alignment_check', message: 'Checking strategy alignment and consistency...', progress: 75 },
        { type: 'autofill_final_review', message: 'Performing final review and optimization...', progress: 85 },
        { type: 'autofill_complete', message: 'Strategy inputs generation completed successfully...', progress: 95 }
      ];
      
      let messageIndex = 0;
      const transparencyInterval = setInterval(() => {
        if (messageIndex < transparencyMessages.length) {
          const message = transparencyMessages[messageIndex];
          setCurrentPhase(message.type);
          addTransparencyMessage(message.message);
          setStoreGenerationProgress(message.progress);
          setRefreshProgress(message.progress);
          messageIndex++;
        } else {
          clearInterval(transparencyInterval);
        }
      }, 2000); // Send a message every 2 seconds for better UX

      // Call the non-streaming refresh endpoint (Polling-based approach)
      const response = await contentPlanningApi.refreshAutofill(1, true, true);

      // Clear the transparency interval since we got the response
      clearInterval(transparencyInterval);

      // Process the response
      if (response) {
        const payload = response;
        const fields = payload.fields || {};
        const sources = payload.sources || {};
        const inputDataPoints = payload.input_data_points || {};
        const meta = payload.meta || {};
        
        console.log('🎯 AI Refresh - Generated fields:', Object.keys(fields).length);
        
        // 🚨 CRITICAL: Check if AI generation failed
        if (meta.error || !meta.ai_used) {
          console.error('❌ AI generation failed:', meta.error || 'AI not used');
          setError(`AI generation failed: ${meta.error || 'AI was not used for generation. Please try again.'}`);
          setTransparencyModalOpen(false);
          setAIGenerating(false);
          setIsRefreshing(false);
          setIsGenerating(false);
          setRefreshError('AI generation failed. Please try again.');
          setRefreshMessage('Refresh failed.');
          return;
        }
        
        // Check if we have any fields generated (more lenient validation)
        const fieldsCount = Object.keys(fields).length;
        if (fieldsCount === 0) {
          console.error('❌ No fields generated');
          setError('No fields were generated. Please try again.');
          setTransparencyModalOpen(false);
          setAIGenerating(false);
          setIsRefreshing(false);
          setIsGenerating(false);
          setRefreshError('No fields generated. Please try again.');
          setRefreshMessage('Refresh failed.');
          return;
        }
        
        console.log(`✅ AI generation successful - ${fieldsCount} fields generated`);
        
        // 🚨 CRITICAL: Validate data source (only check for explicit failure states)
        if (meta.data_source === 'ai_generation_failed' || meta.data_source === 'ai_generation_error') {
          console.error('❌ AI generation failed:', meta.data_source);
          setError(`AI generation failed: ${meta.error || 'Invalid data source. Please try again.'}`);
          setTransparencyModalOpen(false);
          setAIGenerating(false);
          setIsRefreshing(false);
          setIsGenerating(false);
          setRefreshError('AI generation failed. Please try again.');
          setRefreshMessage('Refresh failed.');
          return;
        }
        
        const fieldValues: Record<string, any> = {};
        const confidenceScores: Record<string, number> = {};
        
        Object.keys(fields).forEach((fieldId) => {
          const fieldData = fields[fieldId];
          
          if (fieldData && typeof fieldData === 'object' && 'value' in fieldData) {
            fieldValues[fieldId] = fieldData.value;
            
            // Extract confidence score if available
            if (fieldData.confidence) {
              confidenceScores[fieldId] = fieldData.confidence;
            }
          } else {
            console.warn(`⚠️ Field ${fieldId} has invalid structure`);
          }
        });
        
        // Update the store with the new data - COMPLETELY REPLACE old data
        useStrategyBuilderStore.setState((state) => {
          const newState = {
            autoPopulatedFields: fieldValues, // 🚨 CRITICAL: Replace, don't merge
            dataSources: sources, // 🚨 CRITICAL: Replace, don't merge
            inputDataPoints: inputDataPoints, // 🚨 CRITICAL: Replace, don't merge
            confidenceScores: confidenceScores, // 🚨 CRITICAL: Replace, don't merge
            formData: { ...state.formData, ...fieldValues } // Keep existing manual edits
          };
          console.log('✅ Store updated with fresh AI data:', Object.keys(fieldValues).length, 'fields');
          return newState;
        });
        
        // Add final completion message
        addTransparencyMessage(`✅ AI generation completed successfully! Generated ${Object.keys(fieldValues).length} real AI values.`);
        setStoreGenerationProgress(100);
        setRefreshProgress(100);
        setCurrentPhase('Complete');
        setRefreshMessage(`AI refresh completed! Generated ${Object.keys(fieldValues).length} fields.`);
        
        // Ensure the educational modal shows the completion state
        setTimeout(() => {
          setStoreGenerationProgress(100);
          setRefreshProgress(100);
        }, 100);
        
        // Update session storage with fresh autofill timestamp
        sessionStorage.setItem('lastAutofillTime', new Date().toISOString());
        
        // Reset refresh state
        setAIGenerating(false);
        setIsRefreshing(false);
        setIsGenerating(false);
        console.log('✅ AI refresh completed:', Object.keys(fieldValues).length, 'fields generated');
      } else {
        throw new Error('Invalid response from AI refresh endpoint');
      }
    } catch (e) {
      console.error('AI refresh error', e);
      setAIGenerating(false);
      setIsRefreshing(false);
      setIsGenerating(false);
      setRefreshError('AI refresh failed. Please try again.');
      setRefreshMessage('Refresh failed.');
      setError(`AI refresh failed: ${e instanceof Error ? e.message : 'Unknown error'}`);
    }
  };

  return {
    refreshMessage,
    setRefreshMessage,
    refreshProgress,
    setRefreshProgress,
    isRefreshing,
    setIsRefreshing,
    refreshError,
    setRefreshError,
    handleAIRefresh
  };
};
