import React from 'react';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  Chip,
  IconButton,
  Collapse,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Alert,
  Button
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Psychology as StrategyIcon,
  Search as SearchIcon,
  Analytics as AnalyticsIcon,
  CalendarToday as CalendarIcon,
  HealthAndSafety as HealthIcon
} from '@mui/icons-material';
import { ServiceStatus } from '../../../services/contentPlanningOrchestrator';

interface ProgressIndicatorProps {
  serviceStatuses: ServiceStatus[];
  onRefreshService: (serviceName: string) => void;
  expanded?: boolean;
  onToggleExpanded?: () => void;
}

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({
  serviceStatuses,
  onRefreshService,
  expanded = false,
  onToggleExpanded
}) => {
  const getServiceIcon = (serviceName: string) => {
    switch (serviceName) {
      case 'Content Strategies':
        return <StrategyIcon />;
      case 'Gap Analysis':
        return <SearchIcon />;
      case 'AI Analytics':
        return <AnalyticsIcon />;
      case 'Calendar Events':
        return <CalendarIcon />;
      case 'System Health':
        return <HealthIcon />;
      default:
        return <AnalyticsIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'success';
      case 'error':
        return 'error';
      case 'loading':
        return 'primary';
      default:
        return 'primary';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon color="success" />;
      case 'error':
        return <ErrorIcon color="error" />;
      case 'loading':
        return <RefreshIcon sx={{ animation: 'spin 1s linear infinite' }} />;
      default:
        return null;
    }
  };

  const isLoading = serviceStatuses.some(status => status.status === 'loading');
  const hasErrors = serviceStatuses.some(status => status.status === 'error');
  const allComplete = serviceStatuses.every(status => status.status === 'success');

  const overallProgress = serviceStatuses.reduce((acc, status) => acc + status.progress, 0) / serviceStatuses.length;

  return (
    <Paper 
      elevation={2} 
      sx={{ 
        p: 2, 
        mb: 2,
        border: hasErrors ? '1px solid #f44336' : '1px solid transparent',
        backgroundColor: hasErrors ? 'rgba(244, 67, 54, 0.05)' : 'background.paper',
        '@keyframes spin': {
          from: { transform: 'rotate(0deg)' },
          to: { transform: 'rotate(360deg)' }
        }
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {isLoading && <RefreshIcon sx={{ animation: 'spin 1s linear infinite' }} />}
          Content Planning Progress
          {allComplete && <CheckCircleIcon color="success" />}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Chip 
            label={`${Math.round(overallProgress)}%`}
            color={allComplete ? 'success' : isLoading ? 'primary' : 'default'}
            size="small"
          />
          {onToggleExpanded && (
            <IconButton size="small" onClick={onToggleExpanded}>
              {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
          )}
        </Box>
      </Box>

      {/* Overall Progress Bar */}
      <Box sx={{ mb: 2 }}>
        <LinearProgress 
          variant="determinate" 
          value={overallProgress} 
          color={allComplete ? 'success' : isLoading ? 'primary' : 'inherit'}
          sx={{ height: 8, borderRadius: 4 }}
        />
      </Box>

      {/* Status Messages */}
      {isLoading && (
        <Alert severity="info" sx={{ mb: 2 }}>
          <Typography variant="body2">
            Loading content planning data... This may take a few moments as we analyze your content strategy.
          </Typography>
        </Alert>
      )}

      {hasErrors && (
        <Alert severity="error" sx={{ mb: 2 }}>
          <Typography variant="body2">
            Some services encountered errors. You can refresh individual services below.
          </Typography>
        </Alert>
      )}

      {allComplete && (
        <Alert severity="success" sx={{ mb: 2 }}>
          <Typography variant="body2">
            All content planning services are ready! Your dashboard is fully loaded.
          </Typography>
        </Alert>
      )}

      {/* Detailed Service Status */}
      <Collapse in={expanded}>
        <List dense>
          {serviceStatuses.map((status, index) => (
            <ListItem 
              key={index}
              sx={{ 
                border: '1px solid',
                borderColor: getStatusColor(status.status) === 'error' ? 'error.main' : 'divider',
                borderRadius: 1,
                mb: 1,
                backgroundColor: getStatusColor(status.status) === 'error' ? 'rgba(244, 67, 54, 0.05)' : 'transparent'
              }}
            >
              <ListItemIcon>
                {getServiceIcon(status.name)}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Typography variant="body2" fontWeight="medium">
                      {status.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getStatusIcon(status.status)}
                      <Chip 
                        label={`${status.progress}%`}
                        size="small"
                        color={getStatusColor(status.status)}
                        variant="outlined"
                      />
                    </Box>
                  </Box>
                }
                secondary={
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      {status.message}
                    </Typography>
                    {status.error && (
                      <Typography variant="caption" color="error" sx={{ display: 'block', mt: 0.5 }}>
                        Error: {status.error}
                      </Typography>
                    )}
                    <Box sx={{ mt: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={status.progress} 
                        color={getStatusColor(status.status)}
                        sx={{ height: 4, borderRadius: 2 }}
                      />
                    </Box>
                  </Box>
                }
              />
              {status.status === 'error' && (
                <IconButton 
                  size="small" 
                  onClick={() => onRefreshService(status.name.toLowerCase().replace(' ', ''))}
                  color="primary"
                >
                  <RefreshIcon />
                </IconButton>
              )}
            </ListItem>
          ))}
        </List>
      </Collapse>

      {/* Quick Actions */}
      {hasErrors && (
        <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
          <Button 
            variant="outlined" 
            size="small"
            onClick={() => serviceStatuses.forEach(status => {
              if (status.status === 'error') {
                onRefreshService(status.name.toLowerCase().replace(' ', ''));
              }
            })}
          >
            Refresh All Failed Services
          </Button>
        </Box>
      )}
    </Paper>
  );
};

export default ProgressIndicator; 