import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  IconButton,
  Tooltip,
  Paper,
  Typography,
  Box,
  Chip,
  Button,
  CircularProgress,
  Divider,
  Grid,
  LinearProgress
} from '@mui/material';
import {
  Psychology as MindIcon,
  Chat as ChatIcon,
  TrendingUp as TrendingIcon,
  Category as CategoryIcon,
  Business as BusinessIcon,
  Person as PersonIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { memoryApi, MemoryStatistics } from '../../../services/memoryApi';

interface MemoryIconProps {
  userId: number;
}

const MemoryIcon: React.FC<MemoryIconProps> = ({ userId }) => {
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const [memoryStats, setMemoryStats] = useState<MemoryStatistics | null>(null);
  const [loading, setLoading] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadMemoryStatistics();
  }, [userId]);

  const loadMemoryStatistics = async () => {
    setLoading(true);
    try {
      const stats = await memoryApi.getMemoryStatistics(userId);
      setMemoryStats(stats);
    } catch (error) {
      console.error('Failed to load memory statistics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMouseEnter = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    // Delay hiding to allow moving to tooltip
    setTimeout(() => {
      if (!isHovered) {
        setAnchorEl(null);
      }
    }, 200);
  };

  const handleChatWithMemories = () => {
    navigate('/memory-chat');
    setAnchorEl(null);
  };

  const getMemoryHealthColor = () => {
    if (!memoryStats?.available) return '#f44336'; // Red
    if (memoryStats.total_memories === 0) return '#ff9800'; // Orange
    if (memoryStats.total_memories < 5) return '#2196f3'; // Blue
    return '#4caf50'; // Green
  };

  const getStatusText = () => {
    if (!memoryStats?.available) return 'Memory service offline';
    if (memoryStats.total_memories === 0) return 'No memories stored yet';
    if (memoryStats.total_memories < 5) return 'Building your memory';
    return 'Memory system active';
  };

  const TooltipContent = () => (
    <Paper
      sx={{
        p: 3,
        maxWidth: 400,
        backgroundColor: 'background.paper',
        boxShadow: 3,
        borderRadius: 2
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <MindIcon sx={{ color: getMemoryHealthColor(), mr: 1, fontSize: 28 }} />
        <Typography variant="h6" component="h3">
          ALwrity Memory
        </Typography>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
          <CircularProgress size={24} />
        </Box>
      ) : memoryStats ? (
        <>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {memoryStats.status_message}
          </Typography>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="primary">
                  {memoryStats.activated_strategies}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Activated
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="secondary">
                  {memoryStats.recent_memories}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  This Week
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={4}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="success.main">
                  {memoryStats.cache_hits}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Cached
                </Typography>
              </Box>
            </Grid>
          </Grid>

          {memoryStats.formatted_categories.length > 0 && (
            <>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle2" sx={{ mb: 1, display: 'flex', alignItems: 'center' }}>
                <CategoryIcon sx={{ fontSize: 16, mr: 0.5 }} />
                Top Categories
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                {memoryStats.formatted_categories.slice(0, 4).map((category) => (
                  <Chip
                    key={category.name}
                    label={`${category.name} (${category.count})`}
                    size="small"
                    variant="outlined"
                    sx={{ fontSize: '0.75rem' }}
                  />
                ))}
              </Box>
            </>
          )}

          {Object.keys(memoryStats.user_types).length > 0 && (
            <>
              <Typography variant="subtitle2" sx={{ mb: 1, display: 'flex', alignItems: 'center' }}>
                <PersonIcon sx={{ fontSize: 16, mr: 0.5 }} />
                User Types
              </Typography>
              <Box sx={{ mb: 2 }}>
                {Object.entries(memoryStats.user_types).map(([type, count]) => (
                  <Box key={type} sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
                    <Typography variant="caption" sx={{ minWidth: 100, textTransform: 'capitalize' }}>
                      {type.replace('_', ' ')}
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={(count / memoryStats.total_memories) * 100}
                      sx={{ flexGrow: 1, mx: 1, height: 4 }}
                    />
                    <Typography variant="caption" color="text.secondary">
                      {count}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </>
          )}

          {Object.keys(memoryStats.industries).length > 0 && (
            <>
              <Typography variant="subtitle2" sx={{ mb: 1, display: 'flex', alignItems: 'center' }}>
                <BusinessIcon sx={{ fontSize: 16, mr: 0.5 }} />
                Industries
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                {Object.entries(memoryStats.industries).slice(0, 3).map(([industry, count]) => (
                  <Chip
                    key={industry}
                    label={`${industry} (${count})`}
                    size="small"
                    color="primary"
                    variant="outlined"
                    sx={{ fontSize: '0.75rem', textTransform: 'capitalize' }}
                  />
                ))}
              </Box>
            </>
          )}

          <Divider sx={{ my: 2 }} />
          
          <Button
            fullWidth
            variant="contained"
            startIcon={<ChatIcon />}
            onClick={handleChatWithMemories}
            sx={{
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 600
            }}
          >
            Chat with your memories
          </Button>

          <Box sx={{ mt: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="caption" color="text.secondary">
              Status: {getStatusText()}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {memoryStats.audit_entries} audit entries
            </Typography>
          </Box>
        </>
      ) : (
        <Typography variant="body2" color="error">
          Failed to load memory statistics
        </Typography>
      )}
    </Paper>
  );

  return (
    <Box>
      <Tooltip
        title={<TooltipContent />}
        open={Boolean(anchorEl)}
        onClose={() => setAnchorEl(null)}
        placement="bottom-end"
        arrow
        PopperProps={{
          disablePortal: true,
          sx: {
            '& .MuiTooltip-tooltip': {
              backgroundColor: 'transparent',
              padding: 0,
              margin: '8px 0',
              maxWidth: 'none'
            }
          }
        }}
      >
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <IconButton
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onClick={() => !anchorEl && handleMouseEnter}
            sx={{
              color: getMemoryHealthColor(),
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
              },
              position: 'relative'
            }}
            aria-label="ALwrity Memory"
          >
            <MindIcon />
            {memoryStats && memoryStats.total_memories > 0 && (
              <Box
                sx={{
                  position: 'absolute',
                  top: 4,
                  right: 4,
                  backgroundColor: 'primary.main',
                  color: 'white',
                  borderRadius: '50%',
                  fontSize: '0.65rem',
                  minWidth: 16,
                  height: 16,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold'
                }}
              >
                {memoryStats.total_memories > 99 ? '99+' : memoryStats.total_memories}
              </Box>
            )}
          </IconButton>
        </motion.div>
      </Tooltip>
    </Box>
  );
};

export default MemoryIcon;