  import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Chip,
  IconButton,
  Tooltip as MuiTooltip,
  Card,
  CardContent,
  Grid,
  Divider,
  CircularProgress,
  Badge,
  Collapse,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Business as BusinessIcon,
  People as PeopleIcon,
  TrendingUp as TrendingUpIcon,
  ContentPaste as ContentIcon,
  Analytics as AnalyticsIcon,
  Help as HelpIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  AutoAwesome as AutoAwesomeIcon,
  Refresh as RefreshIcon,
  Save as SaveIcon,
  ArrowForward as ArrowForwardIcon,
  ArrowBack as ArrowBackIcon,
  Assessment as AssessmentIcon,
  ExpandMore as ExpandMoreIcon,
  Info as InfoIcon,
  Visibility as VisibilityIcon,
  School as SchoolIcon,
  Lightbulb as LightbulbIcon,
  Psychology as PsychologyIcon,
  Timeline as TimelineIcon,
  FiberManualRecord as FiberManualRecordIcon,
  Schedule as ScheduleIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useEnhancedStrategyStore, STRATEGIC_INPUT_FIELDS } from '../../../stores/enhancedStrategyStore';
import StrategicInputField from './ContentStrategyBuilder/StrategicInputField';
import EnhancedTooltip from './ContentStrategyBuilder/EnhancedTooltip';
import AIRecommendationsPanel from './AIRecommendationsPanel';
import DataSourceTransparency from './DataSourceTransparency';
import StrategyAutofillTransparencyModal from './StrategyAutofillTransparencyModal';

// Import extracted hooks
import { useCategoryReview } from './ContentStrategyBuilder/hooks/useCategoryReview';
import { useProgressTracking } from './ContentStrategyBuilder/hooks/useProgressTracking';
import { useAutoPopulation } from './ContentStrategyBuilder/hooks/useAutoPopulation';
import { useActionButtonsBusinessLogic } from './ContentStrategyBuilder/components/ActionButtons';

// Import extracted utilities
import { getCategoryIcon, getCategoryColor, getCategoryName, getCategoryStatus } from './ContentStrategyBuilder/utils/categoryHelpers';
import { getEducationalContent } from './ContentStrategyBuilder/utils/educationalContent';

// Import extracted components
import CategoryList from './ContentStrategyBuilder/components/CategoryList';
import ProgressTracker from './ContentStrategyBuilder/components/ProgressTracker';
import HeaderSection from './ContentStrategyBuilder/components/HeaderSection';
import EducationalModal from './ContentStrategyBuilder/components/EducationalModal';
import ActionButtons from './ContentStrategyBuilder/components/ActionButtons';
import StrategyDisplay from './ContentStrategyBuilder/components/StrategyDisplay';
import ErrorAlert from './ContentStrategyBuilder/components/ErrorAlert';
import { contentPlanningApi } from '../../../services/contentPlanningApi';
import CategoryDetailView from './ContentStrategyBuilder/components/CategoryDetailView';

const ContentStrategyBuilder: React.FC = () => {
  const {
    formData,
    formErrors,
    autoPopulatedFields,
    dataSources,
    inputDataPoints, // Add inputDataPoints from store
    loading,
    error,
    saving,
    aiGenerating,
    currentStep,
    completedSteps,
    disclosureSteps,
    currentStrategy,
    updateFormField,
    // Transparency state
    transparencyModalOpen,
    generationProgress: storeGenerationProgress,
    currentPhase,
    educationalContent: storeEducationalContent,
    transparencyMessages,
    isGenerating,
    setTransparencyModalOpen,
    setGenerationProgress: setStoreGenerationProgress,
    setCurrentPhase,
    setEducationalContent: setStoreEducationalContent,
    addTransparencyMessage,
    clearTransparencyMessages,
    setIsGenerating,
    validateFormField,
    validateAllFields,
    completeStep,
    getNextStep,
    getPreviousStep,
    setCurrentStep,
    canProceedToStep,
    resetForm,
    autoPopulateFromOnboarding,
    generateAIRecommendations,
    createEnhancedStrategy,
    calculateCompletionPercentage,
    getCompletionStats,
    setError,
    setCurrentStrategy,
    setAIGenerating,
    setSaving,
    personalizationData
  } = useEnhancedStrategyStore();

  const [showTooltip, setShowTooltip] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [showEducationalInfo, setShowEducationalInfo] = useState<string | null>(null);
  const [showAIRecommendations, setShowAIRecommendations] = useState(false);
  const [showDataSourceTransparency, setShowDataSourceTransparency] = useState(false);
  const [refreshMessage, setRefreshMessage] = useState<string | null>(null);
  const [refreshProgress, setRefreshProgress] = useState<number>(0);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [refreshError, setRefreshError] = useState<string | null>(null);
  const [showEducationalModal, setShowEducationalModal] = useState(false);
  const [localEducationalContent, setLocalEducationalContent] = useState<any>(null);
  const [localGenerationProgress, setLocalGenerationProgress] = useState<number>(0);
  const [showAIRecModal, setShowAIRecModal] = useState(false);

  // Ref to track if we've already set the default category
  const hasSetDefaultCategory = useRef(false);

  const completionStats = getCompletionStats();
  const completionPercentage = calculateCompletionPercentage();

  // Use extracted hooks
  const {
    reviewedCategories,
    isMarkingReviewed,
    categoryCompletionMessage,
    handleConfirmCategoryReview,
    isCategoryReviewed,
    getNextUnreviewedCategory,
    setReviewedCategories
  } = useCategoryReview({ completionStats, setError, setActiveCategory });

  const {
    totalCategories,
    reviewedCategoriesCount,
    reviewProgressPercentage,
    getCategoryProgress,
    getCategoryStatus: getCategoryStatusFromHook,
    isNextInSequence
  } = useProgressTracking({ completionStats, reviewedCategories });

  const { autoPopulateAttempted, setAutoPopulateAttempted } = useAutoPopulation({
    autoPopulateFromOnboarding,
    completionStats
  });

  // Use ActionButtons business logic hook
  const { handleCreateStrategy, handleSaveStrategy } = useActionButtonsBusinessLogic({
    formData,
    error,
    currentStrategy,
    setAIGenerating,
    setError,
    setCurrentStrategy,
    setSaving,
    setGenerationProgress: setStoreGenerationProgress,
    setEducationalContent: setStoreEducationalContent,
    setShowEducationalModal,
    validateAllFields,
    getCompletionStats,
    generateAIRecommendations,
    createEnhancedStrategy,
    contentPlanningApi
  });

  // Auto-populate from onboarding on first load
  useEffect(() => {
    if (!autoPopulateAttempted) {
      autoPopulateFromOnboarding();
    }
  }, [autoPopulateAttempted, autoPopulateFromOnboarding]);

  // Set default category selection
  useEffect(() => {
    // Only set default category once when component mounts and we have categories
    if (hasSetDefaultCategory.current) {
      console.log('🔍 Default category useEffect: SKIPPED - already set default');
      return;
    }
    
    if (Object.keys(completionStats.category_completion).length > 0) {
      const firstCategory = Object.keys(completionStats.category_completion)[0];
      console.log('🎯 Setting default category:', firstCategory);
      setActiveCategory(firstCategory);
      hasSetDefaultCategory.current = true;
      console.log('✅ hasSetDefaultCategory set to true');
    }
  }, [completionStats.category_completion]); // Removed activeCategory dependency

  // Debug activeCategory changes
  useEffect(() => {
    console.log('🔄 activeCategory changed to:', activeCategory);
    console.trace('📍 Stack trace for activeCategory change');
  }, [activeCategory]);

  // Monitor modal state for debugging
  useEffect(() => {
    console.log('🎯 Modal state changed - transparencyModalOpen:', transparencyModalOpen);
  }, [transparencyModalOpen]);

  // Monitor store data changes for debugging
  useEffect(() => {
    console.log('🎯 Store data changed:', {
      autoPopulatedFieldsCount: Object.keys(autoPopulatedFields || {}).length,
      dataSourcesCount: Object.keys(dataSources || {}).length,
      inputDataPointsCount: Object.keys(inputDataPoints || {}).length,
      transparencyMessagesCount: transparencyMessages?.length || 0
    });
  }, [autoPopulatedFields, dataSources, inputDataPoints, transparencyMessages]);

  // Add CSS keyframes for pulse animation
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
      }
      @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
      }
      @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
    `;
    document.head.appendChild(style);
    return () => {
      if (document.head.contains(style)) {
        document.head.removeChild(style);
      }
    };
  }, []);

  const handleReviewCategory = (categoryId: string) => {
    setActiveCategory(activeCategory === categoryId ? null : categoryId);
  };

  const handleShowEducationalInfo = (categoryId: string) => {
    setShowEducationalInfo(showEducationalInfo === categoryId ? null : categoryId);
  };

  // Wrapper for the hook function to maintain the same interface
  const handleConfirmCategoryReviewWrapper = () => {
    console.log('🔧 Wrapper called with activeCategory:', activeCategory);
    handleConfirmCategoryReview(activeCategory);
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header with Title (Region B) - Enhanced with Futuristic Styling */}
      <HeaderSection autoPopulatedFields={autoPopulatedFields} />

      {/* Error Alert */}
      <ErrorAlert
        error={error}
        onRetry={() => autoPopulateFromOnboarding(true)}
        onShowDataSourceTransparency={() => setShowDataSourceTransparency(true)}
      />

      {/* Strategy Display and Success Alerts */}
      <StrategyDisplay
        currentStrategy={currentStrategy}
        error={error}
        categoryCompletionMessage={categoryCompletionMessage}
        onViewStrategicIntelligence={() => window.location.href = '/content-planning?tab=strategic-intelligence'}
      />

      <Grid container spacing={3}>
        {/* Category Overview Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: 'fit-content', position: 'sticky', top: 20, background: 'linear-gradient(180deg, #f7f9fc, #eef3fb)' }}>
            {/* Enhanced Completion Tracker - Integrated into Category List */}
            <ProgressTracker
              reviewProgressPercentage={reviewProgressPercentage}
              reviewedCategoriesCount={reviewedCategoriesCount}
              totalCategories={totalCategories}
              autoPopulatedFields={autoPopulatedFields}
              aiGenerating={aiGenerating}
              onShowAIRecommendations={() => setShowAIRecommendations(true)}
              onShowDataSourceTransparency={() => setShowDataSourceTransparency(true)}
              onRefreshData={() => autoPopulateFromOnboarding()}
              onRefreshAI={async () => {
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
                    hasData: !!response?.data,
                    responseStructure: {
                      hasDataProperty: !!response?.data?.data,
                      hasFieldsDirect: !!response?.data?.fields,
                      hasFieldsInData: !!response?.data?.data?.fields
                    },
                    fieldsCount: Object.keys(response?.data?.data?.fields || response?.data?.fields || {}).length,
                    sourcesCount: Object.keys(response?.data?.data?.sources || response?.data?.sources || {}).length,
                    meta: response?.data?.data?.meta || response?.data?.meta || {},
                    timestamp: new Date().toISOString()
                  });

                  // Clear the transparency interval since we got the response
                  clearInterval(transparencyInterval);

                  // Process the response
                  if (response && response.data) {
                    // The API response is wrapped in ResponseBuilder format:
                    // { status: "success", message: "...", data: { fields: {...}, sources: {...}, meta: {...} } }
                    // So we need to access payload.data.fields, not payload.fields
                    const payload = response.data;
                    const fields = payload.data?.fields || payload.fields || {};
                    const sources = payload.data?.sources || payload.sources || {};
                    const inputDataPoints = payload.data?.input_data_points || payload.input_data_points || {};
                    const meta = payload.data?.meta || payload.meta || {};
                    
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
                    if (meta.error || !meta.ai_used || meta.ai_overrides_count === 0) {
                      console.error('❌ AI generation failed:', meta.error || 'No AI data generated');
                      setError(`AI generation failed: ${meta.error || 'No real AI data was generated. Please try again.'}`);
                      setTransparencyModalOpen(false);
                      setAIGenerating(false);
                      setIsRefreshing(false);
                      setIsGenerating(false);
                      setRefreshError('AI generation failed. Please try again.');
                      setRefreshMessage('Refresh failed.');
                      return;
                    }
                    
                    // 🚨 CRITICAL: Validate data source
                    if (meta.data_source === 'ai_generation_failed' || meta.data_source === 'ai_generation_error' || meta.data_source === 'ai_disabled') {
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
                    useEnhancedStrategyStore.setState((state) => {
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
                    
                    // Close modal after a short delay to show completion
                    setTimeout(() => {
                      setTransparencyModalOpen(false);
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
                    }, 2000);
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
              }}
              refreshMessage={refreshMessage}
              refreshProgress={refreshProgress}
              isRefreshing={isRefreshing}
              refreshError={refreshError}
            />

            {/* Category Progress - Compact with Futuristic Styling */}
            <Typography variant="h6" gutterBottom sx={{ mb: 1.5, fontSize: '1rem' }}>
              Category Progress
            </Typography>
            
            <CategoryList
              completionStats={completionStats}
              formData={formData}
              STRATEGIC_INPUT_FIELDS={STRATEGIC_INPUT_FIELDS}
              activeCategory={activeCategory}
              reviewedCategories={reviewedCategories}
              isMarkingReviewed={isMarkingReviewed}
              isNextInSequence={isNextInSequence}
              onReviewCategory={handleReviewCategory}
              onShowEducationalInfo={handleShowEducationalInfo}
            />
            
            {/* Quick Actions */}
            <Box sx={{ mt: 3, pt: 2, borderTop: 1, borderColor: 'divider' }}>
              <Typography variant="subtitle2" gutterBottom>
                Quick Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<AutoAwesomeIcon />}
                  onClick={() => setShowAIRecommendations(true)}
                  fullWidth
                >
                  View AI Insights
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<InfoIcon />}
                  onClick={() => setShowDataSourceTransparency(true)}
                  fullWidth
                >
                  View Data Sources
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={() => autoPopulateFromOnboarding(true)}
                  fullWidth
                >
                  Refresh Data
                </Button>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Main Content Area */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, minHeight: '600px', background: 'linear-gradient(180deg, #faf7ff, #f1f0ff)' }}>
            <CategoryDetailView
              activeCategory={activeCategory}
              formData={formData}
              formErrors={formErrors}
              autoPopulatedFields={autoPopulatedFields}
              dataSources={dataSources}
              inputDataPoints={inputDataPoints}
              personalizationData={personalizationData}
              completionStats={completionStats}
              reviewedCategories={reviewedCategories}
              isMarkingReviewed={isMarkingReviewed}
              showEducationalInfo={showEducationalInfo}
              STRATEGIC_INPUT_FIELDS={STRATEGIC_INPUT_FIELDS}
              onUpdateFormField={updateFormField}
              onValidateFormField={validateFormField}
              onShowTooltip={setShowTooltip}
              onViewDataSource={(fieldId) => {
                // If a specific field is provided, show field-specific data source info
                if (fieldId) {
                  console.log('🎯 Viewing data source for field:', fieldId);
                  // For now, just open the general data source transparency modal
                  // In the future, this could open a field-specific modal
                  setShowDataSourceTransparency(true);
                } else {
                  setShowDataSourceTransparency(true);
                }
              }}
              onConfirmCategoryReview={handleConfirmCategoryReviewWrapper}
              onSetActiveCategory={setActiveCategory}
              onSetShowEducationalInfo={setShowEducationalInfo}
              getCategoryIcon={getCategoryIcon}
              getCategoryColor={getCategoryColor}
              getEducationalContent={getEducationalContent}
            />
          </Paper>
        </Grid>
      </Grid>

      {/* Action Buttons */}
      <ActionButtons
        aiGenerating={aiGenerating}
        saving={saving}
        reviewProgressPercentage={reviewProgressPercentage}
        onCreateStrategy={handleCreateStrategy}
        onSaveStrategy={handleSaveStrategy}
      />

      {/* AI Recommendations Modal */}
      <Dialog 
        open={showAIRecModal}
        onClose={() => setShowAIRecModal(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <AutoAwesomeIcon color="primary" />
            AI Recommendations
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body1" gutterBottom>
            AI recommendations are being generated for your strategy. This process may take a few minutes.
          </Typography>
          <LinearProgress variant="indeterminate" sx={{ mt: 2 }} />
        </DialogContent>
      </Dialog>

      {/* Enhanced Educational Modal for Strategy Generation */}
      <EducationalModal
        open={showEducationalModal}
        onClose={() => setShowEducationalModal(false)}
                educationalContent={storeEducationalContent}      
        generationProgress={storeGenerationProgress}
      />

      {/* Data Source Transparency Modal */}
      <Dialog 
        open={showDataSourceTransparency} 
        onClose={() => setShowDataSourceTransparency(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <InfoIcon />
            Data Source Transparency
          </Box>
        </DialogTitle>
        <DialogContent>
          <DataSourceTransparency 
            autoPopulatedFields={autoPopulatedFields}
            dataSources={dataSources}
            inputDataPoints={inputDataPoints} // Use real input data points from store
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDataSourceTransparency(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Strategy Autofill Transparency Modal */}
      <StrategyAutofillTransparencyModal
        open={transparencyModalOpen}
        onClose={() => setTransparencyModalOpen(false)}
        autoPopulatedFields={autoPopulatedFields}
        dataSources={dataSources}
        inputDataPoints={inputDataPoints}
        isGenerating={isGenerating}
        generationProgress={storeGenerationProgress}
        currentPhase={currentPhase}
        educationalContent={storeEducationalContent}
        transparencyMessages={transparencyMessages}
        error={error}
      />

      {/* Tooltip */}
      {showTooltip && (
        <EnhancedTooltip
          fieldId={showTooltip}
          open={!!showTooltip}
          onClose={() => setShowTooltip(null)}
        />
      )}
    </Box>
  );
};

export default ContentStrategyBuilder; 