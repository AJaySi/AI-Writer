import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Button, 
  Typography, 
  Alert, 
  Paper,
  Container,
  Fade,
  Zoom,
  Grid,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Card,
  CardContent,
  IconButton,
  Tooltip,
  CircularProgress
} from '@mui/material';
import { 
  CheckCircle, 
  Rocket,
  Star,
  TrendingUp,
  Security,
  ExpandMore,
  Visibility,
  VisibilityOff,
  Lock,
  LockOpen,
  Settings,
  Web,
  Psychology,
  Business,
  ContentCopy
} from '@mui/icons-material';
import OnboardingButton from './common/OnboardingButton';
import { getApiKeys, completeOnboarding, getOnboardingSummary, getWebsiteAnalysisData, getResearchPreferencesData, setCurrentStep } from '../../api/onboarding';

interface FinalStepProps {
  onContinue: () => void;
  updateHeaderContent: (content: { title: string; description: string }) => void;
}

interface OnboardingData {
  apiKeys: Record<string, string>;
  websiteUrl?: string;
  researchPreferences?: any;
  personalizationSettings?: any;
  integrations?: any;
  styleAnalysis?: any;
}

interface Capability {
  id: string;
  title: string;
  description: string;
  icon: React.ReactElement;
  unlocked: boolean;
  required?: string[];
}

const FinalStep: React.FC<FinalStepProps> = ({ onContinue, updateHeaderContent }) => {
  const [loading, setLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [onboardingData, setOnboardingData] = useState<OnboardingData>({
    apiKeys: {}
  });
  const [showApiKeys, setShowApiKeys] = useState(false);
  const [expandedSection, setExpandedSection] = useState<string | null>('summary');

  useEffect(() => {
    updateHeaderContent({
      title: 'Review & Launch Alwrity 🚀',
      description: 'Review your configuration and confirm all settings before launching your AI-powered content creation workspace.'
    });
    loadOnboardingData();
  }, [updateHeaderContent]);

  const loadOnboardingData = async () => {
    setDataLoading(true);
    try {
      // Load comprehensive onboarding summary
      const summary = await getOnboardingSummary();
      
      // Load individual data sources for detailed information
      const websiteAnalysis = await getWebsiteAnalysisData();
      const researchPreferences = await getResearchPreferencesData();
      
      setOnboardingData({
        apiKeys: summary.api_keys || {},
        websiteUrl: websiteAnalysis?.website_url || summary.website_url,
        researchPreferences: researchPreferences || summary.research_preferences,
        personalizationSettings: summary.personalization_settings,
        integrations: summary.integrations || {},
        styleAnalysis: websiteAnalysis?.style_analysis || summary.style_analysis
      });
    } catch (error) {
      console.error('Error loading onboarding data:', error);
      // Fallback to just API keys if other endpoints fail
      try {
        const apiKeys = await getApiKeys();
        setOnboardingData({
          apiKeys,
          websiteUrl: undefined,
          researchPreferences: undefined,
          personalizationSettings: undefined,
          integrations: undefined,
          styleAnalysis: undefined
        });
      } catch (fallbackError) {
        console.error('Error loading API keys as fallback:', fallbackError);
      }
    } finally {
      setDataLoading(false);
    }
  };

  const handleLaunch = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('FinalStep: Starting onboarding completion...');
      
      // First, complete step 6 (Final Step) to mark it as completed
      console.log('FinalStep: Completing step 6...');
      await setCurrentStep(6);
      console.log('FinalStep: Step 6 completed successfully');
      
      // Then complete the entire onboarding process
      console.log('FinalStep: Completing onboarding...');
      await completeOnboarding();
      console.log('FinalStep: Onboarding completed successfully');
      
      // Navigate directly to dashboard without calling onContinue
      // This bypasses the wizard flow and goes straight to the dashboard
      console.log('FinalStep: Navigating to dashboard...');
      window.location.href = '/dashboard';
    } catch (e: any) {
      console.error('FinalStep: Error completing onboarding:', e);
      
      // Provide more specific error messages
      let errorMessage = 'Failed to complete onboarding. Please try again.';
      
      if (e.response?.data?.detail) {
        errorMessage = e.response.data.detail;
      } else if (e.message) {
        errorMessage = e.message;
      }
      
      setError(errorMessage);
    }
    setLoading(false);
  };

  const capabilities: Capability[] = [
    {
      id: 'ai-content',
      title: 'AI Content Generation',
      description: 'Generate high-quality, personalized content using advanced AI models',
      icon: <ContentCopy />,
      unlocked: Object.keys(onboardingData.apiKeys).length > 0,
      required: ['API Keys']
    },
    {
      id: 'style-analysis',
      title: 'Style Analysis',
      description: 'Analyze and match your brand\'s writing style and tone',
      icon: <Psychology />,
      unlocked: !!onboardingData.websiteUrl,
      required: ['Website URL']
    },
    {
      id: 'research-tools',
      title: 'AI Research Tools',
      description: 'Automated research and fact-checking capabilities',
      icon: <TrendingUp />,
      unlocked: !!onboardingData.researchPreferences,
      required: ['Research Configuration']
    },
    {
      id: 'personalization',
      title: 'Content Personalization',
      description: 'Tailored content based on your brand voice and preferences',
      icon: <Settings />,
      unlocked: !!onboardingData.personalizationSettings,
      required: ['Personalization Settings']
    },
    {
      id: 'integrations',
      title: 'Third-party Integrations',
      description: 'Connect with external tools and platforms',
      icon: <Business />,
      unlocked: !!onboardingData.integrations,
      required: ['Integration Setup']
    }
  ];

  const getConfiguredProviders = () => {
    return Object.keys(onboardingData.apiKeys).map(provider => ({
      name: provider.charAt(0).toUpperCase() + provider.slice(1),
      configured: true
    }));
  };

  const getMissingRequirements = () => {
    const missing = [];
    if (Object.keys(onboardingData.apiKeys).length === 0) {
      missing.push('At least one AI provider API key');
    }
    if (!onboardingData.websiteUrl) {
      missing.push('Website URL for style analysis');
    }
    return missing;
  };

  const unlockedCapabilities = capabilities.filter(cap => cap.unlocked);
  const missingRequirements = getMissingRequirements();

  return (
    <Fade in={true} timeout={500}>
      <Container maxWidth="lg" sx={{ py: 2 }}>
        {/* Loading State */}
        {dataLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 8 }}>
            <Box sx={{ textAlign: 'center' }}>
              <CircularProgress size={60} sx={{ mb: 2 }} />
              <Typography variant="h6" sx={{ mb: 1 }}>
                Loading your configuration...
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Retrieving your onboarding data and settings
              </Typography>
            </Box>
          </Box>
        )}

        {/* Content - Only show when data is loaded */}
        {!dataLoading && (
          <React.Fragment>
            {/* Summary Section */}
            <Zoom in={true} timeout={800}>
              <Paper elevation={0} sx={{ 
                p: 4, 
                mb: 4,
                background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)',
                border: '1px solid rgba(16, 185, 129, 0.2)',
                borderRadius: 3
              }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <CheckCircle sx={{ color: 'success.main', fontSize: 32 }} />
                    <Typography variant="h4" color="success.main" sx={{ fontWeight: 600 }}>
                      Setup Summary
                    </Typography>
                  </Box>
                  <Chip 
                    label={`${unlockedCapabilities.length}/${capabilities.length} Capabilities Unlocked`}
                    color="success"
                    variant="filled"
                    icon={<LockOpen />}
                  />
                </Box>

                <Grid container spacing={3}>
                  {/* Configured Providers */}
                  <Grid item xs={12} md={6}>
                    <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.7)', borderRadius: 2 }}>
                      <CardContent>
                        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Security sx={{ color: 'primary.main' }} />
                          AI Providers
                        </Typography>
                        <List dense>
                          {getConfiguredProviders().map((provider, index) => (
                            <ListItem key={index} sx={{ px: 0 }}>
                              <ListItemIcon sx={{ minWidth: 36 }}>
                                <CheckCircle sx={{ color: 'success.main', fontSize: 20 }} />
                              </ListItemIcon>
                              <ListItemText 
                                primary={provider.name}
                                secondary="API key configured"
                              />
                            </ListItem>
                          ))}
                        </List>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Quick Stats */}
                  <Grid item xs={12} md={6}>
                    <Card elevation={0} sx={{ background: 'rgba(255, 255, 255, 0.7)', borderRadius: 2 }}>
                      <CardContent>
                        <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                          <TrendingUp sx={{ color: 'primary.main' }} />
                          Quick Stats
                        </Typography>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body2">AI Providers:</Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {Object.keys(onboardingData.apiKeys).length} configured
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body2">Capabilities:</Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {unlockedCapabilities.length} unlocked
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="body2">Missing:</Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600, color: missingRequirements.length > 0 ? 'warning.main' : 'success.main' }}>
                              {missingRequirements.length} requirements
                            </Typography>
                          </Box>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Paper>
            </Zoom>

            {/* Detailed Configuration Review */}
            <Zoom in={true} timeout={1000}>
              <Paper elevation={0} sx={{ 
                p: 4, 
                mb: 4,
                background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
                border: '1px solid rgba(59, 130, 246, 0.2)',
                borderRadius: 3
              }}>
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Settings sx={{ color: 'primary.main' }} />
                  Configuration Details
                </Typography>

                <Grid container spacing={3}>
                  {/* API Keys Section */}
                  <Grid item xs={12} md={6}>
                    <Accordion 
                      expanded={expandedSection === 'api-keys'}
                      onChange={() => setExpandedSection(expandedSection === 'api-keys' ? null : 'api-keys')}
                      sx={{ background: 'rgba(255, 255, 255, 0.8)', borderRadius: 2 }}
                    >
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                          <Security sx={{ color: 'primary.main' }} />
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            API Keys ({Object.keys(onboardingData.apiKeys).length} configured)
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                          {Object.entries(onboardingData.apiKeys).map(([provider, key]) => (
                            <Box key={provider} sx={{ 
                              p: 2, 
                              border: '1px solid rgba(0,0,0,0.1)', 
                              borderRadius: 1,
                              background: 'rgba(255,255,255,0.5)'
                            }}>
                              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                                <Typography variant="subtitle2" sx={{ fontWeight: 600, textTransform: 'capitalize' }}>
                                  {provider}
                                </Typography>
                                <Box sx={{ display: 'flex', gap: 1 }}>
                                  <Tooltip title={showApiKeys ? 'Hide key' : 'Show key'}>
                                    <IconButton 
                                      size="small" 
                                      onClick={() => setShowApiKeys(!showApiKeys)}
                                    >
                                      {showApiKeys ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                  </Tooltip>
                                </Box>
                              </Box>
                              <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                                {showApiKeys ? key : '••••••••••••••••••••••••••••••••'}
                              </Typography>
                            </Box>
                          ))}
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  </Grid>

                  {/* Website Configuration */}
                  <Grid item xs={12} md={6}>
                    <Accordion 
                      expanded={expandedSection === 'website'}
                      onChange={() => setExpandedSection(expandedSection === 'website' ? null : 'website')}
                      sx={{ background: 'rgba(255, 255, 255, 0.8)', borderRadius: 2 }}
                    >
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                          <Web sx={{ color: 'primary.main' }} />
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            Website Analysis
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        {onboardingData.websiteUrl ? (
                          <Box>
                            <Typography variant="body2" sx={{ mb: 2 }}>
                              <strong>URL:</strong> {onboardingData.websiteUrl}
                            </Typography>
                            {onboardingData.styleAnalysis && (
                              <Typography variant="body2" color="success.main">
                                ✓ Style analysis completed
                              </Typography>
                            )}
                          </Box>
                        ) : (
                          <Typography variant="body2" color="warning.main">
                            ⚠️ No website URL configured
                          </Typography>
                        )}
                      </AccordionDetails>
                    </Accordion>
                  </Grid>

                  {/* Research Preferences */}
                  <Grid item xs={12} md={6}>
                    <Accordion 
                      expanded={expandedSection === 'research'}
                      onChange={() => setExpandedSection(expandedSection === 'research' ? null : 'research')}
                      sx={{ background: 'rgba(255, 255, 255, 0.8)', borderRadius: 2 }}
                    >
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                          <TrendingUp sx={{ color: 'primary.main' }} />
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            Research Configuration
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        {onboardingData.researchPreferences ? (
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                            <Typography variant="body2">
                              <strong>Depth:</strong> {onboardingData.researchPreferences.research_depth}
                            </Typography>
                            <Typography variant="body2">
                              <strong>Content Types:</strong> {onboardingData.researchPreferences.content_types?.join(', ')}
                            </Typography>
                            <Typography variant="body2">
                              <strong>Auto Research:</strong> {onboardingData.researchPreferences.auto_research ? 'Enabled' : 'Disabled'}
                            </Typography>
                          </Box>
                        ) : (
                          <Typography variant="body2" color="warning.main">
                            ⚠️ Research preferences not configured
                          </Typography>
                        )}
                      </AccordionDetails>
                    </Accordion>
                  </Grid>

                  {/* Personalization Settings */}
                  <Grid item xs={12} md={6}>
                    <Accordion 
                      expanded={expandedSection === 'personalization'}
                      onChange={() => setExpandedSection(expandedSection === 'personalization' ? null : 'personalization')}
                      sx={{ background: 'rgba(255, 255, 255, 0.8)', borderRadius: 2 }}
                    >
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                          <Psychology sx={{ color: 'primary.main' }} />
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            Personalization
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        {onboardingData.personalizationSettings ? (
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                            <Typography variant="body2">
                              <strong>Style:</strong> {onboardingData.personalizationSettings.writing_style}
                            </Typography>
                            <Typography variant="body2">
                              <strong>Tone:</strong> {onboardingData.personalizationSettings.tone}
                            </Typography>
                            <Typography variant="body2">
                              <strong>Brand Voice:</strong> {onboardingData.personalizationSettings.brand_voice}
                            </Typography>
                          </Box>
                        ) : (
                          <Typography variant="body2" color="warning.main">
                            ⚠️ Personalization not configured
                          </Typography>
                        )}
                      </AccordionDetails>
                    </Accordion>
                  </Grid>
                </Grid>
              </Paper>
            </Zoom>

            {/* Capabilities Overview */}
            <Zoom in={true} timeout={1200}>
              <Paper elevation={0} sx={{ 
                p: 4, 
                mb: 4,
                background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
                border: '1px solid rgba(245, 158, 11, 0.2)',
                borderRadius: 3
              }}>
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Star sx={{ color: 'warning.main' }} />
                  Capabilities Overview
                </Typography>

                <Grid container spacing={2}>
                  {capabilities.map((capability) => (
                    <Grid item xs={12} sm={6} md={4} key={capability.id}>
                      <Card elevation={0} sx={{ 
                        background: capability.unlocked ? 'rgba(255, 255, 255, 0.8)' : 'rgba(0, 0, 0, 0.05)',
                        border: `1px solid ${capability.unlocked ? 'rgba(16, 185, 129, 0.3)' : 'rgba(0, 0, 0, 0.1)'}`,
                        borderRadius: 2,
                        opacity: capability.unlocked ? 1 : 0.6
                      }}>
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                            <Box sx={{
                              width: 40,
                              height: 40,
                              borderRadius: '50%',
                              background: capability.unlocked 
                                ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                                : 'linear-gradient(135deg, #6b7280 0%, #4b5563 100%)',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                            }}>
                              {React.cloneElement(capability.icon, { 
                                sx: { color: 'white', fontSize: 20 } 
                              })}
                            </Box>
                            <Box>
                              <Typography variant="subtitle1" sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                                {capability.title}
                                {capability.unlocked ? (
                                  <CheckCircle sx={{ color: 'success.main', fontSize: 16 }} />
                                ) : (
                                  <Lock sx={{ color: 'text.secondary', fontSize: 16 }} />
                                )}
                              </Typography>
                            </Box>
                          </Box>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {capability.description}
                          </Typography>
                          {!capability.unlocked && capability.required && (
                            <Box>
                              <Typography variant="caption" color="text.secondary">
                                Requires: {capability.required.join(', ')}
                              </Typography>
                            </Box>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Zoom>

            {/* Missing Requirements Warning */}
            {missingRequirements.length > 0 && (
              <Zoom in={true} timeout={1400}>
                <Alert 
                  severity="warning" 
                  sx={{ mb: 4, borderRadius: 2 }}
                  action={
                    <Button color="inherit" size="small">
                      Configure Now
                    </Button>
                  }
                >
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                    Missing Requirements
                  </Typography>
                  <Typography variant="body2">
                    The following items are recommended for optimal experience: {missingRequirements.join(', ')}
                  </Typography>
                </Alert>
              </Zoom>
            )}

            {/* Alerts */}
            <Box sx={{ mt: 3 }}>
              {error && (
                <Fade in={true}>
                  <Alert 
                    severity="error" 
                    sx={{ mb: 2, borderRadius: 2 }}
                    action={
                      <Button 
                        color="inherit" 
                        size="small"
                        onClick={() => setError(null)}
                      >
                        Dismiss
                      </Button>
                    }
                  >
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                      Setup Incomplete
                    </Typography>
                    <Typography variant="body2">
                      {error}
                    </Typography>
                  </Alert>
                </Fade>
              )}
            </Box>

            {/* Action Button */}
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <OnboardingButton
                variant="primary"
                onClick={handleLaunch}
                loading={loading}
                size="large"
                icon={<Rocket />}
                disabled={Object.keys(onboardingData.apiKeys).length === 0}
              >
                Launch Alwrity & Complete Setup
              </OnboardingButton>
            </Box>

            {/* Help Text */}
            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                This will complete your onboarding and launch Alwrity with your configured settings.
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                <Star sx={{ fontSize: 16 }} />
                Ready to create amazing content with AI-powered assistance
              </Typography>
            </Box>
          </React.Fragment>
        )}
      </Container>
    </Fade>
  );
};

export default FinalStep; 