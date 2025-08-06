import React from 'react';
import { 
  Box, 
  Typography, 
  LinearProgress 
} from '@mui/material';
import { SEOAnalysisLoadingProps } from '../../shared/types';

const SEOAnalysisLoading: React.FC<SEOAnalysisLoadingProps> = ({ loading }) => {
  if (!loading) return null;

  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="body1" sx={{ color: 'white', mb: 2 }}>
        🤖 AI is analyzing your website...
      </Typography>
      <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 2 }}>
        Identifying specific issues and generating actionable fixes...
      </Typography>
      <LinearProgress 
        sx={{ 
          height: 6, 
          borderRadius: 3,
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          '& .MuiLinearProgress-bar': {
            background: 'linear-gradient(90deg, #2196F3, #4CAF50)',
            borderRadius: 3,
          },
        }} 
      />
    </Box>
  );
};

export default SEOAnalysisLoading; 