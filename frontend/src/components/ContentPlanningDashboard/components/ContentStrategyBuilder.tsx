  import React, { useState, useEffect, useRef, useMemo } from 'react';
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
import { useStrategyBuilderStore, STRATEGIC_INPUT_FIELDS } from '../../../stores/strategyBuilderStore';
import { useEnhancedStrategyStore } from '../../../stores/enhancedStrategyStore';
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
  
  // Strategy Builder Store (for form data, validation, auto-population)
  const {
    formData,
    formErrors,
    autoPopulatedFields,
    dataSources,
    inputDataPoints,
    personalizationData,
    confidenceScores,
    loading,
    error,
    saving,
    currentStrategy,
    updateFormField,
    validateFormField,
    validateAllFields,
    resetForm,
    autoPopulateFromOnboarding,
    createStrategy: createEnhancedStrategy,
    calculateCompletionPercentage,
    getCompletionStats,
    setError,
    setCurrentStrategy,
    setSaving
  } = useStrategyBuilderStore();
  
  // Enhanced Strategy Store (for AI analysis, progressive disclosure, transparency)
  const {
    aiGenerating,
    currentStep,
    completedSteps,
    disclosureSteps,
    transparencyModalOpen,
    transparencyGenerationProgress: storeGenerationProgress,
    currentPhase,
    educationalContent: storeEducationalContent,
    transparencyMessages,
    transparencyGenerating: isGenerating,
    setTransparencyModalOpen,
    setTransparencyGenerationProgress: setStoreGenerationProgress,
    setCurrentPhase,
    setEducationalContent: setStoreEducationalContent,
    addTransparencyMessage,
    clearTransparencyMessages,
    setTransparencyGenerating: setIsGenerating,
    completeStep,
    getNextStep,
    getPreviousStep,
    setCurrentStep,
    canProceedToDisclosureStep: canProceedToStep,
    generateAIRecommendations,
    setAIGenerating
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

  // Create a state for educational modal that can be passed to both hooks
  const [showEducationalModal, setShowEducationalModal] = useState(false);
  const [showEnterpriseModal, setShowEnterpriseModal] = useState(false);

  // Persist enterprise modal state across hot reloads
  useEffect(() => {
    const savedModalState = sessionStorage.getItem('showEnterpriseModal');
    if (savedModalState === 'true') {
      console.log('🎯 Restoring enterprise modal state from sessionStorage');
      setShowEnterpriseModal(true);
    }
  }, []);
  
  // Save modal state to sessionStorage when it changes
  useEffect(() => {
    sessionStorage.setItem('showEnterpriseModal', showEnterpriseModal.toString());
  }, [showEnterpriseModal]);
  
  // Cleanup sessionStorage on component unmount
  useEffect(() => {
    return () => {
      // Only clear if we're not in the middle of showing the modal
      if (!showEnterpriseModal) {
        sessionStorage.removeItem('showEnterpriseModal');
      }
    };
  }, [showEnterpriseModal]);

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
    setShowEducationalModal, // Pass the actual setShowEducationalModal function
    validateAllFields,
    getCompletionStats,
    generateAIRecommendations: (strategyId: string) => generateAIRecommendations(strategyId),
    createEnhancedStrategy,
    contentPlanningApi
  });

  const {
    handleProceedWithCurrentStrategy,
    handleAddEnterpriseDatapoints
  } = useModalManagement({
    aiGenerating,
    originalHandleCreateStrategy,
    setShowEnterpriseModal
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

  const completionStats = useMemo(() => getCompletionStats(), [formData]);
  const completionPercentage = useMemo(() => calculateCompletionPercentage(), [formData]);

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

  // Add ref for scroll to review section
  const reviewSectionRef = useRef<HTMLDivElement>(null);

  // Handle scroll to review section
  const handleScrollToReview = () => {
    if (reviewSectionRef.current) {
      reviewSectionRef.current.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
      });
    }
  };

  // Handle continue with present values
  const handleContinueWithPresent = () => {
    console.log('🎯 Continuing with present autofilled values');
    // This will show the next button and allow user to proceed
  };

  // Determine if we have autofill data
  const hasAutofillData = Object.keys(autoPopulatedFields).length > 0;
  
  // Get last autofill time from session storage or use current time
  const lastAutofillTime = sessionStorage.getItem('lastAutofillTime') || new Date().toISOString();
  
  // Get data source from store
  const dataSource = Object.keys(dataSources).length > 0 ? 'Onboarding Database' : undefined;

  // Log autofill data status for debugging
  useEffect(() => {
    console.log('📋 StrategyBuilder: Autofill data status:', {
      hasAutofillData,
      autoPopulatedFieldsCount: Object.keys(autoPopulatedFields).length,
      dataSourcesCount: Object.keys(dataSources).length,
      inputDataPointsCount: Object.keys(inputDataPoints).length,
      personalizationDataCount: Object.keys(personalizationData).length,
      confidenceScoresCount: Object.keys(confidenceScores).length,
      lastAutofillTime,
      dataSource
    });
  }, [hasAutofillData, autoPopulatedFields, dataSources, inputDataPoints, personalizationData, confidenceScores, lastAutofillTime, dataSource]);



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
  }, [autoPopulateAttempted]); // Removed autoPopulateFromOnboarding from dependencies

  // Set default category selection
  useEffect(() => {
    // Only set default category once when component mounts and we have categories
    if (hasSetDefaultCategory.current) {
      console.log('🔍 Default category useEffect: SKIPPED - already set default');
      return;
    }
    
    if (Object.keys(completionStats.category_completion).length > 0) {
      const firstCategory = Object.keys(completionStats.category_completion)[0];
      setActiveCategory(firstCategory);
      hasSetDefaultCategory.current = true;
    }
  }, [completionStats.category_completion]); // Removed activeCategory dependency

  // Monitor enterprise modal state for debugging
  useEffect(() => {
    // If modal was unexpectedly closed, log it
    if (!showEnterpriseModal && aiGenerating) {
      console.warn('Enterprise modal closed while AI is generating');
    }
  }, [showEnterpriseModal, aiGenerating]);

  // Note: Removed store monitoring useEffect to prevent infinite re-renders

  // Add CSS keyframes for pulse animation
  useEffect(() => {
    const style = setupCSSAnimations();
    return () => {
      cleanupCSSAnimations(style);
    };
  }, []);



  // Wrapper for the hook function to maintain the same interface
  const handleConfirmCategoryReviewWrapper = () => {
    handleConfirmCategoryReview(activeCategory);
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header with Title (Region B) - Enhanced with Futuristic Styling */}
                  <HeaderSection
              autoPopulatedFields={autoPopulatedFields}
              dataSources={dataSources}
              inputDataPoints={inputDataPoints}
              personalizationData={personalizationData}
              confidenceScores={confidenceScores}
              loading={loading}
              error={error}
              onRefreshAutofill={handleAIRefresh}
              onContinueWithPresent={handleContinueWithPresent}
              onScrollToReview={handleScrollToReview}
              hasAutofillData={hasAutofillData}
              lastAutofillTime={lastAutofillTime}
              dataSource={dataSource}
            />

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
            

          </Paper>
        </Grid>

        {/* Main Content Area */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, minHeight: '600px', background: 'linear-gradient(180deg, #faf7ff, #f1f0ff)' }}>
            <div ref={reviewSectionRef}>
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
            </div>
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
          setShowEducationalModal(false);
          
          // Set flag to indicate coming from strategy builder
          sessionStorage.setItem('fromStrategyBuilder', 'true');
          
          // Navigate to content planning dashboard with Content Strategy tab active
          navigate('/content-planning', { 
            state: { 
              activeTab: 0, // 0 = Content Strategy tab
              fromStrategyBuilder: true 
            }
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