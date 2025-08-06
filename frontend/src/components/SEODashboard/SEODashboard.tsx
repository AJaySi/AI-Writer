import React, { useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  Alert,
  Skeleton,
  useTheme
} from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';

// Shared components
import { DashboardContainer, GlassCard } from '../shared/styled';
import SEOAnalyzerPanel from './components/SEOAnalyzerPanel';

// Zustand store
import { useSEODashboardStore } from '../../stores/seoDashboardStore';

// API
import { userDataAPI } from '../../api/userData';

// SEO Dashboard component
const SEODashboard: React.FC = () => {
  const theme = useTheme();
  
  // Zustand store hooks
  const {
    loading,
    error,
    data,
    analysisData,
    analysisLoading,
    analysisError,
    setData,
    setLoading,
    setError,
    runSEOAnalysis,
    checkAndRunInitialAnalysis,
  } = useSEODashboardStore();

  useEffect(() => {
    // Simulate fetching dashboard data
    const fetchData = async () => {
      setLoading(true);
      try {
        // Try to get the website URL from the database
        let websiteUrl = null;
        try {
          websiteUrl = await userDataAPI.getWebsiteURL();
          console.log('Fetched website URL from database:', websiteUrl);
        } catch (error) {
          console.warn('Could not fetch website URL from database:', error);
        }
        
        // Mock data for now
        const mockData = {
          health_score: {
            score: 85,
            change: 5,
            trend: 'up',
            label: 'GOOD',
            color: '#4CAF50'
          },
          key_insight: 'Your SEO is performing well with room for improvement',
          priority_alert: 'No critical issues detected',
          metrics: {
            traffic: { value: 12500, change: 12, trend: 'up', description: 'Organic traffic', color: '#4CAF50' },
            rankings: { value: 8.5, change: -0.3, trend: 'down', description: 'Average ranking', color: '#2196F3' },
            mobile: { value: 92, change: 3, trend: 'up', description: 'Mobile speed', color: '#FF9800' },
            keywords: { value: 150, change: 5, trend: 'up', description: 'Keywords tracked', color: '#9C27B0' }
          },
          platforms: {
            google: { status: 'connected', connected: true, last_sync: '2024-01-15T10:30:00Z', data_points: 1250 },
            bing: { status: 'connected', connected: true, last_sync: '2024-01-15T09:45:00Z', data_points: 850 },
            yandex: { status: 'disconnected', connected: false }
          },
          ai_insights: [
            {
              insight: 'Consider adding more internal links to improve page authority',
              priority: 'medium',
              category: 'content',
              action_required: false
            },
            {
              insight: 'Mobile page speed could be optimized further',
              priority: 'high',
              category: 'performance',
              action_required: true,
              tool_path: '/seo-dashboard'
            }
          ],
          last_updated: new Date().toISOString(),
          website_url: websiteUrl || undefined // Convert null to undefined for TypeScript
        };
        
        setData(mockData);
        setLoading(false);
      } catch (err) {
        setError('Failed to load dashboard data');
        setLoading(false);
      }
    };

    fetchData();
  }, [setData, setLoading, setError]);

  useEffect(() => {
    // Run initial SEO analysis if no data exists
    if (!loading && !error && data) {
      checkAndRunInitialAnalysis();
    }
  }, [loading, error, data, checkAndRunInitialAnalysis]);

  if (loading) {
    return <Skeleton variant="rectangular" height={200} />;
  }

  if (error || !data) {
    return <Alert severity="error">Failed to load dashboard data</Alert>;
  }

  return (
    <DashboardContainer>
      <Container maxWidth="xl">
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            {/* Header */}
            <Box sx={{ mb: 4 }}>
              <Typography variant="h4" sx={{ color: 'white', fontWeight: 700 }}>
                🔍 SEO Dashboard
              </Typography>
              <Typography variant="subtitle1" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                AI-powered insights and actionable recommendations
              </Typography>
            </Box>

            {/* Executive Summary */}
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" sx={{ color: 'white', fontWeight: 600, mb: 2 }}>
                📊 Performance Overview
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <GlassCard sx={{ p: 2 }}>
                    <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                      Organic Traffic
                    </Typography>
                    <Typography variant="h5" sx={{ color: '#4CAF50' }}>
                      {data.metrics.traffic.value}
                    </Typography>
                  </GlassCard>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <GlassCard sx={{ p: 2 }}>
                    <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                      Average Ranking
                    </Typography>
                    <Typography variant="h5" sx={{ color: '#2196F3' }}>
                      {data.metrics.rankings.value}
                    </Typography>
                  </GlassCard>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <GlassCard sx={{ p: 2 }}>
                    <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                      Mobile Speed
                    </Typography>
                    <Typography variant="h5" sx={{ color: '#FF9800' }}>
                      {data.metrics.mobile.value}
                    </Typography>
                  </GlassCard>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <GlassCard sx={{ p: 2 }}>
                    <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                      Keywords Tracked
                    </Typography>
                    <Typography variant="h5" sx={{ color: '#9C27B0' }}>
                      {data.metrics.keywords.value}
                    </Typography>
                  </GlassCard>
                </Grid>
              </Grid>
            </Box>

            {/* SEO Analyzer Panel */}
            <SEOAnalyzerPanel
              analysisData={analysisData}
              onRunAnalysis={runSEOAnalysis}
              loading={analysisLoading}
              error={analysisError}
            />
          </motion.div>
        </AnimatePresence>
      </Container>
    </DashboardContainer>
  );
};

export default SEODashboard;