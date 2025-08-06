import React from 'react';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  IconButton,
  Chip,
  Collapse,
  Alert
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { ServiceStatus } from '../../../services/contentPlanningOrchestrator';

interface ServiceStatusPanelProps {
  serviceStatuses: ServiceStatus[];
  onRefreshService: (serviceName: string) => void;
  expanded: boolean;
  onToggleExpanded: () => void;
}

const ServiceStatusPanel: React.FC<ServiceStatusPanelProps> = ({
  serviceStatuses,
  onRefreshService,
  expanded,
  onToggleExpanded
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'success';
      case 'error': return 'error';
      case 'loading': return 'primary';
      default: return 'primary';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return <CheckCircleIcon fontSize="small" />;
      case 'error': return <ErrorIcon fontSize="small" />;
      case 'loading': return <WarningIcon fontSize="small" />;
      default: return null;
    }
  };

  const getOverallStatus = () => {
    const hasErrors = serviceStatuses.some(s => s.status === 'error');
    const hasLoading = serviceStatuses.some(s => s.status === 'loading');
    const allSuccess = serviceStatuses.every(s => s.status === 'success');

    if (hasErrors) return { status: 'error', text: 'Some services failed' };
    if (hasLoading) return { status: 'loading', text: 'Services loading' };
    if (allSuccess) return { status: 'success', text: 'All services operational' };
    return { status: 'idle', text: 'Services idle' };
  };

  const overallStatus = getOverallStatus();

  return (
    <Paper sx={{ mb: 2 }}>
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {getStatusIcon(overallStatus.status)}
            <Typography variant="subtitle2">
              System Status: {overallStatus.text}
            </Typography>
            <Chip
              label={`${serviceStatuses.filter(s => s.status === 'success').length}/${serviceStatuses.length}`}
              size="small"
              color={getStatusColor(overallStatus.status)}
              variant="outlined"
            />
          </Box>
          <IconButton size="small" onClick={onToggleExpanded}>
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Box>
      </Box>

      <Collapse in={expanded}>
        <Box sx={{ p: 2 }}>
          {serviceStatuses.map((service) => (
            <Box key={service.name} sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  {getStatusIcon(service.status)}
                  <Typography variant="body2" fontWeight="medium">
                    {service.name}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="caption" color="text.secondary">
                    {service.progress}%
                  </Typography>
                  <IconButton
                    size="small"
                    onClick={() => onRefreshService(service.name.toLowerCase().replace(/\s+/g, ''))}
                    disabled={service.status === 'loading'}
                  >
                    <RefreshIcon fontSize="small" />
                  </IconButton>
                </Box>
              </Box>
              
              <LinearProgress
                variant="determinate"
                value={service.progress}
                color={getStatusColor(service.status)}
                sx={{ mb: 1 }}
              />
              
              <Typography variant="caption" color="text.secondary">
                {service.message}
              </Typography>
              
              {service.error && (
                <Alert severity="error" sx={{ mt: 1 }}>
                  {service.error}
                </Alert>
              )}
            </Box>
          ))}
        </Box>
      </Collapse>
    </Paper>
  );
};

export default ServiceStatusPanel; 