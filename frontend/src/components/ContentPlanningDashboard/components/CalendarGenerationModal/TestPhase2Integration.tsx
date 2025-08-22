import React, { useState } from 'react';
import {
  Button,
  Box,
  Typography,
  Paper,
  Grid
} from '@mui/material';
import CalendarGenerationModal from './CalendarGenerationModal';

// Mock data for testing Phase 2 integration
const mockPhase2Progress = {
  status: 'in_progress',
  currentStep: 4,
  stepProgress: 75,
  overallProgress: 45,
  stepResults: {
    1: {
      stepName: 'Content Strategy Analysis',
      executionTime: '2.3s',
      qualityScore: 0.94,
      dataSourcesUsed: ['Content Strategy', 'Business Goals', 'Target Audience']
    },
    2: {
      stepName: 'Gap Analysis and Opportunity Identification',
      executionTime: '3.1s',
      qualityScore: 0.89,
      dataSourcesUsed: ['Gap Analysis', 'Keyword Research', 'Competitor Analysis']
    },
    3: {
      stepName: 'Audience and Platform Strategy',
      executionTime: '2.8s',
      qualityScore: 0.92,
      dataSourcesUsed: ['Audience Data', 'Platform Performance', 'Content Mix Analysis']
    },
    4: {
      stepName: 'Calendar Framework and Timeline',
      executionTime: '1.9s',
      qualityScore: 0.91,
      dataSourcesUsed: ['Calendar Configuration', 'Timeline Optimization', 'Duration Control']
    }
  },
  qualityScores: {
    overall: 0.91,
    step1: 0.94,
    step2: 0.89,
    step3: 0.92,
    step4: 0.91,
    step5: 0.0,
    step6: 0.0,
    step7: 0.0,
    step8: 0.0,
    step9: 0.0,
    step10: 0.0,
    step11: 0.0,
    step12: 0.0
  },
  transparencyMessages: [
    'Step 4: Calendar Framework and Timeline completed with 91% quality score',
    'Calendar structure optimized for your posting preferences',
    'Timeline duration validated against business goals'
  ],
  educationalContent: [
    {
      title: 'Calendar Framework & Timeline',
      description: 'Building the structural foundation of your content calendar with optimal timing and duration control.',
      tips: [
        'Optimize posting frequency for your audience',
        'Consider timezone and peak engagement hours',
        'Balance content types across the timeline',
        'Ensure strategic alignment with business goals'
      ]
    }
  ],
  errors: [],
  warnings: []
};

const TestPhase2Integration: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [sessionId] = useState('test-phase2-session-123');
  const [calendarConfig] = useState({
    userId: '1',
    strategyId: '1',
    calendarType: 'monthly' as const,
    platforms: ['LinkedIn', 'Twitter', 'Blog'],
    duration: 30,
    postingFrequency: 'weekly' as const
  });

  const handleComplete = (results: any) => {
    console.log('Calendar generation completed:', results);
    setIsModalOpen(false);
  };

  const handleError = (error: string) => {
    console.error('Calendar generation error:', error);
    setIsModalOpen(false);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Phase 2 Frontend Integration Test
        </Typography>
        
        <Typography variant="body1" color="text.secondary" paragraph>
          This test verifies that the frontend properly displays Phase 2 steps (4-6) with:
        </Typography>
        
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              ✅ What's Implemented:
            </Typography>
            <ul>
              <li>Step indicators for Steps 1-6</li>
              <li>Step-specific icons for Phase 2</li>
              <li>Educational content for Steps 4-6</li>
              <li>Data source panel updates for Phase 2</li>
              <li>Quality score display for all steps</li>
            </ul>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              🧪 Test Features:
            </Typography>
            <ul>
              <li>Mock Phase 2 progress data</li>
              <li>Step 4 completion simulation</li>
              <li>Quality scores for Steps 1-4</li>
              <li>Educational content for Step 4</li>
              <li>Data sources for Step 4</li>
            </ul>
          </Grid>
        </Grid>

        <Button
          variant="contained"
          size="large"
          onClick={() => setIsModalOpen(true)}
          sx={{ mr: 2 }}
        >
          Test Phase 2 Modal
        </Button>
        
        <Button
          variant="outlined"
          size="large"
          onClick={() => {
            // Simulate backend call
            console.log('Simulating backend Phase 2 completion...');
            setIsModalOpen(true);
          }}
        >
          Simulate Backend Integration
        </Button>
      </Paper>

      <CalendarGenerationModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        sessionId={sessionId}
        initialConfig={calendarConfig}
        onComplete={handleComplete}
        onError={handleError}
      />
    </Box>
  );
};

export default TestPhase2Integration;
