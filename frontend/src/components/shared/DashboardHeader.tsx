import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { ShimmerHeader } from './styled';
import { DashboardHeaderProps } from './types';

const DashboardHeader: React.FC<DashboardHeaderProps> = ({ 
  title, 
  subtitle, 
  statusChips = [] 
}) => {
  return (
    <ShimmerHeader sx={{ mb: 5 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
        <Box>
          <Typography variant="h2" component="h1" sx={{ 
            fontWeight: 800, 
            color: 'white',
            textShadow: '0 4px 8px rgba(0,0,0,0.3)',
            mb: 1,
            fontSize: { xs: '2rem', md: '3rem' },
            background: 'linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>
            {title}
          </Typography>
          <Typography variant="h5" sx={{ 
            color: 'rgba(255, 255, 255, 0.9)',
            fontWeight: 400,
            fontSize: { xs: '1rem', md: '1.25rem' },
          }}>
            {subtitle}
          </Typography>
        </Box>
        {statusChips.length > 0 && (
          <Box sx={{ display: 'flex', gap: 1.5 }}>
            {statusChips.map((chip, index) => (
              <Chip 
                key={index}
                icon={chip.icon} 
                label={chip.label} 
                sx={{ 
                  background: `${chip.color}20`,
                  border: `1px solid ${chip.color}40`,
                  color: chip.color,
                  fontWeight: 700,
                }}
              />
            ))}
          </Box>
        )}
      </Box>
    </ShimmerHeader>
  );
};

export default DashboardHeader; 