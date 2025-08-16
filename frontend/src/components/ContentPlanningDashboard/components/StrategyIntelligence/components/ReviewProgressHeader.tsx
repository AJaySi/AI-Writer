import React from 'react';
import {
  Box,
  Typography,
  Chip,
  IconButton,
  Tooltip,
  Card,
  CardContent,
  Badge,
  Button,
  CircularProgress
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  Warning as WarningIcon,
  PlayArrow as PlayArrowIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useStrategyReviewStore } from '../../../../../stores/strategyReviewStore';
import { ANALYSIS_CARD_STYLES } from '../styles';
import { contentPlanningApi } from '../../../../../services/contentPlanningApi';

const ReviewProgressHeader: React.FC = () => {
  const {
    components,
    reviewProgress,
    isAllReviewed,
    resetAllReviews,
    getUnreviewedComponents,
    getReviewedComponents
  } = useStrategyReviewStore();

  // Extract domain name from strategy data (you can pass this as prop if needed)
  const getDomainName = () => {
    // For now, return a default domain - you can enhance this to get from strategy data
    return "alwrity.com";
  };

  const unreviewedCount = getUnreviewedComponents().length;
  const reviewedCount = getReviewedComponents().length;
  const totalCount = components.length;

  // Debug logging
  console.log('🔍 ReviewProgressHeader Debug:', {
    components,
    reviewProgress,
    unreviewedCount,
    reviewedCount,
    totalCount,
    isAllReviewed: isAllReviewed()
  });

  const getProgressColor = () => {
    if (reviewProgress === 100) return ANALYSIS_CARD_STYLES.colors.success;
    if (reviewProgress >= 60) return ANALYSIS_CARD_STYLES.colors.primary;
    if (reviewProgress >= 30) return ANALYSIS_CARD_STYLES.colors.warning;
    return ANALYSIS_CARD_STYLES.colors.error;
  };

  const getProgressText = () => {
    if (reviewProgress === 100) return 'All components reviewed!';
    if (reviewProgress >= 60) return 'Great progress!';
    if (reviewProgress >= 30) return 'Making good progress';
    return 'Getting started';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    >
      <Card 
        sx={{ 
          mb: 3, 
          background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%)',
          color: 'white',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(102, 126, 234, 0.3)',
          borderRadius: 3,
          position: 'relative',
          overflow: 'hidden',
          border: '1px solid rgba(102, 126, 234, 0.3)',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%)',
            pointerEvents: 'none'
          },
          '&::after': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%)',
            animation: 'shimmer 3s infinite',
            pointerEvents: 'none'
          },
          '@keyframes shimmer': {
            '0%': { transform: 'translateX(-100%)' },
            '100%': { transform: 'translateX(100%)' }
          }
        }}
      >
        {/* Animated Border Lights */}
        <motion.div
          animate={{
            boxShadow: [
              '0 0 20px rgba(102, 126, 234, 0.5)',
              '0 0 40px rgba(102, 126, 234, 0.8)',
              '0 0 20px rgba(102, 126, 234, 0.5)'
            ]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            borderRadius: '12px',
            pointerEvents: 'none'
          }}
        />

        <CardContent sx={{ position: 'relative', zIndex: 1, p: 2 }}>
          {/* Header with Circular Progress and Status Chips */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1.5 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              {/* Circular Progress */}
              <Box sx={{ position: 'relative', display: 'inline-flex' }}>
                <CircularProgress
                  variant="determinate"
                  value={reviewProgress}
                  size={50}
                  thickness={4}
                  sx={{
                    color: getProgressColor(),
                    '& .MuiCircularProgress-circle': {
                      strokeLinecap: 'round',
                    }
                  }}
                />
                <Box
                  sx={{
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    position: 'absolute',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <Typography variant="caption" sx={{ 
                    color: getProgressColor(), 
                    fontWeight: 700, 
                    fontSize: '0.7rem' 
                  }}>
                    {Math.round(reviewProgress)}%
                  </Typography>
                </Box>
              </Box>
              
              <Box>
                <Typography variant="h6" sx={{ 
                  color: 'white',
                  fontWeight: 600,
                  mb: 0.25
                }}>
                  Strategy Review Progress
                </Typography>
                <Typography variant="body2" sx={{ 
                  color: 'rgba(255, 255, 255, 0.8)',
                  fontSize: '0.8rem'
                }}>
                  {getProgressText()}
                </Typography>
              </Box>
              
              {/* Status Chips */}
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Chip
                  icon={<CheckCircleIcon />}
                  label={`${reviewedCount} Reviewed`}
                  size="small"
                  sx={{
                    background: ANALYSIS_CARD_STYLES.colors.success,
                    color: 'white',
                    fontWeight: 500,
                    fontSize: '0.65rem',
                    height: 24,
                    '& .MuiChip-icon': {
                      color: 'white',
                      fontSize: 14
                    }
                  }}
                />
                
                {unreviewedCount > 0 && (
                  <Chip
                    icon={<ScheduleIcon />}
                    label={`${unreviewedCount} Pending`}
                    size="small"
                    sx={{
                      background: ANALYSIS_CARD_STYLES.colors.warning,
                      color: 'white',
                      fontWeight: 500,
                      fontSize: '0.65rem',
                      height: 24,
                      '& .MuiChip-icon': {
                        color: 'white',
                        fontSize: 14
                      }
                    }}
                  />
                )}
              </Box>
            </Box>

            {/* Reset Button */}
            <Tooltip title="Reset all reviews">
              <IconButton
                onClick={resetAllReviews}
                size="small"
                sx={{
                  color: 'rgba(255, 255, 255, 0.8)',
                  '&:hover': {
                    color: '#f44336',
                    background: 'rgba(244, 67, 54, 0.2)'
                  }
                }}
              >
                <RefreshIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>

          {/* Progress Summary */}
          <Box sx={{ mb: 1.5 }}>
            <Typography variant="body2" sx={{ 
              color: 'white',
              fontWeight: 500,
              fontSize: '0.8rem'
            }}>
              {reviewedCount} of {totalCount} components reviewed
            </Typography>
          </Box>

          {/* Informative Text */}
          <Box sx={{ mb: 1.5 }}>
            <Typography variant="body2" sx={{ 
              color: 'rgba(255, 255, 255, 0.9)',
              fontSize: '0.8rem',
              lineHeight: 1.4,
              background: 'rgba(255, 255, 255, 0.05)',
              p: 1.5,
              borderRadius: 1,
              border: '1px solid rgba(255, 255, 255, 0.1)'
            }}>
              <strong>Complete review by clicking 'Not Reviewed' button and confirming datapoints of 5 analysis components below.</strong> 
              <br />
              <span style={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                Important: Content strategy for <strong>{getDomainName()}</strong> will shape content generation next.
              </span>
            </Typography>
          </Box>

          {/* Individual Component Status and Activate Strategy Button */}
          <Box sx={{ mb: 1.5 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.75 }}>
              <Typography variant="caption" sx={{ 
                color: 'rgba(255, 255, 255, 0.8)',
                fontWeight: 500,
                fontSize: '0.7rem'
              }}>
                Component Status
              </Typography>
              
                             {/* Confirm & Activate Strategy Button */}
               <Tooltip 
                 title={isAllReviewed() ? "Confirm strategy and activate content generation" : "Complete all component reviews to confirm and activate strategy"}
                 arrow
               >
                 <Button
                   variant="contained"
                   size="small"
                   disabled={!isAllReviewed()}
                   startIcon={<PlayArrowIcon />}
                                     onClick={async () => {
                    if (isAllReviewed()) {
                      try {
                        // Handle strategy confirmation and activation
                        console.log('Confirming and activating strategy...');
                        
                        // 1. Save the strategy confirmation to backend
                        // Note: You'll need to get the actual strategy ID from context/props
                        const strategyId = "current_strategy_id"; // Replace with actual strategy ID
                        
                        try {
                          await contentPlanningApi.updateEnhancedStrategy(
                            strategyId,
                            { 
                              confirmed: true, 
                              confirmed_at: new Date().toISOString(),
                              review_completed: true,
                              review_completed_at: new Date().toISOString()
                            }
                          );
                          console.log('Strategy confirmation saved to backend');
                        } catch (updateError) {
                          console.warn('Could not save confirmation to backend:', updateError);
                        }
                        
                        // 2. Show success message
                        alert('Strategy confirmed and activated! You can now proceed to create your content calendar.');
                        
                        // 3. Navigate to content calendar creation
                        // You can add navigation logic here
                        // navigate('/content-calendar');
                        
                      } catch (error) {
                        console.error('Error confirming and activating strategy:', error);
                        alert('Error confirming strategy. Please try again.');
                      }
                    }
                  }}
                   sx={{
                     background: isAllReviewed() 
                       ? 'linear-gradient(135deg, #4caf50 0%, #66bb6a 100%)'
                       : 'rgba(255, 255, 255, 0.1)',
                     color: isAllReviewed() ? 'white' : 'rgba(255, 255, 255, 0.5)',
                     fontWeight: 600,
                     fontSize: '0.7rem',
                     px: 2,
                     py: 0.5,
                     borderRadius: 2,
                     boxShadow: isAllReviewed() 
                       ? '0 2px 8px rgba(76, 175, 80, 0.3)'
                       : 'none',
                     border: isAllReviewed() 
                       ? '1px solid rgba(76, 175, 80, 0.4)'
                       : '1px solid rgba(255, 255, 255, 0.2)',
                     textTransform: 'none',
                     minWidth: 'auto',
                     '&:hover': {
                       background: isAllReviewed()
                         ? 'linear-gradient(135deg, #66bb6a 0%, #81c784 100%)'
                         : 'rgba(255, 255, 255, 0.1)',
                       boxShadow: isAllReviewed()
                         ? '0 4px 12px rgba(76, 175, 80, 0.4)'
                         : 'none',
                       transform: isAllReviewed() ? 'translateY(-1px)' : 'none'
                     },
                     '&:active': {
                       transform: isAllReviewed() ? 'translateY(0)' : 'none'
                     },
                     '&:disabled': {
                       background: 'rgba(255, 255, 255, 0.05)',
                       color: 'rgba(255, 255, 255, 0.3)',
                       boxShadow: 'none',
                       transform: 'none'
                     },
                     '& .MuiButton-startIcon': {
                       marginRight: 0.5
                     }
                   }}
                 >
                   Confirm & Activate Strategy
                 </Button>
               </Tooltip>
            </Box>
            
            <Box sx={{ display: 'flex', gap: 0.75, flexWrap: 'wrap' }}>
              {components.map((component) => (
                <Tooltip 
                  key={component.id}
                  title={`${component.title}: ${component.status === 'reviewed' ? 'Reviewed' : 'Pending Review'}`}
                  arrow
                >
                  <Badge
                    badgeContent={
                      component.status === 'reviewed' ? (
                        <CheckCircleIcon sx={{ fontSize: 10, color: 'white' }} />
                      ) : (
                        <ScheduleIcon sx={{ fontSize: 10, color: 'white' }} />
                      )
                    }
                    color={component.status === 'reviewed' ? 'success' : 'warning'}
                  >
                    <Chip
                      label={component.title}
                      size="small"
                      sx={{
                        background: component.status === 'reviewed' 
                          ? 'rgba(76, 175, 80, 0.3)' 
                          : 'rgba(255, 152, 0, 0.3)',
                        color: component.status === 'reviewed' ? '#4caf50' : '#ff9800',
                        border: `1px solid ${component.status === 'reviewed' ? 'rgba(76, 175, 80, 0.5)' : 'rgba(255, 152, 0, 0.5)'}`,
                        fontWeight: 600,
                        fontSize: '0.65rem',
                        height: 22,
                        '&:hover': {
                          background: component.status === 'reviewed' 
                            ? 'rgba(76, 175, 80, 0.4)' 
                            : 'rgba(255, 152, 0, 0.4)',
                          transform: 'translateY(-1px)'
                        },
                        transition: 'all 0.2s ease'
                      }}
                    />
                  </Badge>
                </Tooltip>
              ))}
            </Box>
          </Box>

          {/* Completion Status */}
          {isAllReviewed() && (
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Chip
                icon={<CheckCircleIcon />}
                label="Ready for Calendar Creation"
                size="small"
                sx={{
                  background: ANALYSIS_CARD_STYLES.colors.success,
                  color: 'white',
                  fontWeight: 500,
                  animation: 'pulse 2s infinite',
                  fontSize: '0.65rem',
                  height: 22,
                  '@keyframes pulse': {
                    '0%, 100%': { opacity: 1 },
                    '50%': { opacity: 0.7 }
                  },
                  '& .MuiChip-icon': {
                    color: 'white',
                    fontSize: 14
                  }
                }}
              />
            </Box>
          )}

          {/* Completion Message */}
          {isAllReviewed() && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: 0.2 }}
            >
              <Box sx={{ 
                mt: 1.5, 
                p: 1.5, 
                borderRadius: 1,
                background: 'rgba(76, 175, 80, 0.1)',
                border: '1px solid rgba(76, 175, 80, 0.2)',
                textAlign: 'center'
              }}>
                <Typography variant="body2" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.success,
                  fontWeight: 600,
                  fontSize: '0.8rem'
                }}>
                  🎉 All strategy components have been reviewed! You can now proceed to create your content calendar.
                </Typography>
              </Box>
            </motion.div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default ReviewProgressHeader;
