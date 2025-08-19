import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Alert,
  Drawer,
  Button,
  Badge
} from '@mui/material';
import {
  Psychology as StrategyIcon,
  CalendarToday as CalendarIcon,
  Analytics as AnalyticsIcon,
  Search as SearchIcon,
  Lightbulb as AIInsightsIcon,
  Close as CloseIcon,
  Add as CreateIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import ContentStrategyTab from './tabs/ContentStrategyTab';
import CalendarTab from './tabs/CalendarTab';
import AnalyticsTab from './tabs/AnalyticsTab';
import GapAnalysisTab from './tabs/GapAnalysisTab';
import CreateTab from './tabs/CreateTab';
import AIInsightsPanel from './components/AIInsightsPanel';
import ServiceStatusPanel from './components/ServiceStatusPanel';
import ProgressIndicator from './components/ProgressIndicator';
import { useContentPlanningStore } from '../../stores/contentPlanningStore';
import { 
  contentPlanningOrchestrator, 
  ServiceStatus, 
  DashboardData 
} from '../../services/contentPlanningOrchestrator';
import { StrategyCalendarProvider } from '../../contexts/StrategyCalendarContext';

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
      id={`content-planning-tabpanel-${index}`}
      aria-labelledby={`content-planning-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `content-planning-tab-${index}`,
    'aria-controls': `content-planning-tabpanel-${index}`,
  };
}

const ContentPlanningDashboard: React.FC = () => {
  const location = useLocation();
  const [activeTab, setActiveTab] = useState(0);
  const [serviceStatuses, setServiceStatuses] = useState<ServiceStatus[]>([]);
  const [dashboardData, setDashboardData] = useState<DashboardData>({
    strategies: [],
    gapAnalyses: [],
    aiInsights: [],
    aiRecommendations: [],
    calendarEvents: [],
    healthStatus: {
      backend: false,
      database: false,
      aiServices: false
    }
  });
  const [statusPanelExpanded, setStatusPanelExpanded] = useState(false);
  const [progressExpanded, setProgressExpanded] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [aiInsightsDrawerOpen, setAiInsightsDrawerOpen] = useState(false);

  const { 
    updateStrategies,
    updateCalendarEvents,
    updateGapAnalyses,
    updateAIInsights
  } = useContentPlanningStore();

  // Initialize orchestrator callbacks
  useEffect(() => {
    contentPlanningOrchestrator.setProgressCallback((statuses) => {
      setServiceStatuses(statuses);
    });

    contentPlanningOrchestrator.setDataUpdateCallback((data) => {
      setDashboardData(prev => ({ ...prev, ...data }));
      
      // Update store with new data
      if (data.strategies) updateStrategies(data.strategies);
      if (data.calendarEvents) updateCalendarEvents(data.calendarEvents);
      if (data.gapAnalyses) updateGapAnalyses(data.gapAnalyses);
      if (data.aiInsights || data.aiRecommendations) {
        updateAIInsights({
          insights: data.aiInsights || [],
          recommendations: data.aiRecommendations || []
        });
      }
    });
  }, [updateStrategies, updateCalendarEvents, updateGapAnalyses, updateAIInsights]);

  // Handle navigation state for active tab
  useEffect(() => {
    if (location.state?.activeTab !== undefined) {
      setActiveTab(location.state.activeTab);
    }
  }, [location.state]);

  // Load dashboard data using orchestrator
  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        await contentPlanningOrchestrator.loadDashboardData();
      } catch (error: any) {
        console.error('Failed to load dashboard data:', error);
        setError(error.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    // Wrap in try-catch to handle any unexpected errors
    try {
      loadDashboardData();
    } catch (error: any) {
      console.error('Unexpected error in dashboard:', error);
      setError('An unexpected error occurred while loading the dashboard');
      setLoading(false);
    }
  }, []);

  const handleRefreshService = (serviceName: string) => {
    contentPlanningOrchestrator.refreshService(serviceName);
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const getOverallHealthStatus = () => {
    const { healthStatus } = dashboardData;
    if (healthStatus.backend && healthStatus.database && healthStatus.aiServices) {
      return { status: 'success', text: 'Connected' };
    } else if (healthStatus.backend && healthStatus.database) {
      return { status: 'warning', text: 'Connected API & DB' };
    } else {
      return { status: 'error', text: 'Disconnected' };
    }
  };

  const overallHealth = getOverallHealthStatus();

  const tabs = [
    { label: 'CONTENT STRATEGY', icon: <StrategyIcon />, component: <ContentStrategyTab /> },
    { label: 'CALENDAR', icon: <CalendarIcon />, component: <CalendarTab /> },
    { label: 'ANALYTICS', icon: <AnalyticsIcon />, component: <AnalyticsTab /> },
    { label: 'GAP ANALYSIS', icon: <SearchIcon />, component: <GapAnalysisTab /> },
    { label: 'CREATE', icon: <CreateIcon />, component: <CreateTab /> }
  ];

  const totalAIItems = (dashboardData.aiInsights?.length || 0) + (dashboardData.aiRecommendations?.length || 0);

  return (
    <StrategyCalendarProvider>
      <Container maxWidth={false} sx={{ height: '100vh', p: 0 }}>
      <AppBar position="static" color="default" elevation={1}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Content Planning Dashboard
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <ServiceStatusPanel 
              serviceStatuses={serviceStatuses} 
              onRefreshService={handleRefreshService} 
              expanded={statusPanelExpanded} 
              onToggleExpanded={() => setStatusPanelExpanded(!statusPanelExpanded)} 
            />
            
            {/* AI Insights Button with Badge */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Button
                variant="outlined"
                startIcon={<AIInsightsIcon />}
                onClick={() => setAiInsightsDrawerOpen(true)}
                sx={{
                  borderRadius: 2,
                  textTransform: 'none',
                  fontWeight: 600,
                  borderColor: 'primary.main',
                  color: 'primary.main',
                  '&:hover': {
                    borderColor: 'primary.dark',
                    backgroundColor: 'primary.50'
                  }
                }}
              >
                <Badge badgeContent={totalAIItems} color="primary" sx={{ mr: 1 }}>
                  AI Insights
                </Badge>
              </Button>
            </motion.div>
          </Box>
        </Toolbar>
      </AppBar>

      {error && (
        <Alert severity="error" sx={{ m: 2 }}>
          {error}
        </Alert>
      )}

      {/* Progress Indicator */}
      {loading && (
        <Box sx={{ m: 2 }}>
          <ProgressIndicator
            serviceStatuses={serviceStatuses}
            onRefreshService={handleRefreshService}
            expanded={progressExpanded}
            onToggleExpanded={() => setProgressExpanded(!progressExpanded)}
          />
        </Box>
      )}

      <Box sx={{ display: 'flex', height: 'calc(100vh - 64px)' }}>
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs
              value={activeTab}
              onChange={handleTabChange}
              aria-label="content planning tabs"
              sx={{ px: 2 }}
            >
              {tabs.map((tab, index) => (
                <Tab
                  key={index}
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {tab.icon}
                      {tab.label}
                    </Box>
                  }
                  {...a11yProps(index)}
                />
              ))}
            </Tabs>
          </Box>

          {tabs.map((tab, index) => (
            <TabPanel key={index} value={activeTab} index={index}>
              {tab.component}
            </TabPanel>
          ))}
        </Box>
      </Box>

      {/* AI Insights Drawer */}
      <Drawer
        anchor="right"
        open={aiInsightsDrawerOpen}
        onClose={() => setAiInsightsDrawerOpen(false)}
        PaperProps={{
          sx: {
            width: 400,
            height: '100%',
            backgroundColor: 'background.paper',
            borderLeft: '1px solid',
            borderColor: 'divider'
          }
        }}
      >
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
              <AIInsightsIcon sx={{ mr: 1 }} />
              AI Insights
            </Typography>
            <IconButton 
              onClick={() => setAiInsightsDrawerOpen(false)}
              size="small"
            >
              <CloseIcon />
            </IconButton>
          </Box>
        </Box>
        
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          <AnimatePresence>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <AIInsightsPanel />
            </motion.div>
          </AnimatePresence>
        </Box>
      </Drawer>
      </Container>
    </StrategyCalendarProvider>
  );
};

export default ContentPlanningDashboard; 