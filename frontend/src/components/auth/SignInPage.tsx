import React from 'react';
import { Box, Container } from '@mui/material';
import MultiProviderSignIn from './MultiProviderSignIn';

const SignInPage: React.FC = () => {
  const handleSuccess = () => {
    // Handle successful sign in
    console.log('Sign in successful');
  };

  const handleError = (error: string) => {
    // Handle sign in error
    console.error('Sign in error:', error);
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
        <MultiProviderSignIn
          mode="signin"
          onSuccess={handleSuccess}
          onError={handleError}
        />
      </Container>
    </Box>
  );
};

export default SignInPage;
