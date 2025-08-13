import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  TextField,
  Card,
  CardContent,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  LinearProgress,
  Tooltip,
  Badge
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CalendarToday as CalendarIcon,
  Event as EventIcon,
  Refresh as RefreshIcon,
  TrendingUp as TrendingIcon,
  ContentCopy as RepurposeIcon,
  Analytics as AnalyticsIcon,
  ExpandMore as ExpandMoreIcon,
  Schedule as ScheduleIcon,
  Psychology as PsychologyIcon,
  Business as BusinessIcon,
  Group as GroupIcon,
  Timeline as TimelineIcon,
  Lightbulb as LightbulbIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  DataUsage as DataUsageIcon,
  Insights as InsightsIcon,
  Assessment as AssessmentIcon,
  Campaign as CampaignIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';
import { useContentPlanningStore } from '../../../stores/contentPlanningStore';
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
      id={`calendar-tabpanel-${index}`}
      aria-labelledby={`calendar-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const CalendarTab: React.FC = () => {
  const { 
    calendarEvents, 
    createEvent, 
    updateEvent, 
    deleteEvent, 
    loading, 
    error,
    loadCalendarEvents,
    updateCalendarEvents,
    // New calendar generation state
    generatedCalendar,
    performancePrediction,
    contentRepurposing,
    aiInsights,
    calendarGenerationError,
    dataLoading
  } = useContentPlanningStore();
  
  const [tabValue, setTabValue] = useState(0);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState<any>(null);
  const [eventForm, setEventForm] = useState({
    title: '',
    description: '',
    content_type: '',
    platform: '',
    scheduled_date: '',
    status: 'draft' as 'draft' | 'scheduled' | 'published'
  });

  // Enhanced state for data transparency
  const [userData, setUserData] = useState<any>({
    onboardingData: {},
    gapAnalysis: {},
    strategyData: {},
    recommendationsData: [],
    performanceData: {},
    aiAnalysisResults: []
  });

  const safeCalendarEvents = Array.isArray(calendarEvents) ? calendarEvents : [];

  useEffect(() => {
    loadCalendarData();
  }, []);

  const loadCalendarData = async () => {
    try {
      // Load comprehensive user data for calendar generation
      const comprehensiveData = await contentPlanningApi.getComprehensiveUserData(1); // Pass user ID
      setUserData(comprehensiveData.data); // Extract the data from the response
      
      // Load existing calendar events
      await loadCalendarEvents();
    } catch (error) {
      console.error('Error loading calendar data:', error);
    }
  };

  const handleOpenDialog = (event?: any) => {
    if (event) {
      setSelectedEvent(event);
      setEventForm({
        title: event.title,
        description: event.description,
        content_type: event.content_type,
        platform: event.platform,
        scheduled_date: event.scheduled_date || event.date,
        status: event.status as 'draft' | 'scheduled' | 'published'
      });
    } else {
      setSelectedEvent(null);
      setEventForm({
        title: '',
        description: '',
        content_type: '',
        platform: '',
        scheduled_date: '',
        status: 'draft' as 'draft' | 'scheduled' | 'published'
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedEvent(null);
  };

  const handleSaveEvent = async () => {
    try {
      const eventData = {
        title: eventForm.title,
        description: eventForm.description,
        content_type: eventForm.content_type,
        platform: eventForm.platform,
        date: eventForm.scheduled_date, // Map scheduled_date to date for API compatibility
        status: eventForm.status as 'draft' | 'scheduled' | 'published'
      };
      
      if (selectedEvent) {
        await updateEvent(selectedEvent.id, eventData);
      } else {
        await createEvent(eventData);
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving event:', error);
    }
  };

  const handleDeleteEvent = async (eventId: string) => {
    try {
      await deleteEvent(eventId);
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  };

  const handleRefreshData = async () => {
    await loadCalendarData();
  };

  const handleDataUpdate = (updatedData: any) => {
    setUserData((prev: any) => ({ ...prev, ...updatedData }));
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

  const handleOptimizeContent = async (contentData: any) => {
    try {
      await contentPlanningApi.optimizeContent(contentData);
    } catch (error) {
      console.error('Error optimizing content:', error);
    }
  };

  const handlePredictPerformance = async (contentData: any) => {
    try {
      await contentPlanningApi.predictPerformance(contentData);
    } catch (error) {
      console.error('Error predicting performance:', error);
    }
  };

  const handleGetTrendingTopics = async () => {
    try {
      await contentPlanningApi.getTrendingTopics({ user_id: 1, industry: 'technology' });
    } catch (error) {
      console.error('Error getting trending topics:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'default';
      case 'scheduled': return 'warning';
      case 'published': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Content Calendar
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={handleRefreshData}
            disabled={dataLoading}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
          >
            Add Event
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {calendarGenerationError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {calendarGenerationError}
        </Alert>
      )}

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Calendar Events" icon={<CalendarIcon />} iconPosition="start" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        {/* Calendar Events Tab */}
        {dataLoading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  <CalendarIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Scheduled Events
                </Typography>
                
                {safeCalendarEvents.length === 0 ? (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <EventIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary" gutterBottom>
                      No events scheduled
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Create your first content event to get started
                    </Typography>
                  </Box>
                ) : (
                  <Grid container spacing={2}>
                    {safeCalendarEvents.map((event) => (
                      <Grid item xs={12} md={6} lg={4} key={event.id}>
                        <Card>
                          <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                              <Typography variant="h6" component="div">
                                {event.title}
                              </Typography>
                              <Box>
                                <IconButton
                                  size="small"
                                  onClick={() => handleOpenDialog(event)}
                                >
                                  <EditIcon />
                                </IconButton>
                                <IconButton
                                  size="small"
                                  color="error"
                                  onClick={() => handleDeleteEvent(event.id)}
                                >
                                  <DeleteIcon />
                                </IconButton>
                              </Box>
                            </Box>
                            
                            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                              {event.description}
                            </Typography>
                            
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                              <Chip
                                label={event.platform}
                                size="small"
                                variant="outlined"
                              />
                              <Chip
                                label={event.content_type}
                                size="small"
                                variant="outlined"
                              />
                              <Chip
                                label={event.status}
                                size="small"
                                color={getStatusColor(event.status)}
                              />
                            </Box>
                            
                            <Typography variant="caption" color="text.secondary">
                              Scheduled: {new Date(event.scheduled_date || event.date || '').toLocaleDateString()}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                )}
              </Paper>
            </Grid>
          </Grid>
        )}
      </TabPanel>

      {/* Event Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedEvent ? 'Edit Event' : 'Add New Event'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <TextField
              label="Title"
              value={eventForm.title}
              onChange={(e) => setEventForm({ ...eventForm, title: e.target.value })}
                fullWidth
              />
              <TextField
              label="Description"
              value={eventForm.description}
              onChange={(e) => setEventForm({ ...eventForm, description: e.target.value })}
                multiline
                rows={3}
                fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>Content Type</InputLabel>
              <Select
                value={eventForm.content_type}
                onChange={(e) => setEventForm({ ...eventForm, content_type: e.target.value })}
                label="Content Type"
              >
                <MenuItem value="blog_post">Blog Post</MenuItem>
                <MenuItem value="video">Video</MenuItem>
                <MenuItem value="social_post">Social Post</MenuItem>
                <MenuItem value="case_study">Case Study</MenuItem>
                <MenuItem value="whitepaper">Whitepaper</MenuItem>
              </Select>
            </FormControl>
              <FormControl fullWidth>
                <InputLabel>Platform</InputLabel>
                <Select
                value={eventForm.platform}
                onChange={(e) => setEventForm({ ...eventForm, platform: e.target.value })}
                  label="Platform"
                >
                  <MenuItem value="website">Website</MenuItem>
                  <MenuItem value="linkedin">LinkedIn</MenuItem>
                  <MenuItem value="twitter">Twitter</MenuItem>
                  <MenuItem value="instagram">Instagram</MenuItem>
                  <MenuItem value="youtube">YouTube</MenuItem>
                </Select>
              </FormControl>
            <TextField
              label="Scheduled Date"
              type="datetime-local"
              value={eventForm.scheduled_date}
              onChange={(e) => setEventForm({ ...eventForm, scheduled_date: e.target.value })}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                value={eventForm.status}
                onChange={(e) => setEventForm({ ...eventForm, status: e.target.value as 'draft' | 'scheduled' | 'published' })}
                  label="Status"
                >
                  <MenuItem value="draft">Draft</MenuItem>
                  <MenuItem value="scheduled">Scheduled</MenuItem>
                  <MenuItem value="published">Published</MenuItem>
                </Select>
              </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSaveEvent} variant="contained">
            {selectedEvent ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CalendarTab; 