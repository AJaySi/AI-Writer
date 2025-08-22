import { SxProps, Theme } from '@mui/material/styles';

/**
 * Styles for CalendarGenerationModal Component
 * All styling logic extracted for maintainability and reusability
 */

// Dialog and Layout Styles
export const dialogStyles = {
  paper: {
    height: '90vh',
    maxHeight: '90vh'
  }
};

export const contentContainerStyles: SxProps<Theme> = {
  p: 2
};

// Progress Bar Styles
export const progressBarContainerStyles: SxProps<Theme> = {
  flexGrow: 1, 
  position: 'relative'
};

export const progressBarStyles: SxProps<Theme> = {
  height: 8, 
  borderRadius: 4,
  backgroundColor: 'grey.200',
  '& .MuiLinearProgress-bar': {
    borderRadius: 4,
    background: 'linear-gradient(90deg, #1976d2 0%, #42a5f5 100%)',
    transition: 'transform 0.8s ease-in-out'
  }
};

export const stepProgressBarStyles: SxProps<Theme> = {
  height: 10, 
  borderRadius: 5,
  backgroundColor: 'grey.200',
  '& .MuiLinearProgress-bar': {
    borderRadius: 5,
    background: 'linear-gradient(90deg, #1976d2 0%, #42a5f5 100%)',
    transition: 'transform 0.6s ease-in-out'
  }
};

// Step Indicator Styles
export const getStepIndicatorStyles = (currentStep: number, step: number): SxProps<Theme> => ({
  p: 1,
  borderRadius: 1,
  backgroundColor: currentStep === step ? 'primary.light' : 'grey.100',
  color: currentStep === step ? 'primary.contrastText' : 'text.secondary',
  transition: 'all 0.3s ease',
  cursor: 'pointer'
});

// Step Card Styles
export const getStepCardStyles = (currentStep: number, step: number): SxProps<Theme> => ({
  p: 2,
  backgroundColor: currentStep === step ? 'primary.light' : 'grey.50',
  borderColor: currentStep === step ? 'primary.main' : 'grey.300',
  transition: 'all 0.3s ease',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '100%',
    background: currentStep === step 
      ? 'linear-gradient(90deg, transparent, rgba(25, 118, 210, 0.1), transparent)'
      : 'none',
    transition: 'left 0.6s ease-in-out'
  },
  '&:hover::before': {
    left: '100%'
  }
});

// Step Circle Styles
export const stepCircleBaseStyles = {
  width: 32,
  height: 32,
  borderRadius: '50%',
  color: 'white',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: '0.875rem',
  fontWeight: 'bold'
};

export const getStepCircleColor = (currentStep: number, step: number): string => {
  if (currentStep > step) return '#4caf50';
  if (currentStep === step) return '#1976d2';
  return '#9e9e9e';
};

// Tab Button Styles
export const tabButtonStyles: SxProps<Theme> = {
  transition: 'all 0.3s ease',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '100%',
    background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent)',
    transition: 'left 0.5s'
  },
  '&:hover::before': {
    left: '100%'
  }
};

// Activity Indicator Styles
export const activityIndicatorStyles = {
  width: 8,
  height: 8,
  borderRadius: '50%',
  backgroundColor: '#1976d2',
  marginTop: 8,
  flexShrink: 0
};

// Quality Score Styles
export const qualityScoreContainerStyles: SxProps<Theme> = {
  width: 80,
  height: 80,
  borderRadius: '50%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  position: 'relative'
};

export const getQualityScoreBackground = (score: number): string => {
  const color = score >= 0.9 ? '#4caf50' : score >= 0.8 ? '#ff9800' : '#f44336';
  return `conic-gradient(${color} 0deg, ${score * 360}deg, #e0e0e0 ${score * 360}deg, 360deg)`;
};

export const qualityScoreInnerStyles: SxProps<Theme> = {
  width: 60,
  height: 60,
  borderRadius: '50%',
  backgroundColor: 'white',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontWeight: 'bold',
  fontSize: '1.2rem'
};

// Data Source Card Styles
export const dataSourceCardStyles: SxProps<Theme> = {
  p: 2
};

export const dataSourceIconStyles = {
  width: 32,
  height: 32,
  borderRadius: '50%',
  color: 'white',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: '0.875rem'
};

export const getDataSourceIconColor = (type: string): string => {
  switch (type) {
    case 'strategy':
      return '#4caf50'; // success.main
    case 'onboarding':
      return '#2196f3'; // info.main
    case 'ai':
      return '#1976d2'; // primary.main
    case 'performance':
      return '#9c27b0'; // secondary.main
    default:
      return '#757575'; // grey
  }
};

// Quality Metrics Styles
export const qualityMetricsContainerStyles: SxProps<Theme> = {
  textAlign: 'center',
  p: 2
};

export const getMetricColor = (label: string): string => {
  switch (label) {
    case 'Overall Data Quality':
      return '#4caf50'; // success.main
    case 'Data Completeness':
      return '#2196f3'; // info.main
    case 'Data Freshness':
      return '#1976d2'; // primary.main
    default:
      return '#757575';
  }
};

// Step Results Styles
export const stepResultsCardStyles: SxProps<Theme> = {
  p: 2
};

export const stepResultsHeaderStyles: SxProps<Theme> = {
  width: 40,
  height: 40,
  borderRadius: '50%',
  backgroundColor: 'primary.main',
  color: 'white',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontWeight: 'bold'
};

export const stepResultsContentStyles: SxProps<Theme> = {
  backgroundColor: 'grey.50',
  p: 2,
  borderRadius: 1
};

// Loading State Styles
export const loadingContainerStyles: SxProps<Theme> = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '400px'
};

export const loadingContentStyles: SxProps<Theme> = {
  textAlign: 'center'
};

// Animation Constants
export const animationDurations = {
  fast: 0.3,
  medium: 0.5,
  slow: 0.8,
  extraSlow: 1.0
};

export const animationEasing = {
  easeOut: "easeOut" as const,
  easeInOut: "easeInOut" as const,
  linear: "linear" as const
};

export const springConfig = {
  type: "spring" as const,
  stiffness: 200,
  damping: 10
};

export const staggerDelay = 0.1;
export const cardStaggerDelay = 0.2;

// Motion Variants
export const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 }
};

export const fadeInLeft = {
  initial: { opacity: 0, x: -20, scale: 0.95 },
  animate: { opacity: 1, x: 0, scale: 1 },
  exit: { opacity: 0, x: 50, scale: 0.95 }
};

export const scaleIn = {
  initial: { opacity: 0, scale: 0.8 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.8 }
};

export const slideInStaggered = {
  initial: { opacity: 0, y: 50, scale: 0.8 },
  animate: { opacity: 1, y: 0, scale: 1 },
  exit: { opacity: 0, y: -50, scale: 0.8 }
};

// Hover and Interaction Styles
export const hoverLift = {
  scale: 1.02,
  y: -5
};

export const hoverScale = {
  scale: 1.05
};

export const tapScale = {
  scale: 0.95
};

// Pulse Animation Config
export const pulseAnimation = {
  scale: [1, 1.1, 1],
  boxShadow: [
    "0 0 0 0 rgba(76, 175, 80, 0.4)",
    "0 0 0 10px rgba(76, 175, 80, 0)",
    "0 0 0 0 rgba(76, 175, 80, 0)"
  ]
};

export const smallPulseAnimation = {
  scale: [1, 1.1, 1],
  boxShadow: [
    "0 0 0 0 rgba(76, 175, 80, 0.4)",
    "0 0 0 6px rgba(76, 175, 80, 0)",
    "0 0 0 0 rgba(76, 175, 80, 0)"
  ]
};

// Color Animation Config
export const colorPulseAnimation = {
  scale: [1, 1.2, 1],
  backgroundColor: ['#1976d2', '#42a5f5', '#1976d2']
};

// Progress Animation Config
export const progressFillAnimation = {
  initial: { scaleX: 0 },
  animate: (progress: number) => ({ scaleX: progress / 100 }),
  transition: { duration: animationDurations.slow, ease: animationEasing.easeOut }
};

export const progressOverlayStyles = {
  position: 'absolute' as const,
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  background: 'linear-gradient(90deg, #4caf50 0%, #8bc34a 100%)',
  borderRadius: 4,
  transformOrigin: 'left' as const
};

export const stepProgressOverlayStyles = {
  position: 'absolute' as const,
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  background: 'linear-gradient(90deg, #4caf50 0%, #8bc34a 100%)',
  borderRadius: 5,
  transformOrigin: 'left' as const
};
