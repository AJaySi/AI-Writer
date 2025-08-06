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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { 
  Visibility, 
  VisibilityOff, 
  CheckCircle, 
  Error, 
  Info,
  Key,
  Security,
  HelpOutline,
  Warning,
  Star,
  VerifiedUser,
  Lock,
  Launch,
  Info as InfoIcon
} from '@mui/icons-material';
import { getApiKeys, saveApiKey } from '../../api/onboarding';
import { useOnboardingStyles } from './common/useOnboardingStyles';
import { 
  validateApiKey, 
  getKeyStatus, 
  isFormValid, 
  debounce,
  formatErrorMessage 
} from './common/onboardingUtils';
import OnboardingButton from './common/OnboardingButton';

interface ApiKeyStepProps {
  onContinue: () => void;
  updateHeaderContent: (content: { title: string; description: string }) => void;
}

const ApiKeyStep: React.FC<ApiKeyStepProps> = ({ onContinue, updateHeaderContent }) => {
  const [openaiKey, setOpenaiKey] = useState('');
  const [geminiKey, setGeminiKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showOpenaiKey, setShowOpenaiKey] = useState(false);
  const [showGeminiKey, setShowGeminiKey] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [savedKeys, setSavedKeys] = useState<Record<string, string>>({});
  const [benefitsModalOpen, setBenefitsModalOpen] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<any>(null);
  const [keysLoaded, setKeysLoaded] = useState(false);
  
  const styles = useOnboardingStyles();

  useEffect(() => {
    if (!keysLoaded) {
      loadExistingKeys();
    }
    // Update header content when component mounts
    updateHeaderContent({
      title: 'Connect Your AI Services',
      description: 'Alwrity uses AI to generate high-quality, personalized content for your brand. Connect at least one AI service to enable intelligent content creation, style analysis, and automated writing assistance.'
    });
  }, [updateHeaderContent, keysLoaded]);

  const loadExistingKeys = async () => {
    if (keysLoaded) return; // Prevent multiple calls
    
    try {
      console.log('ApiKeyStep: Loading API keys...');
      const keys = await getApiKeys();
      setSavedKeys(keys);
      if (keys.openai) setOpenaiKey(keys.openai);
      if (keys.gemini) setGeminiKey(keys.gemini);
      setKeysLoaded(true);
      console.log('ApiKeyStep: API keys loaded successfully');
    } catch (error) {
      console.error('ApiKeyStep: Error loading API keys:', error);
      setKeysLoaded(true); // Set to true even on error to prevent infinite retries
    }
  };

  const handleContinue = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const promises = [];
      
      if (openaiKey.trim()) {
        promises.push(saveApiKey('openai', openaiKey.trim()));
      }
      
      if (geminiKey.trim()) {
        promises.push(saveApiKey('gemini', geminiKey.trim()));
      }

      await Promise.all(promises);
      
      setSuccess('API keys saved successfully!');
      await loadExistingKeys();
      
      // Auto-continue after a short delay
      setTimeout(() => {
        onContinue();
      }, 1500);
      
    } catch (err) {
      setError(formatErrorMessage(err));
      console.error('Error saving API keys:', err);
    } finally {
      setLoading(false);
    }
  };

  const aiProviders = [
    {
      name: 'OpenAI',
      description: 'Advanced language model for content generation',
      benefits: ['High-quality text generation', 'Creative content creation', 'Natural language processing'],
      key: openaiKey,
      setKey: setOpenaiKey,
      showKey: showOpenaiKey,
      setShowKey: setShowOpenaiKey,
      placeholder: 'sk-...',
      status: getKeyStatus(openaiKey, 'openai'),
      link: 'https://platform.openai.com/api-keys',
      free: false,
      recommended: true
    },
    {
      name: 'Google Gemini',
      description: 'Google\'s latest AI model for content creation',
      benefits: ['Multimodal capabilities', 'Real-time information', 'Google\'s latest technology'],
      key: geminiKey,
      setKey: setGeminiKey,
      showKey: showGeminiKey,
      setShowKey: setShowGeminiKey,
      placeholder: 'AIza...',
      status: getKeyStatus(geminiKey, 'gemini'),
      link: 'https://makersuite.google.com/app/apikey',
      free: true,
      recommended: true
    }
  ];

  const hasAtLeastOneKey = openaiKey.trim() || geminiKey.trim();
  const isValid = hasAtLeastOneKey;

  const handleBenefitsClick = (provider: any) => {
    setSelectedProvider(provider);
    setBenefitsModalOpen(true);
  };

  const handleCloseBenefitsModal = () => {
    setBenefitsModalOpen(false);
    setSelectedProvider(null);
  };

  return (
    <Fade in={true} timeout={500}>
      <Container maxWidth="lg" sx={{ py: 2 }}>
        {/* AI Providers */}
        <Box sx={{ mb: 4 }}>
          <Grid container spacing={3}>
            {aiProviders.map((provider, index) => (
              <Grid item xs={12} md={6} key={provider.name}>
                <Zoom in={true} timeout={700 + index * 100}>
                  <Card 
                    sx={{
                      border: `1px solid ${
                        provider.status === 'valid' 
                          ? 'rgba(16, 185, 129, 0.2)'
                          : provider.status === 'invalid'
                          ? 'rgba(239, 68, 68, 0.2)'
                          : 'rgba(0,0,0,0.08)'
                      }`,
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                      '&:hover': { 
                        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.04)',
                        transform: 'translateY(-1px)',
                        borderColor: provider.status === 'valid' 
                          ? 'rgba(16, 185, 129, 0.4)'
                          : provider.status === 'invalid'
                          ? 'rgba(239, 68, 68, 0.4)'
                          : 'rgba(0,0,0,0.12)'
                      },
                      position: 'relative',
                      overflow: 'hidden',
                      background: 'rgba(255, 255, 255, 0.8)',
                      backdropFilter: 'blur(10px)',
                      '&::before': {
                        content: '""',
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        height: 2,
                        background: provider.status === 'valid' 
                          ? 'linear-gradient(90deg, rgba(16, 185, 129, 0.6) 0%, rgba(5, 150, 105, 0.6) 100%)'
                          : provider.status === 'invalid'
                          ? 'linear-gradient(90deg, rgba(239, 68, 68, 0.6) 0%, rgba(220, 38, 38, 0.6) 100%)'
                          : 'linear-gradient(90deg, rgba(107, 114, 128, 0.3) 0%, rgba(75, 85, 99, 0.3) 100%)',
                      }
                    }}
                  >
                    <CardContent sx={{ p: 3 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                          <Box sx={{
                            width: 40,
                            height: 40,
                            borderRadius: '50%',
                            background: provider.recommended 
                              ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                              : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                          }}>
                            <Key sx={{ color: 'white', fontSize: 20 }} />
                          </Box>
                          <Box>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="h6" sx={{ 
                                fontWeight: 600, 
                                mb: 0.5,
                                fontFamily: 'Inter, system-ui, sans-serif',
                                fontSize: '1.125rem'
                              }}>
                                {provider.name}
                              </Typography>
                              {provider.recommended && (
                                <Chip 
                                  label="Recommended" 
                                  color="success" 
                                  size="small"
                                  sx={{ 
                                    fontWeight: 600,
                                    fontSize: '0.75rem',
                                    height: 20
                                  }}
                                />
                              )}
                              {provider.free && (
                                <Chip 
                                  label="Free Tier" 
                                  color="primary" 
                                  size="small"
                                  sx={{ 
                                    fontWeight: 600,
                                    fontSize: '0.75rem',
                                    height: 20
                                  }}
                                />
                              )}
                            </Box>
                            <Typography variant="body2" color="text.secondary" sx={{
                              fontFamily: 'Inter, system-ui, sans-serif',
                              fontWeight: 400
                            }}>
                              {provider.description}
                            </Typography>
                          </Box>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {/* Benefits Button - Inline with Get Help */}
                          <Button
                            variant="text"
                            onClick={() => handleBenefitsClick(provider)}
                            startIcon={<InfoIcon />}
                            sx={{
                              color: 'primary.main',
                              fontWeight: 600,
                              fontSize: '0.75rem',
                              fontFamily: 'Inter, system-ui, sans-serif',
                              textTransform: 'none',
                              padding: '2px 6px',
                              borderRadius: 1,
                              minWidth: 'auto',
                              '&:hover': {
                                background: 'rgba(102, 126, 234, 0.08)',
                                transform: 'translateY(-1px)'
                              }
                            }}
                          >
                            Benefits ({provider.benefits.length})
                          </Button>
                          
                          {provider.status === 'valid' && (
                            <Chip 
                              icon={<CheckCircle />} 
                              label="Valid" 
                              color="success" 
                              size="small"
                              sx={{ 
                                fontWeight: 600,
                                fontSize: '0.75rem',
                                height: 24
                              }}
                            />
                          )}
                          {provider.status === 'invalid' && (
                            <Chip 
                              icon={<Error />} 
                              label="Invalid" 
                              color="error" 
                              size="small"
                              sx={{ 
                                fontWeight: 600,
                                fontSize: '0.75rem',
                                height: 24
                              }}
                            />
                          )}
                        </Box>
                      </Box>
                      
                      {/* Enhanced API Key Input */}
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
                              sx={{
                                color: 'text.secondary',
                                '&:hover': {
                                  color: 'primary.main',
                                  background: 'rgba(102, 126, 234, 0.08)'
                                }
                              }}
                            >
                              {provider.showKey ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          ),
                        }}
                        sx={{
                          '& .MuiOutlinedInput-root': {
                            borderRadius: 2,
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            border: '1px solid rgba(0,0,0,0.12)',
                            background: 'rgba(255, 255, 255, 0.8)',
                            '&:hover': {
                              borderColor: 'rgba(0,0,0,0.24)',
                              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
                            },
                            '&.Mui-focused': {
                              borderColor: provider.status === 'valid' 
                                ? 'rgba(16, 185, 129, 0.6)' 
                                : provider.status === 'invalid'
                                ? 'rgba(239, 68, 68, 0.6)'
                                : 'rgba(102, 126, 234, 0.6)',
                              boxShadow: `0 0 0 2px ${
                                provider.status === 'valid' 
                                  ? 'rgba(16, 185, 129, 0.1)' 
                                  : provider.status === 'invalid'
                                  ? 'rgba(239, 68, 68, 0.1)'
                                  : 'rgba(102, 126, 234, 0.1)'
                              }, 0 2px 8px rgba(0, 0, 0, 0.08)`,
                              '& .MuiOutlinedInput-notchedOutline': {
                                border: 'none'
                              }
                            },
                            '& .MuiOutlinedInput-notchedOutline': {
                              border: 'none'
                            }
                          },
                          '& .MuiInputBase-input': {
                            padding: '12px 14px',
                            fontFamily: 'Inter, system-ui, sans-serif',
                            fontWeight: 500,
                            fontSize: '0.875rem'
                          }
                        }}
                      />
                      
                      {/* Enhanced Link with Icon */}
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1.5 }}>
                        <Link 
                          href={provider.link} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          sx={{ 
                            display: 'flex', 
                            alignItems: 'center', 
                            gap: 0.75,
                            fontWeight: 600,
                            fontSize: '0.9rem',
                            color: 'primary.main',
                            textDecoration: 'none',
                            fontFamily: 'Inter, system-ui, sans-serif',
                            padding: '4px 8px',
                            borderRadius: 1,
                            transition: 'all 0.2s ease',
                            '&:hover': {
                              background: 'rgba(102, 126, 234, 0.08)',
                              textDecoration: 'none',
                              transform: 'translateY(-1px)'
                            }
                          }}
                        >
                          Get API Key
                          <Launch sx={{ fontSize: 16 }} />
                        </Link>
                      </Box>
                      
                      {savedKeys[provider.name.toLowerCase()] && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                          <CheckCircle sx={{ color: 'success.main', fontSize: 16 }} />
                          <Typography variant="caption" color="success.main" sx={{ 
                            fontWeight: 500,
                            fontFamily: 'Inter, system-ui, sans-serif'
                          }}>
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

        {/* Description moved below cards */}
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" sx={{ 
            mb: 2, 
            lineHeight: 1.6, 
            maxWidth: 800, 
            mx: 'auto',
            fontWeight: 500,
            opacity: 0.8,
            fontFamily: 'Inter, system-ui, sans-serif'
          }}>
            Alwrity uses AI to generate high-quality, personalized content for your brand. Connect at least one AI service to enable intelligent content creation, style analysis, and automated writing assistance.
          </Typography>
          
          {/* Get Help Link moved to description area */}
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
            <OnboardingButton
              variant="text"
              onClick={() => setShowHelp(!showHelp)}
              icon={<HelpOutline />}
              size="small"
            >
              {showHelp ? 'Hide Help' : 'Get Help'}
            </OnboardingButton>
          </Box>
        </Box>

        {/* Benefits Modal */}
        <Dialog
          open={benefitsModalOpen}
          onClose={handleCloseBenefitsModal}
          maxWidth="sm"
          fullWidth
          PaperProps={{
            sx: {
              borderRadius: 3,
              boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
              border: '1px solid rgba(0, 0, 0, 0.08)'
            }
          }}
        >
          <DialogTitle sx={{ 
            pb: 1,
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 600
          }}>
            {selectedProvider?.name} Benefits
          </DialogTitle>
          <DialogContent sx={{ pt: 0 }}>
            <Typography variant="body2" color="text.secondary" sx={{ 
              mb: 2,
              fontFamily: 'Inter, system-ui, sans-serif',
              fontWeight: 400
            }}>
              Discover what {selectedProvider?.name} can do for your content creation:
            </Typography>
            <List sx={{ pt: 0 }}>
              {selectedProvider?.benefits.map((benefit: string, index: number) => (
                <ListItem key={index} sx={{ px: 0, py: 1 }}>
                  <ListItemIcon sx={{ minWidth: 32 }}>
                    <Box sx={{
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      background: 'primary.main',
                      flexShrink: 0
                    }} />
                  </ListItemIcon>
                  <ListItemText 
                    primary={benefit}
                    sx={{
                      '& .MuiListItemText-primary': {
                        fontFamily: 'Inter, system-ui, sans-serif',
                        fontWeight: 500,
                        fontSize: '0.875rem'
                      }
                    }}
                  />
                </ListItem>
              ))}
            </List>
          </DialogContent>
          <DialogActions sx={{ p: 3, pt: 1 }}>
            <Button
              onClick={handleCloseBenefitsModal}
              variant="contained"
              sx={{
                borderRadius: 2,
                textTransform: 'none',
                fontWeight: 600,
                fontFamily: 'Inter, system-ui, sans-serif'
              }}
            >
              Got it
            </Button>
          </DialogActions>
        </Dialog>

        {/* Help Section */}
        <Collapse in={showHelp}>
          <Zoom in={showHelp} timeout={1600}>
            <Paper elevation={0} sx={{ 
              p: 4, 
              mb: 4,
              background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
              border: '1px solid rgba(59, 130, 246, 0.2)',
              borderRadius: 3,
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)'
            }}>
              <Typography variant="h6" gutterBottom sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1, 
                mb: 3,
                fontFamily: 'Inter, system-ui, sans-serif',
                fontWeight: 600
              }}>
                <HelpOutline color="primary" />
                How to Get Your AI API Keys
              </Typography>
              
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle1" gutterBottom sx={{ 
                      fontWeight: 600, 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 1,
                      fontFamily: 'Inter, system-ui, sans-serif'
                    }}>
                      <Star sx={{ color: 'warning.main', fontSize: 20 }} />
                      Recommended Providers
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                      <Box>
                        <Typography variant="subtitle2" sx={{ 
                          fontWeight: 600,
                          fontFamily: 'Inter, system-ui, sans-serif'
                        }}>
                          OpenAI
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom sx={{
                          fontFamily: 'Inter, system-ui, sans-serif',
                          fontWeight: 400
                        }}>
                          Visit{' '}
                          <Link href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" sx={{ 
                            fontWeight: 600,
                            color: 'primary.main',
                            textDecoration: 'none',
                            '&:hover': {
                              textDecoration: 'underline'
                            }
                          }}>
                            platform.openai.com
                          </Link>
                          , sign up, and create an API key in your account settings.
                        </Typography>
                      </Box>
                      <Box>
                        <Typography variant="subtitle2" sx={{ 
                          fontWeight: 600,
                          fontFamily: 'Inter, system-ui, sans-serif'
                        }}>
                          Google Gemini
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{
                          fontFamily: 'Inter, system-ui, sans-serif',
                          fontWeight: 400
                        }}>
                          Visit{' '}
                          <Link href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer" sx={{ 
                            fontWeight: 600,
                            color: 'primary.main',
                            textDecoration: 'none',
                            '&:hover': {
                              textDecoration: 'underline'
                            }
                          }}>
                            makersuite.google.com
                          </Link>
                          , create an account, and generate an API key.
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Box>
                    <Typography variant="subtitle1" gutterBottom sx={{ 
                      fontWeight: 600, 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: 1,
                      fontFamily: 'Inter, system-ui, sans-serif'
                    }}>
                      <Info sx={{ color: 'info.main', fontSize: 20 }} />
                      Why AI Services Matter
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                      <Typography variant="body2" color="text.secondary" sx={{
                        fontFamily: 'Inter, system-ui, sans-serif',
                        fontWeight: 400
                      }}>
                        <strong>Content Generation:</strong> Create high-quality, engaging content for your brand.
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{
                        fontFamily: 'Inter, system-ui, sans-serif',
                        fontWeight: 400
                      }}>
                        <strong>Style Analysis:</strong> Analyze your brand's voice and tone for consistency.
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{
                        fontFamily: 'Inter, system-ui, sans-serif',
                        fontWeight: 400
                      }}>
                        <strong>Automated Writing:</strong> Generate blog posts, social media content, and more.
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{
                        fontFamily: 'Inter, system-ui, sans-serif',
                        fontWeight: 400
                      }}>
                        <strong>Personalization:</strong> Tailor content to your specific audience and goals.
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
              <Alert severity="error" sx={{ 
                mb: 2, 
                borderRadius: 2,
                fontFamily: 'Inter, system-ui, sans-serif'
              }}>
                {error}
              </Alert>
            </Fade>
          )}
          
          {success && (
            <Fade in={true}>
              <Alert severity="success" sx={{ 
                mb: 2, 
                borderRadius: 2,
                fontFamily: 'Inter, system-ui, sans-serif'
              }}>
                {success}
              </Alert>
            </Fade>
          )}
        </Box>

        {/* Security Notice */}
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary" sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            gap: 0.5,
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 400
          }}>
            <Lock sx={{ fontSize: 14 }} />
            Your API keys are encrypted and stored securely on your device
          </Typography>
        </Box>
      </Container>
    </Fade>
  );
};

export default ApiKeyStep; 