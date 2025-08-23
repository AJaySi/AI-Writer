import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider
} from '@mui/material';
import {
  Analytics as AnalyticsIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Search as SearchIcon,
  Article as ArticleIcon,
  Speed as SpeedIcon,
  Lightbulb as LightbulbIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  ExpandMore as ExpandMoreIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Visibility as VisibilityIcon,
  Launch as LaunchIcon
} from '@mui/icons-material';

interface AuditMetrics {
  impressions: number;
  clicks: number;
  ctr: number;
  position: number;
}

interface PagePerformance {
  url: string;
  metrics: AuditMetrics;
  category: string;
  recommendations: string[];
}

interface QueryPerformance {
  query: string;
  metrics: AuditMetrics;
  intent_type: string;
  opportunity_score: number;
}

interface ContentCluster {
  topic: string;
  pages: string[];
  total_metrics: AuditMetrics;
  avg_metrics: AuditMetrics;
  performance_score: number;
  recommendations: string[];
}

interface TrendData {
  query: string;
  interest_over_time: Array<{date: string; interest: number}>;
  average_interest: number;
  peak_interest: number;
  trend_direction: string;
  seasonal_pattern: string;
  related_queries: Array<{query: string; value: number}>;
  rising_queries: Array<{query: string; value: number}>;
  geographic_data: Array<{country: string; country_name: string; interest: number}>;
}

interface SeasonalInsight {
  query: string;
  peak_months: string[];
  low_months: string[];
  seasonality_score: number;
  pattern_type: string;
  recommendations: string[];
}

interface AIInsight {
  insight_type: string;
  title: string;
  description: string;
  priority: string;
  confidence_score: number;
  action_items: string[];
  expected_impact: string;
  timeframe: string;
}

interface ContentStrategy {
  strategy_type: string;
  primary_keywords: string[];
  content_themes: string[];
  seasonal_calendar: {[key: string]: string[]};
  competitive_gaps: string[];
  trending_opportunities: string[];
  recommendations: string[];
}

interface CombinedAnalysis {
  analysis_date: string;
  site_url: string;
  executive_summary: string;
  key_insights: AIInsight[];
  content_strategy: ContentStrategy;
  performance_forecast: any;
  action_plan: Array<{
    order: number;
    title: string;
    description: string;
    action_items: string[];
    priority: string;
    timeframe: string;
    expected_impact: string;
    confidence_score: number;
    category: string;
  }>;
  risk_assessment: any;
}

interface AuditReport {
  site_url: string;
  audit_date: string;
  date_range: {
    start: string;
    end: string;
  };
  summary: {
    total_pages: number;
    total_queries: number;
    total_impressions: number;
    total_clicks: number;
    average_ctr: number;
    average_position: number;
  };
  performance_analysis: {
    top_performers: PagePerformance[];
    underperformers: PagePerformance[];
    low_hanging_fruit: PagePerformance[];
    striking_distance: QueryPerformance[];
    content_decay: PagePerformance[];
  };
  advanced_insights: {
    query_opportunities: QueryPerformance[];
    content_clusters: ContentCluster[];
    technical_issues: any;
  };
  trends: {
    performance_trends: any;
    yoy_comparison?: any;
    mom_comparison?: any;
  };
  google_trends?: {
    trends_data: TrendData[];
    seasonal_insights: SeasonalInsight[];
    trend_comparisons: any[];
  };
  ai_insights?: CombinedAnalysis;
}

const WebsiteAuditDashboard: React.FC = () => {
  const [siteUrl, setSiteUrl] = useState('');
  const [dateRange, setDateRange] = useState('last_30_days');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<AuditReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [analysisType, setAnalysisType] = useState('comprehensive');
  const [selectedPage, setSelectedPage] = useState<string | null>(null);
  const [selectedQuery, setSelectedQuery] = useState<string | null>(null);
  const [pageAnalysis, setPageAnalysis] = useState<any>(null);
  const [queryAnalysis, setQueryAnalysis] = useState<any>(null);

  const dateRangeOptions = [
    { value: 'last_7_days', label: 'Last 7 Days' },
    { value: 'last_30_days', label: 'Last 30 Days' },
    { value: 'last_90_days', label: 'Last 90 Days' },
    { value: 'last_6_months', label: 'Last 6 Months' },
    { value: 'last_year', label: 'Last Year' }
  ];

  const handleStartAudit = async () => {
    if (!siteUrl) {
      setError('Please enter a website URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/gsc-audit/quick-audit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site_url: siteUrl,
          date_range: dateRange,
          analysis_type: analysisType
        })
      });

      const data = await response.json();

      if (data.success) {
        setReport(data.report);
        setActiveTab(0);
      } else {
        setError(data.message || 'Audit failed');
      }
    } catch (err) {
      setError('Failed to conduct audit. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePageAnalysis = async (pageUrl: string) => {
    setSelectedPage(pageUrl);
    
    if (!report) return;
    
    try {
      const response = await fetch('/api/gsc-audit/analyze-page', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site_url: report.site_url,
          page_url: pageUrl,
          start_date: report.date_range.start,
          end_date: report.date_range.end
        })
      });

      const data = await response.json();
      setPageAnalysis(data);
    } catch (err) {
      console.error('Failed to analyze page:', err);
    }
  };

  const handleQueryAnalysis = async (query: string) => {
    setSelectedQuery(query);
    
    if (!report) return;
    
    try {
      const response = await fetch('/api/gsc-audit/analyze-query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site_url: report.site_url,
          query: query,
          start_date: report.date_range.start,
          end_date: report.date_range.end
        })
      });

      const data = await response.json();
      setQueryAnalysis(data);
    } catch (err) {
      console.error('Failed to analyze query:', err);
    }
  };

  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const getPerformanceColor = (category: string): string => {
    switch (category) {
      case 'top_performer': return 'success';
      case 'low_hanging_fruit': return 'warning';
      case 'underperformer': return 'error';
      default: return 'info';
    }
  };

  const getIntentColor = (intent: string): string => {
    switch (intent) {
      case 'transactional': return 'success';
      case 'commercial': return 'warning';
      case 'informational': return 'info';
      case 'navigational': return 'primary';
      default: return 'default';
    }
  };

  const renderOverviewTab = () => (
    <Box>
      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <VisibilityIcon color="primary" />
                <Typography variant="h6">Impressions</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {formatNumber(report?.summary.total_impressions || 0)}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total search impressions
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <LaunchIcon color="success" />
                <Typography variant="h6">Clicks</Typography>
              </Box>
              <Typography variant="h4" color="success.main">
                {formatNumber(report?.summary.total_clicks || 0)}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Total clicks received
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <SpeedIcon color="warning" />
                <Typography variant="h6">Avg CTR</Typography>
              </Box>
              <Typography variant="h4" color="warning.main">
                {report?.summary.average_ctr.toFixed(1)}%
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Click-through rate
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={1}>
                <TrendingUpIcon color="info" />
                <Typography variant="h6">Avg Position</Typography>
              </Box>
              <Typography variant="h4" color="info.main">
                {report?.summary.average_position.toFixed(1)}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Average search position
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Performance Categories */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                Top Performers ({report?.performance_analysis.top_performers.length || 0})
              </Typography>
              <List dense>
                {report?.performance_analysis.top_performers.slice(0, 5).map((page, index) => (
                  <ListItem 
                    key={index}
                    button 
                    onClick={() => handlePageAnalysis(page.url)}
                  >
                    <ListItemText 
                      primary={page.url.length > 50 ? page.url.substring(0, 50) + '...' : page.url}
                      secondary={`${formatNumber(page.metrics.clicks)} clicks • ${page.metrics.ctr.toFixed(1)}% CTR`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <LightbulbIcon color="warning" sx={{ mr: 1 }} />
                Low Hanging Fruit ({report?.performance_analysis.low_hanging_fruit.length || 0})
              </Typography>
              <List dense>
                {report?.performance_analysis.low_hanging_fruit.slice(0, 5).map((page, index) => (
                  <ListItem 
                    key={index}
                    button 
                    onClick={() => handlePageAnalysis(page.url)}
                  >
                    <ListItemText 
                      primary={page.url.length > 50 ? page.url.substring(0, 50) + '...' : page.url}
                      secondary={`${formatNumber(page.metrics.impressions)} impressions • ${page.metrics.ctr.toFixed(1)}% CTR`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderPagesTab = () => (
    <Box>
      <Typography variant="h5" gutterBottom>Page Performance Analysis</Typography>
      
      <Tabs value={activeTab === 1 ? 0 : 0} sx={{ mb: 3 }}>
        <Tab label="Top Performers" />
        <Tab label="Low Hanging Fruit" />
        <Tab label="Underperformers" />
      </Tabs>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Page URL</TableCell>
              <TableCell align="right">Impressions</TableCell>
              <TableCell align="right">Clicks</TableCell>
              <TableCell align="right">CTR (%)</TableCell>
              <TableCell align="right">Avg Position</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {report?.performance_analysis.top_performers.map((page, index) => (
              <TableRow key={index} hover>
                <TableCell>
                  <Typography variant="body2" noWrap>
                    {page.url.length > 40 ? page.url.substring(0, 40) + '...' : page.url}
                  </Typography>
                </TableCell>
                <TableCell align="right">{formatNumber(page.metrics.impressions)}</TableCell>
                <TableCell align="right">{formatNumber(page.metrics.clicks)}</TableCell>
                <TableCell align="right">{page.metrics.ctr.toFixed(2)}</TableCell>
                <TableCell align="right">{page.metrics.position.toFixed(1)}</TableCell>
                <TableCell>
                  <Chip 
                    label={page.category.replace('_', ' ')} 
                    color={getPerformanceColor(page.category) as any}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Button 
                    size="small" 
                    onClick={() => handlePageAnalysis(page.url)}
                    startIcon={<AnalyticsIcon />}
                  >
                    Analyze
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );

  const renderQueriesTab = () => (
    <Box>
      <Typography variant="h5" gutterBottom>Query Performance Analysis</Typography>
      
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Striking Distance Queries
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Queries ranking 11-20 with optimization potential
              </Typography>
              <List dense>
                {report?.performance_analysis.striking_distance.slice(0, 10).map((query, index) => (
                  <ListItem 
                    key={index}
                    button 
                    onClick={() => handleQueryAnalysis(query.query)}
                  >
                    <ListItemIcon>
                      <Chip 
                        label={query.intent_type} 
                        color={getIntentColor(query.intent_type) as any}
                        size="small"
                      />
                    </ListItemIcon>
                    <ListItemText 
                      primary={query.query}
                      secondary={`Position ${query.metrics.position.toFixed(1)} • ${formatNumber(query.metrics.impressions)} impressions`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Query Opportunities
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Highest opportunity score queries
              </Typography>
              <List dense>
                {report?.advanced_insights.query_opportunities.slice(0, 10).map((query, index) => (
                  <ListItem 
                    key={index}
                    button 
                    onClick={() => handleQueryAnalysis(query.query)}
                  >
                    <ListItemIcon>
                      <Chip 
                        label={`${query.opportunity_score.toFixed(1)}`} 
                        color="primary"
                        size="small"
                      />
                    </ListItemIcon>
                    <ListItemText 
                      primary={query.query}
                      secondary={`${query.intent_type} intent • ${formatNumber(query.metrics.impressions)} impressions`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderClustersTab = () => (
    <Box>
      <Typography variant="h5" gutterBottom>Content Clusters Analysis</Typography>
      
      <Grid container spacing={3}>
        {report?.advanced_insights.content_clusters.map((cluster, index) => (
          <Grid item xs={12} md={6} lg={4} key={index}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {cluster.topic}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  {cluster.pages.length} pages • Score: {cluster.performance_score.toFixed(1)}/10
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={cluster.performance_score * 10} 
                    color={cluster.performance_score >= 7 ? 'success' : cluster.performance_score >= 4 ? 'warning' : 'error'}
                  />
                </Box>
                
                <Grid container spacing={2} sx={{ mb: 2 }}>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      <strong>{formatNumber(cluster.total_metrics.clicks)}</strong><br />
                      Total Clicks
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      <strong>{cluster.total_metrics.ctr.toFixed(1)}%</strong><br />
                      Avg CTR
                    </Typography>
                  </Grid>
                </Grid>
                
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="body2">Recommendations</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <List dense>
                      {cluster.recommendations.map((rec, recIndex) => (
                        <ListItem key={recIndex} disablePadding>
                          <ListItemText primary={rec} />
                        </ListItem>
                      ))}
                    </List>
                  </AccordionDetails>
                </Accordion>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderTrendsTab = () => (
    <Box>
      <Typography variant="h5" gutterBottom>Performance Trends & Comparisons</Typography>
      
      {report?.trends.yoy_comparison && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Year-over-Year Comparison
            </Typography>
            <Grid container spacing={3}>
              {Object.entries(report.trends.yoy_comparison.changes).map(([metric, change]: [string, any]) => (
                <Grid item xs={12} md={3} key={metric}>
                  <Box textAlign="center">
                    <Typography variant="h6" color={change.direction === 'increase' ? 'success.main' : 'error.main'}>
                      {change.direction === 'increase' ? '+' : ''}{change.percent_change.toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {metric.charAt(0).toUpperCase() + metric.slice(1)}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}
      
      {report?.trends.mom_comparison && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Month-over-Month Comparison
            </Typography>
            <Grid container spacing={3}>
              {Object.entries(report.trends.mom_comparison.changes).map(([metric, change]: [string, any]) => (
                <Grid item xs={12} md={3} key={metric}>
                  <Box textAlign="center">
                    <Typography variant="h6" color={change.direction === 'increase' ? 'success.main' : 'error.main'}>
                      {change.direction === 'increase' ? '+' : ''}{change.percent_change.toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {metric.charAt(0).toUpperCase() + metric.slice(1)}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </CardContent>
        </Card>
      )}
    </Box>
  );

  const renderGoogleTrendsTab = () => (
    <Box>
      <Typography variant="h5" gutterBottom>Google Trends Analysis</Typography>
      
      {report?.google_trends && (
        <Grid container spacing={3}>
          {/* Trends Data */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Search Interest Trends
                </Typography>
                <Grid container spacing={2}>
                  {report.google_trends.trends_data.map((trend, index) => (
                    <Grid item xs={12} md={6} lg={4} key={index}>
                      <Paper sx={{ p: 2, height: '100%' }}>
                        <Typography variant="subtitle1" gutterBottom>
                          "{trend.query}"
                        </Typography>
                        
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">
                            Avg Interest: <strong>{trend.average_interest}</strong>
                          </Typography>
                          <Chip 
                            label={trend.trend_direction} 
                            color={
                              trend.trend_direction === 'rising' ? 'success' : 
                              trend.trend_direction === 'declining' ? 'error' : 'default'
                            }
                            size="small"
                          />
                        </Box>
                        
                        <Typography variant="body2" color="textSecondary" gutterBottom>
                          Peak: {trend.peak_interest} | Pattern: {trend.seasonal_pattern}
                        </Typography>
                        
                        {trend.rising_queries.length > 0 && (
                          <Box sx={{ mt: 2 }}>
                            <Typography variant="body2" fontWeight="bold">Rising Queries:</Typography>
                            {trend.rising_queries.slice(0, 3).map((rising, idx) => (
                              <Chip 
                                key={idx}
                                label={rising.query}
                                size="small"
                                variant="outlined"
                                sx={{ mr: 0.5, mb: 0.5 }}
                              />
                            ))}
                          </Box>
                        )}
                        
                        {trend.geographic_data.length > 0 && (
                          <Box sx={{ mt: 2 }}>
                            <Typography variant="body2" fontWeight="bold">Top Regions:</Typography>
                            {trend.geographic_data.slice(0, 3).map((geo, idx) => (
                              <Typography key={idx} variant="body2">
                                {geo.country_name}: {geo.interest}
                              </Typography>
                            ))}
                          </Box>
                        )}
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Seasonal Insights */}
          {report.google_trends.seasonal_insights.length > 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Seasonal Patterns
                  </Typography>
                  <Grid container spacing={2}>
                    {report.google_trends.seasonal_insights.map((insight, index) => (
                      <Grid item xs={12} md={6} key={index}>
                        <Paper sx={{ p: 2 }}>
                          <Typography variant="subtitle1" gutterBottom>
                            "{insight.query}"
                          </Typography>
                          
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <Typography variant="body2" sx={{ mr: 1 }}>
                              Seasonality Score: 
                            </Typography>
                            <LinearProgress 
                              variant="determinate" 
                              value={Math.min(insight.seasonality_score * 50, 100)}
                              sx={{ flexGrow: 1, mr: 1 }}
                            />
                            <Typography variant="body2">
                              {insight.seasonality_score.toFixed(2)}
                            </Typography>
                          </Box>
                          
                          <Typography variant="body2" gutterBottom>
                            Pattern: <Chip label={insight.pattern_type} size="small" />
                          </Typography>
                          
                          <Typography variant="body2" gutterBottom>
                            <strong>Peak Months:</strong> {insight.peak_months.join(', ')}
                          </Typography>
                          
                          <Typography variant="body2" gutterBottom>
                            <strong>Low Months:</strong> {insight.low_months.join(', ')}
                          </Typography>
                          
                          <Accordion>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                              <Typography variant="body2">Recommendations</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                              <List dense>
                                {insight.recommendations.map((rec, recIdx) => (
                                  <ListItem key={recIdx} disablePadding>
                                    <ListItemText primary={rec} />
                                  </ListItem>
                                ))}
                              </List>
                            </AccordionDetails>
                          </Accordion>
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}
    </Box>
  );

  const renderAIInsightsTab = () => (
    <Box>
      <Typography variant="h5" gutterBottom>AI-Powered Insights</Typography>
      
      {report?.ai_insights && (
        <Grid container spacing={3}>
          {/* Executive Summary */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Executive Summary
                </Typography>
                <Typography variant="body1">
                  {report.ai_insights.executive_summary}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Key Insights */}
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Key Insights & Recommendations
                </Typography>
                {report.ai_insights.key_insights.map((insight, index) => (
                  <Accordion key={index} sx={{ mb: 1 }}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <Typography variant="subtitle1" sx={{ flexGrow: 1 }}>
                          {insight.title}
                        </Typography>
                        <Chip 
                          label={insight.priority} 
                          color={
                            insight.priority === 'high' ? 'error' : 
                            insight.priority === 'medium' ? 'warning' : 'success'
                          }
                          size="small"
                          sx={{ mr: 1 }}
                        />
                        <Chip 
                          label={`${(insight.confidence_score * 100).toFixed(0)}%`}
                          color="info"
                          size="small"
                        />
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2" paragraph>
                        {insight.description}
                      </Typography>
                      
                      <Typography variant="body2" fontWeight="bold" gutterBottom>
                        Action Items:
                      </Typography>
                      <List dense>
                        {insight.action_items.map((action, actionIdx) => (
                          <ListItem key={actionIdx} disablePadding>
                            <ListItemIcon>
                              <CheckCircleIcon color="primary" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={action} />
                          </ListItem>
                        ))}
                      </List>
                      
                      <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                        <Typography variant="body2">
                          <strong>Expected Impact:</strong> {insight.expected_impact}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Timeframe:</strong> {insight.timeframe}
                        </Typography>
                      </Box>
                    </AccordionDetails>
                  </Accordion>
                ))}
              </CardContent>
            </Card>
          </Grid>
          
          {/* Content Strategy */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Content Strategy
                </Typography>
                
                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Primary Keywords:
                </Typography>
                <Box sx={{ mb: 2 }}>
                  {report.ai_insights.content_strategy.primary_keywords.map((keyword, idx) => (
                    <Chip 
                      key={idx}
                      label={keyword}
                      size="small"
                      sx={{ mr: 0.5, mb: 0.5 }}
                    />
                  ))}
                </Box>
                
                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Content Themes:
                </Typography>
                <List dense>
                  {report.ai_insights.content_strategy.content_themes.map((theme, idx) => (
                    <ListItem key={idx} disablePadding>
                      <ListItemText primary={theme} />
                    </ListItem>
                  ))}
                </List>
                
                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Trending Opportunities:
                </Typography>
                <List dense>
                  {report.ai_insights.content_strategy.trending_opportunities.map((opp, idx) => (
                    <ListItem key={idx} disablePadding>
                      <ListItemIcon>
                        <TrendingUpIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={opp} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Action Plan */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Prioritized Action Plan
                </Typography>
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>#</TableCell>
                        <TableCell>Action</TableCell>
                        <TableCell>Priority</TableCell>
                        <TableCell>Timeframe</TableCell>
                        <TableCell>Expected Impact</TableCell>
                        <TableCell>Confidence</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {report.ai_insights.action_plan.slice(0, 10).map((action, index) => (
                        <TableRow key={index} hover>
                          <TableCell>{action.order}</TableCell>
                          <TableCell>
                            <Typography variant="body2" fontWeight="bold">
                              {action.title}
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                              {action.description.length > 100 
                                ? action.description.substring(0, 100) + '...'
                                : action.description
                              }
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={action.priority} 
                              color={
                                action.priority === 'high' ? 'error' : 
                                action.priority === 'medium' ? 'warning' : 'success'
                              }
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{action.timeframe}</TableCell>
                          <TableCell>{action.expected_impact}</TableCell>
                          <TableCell>
                            <LinearProgress 
                              variant="determinate" 
                              value={action.confidence_score * 100}
                              sx={{ width: 60 }}
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
          
          {/* Performance Forecast */}
          {report.ai_insights.performance_forecast && (
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Performance Forecast
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>CTR Improvement:</strong><br />
                        +{report.ai_insights.performance_forecast.expected_ctr_improvement?.toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Position Improvement:</strong><br />
                        +{report.ai_insights.performance_forecast.expected_position_improvement?.toFixed(1)} positions
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Traffic Growth:</strong><br />
                        +{report.ai_insights.performance_forecast.traffic_growth_potential?.toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Confidence:</strong><br />
                        {report.ai_insights.performance_forecast.confidence_level}
                      </Typography>
                    </Grid>
                  </Grid>
                  
                  <Typography variant="body2" sx={{ mt: 2 }}>
                    <strong>Seasonal Impact:</strong><br />
                    {report.ai_insights.performance_forecast.seasonal_impact}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}
    </Box>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        <AnalyticsIcon sx={{ mr: 2, verticalAlign: 'middle' }} />
        GSC Website Audit Dashboard
      </Typography>
      
      {/* Audit Configuration */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Website URL"
                value={siteUrl}
                onChange={(e) => setSiteUrl(e.target.value)}
                placeholder="https://example.com"
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Date Range</InputLabel>
                <Select
                  value={dateRange}
                  onChange={(e) => setDateRange(e.target.value)}
                  label="Date Range"
                >
                  {dateRangeOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Analysis Type</InputLabel>
                <Select
                  value={analysisType}
                  onChange={(e) => setAnalysisType(e.target.value)}
                  label="Analysis Type"
                >
                  <MenuItem value="basic">Basic</MenuItem>
                  <MenuItem value="trends">With Trends</MenuItem>
                  <MenuItem value="comprehensive">Full + AI</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <Button
                fullWidth
                variant="contained"
                onClick={handleStartAudit}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
              >
                {loading ? 'Analyzing...' : 'Start Audit'}
              </Button>
            </Grid>
            <Grid item xs={12} md={2}>
              {report && (
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={handleStartAudit}
                  disabled={loading}
                >
                  Refresh
                </Button>
              )}
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {report && (
        <Box>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
            <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
              <Tab label="Overview" icon={<AnalyticsIcon />} />
              <Tab label="Pages" icon={<ArticleIcon />} />
              <Tab label="Queries" icon={<SearchIcon />} />
              <Tab label="Content Clusters" icon={<SpeedIcon />} />
              <Tab label="Trends" icon={<TrendingUpIcon />} />
              {report?.google_trends && <Tab label="Google Trends" icon={<TrendingUpIcon />} />}
              {report?.ai_insights && <Tab label="AI Insights" icon={<LightbulbIcon />} />}
            </Tabs>
          </Box>

          {activeTab === 0 && renderOverviewTab()}
          {activeTab === 1 && renderPagesTab()}
          {activeTab === 2 && renderQueriesTab()}
          {activeTab === 3 && renderClustersTab()}
          {activeTab === 4 && renderTrendsTab()}
          {activeTab === 5 && report?.google_trends && renderGoogleTrendsTab()}
          {activeTab === 6 && report?.ai_insights && renderAIInsightsTab()}
          {activeTab === 5 && !report?.google_trends && report?.ai_insights && renderAIInsightsTab()}
        </Box>
      )}

      {/* Page Analysis Dialog */}
      <Dialog 
        open={!!selectedPage} 
        onClose={() => setSelectedPage(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Page Analysis: {selectedPage}
        </DialogTitle>
        <DialogContent>
          {pageAnalysis && (
            <Box>
              <Typography variant="h6" gutterBottom>Performance Metrics</Typography>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={3}>
                  <Typography variant="body2">
                    <strong>{formatNumber(pageAnalysis.overall_metrics.total_impressions)}</strong><br />
                    Impressions
                  </Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="body2">
                    <strong>{formatNumber(pageAnalysis.overall_metrics.total_clicks)}</strong><br />
                    Clicks
                  </Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="body2">
                    <strong>{pageAnalysis.overall_metrics.average_ctr.toFixed(2)}%</strong><br />
                    CTR
                  </Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="body2">
                    <strong>{pageAnalysis.overall_metrics.average_position.toFixed(1)}</strong><br />
                    Position
                  </Typography>
                </Grid>
              </Grid>
              
              <Typography variant="h6" gutterBottom>Recommendations</Typography>
              <List>
                {pageAnalysis.recommendations.map((rec: string, index: number) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <LightbulbIcon color="warning" />
                    </ListItemIcon>
                    <ListItemText primary={rec} />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelectedPage(null)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Query Analysis Dialog */}
      <Dialog 
        open={!!selectedQuery} 
        onClose={() => setSelectedQuery(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Query Analysis: "{selectedQuery}"
        </DialogTitle>
        <DialogContent>
          {queryAnalysis && (
            <Box>
              <Typography variant="h6" gutterBottom>Query Performance</Typography>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={4}>
                  <Typography variant="body2">
                    <strong>{queryAnalysis.query_analysis.intent_type}</strong><br />
                    Intent Type
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="body2">
                    <strong>{queryAnalysis.query_analysis.opportunity_score.toFixed(1)}/10</strong><br />
                    Opportunity Score
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="body2">
                    <strong>{queryAnalysis.query_analysis.competing_pages}</strong><br />
                    Competing Pages
                  </Typography>
                </Grid>
              </Grid>
              
              <Typography variant="h6" gutterBottom>Recommendations</Typography>
              <List>
                {queryAnalysis.recommendations.map((rec: string, index: number) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <LightbulbIcon color="warning" />
                    </ListItemIcon>
                    <ListItemText primary={rec} />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelectedQuery(null)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default WebsiteAuditDashboard;