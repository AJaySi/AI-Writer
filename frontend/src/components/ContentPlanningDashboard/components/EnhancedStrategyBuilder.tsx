import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  StepContent,
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
  Badge
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
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { useEnhancedStrategyStore, STRATEGIC_INPUT_FIELDS } from '../../../stores/enhancedStrategyStore';
import StrategicInputField from './StrategicInputField';
import EnhancedTooltip from './EnhancedTooltip';
import CompletionTracker from './CompletionTracker';
import AIRecommendationsPanel from './AIRecommendationsPanel';
import DataSourceTransparency from './/DataSourceTransparency';

const EnhancedStrategyBuilder: React.FC = () => {
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
    setAIGenerating
  } = useEnhancedStrategyStore();

  const [showTooltip, setShowTooltip] = useState<string | null>(null);
  const [autoPopulateAttempted, setAutoPopulateAttempted] = useState(false);

  // Auto-populate from onboarding on first load
  useEffect(() => {
    if (!autoPopulateAttempted) {
      autoPopulateFromOnboarding();
      setAutoPopulateAttempted(true);
    }
  }, [autoPopulateAttempted, autoPopulateFromOnboarding]);

  const handleStepComplete = () => {
    const currentStepData = disclosureSteps[currentStep];
    if (currentStepData) {
      // Validate all fields in current step
      const stepFields = currentStepData.fields;
      const isValid = stepFields.every(fieldId => validateFormField(fieldId));
      
      if (isValid) {
        completeStep(currentStepData.id);
        
        // Move to next step if available
        const nextStep = getNextStep();
        if (nextStep) {
          setCurrentStep(currentStep + 1);
        }
      }
    }
  };

  const handleNextStep = () => {
    const nextStep = getNextStep();
    if (nextStep) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePreviousStep = () => {
    const prevStep = getPreviousStep();
    if (prevStep) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSaveStrategy = async () => {
    if (validateAllFields()) {
      const completionStats = getCompletionStats();
      const strategyData = {
        ...formData,
        completion_percentage: completionStats.completion_percentage,
        user_id: 1, // This would come from auth context
        name: formData.name || 'Enhanced Content Strategy',
        industry: formData.industry || 'General'
      };
      
      await createEnhancedStrategy(strategyData);
    }
  };

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
          
          console.log('Strategy data to create:', strategyData);
          
          // Save the strategy first and get the created strategy
          const newStrategy = await createEnhancedStrategy(strategyData);
          console.log('Created strategy:', newStrategy);
          
          if (newStrategy && newStrategy.id) {
            console.log('Generating AI recommendations for strategy ID:', newStrategy.id);
            // Now generate AI recommendations with the new strategy ID
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
            console.error('Failed to create strategy or get strategy ID');
            setError('Failed to create strategy. Please try again.');
          }
        } else {
          console.log('Form validation failed');
          setError('Please complete all required fields before creating strategy');
        }
      }
    } catch (error: any) {
      console.error('Error creating strategy:', error);
      setError(error.message || 'Failed to create strategy');
    } finally {
      setAIGenerating(false);
    }
  };

  const getStepIcon = (stepId: string) => {
    const icons = {
      business_context: <BusinessIcon />,
      audience_intelligence: <PeopleIcon />,
      competitive_intelligence: <TrendingUpIcon />,
      content_strategy: <ContentIcon />,
      performance_analytics: <AnalyticsIcon />
    };
    return icons[stepId as keyof typeof icons] || <BusinessIcon />;
  };

  const getStepColor = (stepId: string) => {
    if (completedSteps.includes(stepId)) return 'success';
    if (currentStep === disclosureSteps.findIndex(s => s.id === stepId)) return 'primary';
    return 'default';
  };

  const completionStats = getCompletionStats();
  const completionPercentage = calculateCompletionPercentage();

  // Debug logging
  console.log('Completion percentage:', completionPercentage);
  console.log('Form data keys:', Object.keys(formData));
  console.log('Required fields:', STRATEGIC_INPUT_FIELDS.filter(f => f.required).map(f => f.id));
  console.log('Filled required fields:', STRATEGIC_INPUT_FIELDS.filter(f => f.required && formData[f.id]).map(f => f.id));

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Enhanced Strategy Builder
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Build a comprehensive content strategy with 30+ strategic inputs
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <CompletionTracker 
            completionPercentage={completionPercentage}
            completionStats={completionStats}
          />
          
          <MuiTooltip 
            title={completionPercentage < 20 ? `Complete at least 20% of the form (currently ${Math.round(completionPercentage)}%)` : 'Create a comprehensive content strategy with AI insights'}
            placement="top"
          >
            <span>
              <Button
                variant="outlined"
                startIcon={<AutoAwesomeIcon />}
                onClick={handleCreateStrategy}
                disabled={aiGenerating || completionPercentage < 20}
              >
                {aiGenerating ? 'Creating...' : 'Create Strategy'}
              </Button>
            </span>
          </MuiTooltip>
          
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSaveStrategy}
            disabled={saving || completionPercentage < 30}
          >
            {saving ? 'Saving...' : 'Save Strategy'}
          </Button>
        </Box>
      </Box>

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

      {/* Auto-population Status */}
      {autoPopulatedFields && Object.keys(autoPopulatedFields).length > 0 && (
        <Alert 
          severity="info" 
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={autoPopulateFromOnboarding}>
              <RefreshIcon />
            </Button>
          }
        >
          {autoPopulatedFields && Object.keys(autoPopulatedFields).length} fields auto-populated from onboarding data
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Main Strategy Builder */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            {/* Progress Indicator */}
            <Box sx={{ mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Strategy Completion
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {Math.round(calculateCompletionPercentage?.() || 0)}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={calculateCompletionPercentage?.() || 0} 
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>

            {/* Stepper */}
            <Stepper activeStep={currentStep} orientation="vertical">
              {disclosureSteps.map((step, index) => (
                <Step key={step.id} completed={completedSteps.includes(step.id)}>
                  <StepLabel
                    icon={
                      <Badge
                        badgeContent={step.fields.length}
                        color={getStepColor(step.id)}
                        sx={{ '& .MuiBadge-badge': { fontSize: '0.75rem' } }}
                      >
                        {getStepIcon(step.id)}
                      </Badge>
                    }
                    optional={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {completedSteps.includes(step.id) && (
                          <CheckCircleIcon color="success" fontSize="small" />
                        )}
                        <Chip 
                          label={`${step.fields.length} fields`} 
                          size="small" 
                          variant="outlined"
                        />
                      </Box>
                    }
                  >
                    <Typography variant="h6">{step.title}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {step.description}
                    </Typography>
                  </StepLabel>
                  
                  <StepContent>
                    <Box sx={{ mt: 2 }}>
                      {/* Step Fields */}
                      <Grid container spacing={2}>
                        {step.fields.map((fieldId) => (
                          <Grid item xs={12} key={fieldId}>
                            <StrategicInputField
                              fieldId={fieldId}
                              value={formData[fieldId]}
                              error={formErrors[fieldId]}
                              autoPopulated={!!autoPopulatedFields[fieldId]}
                              dataSource={dataSources[fieldId]}
                              onChange={(value: any) => updateFormField(fieldId, value)}
                              onValidate={() => validateFormField(fieldId)}
                              onShowTooltip={() => setShowTooltip(fieldId)}
                            />
                          </Grid>
                        ))}
                      </Grid>

                      {/* Step Actions */}
                      <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                        <Button
                          variant="contained"
                          onClick={handleStepComplete}
                          disabled={!step.fields.every(fieldId => formData[fieldId])}
                          endIcon={<ArrowForwardIcon />}
                        >
                          {getNextStep() ? 'Complete & Continue' : 'Complete Strategy'}
                        </Button>
                        
                        {getPreviousStep() && (
                          <Button
                            variant="outlined"
                            onClick={handlePreviousStep}
                            startIcon={<ArrowBackIcon />}
                          >
                            Previous Step
                          </Button>
                        )}
                        
                        {getNextStep() && (
                          <Button
                            variant="outlined"
                            onClick={handleNextStep}
                            disabled={!canProceedToStep(getNextStep()!.id)}
                            endIcon={<ArrowForwardIcon />}
                          >
                            Skip to Next
                          </Button>
                        )}
                      </Box>
                    </Box>
                  </StepContent>
                </Step>
              ))}
            </Stepper>
          </Paper>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {/* Data Source Transparency */}
            <DataSourceTransparency 
              autoPopulatedFields={autoPopulatedFields}
              dataSources={dataSources}
            />

            {/* AI Recommendations Panel */}
            <AIRecommendationsPanel 
              aiGenerating={aiGenerating}
              onGenerateRecommendations={handleCreateStrategy}
            />

            {/* Quick Actions */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quick Actions
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={resetForm}
                    disabled={loading}
                  >
                    Reset Form
                  </Button>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={autoPopulateFromOnboarding}
                    disabled={loading}
                  >
                    Re-populate from Onboarding
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Box>
        </Grid>
      </Grid>

      {/* Enhanced Tooltip */}
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

export default EnhancedStrategyBuilder; 