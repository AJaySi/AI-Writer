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
  Timeline as TimelineIcon
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

// Import extracted utilities
import { getCategoryIcon, getCategoryColor, getCategoryName, getCategoryStatus } from './ContentStrategyBuilder/utils/categoryHelpers';
import { getEducationalContent } from './ContentStrategyBuilder/utils/educationalContent';

// Import extracted components
import CategoryList from './ContentStrategyBuilder/components/CategoryList';
import ProgressTracker from './ContentStrategyBuilder/components/ProgressTracker';
import HeaderSection from './ContentStrategyBuilder/components/HeaderSection';

const ContentStrategyBuilder: React.FC = () => {
  const {
    formData,
    formErrors,
    autoPopulatedFields,
    dataSources,
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
    setSaving
  } = useEnhancedStrategyStore();

  const [showTooltip, setShowTooltip] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [showEducationalInfo, setShowEducationalInfo] = useState<string | null>(null);
  const [showAIRecommendations, setShowAIRecommendations] = useState(false);
  const [showDataSourceTransparency, setShowDataSourceTransparency] = useState(false);

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
          const newStrategy = await createEnhancedStrategy(strategyData);
          console.log('New strategy created:', newStrategy);

          if (newStrategy && newStrategy.id) {
            console.log('Generating AI recommendations for new strategy ID:', newStrategy.id);
            await generateAIRecommendations(newStrategy.id);
            
            // Set the current strategy and show success message
            setCurrentStrategy(newStrategy);
            setError(null); // Clear any previous errors
            
            // Show success message
            setTimeout(() => {
              setError('Strategy created successfully! Check the Strategic Intelligence tab for detailed insights.');
            }, 100);
            
            // Auto-switch to Strategic Intelligence tab after creation
            // This would need to be handled by the parent component
          } else {
            setError('Failed to create strategy or get strategy ID for AI generation.');
            console.error('Failed to create strategy or get strategy ID for AI generation.');
          }
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
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Success Alert */}
      {!error && currentStrategy && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Strategy "{currentStrategy.name}" created successfully! Check the Strategic Intelligence tab for detailed insights.
        </Alert>
      )}

      {/* Strategy Display */}
      {currentStrategy && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Created Strategy: {currentStrategy.name}
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Industry: {currentStrategy.industry}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                Completion: {currentStrategy.completion_percentage}%
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Created: {new Date(currentStrategy.created_at).toLocaleDateString()}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                ID: {currentStrategy.id}
              </Typography>
            </Grid>
          </Grid>
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              onClick={() => window.location.href = '/content-planning?tab=strategic-intelligence'}
              startIcon={<AssessmentIcon />}
            >
              View Strategic Intelligence
            </Button>
          </Box>
        </Paper>
      )}

      {categoryCompletionMessage && (
        <Alert
          severity="success"
          sx={{ mb: 3, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
        >
          {categoryCompletionMessage}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Category Overview Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: 'fit-content', position: 'sticky', top: 20 }}>
            {/* Enhanced Completion Tracker - Integrated into Category List */}
            <ProgressTracker
              reviewProgressPercentage={reviewProgressPercentage}
              reviewedCategoriesCount={reviewedCategoriesCount}
              totalCategories={totalCategories}
              autoPopulatedFields={autoPopulatedFields}
              aiGenerating={aiGenerating}
              onShowAIRecommendations={() => setShowAIRecommendations(true)}
              onShowDataSourceTransparency={() => setShowDataSourceTransparency(true)}
              onRefreshData={autoPopulateFromOnboarding}
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
                  onClick={autoPopulateFromOnboarding}
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
          <Paper sx={{ p: 3, minHeight: '600px' }}>
            {activeCategory ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                {/* Category Header */}
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  {getCategoryIcon(activeCategory)}
                  <Typography variant="h5" sx={{ ml: 1 }}>
                    {activeCategory.split('_').map(word => 
                      word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ')}
                  </Typography>
                  <Chip 
                    label={`${Math.round(completionStats.category_completion[activeCategory])}% Complete`}
                    color={getCategoryColor(activeCategory) as any}
                    sx={{ ml: 'auto' }}
                  />
                </Box>

                {/* Educational Info Dialog */}
                <Dialog 
                  open={!!showEducationalInfo} 
                  onClose={() => setShowEducationalInfo(null)}
                  maxWidth="md"
                  fullWidth
                >
                  <DialogTitle>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <SchoolIcon />
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).title}
                    </Box>
                  </DialogTitle>
                  <DialogContent>
                    <Typography variant="body1" paragraph>
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).description}
                    </Typography>
                    
                    <Typography variant="h6" gutterBottom>
                      Key Points:
                    </Typography>
                    <List>
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).points.map((point, index) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemIcon>
                            <LightbulbIcon color="primary" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText primary={point} />
                        </ListItem>
                      ))}
                    </List>
                    
                <Typography variant="h6" gutterBottom>
                      Pro Tips:
                </Typography>
                    <List>
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).tips.map((tip, index) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemIcon>
                            <PsychologyIcon color="secondary" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText primary={tip} />
                        </ListItem>
                      ))}
                    </List>
                  </DialogContent>
                  <DialogActions>
                    <Button onClick={() => setShowEducationalInfo(null)}>
                      Got it!
                    </Button>
                  </DialogActions>
                </Dialog>

                {/* Category Fields */}
                <Grid container spacing={1.5}>
                  {STRATEGIC_INPUT_FIELDS
                    .filter(field => field.category === activeCategory)
                    .map((field) => {
                      // Group number-based fields together
                      const isNumberField = field.type === 'number' || 
                        field.id.includes('budget') || 
                        field.id.includes('size') || 
                        field.id.includes('timeline') ||
                        field.id.includes('metrics');
                      
                      // Determine grid size based on field type
                      const gridSize = isNumberField ? 6 : 12;
                      
                      return (
                        <Grid item xs={12} md={gridSize} key={field.id}>
                          <StrategicInputField
                            fieldId={field.id}
                            value={formData[field.id]}
                            error={formErrors[field.id]}
                            autoPopulated={!!autoPopulatedFields[field.id]}
                            dataSource={dataSources[field.id]}
                            confidenceLevel={autoPopulatedFields[field.id] ? 0.8 : undefined}
                            dataQuality={autoPopulatedFields[field.id] ? 'High Quality' : undefined}
                            onChange={(value: any) => updateFormField(field.id, value)}
                            onValidate={() => validateFormField(field.id)}
                            onShowTooltip={() => setShowTooltip(field.id)}
                          />
                        </Grid>
                      );
                    })}
                </Grid>

                {/* Category Actions */}
                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                  {(() => {
                    const isReviewed = reviewedCategories.has(activeCategory);
                    console.log('🔍 Category review status:', {
                      activeCategory,
                      isReviewed,
                      reviewedCategories: Array.from(reviewedCategories)
                    });
                    return !isReviewed ? (
                      <Button
                        variant="contained"
                        onClick={() => {
                          console.log('🔘 Button clicked! activeCategory:', activeCategory);
                          console.log('🔘 reviewedCategories:', Array.from(reviewedCategories));
                          console.log('🔘 isMarkingReviewed:', isMarkingReviewed);
                          handleConfirmCategoryReviewWrapper();
                        }}
                        startIcon={isMarkingReviewed ? <CircularProgress size={20} /> : <CheckCircleIcon />}
                        disabled={isMarkingReviewed}
                      >
                        {isMarkingReviewed ? 'Marking as Reviewed...' : 'Mark as Reviewed'}
                      </Button>
                    ) : (
                      <Chip
                        label="Category Reviewed"
                        color="success"
                        icon={<CheckCircleIcon />}
                        sx={{ px: 2, py: 1 }}
                      />
                    );
                  })()}
                  
                  <Button
                    variant="outlined"
                    onClick={() => setActiveCategory(null)}
                  >
                    Back to Overview
                  </Button>
                </Box>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <Box sx={{ textAlign: 'center', py: 8 }}>
                  <TimelineIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h5" gutterBottom>
                    Select a Category to Review
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    Click on any category from the left panel to review and complete the fields.
                  </Typography>
          </Box>
              </motion.div>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Action Buttons */}
      <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <MuiTooltip 
          title={reviewProgressPercentage < 20 ? `Complete at least 20% of the form (currently ${Math.round(reviewProgressPercentage)}%)` : 'Create a comprehensive content strategy with AI insights'}
          placement="top"
        >
          <span>
            <Button
              variant="outlined"
              startIcon={<AutoAwesomeIcon />}
              onClick={handleCreateStrategy}
              disabled={aiGenerating || reviewProgressPercentage < 20}
            >
              {aiGenerating ? 'Creating...' : 'Create Strategy'}
            </Button>
          </span>
        </MuiTooltip>
        
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={handleSaveStrategy}
          disabled={saving || reviewProgressPercentage < 30}
        >
          {saving ? 'Saving...' : 'Save Strategy'}
        </Button>
      </Box>

      {/* AI Recommendations Modal */}
      <Dialog 
        open={showAIRecommendations} 
        onClose={() => setShowAIRecommendations(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <AutoAwesomeIcon />
            AI Recommendations & Insights
          </Box>
        </DialogTitle>
        <DialogContent>
          <AIRecommendationsPanel 
            aiGenerating={aiGenerating}
            onGenerateRecommendations={handleCreateStrategy}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAIRecommendations(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

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