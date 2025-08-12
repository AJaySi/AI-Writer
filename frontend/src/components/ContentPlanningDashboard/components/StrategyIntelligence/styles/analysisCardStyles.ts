import { Theme } from '@mui/material/styles';

// Color palette for analysis components
export const ANALYSIS_COLORS = {
  primary: '#667eea',
  secondary: '#764ba2',
  accent: '#f093fb',
  success: '#4caf50',
  warning: '#ff9800',
  error: '#f44336',
  info: '#2196f3',
  background: {
    gradient: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%)',
    dark: 'rgba(0, 0, 0, 0.3)',
    glass: 'rgba(255, 255, 255, 0.05)'
  },
  text: {
    primary: 'white',
    secondary: '#e0e0e0',
    muted: '#b0b0b0'
  },
  border: {
    primary: 'rgba(102, 126, 234, 0.3)',
    secondary: 'rgba(255, 255, 255, 0.1)'
  }
};

// Priority colors for chips
export const PRIORITY_COLORS = {
  high: '#f44336',
  medium: '#ff9800',
  low: '#4caf50',
  default: '#667eea'
};

// Impact colors for chips
export const IMPACT_COLORS = {
  high: '#f44336',
  medium: '#ff9800',
  low: '#4caf50',
  default: '#667eea'
};

// Main card container styles
export const getAnalysisCardStyles = () => ({
  card: {
    height: '100%',
    borderRadius: 3,
    background: ANALYSIS_COLORS.background.gradient,
    color: ANALYSIS_COLORS.text.primary,
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(102, 126, 234, 0.3)',
    border: `1px solid ${ANALYSIS_COLORS.border.primary}`,
    position: 'relative' as const,
    overflow: 'hidden',
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
    '&:hover': {
      boxShadow: '0 25px 70px rgba(102, 126, 234, 0.4)',
      transform: 'translateY(-4px)'
    },
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
  },
  cardContent: {
    p: 2.5,
    position: 'relative' as const,
    zIndex: 1
  }
});

// Header section styles
export const getHeaderStyles = () => ({
  headerContainer: {
    display: 'flex',
    alignItems: 'center',
    mb: 2.5
  },
  iconContainer: {
    p: 1,
    borderRadius: 2,
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    mr: 1.5,
    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
  },
  titleContainer: {
    flex: 1
  },
  title: {
    fontWeight: 700,
    background: 'linear-gradient(45deg, #667eea, #764ba2, #f093fb)',
    backgroundSize: '200% 200%',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    animation: 'gradient 3s ease infinite',
    '@keyframes gradient': {
      '0%': { backgroundPosition: '0% 50%' },
      '50%': { backgroundPosition: '100% 50%' },
      '100%': { backgroundPosition: '0% 50%' }
    }
  }
});

// Market analysis header styles
export const getMarketAnalysisHeaderStyles = () => ({
  marketAnalysisContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: 2,
    p: 1.5,
    background: ANALYSIS_COLORS.background.dark,
    borderRadius: 2,
    border: `1px solid ${ANALYSIS_COLORS.border.secondary}`,
    backdropFilter: 'blur(10px)'
  },
  circularProgress: {
    color: ANALYSIS_COLORS.primary,
    '& .MuiCircularProgress-circle': {
      strokeLinecap: 'round',
      filter: 'drop-shadow(0 2px 4px rgba(102, 126, 234, 0.3))'
    }
  },
  progressText: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    fontWeight: 700,
    color: ANALYSIS_COLORS.primary,
    fontSize: '0.7rem'
  },
  positionText: {
    fontWeight: 600,
    color: ANALYSIS_COLORS.text.primary,
    display: 'block',
    fontSize: '0.7rem'
  },
  positionLabel: {
    color: ANALYSIS_COLORS.text.secondary,
    fontSize: '0.6rem'
  },
  marketChip: {
    background: 'rgba(0, 0, 0, 0.4)',
    color: ANALYSIS_COLORS.primary,
    fontWeight: 600,
    fontSize: '0.6rem',
    height: 20,
    border: `1px solid rgba(102, 126, 234, 0.4)`,
    '& .MuiChip-label': {
      px: 1
    }
  }
});

// Section container styles
export const getSectionStyles = () => ({
  sectionContainer: {
    mb: 2.5,
    p: 2,
    background: ANALYSIS_COLORS.background.dark,
    borderRadius: 2,
    border: `1px solid ${ANALYSIS_COLORS.border.secondary}`,
    backdropFilter: 'blur(10px)'
  },
  sectionTitle: {
    fontWeight: 600,
    color: ANALYSIS_COLORS.text.primary,
    fontSize: '0.85rem'
  }
});

// Accordion styles
export const getAccordionStyles = () => ({
  accordion: {
    mb: 1,
    '&:before': { display: 'none' },
    background: ANALYSIS_COLORS.background.dark,
    borderRadius: 2,
    border: `1px solid ${ANALYSIS_COLORS.border.secondary}`,
    backdropFilter: 'blur(10px)',
    '&.Mui-expanded': {
      margin: '8px 0'
    }
  },
  accordionSummary: {
    '& .MuiAccordionSummary-content': {
      margin: '8px 0'
    }
  },
  accordionTitle: {
    fontWeight: 600,
    color: ANALYSIS_COLORS.text.primary,
    fontSize: '0.8rem'
  },
  accordionSubtitle: {
    color: ANALYSIS_COLORS.text.secondary
  },
  expandIcon: {
    color: ANALYSIS_COLORS.primary
  }
});

// Enhanced chip styles
export const getEnhancedChipStyles = (color: string) => ({
  chip: {
    background: `linear-gradient(135deg, ${color}70 0%, ${color}60 100%)`,
    color: color,
    fontWeight: 700,
    fontSize: '0.75rem',
    height: 30,
    border: `3px solid ${color}80`,
    boxShadow: `0 8px 20px ${color}50, inset 0 3px 0 rgba(255, 255, 255, 0.2), inset 0 -2px 0 rgba(0, 0, 0, 0.4), 0 0 15px ${color}30`,
    backdropFilter: 'blur(20px)',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    textShadow: '0 2px 4px rgba(0, 0, 0, 0.5)',
    position: 'relative' as const,
    '&::before': {
      content: '""',
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: `linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(0, 0, 0, 0.1) 100%)`,
      borderRadius: 'inherit',
      pointerEvents: 'none'
    },
    '&:hover': {
      transform: 'translateY(-4px) scale(1.05)',
      boxShadow: `0 12px 30px ${color}60, inset 0 3px 0 rgba(255, 255, 255, 0.3), inset 0 -2px 0 rgba(0, 0, 0, 0.5), 0 0 25px ${color}40`,
      background: `linear-gradient(135deg, ${color}80 0%, ${color}70 100%)`
    },
    '& .MuiChip-label': {
      px: 2.5,
      py: 1,
      fontWeight: 700,
      letterSpacing: '0.6px',
      position: 'relative' as const,
      zIndex: 1
    },
    '& .MuiChip-icon': {
      color: color,
      fontSize: '1.1rem',
      filter: 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5))',
      position: 'relative' as const,
      zIndex: 1
    }
  }
});

// List item styles
export const getListItemStyles = () => ({
  listItem: {
    px: 0,
    py: 1
  },
  listItemIcon: {
    minWidth: 32
  },
  bulletPoint: {
    width: 8,
    height: 8,
    borderRadius: '50%',
    background: ANALYSIS_COLORS.primary,
    opacity: 0.7
  },
  insightText: {
    fontWeight: 500,
    mb: 1,
    color: ANALYSIS_COLORS.text.primary,
    lineHeight: 1.5
  },
  reasoningText: {
    color: ANALYSIS_COLORS.text.muted,
    fontStyle: 'italic',
    lineHeight: 1.4
  }
});

// Fallback/empty state styles
export const getFallbackStyles = () => ({
  fallbackContainer: {
    textAlign: 'center',
    py: 4
  },
  fallbackText: {
    mb: 2,
    color: ANALYSIS_COLORS.text.secondary
  },
  fallbackCaption: {
    color: ANALYSIS_COLORS.text.muted
  }
});

// Animation styles
export const getAnimationStyles = () => ({
  iconAnimation: {
    animate: { rotate: [0, 10, -10, 0] },
    transition: { duration: 2, repeat: Infinity, ease: "easeInOut" as const }
  },
  cardAnimation: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.5 },
    whileHover: { y: -4 }
  }
});

// Utility functions
export const getPriorityColor = (priority: string): string => {
  switch (priority.toLowerCase()) {
    case 'high':
      return PRIORITY_COLORS.high;
    case 'medium':
      return PRIORITY_COLORS.medium;
    case 'low':
      return PRIORITY_COLORS.low;
    default:
      return PRIORITY_COLORS.default;
  }
};

export const getImpactColor = (impact: string): string => {
  switch (impact.toLowerCase()) {
    case 'high':
      return IMPACT_COLORS.high;
    case 'medium':
      return IMPACT_COLORS.medium;
    case 'low':
      return IMPACT_COLORS.low;
    default:
      return IMPACT_COLORS.default;
  }
};

// Icon mapping for different insight types
export const getInsightIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case 'market positioning':
      return { icon: 'Business', color: ANALYSIS_COLORS.primary };
    case 'content opportunity':
      return { icon: 'Lightbulb', color: ANALYSIS_COLORS.success };
    case 'growth potential':
      return { icon: 'TrendingUp', color: ANALYSIS_COLORS.info };
    case 'competitive advantage':
      return { icon: 'Star', color: ANALYSIS_COLORS.warning };
    case 'strategic recommendation':
      return { icon: 'Psychology', color: ANALYSIS_COLORS.error };
    default:
      return { icon: 'Lightbulb', color: ANALYSIS_COLORS.primary };
  }
};

// Complete style object for easy import
export const ANALYSIS_CARD_STYLES = {
  colors: ANALYSIS_COLORS,
  priorityColors: PRIORITY_COLORS,
  impactColors: IMPACT_COLORS,
  getAnalysisCardStyles,
  getHeaderStyles,
  getMarketAnalysisHeaderStyles,
  getSectionStyles,
  getAccordionStyles,
  getEnhancedChipStyles,
  getListItemStyles,
  getFallbackStyles,
  getAnimationStyles,
  getPriorityColor,
  getImpactColor,
  getInsightIcon
}; 