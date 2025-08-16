import React from 'react';
import { Box, CircularProgress, Typography, Button, Alert } from '@mui/material';
import { useAuthState } from '../../hooks/useAuthState';
import { useNavigate } from 'react-router-dom';

interface EnhancedAuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  requireAuth?: boolean;
  redirectTo?: string;
}

const EnhancedAuthGuard: React.FC<EnhancedAuthGuardProps> = ({
  children,
  fallback,
  requireAuth = true,
  redirectTo = '/auth/signin'
}) => {
  const { isLoaded, isSignedIn, isLoading, error } = useAuthState();
  const navigate = useNavigate();

  // Show loading state while Clerk is initializing
  if (!isLoaded || isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
      >
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Loading authentication...
        </Typography>
      </Box>
    );
  }

  // Show error state if there's an authentication error
  if (error) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
        p={3}
      >
        <Alert severity="error" sx={{ mb: 3, maxWidth: 400 }}>
          <Typography variant="h6" sx={{ mb: 1 }}>
            Authentication Error
          </Typography>
          <Typography variant="body2" sx={{ mb: 2 }}>
            {error}
          </Typography>
          <Button
            variant="contained"
            onClick={() => window.location.reload()}
            sx={{ mr: 1 }}
          >
            Retry
          </Button>
          <Button
            variant="outlined"
            onClick={() => navigate(redirectTo)}
          >
            Sign In
          </Button>
        </Alert>
      </Box>
    );
  }

  // If authentication is required but user is not signed in
  if (requireAuth && !isSignedIn) {
    if (fallback) {
      return <>{fallback}</>;
    }

    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
        p={3}
      >
        <Box
          sx={{
            textAlign: 'center',
            maxWidth: 400,
            p: 4,
            borderRadius: 2,
            bgcolor: 'background.paper',
            boxShadow: 3
          }}
        >
          <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
            Authentication Required
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: 'text.secondary' }}>
            Please sign in to access this page.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate(redirectTo)}
            sx={{ mr: 2 }}
          >
            Sign In
          </Button>
          <Button
            variant="outlined"
            size="large"
            onClick={() => navigate('/')}
          >
            Go Home
          </Button>
        </Box>
      </Box>
    );
  }

  // If user is signed in but we don't require auth (e.g., for public pages)
  if (!requireAuth && isSignedIn) {
    // Optionally redirect signed-in users away from auth pages
    if (redirectTo === '/auth/signin' || redirectTo === '/auth/signup') {
      navigate('/dashboard');
      return null;
    }
  }

  // Render children if all conditions are met
  return <>{children}</>;
};

export default EnhancedAuthGuard;
