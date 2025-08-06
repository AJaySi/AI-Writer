import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { CategoryHeaderProps } from './types';

const CategoryHeader: React.FC<CategoryHeaderProps> = ({ 
  categoryName, 
  category, 
  theme 
}) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      alignItems: 'center', 
      gap: 2, 
      mb: 4,
      p: 3,
      background: 'rgba(255, 255, 255, 0.08)',
      borderRadius: 3,
      border: '1px solid rgba(255, 255, 255, 0.15)',
      backdropFilter: 'blur(20px)',
      position: 'relative',
      overflow: 'hidden',
      '&::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '3px',
        background: category.gradient,
        borderRadius: '3px 3px 0 0',
      },
    }}>
      <Box
        sx={{
          width: 56,
          height: 56,
          borderRadius: 3,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: `${category.color}20`,
          border: `2px solid ${category.color}40`,
          boxShadow: `0 8px 24px ${category.color}30`,
          position: 'relative',
          '&::after': {
            content: '""',
            position: 'absolute',
            top: -2,
            left: -2,
            right: -2,
            bottom: -2,
            background: category.gradient,
            borderRadius: 3,
            zIndex: -1,
            opacity: 0.3,
          },
        }}
      >
        {category.icon}
      </Box>
      <Box sx={{ flex: 1 }}>
        <Typography variant="h3" sx={{ 
          fontWeight: 800, 
          color: 'white',
          textShadow: '0 2px 4px rgba(0,0,0,0.3)',
          fontSize: { xs: '1.75rem', md: '2.25rem' },
          mb: 0.5,
        }}>
          {categoryName}
        </Typography>
        <Typography variant="body1" sx={{ 
          color: 'rgba(255, 255, 255, 0.8)',
          fontWeight: 500,
        }}>
          {'subCategories' in category ? 
            `${Object.keys(category.subCategories).length} sub-categories` : 
            `${category.tools.length} tools`
          }
        </Typography>
      </Box>
      <Chip 
        label={'subCategories' in category ? 
          `${Object.values(category.subCategories).flatMap(subCat => subCat.tools).length} tools` : 
          `${category.tools.length} tools`
        } 
        size="medium"
        sx={{ 
          background: 'rgba(255, 255, 255, 0.15)',
          color: 'rgba(255, 255, 255, 0.9)',
          fontWeight: 700,
          fontSize: '0.9rem',
          height: '32px',
          border: '1px solid rgba(255, 255, 255, 0.2)',
        }}
      />
    </Box>
  );
};

export default CategoryHeader; 