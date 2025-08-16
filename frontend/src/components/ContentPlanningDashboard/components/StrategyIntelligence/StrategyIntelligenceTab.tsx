import React, { useState } from 'react';
import { Box, CircularProgress, Alert, Typography } from '@mui/material';
import { useStrategyData } from './hooks/useStrategyData';
import StrategyHeader from './components/StrategyHeader';
import StrategicInsightsCard from './components/StrategicInsightsCard';
import CompetitiveAnalysisCard from './components/CompetitiveAnalysisCard';
import PerformancePredictionsCard from './components/PerformancePredictionsCard';
import ImplementationRoadmapCard from './components/ImplementationRoadmapCard';
import RiskAssessmentCard from './components/RiskAssessmentCard';
import ReviewProgressHeader from './components/ReviewProgressHeader';

const StrategyIntelligenceTab: React.FC = () => {
  const { strategyData, loading, error } = useStrategyData();
  
  // State to control review progress visibility
  const [showReviewProgress, setShowReviewProgress] = useState(false);

  const handleStartReviewProcess = () => {
    setShowReviewProgress(true);
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
      {showReviewProgress && <ReviewProgressHeader />}

      {/* Strategy Components Grid */}
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

      {/* Action Buttons - Removed, functionality moved to "Confirm & Activate Strategy" button in ReviewProgressHeader */}

      {/* Confirmation Dialog - Removed, functionality moved to "Confirm & Activate Strategy" button */}
    </Box>
  );
};

export default StrategyIntelligenceTab; 