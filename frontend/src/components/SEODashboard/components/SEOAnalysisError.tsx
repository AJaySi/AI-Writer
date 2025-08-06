import React from 'react';
import { 
  Alert, 
  IconButton 
} from '@mui/material';
import { 
  Close as CloseIcon 
} from '@mui/icons-material';
import { SEOAnalysisErrorProps } from '../../shared/types';

const SEOAnalysisError: React.FC<SEOAnalysisErrorProps> = ({ 
  error, 
  showError, 
  onCloseError 
}) => {
  if (!error || !showError) return null;

  return (
    <Alert 
      severity="error" 
      sx={{ mb: 2 }}
      action={
        <IconButton
          color="inherit"
          size="small"
          onClick={onCloseError}
        >
          <CloseIcon />
        </IconButton>
      }
    >
      {error}
    </Alert>
  );
};

export default SEOAnalysisError; 