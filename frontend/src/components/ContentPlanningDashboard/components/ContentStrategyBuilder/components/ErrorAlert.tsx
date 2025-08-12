import React from 'react';
import {
  Box,
  Alert,
  Button,
  Typography
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { ErrorAlertProps } from '../types/contentStrategy.types';

const ErrorAlert: React.FC<ErrorAlertProps> = ({
  error,
  onRetry,
  onShowDataSourceTransparency
}) => {
  if (!error) return null;

  return (
    <Alert
      severity="error"
      sx={{ mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
      action={
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button 
            size="small" 
            variant="outlined" 
            onClick={onRetry} 
            startIcon={<RefreshIcon />}
          >
            Retry
          </Button>
          <Button 
            size="small" 
            variant="contained" 
            color="primary" 
            onClick={onShowDataSourceTransparency} 
            startIcon={<InfoIcon />}
          >
            Why?
          </Button>
        </Box>
      }
    >
      <Box>
        <Typography variant="subtitle2">Real data required</Typography>
        <Typography variant="body2">
          {error || 'We could not auto-populate because required onboarding/analysis data is missing. Connect sources or complete onboarding, then retry.'}
        </Typography>
      </Box>
    </Alert>
  );
};

export default ErrorAlert; 