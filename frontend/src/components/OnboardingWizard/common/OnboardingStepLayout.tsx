import React from 'react';
import { 
  Box, 
  Typography, 
  Fade, 
  Zoom, 
  useTheme,
  Container
} from '@mui/material';
import { ReactNode } from 'react';

interface OnboardingStepLayoutProps {
  icon: ReactNode;
  title: string;
  subtitle: string;
  children: ReactNode;
  maxWidth?: number | string;
  showIcon?: boolean;
  centered?: boolean;
}

const OnboardingStepLayout: React.FC<OnboardingStepLayoutProps> = ({
  icon,
  title,
  subtitle,
  children,
  maxWidth = 800,
  showIcon = true,
  centered = true
}) => {
  const theme = useTheme();

  return (
    <Fade in={true} timeout={500}>
      <Container maxWidth="lg" sx={{ py: 2 }}>
        {/* Header */}
        <Box sx={{ 
          textAlign: centered ? 'center' : 'left', 
          mb: 4,
          maxWidth: maxWidth,
          mx: centered ? 'auto' : 0
        }}>
          <Zoom in={true} timeout={600}>
            <Box>
              {showIcon && (
                <Box sx={{ 
                  mb: 3, 
                  display: 'flex', 
                  justifyContent: centered ? 'center' : 'flex-start',
                  position: 'relative'
                }}>
                  <Box sx={{
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
                  }}>
                    {React.cloneElement(icon as React.ReactElement, { 
                      sx: { fontSize: 36, color: 'white' } 
                    })}
                  </Box>
                </Box>
              )}
              <Typography 
                variant="h4" 
                gutterBottom 
                sx={{ 
                  fontWeight: 700, 
                  mb: 2,
                  letterSpacing: '-0.025em',
                  color: 'text.primary'
                }}
              >
                {title}
              </Typography>
              <Typography 
                variant="body1" 
                color="text.secondary"
                sx={{ 
                  lineHeight: 1.6,
                  maxWidth: 600,
                  mx: centered ? 'auto' : 0,
                  fontSize: '1.1rem'
                }}
              >
                {subtitle}
              </Typography>
            </Box>
          </Zoom>
        </Box>

        {/* Content */}
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          gap: 3,
          maxWidth: maxWidth,
          mx: centered ? 'auto' : 0
        }}>
          {children}
        </Box>
      </Container>
    </Fade>
  );
};

export default OnboardingStepLayout; 