import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Box,
  Tabs,
  Tab,
  Typography
} from '@mui/material';
import {
  AutoAwesome as AutoAwesomeIcon,
  CalendarToday as CalendarIcon
} from '@mui/icons-material';
import ContentStrategyBuilder from '../components/ContentStrategyBuilder';
import CalendarGenerationWizard from '../components/CalendarGenerationWizard';
import { contentPlanningApi } from '../../../services/contentPlanningApi';
import { useStrategyCalendarContext } from '../../../contexts/StrategyCalendarContext';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

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
}

const CreateTab: React.FC = () => {
  const [userData, setUserData] = useState<any>({});
  const location = useLocation();
  
  // Get strategy context from the provider
  const { state: { strategyContext }, isFromStrategyActivation } = useStrategyCalendarContext();
  
  // Removed verbose logging for cleaner console

  // Memoize the strategy activation status to avoid infinite re-renders
  const fromStrategyActivation = useMemo(() => {
    return isFromStrategyActivation();
  }, [isFromStrategyActivation]);

  // Set initial tab value based on strategy activation
  const [tabValue, setTabValue] = useState(0); // Always start with Strategy Builder tab

  useEffect(() => {
    // Only load user data once on mount
    const loadData = async () => {
      try {
        const comprehensiveData = await contentPlanningApi.getComprehensiveUserData(1);
        setUserData(comprehensiveData.data);
      } catch (error) {
        console.error('Error loading user data:', error);
        // Set empty data to prevent infinite loops
        setUserData({});
      }
    };
    
    loadData();
  }, []); // Empty dependency array - only run once

  // Auto-switch to Calendar Wizard tab when coming from strategy activation
  useEffect(() => {
    // Removed verbose logging for cleaner console
    
    // Check multiple sources for strategy activation status
    const isFromStrategy = fromStrategyActivation || 
                          (strategyContext?.activationStatus === 'active') ||
                          (location.state as any)?.fromStrategyActivation;
    
    console.log('🔍 CreateTab: Strategy activation check:', {
      fromStrategyActivation,
      strategyContextActivationStatus: strategyContext?.activationStatus,
      windowLocationState: location.state || 'N/A',
      isFromStrategy
    });
    
    if (isFromStrategy) {
      console.log('🎯 CreateTab: Switching to Calendar Wizard tab (index 1)');
      setTabValue(1); // Switch to Calendar Wizard tab
    }
  }, [fromStrategyActivation, strategyContext?.activationStatus]);

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

  const handleGenerateCalendar = useCallback(async (calendarConfig: any) => {
    try {
      await contentPlanningApi.generateComprehensiveCalendar({
        ...calendarConfig,
        userData
      });
    } catch (error) {
      console.error('Error generating calendar:', error);
    }
  }, [userData]);

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
          fromStrategyActivation={fromStrategyActivation}
        />
      </TabPanel>
    </Box>
  );
};

export default CreateTab; 