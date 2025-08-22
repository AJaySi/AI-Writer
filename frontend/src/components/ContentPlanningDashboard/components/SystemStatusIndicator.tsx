import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Tooltip, 
  Typography, 
  Chip,
  CircularProgress,
  Alert,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Paper,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Card,
  CardContent,
  CardHeader,
  Avatar,
  Badge
} from '@mui/material';
import {
  CheckCircle as HealthyIcon,
  Warning as WarningIcon,
  Error as CriticalIcon,
  Help as UnknownIcon,
  Refresh as RefreshIcon,
  Close as CloseIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Speed as SpeedIcon,
  BugReport as BugReportIcon,
  Storage as StorageIcon,
  Timeline as TimelineIcon,
  Analytics as AnalyticsIcon,
  NetworkCheck as NetworkCheckIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import MonitoringCharts from './MonitoringCharts';

interface SystemStatusData {
  status: 'healthy' | 'warning' | 'critical' | 'unknown';
  icon: string;
  recent_requests: number;
  recent_errors: number;
  error_rate: number;
  timestamp: string;
}

interface DetailedStatsData {
  overview: {
    total_requests: number;
    total_errors: number;
    recent_requests: number;
    recent_errors: number;
  };
  cache_performance: {
    hits: number;
    misses: number;
    hit_rate: number;
  };
  top_endpoints: Array<{
    endpoint: string;
    count: number;
    avg_time: number;
    errors: number;
    last_called: string;
    cache_hit_rate: number;
  }>;
  recent_errors: Array<{
    timestamp: string;
    path: string;
    method: string;
    status_code: number;
    duration: number;
  }>;
  system_health: {
    status: string;
    error_rate: number;
  };
}

interface SystemStatusIndicatorProps {
  className?: string;
}

const SystemStatusIndicator: React.FC<SystemStatusIndicatorProps> = ({ className }) => {
  const [statusData, setStatusData] = useState<SystemStatusData | null>(null);
  const [detailedStats, setDetailedStats] = useState<DetailedStatsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dashboardOpen, setDashboardOpen] = useState(false);
  const [chartData, setChartData] = useState<any[]>([]);

  const fetchStatus = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/content-planning/monitoring/lightweight-stats');
      if (!response.ok) {
        throw new Error('Failed to fetch system status');
      }
      
      const result = await response.json();
      if (result.status === 'success') {
        setStatusData(result.data);
      } else {
        throw new Error(result.message || 'Failed to get system status');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setStatusData({
        status: 'unknown',
        icon: '⚪',
        recent_requests: 0,
        recent_errors: 0,
        error_rate: 0,
        timestamp: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchDetailedStats = async () => {
    try {
      const response = await fetch('/api/content-planning/monitoring/api-stats');
      if (response.ok) {
        const result = await response.json();
        if (result.status === 'success') {
          setDetailedStats(result.data);
          
          // Generate chart data
          const chartData = result.data.top_endpoints.slice(0, 5).map((endpoint: any, index: number) => ({
            name: endpoint.endpoint.split(' ')[1].split('/').pop() || 'API',
            requests: endpoint.count,
            avgTime: endpoint.avg_time,
            errors: endpoint.errors,
            hitRate: endpoint.cache_hit_rate
          }));
          setChartData(chartData);
        }
      }
    } catch (err) {
      console.error('Error fetching detailed stats:', err);
    }
  };

  useEffect(() => {
    fetchStatus();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (dashboardOpen) {
      fetchDetailedStats();
      const interval = setInterval(fetchDetailedStats, 10000); // Refresh every 10 seconds when dashboard is open
      return () => clearInterval(interval);
    }
  }, [dashboardOpen]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <HealthyIcon sx={{ color: 'success.main', fontSize: 20 }} />;
      case 'warning':
        return <WarningIcon sx={{ color: 'warning.main', fontSize: 20 }} />;
      case 'critical':
        return <CriticalIcon sx={{ color: 'error.main', fontSize: 20 }} />;
      default:
        return <UnknownIcon sx={{ color: 'grey.500', fontSize: 20 }} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'success';
      case 'warning':
        return 'warning';
      case 'critical':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const tooltipContent = statusData ? (
    <Box sx={{ p: 1, maxWidth: 300 }}>
      <Typography variant="subtitle2" gutterBottom>
        System Status: {statusData.status.toUpperCase()}
      </Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>
        Recent Requests: {statusData.recent_requests}
      </Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>
        Recent Errors: {statusData.recent_errors}
      </Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>
        Error Rate: {statusData.error_rate}%
      </Typography>
      <Typography variant="caption" color="text.secondary">
        Last Updated: {formatTimestamp(statusData.timestamp)}
      </Typography>
      <Typography variant="caption" color="primary" sx={{ display: 'block', mt: 1 }}>
        Click for detailed dashboard
      </Typography>
    </Box>
  ) : (
    <Typography>Loading system status...</Typography>
  );

  const handleDashboardClick = () => {
    console.log('Dashboard clicked, setting dashboardOpen to true');
    setDashboardOpen(true);
  };

  if (loading && !statusData) {
    return (
      <Box className={className} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <CircularProgress size={16} />
        <Typography variant="caption">System Status</Typography>
      </Box>
    );
  }

  return (
    <>
      <Box className={className} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Tooltip title={tooltipContent} arrow placement="bottom">
          <Box 
            sx={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}
            onClick={handleDashboardClick}
          >
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              {statusData ? getStatusIcon(statusData.status) : <UnknownIcon />}
            </motion.div>
          </Box>
        </Tooltip>
        
        <Chip
          label={statusData?.status || 'Unknown'}
          size="small"
          color={getStatusColor(statusData?.status || 'unknown')}
          variant="outlined"
          sx={{ height: 24, fontSize: '0.75rem' }}
        />
        
        <IconButton
          size="small"
          onClick={fetchStatus}
          disabled={loading}
          sx={{ p: 0.5 }}
        >
          <RefreshIcon sx={{ fontSize: 16 }} />
        </IconButton>

        {/* Debug button to test dashboard opening */}
        <IconButton
          size="small"
          onClick={handleDashboardClick}
          sx={{ p: 0.5, color: 'primary.main' }}
          title="Open Dashboard (Debug)"
        >
          <AnalyticsIcon sx={{ fontSize: 16 }} />
        </IconButton>
        
        {error && (
          <Alert severity="error" sx={{ fontSize: '0.75rem', py: 0 }}>
            {error}
          </Alert>
        )}
      </Box>

      {/* Enhanced Monitoring Dashboard */}
      <Dialog 
        open={dashboardOpen} 
        onClose={() => {
          console.log('Dialog closing, setting dashboardOpen to false');
          setDashboardOpen(false);
        }}
        maxWidth="lg"
        fullWidth
        sx={{
          '& .MuiDialog-paper': {
            borderRadius: 3,
            background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            maxHeight: '90vh'
          }
        }}
      >
        <DialogTitle sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          borderRadius: '12px 12px 0 0'
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <AnalyticsIcon />
            <Typography variant="h6">System Monitoring Dashboard</Typography>
            {statusData && (
              <Chip 
                label={statusData.status.toUpperCase()} 
                color={getStatusColor(statusData.status)}
                size="small"
                sx={{ color: 'white' }}
              />
            )}
          </Box>
          <IconButton onClick={() => setDashboardOpen(false)} sx={{ color: 'white' }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>

        <DialogContent sx={{ p: 3, overflow: 'auto' }}>
          <Typography variant="body1" sx={{ mb: 2 }}>
            Dashboard is open! Status: {dashboardOpen ? 'Open' : 'Closed'}
          </Typography>
          
          <AnimatePresence>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              {detailedStats ? (
                <MonitoringCharts
                  chartData={chartData}
                  cachePerformance={detailedStats.cache_performance}
                  apiPerformance={{
                    recent_requests: detailedStats.overview.recent_requests,
                    recent_errors: detailedStats.overview.recent_errors,
                    error_rate: detailedStats.system_health.error_rate
                  }}
                />
              ) : (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
                  <CircularProgress size={60} />
                </Box>
              )}

              {/* Recent Errors Section */}
              {detailedStats?.recent_errors && detailedStats.recent_errors.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                >
                  <Card sx={{ mt: 3, background: 'rgba(255,255,255,0.95)' }}>
                    <CardHeader
                      avatar={<Avatar sx={{ bgcolor: 'error.main' }}><BugReportIcon /></Avatar>}
                      title="Recent Errors"
                      subheader="Latest API errors and issues"
                    />
                    <CardContent>
                      <List>
                        {detailedStats.recent_errors.slice(0, 5).map((error, index) => (
                          <ListItem key={index} sx={{ border: '1px solid #f0f0f0', borderRadius: 1, mb: 1 }}>
                            <ListItemIcon>
                              <CriticalIcon color="error" />
                            </ListItemIcon>
                            <ListItemText
                              primary={`${error.method} ${error.path}`}
                              secondary={`Status: ${error.status_code} | Duration: ${error.duration.toFixed(3)}s | ${formatTimestamp(error.timestamp)}`}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                </motion.div>
              )}
            </motion.div>
          </AnimatePresence>
        </DialogContent>

        <DialogActions sx={{ p: 3, background: 'rgba(255,255,255,0.9)' }}>
          <Button 
            onClick={() => setDashboardOpen(false)}
            variant="outlined"
            startIcon={<CloseIcon />}
          >
            Close
          </Button>
          <Button 
            onClick={fetchDetailedStats}
            variant="contained"
            startIcon={<RefreshIcon />}
            disabled={loading}
          >
            Refresh Data
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default SystemStatusIndicator;
