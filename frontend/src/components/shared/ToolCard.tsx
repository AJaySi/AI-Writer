import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Chip, 
  Box, 
  IconButton, 
  Tooltip 
} from '@mui/material';
import { 
  Star as StarIcon, 
  StarBorder as StarBorderIcon 
} from '@mui/icons-material';
import { ToolCardProps } from './types';
import { getStatusConfig } from './utils';

const ToolCard: React.FC<ToolCardProps> = ({
  tool,
  onToolClick,
  isFavorite,
  onToggleFavorite
}) => {
  const config = getStatusConfig(tool.status);

  return (
    <Card
      sx={{
        background: 'rgba(255, 255, 255, 0.08)',
        backdropFilter: 'blur(24px)',
        border: '1px solid rgba(255, 255, 255, 0.12)',
        borderRadius: 3,
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        position: 'relative',
        overflow: 'hidden',
        '&:hover': {
          transform: 'translateY(-8px) scale(1.02)',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
        },
      }}
      onClick={() => onToolClick(tool)}
    >
      <CardContent sx={{ p: 3 }}>
        {/* Header with Icon and Status */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ mr: 2 }}>
            {tool.icon}
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 600, mb: 0.5 }}>
              {tool.name}
            </Typography>
            <Chip
              label={config.label || tool.status}
              size="small"
              sx={{
                background: `${config.color}20`,
                color: config.color,
                border: `1px solid ${config.color}40`,
                fontWeight: 600,
                fontSize: '0.75rem',
              }}
            />
          </Box>
          <Tooltip title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}>
            <IconButton
              onClick={(e) => {
                e.stopPropagation();
                onToggleFavorite(tool.name);
              }}
              sx={{
                color: isFavorite ? '#FFD700' : 'rgba(255, 255, 255, 0.7)',
                '&:hover': {
                  color: isFavorite ? '#FFD700' : 'white',
                },
              }}
            >
              {isFavorite ? <StarIcon /> : <StarBorderIcon />}
            </IconButton>
          </Tooltip>
        </Box>

        {/* Description */}
        <Typography 
          variant="body2" 
          sx={{ 
            color: 'rgba(255, 255, 255, 0.8)', 
            mb: 2,
            lineHeight: 1.6,
            minHeight: '3.2em'
          }}
        >
          {tool.description}
        </Typography>

        {/* Features */}
        {tool.features && tool.features.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', mb: 1, display: 'block' }}>
              Features:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {tool.features.slice(0, 3).map((feature, index) => (
                <Chip
                  key={index}
                  label={feature}
                  size="small"
                  sx={{
                    background: 'rgba(255, 255, 255, 0.1)',
                    color: 'rgba(255, 255, 255, 0.8)',
                    fontSize: '0.7rem',
                    height: '20px',
                  }}
                />
              ))}
              {tool.features.length > 3 && (
                <Chip
                  label={`+${tool.features.length - 3} more`}
                  size="small"
                  sx={{
                    background: 'rgba(255, 255, 255, 0.1)',
                    color: 'rgba(255, 255, 255, 0.6)',
                    fontSize: '0.7rem',
                    height: '20px',
                  }}
                />
              )}
            </Box>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ToolCard; 