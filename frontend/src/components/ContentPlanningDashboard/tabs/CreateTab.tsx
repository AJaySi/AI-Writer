import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Button
} from '@mui/material';
import {
  AutoAwesome as AutoAwesomeIcon,
  CalendarToday as CalendarIcon
} from '@mui/icons-material';
import { useLocation } from 'react-router-dom';

// Import components
import ContentStrategyBuilder from '../components/ContentStrategyBuilder';
import CalendarGenerationWizard from '../components/CalendarGenerationWizard';
import { CalendarGenerationModal } from '../components/CalendarGenerationModal';

// Import hooks and services
import { useStrategyCalendarContext } from '../../../contexts/StrategyCalendarContext';
import { contentPlanningApi } from '../../../services/contentPlanningApi';

// Import types
import { type CalendarConfig } from '../components/CalendarWizardSteps/types';

// TabPanel component
interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index, ...other }) => {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`create-tabpanel-${index}`}
      aria-labelledby={`create-tab-${index}`}
      {...other}
    >
      {value === index && <Box>{children}</Box>}
    </div>
  );
};

const CreateTab: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentCalendarConfig, setCurrentCalendarConfig] = useState<CalendarConfig | null>(null);
  const [sessionId, setSessionId] = useState<string>('');
  const [isStartingGeneration, setIsStartingGeneration] = useState(false);

  const location = useLocation();
  const { state: { strategyContext }, isFromStrategyActivation } = useStrategyCalendarContext();
  const [userData, setUserData] = useState<any>({});

  // Handle navigation from strategy activation
  useEffect(() => {
    const fromStrategyActivation = isFromStrategyActivation();
    const isFromStrategy = fromStrategyActivation || 
      (location.state as any)?.fromStrategyActivation ||
      (location.state as any)?.strategyContext;

    console.log('🔍 CreateTab: Navigation state check:', {
      fromStrategyActivation,
      windowLocationState: location.state || 'N/A',
      isFromStrategy
    });
    
    if (isFromStrategy) {
      console.log('🎯 CreateTab: Switching to Calendar Wizard tab (index 1)');
      setTabValue(1); // Switch to Calendar Wizard tab
    }
  }, [isFromStrategyActivation, strategyContext?.activationStatus]);

  // Also check on mount for immediate navigation state
  useEffect(() => {
    const checkNavigationState = () => {
      const locationState = location.state as any;
      console.log('🔍 CreateTab: Initial navigation state check:', locationState);
      
      if (locationState?.fromStrategyActivation || locationState?.strategyContext) {
        console.log('🎯 CreateTab: Found navigation state, switching to Calendar Wizard tab (index 1)');
        setTabValue(1);
      }
    };
    
    // Check immediately
    checkNavigationState();
    
    // Also check after a short delay to ensure context is loaded
    const timer = setTimeout(checkNavigationState, 100);
    return () => clearTimeout(timer);
  }, [location.state]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleGenerateCalendar = useCallback(async (calendarConfig: CalendarConfig) => {
    try {
      console.log('🎯 handleGenerateCalendar called with config:', calendarConfig);
      
      // OPEN MODAL IMMEDIATELY - Don't wait for backend response
      console.log('🎯 Opening modal immediately');
      setCurrentCalendarConfig(calendarConfig);
      setIsModalOpen(true);
      
      // Set loading state to prevent multiple clicks
      setIsStartingGeneration(true);
      
      // Transform calendarConfig to match backend CalendarGenerationRequest format
      const requestData = {
        user_id: 1, // Default user ID
        strategy_id: strategyContext?.strategyId ? parseInt(strategyContext.strategyId) : undefined,
        calendar_type: calendarConfig.calendarType || 'monthly',
        industry: userData?.industry || 'technology',
        business_size: 'sme',
        force_refresh: false
      };
      
      console.log('🎯 Starting calendar generation request:', requestData);
      
      // Call the new start endpoint to get session ID with retry logic
      let startResponse;
      let retryCount = 0;
      const maxRetries = 3;
      
      while (retryCount < maxRetries) {
        try {
          startResponse = await fetch('/api/content-planning/calendar-generation/start', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
          });
          
          if (startResponse.ok) {
            break; // Success, exit retry loop
          } else {
            console.warn(`⚠️ Attempt ${retryCount + 1} failed with status: ${startResponse.status}`);
            retryCount++;
            if (retryCount < maxRetries) {
              // Wait before retry (exponential backoff)
              await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
            }
          }
        } catch (error) {
          console.warn(`⚠️ Attempt ${retryCount + 1} failed with error:`, error);
          retryCount++;
          if (retryCount < maxRetries) {
            // Wait before retry (exponential backoff)
            await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
          }
        }
      }
      
      if (!startResponse || !startResponse.ok) {
        throw new Error(`Failed to start calendar generation after ${maxRetries} attempts: ${startResponse?.statusText || 'Network error'}`);
      }
      
      const startData = await startResponse.json();
      const sessionId = startData.session_id;
      
      console.log('🎯 Backend response received, session ID:', sessionId);
      console.log('🎯 Session status:', startData.status);
      
      // Update modal with the real session ID
      console.log('🎯 Updating modal with real session ID');
      setSessionId(sessionId);
      
      console.log('🎯 Modal updated with session ID - polling should start immediately');
      
    } catch (error) {
      console.error('Error starting calendar generation:', error);
      
      // Show user-friendly error message
      const errorMessage = error instanceof Error ? error.message : 'Failed to start calendar generation';
      console.error('❌ Calendar generation failed:', errorMessage);
      
      // Show error to user and close modal
      alert(`Failed to start calendar generation: ${errorMessage}`);
      setIsModalOpen(false);
      setCurrentCalendarConfig(null);
      setSessionId('');
    } finally {
      // Clear loading state
      setIsStartingGeneration(false);
    }
  }, [userData, strategyContext]);

  const handleModalComplete = useCallback((results: any) => {
    console.log('🎉 Calendar generation completed:', results);
    setIsModalOpen(false);
    setCurrentCalendarConfig(null);
    setSessionId('');
    
    // TODO: Handle the completed calendar results
    // This could include navigating to a calendar view, showing success message, etc.
  }, []);

  const handleModalError = useCallback((error: string) => {
    console.error('❌ Calendar generation error:', error);
    setIsModalOpen(false);
    setCurrentCalendarConfig(null);
    setSessionId('');
    
    // TODO: Handle error display (could show a toast notification)
  }, []);

  const handleModalClose = useCallback(() => {
    setIsModalOpen(false);
    setCurrentCalendarConfig(null);
    setSessionId('');
  }, []);



  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Create
      </Typography>
      


      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="create tabs">
          <Tab 
            label={
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <AutoAwesomeIcon sx={{ mr: 1 }} />
                Enhanced Strategy Builder
              </Box>
            } 
          />
          <Tab 
            label={
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <CalendarIcon sx={{ mr: 1 }} />
                Calendar Wizard
              </Box>
            } 
          />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <ContentStrategyBuilder />
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <CalendarGenerationWizard
          userData={userData}
          onGenerateCalendar={handleGenerateCalendar}
          strategyContext={strategyContext}
          fromStrategyActivation={isFromStrategyActivation()}
        />
      </TabPanel>

      {/* Calendar Generation Modal */}
      <CalendarGenerationModal
        open={isModalOpen}
        onClose={handleModalClose}
        sessionId={sessionId}
        initialConfig={{
          userId: userData?.id?.toString() || '1',
          strategyId: strategyContext?.strategyId || '',
          calendarType: currentCalendarConfig?.calendarType === 'weekly' ? 'monthly' : 
                       currentCalendarConfig?.calendarType === 'quarterly' ? 'quarterly' : 'monthly',
          platforms: currentCalendarConfig?.priorityPlatforms || [],
          duration: currentCalendarConfig?.calendarDuration || 30,
          postingFrequency: currentCalendarConfig?.postingFrequency ? 
            (currentCalendarConfig.postingFrequency >= 7 ? 'daily' : 
             currentCalendarConfig.postingFrequency >= 3 ? 'biweekly' : 'weekly') : 'weekly'
        }}
        onComplete={handleModalComplete}
        onError={handleModalError}
      />
    </Box>
  );
};

export default CreateTab; 