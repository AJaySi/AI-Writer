import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  IconButton,
  Tooltip,
  Alert,
  AlertTitle,
  CircularProgress,
  LinearProgress,
  Divider,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Assessment as AssessmentIcon,
  Speed as SpeedIcon,
  Visibility as VisibilityIcon,
  People as EngagementIcon,
  MonetizationOn as MonetizationOnIcon,
  Refresh as RefreshIcon,
  AutoAwesome as AutoAwesomeIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Analytics as AnalyticsIcon,
  Lightbulb as LightbulbIcon,
  Timeline as TimelineIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

// Import our advanced chart components
import {
  PerformanceTrendChart,
  QualityMetricsRadar,
  PerformanceMetricsBar,
  ContentDistributionPie,
  PerformanceGauge
} from '../../../../shared/charts/AdvancedChartComponents';

// Import real-time data hook
import { useMockRealTimeData } from '../../../../../hooks/useRealTimeData';

// Import API services
import { strategyMonitoringApi } from '../../../../../services/strategyMonitoringApi';

interface EnhancedPerformanceVisualizationProps {
  strategyId: number;
  strategyData: any;
}

interface QualityAnalysisData {
  overall_score: number;
  overall_status: string;
  metrics: Array<{
    name: string;
    score: number;
    status: string;
    description: string;
    recommendations: string[];
  }>;
  recommendations: string[];
  confidence_score: number;
}

const EnhancedPerformanceVisualization: React.FC<EnhancedPerformanceVisualizationProps> = ({
  strategyId,
  strategyData
}) => {
  const [qualityAnalysis, setQualityAnalysis] = useState<QualityAnalysisData | null>(null);
  const [loadingQuality, setLoadingQuality] = useState(false);
  const [showQualityDialog, setShowQualityDialog] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Use real-time data hook
  const { data: realTimeData, isConnected, error: realTimeError } = useMockRealTimeData(strategyId);

  useEffect(() => {
    loadQualityAnalysis();
  }, [strategyId]);

  const loadQualityAnalysis = async () => {
    try {
      setLoadingQuality(true);
      setError(null);
      
      // Call the quality analysis API
      const response = await strategyMonitoringApi.getQualityAnalysis(strategyId);
      setQualityAnalysis(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load quality analysis');
      console.error('Error loading quality analysis:', err);
    } finally {
      setLoadingQuality(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'success';
      case 'good': return 'info';
      case 'needs_attention': return 'warning';
      case 'poor': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'excellent': return <CheckCircleIcon />;
      case 'good': return <CheckCircleIcon />;
      case 'needs_attention': return <WarningIcon />;
      case 'poor': return <ErrorIcon />;
      default: return <AssessmentIcon />;
    }
  };

  // Prepare chart data from real-time data
  const trendData = realTimeData?.trends?.daily || [];
  const qualityMetricsData = qualityAnalysis?.metrics?.map(metric => ({
    metric: metric.name,
    score: metric.score,
    target: 85 // Target score
  })) || [];

  const performanceMetricsData = realTimeData?.metrics ? [
    {
      metric: 'Traffic Growth',
      value: realTimeData.metrics.traffic_growth_percentage,
      target: 15,
      status: (realTimeData.metrics.traffic_growth_percentage >= 15 ? 'excellent' : 
              realTimeData.metrics.traffic_growth_percentage >= 10 ? 'good' : 'needs_attention') as 'excellent' | 'good' | 'needs_attention'
    },
    {
      metric: 'Engagement Rate',
      value: realTimeData.metrics.engagement_rate_percentage,
      target: 8,
      status: (realTimeData.metrics.engagement_rate_percentage >= 8 ? 'excellent' : 
              realTimeData.metrics.engagement_rate_percentage >= 6 ? 'good' : 'needs_attention') as 'excellent' | 'good' | 'needs_attention'
    },
    {
      metric: 'Conversion Rate',
      value: realTimeData.metrics.conversion_rate_percentage,
      target: 2.5,
      status: (realTimeData.metrics.conversion_rate_percentage >= 2.5 ? 'excellent' : 
              realTimeData.metrics.conversion_rate_percentage >= 2 ? 'good' : 'needs_attention') as 'excellent' | 'good' | 'needs_attention'
    },
    {
      metric: 'Content Quality',
      value: realTimeData.metrics.content_quality_score,
      target: 90,
      status: (realTimeData.metrics.content_quality_score >= 90 ? 'excellent' : 
              realTimeData.metrics.content_quality_score >= 80 ? 'good' : 'needs_attention') as 'excellent' | 'good' | 'needs_attention'
    }
  ] : [];

  const contentDistributionData = [
    { name: 'Blog Posts', value: 40, color: '#667eea' },
    { name: 'Social Media', value: 25, color: '#764ba2' },
    { name: 'Video Content', value: 20, color: '#4caf50' },
    { name: 'Infographics', value: 10, color: '#ff9800' },
    { name: 'Newsletters', value: 5, color: '#f44336' }
  ];

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        <AlertTitle>Error Loading Performance Data</AlertTitle>
        {error}
      </Alert>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
    >
      {/* Header Section */}
      <Box sx={{ mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="h4" sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(45deg, #667eea, #764ba2)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 1
            }}>
              🚀 Advanced Performance Dashboard
            </Typography>
            <Typography variant="body1" sx={{ color: 'text.secondary' }}>
              Real-time monitoring and AI-powered quality analysis for your content strategy
            </Typography>
          </Box>
          
          <Box display="flex" alignItems="center" gap={2}>
            <Chip
              icon={isConnected ? <CheckCircleIcon /> : <ErrorIcon />}
              label={isConnected ? 'Live Data' : 'Offline'}
              color={isConnected ? 'success' : 'error'}
              size="small"
            />
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Last updated: {realTimeData?.timestamp ? new Date(realTimeData.timestamp).toLocaleString() : 'N/A'}
            </Typography>
            <Tooltip title="Refresh data">
              <IconButton onClick={loadQualityAnalysis} sx={{ color: 'primary.main' }}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
        
        <Divider sx={{ mb: 3 }} />
      </Box>

      {/* Real-time Performance Gauges */}
      {realTimeData?.metrics && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={6} lg={3}>
            <PerformanceGauge
              value={realTimeData.metrics.traffic_growth_percentage}
              maxValue={25}
              title="Traffic Growth"
              color="#667eea"
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <PerformanceGauge
              value={realTimeData.metrics.engagement_rate_percentage}
              maxValue={15}
              title="Engagement Rate"
              color="#4caf50"
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <PerformanceGauge
              value={realTimeData.metrics.conversion_rate_percentage}
              maxValue={5}
              title="Conversion Rate"
              color="#ff9800"
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <PerformanceGauge
              value={realTimeData.metrics.content_quality_score}
              maxValue={100}
              title="Content Quality"
              color="#2196f3"
            />
          </Grid>
        </Grid>
      )}

      {/* Quality Analysis Section */}
      <Box sx={{ mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            <AutoAwesomeIcon sx={{ mr: 1, color: 'primary.main' }} />
            AI Quality Analysis
          </Typography>
          <Button
            variant="outlined"
            startIcon={<AnalyticsIcon />}
            onClick={() => setShowQualityDialog(true)}
            disabled={loadingQuality}
          >
            {loadingQuality ? 'Analyzing...' : 'View Detailed Analysis'}
          </Button>
        </Box>

        {qualityAnalysis && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card elevation={2}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Overall Quality Score
                  </Typography>
                  <Box display="flex" alignItems="center" gap={2}>
                    <Typography variant="h3" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      {qualityAnalysis.overall_score.toFixed(1)}
                    </Typography>
                    <Box>
                      <Chip
                        icon={getStatusIcon(qualityAnalysis.overall_status)}
                        label={qualityAnalysis.overall_status.replace('_', ' ').toUpperCase()}
                        color={getStatusColor(qualityAnalysis.overall_status) as any}
                        size="small"
                      />
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Confidence: {qualityAnalysis.confidence_score.toFixed(1)}%
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card elevation={2}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Priority Areas
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {qualityAnalysis.metrics
                      .filter(metric => metric.status === 'needs_attention' || metric.status === 'poor')
                      .map((metric, index) => (
                        <Chip
                          key={index}
                          label={metric.name}
                          color={getStatusColor(metric.status) as any}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    {qualityAnalysis.metrics.filter(m => m.status === 'needs_attention' || m.status === 'poor').length === 0 && (
                      <Typography variant="body2" color="text.secondary">
                        All areas are performing well! 🎉
                      </Typography>
                    )}
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </Box>

      {/* Advanced Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Performance Trends Chart */}
        <Grid item xs={12} lg={8}>
          <PerformanceTrendChart
            data={trendData}
            title="Performance Trends Over Time"
            height={400}
          />
        </Grid>

        {/* Content Distribution Chart */}
        <Grid item xs={12} lg={4}>
          <ContentDistributionPie
            data={contentDistributionData}
            title="Content Distribution"
            height={400}
          />
        </Grid>

        {/* Quality Metrics Radar Chart */}
        <Grid item xs={12} lg={6}>
          <QualityMetricsRadar
            data={qualityMetricsData}
            title="Quality Metrics Analysis"
            height={400}
          />
        </Grid>

        {/* Performance Metrics Bar Chart */}
        <Grid item xs={12} lg={6}>
          <PerformanceMetricsBar
            data={performanceMetricsData}
            title="Performance vs Targets"
            height={400}
          />
        </Grid>
      </Grid>

      {/* Quality Analysis Dialog */}
      <Dialog
        open={showQualityDialog}
        onClose={() => setShowQualityDialog(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box display="flex" alignItems="center" gap={1}>
              <AutoAwesomeIcon color="primary" />
              <Typography variant="h6">AI Quality Analysis Details</Typography>
            </Box>
            <IconButton onClick={() => setShowQualityDialog(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          {qualityAnalysis && (
            <Box>
              {/* Overall Score */}
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Overall Quality Assessment
                  </Typography>
                  <Box display="flex" alignItems="center" gap={2}>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      {qualityAnalysis.overall_score.toFixed(1)}/100
                    </Typography>
                    <Chip
                      icon={getStatusIcon(qualityAnalysis.overall_status)}
                      label={qualityAnalysis.overall_status.replace('_', ' ').toUpperCase()}
                      color={getStatusColor(qualityAnalysis.overall_status) as any}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Confidence Score: {qualityAnalysis.confidence_score.toFixed(1)}%
                  </Typography>
                </CardContent>
              </Card>

              {/* Detailed Metrics */}
              <Typography variant="h6" gutterBottom>
                Detailed Quality Metrics
              </Typography>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                {qualityAnalysis.metrics.map((metric, index) => (
                  <Grid item xs={12} md={6} key={index}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                          <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                            {metric.name}
                          </Typography>
                          <Chip
                            label={`${metric.score.toFixed(1)}/100`}
                            color={getStatusColor(metric.status) as any}
                            size="small"
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          {metric.description}
                        </Typography>
                        <Chip
                          icon={getStatusIcon(metric.status)}
                          label={metric.status.replace('_', ' ').toUpperCase()}
                          color={getStatusColor(metric.status) as any}
                          size="small"
                          variant="outlined"
                        />
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>

              {/* Recommendations */}
              <Typography variant="h6" gutterBottom>
                <LightbulbIcon sx={{ mr: 1, color: 'warning.main' }} />
                AI Recommendations
              </Typography>
              <List>
                {qualityAnalysis.recommendations.map((recommendation, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <LightbulbIcon color="warning" />
                    </ListItemIcon>
                    <ListItemText primary={recommendation} />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowQualityDialog(false)}>Close</Button>
          <Button 
            variant="contained" 
            onClick={loadQualityAnalysis}
            disabled={loadingQuality}
          >
            Refresh Analysis
          </Button>
        </DialogActions>
      </Dialog>
    </motion.div>
  );
};

export default EnhancedPerformanceVisualization;
