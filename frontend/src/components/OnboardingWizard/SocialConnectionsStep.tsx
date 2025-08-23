import React, { useEffect, useState } from 'react';
import WebsiteAuditDashboard from '../GSCWebsiteAudit/WebsiteAuditDashboard';
import {
  Box,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Grid,
  Chip,
  IconButton,
  Tooltip,
  Fade,
  Zoom,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Link as LinkIcon,
  Launch as LaunchIcon,
  Analytics as AnalyticsIcon,
  AutoAwesome as AutoAwesomeIcon,
  TrendingUp as TrendingUpIcon,
  Schedule as ScheduleIcon,
  ContentPaste as ContentPasteIcon,
  SmartToy as SmartToyIcon,
  Google as GoogleIcon,
  Facebook as FacebookIcon,
  Twitter as TwitterIcon,
  LinkedIn as LinkedInIcon,
  YouTube as YouTubeIcon,
  Pinterest as PinterestIcon,
  VideoLibrary as TikTokIcon,
  Instagram as InstagramIcon,
  Refresh as RefreshIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

interface SocialConnectionsStepProps {
  onContinue: () => void;
  updateHeaderContent: (content: { title: string; description: string }) => void;
}

interface Platform {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  features: string[];
  isConnected: boolean;
  connectionData?: any;
}

interface Connection {
  id: number;
  platform: string;
  platform_username: string;
  connection_status: string;
  auto_post_enabled: boolean;
  analytics_enabled: boolean;
  connected_at: string;
  profile_data: any;
}

const SocialConnectionsStep: React.FC<SocialConnectionsStepProps> = ({ onContinue, updateHeaderContent }) => {
  const [platforms, setPlatforms] = useState<Platform[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [authWindow, setAuthWindow] = useState<Window | null>(null);
  const [showGSCDemo, setShowGSCDemo] = useState(false);
  const [gscDemoData, setGscDemoData] = useState<any>(null);
  const [connectingPlatform, setConnectingPlatform] = useState<string | null>(null);
  const [testingConnection, setTestingConnection] = useState<number | null>(null);
  const [connectionDetails, setConnectionDetails] = useState<any>(null);
  const [showBenefits, setShowBenefits] = useState<string | null>(null);
  const [showWebsiteAudit, setShowWebsiteAudit] = useState(false);

  useEffect(() => {
    updateHeaderContent({
      title: 'Connect Your Platforms',
      description: 'Connect your social media accounts and Google Search Console to unlock powerful analytics and automated content features.'
    });
    
    // Load platforms and connections
    loadPlatforms();
    loadConnections();
  }, [updateHeaderContent]);

  const loadPlatforms = async () => {
    try {
      const response = await fetch('/api/social/test/platforms');
      const data = await response.json();
      
      if (data.supported_platforms) {
        const platformsWithIcons = data.supported_platforms.map((platform: any) => ({
          ...platform,
          icon: getPlatformIcon(platform.id),
          isConnected: false,
          connectionData: null
        }));
        setPlatforms(platformsWithIcons);
      }
    } catch (err) {
      console.error('Failed to load platforms:', err);
      setError('Failed to load available platforms');
    }
  };

  const getPlatformIcon = (platformId: string) => {
    const iconMap: { [key: string]: React.ReactNode } = {
      'google_search_console': <GoogleIcon />,
      'youtube': <YouTubeIcon />,
      'facebook': <FacebookIcon />,
      'instagram': <InstagramIcon />,
      'twitter': <TwitterIcon />,
      'linkedin': <LinkedInIcon />,
      'tiktok': <TikTokIcon />,
      'pinterest': <PinterestIcon />,
      'snapchat': <SmartToyIcon />, // Using SmartToy as alternative
      'reddit': <SmartToyIcon />, // Using SmartToy as alternative
      'discord': <SmartToyIcon /> // Using SmartToy as alternative
    };
    return iconMap[platformId] || <SmartToyIcon />;
  };

  const loadConnections = async () => {
    try {
      const response = await fetch('/api/social/connections');
      const result = await response.json();
      
      if (Array.isArray(result)) {
        setConnections(result);
        
        // Update platform connection status
        setPlatforms(prev => prev.map(platform => {
          const connection = result.find((conn: Connection) => conn.platform === platform.id);
          return {
            ...platform,
            isConnected: !!connection && connection.connection_status === 'active',
            connectionData: connection
          };
        }));
      }
    } catch (err) {
      console.error('Failed to load connections:', err);
    }
  };

  const handleConnect = async (platformId: string) => {
    setConnectingPlatform(platformId);
    setError(null);
    setSuccess(null);

    try {
      // Get OAuth URL
      const response = await fetch(`/api/social/auth/${platformId}?user_id=1`);
      const data = await response.json();
      
      if (data.auth_url) {
        // Open OAuth window
        const width = 600;
        const height = 700;
        const left = window.screenX + (window.innerWidth - width) / 2;
        const top = window.screenY + (window.innerHeight - height) / 2;
        
        const authWindow = window.open(
          data.auth_url,
          'oauth',
          `width=${width},height=${height},left=${left},top=${top},scrollbars=yes,resizable=yes`
        );
        
        setAuthWindow(authWindow);
        
        // Monitor auth window
        const checkClosed = setInterval(() => {
          if (authWindow?.closed) {
            clearInterval(checkClosed);
            setAuthWindow(null);
            // Reload connections to check if successful
            setTimeout(async () => {
              await loadConnections();
              
              // Check if the connection was successful and show benefits
              const newConnection = connections.find(c => c.platform === platformId);
              if (newConnection) {
                setSuccess(`Successfully connected ${platformId}!`);
                setShowBenefits(platformId);
                
                // Auto-hide benefits after 10 seconds
                setTimeout(() => setShowBenefits(null), 10000);
              }
              
              setConnectingPlatform(null);
            }, 1000);
          }
        }, 1000);
        
        // Set timeout for auth
        setTimeout(() => {
          if (authWindow && !authWindow.closed) {
            authWindow.close();
            setAuthWindow(null);
            setConnectingPlatform(null);
            setError('Authentication timed out. Please try again.');
          }
        }, 300000); // 5 minutes timeout
      }
    } catch (err) {
      setError(`Failed to connect ${platformId}. Please try again.`);
      setConnectingPlatform(null);
    }
  };

  const testConnection = async (connectionId: number) => {
    setTestingConnection(connectionId);
    try {
      const response = await fetch(`/api/social/connections/${connectionId}/test`, {
        method: 'POST'
      });
      const result = await response.json();
      
      if (result.status === 'passed') {
        setSuccess('Connection test passed successfully!');
      } else if (result.status === 'failed') {
        setError(`Connection test failed: ${result.errors.join(', ')}`);
      } else {
        setError('Connection test completed with warnings. Check connection details.');
      }
      
      setConnectionDetails(result);
      
    } catch (err) {
      setError('Failed to test connection');
    } finally {
      setTestingConnection(null);
    }
  };

  const handleDisconnect = async (connectionId: number) => {
    try {
      const response = await fetch(`/api/social/connections/${connectionId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        setSuccess('Platform disconnected successfully');
        loadConnections();
      } else {
        setError('Failed to disconnect platform');
      }
    } catch (err) {
      setError('Failed to disconnect platform');
    }
  };

  const showGSCDemoData = async () => {
    if (!platforms.find(p => p.id === 'google_search_console')?.isConnected) {
      setError('Please connect Google Search Console first');
      return;
    }

    setShowGSCDemo(true);
    
    try {
      const connection = connections.find(c => c.platform === 'google_search_console');
      if (connection) {
        // Fetch demo data from connected GSC
        const sitesResponse = await fetch(`/api/social/gsc/${connection.id}/sites`);
        const sitesData = await sitesResponse.json();
        
        if (sitesData.success && sitesData.sites.length > 0) {
          const siteUrl = sitesData.sites[0].siteUrl;
          
          // Fetch performance data
          const perfResponse = await fetch(`/api/social/gsc/${connection.id}/analytics/performance?site_url=${encodeURIComponent(siteUrl)}`);
          const perfData = await perfResponse.json();
          
          setGscDemoData({
            sites: sitesData.sites,
            performance: perfData.data
          });
        }
      }
    } catch (err) {
      console.error('Failed to fetch GSC demo data:', err);
      setGscDemoData({
        error: 'Failed to fetch data'
      });
    }
  };

  const getBenefitsForPlatform = (platformId: string) => {
    const benefits: { [key: string]: string[] } = {
      'google_search_console': [
        'Track your website\'s search performance in real-time',
        'Identify top-performing keywords and optimize content',
        'Monitor search rankings and click-through rates',
        'Discover content gaps and opportunities'
      ],
      'youtube': [
        'Analyze video performance and audience engagement',
        'Optimize video titles and descriptions with AI',
        'Track subscriber growth and viewer demographics',
        'Schedule and manage content uploads'
      ],
      'facebook': [
        'Post content directly to your Facebook pages',
        'Analyze post engagement and reach metrics',
        'Schedule posts for optimal engagement times',
        'Monitor audience growth and demographics'
      ],
      'instagram': [
        'Share photos and videos to your Instagram business account',
        'Optimize hashtags for maximum reach',
        'Track story and post engagement metrics',
        'Analyze follower growth and audience insights'
      ],
      'twitter': [
        'Tweet content automatically or on schedule',
        'Monitor engagement rates and retweet metrics',
        'Analyze follower growth and audience activity',
        'Track trending topics and hashtag performance'
      ],
      'linkedin': [
        'Share professional content to boost your network',
        'Analyze post performance in professional context',
        'Track connection growth and engagement rates',
        'Monitor industry-specific content performance'
      ],
      'tiktok': [
        'Analyze video performance and viral potential',
        'Track trending sounds and hashtags',
        'Monitor follower demographics and engagement',
        'Optimize content for TikTok algorithm'
      ],
      'pinterest': [
        'Pin content to relevant boards automatically',
        'Analyze pin performance and board engagement',
        'Track seasonal trends and popular pins',
        'Optimize visual content for Pinterest discovery'
      ]
    };
    return benefits[platformId] || ['Enhanced analytics and automated posting capabilities'];
  };

  const renderBenefitsModal = () => {
    if (!showBenefits) return null;
    
    const platform = platforms.find(p => p.id === showBenefits);
    if (!platform) return null;
    
    return (
      <Dialog 
        open={!!showBenefits} 
        onClose={() => setShowBenefits(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={2}>
            <Box sx={{ fontSize: 32 }}>{platform.icon}</Box>
            <Box>
              <Typography variant="h5" fontWeight={600}>
                🎉 {platform.name} Connected Successfully!
              </Typography>
              <Typography variant="body2" color="textSecondary">
                You can now unlock these powerful features:
              </Typography>
            </Box>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            {getBenefitsForPlatform(showBenefits).map((benefit, index) => (
              <Grid item xs={12} key={index}>
                <Box display="flex" alignItems="center" gap={2}>
                  <CheckIcon color="success" />
                  <Typography variant="body1">{benefit}</Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
          
          <Box mt={3} p={2} bgcolor="primary.50" borderRadius={2}>
            <Typography variant="h6" color="primary" gutterBottom>
              🚀 What's Next?
            </Typography>
            <Typography variant="body2">
              Your {platform.name} account is now integrated with ALwrity. You can start using these features 
              immediately in your content strategy and analytics dashboard. All data is synced automatically 
              and refreshed regularly to keep your insights up-to-date.
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowBenefits(null)} variant="contained">
            Got it!
          </Button>
        </DialogActions>
      </Dialog>
    );
  };

  const renderPlatformCard = (platform: Platform) => (
    <Grid item xs={12} md={6} key={platform.id}>
      <Zoom in timeout={300}>
        <Card 
          sx={{ 
            height: '100%',
            border: platform.isConnected ? '2px solid' : '1px solid rgba(0,0,0,0.12)',
            borderColor: platform.isConnected ? 'success.main' : 'rgba(0,0,0,0.12)',
            background: platform.isConnected ? 'success.50' : 'background.paper',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: 3
            }
          }}
        >
          <CardContent sx={{ p: 3, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
              <Box display="flex" alignItems="center" gap={2}>
                <Box sx={{ 
                  color: platform.isConnected ? 'success.main' : 'primary.main',
                  fontSize: 32 
                }}>
                  {platform.icon}
                </Box>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    {platform.name}
                  </Typography>
                  <Chip 
                    label={platform.isConnected ? 'Connected' : 'Not Connected'} 
                    color={platform.isConnected ? 'success' : 'default'}
                    size="small"
                    icon={platform.isConnected ? <CheckIcon /> : <InfoIcon />}
                  />
                </Box>
              </Box>
            </Box>

            <Typography variant="body2" color="textSecondary" mb={2} sx={{ flexGrow: 1 }}>
              {platform.description}
            </Typography>

            <Box mb={2}>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                Features:
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {platform.features.map((feature, index) => (
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

            <Box display="flex" gap={1} mt="auto">
              {platform.isConnected ? (
                <>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<CheckIcon />}
                    disabled
                    sx={{ flex: 1 }}
                  >
                    Connected
                  </Button>
                  <Tooltip title="Test Connection">
                    <IconButton
                      color="primary"
                      onClick={() => platform.connectionData && testConnection(platform.connectionData.id)}
                      disabled={testingConnection === platform.connectionData?.id}
                    >
                      {testingConnection === platform.connectionData?.id ? 
                        <CircularProgress size={20} /> : 
                        <RefreshIcon />
                      }
                    </IconButton>
                  </Tooltip>
                  {platform.id === 'google_search_console' && (
                    <>
                      <Tooltip title="View GSC Demo">
                        <IconButton
                          color="primary"
                          onClick={showGSCDemoData}
                        >
                          <AnalyticsIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Website Audit">
                        <IconButton
                          color="secondary"
                          onClick={() => setShowWebsiteAudit(true)}
                        >
                          <SpeedIcon />
                        </IconButton>
                      </Tooltip>
                    </>
                  )}
                  <Tooltip title="View Benefits">
                    <IconButton
                      color="info"
                      onClick={() => setShowBenefits(platform.id)}
                    >
                      <InfoIcon />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Disconnect">
                    <IconButton
                      color="error"
                      onClick={() => platform.connectionData && handleDisconnect(platform.connectionData.id)}
                    >
                      <ErrorIcon />
                    </IconButton>
                  </Tooltip>
                </>
              ) : (
                <Button
                  variant="contained"
                  size="small"
                  startIcon={connectingPlatform === platform.id ? 
                    <CircularProgress size={16} color="inherit" /> : 
                    <LinkIcon />
                  }
                  onClick={() => handleConnect(platform.id)}
                  disabled={connectingPlatform === platform.id}
                  fullWidth
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                    }
                  }}
                >
                  {connectingPlatform === platform.id ? 'Connecting...' : 'Connect'}
                </Button>
              )}
            </Box>
          </CardContent>
        </Card>
      </Zoom>
    </Grid>
  );

  const connectedCount = platforms.filter(p => p.isConnected).length;
  const gscConnected = platforms.find(p => p.id === 'google_search_console')?.isConnected;

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      {/* Header Section */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Connect Your Platforms
        </Typography>
        <Typography variant="body1" color="textSecondary" sx={{ mb: 3, maxWidth: 800, mx: 'auto' }}>
          Connect your social media accounts and Google Search Console to unlock powerful AI-driven analytics, 
          automated content creation, and comprehensive performance insights.
        </Typography>
        
        {/* Progress Stats */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary" fontWeight={700}>
                {platforms.length}
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
              <LinearProgress 
                variant="determinate" 
                value={(connectedCount / platforms.length) * 100}
                sx={{ height: 8, borderRadius: 4, mb: 1 }}
              />
              <Typography variant="body2" color="textSecondary">
                {Math.round((connectedCount / platforms.length) * 100)}% Complete
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* Special GSC Recommendation */}
      {!gscConnected && (
        <Alert severity="info" sx={{ mb: 3 }}>
          <Typography variant="body2">
            <strong>Recommended:</strong> Start by connecting Google Search Console to unlock powerful SEO insights 
            and analytics for your content strategy. This will help ALwrity understand your website's performance 
            and optimize content accordingly.
          </Typography>
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {loading && (
        <Box display="flex" justifyContent="center" alignItems="center" mb={3}>
          <CircularProgress size={24} sx={{ mr: 2 }} />
          <Typography>Connecting platform...</Typography>
        </Box>
      )}

      {/* Platform Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {platforms.map(platform => renderPlatformCard(platform))}
      </Grid>

      {/* Benefits Section */}
      {connectedCount > 0 && (
        <Card sx={{ mb: 4, background: 'linear-gradient(135deg, #f6f9fc 0%, #e9f4f9 100%)' }}>
          <CardContent sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" gap={1} mb={2}>
              <SmartToyIcon color="primary" />
              <Typography variant="h6">Your Connected Features</Typography>
            </Box>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <List dense>
                  <ListItem>
                    <ListItemIcon><ContentPasteIcon color="success" /></ListItemIcon>
                    <ListItemText primary="AI-powered content generation based on your data" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon><AnalyticsIcon color="success" /></ListItemIcon>
                    <ListItemText primary="Cross-platform analytics and insights" />
                  </ListItem>
                </List>
              </Grid>
              <Grid item xs={12} md={6}>
                <List dense>
                  <ListItem>
                    <ListItemIcon><ScheduleIcon color="success" /></ListItemIcon>
                    <ListItemText primary="Automated content scheduling and posting" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon><TrendingUpIcon color="success" /></ListItemIcon>
                    <ListItemText primary="Performance optimization recommendations" />
                  </ListItem>
                </List>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Continue Button */}
      <Box display="flex" justifyContent="center" mt={4}>
        <Button
          variant="contained"
          size="large"
          onClick={onContinue}
          startIcon={connectedCount > 0 ? <CheckIcon /> : <InfoIcon />}
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
            ? 'Skip for now - Continue Setup' 
            : `Continue with ${connectedCount} connected platform${connectedCount > 1 ? 's' : ''}`
          }
        </Button>
      </Box>

      {/* GSC Demo Dialog */}
      <Dialog 
        open={showGSCDemo} 
        onClose={() => setShowGSCDemo(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <GoogleIcon color="primary" />
            Google Search Console - Live Data
          </Box>
        </DialogTitle>
        <DialogContent>
          {gscDemoData ? (
            gscDemoData.error ? (
              <Alert severity="error">{gscDemoData.error}</Alert>
            ) : (
              <Box>
                <Typography variant="h6" gutterBottom>Connected Sites:</Typography>
                {gscDemoData.sites?.map((site: any, index: number) => (
                  <Chip key={index} label={site.siteUrl} sx={{ mr: 1, mb: 1 }} />
                ))}
                
                {gscDemoData.performance && (
                  <Box mt={2}>
                    <Typography variant="h6" gutterBottom>Performance Summary:</Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <Typography variant="h5" color="primary">
                            {gscDemoData.performance.totals?.clicks || 0}
                          </Typography>
                          <Typography variant="body2">Total Clicks</Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <Typography variant="h5" color="info.main">
                            {gscDemoData.performance.totals?.impressions || 0}
                          </Typography>
                          <Typography variant="body2">Impressions</Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <Typography variant="h5" color="success.main">
                            {(gscDemoData.performance.totals?.ctr * 100).toFixed(2) || 0}%
                          </Typography>
                          <Typography variant="body2">CTR</Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <Typography variant="h5" color="warning.main">
                            {gscDemoData.performance.totals?.position?.toFixed(1) || 0}
                          </Typography>
                          <Typography variant="body2">Avg Position</Typography>
                        </Paper>
                      </Grid>
                    </Grid>
                  </Box>
                )}
              </Box>
            )
          ) : (
            <Box display="flex" justifyContent="center" p={3}>
              <CircularProgress />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowGSCDemo(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Benefits Modal */}
      {renderBenefitsModal()}

      {/* Website Audit Modal */}
      <Dialog 
        open={showWebsiteAudit} 
        onClose={() => setShowWebsiteAudit(false)}
        maxWidth="xl"
        fullWidth
        fullScreen
      >
        <DialogTitle>
          <Typography variant="h5">
            Google Search Console Website Audit
          </Typography>
        </DialogTitle>
        <DialogContent>
          <WebsiteAuditDashboard />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowWebsiteAudit(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SocialConnectionsStep;