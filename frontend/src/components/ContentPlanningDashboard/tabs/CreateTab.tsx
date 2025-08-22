import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  Tabs,
  Tab
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
      // Transform calendarConfig to match backend CalendarGenerationRequest format
      const requestData = {
        user_id: 1, // Default user ID
        strategy_id: strategyContext?.strategyId ? parseInt(strategyContext.strategyId) : undefined,
        calendar_type: calendarConfig.calendarType || 'monthly',
        industry: userData?.industry || 'technology',
        business_size: 'sme',
        force_refresh: false
      };
      
      console.log('🎯 Starting calendar generation with modal:', requestData);
      
      // Call the new start endpoint to get session ID
      const startResponse = await fetch('/api/content-planning/calendar-generation/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
      
      if (!startResponse.ok) {
        throw new Error(`Failed to start calendar generation: ${startResponse.statusText}`);
      }
      
      const startData = await startResponse.json();
      const sessionId = startData.session_id;
      
      // Store the session ID and calendar config for the modal
      setSessionId(sessionId);
      setCurrentCalendarConfig(calendarConfig);
      
      // Open the modal to show progress
      setIsModalOpen(true);
      
    } catch (error) {
      console.error('Error starting calendar generation:', error);
      // The modal will handle error display
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
          loading={false}
          strategyContext={strategyContext}
          fromStrategyActivation={isFromStrategyActivation()}
        />
      </TabPanel>

      {/* Calendar Generation Modal */}
      {currentCalendarConfig && (
        <CalendarGenerationModal
          open={isModalOpen}
          onClose={handleModalClose}
          sessionId={sessionId}
          initialConfig={{
            userId: userData?.id?.toString() || '1',
            strategyId: strategyContext?.strategyId || '',
            calendarType: currentCalendarConfig.calendarType === 'weekly' ? 'monthly' : 
                         currentCalendarConfig.calendarType === 'quarterly' ? 'quarterly' : 'monthly',
            platforms: currentCalendarConfig.priorityPlatforms || [],
            duration: currentCalendarConfig.calendarDuration || 30,
            postingFrequency: currentCalendarConfig.postingFrequency ? 
              (currentCalendarConfig.postingFrequency >= 7 ? 'daily' : 
               currentCalendarConfig.postingFrequency >= 3 ? 'biweekly' : 'weekly') : 'weekly'
          }}
          onComplete={handleModalComplete}
          onError={handleModalError}
        />
      )}
    </Box>
  );
};

export default CreateTab; 