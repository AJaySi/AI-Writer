import React, { useEffect, useState } from 'react';
import { 
  Box, 
  TextField, 
  Typography, 
  Alert, 
  Card,
  CardContent,
  Fade,
  Zoom,
  Chip,
  IconButton,
  Collapse,
  Divider,
  Link,
  Container,
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  OutlinedInput,
  FormHelperText,
  Switch,
  FormControlLabel,
  Button,
  CircularProgress,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { 
  Visibility, 
  VisibilityOff, 
  CheckCircle, 
  Error as ErrorIcon, 
  Info,
  Search,
  HelpOutline,
  Warning,
  Star,
  VerifiedUser,
  Lock,
  Science,
  TrendingUp,
  Security,
  AutoAwesome,
  School,
  Link as LinkIcon,
  Launch,
  Close
} from '@mui/icons-material';
import { getApiKeys, saveApiKey } from '../../api/onboarding';
import { configureResearchPreferences } from '../../api/componentLogic';
import { useOnboardingStyles } from './common/useOnboardingStyles';
import { 
  validateApiKey, 
  getKeyStatus, 
  isFormValid, 
  debounce,
  formatErrorMessage 
} from './common/onboardingUtils';
import OnboardingButton from './common/OnboardingButton';
import OnboardingCard from './common/OnboardingCard';

interface ResearchStepProps {
  onContinue: () => void;
  updateHeaderContent: (content: { title: string; description: string }) => void;
}

const ResearchStep: React.FC<ResearchStepProps> = ({ onContinue, updateHeaderContent }) => {
  console.log('ResearchStep: Component rendered');
  
  // API Keys State
  const [tavilyKey, setTavilyKey] = useState('');
  const [serperKey, setSerperKey] = useState('');
  const [exaKey, setExaKey] = useState('');
  const [firecrawlKey, setFirecrawlKey] = useState('');

  // User Information State
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('Content Creator');

  // Research Preferences State
  const [researchDepth, setResearchDepth] = useState('Comprehensive');
  const [contentTypes, setContentTypes] = useState<string[]>(['Blog Posts', 'Social Media', 'Articles']);
  const [autoResearch, setAutoResearch] = useState(true);
  const [factualContent, setFactualContent] = useState(true);

  // UI State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showTavilyKey, setShowTavilyKey] = useState(false);
  const [showSerperKey, setShowSerperKey] = useState(false);
  const [showExaKey, setShowExaKey] = useState(false);
  const [showFirecrawlKey, setShowFirecrawlKey] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [savedKeys, setSavedKeys] = useState<Record<string, string>>({});
  const [benefitsDialog, setBenefitsDialog] = useState<{ open: boolean; provider: any }>({ open: false, provider: null });
  const [keysLoaded, setKeysLoaded] = useState(false);
  const [preferencesLoaded, setPreferencesLoaded] = useState(false);
  
  const styles = useOnboardingStyles();

  useEffect(() => {
    console.log('ResearchStep: useEffect triggered', { keysLoaded });
    if (!keysLoaded) {
      console.log('ResearchStep: Calling debouncedLoadKeys');
      debouncedLoadKeys();
    } else {
      console.log('ResearchStep: Keys already loaded, skipping debouncedLoadKeys');
    }
    loadWebsiteDefaults();
  }, [keysLoaded]); // Removed updateHeaderContent from dependencies

  useEffect(() => {
    updateHeaderContent({
      title: "Configure AI Research",
      description: "Set up research APIs and preferences for intelligent content generation"
    });
  }, [updateHeaderContent]);

  useEffect(() => {
    // Prefill research preferences on mount
    const fetchPreferences = async () => {
      if (preferencesLoaded) {
        console.log('ResearchStep: Preferences already loaded, skipping API call');
        return;
      }
      
      try {
        console.log('ResearchStep: Loading research preferences...');
        const res = await import('../../api/componentLogic');
        const { getResearchPreferences } = res;
        const data = await getResearchPreferences();
        if (data && data.preferences) {
          if (data.preferences.research_depth) setResearchDepth(data.preferences.research_depth);
          if (data.preferences.content_types) setContentTypes(data.preferences.content_types);
          if (typeof data.preferences.auto_research === 'boolean') setAutoResearch(data.preferences.auto_research);
          if (typeof data.preferences.factual_content === 'boolean') setFactualContent(data.preferences.factual_content);
        }
        setPreferencesLoaded(true);
        console.log('ResearchStep: Research preferences loaded successfully');
      } catch (err) {
        console.error('ResearchStep: Error pre-filling research preferences', err);
        setPreferencesLoaded(true); // Set to true even on error to prevent infinite retries
      }
    };
    fetchPreferences();
  }, []); // Empty dependency array to run only once on mount

  const loadExistingKeys = async () => {
    if (keysLoaded) {
      console.log('ResearchStep: Keys already loaded, skipping API call');
      return; // Prevent multiple calls
    }
    
    console.log('ResearchStep: Starting to load API keys...');
    try {
      const keys = await getApiKeys();
      console.log('ResearchStep: API keys loaded successfully:', Object.keys(keys));
      setSavedKeys(keys);
      if (keys.tavily) setTavilyKey(keys.tavily);
      if (keys.serperapi) setSerperKey(keys.serperapi);
      if (keys.exa) setExaKey(keys.exa);
      if (keys.firecrawl) setFirecrawlKey(keys.firecrawl);
      setKeysLoaded(true); // Set keysLoaded to true after keys are loaded
      console.log('ResearchStep: Keys loaded and state updated');
    } catch (error: any) {
      console.error('ResearchStep: Error loading API keys:', error);
      
      // Don't show error for rate limiting - it will retry automatically
      if (error.response?.status !== 429) {
        setError(`Failed to load API keys: ${error.message || 'Unknown error'}`);
      }
      
      setKeysLoaded(true); // Set to true even on error to prevent infinite retries
      console.log('ResearchStep: Set keysLoaded to true after error');
    }
  };

  // Debounced version to prevent rapid calls
  const debouncedLoadKeys = debounce(() => {
    console.log('ResearchStep: debouncedLoadKeys called');
    loadExistingKeys();
  }, 1000);

  const loadWebsiteDefaults = async () => {
    try {
      // TODO: Load website analysis data and populate intelligent defaults
      // This would be based on the website URL from step 2
      // For now, we'll use sensible defaults
      setCompany('Your Company');
      setRole('Content Creator');
      setResearchDepth('Comprehensive');
      setContentTypes(['Blog Posts', 'Social Media', 'Articles']);
    } catch (error) {
      console.error('Error loading website defaults:', error);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const promises = [];
      
      // Save API keys
      if (tavilyKey.trim()) {
        promises.push(saveApiKey('tavily', tavilyKey.trim()));
      }
      if (serperKey.trim()) {
        promises.push(saveApiKey('serperapi', serperKey.trim()));
      }
      if (exaKey.trim()) {
        promises.push(saveApiKey('exa', exaKey.trim()));
      }
      if (firecrawlKey.trim()) {
        promises.push(saveApiKey('firecrawl', firecrawlKey.trim()));
      }

      // Save research preferences to database
      const researchPreferences = {
        research_depth: researchDepth,
        content_types: contentTypes,
        auto_research: autoResearch,
        factual_content: factualContent
      };

      const preferencesResponse = await configureResearchPreferences(researchPreferences);
      if (!preferencesResponse.valid) {
        const errorMessage = preferencesResponse.errors?.join(', ') || 'Unknown error';
        const error = `Failed to save research preferences: ${errorMessage}`;
        throw error;
      }

      await Promise.all(promises);
      
      setSuccess('Research configuration and preferences saved successfully!');
      
      // Auto-continue after a short delay
      setTimeout(() => {
        onContinue();
      }, 1500);
      
    } catch (err) {
      setError(formatErrorMessage(err));
      console.error('Error saving research configuration:', err);
    } finally {
      setLoading(false);
    }
  };

  const researchProviders = [
    {
      name: 'Tavily AI',
      description: 'Intelligent web research and content analysis',
      benefits: ['Factual content generation', 'Real-time information', 'Comprehensive research'],
      key: tavilyKey,
      setKey: setTavilyKey,
      showKey: showTavilyKey,
      setShowKey: setShowTavilyKey,
      placeholder: 'tvly-...',
      status: getKeyStatus(tavilyKey, 'tavily'),
      link: 'https://tavily.com/',
      free: true,
      recommended: true
    },
    {
      name: 'Exa',
      description: 'Advanced web search and content discovery',
      benefits: ['High-quality search results', 'Content verification', 'Source credibility'],
      key: exaKey,
      setKey: setExaKey,
      showKey: showExaKey,
      setShowKey: setShowExaKey,
      placeholder: 'exa-...',
      status: getKeyStatus(exaKey, 'exa'),
      link: 'https://exa.ai/',
      free: true,
      recommended: true
    },
    {
      name: 'Serper API',
      description: 'Google search results and web data',
      benefits: ['Google search integration', 'Real-time data', 'Comprehensive coverage'],
      key: serperKey,
      setKey: setSerperKey,
      showKey: showSerperKey,
      setShowKey: setShowSerperKey,
      placeholder: 'serper-...',
      status: getKeyStatus(serperKey, 'serperapi'),
      link: 'https://serper.dev/',
      free: true,
      recommended: false
    },
    {
      name: 'Firecrawl',
      description: 'Web content extraction and processing',
      benefits: ['Content extraction', 'Data processing', 'Structured information'],
      key: firecrawlKey,
      setKey: setFirecrawlKey,
      showKey: showFirecrawlKey,
      setShowKey: setShowFirecrawlKey,
      placeholder: 'firecrawl-...',
      status: getKeyStatus(firecrawlKey, 'firecrawl'),
      link: 'https://firecrawl.dev/',
      free: true,
      recommended: false
    }
  ];

  const hasAtLeastOneKey = tavilyKey.trim() || exaKey.trim() || serperKey.trim() || firecrawlKey.trim();
  const isValid = fullName.trim() && email.trim() && company.trim();

  return (
    <Fade in={true} timeout={500}>
      <Container maxWidth="lg" sx={{ py: 2 }}>
        
        
        {/* Importance Notice */}
        <Paper elevation={0} sx={{ 
          p: 3, 
          mb: 4, 
          textAlign: 'left',
          background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
          border: '1px solid rgba(245, 158, 11, 0.2)',
          borderRadius: 2
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 2 }}>
            <AutoAwesome sx={{ color: 'warning.main', fontSize: 24 }} />
            <Typography variant="h6" color="warning.dark" sx={{ fontWeight: 600 }}>
              Why Research APIs Matter
            </Typography>
          </Box>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <CheckCircle sx={{ color: 'success.main', fontSize: 16 }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  Factual Content
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Generate content based on real, verified information instead of AI hallucinations.
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <TrendingUp sx={{ color: 'success.main', fontSize: 16 }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  Real-time Data
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Access current information, trends, and latest developments in your industry.
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <Security sx={{ color: 'success.main', fontSize: 16 }} />
                <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                  Source Verification
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Verify facts and cite reliable sources to build trust with your audience.
              </Typography>
            </Grid>
          </Grid>
        </Paper>

        {/* Research Providers */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Search sx={{ color: 'primary.main' }} />
            Research API Providers
          </Typography>
          
          <Grid container spacing={3}>
            {researchProviders.map((provider, index) => (
              <Grid item xs={12} md={6} key={provider.name}>
                <Zoom in={true} timeout={700 + index * 100}>
                  <Card 
                    sx={{
                      background: provider.status === 'valid' 
                        ? 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)'
                        : provider.status === 'invalid'
                        ? 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)'
                        : 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
                      border: `2px solid ${
                        provider.status === 'valid' 
                          ? '#10b981'
                          : provider.status === 'invalid'
                          ? '#ef4444'
                          : 'rgba(0,0,0,0.08)'
                      }`,
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                      '&:hover': { 
                        boxShadow: provider.status === 'valid'
                          ? '0 8px 25px rgba(16, 185, 129, 0.25), 0 0 0 1px rgba(16, 185, 129, 0.1)'
                          : provider.status === 'invalid'
                          ? '0 8px 25px rgba(239, 68, 68, 0.25), 0 0 0 1px rgba(239, 68, 68, 0.1)'
                          : '0 8px 25px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0, 0, 0, 0.05)',
                        transform: 'translateY(-2px)'
                      },
                      position: 'relative',
                      overflow: 'hidden',
                      borderRadius: 3,
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: 3,
                        background: provider.status === 'valid' 
                          ? 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
                          : provider.status === 'invalid'
                          ? 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)'
                          : 'linear-gradient(90deg, #6b7280 0%, #4b5563 100%)',
                      },
                      '&::after': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: provider.status === 'valid'
                          ? 'radial-gradient(circle at top right, rgba(16, 185, 129, 0.1) 0%, transparent 70%)'
                          : provider.status === 'invalid'
                          ? 'radial-gradient(circle at top right, rgba(239, 68, 68, 0.1) 0%, transparent 70%)'
                          : 'radial-gradient(circle at top right, rgba(107, 114, 128, 0.1) 0%, transparent 70%)',
                        pointerEvents: 'none'
                      }
                    }}
                  >
                    <CardContent sx={{ p: 2.5, position: 'relative', zIndex: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1.5 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                          <Box sx={{
                            width: 36,
                            height: 36,
                            borderRadius: '50%',
                            background: provider.recommended 
                              ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
                          }}>
                            <Search sx={{ color: 'white', fontSize: 18 }} />
                          </Box>
                          <Box>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.25 }}>
                              <Typography variant="h6" sx={{ fontWeight: 600, mb: 0 }}>
                                {provider.name}
                              </Typography>
                              {provider.recommended && (
                                <Chip 
                                  label="Recommended" 
                                  color="success" 
                                  size="small"
                                  sx={{ fontWeight: 600, height: 20 }}
                                />
                              )}
                              {provider.free && (
                                <Chip 
                                  label="Free Tier" 
                                  color="primary" 
                                  size="small"
                                  sx={{ fontWeight: 600, height: 20 }}
                                />
                              )}
                            </Box>
                            <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.875rem' }}>
                              {provider.description}
                            </Typography>
                          </Box>
                        </Box>
                        {provider.status === 'valid' && (
                          <Chip 
                            icon={<CheckCircle />} 
                            label="Valid" 
                            color="success" 
                            size="small"
                            sx={{ fontWeight: 600, height: 24 }}
                          />
                        )}
                        {provider.status === 'invalid' && (
                          <Chip 
                            icon={<ErrorIcon />} 
                            label="Invalid" 
                            color="error" 
                            size="small"
                            sx={{ fontWeight: 600, height: 24 }}
                          />
                        )}
                      </Box>
                      
                      <Box sx={{ mb: 1.5 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.5 }}>
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Benefits:
                          </Typography>
                          <Tooltip title="View all benefits">
                            <IconButton
                              size="small"
                              onClick={() => setBenefitsDialog({ open: true, provider })}
                              sx={{ 
                                color: 'primary.main',
                                '&:hover': {
                                  background: 'rgba(59, 130, 246, 0.1)'
                                }
                              }}
                            >
                              <HelpOutline sx={{ fontSize: 16 }} />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </Box>
                      
                      <TextField
                        fullWidth
                        type={provider.showKey ? 'text' : 'password'}
                        value={provider.key}
                        onChange={(e) => provider.setKey(e.target.value)}
                        placeholder={provider.placeholder}
                        variant="outlined"
                        size="small"
                        InputProps={{
                          startAdornment: (
                            <Lock sx={{ color: 'text.secondary', mr: 1, fontSize: 16 }} />
                          ),
                          endAdornment: (
                            <IconButton
                              onClick={() => provider.setShowKey(!provider.showKey)}
                              edge="end"
                              size="small"
                            >
                              {provider.showKey ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          ),
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            background: 'rgba(255, 255, 255, 0.9)',
                            backdropFilter: 'blur(10px)',
                            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.8)',
                            border: '1px solid rgba(0, 0, 0, 0.08)',
                            transition: 'all 0.2s ease-in-out',
                            '&:hover': {
                              background: 'rgba(255, 255, 255, 0.95)',
                              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.9)',
                              border: '1px solid rgba(0, 0, 0, 0.12)'
                            },
                            '&.Mui-focused': {
                              background: 'rgba(255, 255, 255, 0.98)',
                              boxShadow: '0 0 0 3px rgba(59, 130, 246, 0.1), 0 4px 12px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.95)',
                              border: '1px solid rgba(59, 130, 246, 0.3)'
                            }
                          }
                        }}
                      />
                      
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                        <LinkIcon sx={{ color: 'text.secondary', fontSize: 14 }} />
                        <Link 
                          href={provider.link} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          sx={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: 0.5,
                            fontWeight: 600,
                            fontSize: '0.875rem'
                          }}
                        >
                          Get API Key
                          <Launch sx={{ fontSize: 14 }} />
                        </Link>
                      </Box>
                      
                      {savedKeys[provider.name.toLowerCase()] && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                          <CheckCircle sx={{ color: 'success.main', fontSize: 16 }} />
                          <Typography variant="caption" color="success.main" sx={{ fontWeight: 500 }}>
                            Key already saved and secured
                          </Typography>
                        </Box>
                      )}
                    </CardContent>
                  </Card>
                </Zoom>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Research Preferences */}
        <Zoom in={true} timeout={1400}>
          <Paper elevation={0} sx={{ 
            p: 4, 
            mb: 4,
            background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)',
            border: '1px solid rgba(16, 185, 129, 0.2)',
            borderRadius: 3
          }}>
            <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
              <School sx={{ color: 'success.main' }} />
              Research Preferences
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Research Depth</InputLabel>
                  <Select
                    value={researchDepth}
                    onChange={(e) => setResearchDepth(e.target.value)}
                    label="Research Depth"
                    size="medium"
                  >
                    <MenuItem value="Basic">Basic - Quick overview</MenuItem>
                    <MenuItem value="Standard">Standard - Balanced depth</MenuItem>
                    <MenuItem value="Comprehensive">Comprehensive - Detailed analysis</MenuItem>
                    <MenuItem value="Expert">Expert - In-depth research</MenuItem>
                  </Select>
                  <FormHelperText>Choose how detailed you want the AI research to be</FormHelperText>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Content Types</InputLabel>
                  <Select
                    multiple
                    value={contentTypes}
                    onChange={(e) => setContentTypes(typeof e.target.value === 'string' ? e.target.value.split(',') : e.target.value)}
                    input={<OutlinedInput label="Content Types" />}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.map((value) => (
                          <Chip key={value} label={value} size="small" />
                        ))}
                      </Box>
                    )}
                    size="medium"
                  >
                    <MenuItem value="Blog Posts">Blog Posts</MenuItem>
                    <MenuItem value="Social Media">Social Media</MenuItem>
                    <MenuItem value="Articles">Articles</MenuItem>
                    <MenuItem value="Email Newsletters">Email Newsletters</MenuItem>
                    <MenuItem value="Product Descriptions">Product Descriptions</MenuItem>
                    <MenuItem value="Landing Pages">Landing Pages</MenuItem>
                  </Select>
                  <FormHelperText>Choose what types of content you want to research</FormHelperText>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={autoResearch}
                        onChange={(e) => setAutoResearch(e.target.checked)}
                        color="primary"
                      />
                    }
                    label="Enable Automated Research"
                  />
                  <Typography variant="body2" color="text.secondary" sx={{ ml: 4 }}>
                    Automatically start research when content topics are added
                  </Typography>
                  
                  <FormControlLabel
                    control={
                      <Switch
                        checked={factualContent}
                        onChange={(e) => setFactualContent(e.target.checked)}
                        color="primary"
                      />
                    }
                    label="Prioritize Factual Content"
                  />
                  <Typography variant="body2" color="text.secondary" sx={{ ml: 4 }}>
                    Focus on generating content based on verified facts and sources
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Zoom>

        {/* Help Section */}
        <Collapse in={showHelp}>
          <Zoom in={showHelp} timeout={1600}>
            <Paper elevation={0} sx={{ 
              p: 4, 
              mb: 4,
              background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
              border: '1px solid rgba(59, 130, 246, 0.2)',
              borderRadius: 3
            }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <HelpOutline color="primary" />
                How to Get Your Research API Keys
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Star sx={{ color: 'warning.main', fontSize: 20 }} />
                      Recommended Providers
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          Tavily AI
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Visit{' '}
                          <Link href="https://tavily.com/" target="_blank" rel="noopener noreferrer" sx={{ fontWeight: 600 }}>
                            tavily.com
                          </Link>
                          , sign up for free, and get your API key from the dashboard.
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                          Exa
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Visit{' '}
                          <Link href="https://exa.ai/" target="_blank" rel="noopener noreferrer" sx={{ fontWeight: 600 }}>
                            exa.ai
                          </Link>
                          , create an account, and access your API key in the settings.
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Box>
                    <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Info sx={{ color: 'info.main', fontSize: 20 }} />
                      Why These APIs Matter
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Factual Content:</strong> Generate content based on real, verified information instead of AI hallucinations.
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Real-time Data:</strong> Access current information, trends, and latest developments in your industry.
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Source Verification:</strong> Verify facts and cite reliable sources to build trust with your audience.
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Free Tiers:</strong> Most providers offer generous free tiers to get you started.
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Zoom>
        </Collapse>

        {/* Alerts */}
        <Box sx={{ mt: 3 }}>
          {error && (
            <Fade in={true}>
              <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
                {error}
              </Alert>
            </Fade>
          )}
          
          {success && (
            <Fade in={true}>
              <Alert severity="success" sx={{ mb: 2, borderRadius: 2 }}>
                {success}
              </Alert>
            </Fade>
          )}
        </Box>

        {/* Action Buttons */}
        <Box sx={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center', mt: 4 }}>
          <OnboardingButton
            variant="text"
            onClick={() => setShowHelp(!showHelp)}
            icon={<HelpOutline />}
          >
            {showHelp ? 'Hide Help' : 'Get Help'}
          </OnboardingButton>
        </Box>

        {/* Security Notice */}
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
            <Lock sx={{ fontSize: 14 }} />
            Your API keys are encrypted and stored securely on your device
          </Typography>
        </Box>

        {/* Benefits Dialog */}
        <Dialog
          open={benefitsDialog.open}
          onClose={() => setBenefitsDialog({ open: false, provider: null })}
          maxWidth="sm"
          fullWidth
          PaperProps={{
            sx: {
              borderRadius: 3,
              background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
              boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)'
            }
          }}
        >
          <DialogTitle sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-between',
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            color: 'white',
            borderRadius: '12px 12px 0 0'
          }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
              <Search sx={{ fontSize: 24 }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                {benefitsDialog.provider?.name} Benefits
              </Typography>
            </Box>
            <IconButton
              onClick={() => setBenefitsDialog({ open: false, provider: null })}
              sx={{ color: 'white' }}
            >
              <Close />
            </IconButton>
          </DialogTitle>
          <DialogContent sx={{ p: 3 }}>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              {benefitsDialog.provider?.description}
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {benefitsDialog.provider?.benefits.map((benefit: string, index: number) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Box sx={{
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    <CheckCircle sx={{ color: 'white', fontSize: 18 }} />
                  </Box>
                  <Typography variant="body1" sx={{ fontWeight: 500 }}>
                    {benefit}
                  </Typography>
                </Box>
              ))}
            </Box>
          </DialogContent>
          <DialogActions sx={{ p: 3, pt: 0 }}>
            <Button
              variant="outlined"
              onClick={() => setBenefitsDialog({ open: false, provider: null })}
              sx={{ borderRadius: 2 }}
            >
              Close
            </Button>
            <Button
              variant="contained"
              onClick={() => {
                if (benefitsDialog.provider?.link) {
                  window.open(benefitsDialog.provider.link, '_blank');
                }
              }}
              sx={{ 
                borderRadius: 2,
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #059669 0%, #047857 100%)'
                }
              }}
            >
              Get API Key
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </Fade>
  );
};

export default ResearchStep; 