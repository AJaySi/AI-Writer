import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress, Typography } from '@mui/material';
import Wizard from './components/OnboardingWizard/Wizard';
import MainDashboard from './components/MainDashboard/MainDashboard';
import SEODashboard from './components/SEODashboard/SEODashboard';
import ContentPlanningDashboard from './components/ContentPlanningDashboard/ContentPlanningDashboard';
import MemoryChatPage from './components/MemoryChat/MemoryChatPage';
import { apiClient } from './api/client';

interface OnboardingStatus {
  onboarding_required: boolean;
  onboarding_complete: boolean;
  current_step?: number;
  total_steps?: number;
  completion_percentage?: number;
}

const App: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [onboardingStatus, setOnboardingStatus] = useState<OnboardingStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkOnboardingStatus();
  }, []);

  const checkOnboardingStatus = async () => {
    try {
      setLoading(true);
      // Use the correct endpoint that exists in our backend
      const response = await apiClient.get('/api/onboarding/status');
      const status: any = response.data;
      
      // Transform the backend response to match frontend expectations
      const transformedStatus: OnboardingStatus = {
        onboarding_required: !status.is_completed,
        onboarding_complete: status.is_completed || false,
        current_step: status.current_step,
        total_steps: 6, // We know there are 6 steps
        completion_percentage: status.completion_percentage
      };
      
      setOnboardingStatus(transformedStatus);
    } catch (err) {
      console.error('Error checking onboarding status:', err);
      // If the endpoint doesn't exist, assume onboarding is required
      setOnboardingStatus({
        onboarding_required: true,
        onboarding_complete: false,
        current_step: 1,
        total_steps: 6,
        completion_percentage: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const handleOnboardingComplete = async () => {
    // Refresh onboarding status after completion
    await checkOnboardingStatus();
  };

  if (loading) {
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
          Loading Alwrity...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection="column"
      >
        <Typography variant="h6" color="error">
          {error}
        </Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>
          Please refresh the page to try again.
        </Typography>
      </Box>
    );
  }

  return (
    <Router>
      <Routes>
        {/* Dashboard Route */}
        <Route 
          path="/dashboard" 
          element={
            <DashboardWrapper />
          } 
        />
        
        {/* SEO Dashboard Route */}
        <Route 
          path="/seo-dashboard" 
          element={
            <SEODashboard />
          } 
        />
        
        {/* Content Planning Dashboard Route */}
        <Route 
          path="/content-planning" 
          element={
            <ContentPlanningDashboard />
          } 
        />
        
        {/* Memory Chat Route */}
        <Route 
          path="/memory-chat" 
          element={
            <MemoryChatPage />
          } 
        />
        
        {/* Root Route - Show onboarding or redirect to dashboard */}
        <Route 
          path="/" 
          element={
            onboardingStatus?.onboarding_required ? (
              <Wizard onComplete={handleOnboardingComplete} />
            ) : (
              <Navigate to="/dashboard" replace />
            )
          } 
        />
        
        {/* Catch all other routes */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

// Separate component to handle dashboard logic
const DashboardWrapper: React.FC = () => {
  const [dashboardLoading, setDashboardLoading] = useState(true);
  const [onboardingComplete, setOnboardingComplete] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    const checkDashboardAccess = async () => {
      try {
        console.log('DashboardWrapper: Checking dashboard access...');
        // Check if onboarding is complete
        const response = await apiClient.get('/api/onboarding/status');
        const status = response.data;
        
        console.log('DashboardWrapper: Backend status:', status);
        console.log('DashboardWrapper: is_completed:', status.is_completed);
        console.log('DashboardWrapper: current_step:', status.current_step);
        
        if (status.is_completed) {
          console.log('DashboardWrapper: Onboarding is complete, showing dashboard');
          setOnboardingComplete(true);
        } else {
          console.log('DashboardWrapper: Onboarding not complete, retry count:', retryCount);
          
          // If onboarding is not complete, try a few times with delay
          if (retryCount < 3) {
            console.log('DashboardWrapper: Retrying in 1 second...');
            setTimeout(() => {
              setRetryCount(prev => prev + 1);
            }, 1000);
            return;
          } else {
            console.log('DashboardWrapper: Max retries reached, redirecting to root');
            // If onboarding is not complete after retries, redirect to root
            window.location.href = '/';
            return;
          }
        }
      } catch (error) {
        console.error('DashboardWrapper: Error checking dashboard access:', error);
        
        // If there's an error, try a few times before redirecting
        if (retryCount < 3) {
          console.log('DashboardWrapper: Error occurred, retrying in 1 second...');
          setTimeout(() => {
            setRetryCount(prev => prev + 1);
          }, 1000);
          return;
        } else {
          console.log('DashboardWrapper: Max retries reached after error, redirecting to root');
          // If there's an error after retries, redirect to root
          window.location.href = '/';
          return;
        }
      } finally {
        setDashboardLoading(false);
      }
    };

    checkDashboardAccess();
  }, [retryCount]);

  if (dashboardLoading) {
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
          Loading Dashboard...
        </Typography>
        {retryCount > 0 && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Checking onboarding status... (Attempt {retryCount + 1}/3)
          </Typography>
        )}
      </Box>
    );
  }

  if (!onboardingComplete) {
    return <Navigate to="/" replace />;
  }

  return <MainDashboard />;
};

export default App; 