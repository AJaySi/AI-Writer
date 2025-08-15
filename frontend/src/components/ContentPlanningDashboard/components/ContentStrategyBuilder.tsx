  import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
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
import EnterpriseDatapointsModal from './EnterpriseDatapointsModal';

// Import extracted hooks
import { useCategoryReview } from './ContentStrategyBuilder/hooks/useCategoryReview';
import { useProgressTracking } from './ContentStrategyBuilder/hooks/useProgressTracking';
import { useAutoPopulation } from './ContentStrategyBuilder/hooks/useAutoPopulation';
import { useModalManagement } from './ContentStrategyBuilder/hooks/useModalManagement';
import { useAIRefresh } from './ContentStrategyBuilder/hooks/useAIRefresh';
import { useEventHandlers } from './ContentStrategyBuilder/hooks/useEventHandlers';
import { useStrategyCreation } from './ContentStrategyBuilder/hooks/useStrategyCreation';

// Import extracted utilities
import { getCategoryIcon, getCategoryColor, getCategoryName, getCategoryStatus } from './ContentStrategyBuilder/utils/categoryHelpers';
import { getEducationalContent } from './ContentStrategyBuilder/utils/educationalContent';
import { setupCSSAnimations, cleanupCSSAnimations } from './ContentStrategyBuilder/utils/cssAnimations';

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
  const navigate = useNavigate();
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

  const [showAIRecommendations, setShowAIRecommendations] = useState(false);
  const [showDataSourceTransparency, setShowDataSourceTransparency] = useState(false);
  const [localEducationalContent, setLocalEducationalContent] = useState<any>(null);
  const [localGenerationProgress, setLocalGenerationProgress] = useState<number>(0);
  const [showAIRecModal, setShowAIRecModal] = useState(false);

  // Ref to track if we've already set the default category
  const hasSetDefaultCategory = useRef(false);

  // Use extracted hooks
  const {
    showTooltip,
    setShowTooltip,
    activeCategory,
    setActiveCategory,
    showEducationalInfo,
    setShowEducationalInfo,
    handleReviewCategory,
    handleShowEducationalInfo
  } = useEventHandlers();

  // Use strategy creation hook first
  const { originalHandleCreateStrategy, handleSaveStrategy } = useStrategyCreation({
    formData,
    error,
    currentStrategy,
    setAIGenerating,
    setError,
    setCurrentStrategy,
    setSaving,
    setGenerationProgress: setStoreGenerationProgress,
    setEducationalContent: setStoreEducationalContent,
    setShowEducationalModal: () => {}, // Temporary placeholder
    validateAllFields,
    getCompletionStats,
    generateAIRecommendations: (strategyId: string) => generateAIRecommendations(strategyId),
    createEnhancedStrategy,
    contentPlanningApi
  });

  const {
    showEducationalModal,
    setShowEducationalModal,
    showEnterpriseModal,
    setShowEnterpriseModal,
    handleProceedWithCurrentStrategy,
    handleAddEnterpriseDatapoints
  } = useModalManagement({
    aiGenerating,
    originalHandleCreateStrategy
  });

  const {
    refreshMessage,
    setRefreshMessage,
    refreshProgress,
    setRefreshProgress,
    isRefreshing,
    setIsRefreshing,
    refreshError,
    setRefreshError,
    handleAIRefresh
  } = useAIRefresh({
    setTransparencyModalOpen,
    setIsGenerating,
    setStoreGenerationProgress,
    setCurrentPhase,
    clearTransparencyMessages,
    addTransparencyMessage,
    setAIGenerating,
    setError
  });

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



  // Enhanced handleCreateStrategy to show enterprise modal
  const handleCreateStrategy = () => {
    console.log('🎯 handleCreateStrategy called');
    console.log('🎯 completionStats.category_completion:', completionStats.category_completion);
    console.log('🎯 reviewedCategories:', reviewedCategories);
    console.log('🎯 Current showEnterpriseModal state:', showEnterpriseModal);
    console.log('🎯 Current aiGenerating state:', aiGenerating);
    
    // Prevent multiple calls
    if (aiGenerating) {
      console.log('🎯 Already generating, skipping duplicate call');
      return;
    }
    
    // Check if all categories are reviewed
    const allCategoriesReviewed = Object.keys(completionStats.category_completion).every(
      category => Array.from(reviewedCategories).includes(category)
    );

    console.log('🎯 allCategoriesReviewed:', allCategoriesReviewed);

    if (allCategoriesReviewed) {
      // Show enterprise modal instead of creating strategy immediately
      console.log('🎯 Showing enterprise modal - setting to true');
      setShowEnterpriseModal(true);
      
      // Add debugging to confirm modal state change
      setTimeout(() => {
        console.log('🎯 Enterprise modal state after setShowEnterpriseModal(true):', showEnterpriseModal);
      }, 0);
      
      // Return early to prevent calling originalHandleCreateStrategy
      return;
    } else {
      // If not all categories reviewed, proceed with original logic
      console.log('🎯 Not all categories reviewed, proceeding with original logic');
      originalHandleCreateStrategy();
    }
  };



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

  // Monitor enterprise modal state for debugging
  useEffect(() => {
    console.log('🎯 Enterprise modal state changed - showEnterpriseModal:', showEnterpriseModal);
    
    // If modal was unexpectedly closed, log it
    if (!showEnterpriseModal && aiGenerating) {
      console.warn('🎯 WARNING: Enterprise modal closed while AI is generating');
    }
    
    // Only warn about unexpected closure if it's not due to hot reload
    if (!showEnterpriseModal && !aiGenerating) {
      const savedModalState = sessionStorage.getItem('showEnterpriseModal');
      if (savedModalState !== 'true') {
        console.warn('🎯 WARNING: Enterprise modal closed unexpectedly (not due to hot reload)');
      }
    }
  }, [showEnterpriseModal, aiGenerating]);

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
    const style = setupCSSAnimations();
    return () => {
      cleanupCSSAnimations(style);
    };
  }, []);



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
              onRefreshAI={handleAIRefresh}
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
        onSaveStrategy={() => handleSaveStrategy()}
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
        onReviewStrategy={() => {
          console.log('🎯 User clicked "Next: Review Strategy and Create Calendar"');
          setShowEducationalModal(false);
          // Navigate to content planning dashboard with Content Strategy tab active
          navigate('/content-planning', { 
            state: { activeTab: 0 } // 0 = Content Strategy tab
          });
        }}
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
        onClose={() => {
          setTransparencyModalOpen(false);
          // Ensure form data is refreshed after modal closes
          console.log('🎯 Modal closed - ensuring form data is updated');
          console.log('🎯 Current autoPopulatedFields:', Object.keys(autoPopulatedFields || {}));
          console.log('🎯 Current formData keys:', Object.keys(formData || {}));
        }}
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

      {/* Enterprise Datapoints Modal */}
      <EnterpriseDatapointsModal
        open={showEnterpriseModal}
        onClose={() => {
          console.log('🎯 Enterprise modal onClose called');
          console.log('🎯 Current aiGenerating state:', aiGenerating);
          setShowEnterpriseModal(false);
          sessionStorage.removeItem('showEnterpriseModal'); // Clear sessionStorage
        }}
        onProceedWithCurrent={handleProceedWithCurrentStrategy}
        onAddEnterpriseDatapoints={handleAddEnterpriseDatapoints}
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