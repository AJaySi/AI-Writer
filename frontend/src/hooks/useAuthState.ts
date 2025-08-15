import { useState, useEffect } from 'react';
import { useUser, useAuth } from '@clerk/clerk-react';

export interface AuthState {
  isLoaded: boolean;
  isSignedIn: boolean;
  user: any;
  provider: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface AuthActions {
  signOut: () => Promise<void>;
  refreshUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthState = (): AuthState & AuthActions => {
  const { isLoaded, isSignedIn, user } = useUser();
  const { signOut: clerkSignOut } = useAuth();
  
  const [provider, setProvider] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Determine authentication provider
  useEffect(() => {
    if (user && isSignedIn) {
      const externalAccounts = user.externalAccounts || [];
      if (externalAccounts.length > 0) {
        const primaryAccount = externalAccounts[0];
        setProvider(primaryAccount.provider);
      } else {
        setProvider('email');
      }
    } else {
      setProvider(null);
    }
  }, [user, isSignedIn]);

  const signOut = async (): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      await clerkSignOut();
      setProvider(null);
    } catch (err: any) {
      setError(err.message || 'Failed to sign out');
    } finally {
      setIsLoading(false);
    }
  };

  const refreshUser = async (): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      await user?.reload();
    } catch (err: any) {
      setError(err.message || 'Failed to refresh user data');
    } finally {
      setIsLoading(false);
    }
  };

  const clearError = (): void => {
    setError(null);
  };

  return {
    isLoaded: isLoaded || false,
    isSignedIn: isSignedIn || false,
    user,
    provider,
    isLoading,
    error,
    signOut,
    refreshUser,
    clearError
  };
};

// Hook for checking if specific providers are enabled
export const useProviderAvailability = () => {
  const [providers, setProviders] = useState({
    google: false,
    github: false,
    facebook: false,
    email: false
  });

  useEffect(() => {
    // Check environment variables for provider availability
    const checkProviders = () => {
      setProviders({
        google: (import.meta.env?.VITE_ENABLE_GOOGLE_AUTH || 'false') === 'true',
        github: (import.meta.env?.VITE_ENABLE_GITHUB_AUTH || 'false') === 'true',
        facebook: (import.meta.env?.VITE_ENABLE_FACEBOOK_AUTH || 'false') === 'true',
        email: (import.meta.env?.VITE_ENABLE_EMAIL_AUTH || 'false') === 'true'
      });
    };

    checkProviders();
  }, []);

  return providers;
};

// Hook for authentication analytics
export const useAuthAnalytics = () => {
  const { provider, isSignedIn } = useAuthState();

  useEffect(() => {
    if (isSignedIn && provider) {
      // Track authentication events
      console.log(`User signed in with ${provider}`);
      
      // You can integrate with analytics services here
      // Example: analytics.track('user_signed_in', { provider });
    }
  }, [isSignedIn, provider]);

  const trackAuthEvent = (event: string, data?: any) => {
    console.log(`Auth event: ${event}`, data);
    // Integrate with your analytics service
  };

  return { trackAuthEvent };
};
