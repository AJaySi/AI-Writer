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
      console.log('🎯 Opening transparency modal...');
      setTransparencyModalOpen(true);
      setIsGenerating(true);
      setStoreGenerationProgress(0);
      setCurrentPhase('autofill_initialization');
      clearTransparencyMessages();
      addTransparencyMessage('Starting strategy inputs generation process...');
      console.log('🎯 Modal state set, transparency initialized');
      
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
          console.log('🎯 Raw Polling Message:', {
            type: message.type,
            message: message.message,
            progress: message.progress,
            timestamp: new Date().toISOString()
          });
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
      console.log('🎯 Calling AI refresh endpoint (Polling-based)...');
      const response = await contentPlanningApi.refreshAutofill(1, true, true);
      console.log('🎯 Raw Polling Response:', {
        success: !!response,
        hasData: !!response?.fields,
        responseStructure: {
          hasFieldsProperty: !!response?.fields,
          hasSourcesProperty: !!response?.sources,
          hasMetaProperty: !!response?.meta
        },
        fieldsCount: Object.keys(response?.fields || {}).length,
        sourcesCount: Object.keys(response?.sources || {}).length,
        meta: response?.meta || {},
        timestamp: new Date().toISOString()
      });

      // Clear the transparency interval since we got the response
      clearInterval(transparencyInterval);

      // Process the response
      // The API method already returns the extracted data, not the full response
      if (response) {
        // Debug the actual response structure
        console.log('🎯 Raw response structure:', {
          responseType: typeof response,
          responseKeys: Object.keys(response),
          hasFieldsProperty: response?.hasOwnProperty('fields'),
          hasSourcesProperty: response?.hasOwnProperty('sources'),
          hasMetaProperty: response?.hasOwnProperty('meta')
        });
        
        // Debug the actual response data
        console.log('🎯 Raw response:', response);
        console.log('🎯 Raw response.fields:', response?.fields);
        console.log('🎯 Raw response.sources:', response?.sources);
        console.log('🎯 Raw response.meta:', response?.meta);
        
        // The API method already returns the extracted payload from ResponseBuilder
        // So response is already the payload with fields, sources, meta, etc.
        const payload = response;
        
        // Debug the payload structure
        console.log('🎯 Payload structure:', {
          payloadType: typeof payload,
          payloadKeys: Object.keys(payload),
          hasFieldsProperty: payload?.hasOwnProperty('fields'),
          hasSourcesProperty: payload?.hasOwnProperty('sources'),
          hasMetaProperty: payload?.hasOwnProperty('meta'),
          fieldsKeys: payload?.fields ? Object.keys(payload.fields) : 'no fields'
        });
        
        const fields = payload.fields || {};
        const sources = payload.sources || {};
        const inputDataPoints = payload.input_data_points || {};
        const meta = payload.meta || {};
        
        // Debug the extracted data
        console.log('🎯 Extracted fields:', fields);
        console.log('🎯 Extracted sources:', sources);
        console.log('🎯 Extracted inputDataPoints:', inputDataPoints);
        console.log('🎯 Extracted meta:', meta);
        console.log('🎯 Fields count:', Object.keys(fields).length);
        console.log('🎯 Sources count:', Object.keys(sources).length);
        console.log('🎯 InputDataPoints count:', Object.keys(inputDataPoints).length);
        
        console.log('🎯 AI Refresh Result - Payload:', payload);
        console.log('🎯 AI Refresh Result - Fields:', fields);
        console.log('🎯 AI Refresh Result - Meta:', meta);
        console.log('🎯 Fields structure check:', {
          fieldsType: typeof fields,
          fieldsKeys: Object.keys(fields),
          sampleField: fields[Object.keys(fields)[0]],
          hasValueProperty: fields[Object.keys(fields)[0]]?.hasOwnProperty('value')
        });
        
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
        
        console.log(`✅ AI generation successful - generated ${fieldsCount} fields, AI overrides: ${meta.ai_overrides_count || 0}`);
        
        // 🚨 CRITICAL: Validate data source (only check for explicit failure states)
        if (meta.data_source === 'ai_generation_failed' || meta.data_source === 'ai_generation_error') {
          console.error('❌ Invalid data source:', meta.data_source);
          setError(`AI generation failed: ${meta.error || 'Invalid data source. Please try again.'}`);
          setTransparencyModalOpen(false);
          setAIGenerating(false);
          setIsRefreshing(false);
          setIsGenerating(false);
          setRefreshError('AI generation failed. Please try again.');
          setRefreshMessage('Refresh failed.');
          return;
        }
        
        console.log('✅ AI generation successful - processing real AI data');
        
        const fieldValues: Record<string, any> = {};
        const confidenceScores: Record<string, number> = {};
        
        Object.keys(fields).forEach((fieldId) => {
          const fieldData = fields[fieldId];
          console.log(`🎯 Processing field ${fieldId}:`, fieldData);
          
          if (fieldData && typeof fieldData === 'object' && 'value' in fieldData) {
            fieldValues[fieldId] = fieldData.value;
            console.log(`✅ Field ${fieldId} value extracted:`, fieldData.value);
            
            // Extract confidence score if available
            if (fieldData.confidence) {
              confidenceScores[fieldId] = fieldData.confidence;
              console.log(`🎯 Field ${fieldId} confidence: ${fieldData.confidence}`);
            }
            
            // Extract personalization data if available
            if (fieldData.personalization_data) {
              console.log(`🎯 Field ${fieldId} personalization:`, fieldData.personalization_data);
            }
          } else {
            console.warn(`⚠️ Field ${fieldId} has invalid structure:`, fieldData);
          }
        });
        
        console.log('🎯 Processed field values:', Object.keys(fieldValues));
        console.log('🎯 Confidence scores:', confidenceScores);
        console.log('🎯 Field values details:', fieldValues);
        
        // Update the store with the new data
        useStrategyBuilderStore.setState((state) => {
          const newState = {
            autoPopulatedFields: { ...state.autoPopulatedFields, ...fieldValues },
            dataSources: { ...state.dataSources, ...sources },
            inputDataPoints: { ...state.inputDataPoints, ...inputDataPoints },
            confidenceScores: { ...state.confidenceScores, ...confidenceScores },
            formData: { ...state.formData, ...fieldValues }
          };
          console.log('🎯 Updated store state:', newState);
          console.log('🎯 Field values being added:', fieldValues);
          console.log('🎯 Confidence scores being added:', confidenceScores);
          console.log('🎯 Store autoPopulatedFields count:', Object.keys(newState.autoPopulatedFields).length);
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
        
        // Reset refresh state
        setAIGenerating(false);
        setIsRefreshing(false);
        setIsGenerating(false);
        console.log('🎯 Polling-based AI refresh completed successfully!', {
          fieldsGenerated: Object.keys(fieldValues).length,
          confidenceScoresCount: Object.keys(confidenceScores).length,
          dataSourcesCount: Object.keys(sources).length,
          approach: 'Polling (No SSE)',
          timestamp: new Date().toISOString()
        });
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
