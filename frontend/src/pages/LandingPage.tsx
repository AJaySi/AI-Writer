import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Stack,
  Grid,
  useTheme
} from '@mui/material';
import {
  Facebook,
  Google,
  GitHub
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useSignIn } from '@clerk/clerk-react';

const LandingPage: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { signIn, isLoaded } = useSignIn();

  const handleOAuthSignIn = async (strategy: 'oauth_google' | 'oauth_github' | 'oauth_facebook') => {
    if (!isLoaded || !signIn) {
      navigate('/auth/signin');
      return;
    }

    try {
      await signIn.authenticateWithRedirect({
        strategy,
        redirectUrl: '/dashboard',
        redirectUrlComplete: '/dashboard'
      });
    } catch (error) {
      console.error('Authentication error:', error);
      navigate('/auth/signin');
    }
  };

  const handleFacebookLogin = () => {
    handleOAuthSignIn('oauth_facebook');
  };

  const handleGoogleLogin = () => {
    handleOAuthSignIn('oauth_google');
  };

  const handleGitHubLogin = () => {
    handleOAuthSignIn('oauth_github');
  };

  const handleEmailSignIn = () => {
    navigate('/auth/signin');
  };

  return (
    <Box sx={{ minHeight: '100vh' }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: { xs: 8, md: 12 },
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center', maxWidth: 800, mx: 'auto' }}>
            <Typography
              variant="h2"
              component="h1"
              sx={{
                fontWeight: 700,
                mb: 3,
                fontSize: { xs: '2.5rem', md: '3.5rem' }
              }}
            >
              Alwrity
            </Typography>
            <Typography
              variant="h5"
              sx={{
                mb: 4,
                opacity: 0.9,
                lineHeight: 1.6
              }}
            >
              AI-powered content creation and SEO optimization, designed for modern creators and businesses
            </Typography>
            
            {/* Security Badge */}
            <Box
              sx={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 1,
                px: 2,
                py: 1,
                borderRadius: 2,
                border: '1px solid rgba(255, 255, 255, 0.2)',
                background: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
                mb: 6
              }}
            >
              <Box
                component="span"
                sx={{
                  width: 16,
                  height: 16,
                  borderRadius: '50%',
                  background: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '12px',
                  fontWeight: 'bold'
                }}
              >
                🛡️
              </Box>
              <Typography variant="body2" sx={{ color: 'white', fontWeight: 500 }}>
                Enterprise-Grade Security
              </Typography>
            </Box>
            
            {/* Login Buttons - 2x2 Grid Layout */}
            <Grid container spacing={2} sx={{ 
              justifyContent: 'center',
              mb: 4,
              maxWidth: 600,
              mx: 'auto'
            }}>
              {/* Row 1: Google and GitHub */}
              <Grid item xs={12} sm={6}>
                <Button
                  fullWidth
                  variant="contained"
                  size="large"
                  onClick={handleGoogleLogin}
                  startIcon={<Google />}
                  sx={{
                    bgcolor: '#4285f4',
                    color: 'white',
                    '&:hover': {
                      bgcolor: '#357abd'
                    },
                    px: 4,
                    py: 1.5,
                    fontSize: '1rem',
                    fontWeight: 600,
                    borderRadius: 2
                  }}
                >
                  Continue with Google
                </Button>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Button
                  fullWidth
                  variant="contained"
                  size="large"
                  onClick={handleGitHubLogin}
                  startIcon={<GitHub />}
                  sx={{
                    bgcolor: '#24292e',
                    color: 'white',
                    '&:hover': {
                      bgcolor: '#1a1e22'
                    },
                    px: 4,
                    py: 1.5,
                    fontSize: '1rem',
                    fontWeight: 600,
                    borderRadius: 2
                  }}
                >
                  Continue with GitHub
                </Button>
              </Grid>
              
              {/* Row 2: Facebook and Email */}
              <Grid item xs={12} sm={6}>
                <Button
                  fullWidth
                  variant="contained"
                  size="large"
                  onClick={handleFacebookLogin}
                  startIcon={<Facebook />}
                  sx={{
                    bgcolor: '#1877f2',
                    color: 'white',
                    '&:hover': {
                      bgcolor: '#166fe5'
                    },
                    px: 4,
                    py: 1.5,
                    fontSize: '1rem',
                    fontWeight: 600,
                    borderRadius: 2
                  }}
                >
                  Continue with Facebook
                </Button>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Button
                  fullWidth
                  variant="outlined"
                  size="large"
                  onClick={handleEmailSignIn}
                  sx={{
                    borderColor: 'white',
                    color: 'white',
                    '&:hover': {
                      borderColor: 'white',
                      bgcolor: 'rgba(255, 255, 255, 0.1)'
                    },
                    px: 4,
                    py: 1.5,
                    fontSize: '1rem',
                    fontWeight: 600,
                    borderRadius: 2
                  }}
                >
                  Continue with Email
                </Button>
              </Grid>
            </Grid>
            
            {/* Legal Text */}
            <Typography
              variant="body2"
              sx={{
                color: 'white',
                opacity: 0.8,
                textAlign: 'center'
              }}
            >
              By continuing you agree to our{' '}
              <Box component="span" sx={{ textDecoration: 'underline', cursor: 'pointer' }}>
                Terms of Service
              </Box>
              {' '}and{' '}
              <Box component="span" sx={{ textDecoration: 'underline', cursor: 'pointer' }}>
                Privacy Policy
              </Box>
            </Typography>

            {/* Feature Cards */}
            <Grid container spacing={3} sx={{ mb: 6, justifyContent: 'center', mt: 8 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    borderRadius: 3,
                    background: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    textAlign: 'center',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center'
                  }}
                >
                  <Box sx={{ fontSize: '2rem', mb: 2 }}>✨</Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, color: 'white' }}>
                    AI-Powered
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'white', opacity: 0.9 }}>
                    Advanced AI for content creation
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    borderRadius: 3,
                    background: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    textAlign: 'center',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center'
                  }}
                >
                  <Box sx={{ fontSize: '2rem', mb: 2 }}>📈</Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, color: 'white' }}>
                    SEO Optimized
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'white', opacity: 0.9 }}>
                    Built-in SEO analysis & optimization
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    borderRadius: 3,
                    background: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    textAlign: 'center',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center'
                  }}
                >
                  <Box sx={{ fontSize: '2rem', mb: 2 }}>💡</Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, color: 'white' }}>
                    Smart Research
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'white', opacity: 0.9 }}>
                    Automated content research & insights
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Paper
                  elevation={0}
                  sx={{
                    p: 3,
                    borderRadius: 3,
                    background: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    textAlign: 'center',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center'
                  }}
                >
                  <Box sx={{ fontSize: '2rem', mb: 2 }}>⚡</Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, color: 'white' }}>
                    Lightning Fast
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'white', opacity: 0.9 }}>
                    Generate content in seconds
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        </Container>
      </Box>

      {/* Footer */}
      <Box sx={{ bgcolor: 'grey.900', color: 'white', py: 4 }}>
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 700 }}>
              Alwrity
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8, mb: 2 }}>
              AI-powered content creation platform
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.6 }}>
              © 2024 Alwrity. All rights reserved.
            </Typography>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default LandingPage;
