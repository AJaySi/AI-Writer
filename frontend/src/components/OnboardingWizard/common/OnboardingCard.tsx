import React from 'react';
import { 
  Card, 
  CardContent, 
  Box, 
  Typography,
  Chip,
  Zoom,
  useTheme,
  Paper
} from '@mui/material';
import { ReactNode } from 'react';

interface OnboardingCardProps {
  title: string;
  icon: ReactNode;
  children: ReactNode;
  status?: 'valid' | 'invalid' | 'empty';
  statusLabel?: string;
  elevation?: number;
  delay?: number;
  saved?: boolean;
  variant?: 'default' | 'info' | 'warning' | 'success';
}

const OnboardingCard: React.FC<OnboardingCardProps> = ({
  title,
  icon,
  children,
  status,
  statusLabel,
  elevation = 2,
  delay = 0,
  saved = false,
  variant = 'default'
}) => {
  const theme = useTheme();

  const getStatusColor = () => {
    switch (status) {
      case 'valid':
        return '#10b981';
      case 'invalid':
        return '#ef4444';
      default:
        return 'transparent';
    }
  };

  const getStatusChip = () => {
    if (!status || status === 'empty') return null;
    
    return (
      <Chip 
        icon={status === 'valid' ? <Box component="span">✅</Box> : <Box component="span">❌</Box>}
        label={statusLabel || (status === 'valid' ? 'Valid' : 'Invalid')}
        color={status === 'valid' ? 'success' : 'error'}
        size="small"
        sx={{ fontWeight: 600, borderRadius: 1 }}
      />
    );
  };

  const getVariantStyles = () => {
    switch (variant) {
      case 'info':
        return {
          background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
          border: '1px solid rgba(59, 130, 246, 0.2)',
        };
      case 'warning':
        return {
          background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
          border: '1px solid rgba(245, 158, 11, 0.2)',
        };
      case 'success':
        return {
          background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)',
          border: '1px solid rgba(16, 185, 129, 0.2)',
        };
      default:
        return {
          background: 'white',
          border: `2px solid ${getStatusColor()}`,
        };
    }
  };

  return (
    <Zoom in={true} timeout={700 + delay}>
      <Card 
        elevation={elevation}
        sx={{ 
          ...getVariantStyles(),
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          borderRadius: 3,
          position: 'relative',
          overflow: 'hidden',
          '&:hover': {
            elevation: 4,
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
          },
          '&::before': variant === 'default' ? {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: 3,
            background: status === 'valid' 
              ? 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
              : status === 'invalid'
              ? 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)'
              : 'linear-gradient(90deg, #6b7280 0%, #4b5563 100%)',
          } : {},
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flex: 1 }}>
              <Box sx={{
                width: 40,
                height: 40,
                borderRadius: '50%',
                background: variant === 'default' 
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  : variant === 'info'
                  ? 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)'
                  : variant === 'warning'
                  ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                  : 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
              }}>
                {React.cloneElement(icon as React.ReactElement, { 
                  sx: { color: 'white', fontSize: 20 } 
                })}
              </Box>
              <Box sx={{ flex: 1 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                  {title}
                </Typography>
                {variant !== 'default' && (
                  <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.4 }}>
                    {children}
                  </Typography>
                )}
              </Box>
            </Box>
            {getStatusChip()}
          </Box>
          
          {variant === 'default' && children}
          
          {saved && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1.5 }}>
              <Box component="span" sx={{ 
                width: 16, 
                height: 16, 
                borderRadius: '50%', 
                background: '#10b981',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '10px',
                color: 'white',
                fontWeight: 'bold'
              }}>
                ✓
              </Box>
              <Typography variant="caption" color="success.main" sx={{ fontWeight: 500 }}>
                Already saved and secured
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Zoom>
  );
};

export default OnboardingCard; 