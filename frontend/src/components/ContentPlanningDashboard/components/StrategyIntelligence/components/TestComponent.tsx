import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { StrategyData } from '../types/strategy.types';

interface TestComponentProps {
  strategyData: StrategyData | null;
}

const TestComponent: React.FC<TestComponentProps> = ({ strategyData }) => {
  if (!strategyData) return null;

  return (
    <Paper sx={{ p: 2, mb: 2, background: 'rgba(76, 175, 80, 0.1)' }}>
      <Typography variant="h6" color="success.main" gutterBottom>
        ✅ Modular Structure Test
      </Typography>
      <Typography variant="body2">
        Strategy Name: {strategyData.strategy_metadata?.strategy_name || strategyData.metadata?.strategy_name}
      </Typography>
      <Typography variant="body2">
        ROI: {strategyData.summary?.estimated_roi}
      </Typography>
      <Typography variant="body2">
        Success Probability: {strategyData.summary?.success_probability}
      </Typography>
      <Typography variant="body2" color="success.main">
        ✅ Modular structure is working correctly!
      </Typography>
    </Paper>
  );
};

export default TestComponent; 