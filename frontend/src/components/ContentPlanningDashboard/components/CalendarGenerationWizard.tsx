import React, { useMemo, useRef, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Button,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Alert,
  Chip
} from '@mui/material';
import {
  DataUsage as DataUsageIcon,
  CalendarToday as CalendarIcon,
  Campaign as CampaignIcon
} from '@mui/icons-material';

// Import modular step components
import {
  CalendarConfigurationStep,
  GenerateCalendarStep,
  useCalendarWizardState,
  WizardErrorBoundary,
  CalendarGenerationLoading
} from './CalendarWizardSteps';

// Import types
import { type CalendarConfig } from './CalendarWizardSteps/types';

interface CalendarGenerationWizardProps {
  userData: any;
  onGenerateCalendar: (calendarConfig: any) => void;
  loading?: boolean;
  strategyContext?: any;
  fromStrategyActivation?: boolean;
}

const CalendarGenerationWizard: React.FC<CalendarGenerationWizardProps> = ({
  userData,
  onGenerateCalendar,
  loading = false,
  strategyContext,
  fromStrategyActivation = false
}) => {
  // SIMPLIFIED CALENDAR WIZARD - Focused on calendar-specific inputs only
  // Strategy context is used internally during generation, not for mapping
  
  console.log('🔍 CalendarGenerationWizard: Starting calendar wizard', { 
    fromStrategyActivation, 
    hasStrategyContext: !!strategyContext
  });

  // Use enhanced state management with calendar-specific config
  const [state, actions] = useCalendarWizardState(onGenerateCalendar);
  const { 
    activeStep, 
    calendarConfig,
    validationErrors, 
    isLoading, 
    error, 
    isGenerating, 
    generationProgress 
  } = state;

  // Streamlined 2 steps for calendar-specific inputs
  const steps = [
    {
      label: 'Calendar Configuration',
      icon: <CalendarIcon />,
      description: 'Configure all your calendar settings and preferences'
    },
    {
      label: 'Generate Calendar',
      icon: <CampaignIcon />,
      description: 'Review and generate your optimized content calendar'
    }
  ];

  const handleNext = useCallback(() => {
    if (actions.validateStep(activeStep)) {
      actions.setActiveStep(activeStep + 1);
    }
  }, [actions, activeStep]);

  const handleBack = useCallback(() => {
    actions.setActiveStep(activeStep - 1);
  }, [actions, activeStep]);

  // Create stable callback for generate calendar
  const handleGenerateCalendar = useCallback(() => {
    onGenerateCalendar(calendarConfig);
  }, [onGenerateCalendar, calendarConfig]);

  // Show loading state if generating
  if (isGenerating) {
    return (
      <CalendarGenerationLoading 
        progress={generationProgress} 
        error={error || undefined}
      />
    );
  }

  // Show error state if there's an error
  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button 
          variant="contained" 
          onClick={actions.resetWizard}
          sx={{ mr: 1 }}
        >
          Reset Wizard
        </Button>
      </Box>
    );
  }

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <CalendarConfigurationStep
            calendarConfig={calendarConfig}
            onConfigUpdate={actions.updateCalendarConfig}
            strategyContext={strategyContext}
            isFromStrategyActivation={fromStrategyActivation}
          />
        );
      case 1:
        return (
          <GenerateCalendarStep
            calendarConfig={calendarConfig}
            onGenerateCalendar={handleGenerateCalendar}
            loading={loading}
            strategyContext={strategyContext}
            isFromStrategyActivation={fromStrategyActivation}
          />
        );
      default:
        return null;
    }
  };

  return (
    <WizardErrorBoundary>
      <Box sx={{ p: 3 }}>
        {/* Simplified header */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Content Calendar Wizard
          </Typography>
          {fromStrategyActivation && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
              <Chip 
                label="Strategy Context Available"
                color="success"
                variant="outlined"
              />
            </Box>
          )}
        </Box>

        <Stepper activeStep={activeStep} orientation="vertical">
          {steps.map((step, index) => (
            <Step key={step.label}>
              <StepLabel
                icon={step.icon}
                optional={index === steps.length - 1 ? (
                  <Typography variant="caption">Generate Calendar</Typography>
                ) : null}
              >
                {step.label}
              </StepLabel>
              <StepContent>
                <Box sx={{ mb: 2 }}>
                  {renderStepContent(index)}
                  <Box sx={{ mt: 2 }}>
                    <Button
                      variant="contained"
                      onClick={index === steps.length - 1 ? handleGenerateCalendar : handleNext}
                      sx={{ mr: 1 }}
                      disabled={loading || !actions.canProceedToStep(index + 1)}
                    >
                      {index === steps.length - 1 ? 'Generate Calendar' : 'Continue'}
                    </Button>
                    <Button
                      disabled={index === 0}
                      onClick={handleBack}
                      sx={{ mr: 1 }}
                    >
                      Back
                    </Button>
                  </Box>
                </Box>
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </Box>
    </WizardErrorBoundary>
  );
};

export default CalendarGenerationWizard;
