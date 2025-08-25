import React, { useEffect, useState, useCallback } from 'react';
import { 
  Box, 
  Stepper, 
  Step, 
  StepLabel, 
  Button, 
  Typography, 
  Paper,
  LinearProgress,
  Fade,
  Slide,
  useTheme,
  useMediaQuery,
  IconButton,
  Tooltip,
  Container
} from '@mui/material';
import { 
  ArrowBack, 
  ArrowForward, 
  CheckCircle,
  HelpOutline,
  Close
} from '@mui/icons-material';
import { startOnboarding, getCurrentStep, setCurrentStep, getProgress } from '../../api/onboarding';
import ApiKeyStep from './ApiKeyStep';
import WebsiteStep from './WebsiteStep';
import ResearchStep from './ResearchStep';
import PersonalizationStep from './PersonalizationStep';
import SocialConnectionsStep from './SocialConnectionsStep';
import IntegrationsStep from './IntegrationsStep';
import FinalStep from './FinalStep';

const steps = [
  { label: 'API Keys', description: 'Connect your AI services', icon: '🔑' },
  { label: 'Website', description: 'Set up your website', icon: '🌐' },
  { label: 'Research', description: 'Configure research tools', icon: '🔍' },
  { label: 'Personalization', description: 'Customize your experience', icon: '⚙️' },
  { label: 'Social Media', description: 'Connect your platforms', icon: '📱' },
  { label: 'Integrations', description: 'Connect additional services', icon: '🔗' },
  { label: 'Finish', description: 'Complete setup', icon: '✅' }
];

interface WizardProps {
  onComplete?: () => void;
}

interface StepHeaderContent {
  title: string;
  description: string;
}

const Wizard: React.FC<WizardProps> = ({ onComplete }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(true);
  const [progress, setProgressState] = useState(0);
  const [direction, setDirection] = useState<'left' | 'right'>('right');
  const [showHelp, setShowHelp] = useState(false);
  const [showProgressMessage, setShowProgressMessage] = useState(false);
  const [progressMessage, setProgressMessage] = useState('');
  const [stepHeaderContent, setStepHeaderContent] = useState<StepHeaderContent>({
    title: steps[0].label,
    description: steps[0].description
  });
  
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  useEffect(() => {
    console.log('Wizard: Component mounted');
    const init = async () => {
      try {
        setLoading(true);
        console.log('Wizard: Starting initialization...');
        
        // Check if there's existing progress first
        const stepResponse = await getCurrentStep();
        console.log('Wizard: Backend returned step:', stepResponse.step);
        
        // Only start onboarding if we're at step 1 (no progress)
        if (stepResponse.step === 1) {
          console.log('Wizard: No existing progress, starting new onboarding');
          await startOnboarding();
        } else {
          console.log('Wizard: Existing progress found, continuing from step:', stepResponse.step);
        }
        
        // Get the current step and progress
        const finalStepResponse = await getCurrentStep();
        const progressResponse = await getProgress();
        console.log('Wizard: Final step:', finalStepResponse.step);
        console.log('Wizard: Backend returned progress:', progressResponse.progress);
        console.log('Wizard: Setting activeStep to:', finalStepResponse.step - 1);
        setActiveStep(finalStepResponse.step - 1);
        setProgressState(progressResponse.progress);
        console.log('Wizard: Initialization complete');
      } catch (error) {
        console.error('Error initializing onboarding:', error);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const handleNext = async () => {
    console.log('Wizard: handleNext called');
    console.log('Wizard: Current activeStep:', activeStep);
    console.log('Wizard: Steps length:', steps.length);
    
    setDirection('right');
    const nextStep = activeStep + 1;
    
    console.log('Wizard: Next step will be:', nextStep);
    
    // Show progress message
    const newProgress = ((nextStep + 1) / steps.length) * 100;
    setProgressMessage(`Your data is saved, moving to the next step. Progress is ${Math.round(newProgress)}%`);
    setShowProgressMessage(true);
    
    // Hide message after 3 seconds
    setTimeout(() => {
      setShowProgressMessage(false);
    }, 3000);
    
    // Complete the current step (activeStep + 1 because steps are 1-indexed)
    const currentStepNumber = activeStep + 1;
    console.log('Wizard: Completing current step:', currentStepNumber);
    await setCurrentStep(currentStepNumber);
    
    // Check what step the backend thinks we should be on after completion
    console.log('Wizard: Checking backend step after completion...');
    const stepResponse = await getCurrentStep();
    console.log('Wizard: Backend says current step should be:', stepResponse.step);
    
    setActiveStep(nextStep);
    console.log('Wizard: Setting activeStep to:', nextStep);
    
    // Update progress
    setProgressState(newProgress);
    
    // If this is the final step, call onComplete
    if (nextStep === steps.length - 1) {
      console.log('Wizard: This is the final step, calling onComplete');
      onComplete?.();
    } else {
      console.log('Wizard: Not the final step, continuing to next step');
    }
  };

  const handleBack = async () => {
    setDirection('left');
    const prevStep = activeStep - 1;
    setActiveStep(prevStep);
    await setCurrentStep(prevStep + 1);
    
    // Update progress
    const newProgress = ((prevStep + 1) / steps.length) * 100;
    setProgressState(newProgress);
  };

  const handleStepClick = (stepIndex: number) => {
    if (stepIndex <= activeStep) {
      setDirection(stepIndex > activeStep ? 'right' : 'left');
      setActiveStep(stepIndex);
      setCurrentStep(stepIndex + 1);
    }
  };

  const updateHeaderContent = useCallback((content: StepHeaderContent) => {
    setStepHeaderContent(content);
  }, []);

  const handleComplete = async () => {
    console.log('Wizard: handleComplete called - completing onboarding');
    try {
      // Call onComplete to notify parent component
      onComplete?.();
    } catch (error) {
      console.error('Error completing onboarding:', error);
    }
  };

  const renderStepContent = (step: number) => {
    const stepComponents = [
      <ApiKeyStep key="api-keys" onContinue={handleNext} updateHeaderContent={updateHeaderContent} />,
      <WebsiteStep key="website" onContinue={handleNext} updateHeaderContent={updateHeaderContent} />,
      <ResearchStep key="research" onContinue={handleNext} updateHeaderContent={updateHeaderContent} />,
      <PersonalizationStep key="personalization" onContinue={handleNext} updateHeaderContent={updateHeaderContent} />,
      <SocialConnectionsStep key="social-connections" onContinue={handleNext} updateHeaderContent={updateHeaderContent} />,
      <IntegrationsStep key="integrations" onContinue={handleNext} updateHeaderContent={updateHeaderContent} />,
      <FinalStep key="final" onContinue={handleComplete} updateHeaderContent={updateHeaderContent} />
    ];

    return (
      <Slide direction={direction} in={true} mountOnEnter unmountOnExit>
        <Box sx={{ minHeight: '500px', display: 'flex', flexDirection: 'column' }}>
          {stepComponents[step]}
        </Box>
      </Slide>
    );
  };

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}
      >
        <Fade in={true}>
          <Paper
            elevation={24}
            sx={{
              p: 4,
              borderRadius: 3,
              background: 'rgba(255, 255, 255, 0.98)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              maxWidth: 400,
              width: '100%',
            }}
          >
            <Typography variant="h5" align="center" gutterBottom sx={{ fontWeight: 600 }}>
              Setting up your workspace...
            </Typography>
            <LinearProgress 
              sx={{ 
                mt: 3, 
                height: 8, 
                borderRadius: 4,
                backgroundColor: 'rgba(0,0,0,0.08)',
                '& .MuiLinearProgress-bar': {
                  borderRadius: 4,
                  background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                }
              }} 
            />
          </Paper>
        </Fade>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: { xs: 2, md: 4 },
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%)',
          pointerEvents: 'none',
        }
      }}
    >
      <Paper
        elevation={24}
        sx={{
          maxWidth: { xs: '100%', md: '1200px' },
          width: '100%',
          borderRadius: 4,
          overflow: 'hidden',
          background: 'rgba(255, 255, 255, 0.98)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          position: 'relative',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        }}
      >
        {/* Header with Stepper */}
        <Box
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            p: { xs: 3, md: 4 },
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%)',
              pointerEvents: 'none',
            }
          }}
        >
          {/* Progress Message */}
          {showProgressMessage && (
            <Fade in={showProgressMessage}>
              <Box
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  background: 'rgba(16, 185, 129, 0.9)',
                  color: 'white',
                  p: 2,
                  textAlign: 'center',
                  zIndex: 10,
                  backdropFilter: 'blur(10px)',
                  borderBottom: '1px solid rgba(255, 255, 255, 0.2)'
                }}
              >
                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                  {progressMessage}
                </Typography>
              </Box>
            </Fade>
          )}
          
          {/* Top Row - Title and Actions */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3, position: 'relative', zIndex: 1 }}>
            <Box sx={{ flex: 1 }} />
            <Box sx={{ flex: 2, textAlign: 'center' }}>
              <Typography variant="h4" sx={{ fontWeight: 700, letterSpacing: '-0.025em' }}>
                {stepHeaderContent.title}
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 1, flex: 1, justifyContent: 'flex-end' }}>
              <Tooltip title="Get Help" arrow>
                <IconButton 
                  onClick={() => setShowHelp(!showHelp)}
                  sx={{ 
                    color: 'white', 
                    bgcolor: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    '&:hover': {
                      bgcolor: 'rgba(255, 255, 255, 0.2)',
                    }
                  }}
                >
                  <HelpOutline />
                </IconButton>
              </Tooltip>
              <Tooltip title="Skip for now" arrow>
                <IconButton 
                  sx={{ 
                    color: 'white',
                    bgcolor: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    '&:hover': {
                      bgcolor: 'rgba(255, 255, 255, 0.2)',
                    }
                  }}
                >
                  <Close />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>
          
          {/* Progress Bar */}
          <Box sx={{ mb: 3, position: 'relative', zIndex: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography variant="body2" sx={{ opacity: 0.9, fontWeight: 500 }}>
                Setup Progress
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9, fontWeight: 600 }}>
                {Math.round(progress)}% Complete
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{
                height: 8,
                borderRadius: 4,
                backgroundColor: 'rgba(255,255,255,0.2)',
                '& .MuiLinearProgress-bar': {
                  borderRadius: 4,
                  background: 'linear-gradient(90deg, #fff 0%, #f8fafc 100%)',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                }
              }}
            />
          </Box>

          {/* Stepper in Header */}
          <Box sx={{ position: 'relative', zIndex: 1 }}>
            <Stepper 
              activeStep={activeStep} 
              alternativeLabel={!isMobile}
              sx={{
                '& .MuiStepLabel-root': {
                  cursor: 'pointer',
                },
                '& .MuiStepLabel-label': {
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  color: 'white',
                },
                '& .MuiStepLabel-labelContainer': {
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                },
                '& .MuiStepLabel-label.Mui-completed': {
                  color: 'rgba(255, 255, 255, 0.9)',
                },
                '& .MuiStepLabel-label.Mui-active': {
                  color: 'white',
                },
                '& .MuiStepLabel-label.Mui-disabled': {
                  color: 'rgba(255, 255, 255, 0.6)',
                },
              }}
            >
              {steps.map((step, index) => (
                <Step key={step.label}>
                  <StepLabel
                    onClick={() => handleStepClick(index)}
                    sx={{
                      cursor: index <= activeStep ? 'pointer' : 'default',
                      '& .MuiStepLabel-iconContainer': {
                        background: index <= activeStep 
                          ? 'rgba(255, 255, 255, 0.2)'
                          : 'rgba(255, 255, 255, 0.1)',
                        borderRadius: '50%',
                        width: 40,
                        height: 40,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: index <= activeStep ? 'white' : 'rgba(255, 255, 255, 0.6)',
                        fontSize: '1.2rem',
                        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                        boxShadow: index <= activeStep 
                          ? '0 4px 12px rgba(255, 255, 255, 0.2)'
                          : 'none',
                        '&:hover': {
                          transform: index <= activeStep ? 'scale(1.05)' : 'none',
                          boxShadow: index <= activeStep 
                            ? '0 6px 16px rgba(255, 255, 255, 0.3)'
                            : 'none',
                        }
                      },
                    }}
                  >
                    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5 }}>
                      <Typography variant="h6" sx={{ mb: 0.5 }}>
                        {step.icon}
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600, textAlign: 'center' }}>
                        {step.label}
                      </Typography>
                    </Box>
                  </StepLabel>
                </Step>
              ))}
            </Stepper>
          </Box>
        </Box>

        {/* Content */}
        <Box sx={{ p: { xs: 2, md: 3 }, pt: 2 }}>
          <Fade in={true} timeout={400}>
            <Box>
              {renderStepContent(activeStep)}
            </Box>
          </Fade>
        </Box>

        {/* Navigation */}
        <Box
          sx={{
            p: { xs: 2, md: 3 },
            pt: 2,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderTop: '1px solid rgba(0,0,0,0.08)',
            background: 'rgba(0,0,0,0.02)',
          }}
        >
          <Button
            variant="outlined"
            onClick={handleBack}
            disabled={activeStep === 0}
            startIcon={<ArrowBack />}
            sx={{
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 600,
              borderColor: 'rgba(0,0,0,0.2)',
              color: 'text.primary',
              '&:hover': {
                borderColor: 'rgba(0,0,0,0.4)',
                background: 'rgba(0,0,0,0.04)',
              },
              '&:disabled': {
                borderColor: 'rgba(0,0,0,0.1)',
                color: 'rgba(0,0,0,0.3)',
              }
            }}
          >
            Back
          </Button>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2" sx={{ opacity: 0.7, fontWeight: 500 }}>
              Step {activeStep + 1} of {steps.length}
            </Typography>
            {activeStep === steps.length - 1 && (
              <CheckCircle sx={{ color: 'success.main', fontSize: 20 }} />
            )}
          </Box>

          <Button
            variant="contained"
            onClick={handleNext}
            disabled={activeStep === steps.length - 1}
            endIcon={activeStep === steps.length - 1 ? <CheckCircle /> : <ArrowForward />}
            sx={{
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 600,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
              '&:hover': {
                background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                transform: 'translateY(-1px)',
                boxShadow: '0 6px 16px rgba(102, 126, 234, 0.4)',
              },
              '&:disabled': {
                background: 'rgba(0,0,0,0.1)',
                color: 'rgba(0,0,0,0.4)',
                boxShadow: 'none',
                transform: 'none',
              }
            }}
          >
            {activeStep === steps.length - 1 ? 'Complete Setup' : 'Continue'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default Wizard; 