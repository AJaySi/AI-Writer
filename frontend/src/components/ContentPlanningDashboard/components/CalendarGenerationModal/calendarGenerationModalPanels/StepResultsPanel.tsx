import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Chip,
  Card
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';

// Import styles
import {
  stepResultsCardStyles,
  stepResultsHeaderStyles,
  stepResultsContentStyles
} from '../CalendarGenerationModal.styles';

// Types
interface QualityScores {
  overall: number;
  step1: number;
  step2: number;
  step3: number;
  step4: number;
  step5: number;
  step6: number;
  step7: number;
  step8: number;
  step9: number;
  step10: number;
  step11: number;
  step12: number;
}

interface StepResultsPanelProps {
  stepResults: Record<number, any>;
  qualityScores: QualityScores;
}

const StepResultsPanel: React.FC<StepResultsPanelProps> = ({ stepResults, qualityScores }) => (
  <Paper elevation={1} sx={{ p: 2 }}>
    <Typography variant="h6" gutterBottom>
      Step Results
    </Typography>
    
    {Object.entries(stepResults).map(([stepNumber, results]) => (
      <Box key={stepNumber} mb={3}>
        <Card variant="outlined" sx={stepResultsCardStyles}>
          {/* Step Header */}
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center" gap={2}>
              <Box sx={stepResultsHeaderStyles}>
                {stepNumber}
              </Box>
              <Box>
                <Typography variant="h6">
                  {results.stepName}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Execution Time: {results.executionTime}
                </Typography>
              </Box>
            </Box>
            
            <Box display="flex" alignItems="center" gap={1}>
              <Chip
                label={`${Math.round(results.qualityScore * 100)}%`}
                color={results.qualityScore >= 0.9 ? 'success' : results.qualityScore >= 0.8 ? 'warning' : 'error'}
                size="small"
              />
              <CheckCircleIcon color="success" />
            </Box>
          </Box>

          {/* Data Sources Used */}
          <Box mb={2}>
            <Typography variant="subtitle2" gutterBottom>
              Data Sources Used:
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {results.dataSourcesUsed.map((source: string, index: number) => (
                <Chip
                  key={index}
                  label={source}
                  size="small"
                  variant="outlined"
                  color="primary"
                />
              ))}
            </Box>
          </Box>

          {/* Step Results */}
          <Box mb={2}>
            <Typography variant="subtitle2" gutterBottom>
              Results:
            </Typography>
            <Box sx={stepResultsContentStyles}>
              {Object.entries(results.results).map(([key, value]) => (
                <Box key={key} mb={1}>
                  <Typography variant="body2" fontWeight="bold" color="text.secondary">
                    {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}:
                  </Typography>
                  <Typography variant="body2">
                    {Array.isArray(value) ? value.join(', ') : String(value)}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Box>

          {/* Insights */}
          <Box mb={2}>
            <Typography variant="subtitle2" gutterBottom>
              Key Insights:
            </Typography>
            <Box component="ul" sx={{ pl: 2, m: 0 }}>
              {results.insights.map((insight: string, index: number) => (
                <Box component="li" key={index} mb={0.5}>
                  <Typography variant="body2">
                    {insight}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Box>

          {/* Recommendations */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>
              Recommendations:
            </Typography>
            <Box component="ul" sx={{ pl: 2, m: 0 }}>
              {results.recommendations.map((rec: string, index: number) => (
                <Box component="li" key={index} mb={0.5}>
                  <Typography variant="body2" color="primary">
                    {rec}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Box>
        </Card>
      </Box>
    ))}
  </Paper>
);

export default StepResultsPanel;
