import React from 'react';
import { Box, Container, Alert, Button } from '@mui/material';
import { DashboardContainer } from './styled';
import { ErrorDisplayProps } from './types';

const ErrorDisplay: React.FC<ErrorDisplayProps> = ({ 
  error, 
  onRetry, 
  retryButtonText = 'Retry' 
}) => {
  return (
    <DashboardContainer>
      <Container maxWidth="xl">
        <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }}>
          {error}
        </Alert>
        {onRetry && (
          <Button onClick={onRetry} variant="contained">
            {retryButtonText}
          </Button>
        )}
      </Container>
    </DashboardContainer>
  );
};

export default ErrorDisplay; 