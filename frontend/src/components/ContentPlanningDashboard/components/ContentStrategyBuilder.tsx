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
  const [educationalContent, setEducationalContent] = useState<any>(null);
  const [generationProgress, setGenerationProgress] = useState<number>(0);
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
    setGenerationProgress,
    setEducationalContent,
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
                  setAIGenerating(true);
                  setIsRefreshing(true);
                  setRefreshError(null);
                  setRefreshMessage('Initializing refresh…');
                  setRefreshProgress(5);
                  const es = await contentPlanningApi.streamAutofillRefresh(1, true, true);
                  es.onmessage = (evt: MessageEvent) => {
                    try {
                      const data = JSON.parse(evt.data);
                      if (data.type === 'status' || data.type === 'progress') {
                        setRefreshMessage(data.message || 'Refreshing…');
                        if (typeof data.progress === 'number') setRefreshProgress(data.progress);
                      }
                      if (data.type === 'result') {
                        const payload = data.data || {};
                        const fields = payload.fields || {};
                        const sources = payload.sources || {};
                        const inputDataPoints = payload.input_data_points || {};
                        const meta = payload.meta || {};
                        
                        console.log('🎯 AI Refresh Result - Payload:', payload);
                        console.log('🎯 AI Refresh Result - Fields:', fields);
                        console.log('🎯 AI Refresh Result - Meta:', meta);
                        
                        const fieldValues: Record<string, any> = {};
                        Object.keys(fields).forEach((fieldId) => {
                          const fieldData = fields[fieldId];
                          if (fieldData && typeof fieldData === 'object' && 'value' in fieldData) {
                            fieldValues[fieldId] = fieldData.value;
                            console.log(`✅ Processed field ${fieldId}:`, fieldData.value);
                          } else {
                            console.log(`❌ Skipped field ${fieldId}:`, fieldData);
                          }
                        });
                        
                        console.log('🎯 Final fieldValues:', fieldValues);
                        
                        useEnhancedStrategyStore.setState((state) => {
                          const newState = {
                            autoPopulatedFields: { ...state.autoPopulatedFields, ...fieldValues },
                            dataSources: { ...state.dataSources, ...sources },
                            inputDataPoints,
                            formData: { ...state.formData, ...fieldValues }
                          };
                          console.log('🎯 Updated store state:', newState);
                          return newState;
                        });
                        
                        // Enhanced success/error messaging based on retry attempts and success rate
                        const attempts = meta.attempts || 1;
                        const successRate = meta.success_rate || 0;
                        const aiOverridesCount = meta.ai_overrides_count || 0;
                        
                        if (!meta.ai_used || aiOverridesCount === 0) {
                          const msg = meta.error || 'AI did not produce new values. Please try again or complete onboarding data.';
                          setError(msg);
                          setRefreshError(msg);
                          setRefreshMessage(`No new AI values available. (${attempts} attempt${attempts > 1 ? 's' : ''})`);
                        } else {
                          // Show success message with retry info if applicable
                          if (attempts > 1) {
                            setRefreshMessage(`AI refresh completed successfully! Generated ${aiOverridesCount} fields in ${attempts} attempts (${successRate.toFixed(1)}% success rate).`);
                          } else {
                            setRefreshMessage(`AI refresh completed! Generated ${aiOverridesCount} fields (${successRate.toFixed(1)}% success rate).`);
                          }
                          
                          // Show warning if success rate is low but we got some data
                          if (successRate < 70 && aiOverridesCount > 0) {
                            setRefreshError(`Warning: Only ${successRate.toFixed(1)}% of fields were filled. Some fields may need manual input.`);
                          }
                        }
                        
                        es.close();
                        setAIGenerating(false);
                        setIsRefreshing(false);
                        
                        // Clear success message after a delay
                        if (aiOverridesCount > 0) {
                          setTimeout(() => {
                            setRefreshMessage(null);
                            setRefreshProgress(0);
                          }, 5000);
                        }
                      }
                      if (data.type === 'error') {
                        const msg = data.message || 'AI refresh failed.';
                        setRefreshError(msg);
                        es.close();
                        setAIGenerating(false);
                        setIsRefreshing(false);
                        setRefreshMessage('Refresh failed.');
                      }
                    } catch (err: any) {
                      console.error('SSE parse error:', err);
                    }
                  };
                  es.onerror = (err: any) => {
                    console.error('SSE connection error:', err);
                    es.close();
                    setAIGenerating(false);
                    setIsRefreshing(false);
                    setRefreshError('AI refresh connection lost. Please try again.');
                    setRefreshMessage('Connection lost.');
                  };
                } catch (e) {
                  console.error('AI refresh error', e);
                  setAIGenerating(false);
                  setIsRefreshing(false);
                  setRefreshError('AI refresh failed. Please try again.');
                  setRefreshMessage('Refresh failed.');
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
              personalizationData={personalizationData}
              completionStats={completionStats}
              reviewedCategories={reviewedCategories}
              isMarkingReviewed={isMarkingReviewed}
              showEducationalInfo={showEducationalInfo}
              STRATEGIC_INPUT_FIELDS={STRATEGIC_INPUT_FIELDS}
              onUpdateFormField={updateFormField}
              onValidateFormField={validateFormField}
              onShowTooltip={setShowTooltip}
                                onViewDataSource={() => setShowDataSourceTransparency(true)}
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
        educationalContent={educationalContent}
        generationProgress={generationProgress}
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