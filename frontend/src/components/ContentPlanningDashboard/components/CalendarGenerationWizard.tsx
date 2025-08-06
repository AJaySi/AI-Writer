import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Button,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Checkbox,
  FormControlLabel,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  LinearProgress,
  Tooltip,
  Badge,
  Alert,
  CircularProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Business as BusinessIcon,
  Analytics as AnalyticsIcon,
  TrendingUp as TrendingIcon,
  Psychology as PsychologyIcon,
  Group as GroupIcon,
  Timeline as TimelineIcon,
  Lightbulb as LightbulbIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon,
  ExpandMore as ExpandMoreIcon,
  DataUsage as DataUsageIcon,
  Insights as InsightsIcon,
  Assessment as AssessmentIcon,
  Campaign as CampaignIcon,
  Speed as SpeedIcon,
  CalendarToday as CalendarIcon,
  Schedule as ScheduleIcon,
  ContentCopy as ContentIcon,
  Public as PlatformIcon,
  TrendingUp as TrendingIcon2,
  AutoAwesome as AIIcon
} from '@mui/icons-material';

interface CalendarGenerationWizardProps {
  userData: any;
  onGenerateCalendar: (calendarConfig: any) => void;
  loading?: boolean;
}

interface CalendarConfig {
  calendarType: string;
  industry: string;
  businessSize: string;
  contentPillars: string[];
  platforms: string[];
  contentMix: {
    educational: number;
    thoughtLeadership: number;
    engagement: number;
    promotional: number;
  };
  targetKeywords: string[];
  optimalTiming: {
    bestDays: string[];
    bestTimes: string[];
  };
  performancePredictions: {
    trafficGrowth: number;
    engagementRate: number;
    conversionRate: number;
  };
}

const CalendarGenerationWizard: React.FC<CalendarGenerationWizardProps> = ({
  userData,
  onGenerateCalendar,
  loading = false
}) => {
  const [activeStep, setActiveStep] = useState(0);
  const [calendarConfig, setCalendarConfig] = useState<CalendarConfig>({
    calendarType: 'monthly',
    industry: userData.onboardingData?.industry || 'technology',
    businessSize: 'sme',
    contentPillars: userData.strategyData?.contentPillars || [],
    platforms: ['website', 'linkedin'],
    contentMix: {
      educational: 40,
      thoughtLeadership: 30,
      engagement: 20,
      promotional: 10
    },
    targetKeywords: userData.gapAnalysis?.keywordOpportunities?.slice(0, 10).map((k: any) => k.keyword) || [],
    optimalTiming: {
      bestDays: ['Monday', 'Wednesday', 'Friday'],
      bestTimes: ['9:00 AM', '2:00 PM', '7:00 PM']
    },
    performancePredictions: {
      trafficGrowth: 25,
      engagementRate: 15,
      conversionRate: 10
    }
  });

  const steps = [
    {
      label: 'Data Review & Transparency',
      icon: <DataUsageIcon />,
      description: 'Review and modify all analysis data that will be used for calendar generation'
    },
    {
      label: 'Calendar Configuration',
      icon: <CalendarIcon />,
      description: 'Configure your content calendar settings and preferences'
    },
    {
      label: 'Advanced Options',
      icon: <AIIcon />,
      description: 'Set advanced options for timing, performance, and optimization'
    },
    {
      label: 'Generate Calendar',
      icon: <CampaignIcon />,
      description: 'Generate your enterprise-level content calendar'
    }
  ];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleConfigUpdate = (updates: Partial<CalendarConfig>) => {
    setCalendarConfig(prev => ({ ...prev, ...updates }));
  };

  const renderDataReviewStep = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Review Your Analysis Data
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        The following data points have been analyzed and will be used to generate your content calendar.
        You can modify any of these settings before proceeding.
      </Typography>

      {/* Data Usage Summary */}
      <Paper sx={{ p: 3, mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <DataUsageIcon />
          <Typography variant="h6">Data Usage Summary</Typography>
        </Box>
        
        <Grid container spacing={2}>
          <Grid item xs={12} md={3}>
            <Typography variant="subtitle2">Analysis Sources</Typography>
            <Typography variant="body2">Website, Competitors, Keywords, Performance</Typography>
            <Tooltip title="Comprehensive analysis of your website content, competitor strategies, keyword opportunities, and performance metrics">
              <Typography variant="caption" sx={{ textDecoration: 'underline', cursor: 'pointer' }}>
                View Details
              </Typography>
            </Tooltip>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="subtitle2">Data Points Used</Typography>
            <Typography variant="body2">150+ data points analyzed</Typography>
            <Tooltip title="Includes content structure, keyword analysis, competitor insights, performance metrics, and audience behavior patterns">
              <Typography variant="caption" sx={{ textDecoration: 'underline', cursor: 'pointer' }}>
                View Details
              </Typography>
            </Tooltip>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="subtitle2">AI Insights Generated</Typography>
            <Typography variant="body2">25+ strategic recommendations</Typography>
            <Tooltip title="AI-generated content recommendations, gap analysis, performance predictions, and strategic insights">
              <Typography variant="caption" sx={{ textDecoration: 'underline', cursor: 'pointer' }}>
                View Details
              </Typography>
            </Tooltip>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="subtitle2">Confidence Score</Typography>
            <Typography variant="body2">95% accuracy</Typography>
            <Tooltip title="AI confidence score based on data quality, analysis depth, and prediction accuracy">
              <Typography variant="caption" sx={{ textDecoration: 'underline', cursor: 'pointer' }}>
                View Details
              </Typography>
            </Tooltip>
          </Grid>
        </Grid>

        {/* Additional Analysis Details */}
        <Box sx={{ mt: 2, pt: 2, borderTop: 1, borderColor: 'rgba(255,255,255,0.2)' }}>
          <Typography variant="subtitle2" gutterBottom>
            Analysis Breakdown
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Typography variant="caption" display="block">Content Analysis</Typography>
              <Typography variant="body2">
                {userData?.onboarding_data?.website_analysis?.content_types?.length || 0} content types analyzed
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="caption" display="block">Competitor Analysis</Typography>
              <Typography variant="body2">
                {userData?.onboarding_data?.competitor_analysis?.top_performers?.length || 0} competitors analyzed
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="caption" display="block">Keyword Research</Typography>
              <Typography variant="body2">
                {userData?.onboarding_data?.keyword_analysis?.high_value_keywords?.length || 0} high-value keywords identified
              </Typography>
            </Grid>
          </Grid>
        </Box>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Business Context"
              avatar={<BusinessIcon color="primary" />}
              action={
                <Chip label="Pre-populated" size="small" color="primary" variant="outlined" />
              }
            />
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                Industry: {userData?.industry || 'technology'}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                Business Size: {calendarConfig.businessSize}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Based on your website analysis and onboarding data
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Content Gaps"
              avatar={<AssessmentIcon color="primary" />}
              action={
                <Tooltip title={`${userData?.gap_analysis?.content_gaps?.length || 0} content gaps identified through AI analysis`}>
                  <Chip label={`${userData?.gap_analysis?.content_gaps?.length || 0} gaps`} size="small" color="warning" />
                </Tooltip>
              }
            />
            <CardContent>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {userData?.gap_analysis?.content_gaps?.length || 0} content gaps identified through competitor analysis
              </Typography>
              
              {/* Show first 2 gaps with details */}
              {userData?.gap_analysis?.content_gaps?.slice(0, 2).map((gap: any, index: number) => (
                <Box key={index} sx={{ mb: 1, p: 1, bgcolor: 'grey.50', borderRadius: 1 }}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    {gap.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {gap.description}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip label={`Priority: ${gap.priority}`} size="small" color="warning" />
                    <Chip label={`Impact: ${gap.estimated_impact}`} size="small" color="success" />
                    <Chip label={`Time: ${gap.implementation_time}`} size="small" color="info" />
                  </Box>
                </Box>
              ))}
              
              {userData?.gap_analysis?.content_gaps?.length > 2 && (
                <Button size="small" color="primary">
                  View all {userData?.gap_analysis?.content_gaps?.length} gaps
                </Button>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Keyword Opportunities"
              avatar={<TrendingIcon color="primary" />}
              action={
                <Tooltip title={`${userData?.gap_analysis?.keyword_opportunities?.length || 0} high-value keywords identified for content targeting`}>
                  <Chip label={`${userData?.gap_analysis?.keyword_opportunities?.length || 0} keywords`} size="small" color="success" />
                </Tooltip>
              }
            />
            <CardContent>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {userData?.gap_analysis?.keyword_opportunities?.length || 0} keyword opportunities identified
              </Typography>
              
              {/* Show keyword opportunities */}
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {userData?.gap_analysis?.keyword_opportunities?.slice(0, 6).map((keyword: string, index: number) => (
                  <Tooltip key={index} title={`Target this keyword in your content strategy`}>
                    <Chip 
                      label={keyword} 
                      size="small" 
                      color="success"
                      variant="outlined"
                    />
                  </Tooltip>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="AI Recommendations"
              avatar={<LightbulbIcon color="primary" />}
              action={
                <Tooltip title={`${userData?.gap_analysis?.recommendations?.length || 0} AI-generated strategic recommendations with detailed implementation plans`}>
                  <Chip label={`${userData?.gap_analysis?.recommendations?.length || 0} recs`} size="small" color="info" />
                </Tooltip>
              }
            />
            <CardContent>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {userData?.gap_analysis?.recommendations?.length || 0} AI-generated strategic recommendations
              </Typography>
              
              {/* Show first 2 recommendations with details */}
              {userData?.gap_analysis?.recommendations?.slice(0, 2).map((rec: any, index: number) => (
                <Box key={index} sx={{ mb: 1, p: 1, bgcolor: 'grey.50', borderRadius: 1 }}>
                  <Typography variant="subtitle2" color="primary" gutterBottom>
                    {rec.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {rec.description}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip label={`Priority: ${rec.priority}`} size="small" color="warning" />
                    <Chip label={`Impact: ${rec.estimated_impact}`} size="small" color="success" />
                    <Chip label={`Time: ${rec.implementation_time}`} size="small" color="info" />
                  </Box>
                </Box>
              ))}
              
              {userData?.gap_analysis?.recommendations?.length > 2 && (
                <Button size="small" color="primary">
                  View all {userData?.gap_analysis?.recommendations?.length} recommendations
                </Button>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Detailed Data Sections */}
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Detailed Analysis Data
          </Typography>
        </Grid>

        {/* Business Context Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Business Context Details"
              avatar={<BusinessIcon color="primary" />}
            />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Industry Analysis
                  </Typography>
                  <Chip 
                    label={userData.onboardingData?.industry || 'Technology'} 
                    color="primary" 
                    sx={{ mb: 1 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    Based on your website analysis and onboarding data
                  </Typography>
                </Grid>
                
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Business Goals
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {userData?.business_goals?.map((goal: string, index: number) => (
                      <Chip key={index} label={goal} size="small" variant="outlined" />
                    )) || []}
                  </Box>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Target Audience
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="body2">
                      {userData?.target_audience?.join(', ') || 
                       'Demographics and behavior patterns analyzed from your website and competitor data'}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Gap Analysis Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Content Gap Analysis Details"
              avatar={<AssessmentIcon color="primary" />}
              action={
                <Tooltip title="AI-identified content gaps with detailed analysis and implementation strategies">
                  <InfoIcon color="primary" />
                </Tooltip>
              }
            />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Content Gaps Identified
                  </Typography>
                  <List dense>
                    {userData?.gap_analysis?.content_gaps?.slice(0, 3).map((gap: any, index: number) => (
                      <ListItem key={index} sx={{ px: 0 }}>
                        <ListItemIcon>
                          <WarningIcon color="warning" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText 
                          primary={
                            <Tooltip title={gap.description}>
                              <Typography variant="body2" color="primary">
                                {gap.title}
                              </Typography>
                            </Tooltip>
                          }
                          secondary={
                            <Box>
                              <Typography variant="caption" color="text.secondary">
                                Impact: {gap.estimated_impact} • Time: {gap.implementation_time}
                              </Typography>
                              <Box sx={{ mt: 0.5 }}>
                                <Typography variant="caption" color="text.secondary">
                                  AI Confidence: {Math.round((gap.ai_confidence || 0) * 100)}%
                                </Typography>
                              </Box>
                            </Box>
                          }
                        />
                      </ListItem>
                    )) || []}
                  </List>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Keyword Opportunities
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {userData?.gap_analysis?.keyword_opportunities?.slice(0, 6).map((keyword: string, index: number) => (
                      <Tooltip key={index} title={`High-value keyword for content targeting. Search volume and competition analyzed.`}>
                        <Chip 
                          label={keyword} 
                          size="small" 
                          color="success"
                          variant="outlined"
                        />
                      </Tooltip>
                    )) || []}
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Competitor Intelligence Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Competitor Intelligence Details"
              avatar={<InsightsIcon color="primary" />}
              action={
                <Tooltip title="Competitor analysis insights and market positioning data">
                  <InfoIcon color="primary" />
                </Tooltip>
              }
            />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Competitor Analysis
                  </Typography>
                  <List dense>
                    {userData?.gap_analysis?.competitor_insights?.slice(0, 2).map((insight: string, index: number) => (
                      <ListItem key={index} sx={{ px: 0 }}>
                        <ListItemIcon>
                          <TrendingIcon color="info" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText 
                          primary={
                            <Tooltip title="Competitor website analyzed for content strategy insights">
                              <Typography variant="body2" color="primary">
                                {insight}
                              </Typography>
                            </Tooltip>
                          }
                          secondary="Competitor insight"
                        />
                      </ListItem>
                    )) || []}
                  </List>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Market Position
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="body2">
                      {userData?.ai_analysis_results?.market_positioning?.industry_position || 
                       'Market position analysis based on competitor data'}
                    </Typography>
                    {userData?.ai_analysis_results?.market_positioning?.competitive_advantage && (
                      <Typography variant="caption" color="success.main" sx={{ mt: 1, display: 'block' }}>
                        Competitive Advantage: {userData.ai_analysis_results.market_positioning.competitive_advantage}
                      </Typography>
                    )}
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Strategic Recommendations Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="AI Strategic Recommendations Details"
              avatar={<LightbulbIcon color="primary" />}
              action={
                <Tooltip title="AI-generated strategic recommendations with detailed implementation plans">
                  <InfoIcon color="primary" />
                </Tooltip>
              }
            />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Content Pillars
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {userData?.strategy_data?.content_pillars?.slice(0, 5).map((pillar: string, index: number) => (
                      <Tooltip key={index} title={`Core content theme for your content strategy`}>
                        <Chip 
                          label={pillar} 
                          size="small" 
                          color="primary"
                          variant="outlined"
                        />
                      </Tooltip>
                    )) || []}
                  </Box>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Priority Recommendations
                  </Typography>
                  <List dense>
                    {userData?.gap_analysis?.recommendations?.slice(0, 3).map((rec: any, index: number) => (
                      <ListItem key={index} sx={{ px: 0 }}>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText 
                          primary={
                            <Tooltip title={rec.description}>
                              <Typography variant="body2" color="primary">
                                {rec.title}
                              </Typography>
                            </Tooltip>
                          }
                          secondary={
                            <Box>
                              <Typography variant="caption" color="text.secondary">
                                Priority: {rec.priority} • Impact: {rec.estimated_impact}
                              </Typography>
                              <Box sx={{ mt: 0.5 }}>
                                <Typography variant="caption" color="text.secondary">
                                  Time: {rec.implementation_time} • Confidence: {Math.round((rec.ai_confidence || 0) * 100)}%
                                </Typography>
                              </Box>
                            </Box>
                          }
                        />
                      </ListItem>
                    )) || []}
                  </List>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Performance Analytics Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Performance Analytics Details"
              avatar={<SpeedIcon color="primary" />}
            />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Historical Performance
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="body2">
                      {userData.performanceData?.summary || 
                       'Performance metrics analyzed from your existing content and competitor benchmarks'}
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Predicted Performance
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Traffic Growth</Typography>
                      <Typography variant="body2" color="success.main">+25%</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Engagement Rate</Typography>
                      <Typography variant="body2" color="success.main">+15%</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Conversion Rate</Typography>
                      <Typography variant="body2" color="success.main">+10%</Typography>
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* AI Analysis Results Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="AI Analysis Results Details"
              avatar={<AIIcon color="primary" />}
              action={
                <Tooltip title="Comprehensive AI analysis results with strategic insights and market intelligence">
                  <InfoIcon color="primary" />
                </Tooltip>
              }
            />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Strategic Intelligence
                  </Typography>
                  <List dense>
                    {userData.aiAnalysisResults?.map((result: any, index: number) => (
                      <ListItem key={index} sx={{ px: 0 }}>
                        <ListItemIcon>
                          {result.type === 'opportunity' && <LightbulbIcon color="success" fontSize="small" />}
                          {result.type === 'trend' && <TrendingIcon color="info" fontSize="small" />}
                          {result.type === 'performance' && <SpeedIcon color="primary" fontSize="small" />}
                        </ListItemIcon>
                        <ListItemText 
                          primary={
                            <Tooltip title={result.description}>
                              <Typography variant="body2" color="primary">
                                {result.title}
                              </Typography>
                            </Tooltip>
                          }
                          secondary={result.description}
                        />
                      </ListItem>
                    )) || []}
                  </List>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Market Positioning
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="body2" gutterBottom>
                      Industry Position: {userData?.ai_analysis_results?.market_positioning?.industry_position || 'Analyzing...'}
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      Market Share: {userData?.ai_analysis_results?.market_positioning?.market_share || 'Medium'}
                    </Typography>
                    <Typography variant="body2">
                      Competitive Advantage: {userData?.ai_analysis_results?.market_positioning?.competitive_advantage || 'Content quality'}
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Strategic Scores
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    {userData?.ai_analysis_results?.strategic_scores && Object.entries(userData.ai_analysis_results.strategic_scores).map(([key, value]: [string, any]) => (
                      <Box key={key} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="body2" color="text.secondary">
                          {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </Typography>
                        <Chip 
                          label={`${Math.round((value || 0) * 100)}%`} 
                          size="small" 
                          color={value > 0.8 ? 'success' : value > 0.6 ? 'warning' : 'error'}
                        />
                      </Box>
                    ))}
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Content Recommendations Details */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Content Recommendations Details"
              avatar={<CampaignIcon color="primary" />}
              action={
                <Tooltip title="Detailed content recommendations with implementation strategies and performance predictions">
                  <InfoIcon color="primary" />
                </Tooltip>
              }
            />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Priority Content Recommendations
                  </Typography>
                  <List dense>
                    {userData.recommendationsData?.map((rec: any, index: number) => (
                      <ListItem key={index} sx={{ px: 0 }}>
                        <ListItemIcon>
                          <CampaignIcon color="primary" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText 
                          primary={
                            <Tooltip title={rec.description || 'Content recommendation based on AI analysis'}>
                              <Typography variant="body2" color="primary">
                                {rec.title}
                              </Typography>
                            </Tooltip>
                          }
                          secondary={`Type: ${rec.type} • Priority: ${rec.priority}`}
                        />
                      </ListItem>
                    )) || []}
                  </List>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Implementation Timeline
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    <Tooltip title="Weekly content updates based on trending topics">
                      <Chip label="Weekly Updates" size="small" color="primary" />
                    </Tooltip>
                    <Tooltip title="Monthly deep-dive content pieces">
                      <Chip label="Monthly Deep Dives" size="small" color="secondary" />
                    </Tooltip>
                    <Tooltip title="Quarterly comprehensive reports and analysis">
                      <Chip label="Quarterly Reports" size="small" color="success" />
                    </Tooltip>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Comprehensive AI Insights Summary */}
        <Grid item xs={12}>
          <Card>
            <CardHeader
              title="Comprehensive AI Insights Summary"
              avatar={<AIIcon color="primary" />}
              action={
                <Tooltip title="Complete AI analysis summary with all insights and recommendations">
                  <InfoIcon color="primary" />
                </Tooltip>
              }
            />
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Content Strategy Insights
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Content Gaps Identified</Typography>
                      <Chip label={userData?.gap_analysis?.content_gaps?.length || 0} size="small" color="warning" />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Keyword Opportunities</Typography>
                      <Chip label={userData?.gap_analysis?.keyword_opportunities?.length || 0} size="small" color="success" />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">AI Recommendations</Typography>
                      <Chip label={userData?.gap_analysis?.recommendations?.length || 0} size="small" color="info" />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Competitor Insights</Typography>
                      <Chip label={userData?.gap_analysis?.competitor_insights?.length || 0} size="small" color="primary" />
                    </Box>
                  </Box>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Performance Predictions
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Traffic Growth</Typography>
                      <Chip label="+25%" size="small" color="success" />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Engagement Rate</Typography>
                      <Chip label="+15%" size="small" color="success" />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">Conversion Rate</Typography>
                      <Chip label="+10%" size="small" color="success" />
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography variant="body2">AI Confidence</Typography>
                      <Chip label="95%" size="small" color="primary" />
                    </Box>
                  </Box>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Key Insights from AI Analysis
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="body2" gutterBottom>
                      <strong>Market Position:</strong> {userData?.ai_analysis_results?.market_positioning?.industry_position || 'Established'} in the industry
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      <strong>Competitive Advantage:</strong> {userData?.ai_analysis_results?.market_positioning?.competitive_advantage || 'Content quality'} 
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      <strong>Content Strategy:</strong> Focus on {userData?.gap_analysis?.content_gaps?.slice(0, 2).map((gap: any) => gap.title).join(', ') || 'educational and thought leadership content'}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Target Keywords:</strong> {userData?.gap_analysis?.keyword_opportunities?.slice(0, 3).join(', ') || 'AI marketing, content automation, digital strategy'}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderCalendarConfigurationStep = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Configure Your Content Calendar
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Customize your calendar settings based on the analyzed data and your preferences.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Calendar Type</InputLabel>
            <Select
              value={calendarConfig.calendarType}
              onChange={(e) => handleConfigUpdate({ calendarType: e.target.value })}
              label="Calendar Type"
            >
              <MenuItem value="weekly">Weekly Calendar</MenuItem>
              <MenuItem value="monthly">Monthly Calendar</MenuItem>
              <MenuItem value="quarterly">Quarterly Calendar</MenuItem>
            </Select>
          </FormControl>

          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Industry</InputLabel>
            <Select
              value={calendarConfig.industry}
              onChange={(e) => handleConfigUpdate({ industry: e.target.value })}
              label="Industry"
            >
              <MenuItem value="technology">Technology</MenuItem>
              <MenuItem value="healthcare">Healthcare</MenuItem>
              <MenuItem value="finance">Finance</MenuItem>
              <MenuItem value="education">Education</MenuItem>
              <MenuItem value="retail">Retail</MenuItem>
              <MenuItem value="manufacturing">Manufacturing</MenuItem>
            </Select>
          </FormControl>

          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Business Size</InputLabel>
            <Select
              value={calendarConfig.businessSize}
              onChange={(e) => handleConfigUpdate({ businessSize: e.target.value })}
              label="Business Size"
            >
              <MenuItem value="startup">Startup</MenuItem>
              <MenuItem value="sme">SME</MenuItem>
              <MenuItem value="enterprise">Enterprise</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" gutterBottom>
            Content Pillars
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
            {calendarConfig.contentPillars.map((pillar, index) => (
              <Chip key={index} label={pillar} color="primary" />
            ))}
          </Box>

          <Typography variant="subtitle2" gutterBottom>
            Target Platforms
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {calendarConfig.platforms.map((platform, index) => (
              <Chip key={index} label={platform} color="secondary" />
            ))}
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            Content Mix Distribution
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Educational: {calendarConfig.contentMix.educational}%</Typography>
              <LinearProgress 
                variant="determinate" 
                value={calendarConfig.contentMix.educational} 
                color="primary"
                sx={{ mt: 1 }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Thought Leadership: {calendarConfig.contentMix.thoughtLeadership}%</Typography>
              <LinearProgress 
                variant="determinate" 
                value={calendarConfig.contentMix.thoughtLeadership} 
                color="secondary"
                sx={{ mt: 1 }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Engagement: {calendarConfig.contentMix.engagement}%</Typography>
              <LinearProgress 
                variant="determinate" 
                value={calendarConfig.contentMix.engagement} 
                color="success"
                sx={{ mt: 1 }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Promotional: {calendarConfig.contentMix.promotional}%</Typography>
              <LinearProgress 
                variant="determinate" 
                value={calendarConfig.contentMix.promotional} 
                color="warning"
                sx={{ mt: 1 }}
              />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );

  const renderAdvancedOptionsStep = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Advanced Calendar Options
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Configure advanced settings for timing optimization and performance predictions.
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Optimal Timing"
              avatar={<ScheduleIcon color="primary" />}
            />
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                Best Days
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                {calendarConfig.optimalTiming.bestDays.map((day, index) => (
                  <Chip key={index} label={day} size="small" variant="outlined" />
                ))}
              </Box>
              
              <Typography variant="subtitle2" gutterBottom>
                Best Times
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {calendarConfig.optimalTiming.bestTimes.map((time, index) => (
                  <Chip key={index} label={time} size="small" variant="outlined" />
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader
              title="Performance Predictions"
              avatar={<TrendingIcon2 color="primary" />}
            />
            <CardContent>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2">Traffic Growth</Typography>
                  <Typography variant="body2" color="success.main">
                    +{calendarConfig.performancePredictions.trafficGrowth}%
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2">Engagement Rate</Typography>
                  <Typography variant="body2" color="success.main">
                    +{calendarConfig.performancePredictions.engagementRate}%
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2">Conversion Rate</Typography>
                  <Typography variant="body2" color="success.main">
                    +{calendarConfig.performancePredictions.conversionRate}%
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardHeader
              title="Target Keywords"
              avatar={<TrendingIcon color="primary" />}
            />
            <CardContent>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {calendarConfig.targetKeywords.slice(0, 15).map((keyword, index) => (
                  <Chip key={index} label={keyword} size="small" color="success" variant="outlined" />
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );

  const renderGenerateCalendarStep = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Generate Your Enterprise Calendar
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Based on your configuration and analyzed data, we'll generate a comprehensive content calendar.
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          Your calendar will be generated using:
        </Typography>
        <List dense>
          <ListItem sx={{ px: 0 }}>
            <ListItemIcon>
              <CheckCircleIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Database-driven insights from your analysis" />
          </ListItem>
          <ListItem sx={{ px: 0 }}>
            <ListItemIcon>
              <CheckCircleIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Industry-specific content templates" />
          </ListItem>
          <ListItem sx={{ px: 0 }}>
            <ListItemIcon>
              <CheckCircleIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="AI-powered performance predictions" />
          </ListItem>
          <ListItem sx={{ px: 0 }}>
            <ListItemIcon>
              <CheckCircleIcon color="success" fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Competitive intelligence insights" />
          </ListItem>
        </List>
      </Alert>

      <Button
        variant="contained"
        size="large"
        startIcon={<CampaignIcon />}
        onClick={() => onGenerateCalendar(calendarConfig)}
        disabled={loading}
        sx={{ mt: 2 }}
      >
        {loading ? 'Generating Calendar...' : 'Generate Enterprise Calendar'}
      </Button>
    </Box>
  );

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return renderDataReviewStep();
      case 1:
        return renderCalendarConfigurationStep();
      case 2:
        return renderAdvancedOptionsStep();
      case 3:
        return renderGenerateCalendarStep();
      default:
        return null;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Enterprise Calendar Generation Wizard
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Create a comprehensive content calendar using AI-powered insights and your analyzed data.
      </Typography>

      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map((step, index) => (
          <Step key={step.label}>
            <StepLabel
              icon={step.icon}
              optional={index === steps.length - 1 ? (
                <Typography variant="caption">Generate Calendar</Typography>
              ) : null}
            >
              {step.label}
            </StepLabel>
            <StepContent>
              <Box sx={{ mb: 2 }}>
                {renderStepContent(index)}
                <Box sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    onClick={index === steps.length - 1 ? () => onGenerateCalendar(calendarConfig) : handleNext}
                    sx={{ mr: 1 }}
                    disabled={loading}
                  >
                    {index === steps.length - 1 ? 'Generate Calendar' : 'Continue'}
                  </Button>
                  <Button
                    disabled={index === 0}
                    onClick={handleBack}
                    sx={{ mr: 1 }}
                  >
                    Back
                  </Button>
                </Box>
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </Box>
  );
};

export default CalendarGenerationWizard; 