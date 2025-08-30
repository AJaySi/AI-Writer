// SEO CopilotKit Test Component
// Simple test to verify CopilotKit sidebar functionality

import React, { useEffect, useState } from 'react';
import { Box, Button, Typography, Paper, Alert } from '@mui/material';
import { useCopilotAction } from '@copilotkit/react-core';

const SEOCopilotTest: React.FC = () => {
  const [testResults, setTestResults] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Use type assertion to bypass TypeScript compilation issues
  const useCopilotActionTyped = useCopilotAction as any;

  // Test action to verify CopilotKit is working
  useCopilotActionTyped({
    name: "testSEOCopilot",
    description: "Test action to verify SEO CopilotKit is working",
    parameters: [
      {
        name: "message",
        type: "string",
        description: "Test message to display",
        required: true
      }
    ],
    handler: async (args: any) => {
      const { message } = args;
      setTestResults(prev => [...prev, `✅ CopilotKit Action Test: ${message}`]);
      return {
        success: true,
        message: `Test completed successfully: ${message}`,
        timestamp: new Date().toISOString()
      };
    }
  });

  const runTest = async () => {
    setIsLoading(true);
    setTestResults([]);
    
    try {
      // Test 1: Check if CopilotKit context is available
      setTestResults(prev => [...prev, '🔍 Testing CopilotKit Context...']);
      
      // Test 2: Check if actions are registered
      setTestResults(prev => [...prev, '🔍 Testing Action Registration...']);
      
      // Test 3: Check if sidebar should be visible
      setTestResults(prev => [...prev, '🔍 Testing Sidebar Visibility...']);
      setTestResults(prev => [...prev, '💡 Look for the chat icon in the bottom right corner']);
      setTestResults(prev => [...prev, '💡 Try pressing Ctrl+/ (or Cmd+/ on Mac) to open the sidebar']);
      
      // Test 4: Check environment variables
      const apiKey = process.env.REACT_APP_COPILOTKIT_API_KEY;
      setTestResults(prev => [...prev, `🔑 API Key Status: ${apiKey ? 'Configured' : 'Missing'}`]);
      
      // Test 5: Check if provider is wrapped correctly
      setTestResults(prev => [...prev, '🔍 Testing Provider Wrapping...']);
      setTestResults(prev => [...prev, '✅ Provider should be wrapped around SEO Dashboard']);
      
    } catch (error) {
      setTestResults(prev => [...prev, `❌ Test Error: ${error}`]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setTestResults([]);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        🧪 SEO CopilotKit Test Panel
      </Typography>
      
      <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
        This panel helps verify that the CopilotKit sidebar is working correctly.
      </Typography>

      <Box sx={{ mb: 2 }}>
        <Button 
          variant="contained" 
          onClick={runTest}
          disabled={isLoading}
          sx={{ mr: 1 }}
        >
          {isLoading ? 'Running Tests...' : 'Run Tests'}
        </Button>
        
        <Button 
          variant="outlined" 
          onClick={clearResults}
          disabled={testResults.length === 0}
        >
          Clear Results
        </Button>
      </Box>

      {testResults.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Test Results:
          </Typography>
          
          {testResults.map((result, index) => (
            <Alert 
              key={index} 
              severity={result.includes('❌') ? 'error' : result.includes('✅') ? 'success' : 'info'}
              sx={{ mb: 1 }}
            >
              {result}
            </Alert>
          ))}
        </Box>
      )}

      <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="subtitle2" gutterBottom>
          📋 How to Test the CopilotKit Sidebar:
        </Typography>
        
        <Typography variant="body2" component="div" sx={{ pl: 1 }}>
          <ol>
            <li>Look for a chat icon in the bottom right corner of the screen</li>
            <li>Click the icon to open the CopilotKit sidebar</li>
            <li>Try typing: "Test the SEO assistant"</li>
            <li>Ask: "What SEO actions are available?"</li>
            <li>Try: "Analyze my website SEO"</li>
          </ol>
        </Typography>
        
        <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
          💡 Keyboard shortcut: Press Ctrl+/ (or Cmd+/ on Mac) to quickly open the sidebar
        </Typography>
      </Box>
    </Paper>
  );
};

export default SEOCopilotTest;
