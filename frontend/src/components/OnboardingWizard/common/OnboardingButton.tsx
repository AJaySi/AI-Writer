import React from 'react';
import { Button, Box, CircularProgress } from '@mui/material';
import { ReactNode } from 'react';

interface OnboardingButtonProps {
  variant?: 'primary' | 'secondary' | 'text';
  loading?: boolean;
  children: ReactNode;
  icon?: ReactNode;
  iconPosition?: 'start' | 'end';
  onClick?: () => void;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
  fullWidth?: boolean;
  size?: 'small' | 'medium' | 'large';
  [key: string]: any;
}

const OnboardingButton: React.FC<OnboardingButtonProps> = ({
  variant = 'primary',
  loading = false,
  children,
  icon,
  iconPosition = 'start',
  onClick,
  disabled,
  type = 'button',
  fullWidth = false,
  size = 'medium',
  ...props
}) => {
  const baseStyles = {
    borderRadius: 2,
    textTransform: 'none' as const,
    fontWeight: 600,
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    position: 'relative' as const,
    overflow: 'hidden' as const,
    '&::before': {
      content: '""',
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
      opacity: 0,
      transition: 'opacity 0.3s ease',
    },
    '&:hover::before': {
      opacity: 1,
    },
  };

  const getStyles = () => {
    const sizeStyles = {
      small: { px: 2, py: 1, fontSize: '0.875rem' },
      medium: { px: 3, py: 1.5, fontSize: '1rem' },
      large: { px: 4, py: 2, fontSize: '1.125rem' },
    };

    switch (variant) {
      case 'primary':
        return {
          ...baseStyles,
          ...sizeStyles[size],
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
          color: 'white',
          '&:hover': {
            background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
            transform: 'translateY(-1px)',
            boxShadow: '0 6px 16px rgba(102, 126, 234, 0.4)',
          },
          '&:active': {
            transform: 'translateY(0px)',
            boxShadow: '0 2px 8px rgba(102, 126, 234, 0.3)',
          },
          '&:disabled': {
            background: 'rgba(0,0,0,0.1)',
            color: 'rgba(0,0,0,0.4)',
            boxShadow: 'none',
            transform: 'none',
          },
        };
      case 'secondary':
        return {
          ...baseStyles,
          ...sizeStyles[size],
          borderColor: 'rgba(0,0,0,0.2)',
          color: 'text.primary',
          background: 'transparent',
          '&:hover': {
            borderColor: 'rgba(0,0,0,0.4)',
            background: 'rgba(0,0,0,0.04)',
            transform: 'translateY(-1px)',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
          },
          '&:active': {
            transform: 'translateY(0px)',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          },
          '&:disabled': {
            borderColor: 'rgba(0,0,0,0.1)',
            color: 'rgba(0,0,0,0.3)',
            background: 'transparent',
            transform: 'none',
            boxShadow: 'none',
          }
        };
      case 'text':
        return {
          ...baseStyles,
          ...sizeStyles[size],
          color: 'primary.main',
          background: 'transparent',
          '&:hover': {
            background: 'rgba(102, 126, 234, 0.08)',
            transform: 'translateY(-1px)',
          },
          '&:active': {
            transform: 'translateY(0px)',
          },
          '&:disabled': {
            color: 'rgba(0,0,0,0.3)',
            background: 'transparent',
            transform: 'none',
          }
        };
      default:
        return baseStyles;
    }
  };

  const buttonVariant = variant === 'primary' ? 'contained' : variant === 'secondary' ? 'outlined' : 'text';

  return (
    <Button
      variant={buttonVariant}
      onClick={onClick}
      disabled={loading || disabled}
      type={type}
      fullWidth={fullWidth}
      startIcon={iconPosition === 'start' && icon && !loading ? icon : undefined}
      endIcon={iconPosition === 'end' && icon && !loading ? icon : undefined}
      sx={getStyles()}
      {...props}
    >
      {loading ? (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CircularProgress 
            size={size === 'small' ? 16 : size === 'large' ? 24 : 20} 
            color="inherit" 
            thickness={4}
          />
          {children}
        </Box>
      ) : (
        children
      )}
    </Button>
  );
};

export default OnboardingButton; 