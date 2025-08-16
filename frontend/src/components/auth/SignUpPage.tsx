import React from 'react';
import { Box, Container } from '@mui/material';
import MultiProviderSignIn from './MultiProviderSignIn';

const SignUpPage: React.FC = () => {
  const handleSuccess = () => {
    // Handle successful sign up
    console.log('Sign up successful');
  };

  const handleError = (error: string) => {
    // Handle sign up error
    console.error('Sign up error:', error);
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
          mode="signup"
          onSuccess={handleSuccess}
          onError={handleError}
        />
      </Container>
    </Box>
  );
};

export default SignUpPage;
