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
  FiberManualRecord as FiberManualRecordIcon
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
import { contentPlanningApi } from '../../../services/contentPlanningApi';

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
          
          // Use SSE streaming endpoint for strategy generation with educational content
          await generateStrategyWithSSE(strategyData);
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

  const generateStrategyWithSSE = async (strategyData: any) => {
    try {
      console.log('🚀 Starting SSE strategy generation...');
      
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

      // Create basic strategy first
      const newStrategy = await createEnhancedStrategy(strategyData);
      console.log('Basic strategy created:', newStrategy);

      if (newStrategy && newStrategy.id) {
        console.log('Starting AI generation for strategy ID:', newStrategy.id);
        
        // Set a timeout for the entire process (5 minutes)
        const processTimeout = setTimeout(async () => {
          console.error('⏰ Strategy generation timeout after 5 minutes');
          
          // Try to check if the strategy was actually created
          try {
            const existingStrategy = await contentPlanningApi.getEnhancedStrategy(newStrategy.id.toString());
            if (existingStrategy) {
              console.log('✅ Strategy was created successfully despite SSE timeout');
              setCurrentStrategy(existingStrategy);
              setError('Strategy created successfully! The AI generation may still be running in the background. Check the Strategic Intelligence tab for detailed insights.');
            } else {
              setError('Strategy generation is taking longer than expected. The process may still be running in the background. Please check the Strategic Intelligence tab for results.');
            }
          } catch (checkError) {
            console.error('Error checking strategy status:', checkError);
            setError('Strategy generation is taking longer than expected. The process may still be running in the background. Please check the Strategic Intelligence tab for results.');
          }
          
          setShowEducationalModal(false);
        }, 5 * 60 * 1000); // 5 minutes
        
        // Add heartbeat monitoring
        let lastMessageTime = Date.now();
        const heartbeatInterval = setInterval(() => {
          const timeSinceLastMessage = Date.now() - lastMessageTime;
          if (timeSinceLastMessage > 30000) { // 30 seconds without message
            console.warn('⚠️ No SSE messages received for 30 seconds');
            setEducationalContent({
              title: '🤖 AI-Powered Strategy Generation',
              description: 'AI analysis is still running in the background. This may take a few more minutes.',
              details: [
                '⏳ Processing complex AI analysis',
                '📊 Analyzing market data',
                '🎯 Generating strategic insights',
                '📈 Calculating performance predictions'
              ],
              insight: 'The AI is working on comprehensive analysis. This is normal for complex strategies.',
              estimated_time: 'Additional 1-2 minutes'
            });
          }
        }, 10000); // Check every 10 seconds
        
        // Use SSE endpoint for AI generation with educational content
        const eventSource = await contentPlanningApi.streamStrategyGeneration(Number(newStrategy.id));
        
        console.log('🔌 SSE EventSource created:', eventSource);
        console.log('🔌 SSE readyState:', eventSource.readyState);
        
        // Handle SSE data with proper parsing
        eventSource.onmessage = (event) => {
          try {
            console.log('📨 Raw SSE message:', event.data);
            
            // Update last message time for heartbeat
            lastMessageTime = Date.now();
            
            // Parse the SSE data
            const data = JSON.parse(event.data);
            console.log('📨 Parsed SSE data:', data);
            console.log('📨 Message type analysis:', {
              hasStep: data.step !== undefined,
              hasProgress: data.progress !== undefined,
              hasEducationalContent: !!data.educational_content,
              hasError: !!data.error,
              hasSuccess: !!data.success,
              hasType: !!data.type,
              step: data.step,
              progress: data.progress,
              message: data.message
            });
            
            // Handle different types of messages
            if (data.error) {
              console.error('❌ SSE Error:', data.error);
              clearTimeout(processTimeout);
              clearInterval(heartbeatInterval);
              setError(`AI generation failed: ${data.error}`);
              setShowEducationalModal(false);
              eventSource.close();
              return;
            }
            
            // Handle step and progress updates (backend sends these)
            if (data.step !== undefined) {
              console.log('🔢 Updating step:', data.step);
              // Calculate progress from step (each step is 10%)
              const stepProgress = Math.min(data.step * 10, 100);
              console.log('📊 Calculated progress from step:', stepProgress);
              setGenerationProgress(stepProgress);
            }
            
            // Handle explicit progress updates
            if (data.progress !== undefined) {
              console.log('📊 Updating progress:', data.progress);
              setGenerationProgress(data.progress);
            }
            
            // Handle educational content updates
            if (data.educational_content) {
              console.log('📚 Updating educational content:', data.educational_content);
              setEducationalContent(data.educational_content);
            }
            
            // Handle completion
            if (data.step === 10 && data.success) {
              console.log('✅ Strategy generation completed successfully!');
              clearTimeout(processTimeout);
              clearInterval(heartbeatInterval);
              setCurrentStrategy(data.strategy);
              setShowEducationalModal(false);
              setError('Strategy created successfully! Check the Strategic Intelligence tab for detailed insights.');
              eventSource.close();
            }
            
            // Handle educational content from AI service manager
            if (data.type === 'educational_content' && data.educational_content) {
              console.log('📚 AI Service educational content:', data.educational_content);
              setEducationalContent(data.educational_content);
            }
            
            // Handle success messages for individual steps
            if (data.success && data.message) {
              console.log('✅ Step completed:', data.message);
              // Progress is already updated above, just log the success
            }
            
          } catch (parseError) {
            console.error('❌ Error parsing SSE message:', parseError);
            console.error('Raw message:', event.data);
          }
        };
        
        // Handle SSE errors
        eventSource.onerror = (error) => {
          console.error('❌ SSE connection error:', error);
          console.error('   ReadyState:', eventSource.readyState);
          
          // Check connection state
          switch (eventSource.readyState) {
            case EventSource.CONNECTING:
              console.log('🔄 SSE connection is connecting...');
              break;
            case EventSource.OPEN:
              console.log('✅ SSE connection is open');
              break;
            case EventSource.CLOSED:
              console.log('🔌 SSE connection is closed');
              clearTimeout(processTimeout);
              clearInterval(heartbeatInterval);
              setError('Connection lost during AI generation. The process may still be running in the background. Please check the Strategic Intelligence tab for results.');
              setShowEducationalModal(false);
              break;
          }
        };
        
        // Handle SSE connection open
        eventSource.onopen = () => {
          console.log('✅ SSE connection opened successfully');
          console.log('   ReadyState:', eventSource.readyState);
          console.log('   URL:', eventSource.url);
          
          // Update educational content to show connection is established
          setEducationalContent({
            title: '🔌 Connection Established',
            description: 'Successfully connected to AI generation service. Starting analysis...',
            details: [
              '✅ SSE connection active',
              '🤖 AI service ready',
              '📊 Data processing initialized',
              '🎯 Strategy generation starting'
            ],
            insight: 'The connection is now established and AI analysis is beginning.',
            estimated_time: '2-3 minutes total'
          });
        };
        
      } else {
        setError('Failed to create strategy or get strategy ID for AI generation.');
        console.error('Failed to create strategy or get strategy ID for AI generation.');
        setShowEducationalModal(false);
      }
    } catch (error: any) {
      console.error('Error in SSE strategy generation:', error);
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
        <Alert
          severity="error"
          sx={{ mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
          action={
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button size="small" variant="outlined" onClick={() => autoPopulateFromOnboarding(true)} startIcon={<RefreshIcon />}>Retry</Button>
              <Button size="small" variant="contained" color="primary" onClick={() => setShowDataSourceTransparency(true)} startIcon={<InfoIcon />}>Why?</Button>
            </Box>
          }
        >
          <Box>
            <Typography variant="subtitle2">Real data required</Typography>
            <Typography variant="body2">{error || 'We could not auto-populate because required onboarding/analysis data is missing. Connect sources or complete onboarding, then retry.'}</Typography>
          </Box>
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
                <Box sx={{ mt: 1 }}>
                  <Grid container spacing={2}>
                  {STRATEGIC_INPUT_FIELDS
                    .filter(field => field.category === activeCategory)
                      .map((field, index) => {
                        // Determine grid size based on field type for better layout organization
                        const type = field.type;
                        const isWideField = type === 'json';
                        const isMediumField = type === 'multiselect' || type === 'select' || type === 'text';
                        const isCompactField = type === 'number' || type === 'boolean';
                        const forceFullWidth = field.id === 'content_budget' || field.id === 'team_size';

                        const gridMd = forceFullWidth ? 12 : (isWideField ? 12 : isMediumField ? 6 : 4);
                        const gridLg = forceFullWidth ? 12 : (isWideField ? 12 : isMediumField ? 6 : 4);
                        const gridSm = 12;
                      
                      return (
                          <Grid item xs={12} sm={gridSm} md={gridMd} lg={gridLg} key={field.id}>
                            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25, delay: index * 0.03 }}>
                          <StrategicInputField
                            fieldId={field.id}
                            value={formData[field.id]}
                            error={formErrors[field.id]}
                            autoPopulated={!!autoPopulatedFields[field.id]}
                            dataSource={dataSources[field.id]}
                            confidenceLevel={autoPopulatedFields[field.id] ? 0.8 : undefined}
                            dataQuality={autoPopulatedFields[field.id] ? 'High Quality' : undefined}
                            personalizationData={personalizationData[field.id]}
                            onChange={(value: any) => updateFormField(field.id, value)}
                            onValidate={() => validateFormField(field.id)}
                            onShowTooltip={() => setShowTooltip(field.id)}
                                onViewDataSource={() => setShowDataSourceTransparency(true)}
                                accentColorKey={getCategoryColor(activeCategory) as any}
                                isCompact={isCompactField}
                          />
                            </motion.div>
                        </Grid>
                      );
                    })}
                </Grid>
                </Box>

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

      {/* Educational Modal for Strategy Generation */}
      <Dialog
        open={showEducationalModal}
        onClose={() => setShowEducationalModal(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <SchoolIcon color="primary" />
            {educationalContent?.title || 'AI Strategy Generation'}
          </Box>
        </DialogTitle>
        <DialogContent>
          {educationalContent ? (
            <Box>
              {/* Progress Bar */}
              <Box sx={{ mb: 3 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Progress: {generationProgress}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Step {Math.ceil(generationProgress / 10)} of 10
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={generationProgress} 
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              {/* Educational Content */}
              <Typography variant="h6" gutterBottom color="primary">
                {educationalContent.title || 'AI Strategy Generation'}
              </Typography>
              
              {educationalContent.description && (
                <Typography variant="body1" paragraph>
                  {educationalContent.description}
                </Typography>
              )}

              {educationalContent.details && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    What's happening:
                  </Typography>
                  <List dense>
                    {educationalContent.details.map((detail: string, index: number) => (
                      <ListItem key={index} sx={{ py: 0.5 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <FiberManualRecordIcon sx={{ fontSize: 8 }} />
                        </ListItemIcon>
                        <ListItemText primary={detail} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              {educationalContent.insight && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    💡 Insight:
                  </Typography>
                  <Typography variant="body2">
                    {educationalContent.insight}
                  </Typography>
                </Box>
              )}

              {educationalContent.ai_prompt_preview && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'blue.50', borderRadius: 1 }}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    🤖 AI Prompt Preview:
                  </Typography>
                  <Typography variant="body2" fontFamily="monospace" fontSize="0.875rem">
                    {educationalContent.ai_prompt_preview}
                  </Typography>
                </Box>
              )}

              {educationalContent.estimated_time && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'orange.50', borderRadius: 1 }}>
                  <Typography variant="subtitle2" color="warning.main" gutterBottom>
                    ⏱️ Estimated Time:
                  </Typography>
                  <Typography variant="body2">
                    {educationalContent.estimated_time}
                  </Typography>
                </Box>
              )}

              {educationalContent.achievement && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'green.50', borderRadius: 1 }}>
                  <Typography variant="subtitle2" color="success.main" gutterBottom>
                    ✅ Achievement:
                  </Typography>
                  <Typography variant="body2">
                    {educationalContent.achievement}
                  </Typography>
                </Box>
              )}

              {educationalContent.next_step && (
                <Box sx={{ mb: 2, p: 2, bgcolor: 'purple.50', borderRadius: 1 }}>
                  <Typography variant="subtitle2" color="secondary.main" gutterBottom>
                    🔄 Next Step:
                  </Typography>
                  <Typography variant="body2">
                    {educationalContent.next_step}
                  </Typography>
                </Box>
              )}

              {/* Summary for completion */}
              {educationalContent.summary && (
                <Box sx={{ mt: 3, p: 2, bgcolor: 'primary.50', borderRadius: 1 }}>
                  <Typography variant="h6" gutterBottom color="primary">
                    🎉 Strategy Generation Summary
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Components:</strong> {educationalContent.summary.successful_components}/{educationalContent.summary.total_components}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Content Pieces:</strong> {educationalContent.summary.total_content_pieces}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Estimated ROI:</strong> {educationalContent.summary.estimated_roi}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Timeline:</strong> {educationalContent.summary.implementation_timeline}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              )}
            </Box>
          ) : (
            /* Loading state when educational content is not yet available */
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <CircularProgress sx={{ mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                🤖 AI-Powered Strategy Generation
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Initializing AI analysis and preparing educational content...
              </Typography>
              <Typography variant="body2" color="text.secondary">
                This may take a few moments as we set up the AI services.
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setShowEducationalModal(false)}
            disabled={generationProgress < 100}
          >
            {generationProgress < 100 ? 'Please wait...' : 'Close'}
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