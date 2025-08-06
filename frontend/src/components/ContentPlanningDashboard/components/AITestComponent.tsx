import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
  CircularProgress
} from '@mui/material';
import { contentPlanningApi } from '../../../services/contentPlanningApi';

const AITestComponent: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const testAIConnection = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await contentPlanningApi.getAIAnalyticsSafe();
      setResult(response);
      console.log('AI Test Response:', response);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to AI service');
      console.error('AI Test Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 2, m: 2 }}>
      <Typography variant="h6" gutterBottom>
        AI Integration Test
      </Typography>
      
      <Button
        variant="contained"
        onClick={testAIConnection}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? <CircularProgress size={20} /> : 'Test AI Connection'}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {result && (
        <Box>
          <Typography variant="subtitle2" gutterBottom>
            AI Test Results:
          </Typography>
          <pre style={{ fontSize: '12px', overflow: 'auto' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </Box>
      )}
    </Paper>
  );
};

export default AITestComponent; 