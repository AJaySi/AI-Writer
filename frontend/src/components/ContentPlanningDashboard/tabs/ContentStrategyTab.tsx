import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  PlayArrow as PlayArrowIcon,
  AutoAwesome as AutoAwesomeIcon,
  Edit as EditIcon
} from '@mui/icons-material';
import { useContentPlanningStore } from '../../../stores/contentPlanningStore';
import { contentPlanningApi } from '../../../services/contentPlanningApi';
import StrategyIntelligenceTab from '../components/StrategyIntelligence/StrategyIntelligenceTab';
import StrategyOnboardingDialog from '../components/StrategyOnboardingDialog';
import { StrategyData } from '../components/StrategyIntelligence/types/strategy.types';

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
  const [strategyData, setStrategyData] = useState<StrategyData | null>(null);
  const [strategyDataLoading, setStrategyDataLoading] = useState(false);
  const [strategyDataError, setStrategyDataError] = useState<string | null>(null);
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
      loadStrategyData();
    } else if (strategiesArray.length === 0 && hasCheckedStrategy) {
      // Only set to 'none' if we've already checked and confirmed no strategies
      console.log('❌ No strategies found, setting status to none...');
      setStrategyStatus('none');
      setShowOnboarding(true);
    }
    // If strategiesArray.length === 0 and !hasCheckedStrategy, do nothing (wait for data to load)
  }, [strategies, loadStrategies]);

  const loadStrategyData = async () => {
    try {
      setStrategyDataLoading(true);
      setStrategyDataError(null);
      
      const userId = 1; // Default user ID
      
      // Try to get the latest generated strategy
      try {
        const latestStrategyResponse = await contentPlanningApi.getLatestGeneratedStrategy(userId);
        
        console.log('🔍 Latest strategy response from API:', latestStrategyResponse);
        
        if (latestStrategyResponse && latestStrategyResponse.strategic_insights) {
          console.log('✅ Found latest generated strategy:', latestStrategyResponse);
          setStrategyData(latestStrategyResponse);
          return;
        }
      } catch (pollingError) {
        console.log('No latest strategy found in polling system, checking database...', pollingError);
      }
      
      // If no strategy found in polling system, try to get from database
      try {
        const strategiesResponse = await contentPlanningApi.getEnhancedStrategies(userId);
        
        const strategies = strategiesResponse?.data?.strategies || strategiesResponse?.strategies || [];
        
        if (strategies && strategies.length > 0) {
          const latestStrategy = strategies[0];
          
          if (latestStrategy.comprehensive_ai_analysis) {
            console.log('✅ Found comprehensive strategy in database:', latestStrategy);
            setStrategyData(latestStrategy.comprehensive_ai_analysis);
            return;
          }
        }
      } catch (dbError) {
        console.log('No comprehensive strategies found in database:', dbError);
      }
      
      // If no strategy data is available
      console.log('❌ No comprehensive strategy data found');
      setStrategyData(null);
      setStrategyDataError('No comprehensive strategy data available. Please generate a strategy first.');
      
    } catch (err: any) {
      console.error('Error loading strategy data:', err);
      setStrategyDataError(err.message || 'Failed to load strategy data');
      setStrategyData(null);
    } finally {
      setStrategyDataLoading(false);
    }
  };

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
      
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setDataLoading({ strategies: false, insights: false, recommendations: false, strategicIntelligence: false });
    }
  };

  const handleConfirmStrategy = async () => {
    try {
      // In a real implementation, you would update the strategy status in the database
      setShowOnboarding(false);
      
      // Reload strategies to get updated data
      await loadStrategies();
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

      {/* Active Strategy Status Banner */}
      {strategyStatus === 'active' && currentStrategy && (
        <Alert 
          severity="success" 
          sx={{ mb: 3 }}
          action={
            <Button 
              color="inherit" 
              size="small" 
              onClick={() => setShowOnboarding(true)}
              startIcon={<EditIcon />}
            >
              Edit Strategy
            </Button>
          }
        >
          <Typography variant="body1">
            <strong>Strategy Active:</strong> Your AI-powered content strategy is active and being monitored. View performance analytics in the Analytics tab.
          </Typography>
        </Alert>
      )}

      {/* Strategic Intelligence - Only show if there's an active strategy */}
      {strategyStatus === 'active' && (
        <Paper sx={{ width: '100%', mb: 3 }}>
          <StrategyIntelligenceTab 
            strategyData={strategyData}
            loading={strategyDataLoading}
            error={strategyDataError}
          />
        </Paper>
      )}

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