import React, { useState, useEffect } from 'react';
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
  const [tabValue, setTabValue] = useState(0);
  const [userData, setUserData] = useState<any>({});

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      // Load comprehensive user data for calendar generation
      const comprehensiveData = await contentPlanningApi.getComprehensiveUserData(1); // Pass user ID
      setUserData(comprehensiveData.data); // Extract the data from the response
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleGenerateCalendar = async (calendarConfig: any) => {
    try {
      await contentPlanningApi.generateComprehensiveCalendar({
        ...calendarConfig,
        userData
      });
    } catch (error) {
      console.error('Error generating calendar:', error);
    }
  };

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
        />
      </TabPanel>
    </Box>
  );
};

export default CreateTab; 