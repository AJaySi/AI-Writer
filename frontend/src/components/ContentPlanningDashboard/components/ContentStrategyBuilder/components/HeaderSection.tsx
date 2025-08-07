import React from 'react';
import {
  Paper,
  Box,
  Typography
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';

interface HeaderSectionProps {
  autoPopulatedFields: any;
}

const HeaderSection: React.FC<HeaderSectionProps> = ({ autoPopulatedFields }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Paper 
        sx={{ 
          p: 2.5, // More compact padding
          mb: 3, 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)', // Enhanced gradient
          color: 'white',
          borderRadius: 3,
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%)',
            animation: 'shimmer 3s ease-in-out infinite',
          },
          boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3), 0 0 0 1px rgba(255,255,255,0.1)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255,255,255,0.2)',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'relative', zIndex: 1 }}>
          <Box>
            <Typography 
              variant="h4" 
              gutterBottom 
              sx={{ 
                fontWeight: 'bold',
                background: 'linear-gradient(45deg, #fff, #f0f0f0)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                textShadow: '0 0 20px rgba(255,255,255,0.5)',
                mb: 1
              }}
            >
              AI Content Strategy Co-pilot
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9, fontSize: '0.9rem' }}>
              Build a comprehensive content strategy with 30+ strategic inputs
            </Typography>
            
            {/* Auto-population Status - Moved to header (Region 4) */}
            {autoPopulatedFields && Object.keys(autoPopulatedFields).length > 0 && (
              <Box sx={{ mt: 1.5, display: 'flex', alignItems: 'center', gap: 1 }}>
                <CheckCircleIcon sx={{ color: 'rgba(255,255,255,0.8)', fontSize: 18 }} />
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.85rem' }}>
                  {Object.keys(autoPopulatedFields).length} fields auto-populated from onboarding data
                </Typography>
              </Box>
            )}
          </Box>
        </Box>
      </Paper>
    </motion.div>
  );
};

export default HeaderSection; 