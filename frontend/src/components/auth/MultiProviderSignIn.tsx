import React, { useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Paper,
  Divider,
  TextField,
  Alert,
  CircularProgress,
  useTheme
} from '@mui/material';
import {
  Google,
  GitHub,
  Facebook,
  Email,
  Visibility,
  VisibilityOff
} from '@mui/icons-material';
import { useSignIn, useSignUp } from '@clerk/clerk-react';
import { useNavigate } from 'react-router-dom';

interface MultiProviderSignInProps {
  mode?: 'signin' | 'signup';
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

const MultiProviderSignIn: React.FC<MultiProviderSignInProps> = ({
  mode = 'signin',
  onSuccess,
  onError
}) => {
  const theme = useTheme();
  const navigate = useNavigate();
  
  const { signIn, isLoaded: signInLoaded } = useSignIn();
  const { signUp, isLoaded: signUpLoaded } = useSignUp();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isEmailMode, setIsEmailMode] = useState(false);

  const isLoaded = mode === 'signin' ? signInLoaded : signUpLoaded;
  const authAction = mode === 'signin' ? signIn : signUp;

  const handleOAuthSignIn = async (strategy: 'oauth_google' | 'oauth_github' | 'oauth_facebook') => {
    if (!isLoaded || !authAction) return;

    try {
      setLoading(true);
      setError('');
      
      await authAction.authenticateWithRedirect({
        strategy,
        redirectUrl: '/dashboard',
        redirectUrlComplete: '/dashboard'
      });
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
      onError?.(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleEmailSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isLoaded || !authAction) return;

    try {
      setLoading(true);
      setError('');

      if (mode === 'signin') {
        const result = await signIn?.create({
          identifier: email,
          password
        });

        if (result?.status === 'complete') {
          onSuccess?.();
          navigate('/dashboard');
        }
      } else {
        const result = await signUp?.create({
          emailAddress: email,
          password
        });

        if (result?.status === 'complete') {
          onSuccess?.();
          navigate('/dashboard');
        } else if (result?.status === 'missing_requirements') {
          // Handle email verification
          navigate('/verify-email');
        }
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
      onError?.(err.message);
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  if (!isLoaded) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper
      elevation={3}
      sx={{
        p: { xs: 3, md: 4 },
        borderRadius: 3,
        maxWidth: 400,
        width: '100%',
        mx: 'auto',
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)'
      }}
    >
      <Box sx={{ textAlign: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 700, mb: 1 }}>
          {mode === 'signin' ? 'Welcome Back' : 'Create Account'}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {mode === 'signin' 
            ? 'Sign in to continue to Alwrity' 
            : 'Join Alwrity to start creating amazing content'
          }
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {!isEmailMode ? (
        // OAuth Providers
        <Box>
          <Button
            fullWidth
            variant="contained"
            size="large"
            onClick={() => handleOAuthSignIn('oauth_google')}
            disabled={loading}
            startIcon={<Google />}
            sx={{
              mb: 2,
              bgcolor: '#4285f4',
              color: 'white',
              '&:hover': { bgcolor: '#357abd' },
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600
            }}
          >
            Continue with Google
          </Button>

          <Button
            fullWidth
            variant="contained"
            size="large"
            onClick={() => handleOAuthSignIn('oauth_github')}
            disabled={loading}
            startIcon={<GitHub />}
            sx={{
              mb: 2,
              bgcolor: '#24292e',
              color: 'white',
              '&:hover': { bgcolor: '#1a1e22' },
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600
            }}
          >
            Continue with GitHub
          </Button>

          <Button
            fullWidth
            variant="contained"
            size="large"
            onClick={() => handleOAuthSignIn('oauth_facebook')}
            disabled={loading}
            startIcon={<Facebook />}
            sx={{
              mb: 2,
              bgcolor: '#1877f2',
              color: 'white',
              '&:hover': { bgcolor: '#166fe5' },
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600
            }}
          >
            Continue with Facebook
          </Button>

          <Divider sx={{ my: 3 }}>
            <Typography variant="body2" color="text.secondary">
              or
            </Typography>
          </Divider>

          <Button
            fullWidth
            variant="outlined"
            size="large"
            onClick={() => setIsEmailMode(true)}
            startIcon={<Email />}
            sx={{
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600
            }}
          >
            Continue with Email
          </Button>
        </Box>
      ) : (
        // Email/Password Form
        <Box component="form" onSubmit={handleEmailSignIn}>
          <TextField
            fullWidth
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            sx={{ mb: 2 }}
            disabled={loading}
          />

          <TextField
            fullWidth
            label="Password"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            sx={{ mb: 3 }}
            disabled={loading}
            InputProps={{
              endAdornment: (
                <Button
                  onClick={togglePasswordVisibility}
                  sx={{ minWidth: 'auto', p: 1 }}
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </Button>
              )
            }}
          />

          <Button
            fullWidth
            type="submit"
            variant="contained"
            size="large"
            disabled={loading}
            sx={{
              mb: 2,
              py: 1.5,
              fontSize: '1rem',
              fontWeight: 600
            }}
          >
            {loading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              mode === 'signin' ? 'Sign In' : 'Create Account'
            )}
          </Button>

          <Button
            fullWidth
            variant="text"
            onClick={() => setIsEmailMode(false)}
            disabled={loading}
            sx={{ mb: 1 }}
          >
            Back to other options
          </Button>
        </Box>
      )}

      <Divider sx={{ my: 3 }} />

      <Box sx={{ textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          {mode === 'signin' ? "Don't have an account? " : "Already have an account? "}
          <Button
            variant="text"
            onClick={() => navigate(mode === 'signin' ? '/auth/signup' : '/auth/signin')}
            sx={{ p: 0, minWidth: 'auto', textTransform: 'none' }}
          >
            {mode === 'signin' ? 'Sign up' : 'Sign in'}
          </Button>
        </Typography>
      </Box>
    </Paper>
  );
};

export default MultiProviderSignIn;
