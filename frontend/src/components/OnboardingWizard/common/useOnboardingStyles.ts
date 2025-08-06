import { useTheme } from '@mui/material';

export const useOnboardingStyles = () => {
  const theme = useTheme();

  const styles = {
    // Layout styles
    container: {
      maxWidth: 800,
      mx: 'auto',
    },
    
    // Header styles
    header: {
      textAlign: 'center',
      mb: 4,
    },
    
    headerIcon: {
      fontSize: 64,
      color: 'primary.main',
      mb: 2,
    },
    
    headerIconContainer: {
      width: 80,
      height: 80,
      borderRadius: '50%',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      boxShadow: '0 8px 25px rgba(102, 126, 234, 0.3)',
      position: 'relative',
      '&::before': {
        content: '""',
        position: 'absolute',
        top: -2,
        left: -2,
        right: -2,
        bottom: -2,
        borderRadius: '50%',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        opacity: 0.3,
        zIndex: -1,
      }
    },
    
    headerTitle: {
      fontWeight: 700,
      letterSpacing: '-0.025em',
    },
    
    headerSubtitle: {
      color: 'text.secondary',
      lineHeight: 1.6,
      maxWidth: 600,
      mx: 'auto',
    },
    
    // Card styles
    card: {
      elevation: 2,
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      borderRadius: 3,
      '&:hover': {
        elevation: 4,
        transform: 'translateY(-2px)',
        boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
      },
    },
    
    cardContent: {
      p: 3,
    },
    
    cardHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      mb: 2,
    },
    
    cardTitle: {
      display: 'flex',
      alignItems: 'center',
      gap: 1.5,
    },
    
    cardIconContainer: {
      width: 40,
      height: 40,
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    },
    
    // Button styles
    primaryButton: {
      borderRadius: 2,
      textTransform: 'none' as const,
      fontWeight: 600,
      px: 4,
      py: 1.5,
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
      },
    },
    
    secondaryButton: {
      borderRadius: 2,
      textTransform: 'none' as const,
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
    },
    
    textButton: {
      textTransform: 'none' as const,
      fontWeight: 600,
    },
    
    // Form styles
    textField: {
      '& .MuiOutlinedInput-root': {
        borderRadius: 2,
      },
      '& .MuiInputBase-input': {
        padding: '12px 16px',
      },
    },
    
    // Alert styles
    alert: {
      borderRadius: 2,
      '& .MuiAlert-icon': {
        fontSize: 20,
      },
    },
    
    // Paper styles
    infoPaper: {
      background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
      border: '1px solid rgba(59, 130, 246, 0.2)',
      borderRadius: 2,
    },
    
    warningPaper: {
      background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
      border: '1px solid rgba(245, 158, 11, 0.2)',
      borderRadius: 2,
    },
    
    successPaper: {
      background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)',
      border: '1px solid rgba(16, 185, 129, 0.2)',
      borderRadius: 2,
    },
    
    // Progress styles
    progressBar: {
      height: 8,
      borderRadius: 4,
      backgroundColor: 'rgba(0,0,0,0.08)',
      '& .MuiLinearProgress-bar': {
        borderRadius: 4,
        background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
      }
    },
    
    // Chip styles
    chip: {
      fontWeight: 600,
      borderRadius: 1,
    },
    
    // Divider styles
    divider: {
      my: 2,
      opacity: 0.6,
    },
    
    // Link styles
    link: {
      fontWeight: 600,
      textDecoration: 'none',
      '&:hover': {
        textDecoration: 'underline',
      },
    },
    
    // Animation styles
    fadeIn: {
      animation: 'fadeIn 0.5s ease-in-out',
    },
    
    slideUp: {
      animation: 'slideUp 0.3s ease-out',
    },
    
    // Responsive styles
    responsiveContainer: {
      maxWidth: { xs: '100%', md: 800 },
      mx: 'auto',
      px: { xs: 2, md: 3 },
    },
    
    // Spacing utilities
    sectionSpacing: {
      mb: 4,
    },
    
    cardSpacing: {
      gap: 3,
    },
    
    buttonSpacing: {
      gap: 2,
    },
  };

  return styles;
}; 