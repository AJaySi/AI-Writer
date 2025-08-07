import React from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  IconButton,
  Badge,
  Tooltip as MuiTooltip
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  AutoAwesome as AutoAwesomeIcon,
  Info as InfoIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';

interface ProgressTrackerProps {
  reviewProgressPercentage: number;
  reviewedCategoriesCount: number;
  totalCategories: number;
  autoPopulatedFields: any;
  aiGenerating: boolean;
  onShowAIRecommendations: () => void;
  onShowDataSourceTransparency: () => void;
  onRefreshData: () => void;
}

const ProgressTracker: React.FC<ProgressTrackerProps> = ({
  reviewProgressPercentage,
  reviewedCategoriesCount,
  totalCategories,
  autoPopulatedFields,
  aiGenerating,
  onShowAIRecommendations,
  onShowDataSourceTransparency,
  onRefreshData
}) => {
  return (
    <Box sx={{ mb: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1.5 }}>
        <Typography variant="h6" gutterBottom sx={{ mb: 0 }}>
          Progress
        </Typography>
        {/* Spiral Progress - Moved from Region 2 to Region 3 */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ position: 'relative', display: 'inline-flex' }}>
            <CircularProgress
              variant="determinate"
              value={reviewProgressPercentage}
              size={40}
              thickness={4}
              sx={{
                color: 'primary.main',
                '& .MuiCircularProgress-circle': {
                  strokeLinecap: 'round',
                }
              }}
            />
            <Box
              sx={{
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                position: 'absolute',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Typography
                variant="caption"
                component="div"
                color="text.secondary"
                sx={{ fontSize: '0.7rem', fontWeight: 'bold' }}
              >
                {`${Math.round(reviewProgressPercentage)}%`}
              </Typography>
            </Box>
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
            {reviewedCategoriesCount}/{totalCategories}
          </Typography>
        </Box>
      </Box>
      
      {/* Status Indicators - Compact */}
      <Box sx={{ mb: 1.5 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 0.5 }}>
          <CheckCircleIcon color="success" fontSize="small" sx={{ fontSize: 14 }} />
          <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
            Auto-population: {Object.keys(autoPopulatedFields || {}).length} fields
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <AutoAwesomeIcon color="primary" fontSize="small" sx={{ fontSize: 14 }} />
          <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
            AI Insights: {aiGenerating ? 'Generating...' : 'Ready'}
          </Typography>
        </Box>
      </Box>

      {/* Icons moved from Region A to Region B - Now integrated into Progress title area */}
      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', mt: 1.5 }}>
        {/* AI Recommendations Button - Compact */}
        <MuiTooltip title="View AI-powered recommendations and insights" placement="top">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <IconButton 
              onClick={onShowAIRecommendations}
              sx={{ 
                color: 'primary.main', 
                bgcolor: 'rgba(255, 193, 7, 0.1)',
                border: '1px solid rgba(255, 193, 7, 0.3)',
                '&:hover': { 
                  bgcolor: 'rgba(255, 193, 7, 0.2)',
                  transform: 'translateY(-1px)',
                  boxShadow: '0 4px 12px rgba(255, 193, 7, 0.3)'
                },
                transition: 'all 0.3s ease',
                width: 36,
                height: 36
              }}
            >
              <Badge 
                badgeContent={5} 
                sx={{
                  '& .MuiBadge-badge': {
                    fontSize: '0.6rem',
                    fontWeight: 'bold',
                    animation: 'pulse 2s infinite',
                    bgcolor: '#ff6b35',
                    color: 'white'
                  }
                }}
              >
                <AutoAwesomeIcon sx={{ fontSize: 16 }} />
              </Badge>
            </IconButton>
          </motion.div>
        </MuiTooltip>
        
        {/* Data Source Transparency Button - Compact */}
        <MuiTooltip title="View data sources and transparency information" placement="top">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <IconButton 
              onClick={onShowDataSourceTransparency}
              sx={{ 
                color: 'primary.main', 
                bgcolor: 'rgba(76, 175, 80, 0.1)',
                border: '1px solid rgba(76, 175, 80, 0.3)',
                '&:hover': { 
                  bgcolor: 'rgba(76, 175, 80, 0.2)',
                  transform: 'translateY(-1px)',
                  boxShadow: '0 4px 12px rgba(76, 175, 80, 0.3)'
                },
                transition: 'all 0.3s ease',
                width: 36,
                height: 36
              }}
            >
              <Badge
                badgeContent={Object.keys(autoPopulatedFields || {}).length} 
                sx={{
                  '& .MuiBadge-badge': {
                    fontSize: '0.6rem',
                    fontWeight: 'bold',
                    animation: 'pulse 2s infinite',
                    bgcolor: '#2196f3',
                    color: 'white'
                  }
                }}
              >
                <InfoIcon sx={{ fontSize: 16 }} />
              </Badge>
            </IconButton>
          </motion.div>
        </MuiTooltip>
        
        {/* Refresh Button - Compact */}
        <MuiTooltip title="Refresh auto-populated data" placement="top">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <IconButton 
              onClick={onRefreshData}
              sx={{ 
                color: 'primary.main', 
                bgcolor: 'rgba(0,0,0,0.05)',
                border: '1px solid rgba(0,0,0,0.1)',
                '&:hover': { 
                  bgcolor: 'rgba(0,0,0,0.1)',
                  transform: 'translateY(-1px)',
                  boxShadow: '0 4px 12px rgba(0,0,0,0.2)'
                },
                transition: 'all 0.3s ease',
                width: 36,
                height: 36
              }}
            >
              <RefreshIcon sx={{ fontSize: 16 }} />
            </IconButton>
          </motion.div>
        </MuiTooltip>
      </Box>
    </Box>
  );
};

export default ProgressTracker; 