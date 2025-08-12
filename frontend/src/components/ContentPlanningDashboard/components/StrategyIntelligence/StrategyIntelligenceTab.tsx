import React from 'react';
import { Box, CircularProgress, Alert, Typography, Grid } from '@mui/material';
import { useStrategyData } from './hooks/useStrategyData';
import { useStrategyActions } from './hooks/useStrategyActions';
import StrategyHeader from './components/StrategyHeader';
import StrategicInsightsCard from './components/StrategicInsightsCard';
import CompetitiveAnalysisCard from './components/CompetitiveAnalysisCard';
import PerformancePredictionsCard from './components/PerformancePredictionsCard';
import ImplementationRoadmapCard from './components/ImplementationRoadmapCard';
import RiskAssessmentCard from './components/RiskAssessmentCard';
import StrategyActions from './components/StrategyActions';
import ConfirmationDialog from './components/ConfirmationDialog';

const StrategyIntelligenceTab: React.FC = () => {
  const { strategyData, loading, error, loadStrategyData } = useStrategyData();
  const { 
    strategyConfirmed, 
    showConfirmDialog, 
    setShowConfirmDialog, 
    handleConfirmStrategy, 
    confirmStrategy, 
    handleGenerateContentCalendar 
  } = useStrategyActions();

  const handleConfirmStrategyClick = () => {
    handleConfirmStrategy();
  };

  const handleConfirmStrategyAction = async () => {
    await confirmStrategy(strategyData);
  };

  const handleGenerateContentCalendarAction = async () => {
    try {
      await handleGenerateContentCalendar(strategyData);
    } catch (error) {
      console.error('Error generating content calendar:', error);
    }
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
      <StrategyHeader strategyData={strategyData} strategyConfirmed={strategyConfirmed} />

      {/* Strategy Components Grid */}
      <Grid container spacing={2}>
        <StrategicInsightsCard strategyData={strategyData} />
        <CompetitiveAnalysisCard strategyData={strategyData} />
        <PerformancePredictionsCard strategyData={strategyData} />
        <ImplementationRoadmapCard strategyData={strategyData} />
        <RiskAssessmentCard strategyData={strategyData} />
      </Grid>

      {/* Action Buttons */}
      <StrategyActions
        strategyData={strategyData}
        strategyConfirmed={strategyConfirmed}
        onConfirmStrategy={handleConfirmStrategyClick}
        onGenerateContentCalendar={handleGenerateContentCalendarAction}
        onRefreshData={loadStrategyData}
      />

      {/* Confirmation Dialog */}
      <ConfirmationDialog
        open={showConfirmDialog}
        onClose={() => setShowConfirmDialog(false)}
        onConfirm={handleConfirmStrategyAction}
      />
    </Box>
  );
};

export default StrategyIntelligenceTab; 