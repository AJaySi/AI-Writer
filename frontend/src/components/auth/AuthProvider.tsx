import React from 'react';
import { ClerkProvider, useAuth, useUser } from '@clerk/clerk-react';
import { Box, CircularProgress, Typography } from '@mui/material';

// Get Clerk publishable key from Vite environment variables with fallback
const CLERK_PUBLISHABLE_KEY = (import.meta.env && import.meta.env.VITE_CLERK_PUBLISHABLE_KEY) || 'pk_test_bGl2aW5nLWhhbXN0ZXItNTkuY2xlcmsuYWNjb3VudHMuZGV2JA';

console.log('Clerk Key:', CLERK_PUBLISHABLE_KEY ? 'Found' : 'Missing');

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  return (
    <ClerkProvider publishableKey={CLERK_PUBLISHABLE_KEY}>
      {children}
    </ClerkProvider>
  );
};

export const useAuthContext = () => {
  const { isLoaded, isSignedIn, user } = useUser();
  const { signOut } = useAuth();

  return {
    isLoaded,
    isSignedIn,
    user,
    signOut
  };
};

export const AuthGuard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isLoaded, isSignedIn } = useAuthContext();

  if (!isLoaded) {
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

  if (!isSignedIn) {
    return <div>Please sign in to access this page.</div>;
  }

  return <>{children}</>;
};
