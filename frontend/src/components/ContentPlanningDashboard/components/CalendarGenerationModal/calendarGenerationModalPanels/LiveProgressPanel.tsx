import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  LinearProgress,
  Chip,
  CircularProgress,
  Card
} from '@mui/material';
import { motion } from 'framer-motion';

// Import styles
import {
  progressBarContainerStyles,
  stepProgressBarStyles,
  getStepCardStyles,
  stepCircleBaseStyles,
  getStepCircleColor,
  activityIndicatorStyles,
  animationDurations,
  animationEasing,
  springConfig,
  staggerDelay,
  smallPulseAnimation,
  colorPulseAnimation,
  stepProgressOverlayStyles
} from '../CalendarGenerationModal.styles';

// Types
interface QualityScores {
  overall: number;
  step1: number;
  step2: number;
  step3: number;
  step4: number;
  step5: number;
  step6: number;
  step7: number;
  step8: number;
  step9: number;
  step10: number;
  step11: number;
  step12: number;
}

interface CalendarGenerationProgress {
  status: 'initializing' | 'step1' | 'step2' | 'step3' | 'completed' | 'error';
  currentStep: number;
  stepProgress: number;
  overallProgress: number;
  stepResults: Record<number, any>;
  qualityScores: QualityScores;
  transparencyMessages: string[];
  educationalContent: any[];
  errors: any[];
  warnings: any[];
}

interface LiveProgressPanelProps {
  progress: CalendarGenerationProgress;
  isPolling: boolean;
}

const LiveProgressPanel: React.FC<LiveProgressPanelProps> = ({ progress, isPolling }) => (
  <Paper elevation={1} sx={{ p: 2 }}>
    <Typography variant="h6" gutterBottom>
      Live Progress
    </Typography>
    
    {/* Current Status with Enhanced Animation */}
    <Box mb={3}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box display="flex" alignItems="center" gap={2} mb={2}>
          <motion.div
            animate={{ 
              rotate: isPolling ? 360 : 0,
              scale: isPolling ? [1, 1.2, 1] : 1
            }}
            transition={{ 
              rotate: { duration: 2, repeat: Infinity, ease: "linear" },
              scale: { duration: 1, repeat: Infinity, ease: "easeInOut" }
            }}
          >
            <CircularProgress size={20} />
          </motion.div>
          <motion.div
            key={progress.status}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Typography variant="subtitle1">
              Current Step: {progress.currentStep} - {progress.status}
            </Typography>
          </motion.div>
        </Box>
      </motion.div>
      
      <Box display="flex" alignItems="center" gap={2}>
        <Typography variant="body2" color="text.secondary">
          Step Progress:
        </Typography>
        <Box sx={progressBarContainerStyles}>
          <LinearProgress
            variant="determinate"
            value={progress.stepProgress}
            sx={stepProgressBarStyles}
          />
          <motion.div
            initial={{ scaleX: 0 }}
            animate={{ scaleX: progress.stepProgress / 100 }}
            transition={{ duration: 0.6, ease: animationEasing.easeOut }}
            style={stepProgressOverlayStyles}
          />
        </Box>
        <motion.div
          key={progress.stepProgress}
          initial={{ scale: 1.2, color: '#1976d2' }}
          animate={{ scale: 1, color: 'inherit' }}
          transition={{ duration: 0.3 }}
        >
          <Typography variant="body2" color="text.secondary">
            {Math.round(progress.stepProgress)}%
          </Typography>
        </motion.div>
      </Box>
    </Box>

    {/* Step-by-Step Progress with Staggered Animation */}
    <Box mb={3}>
      <Typography variant="subtitle1" gutterBottom>
        Step-by-Step Progress
      </Typography>
      
      <Grid container spacing={2}>
        {[1, 2, 3].map((step, index) => (
          <Grid item xs={12} md={4} key={step}>
            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.8 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ 
                delay: index * 0.2, 
                duration: 0.6, 
                ease: "easeOut",
                type: "spring",
                stiffness: 100
              }}
              whileHover={{ 
                scale: 1.02,
                y: -5,
                transition: { duration: 0.2 }
              }}
            >
              <Card 
                variant="outlined" 
                sx={getStepCardStyles(progress.currentStep, step)}
              >
                <Box display="flex" alignItems="center" gap={2} mb={1}>
                  <motion.div
                    animate={{ 
                      rotate: progress.currentStep === step ? [0, 10, -10, 0] : 0,
                      scale: progress.currentStep === step ? 1.1 : 1,
                      backgroundColor: progress.currentStep > step ? '#4caf50' : 
                                     progress.currentStep === step ? '#1976d2' : '#9e9e9e'
                    }}
                    transition={{ 
                      rotate: { duration: 0.5 },
                      scale: { duration: 0.3 },
                      backgroundColor: { duration: 0.3 }
                    }}
                    style={{
                      ...stepCircleBaseStyles,
                      backgroundColor: getStepCircleColor(progress.currentStep, step)
                    }}
                  >
                    {progress.currentStep > step ? (
                      <motion.div
                        initial={{ scale: 0, rotate: -180 }}
                        animate={{ scale: 1, rotate: 0 }}
                        transition={{ type: "spring", stiffness: 200, damping: 10 }}
                      >
                        ✓
                      </motion.div>
                    ) : (
                      step
                    )}
                  </motion.div>
                  <Typography variant="subtitle2">
                    Step {step}
                  </Typography>
                </Box>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {step === 1 ? 'Content Strategy Analysis' :
                   step === 2 ? 'Gap Analysis & Opportunities' :
                   'Audience & Platform Strategy'}
                </Typography>
                
                {progress.currentStep >= step && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
                  >
                    <Box display="flex" alignItems="center" gap={1}>
                      <motion.div
                        animate={smallPulseAnimation}
                        transition={{ 
                          duration: 2, 
                          repeat: Infinity,
                          ease: animationEasing.easeInOut 
                        }}
                      >
                        <Chip
                          label={`${Math.round(progress.qualityScores[`step${step}` as keyof QualityScores] * 100)}%`}
                          size="small"
                          color={progress.qualityScores[`step${step}` as keyof QualityScores] >= 0.9 ? 'success' : 
                                 progress.qualityScores[`step${step}` as keyof QualityScores] >= 0.8 ? 'warning' : 'error'}
                        />
                      </motion.div>
                      <Typography variant="caption" color="text.secondary">
                        Quality Score
                      </Typography>
                    </Box>
                  </motion.div>
                )}
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </Box>

    {/* Recent Activity with Staggered Animation */}
    <Box mb={3}>
      <Typography variant="subtitle1" gutterBottom>
        Recent Activity
      </Typography>
      
      <Box sx={{ maxHeight: 200, overflowY: 'auto' }}>
        {progress.transparencyMessages.map((message, index) => (
          <motion.div
            key={`${message}-${index}`}
            initial={{ opacity: 0, x: -20, scale: 0.95 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            transition={{ 
              delay: index * 0.1, 
              duration: 0.4,
              ease: "easeOut"
            }}
          >
            <Box display="flex" alignItems="flex-start" gap={2} mb={1}>
              <motion.div
                animate={colorPulseAnimation}
                transition={{ 
                  duration: 2, 
                  repeat: Infinity,
                  ease: "easeInOut" 
                }}
                style={activityIndicatorStyles}
              />
              <Typography variant="body2">
                {message}
              </Typography>
            </Box>
          </motion.div>
        ))}
      </Box>
    </Box>

    {/* Performance Metrics with Counter Animation */}
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        Performance Metrics
      </Typography>
      
      <Grid container spacing={2}>
        {[
          { 
            value: progress.overallProgress, 
            label: 'Overall Progress', 
            color: 'primary.main',
            suffix: '%'
          },
          { 
            value: progress.qualityScores.overall * 100, 
            label: 'Quality Score', 
            color: 'success.main',
            suffix: '%'
          },
          { 
            value: progress.currentStep, 
            label: 'Steps Completed', 
            color: 'info.main',
            suffix: '/3'
          },
          { 
            value: progress.errors.length, 
            label: 'Issues Found', 
            color: 'secondary.main',
            suffix: ''
          }
        ].map((metric, index) => (
          <Grid item xs={12} md={3} key={index}>
            <motion.div
              initial={{ opacity: 0, y: 30, scale: 0.8 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ 
                delay: index * staggerDelay, 
                duration: animationDurations.medium,
                type: springConfig.type,
                stiffness: 100
              }}
              whileHover={{ scale: 1.05 }}
            >
              <Box textAlign="center" p={2}>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ 
                    delay: index * 0.1 + 0.3, 
                    type: "spring",
                    stiffness: 200,
                    damping: 10
                  }}
                >
                  <Typography 
                    variant="h5" 
                    sx={{ color: metric.color }} 
                    gutterBottom
                  >
                    <motion.span
                      initial={{ opacity: 0, scale: 0.5 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ 
                        delay: index * 0.1 + 0.5, 
                        duration: 0.5,
                        ease: "easeOut"
                      }}
                    >
                      {Math.round(metric.value)}
                    </motion.span>
                    {metric.suffix}
                  </Typography>
                </motion.div>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.1 + 0.8, duration: 0.5 }}
                >
                  <Typography variant="body2">
                    {metric.label}
                  </Typography>
                </motion.div>
              </Box>
            </motion.div>
          </Grid>
        ))}
      </Grid>
    </Box>
  </Paper>
);

export default LiveProgressPanel;
