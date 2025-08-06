import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  Divider,
  Alert,
  CircularProgress,
  LinearProgress
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Analytics as AnalyticsIcon,
  ShowChart as ShowChartIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { useContentPlanningStore } from '../../../stores/contentPlanningStore';
import { contentPlanningApi } from '../../../services/contentPlanningApi';

const AnalyticsTab: React.FC = () => {
  const { 
    performanceMetrics, 
    aiInsights, 
    loading, 
    error,
    loadAIInsights,
    loadAIRecommendations
  } = useContentPlanningStore();
  
  const [analyticsData, setAnalyticsData] = useState<any>(null);
  const [dataLoading, setDataLoading] = useState(false);

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    try {
      setDataLoading(true);
      
      console.log('Loading analytics data...');
      
      // Load AI insights and recommendations
      await Promise.all([
        loadAIInsights(),
        loadAIRecommendations()
      ]);
      
      // Load analytics data from backend
      const response = await contentPlanningApi.getAIAnalyticsSafe();
      
      console.log('Analytics Response:', response);
      
      if (response) {
        const analyticsData = {
          performance_trends: response.performance_trends || {},
          content_evolution: response.content_evolution || {},
          engagement_patterns: response.engagement_patterns || {},
          recommendations: response.recommendations || [],
          insights: response.insights || []
        };
        
        console.log('Analytics Data:', analyticsData);
        setAnalyticsData(analyticsData);
      }
    } catch (error) {
      console.error('Error loading analytics data:', error);
    } finally {
      setDataLoading(false);
    }
  };

  const getPerformanceColor = (value: number) => {
    if (value >= 80) return 'success';
    if (value >= 60) return 'warning';
    return 'error';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Performance Analytics
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {dataLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {/* Performance Overview */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                <AnalyticsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Performance Overview
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {performanceMetrics ? (
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Engagement Rate
                    </Typography>
                    <Typography variant="h4" color={getPerformanceColor(performanceMetrics.engagement)}>
                      {performanceMetrics.engagement}%
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Reach
                    </Typography>
                    <Typography variant="h4" color="primary">
                      {performanceMetrics.reach.toLocaleString()}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Conversion Rate
                    </Typography>
                    <Typography variant="h4" color={getPerformanceColor(performanceMetrics.conversion)}>
                      {performanceMetrics.conversion}%
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      ROI
                    </Typography>
                    <Typography variant="h4" color="success.main">
                      ${performanceMetrics.roi.toLocaleString()}
                    </Typography>
                  </Grid>
                </Grid>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No performance data available
                </Typography>
              )}
            </Paper>
          </Grid>

          {/* AI Insights */}
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                <AssessmentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                AI Insights
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {aiInsights && aiInsights.length > 0 ? (
                <Box>
                  {aiInsights.slice(0, 3).map((insight, index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        {insight.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        {insight.description}
                      </Typography>
                      <Chip 
                        label={insight.priority} 
                        color={insight.priority === 'high' ? 'error' : insight.priority === 'medium' ? 'warning' : 'success'}
                        size="small"
                      />
                    </Box>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No AI insights available
                </Typography>
              )}
            </Paper>
          </Grid>

          {/* Content Evolution */}
          {analyticsData && analyticsData.content_evolution && (
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <ShowChartIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Content Evolution
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {analyticsData.content_evolution.content_types ? (
                  <Box>
                    {analyticsData.content_evolution.content_types.map((contentType: string, index: number) => {
                      const performance = analyticsData.content_evolution.performance_by_type?.[contentType];
                      return (
                        <Box key={index} sx={{ mb: 2 }}>
                          <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
                            {contentType.replace('_', ' ')}
                          </Typography>
                          {performance && (
                            <Grid container spacing={1}>
                              <Grid item xs={6}>
                                <Typography variant="body2" color="text.secondary">
                                  Growth
                                </Typography>
                                <Typography variant="h6" color="success.main">
                                  +{performance.growth}%
                                </Typography>
                              </Grid>
                              <Grid item xs={6}>
                                <Typography variant="body2" color="text.secondary">
                                  Engagement
                                </Typography>
                                <Typography variant="h6">
                                  {performance.engagement}%
                                </Typography>
                              </Grid>
                            </Grid>
                          )}
                        </Box>
                      );
                    })}
                  </Box>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No content evolution data available
                  </Typography>
                )}
              </Paper>
            </Grid>
          )}

          {/* Performance Trends */}
          {analyticsData && analyticsData.performance_trends && (
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Performance Trends
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {analyticsData.performance_trends.engagement_trend ? (
                  <Box>
                    <Typography variant="subtitle2" gutterBottom>
                      Engagement Trend (Last 5 periods)
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {analyticsData.performance_trends.engagement_trend.map((value: number, index: number) => (
                        <Box key={index} sx={{ flex: 1, textAlign: 'center' }}>
                          <Typography variant="h6" color="primary">
                            {value}%
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Period {index + 1}
                          </Typography>
                        </Box>
                      ))}
                    </Box>
                  </Box>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No trend data available
                  </Typography>
                )}
              </Paper>
            </Grid>
          )}

          {/* Engagement Patterns */}
          {analyticsData && analyticsData.engagement_patterns && (
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <AnalyticsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Engagement Patterns
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Grid container spacing={3}>
                  {analyticsData.engagement_patterns.peak_times && (
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle2" gutterBottom>
                        Peak Engagement Times
                      </Typography>
                      {analyticsData.engagement_patterns.peak_times.map((time: string, index: number) => (
                        <Chip 
                          key={index}
                          label={time} 
                          color="primary" 
                          variant="outlined"
                          sx={{ mr: 1, mb: 1 }}
                        />
                      ))}
                    </Grid>
                  )}
                  
                  {analyticsData.engagement_patterns.best_days && (
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle2" gutterBottom>
                        Best Performing Days
                      </Typography>
                      {analyticsData.engagement_patterns.best_days.map((day: string, index: number) => (
                        <Chip 
                          key={index}
                          label={day} 
                          color="success" 
                          variant="outlined"
                          sx={{ mr: 1, mb: 1 }}
                        />
                      ))}
                    </Grid>
                  )}
                  
                  {analyticsData.engagement_patterns.audience_segments && (
                    <Grid item xs={12} md={4}>
                      <Typography variant="subtitle2" gutterBottom>
                        Top Audience Segments
                      </Typography>
                      {analyticsData.engagement_patterns.audience_segments.map((segment: string, index: number) => (
                        <Chip 
                          key={index}
                          label={segment.replace('_', ' ')} 
                          color="secondary" 
                          variant="outlined"
                          sx={{ mr: 1, mb: 1 }}
                        />
                      ))}
                    </Grid>
                  )}
                </Grid>
              </Paper>
            </Grid>
          )}

          {/* Recommendations */}
          {analyticsData && analyticsData.recommendations && analyticsData.recommendations.length > 0 && (
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <AssessmentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  AI Recommendations
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Grid container spacing={2}>
                  {analyticsData.recommendations.map((recommendation: any, index: number) => (
                    <Grid item xs={12} md={6} key={index}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle1" gutterBottom>
                            {recommendation.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {recommendation.description}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Chip 
                              label={recommendation.type} 
                              color="primary" 
                              size="small"
                            />
                            <Chip 
                              label={`${(recommendation.confidence * 100).toFixed(0)}% confidence`} 
                              color="success" 
                              size="small"
                            />
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Grid>
          )}
        </Grid>
      )}
    </Box>
  );
};

export default AnalyticsTab; 