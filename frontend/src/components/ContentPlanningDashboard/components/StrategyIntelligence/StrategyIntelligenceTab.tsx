import React, { useEffect } from 'react';
import { Box, CircularProgress, Alert, Typography } from '@mui/material';
import StrategyHeader from './components/StrategyHeader';
import StrategicInsightsCard from './components/StrategicInsightsCard';
import CompetitiveAnalysisCard from './components/CompetitiveAnalysisCard';
import PerformancePredictionsCard from './components/PerformancePredictionsCard';
import ImplementationRoadmapCard from './components/ImplementationRoadmapCard';
import RiskAssessmentCard from './components/RiskAssessmentCard';
import ReviewProgressHeader from './components/ReviewProgressHeader';
import { StrategyData } from './types/strategy.types';
import { useStrategyReviewStore } from '../../../../stores/strategyReviewStore';

interface StrategyIntelligenceTabProps {
  strategyData?: StrategyData | null;
  loading?: boolean;
  error?: string | null;
}

const StrategyIntelligenceTab: React.FC<StrategyIntelligenceTabProps> = ({ 
  strategyData, 
  loading = false, 
  error = null 
}) => {
  // Get review process state from store
  const { reviewProcessStarted, startReviewProcess, components, initializeComponents } = useStrategyReviewStore();

  // Initialize components if they don't exist
  useEffect(() => {
    if (components.length === 0) {
      console.log('🔧 StrategyIntelligenceTab: Initializing components');
      const STRATEGY_COMPONENTS = [
        {
          id: 'strategic_insights',
          title: 'Strategic Insights',
          subtitle: 'AI-powered market analysis'
        },
        {
          id: 'competitive_analysis',
          title: 'Competitive Analysis',
          subtitle: 'Market positioning insights'
        },
        {
          id: 'performance_predictions',
          title: 'Performance Predictions',
          subtitle: 'ROI and success metrics'
        },
        {
          id: 'implementation_roadmap',
          title: 'Implementation Roadmap',
          subtitle: 'Project timeline and phases'
        },
        {
          id: 'risk_assessment',
          title: 'Risk Assessment',
          subtitle: 'Risk analysis and mitigation'
        }
      ];
      initializeComponents(STRATEGY_COMPONENTS);
    }
  }, [components.length, initializeComponents]);

  const handleStartReviewProcess = () => {
    startReviewProcess();
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!strategyData) {
    return (
      <Box sx={{ textAlign: 'center', p: 4 }}>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          No Strategy Data Available
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Generate a comprehensive strategy first to view strategic intelligence.
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header Section */}
      <StrategyHeader 
        strategyData={strategyData} 
        strategyConfirmed={false}
        onStartReview={handleStartReviewProcess}
      />

      {/* Review Progress Header - Only shown when review process is started */}
      {reviewProcessStarted && <ReviewProgressHeader strategyData={strategyData} />}

      {/* Strategy Intelligence Cards */}
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            sm: '1fr',
            md: 'repeat(2, 1fr)',
            lg: 'repeat(2, 1fr)',
            xl: 'repeat(3, 1fr)'
          },
          gridAutoRows: 'minmax(min-content, auto)',
          gap: 3,
          position: 'relative',
          minHeight: '400px',
          padding: 2,
          '& > *': {
            minHeight: 'fit-content',
            position: 'relative',
            zIndex: 1,
            transition: 'z-index 0.3s ease, transform 0.3s ease',
          },
          '& > *:hover': {
            zIndex: 10,
          }
        }}
      >
        <StrategicInsightsCard strategyData={strategyData} />
        <CompetitiveAnalysisCard strategyData={strategyData} />
        <PerformancePredictionsCard strategyData={strategyData} />
        <ImplementationRoadmapCard strategyData={strategyData} />
        <RiskAssessmentCard strategyData={strategyData} />
      </Box>
    </Box>
  );
};

export default StrategyIntelligenceTab; 