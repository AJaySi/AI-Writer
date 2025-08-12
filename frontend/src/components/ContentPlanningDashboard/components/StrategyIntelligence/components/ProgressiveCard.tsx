import React, { useState, useRef } from 'react';
import {
  Card,
  CardContent,
  Box,
  Button,
  Typography,
  Fade,
  useTheme
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  KeyboardArrowDown as ArrowDownIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ANALYSIS_CARD_STYLES,
  getAnalysisCardStyles,
  getEnhancedChipStyles
} from '../styles';

interface ProgressiveCardProps {
  summary: React.ReactNode;
  details: React.ReactNode;
  trigger?: 'hover' | 'click';
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
  autoCollapseDelay?: number; // milliseconds
  className?: string;
}

const ProgressiveCard: React.FC<ProgressiveCardProps> = ({
  summary,
  details,
  trigger = 'click',
  title,
  subtitle,
  icon,
  autoCollapseDelay = 3000, // 3 seconds default
  className
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const hoverTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const theme = useTheme();
  
  const cardStyles = getAnalysisCardStyles();

  // Handle hover interactions
  const handleMouseEnter = () => {
    if (trigger === 'hover') {
      // Clear any existing timeout
      if (hoverTimeoutRef.current) {
        clearTimeout(hoverTimeoutRef.current);
        hoverTimeoutRef.current = null;
      }
      setIsExpanded(true);
    }
  };

  const handleMouseLeave = () => {
    if (trigger === 'hover') {
      // Set timeout to auto-collapse
      hoverTimeoutRef.current = setTimeout(() => {
        setIsExpanded(false);
        hoverTimeoutRef.current = null;
      }, autoCollapseDelay);
    }
  };

  // Handle click interactions
  const handleToggle = () => {
    if (trigger === 'click') {
      setIsExpanded(!isExpanded);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
      whileHover={{ y: -4 }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className={className}
    >
      <Card sx={{
        ...cardStyles.card,
        '& .shimmer-text': {
          background: `linear-gradient(135deg, ${ANALYSIS_CARD_STYLES.colors.primary} 0%, ${ANALYSIS_CARD_STYLES.colors.secondary} 100%)`,
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          animation: 'shimmer 2s ease-in-out infinite'
        },
        '& .bounce-icon': {
          animation: 'bounce 2s infinite'
        },
        '@keyframes shimmer': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.8 }
        },
        '@keyframes bounce': {
          '0%, 20%, 50%, 80%, 100%': { transform: 'translateY(0)' },
          '40%': { transform: 'translateY(-4px)' },
          '60%': { transform: 'translateY(-2px)' }
        }
      }}>
        <CardContent sx={cardStyles.cardContent}>
          {/* Header Section */}
          {title && (
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'space-between',
              mb: 2 
            }}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                {icon && (
                  <Box sx={{ 
                    p: 1, 
                    borderRadius: 2, 
                    background: `linear-gradient(135deg, ${ANALYSIS_CARD_STYLES.colors.primary} 0%, ${ANALYSIS_CARD_STYLES.colors.secondary} 100%)`,
                    mr: 1.5,
                    boxShadow: `0 4px 12px ${ANALYSIS_CARD_STYLES.colors.primary}30`
                  }}>
                    {icon}
                  </Box>
                )}
                <Box>
                  <Typography variant="h6" className="shimmer-text" sx={{ 
                    fontWeight: 600
                  }}>
                    {title}
                  </Typography>
                  {subtitle && (
                    <Typography variant="caption" sx={{ 
                      color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                      fontSize: '0.75rem'
                    }}>
                      {subtitle}
                    </Typography>
                  )}
                </Box>
              </Box>
              
              {/* Trigger Button */}
              {trigger === 'click' && (
                <Button
                  onClick={handleToggle}
                  variant="text"
                  size="small"
                  sx={{
                    color: ANALYSIS_CARD_STYLES.colors.primary,
                    '&:hover': {
                      background: 'rgba(102, 126, 234, 0.1)'
                    },
                    minWidth: 'auto',
                    px: 1.5,
                    py: 0.5,
                    borderRadius: 2,
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    textTransform: 'none'
                  }}
                  endIcon={
                    isExpanded ? (
                      <ExpandLessIcon sx={{ fontSize: 16 }} />
                    ) : (
                      <ExpandMoreIcon sx={{ fontSize: 16 }} />
                    )
                  }
                >
                  {isExpanded ? 'Show Less' : 'Read More'}
                </Button>
              )}
            </Box>
          )}

          {/* Summary Section - Always Visible */}
          <Box sx={{ mb: trigger === 'click' ? 2 : 0 }}>
            {summary}
          </Box>

          {/* Progressive Details Section */}
          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ 
                  height: 0, 
                  opacity: 0,
                  overflow: 'hidden'
                }}
                animate={{ 
                  height: 'auto', 
                  opacity: 1,
                  overflow: 'visible'
                }}
                exit={{ 
                  height: 0, 
                  opacity: 0,
                  overflow: 'hidden'
                }}
                transition={{ 
                  duration: 0.4, 
                  ease: [0.4, 0.0, 0.2, 1],
                  opacity: { duration: 0.3 }
                }}
              >
                <Fade in={isExpanded} timeout={300}>
                  <Box sx={{ 
                    pt: 2,
                    borderTop: `1px solid ${ANALYSIS_CARD_STYLES.colors.border.secondary}`,
                    opacity: 0.9
                  }}>
                    {details}
                  </Box>
                </Fade>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Hover Indicator (for hover trigger) */}
          {trigger === 'hover' && !isExpanded && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.6 }}
              transition={{ duration: 0.3 }}
            >
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                mt: 1,
                py: 0.5
              }}>
                <ArrowDownIcon className="bounce-icon" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                  fontSize: 16
                }} />
                <Typography variant="caption" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                  ml: 0.5,
                  fontSize: '0.7rem'
                }}>
                  Hover to see more
                </Typography>
              </Box>
            </motion.div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default ProgressiveCard; 