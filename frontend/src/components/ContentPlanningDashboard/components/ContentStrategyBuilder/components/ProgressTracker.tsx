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
    <Box sx={{ mb: 1.5 }}>
      {/* Compact header row with title, progress, counts and actions */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.75 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography variant="h6" sx={{ mb: 0, fontSize: '1rem' }}>
            Progress
          </Typography>
          <Box sx={{ position: 'relative', display: 'inline-flex' }}>
            <CircularProgress
              variant="determinate"
              value={reviewProgressPercentage}
              size={28}
              thickness={4}
              sx={{ color: 'primary.main', '& .MuiCircularProgress-circle': { strokeLinecap: 'round' } }}
            />
            <Box sx={{ top: 0, left: 0, bottom: 0, right: 0, position: 'absolute', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Typography variant="caption" component="div" color="text.secondary" sx={{ fontSize: '0.65rem', fontWeight: 700 }}>
                {`${Math.round(reviewProgressPercentage)}%`}
              </Typography>
            </Box>
          </Box>
          <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
            {reviewedCategoriesCount}/{totalCategories}
          </Typography>
        </Box>

        {/* Actions inline in header */}
        <Box sx={{ display: 'flex', gap: 0.75 }}>
          <MuiTooltip title="View AI-powered recommendations and insights" placement="top">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <IconButton 
                onClick={onShowAIRecommendations}
                sx={{ color: 'primary.main', bgcolor: 'rgba(255, 193, 7, 0.08)', border: '1px solid rgba(255, 193, 7, 0.25)', width: 32, height: 32, '&:hover': { bgcolor: 'rgba(255, 193, 7, 0.16)' } }}
              >
                <Badge badgeContent={5} sx={{ '& .MuiBadge-badge': { fontSize: '0.55rem', fontWeight: 700, bgcolor: '#ff6b35', color: 'white' } }}>
                  <AutoAwesomeIcon sx={{ fontSize: 16 }} />
                </Badge>
              </IconButton>
            </motion.div>
          </MuiTooltip>

          <MuiTooltip title="View data sources and transparency information" placement="top">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <IconButton 
                onClick={onShowDataSourceTransparency}
                sx={{ color: 'primary.main', bgcolor: 'rgba(76, 175, 80, 0.08)', border: '1px solid rgba(76, 175, 80, 0.25)', width: 32, height: 32, '&:hover': { bgcolor: 'rgba(76, 175, 80, 0.16)' } }}
              >
                <Badge badgeContent={Object.keys(autoPopulatedFields || {}).length} sx={{ '& .MuiBadge-badge': { fontSize: '0.55rem', fontWeight: 700, bgcolor: '#2196f3', color: 'white' } }}>
                  <InfoIcon sx={{ fontSize: 16 }} />
                </Badge>
              </IconButton>
            </motion.div>
          </MuiTooltip>

          <MuiTooltip title="Refresh auto-populated data" placement="top">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <IconButton onClick={onRefreshData} sx={{ color: 'primary.main', bgcolor: 'rgba(0,0,0,0.04)', border: '1px solid rgba(0,0,0,0.12)', width: 32, height: 32, '&:hover': { bgcolor: 'rgba(0,0,0,0.08)' } }}>
                <RefreshIcon sx={{ fontSize: 16 }} />
              </IconButton>
            </motion.div>
          </MuiTooltip>
        </Box>
      </Box>

      {/* Combined info line */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <CheckCircleIcon color="success" sx={{ fontSize: 14 }} />
        <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
          Auto-population: {Object.keys(autoPopulatedFields || {}).length} fields • AI Insights: {aiGenerating ? 'Generating...' : 'Ready'}
        </Typography>
      </Box>
    </Box>
  );
};

export default ProgressTracker; 