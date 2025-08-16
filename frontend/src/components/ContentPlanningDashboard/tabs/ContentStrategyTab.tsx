import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Chip,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress,
  CircularProgress,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Tooltip,
  Badge
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Business as BusinessIcon,
  Lightbulb as LightbulbIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Analytics as AnalyticsIcon,
  Timeline as TimelineIcon,
  Assessment as AssessmentIcon,
  ExpandMore as ExpandMoreIcon,
  Refresh as RefreshIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Visibility as VisibilityIcon,
  ShowChart as ShowChartIcon,
  AutoAwesome as AutoAwesomeIcon,
  PlayArrow as PlayArrowIcon
} from '@mui/icons-material';
import { useContentPlanningStore } from '../../../stores/contentPlanningStore';
import { contentPlanningApi } from '../../../services/contentPlanningApi';
import StrategyIntelligenceTab from '../components/StrategyIntelligence/StrategyIntelligenceTab';
import StrategyOnboardingDialog from '../components/StrategyOnboardingDialog';

const ContentStrategyTab: React.FC = () => {
  const { 
    strategies, 
    currentStrategy, 
    aiInsights, 
    aiRecommendations, 
    loading, 
    error,
    loadStrategies,
    loadAIInsights,
    loadAIRecommendations
  } = useContentPlanningStore();
  
  const [strategyForm, setStrategyForm] = useState({
    name: '',
    description: '',
    industry: '',
    target_audience: '',
    content_pillars: []
  });

  // Real data states
  const [strategicIntelligence, setStrategicIntelligence] = useState<any>(null);
  const [dataLoading, setDataLoading] = useState({
    strategies: false,
    insights: false,
    recommendations: false,
    strategicIntelligence: false
  });

  // Strategy status and onboarding
  const [strategyStatus, setStrategyStatus] = useState<'active' | 'inactive' | 'none'>('none');
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [hasCheckedStrategy, setHasCheckedStrategy] = useState(false);

  // Load data on component mount
  useEffect(() => {
    loadInitialData();
  }, []);

  // Check strategy status when strategies are loaded
  useEffect(() => {
    console.log('🔄 useEffect triggered - strategies changed:', strategies);
    console.log('🔄 Strategies type:', typeof strategies);
    console.log('🔄 Is Array:', Array.isArray(strategies));
    console.log('🔄 Strategies length:', strategies?.length);
    console.log('🔄 Has checked strategy:', hasCheckedStrategy);
    
    // Handle different response formats
    let strategiesArray: any[] = [];
    
    if (Array.isArray(strategies)) {
      // Direct array
      strategiesArray = strategies;
    } else if (strategies && typeof strategies === 'object' && 'strategies' in strategies && Array.isArray((strategies as any).strategies)) {
      // API response object with strategies array
      strategiesArray = (strategies as any).strategies;
    }
    
    console.log('🔄 StrategiesArray length:', strategiesArray.length);
    
    if (strategiesArray.length > 0) {
      console.log('✅ Strategies found, checking status...');
      checkStrategyStatus();
    } else if (strategiesArray.length === 0 && hasCheckedStrategy) {
      // Only set to 'none' if we've already checked and confirmed no strategies
      console.log('❌ No strategies found, setting status to none...');
      setStrategyStatus('none');
      setShowOnboarding(true);
    }
    // If strategiesArray.length === 0 and !hasCheckedStrategy, do nothing (wait for data to load)
  }, [strategies, loadStrategies]);

  const checkStrategyStatus = () => {
    console.log('🔍 Checking strategy status...');
    console.log('🔍 Strategies from store:', strategies);
    console.log('🔍 Strategies type:', typeof strategies);
    console.log('🔍 Is Array:', Array.isArray(strategies));
    console.log('🔍 Strategies length:', strategies?.length);
    
    // Handle different response formats
    let strategiesArray: any[] = [];
    
    if (Array.isArray(strategies)) {
      // Direct array
      strategiesArray = strategies;
    } else if (strategies && typeof strategies === 'object' && 'strategies' in strategies && Array.isArray((strategies as any).strategies)) {
      // API response object with strategies array
      strategiesArray = (strategies as any).strategies;
    }
    
    console.log('🔍 StrategiesArray length:', strategiesArray.length);
    
    if (strategiesArray.length > 0) {
      // Find the most recent strategy
      const latestStrategy = strategiesArray[0]; // Assuming strategies are sorted by date
      
      console.log('✅ Found strategies in database:', strategiesArray.length);
      console.log('📊 Latest strategy:', latestStrategy);
      
      // For now, we'll assume strategies are active if they exist
      // In a real implementation, you would check a status field from the database
      setStrategyStatus('active');
      setShowOnboarding(false);
    } else {
      console.log('❌ No strategies found in database');
      setStrategyStatus('none');
      setShowOnboarding(true);
    }
    setHasCheckedStrategy(true);
  };

  const loadInitialData = async () => {
    try {
      setDataLoading({ strategies: true, insights: true, recommendations: true, strategicIntelligence: true });
      
      // Load strategies
      await loadStrategies();
      
      // Load AI insights and recommendations
      await Promise.all([
        loadAIInsights(),
        loadAIRecommendations()
      ]);

      // Load strategic intelligence
      await loadStrategicIntelligence();
      
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setDataLoading({ strategies: false, insights: false, recommendations: false, strategicIntelligence: false });
    }
  };

  const loadStrategicIntelligence = async () => {
    try {
      setDataLoading(prev => ({ ...prev, strategicIntelligence: true }));
      
      // Use streaming endpoint for real-time updates
      const eventSource = await contentPlanningApi.streamStrategicIntelligence(1);
      
      contentPlanningApi.handleSSEData(
        eventSource,
        (data) => {
          
          if (data.type === 'status') {
            // Update loading message
          } else if (data.type === 'progress') {
            // Update progress (could be used for progress bar)
          } else if (data.type === 'result' && data.status === 'success') {
            // Set the strategic intelligence data
            setStrategicIntelligence(data.data);
            setDataLoading(prev => ({ ...prev, strategicIntelligence: false }));
          } else if (data.type === 'error') {
            // Set fallback data on error
            setStrategicIntelligence({
              market_positioning: {
                score: 75,
                strengths: ['Strong brand voice', 'Consistent content quality'],
                weaknesses: ['Limited video content', 'Slow content production']
              },
              competitive_advantages: [
                { advantage: 'AI-powered content creation', impact: 'High', implementation: 'In Progress' },
                { advantage: 'Data-driven strategy', impact: 'Medium', implementation: 'Complete' }
              ],
              strategic_risks: [
                { risk: 'Content saturation in market', probability: 'Medium', impact: 'High' },
                { risk: 'Algorithm changes affecting reach', probability: 'High', impact: 'Medium' }
              ]
            });
            setDataLoading(prev => ({ ...prev, strategicIntelligence: false }));
          }
        },
        (error) => {
          // Set fallback data on error
          setStrategicIntelligence({
            market_positioning: {
              score: 75,
              strengths: ['Strong brand voice', 'Consistent content quality'],
              weaknesses: ['Limited video content', 'Slow content production']
            },
            competitive_advantages: [
              { advantage: 'AI-powered content creation', impact: 'High', implementation: 'In Progress' },
              { advantage: 'Data-driven strategy', impact: 'Medium', implementation: 'Complete' }
            ],
            strategic_risks: [
              { risk: 'Content saturation in market', probability: 'Medium', impact: 'High' },
              { risk: 'Algorithm changes affecting reach', probability: 'High', impact: 'Medium' }
            ]
          });
          setDataLoading(prev => ({ ...prev, strategicIntelligence: false }));
        }
      );
      
    } catch (error) {
      console.error('Error loading strategic intelligence:', error);
      // Set fallback data on error
      setStrategicIntelligence({
        market_positioning: {
          score: 75,
          strengths: ['Strong brand voice', 'Consistent content quality'],
          weaknesses: ['Limited video content', 'Slow content production']
        },
        competitive_advantages: [
          { advantage: 'AI-powered content creation', impact: 'High', implementation: 'In Progress' },
          { advantage: 'Data-driven strategy', impact: 'Medium', implementation: 'Complete' }
        ],
        strategic_risks: [
          { risk: 'Content saturation in market', probability: 'Medium', impact: 'High' },
          { risk: 'Algorithm changes affecting reach', probability: 'High', impact: 'Medium' }
        ]
      });
      setDataLoading(prev => ({ ...prev, strategicIntelligence: false }));
    }
  };

  const handleStrategyFormChange = (field: string, value: string) => {
    setStrategyForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleCreateStrategy = async () => {
    if (!strategyForm.name || !strategyForm.description) {
      return;
    }

    try {
      // Call backend API to create strategy
      await contentPlanningApi.createStrategy({
        name: strategyForm.name,
        description: strategyForm.description,
        industry: strategyForm.industry,
        target_audience: strategyForm.target_audience,
        content_pillars: strategyForm.content_pillars
      });

      // Reload data after creating strategy
      await loadInitialData();
      
      // Reset form
      setStrategyForm({
        name: '',
        description: '',
        industry: '',
        target_audience: '',
        content_pillars: []
      });
    } catch (error) {
      console.error('Error creating strategy:', error);
    }
  };

  const handleRefreshData = async () => {
    await loadInitialData();
  };

  // Onboarding dialog handlers
  const handleConfirmStrategy = async () => {
    try {
      if (currentStrategy) {
        // For now, we'll just close the dialog since we can't update status
        // In a real implementation, you would update the strategy status in the database
        setShowOnboarding(false);
        
        // Reload strategies to get updated data
        await loadStrategies();
      }
    } catch (error) {
      console.error('Error activating strategy:', error);
    }
  };

  const handleEditStrategy = () => {
    setShowOnboarding(false);
    // Navigate to Create tab to edit strategy
    // This would typically involve changing the active tab in the parent component
  };

  const handleCreateNewStrategy = () => {
    setShowOnboarding(false);
    // Navigate to Create tab to create new strategy
    // This would typically involve changing the active tab in the parent component
  };

  const handleCloseOnboarding = () => {
    setShowOnboarding(false);
  };

  return (
    <Box sx={{ p: 3 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Strategy Status Banner */}
      {strategyStatus === 'inactive' && (
        <Alert 
          severity="warning" 
          sx={{ mb: 3 }}
          action={
            <Button 
              color="inherit" 
              size="small" 
              onClick={() => setShowOnboarding(true)}
              startIcon={<PlayArrowIcon />}
            >
              Activate Strategy
            </Button>
          }
        >
          <Typography variant="body1">
            <strong>Strategy Pending Activation:</strong> Your content strategy is ready but needs to be activated to start your AI-powered content marketing journey.
          </Typography>
        </Alert>
      )}

      {strategyStatus === 'none' && (
        <Alert 
          severity="info" 
          sx={{ mb: 3 }}
          action={
            <Button 
              color="inherit" 
              size="small" 
              onClick={() => setShowOnboarding(true)}
              startIcon={<AutoAwesomeIcon />}
            >
              Create Strategy
            </Button>
          }
        >
          <Typography variant="body1">
            <strong>No Strategy Found:</strong> Let's create your first AI-powered content strategy to start your digital marketing journey.
          </Typography>
        </Alert>
      )}



      {/* Strategic Intelligence */}
      <Paper sx={{ width: '100%', mb: 3 }}>
        <StrategyIntelligenceTab />
      </Paper>

      {/* Strategy Onboarding Dialog */}
      <StrategyOnboardingDialog
        open={showOnboarding}
        onClose={handleCloseOnboarding}
        onConfirmStrategy={handleConfirmStrategy}
        onEditStrategy={handleEditStrategy}
        onCreateNewStrategy={handleCreateNewStrategy}
        currentStrategy={currentStrategy}
        strategyStatus={strategyStatus}
      />
    </Box>
  );
};

export default ContentStrategyTab;