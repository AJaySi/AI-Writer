import React from 'react';
import { SignIn } from '@clerk/clerk-react';
import { Box, Container, Typography, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const SignInPage: React.FC = () => {
  const navigate = useNavigate();

  const handleSignInComplete = () => {
    // Redirect to dashboard after successful sign in
    navigate('/dashboard');
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 4
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={8}
          sx={{
            p: 4,
            borderRadius: 3,
            textAlign: 'center'
          }}
        >
          <Typography
            variant="h4"
            component="h1"
            sx={{
              fontWeight: 700,
              mb: 1,
              color: 'primary.main'
            }}
          >
            Welcome Back
          </Typography>
          <Typography
            variant="body1"
            color="text.secondary"
            sx={{ mb: 4 }}
          >
            Sign in to your Alwrity account to continue creating amazing content.
          </Typography>
          
          <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <SignIn
              appearance={{
                elements: {
                  rootBox: {
                    width: '100%',
                    maxWidth: '400px'
                  },
                  card: {
                    boxShadow: 'none',
                    border: 'none'
                  },
                  headerTitle: {
                    display: 'none'
                  },
                  headerSubtitle: {
                    display: 'none'
                  },
                                     socialButtonsBlockButton: {
                     borderRadius: '8px',
                     textTransform: 'none',
                     fontWeight: 600
                   },
                   socialButtonsBlockButtonFacebook: {
                     backgroundColor: '#1877f2',
                     '&:hover': {
                       backgroundColor: '#166fe5'
                     }
                   },
                  formButtonPrimary: {
                    borderRadius: '8px',
                    textTransform: 'none',
                    fontWeight: 600,
                    backgroundColor: '#667eea',
                    '&:hover': {
                      backgroundColor: '#5a6fd8'
                    }
                  },
                  formFieldInput: {
                    borderRadius: '8px'
                  },
                  footerActionLink: {
                    color: '#667eea',
                    textDecoration: 'none',
                    '&:hover': {
                      textDecoration: 'underline'
                    }
                  }
                }
              }}
              redirectUrl="/dashboard"
              afterSignInUrl="/dashboard"
            />
          </Box>
          
          <Box sx={{ mt: 3, pt: 3, borderTop: '1px solid', borderColor: 'divider' }}>
            <Typography variant="body2" color="text.secondary">
              Don't have an account?{' '}
              <Typography
                component="span"
                variant="body2"
                sx={{
                  color: 'primary.main',
                  cursor: 'pointer',
                  textDecoration: 'underline',
                  '&:hover': {
                    color: 'primary.dark'
                  }
                }}
                onClick={() => navigate('/auth/signup')}
              >
                Sign up here
              </Typography>
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default SignInPage;
