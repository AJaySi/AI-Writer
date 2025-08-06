import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { EmptyStateProps } from './types';

const EmptyState: React.FC<EmptyStateProps> = ({ 
  title, 
  message, 
  onClearFilters, 
  clearButtonText = 'Clear Filters' 
}) => {
  return (
    <Box sx={{ textAlign: 'center', py: 8 }}>
      <Typography variant="h5" sx={{ color: 'rgba(255, 255, 255, 0.9)', mb: 2, fontWeight: 600 }}>
        {title}
      </Typography>
      <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 3 }}>
        {message}
      </Typography>
      {onClearFilters && (
        <Button
          variant="outlined"
          onClick={onClearFilters}
          sx={{
            color: 'white',
            borderColor: 'rgba(255, 255, 255, 0.3)',
            '&:hover': {
              borderColor: 'rgba(255, 255, 255, 0.5)',
              background: 'rgba(255, 255, 255, 0.1)',
            },
          }}
        >
          {clearButtonText}
        </Button>
      )}
    </Box>
  );
};

export default EmptyState; 