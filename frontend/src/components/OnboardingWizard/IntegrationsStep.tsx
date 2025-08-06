import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Grid,
  Tabs,
  Tab,
  Chip,
  Divider,
  FormControlLabel,
  Switch,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip,
  Fade,
  Zoom,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Add as AddIcon,
  Settings as SettingsIcon,
  Link as LinkIcon,
  Launch as LaunchIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  // Social Media Icons
  Facebook as FacebookIcon,
  Twitter as TwitterIcon,
  Instagram as InstagramIcon,
  LinkedIn as LinkedInIcon,
  YouTube as YouTubeIcon,
  VideoLibrary as TikTokIcon, // Using VideoLibrary as alternative for TikTok
  Pinterest as PinterestIcon,
  // Platform Icons
  Web as WordPressIcon, // Using Web as alternative for WordPress
  Web as WebIcon,
  // AI and Analytics Icons
  Analytics as AnalyticsIcon,
  AutoAwesome as AutoAwesomeIcon,
  TrendingUp as TrendingUpIcon,
  Schedule as ScheduleIcon,
  ContentPaste as ContentPasteIcon,
  SmartToy as SmartToyIcon,
  // Status Icons
  Warning as WarningIcon,
  HelpOutline as HelpOutlineIcon,
  Verified as VerifiedIcon,
  Close as CloseIcon
} from '@mui/icons-material';

interface IntegrationsStepProps {
  onContinue: () => void;
  updateHeaderContent: (content: { title: string; description: string }) => void;
}

interface IntegrationConfig {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  category: 'social' | 'platform' | 'analytics';
  apiKeyField: string;
  apiKeyPlaceholder: string;
  setupUrl: string;
  features: string[];
  isConnected: boolean;
  apiKey: string;
  showApiKey: boolean;
  isEnabled: boolean;
  status: 'connected' | 'disconnected' | 'error' | 'pending';
}

const IntegrationsStep: React.FC<IntegrationsStepProps> = ({ onContinue, updateHeaderContent }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [integrations, setIntegrations] = useState<IntegrationConfig[]>([
    // Social Media Platforms
    {
      id: 'facebook',
      name: 'Facebook',
      description: 'Connect your Facebook page for AI-powered content creation and automated posting',
      icon: <FacebookIcon />,
      category: 'social',
      apiKeyField: 'facebook_access_token',
      apiKeyPlaceholder: 'EAA...',
      setupUrl: 'https://developers.facebook.com/apps/',
      features: ['AI Content Generation', 'Automated Posting', 'Trend Analysis', 'Engagement Tracking'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    {
      id: 'twitter',
      name: 'Twitter/X',
      description: 'Connect your Twitter account for AI-powered tweets and trend analysis',
      icon: <TwitterIcon />,
      category: 'social',
      apiKeyField: 'twitter_bearer_token',
      apiKeyPlaceholder: 'AAAA...',
      setupUrl: 'https://developer.twitter.com/en/portal/dashboard',
      features: ['AI Tweet Generation', 'Trend Analysis', 'Automated Posting', 'Hashtag Optimization'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    {
      id: 'instagram',
      name: 'Instagram',
      description: 'Connect your Instagram account for AI-powered content and caption generation',
      icon: <InstagramIcon />,
      category: 'social',
      apiKeyField: 'instagram_access_token',
      apiKeyPlaceholder: 'IGQ...',
      setupUrl: 'https://developers.facebook.com/apps/',
      features: ['AI Caption Generation', 'Hashtag Optimization', 'Content Scheduling', 'Engagement Analytics'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    {
      id: 'linkedin',
      name: 'LinkedIn',
      description: 'Connect your LinkedIn profile for professional content creation and networking',
      icon: <LinkedInIcon />,
      category: 'social',
      apiKeyField: 'linkedin_access_token',
      apiKeyPlaceholder: 'AQV...',
      setupUrl: 'https://www.linkedin.com/developers/',
      features: ['Professional Content', 'Network Analysis', 'Industry Insights', 'Thought Leadership'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    {
      id: 'youtube',
      name: 'YouTube',
      description: 'Connect your YouTube channel for AI-powered video descriptions and SEO optimization',
      icon: <YouTubeIcon />,
      category: 'social',
      apiKeyField: 'youtube_api_key',
      apiKeyPlaceholder: 'AIza...',
      setupUrl: 'https://console.developers.google.com/',
      features: ['Video Description AI', 'SEO Optimization', 'Trend Analysis', 'Content Strategy'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    {
      id: 'tiktok',
      name: 'TikTok',
      description: 'Connect your TikTok account for AI-powered video captions and trend analysis',
      icon: <TikTokIcon />,
      category: 'social',
      apiKeyField: 'tiktok_access_token',
      apiKeyPlaceholder: 'TikTok...',
      setupUrl: 'https://developers.tiktok.com/',
      features: ['Video Caption AI', 'Trend Analysis', 'Hashtag Optimization', 'Viral Content'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    {
      id: 'pinterest',
      name: 'Pinterest',
      description: 'Connect your Pinterest account for AI-powered pin descriptions and board optimization',
      icon: <PinterestIcon />,
      category: 'social',
      apiKeyField: 'pinterest_access_token',
      apiKeyPlaceholder: 'Pinterest...',
      setupUrl: 'https://developers.pinterest.com/',
      features: ['Pin Description AI', 'Board Optimization', 'Visual Content Strategy', 'SEO Enhancement'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    // Website Platforms
    {
      id: 'wordpress',
      name: 'WordPress',
      description: 'Connect your WordPress site for AI-powered content management and SEO optimization',
      icon: <WordPressIcon />,
      category: 'platform',
      apiKeyField: 'wordpress_api_key',
      apiKeyPlaceholder: 'wp_...',
      setupUrl: 'https://wordpress.org/plugins/rest-api/',
      features: ['AI Content Creation', 'SEO Optimization', 'Automated Publishing', 'Performance Analytics'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    },
    {
      id: 'wix',
      name: 'Wix',
      description: 'Connect your Wix website for AI-powered content management and optimization',
      icon: <WebIcon />,
      category: 'platform',
      apiKeyField: 'wix_api_key',
      apiKeyPlaceholder: 'wix_...',
      setupUrl: 'https://developers.wix.com/',
      features: ['AI Content Creation', 'SEO Optimization', 'Automated Updates', 'Performance Tracking'],
      isConnected: false,
      apiKey: '',
      showApiKey: false,
      isEnabled: false,
      status: 'disconnected'
    }
  ]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    updateHeaderContent({
      title: 'Connect Your Platforms',
      description: 'Integrate your social media accounts and websites to enable AI-powered content creation, automated posting, and comprehensive analytics across all your platforms.'
    });
  }, [updateHeaderContent]);

  useEffect(() => {
    // Prefill integrations on mount
    const fetchIntegrations = async () => {
      try {
        const res = await fetch('/api/onboarding/integrations');
        const data = await res.json();
        if (data.success && Array.isArray(data.integrations)) {
          setIntegrations(prev => prev.map(intg => {
            const found = data.integrations.find((i: any) => i.id === intg.id);
            if (found) {
              return {
                ...intg,
                apiKey: found.apiKey || '',
                isConnected: !!found.isConnected,
                isEnabled: typeof found.isEnabled === 'boolean' ? found.isEnabled : intg.isEnabled,
                status: found.status || intg.status,
              };
            }
            return intg;
          }));
        }
      } catch (err) {
        console.error('IntegrationsStep: Error pre-filling integrations', err);
      }
    };
    fetchIntegrations();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleApiKeyChange = (integrationId: string, value: string) => {
    setIntegrations(prev => prev.map(integration => 
      integration.id === integrationId 
        ? { ...integration, apiKey: value }
        : integration
    ));
  };

  const handleToggleApiKeyVisibility = (integrationId: string) => {
    setIntegrations(prev => prev.map(integration => 
      integration.id === integrationId 
        ? { ...integration, showApiKey: !integration.showApiKey }
        : integration
    ));
  };

  const handleToggleIntegration = (integrationId: string) => {
    setIntegrations(prev => prev.map(integration => 
      integration.id === integrationId 
        ? { ...integration, isEnabled: !integration.isEnabled }
        : integration
    ));
  };

  const handleConnectIntegration = async (integrationId: string) => {
    const integration = integrations.find(i => i.id === integrationId);
    if (!integration) return;

    setLoading(true);
    setError(null);

    try {
      // Simulate API call to connect integration
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setIntegrations(prev => prev.map(i => 
        i.id === integrationId 
          ? { ...i, isConnected: true, status: 'connected' }
          : i
      ));
      
      setSuccess(`${integration.name} connected successfully!`);
    } catch (err) {
      setError(`Failed to connect ${integration.name}. Please check your API key and try again.`);
      setIntegrations(prev => prev.map(i => 
        i.id === integrationId 
          ? { ...i, status: 'error' }
          : i
      ));
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = async () => {
    const connectedIntegrations = integrations.filter(i => i.isConnected);
    if (connectedIntegrations.length === 0) {
      setError('Please connect at least one platform to continue.');
      return;
    }
    
    console.log('IntegrationsStep: handleContinue called');
    console.log('IntegrationsStep: Connected integrations:', connectedIntegrations.length);
    console.log('IntegrationsStep: Current step should be 5 (IntegrationsStep)');
    console.log('IntegrationsStep: Calling onContinue()');
    
    try {
      // Add a small delay to see the logs
      await new Promise(resolve => setTimeout(resolve, 100));
      onContinue();
    } catch (error) {
      console.error('IntegrationsStep: Error in onContinue:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'success';
      case 'error': return 'error';
      case 'pending': return 'warning';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected': return <CheckIcon color="success" />;
      case 'error': return <ErrorIcon color="error" />;
      case 'pending': return <CircularProgress size={16} />;
      default: return <InfoIcon color="action" />;
    }
  };

  const renderIntegrationCard = (integration: IntegrationConfig) => (
    <Zoom in timeout={300}>
      <Card 
        sx={{ 
          mb: 2, 
          border: integration.isConnected ? '2px solid success.main' : '1px solid rgba(0,0,0,0.12)',
          background: integration.isConnected ? 'success.50' : 'background.paper',
          transition: 'all 0.3s ease'
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center" gap={2}>
              <Box sx={{ 
                color: integration.isConnected ? 'success.main' : 'primary.main',
                fontSize: 32 
              }}>
                {integration.icon}
              </Box>
              <Box>
                <Typography variant="h6" fontWeight={600}>
                  {integration.name}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {integration.description}
                </Typography>
              </Box>
            </Box>
            <Box display="flex" alignItems="center" gap={1}>
              {getStatusIcon(integration.status)}
              <Chip 
                label={integration.status} 
                color={getStatusColor(integration.status) as any}
                size="small"
              />
            </Box>
          </Box>

          <Grid container spacing={2} mb={2}>
            <Grid item xs={12} md={8}>
              <TextField
                label={`${integration.name} API Key`}
                type={integration.showApiKey ? 'text' : 'password'}
                value={integration.apiKey}
                onChange={(e) => handleApiKeyChange(integration.id, e.target.value)}
                placeholder={integration.apiKeyPlaceholder}
                fullWidth
                size="small"
                disabled={integration.isConnected}
                InputProps={{
                  endAdornment: (
                    <IconButton
                      onClick={() => handleToggleApiKeyVisibility(integration.id)}
                      edge="end"
                    >
                      {integration.showApiKey ? <VisibilityOffIcon /> : <VisibilityIcon />}
                    </IconButton>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <Box display="flex" gap={1}>
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<LaunchIcon />}
                  onClick={() => window.open(integration.setupUrl, '_blank')}
                  fullWidth
                >
                  Setup Guide
                </Button>
                {!integration.isConnected && (
                  <Button
                    variant="contained"
                    size="small"
                    startIcon={<LinkIcon />}
                    onClick={() => handleConnectIntegration(integration.id)}
                    disabled={!integration.apiKey || loading}
                    fullWidth
                  >
                    Connect
                  </Button>
                )}
              </Box>
            </Grid>
          </Grid>

          <Box mb={2}>
            <Typography variant="subtitle2" color="primary" gutterBottom>
              Features:
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {integration.features.map((feature, index) => (
                <Chip
                  key={index}
                  label={feature}
                  size="small"
                  variant="outlined"
                  icon={<AutoAwesomeIcon />}
                />
              ))}
            </Box>
          </Box>

          <FormControlLabel
            control={
              <Switch
                checked={integration.isEnabled}
                onChange={() => handleToggleIntegration(integration.id)}
                disabled={!integration.isConnected}
              />
            }
            label="Enable AI-powered features for this platform"
          />
        </CardContent>
      </Card>
    </Zoom>
  );

  const renderTabContent = (category: 'social' | 'platform' | 'analytics') => {
    const categoryIntegrations = integrations.filter(i => i.category === category);
    
    return (
      <Box>
        {categoryIntegrations.map(integration => renderIntegrationCard(integration))}
      </Box>
    );
  };

  const connectedCount = integrations.filter(i => i.isConnected).length;
  const enabledCount = integrations.filter(i => i.isEnabled).length;

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      {/* Header Section */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Connect Your Platforms
        </Typography>
        <Typography variant="body1" color="textSecondary" sx={{ mb: 3, maxWidth: 800, mx: 'auto' }}>
          Integrate your social media accounts and websites to enable AI-powered content creation, 
          automated posting, and comprehensive analytics across all your platforms.
        </Typography>
        
        {/* Stats Cards */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary" fontWeight={700}>
                {integrations.length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Available Platforms
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="success.main" fontWeight={700}>
                {connectedCount}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Connected Platforms
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="info.main" fontWeight={700}>
                {enabledCount}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                AI Features Enabled
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* Info Alert */}
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>How it works:</strong> Connect your platforms using their API keys. Once connected, 
          ALwrity can generate AI-powered content, analyze trends, and automatically post to your platforms. 
          Your API keys are securely stored and never shared.
        </Typography>
      </Alert>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}

      {/* Tabs for Different Categories */}
      <Paper elevation={2} sx={{ mb: 3 }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          variant="fullWidth"
          sx={{
            borderBottom: 1,
            borderColor: 'divider',
            '& .MuiTab-root': {
              textTransform: 'none',
              fontWeight: 600,
              fontSize: '1rem'
            }
          }}
        >
          <Tab 
            label={
              <Box display="flex" alignItems="center" gap={1}>
                <AutoAwesomeIcon />
                Social Media ({integrations.filter(i => i.category === 'social').length})
              </Box>
            } 
          />
          <Tab 
            label={
              <Box display="flex" alignItems="center" gap={1}>
                <WebIcon />
                Website Platforms ({integrations.filter(i => i.category === 'platform').length})
              </Box>
            } 
          />
        </Tabs>
      </Paper>

      {/* Tab Content */}
      <Box sx={{ mb: 4 }}>
        {activeTab === 0 && renderTabContent('social')}
        {activeTab === 1 && renderTabContent('platform')}
      </Box>

      {/* Features Preview */}
      {connectedCount > 0 && (
        <Accordion sx={{ mb: 3 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box display="flex" alignItems="center" gap={1}>
              <SmartToyIcon color="primary" />
              <Typography variant="h6">AI Features Preview</Typography>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <ContentPasteIcon color="primary" />
                    <Typography variant="h6">Content Creation</Typography>
                  </Box>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="AI-powered content generation" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Platform-specific optimization" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Hashtag and SEO optimization" />
                    </ListItem>
                  </List>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <ScheduleIcon color="primary" />
                    <Typography variant="h6">Automation</Typography>
                  </Box>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Automated posting schedules" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Cross-platform content distribution" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Smart timing optimization" />
                    </ListItem>
                  </List>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <AnalyticsIcon color="primary" />
                    <Typography variant="h6">Analytics</Typography>
                  </Box>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Performance tracking" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Trend analysis" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Engagement insights" />
                    </ListItem>
                  </List>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <TrendingUpIcon color="primary" />
                    <Typography variant="h6">Optimization</Typography>
                  </Box>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Content performance optimization" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="Audience targeting" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" /></ListItemIcon>
                      <ListItemText primary="ROI tracking" />
                    </ListItem>
                  </List>
                </Card>
              </Grid>
            </Grid>
          </AccordionDetails>
        </Accordion>
      )}

      {/* Continue Button */}
      <Box display="flex" justifyContent="center" mt={4}>
        <Button
          variant="contained"
          size="large"
          onClick={handleContinue}
          disabled={connectedCount === 0}
          startIcon={connectedCount > 0 ? <CheckIcon /> : <WarningIcon />}
          sx={{
            px: 4,
            py: 1.5,
            fontSize: '1.1rem',
            fontWeight: 600,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
            }
          }}
        >
          {connectedCount === 0 
            ? 'Connect at least one platform to continue' 
            : `Continue with ${connectedCount} connected platform${connectedCount > 1 ? 's' : ''}`
          }
        </Button>
      </Box>
    </Box>
  );
};

export default IntegrationsStep; 