import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Button, 
  TextField, 
  Typography, 
  Alert, 
  CircularProgress,
  Card,
  CardContent,
  CardActions,
  Grid,
  Chip,
  Divider
} from '@mui/material';
import { getApiKeys } from '../../api/onboarding';
import { 
  processResearchTopic,
  processResearchResults,
  validateResearchRequest,
  getResearchProvidersInfo,
  generateResearchReport,
  ResearchTopicRequest
} from '../../api/componentLogic';

const ResearchTestStep: React.FC<{ onContinue: () => void }> = ({ onContinue }) => {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [researchResults, setResearchResults] = useState<any>(null);
  const [providersInfo, setProvidersInfo] = useState<any>(null);
  const [apiKeys, setApiKeys] = useState<Record<string, string>>({});

  useEffect(() => {
    async function loadData() {
      try {
        // Load API keys
        const keys = await getApiKeys();
        setApiKeys(keys);

        // Load providers info
        const providers = await getResearchProvidersInfo();
        setProvidersInfo(providers.providers_info);
      } catch (e) {
        console.error('Failed to load research data:', e);
      }
    }
    loadData();
  }, []);

  const handleResearch = async () => {
    if (!topic.trim()) {
      setError('Please enter a research topic.');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);
    setResearchResults(null);

    try {
      // Validate research request
      const validation = await validateResearchRequest(topic, apiKeys);
      if (!validation.valid) {
        setError(`Research validation failed: ${validation.errors.join(', ')}`);
        if (validation.warnings.length > 0) {
          console.warn('Research warnings:', validation.warnings);
        }
        setLoading(false);
        return;
      }

      // Process research topic
      const request: ResearchTopicRequest = {
        topic: topic.trim(),
        api_keys: apiKeys
      };

      const results = await processResearchTopic(request);
      if (!results.success) {
        setError(`Research failed: ${results.error}`);
        setLoading(false);
        return;
      }

      // Process research results
      const processedResults = await processResearchResults(results);
      if (processedResults.success) {
        setResearchResults(processedResults.processed_results);
        setSuccess('Research completed successfully!');
      } else {
        setError('Failed to process research results.');
      }

    } catch (e) {
      setError('Research failed. Please try again.');
      console.error('Research error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!researchResults) {
      setError('No research results available to generate report.');
      return;
    }

    setLoading(true);
    try {
      const report = await generateResearchReport({ processed_results: researchResults });
      if (report.success) {
        setSuccess('Research report generated successfully!');
        console.log('Generated report:', report.report);
      } else {
        setError('Failed to generate research report.');
      }
    } catch (e) {
      setError('Failed to generate research report.');
      console.error('Report generation error:', e);
    } finally {
      setLoading(false);
    }
  };

  const availableProviders = providersInfo ? Object.keys(providersInfo.providers).filter(
    provider => apiKeys[providersInfo.providers[provider].api_key_name]
  ) : [];

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Test Research Functionality
      </Typography>
      <Typography variant="body2" color="textSecondary" gutterBottom>
        Test the AI research capabilities with your configured settings and API keys.
      </Typography>

      {/* Research Input */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="subtitle1" gutterBottom>
            Research Topic
          </Typography>
          <TextField
            label="Enter a topic to research"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            fullWidth
            multiline
            rows={2}
            placeholder="e.g., 'Latest trends in artificial intelligence'"
            disabled={loading}
          />
          
          {availableProviders.length > 0 && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="caption" color="textSecondary">
                Available providers: {availableProviders.map(provider => (
                  <Chip key={provider} label={provider} size="small" sx={{ mr: 0.5 }} />
                ))}
              </Typography>
            </Box>
          )}
        </CardContent>
        <CardActions>
          <Button 
            variant="contained" 
            onClick={handleResearch}
            disabled={loading || !topic.trim()}
          >
            {loading ? 'Researching...' : 'Start Research'}
          </Button>
        </CardActions>
      </Card>

      {/* Research Results */}
      {researchResults && (
        <Card sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>
              Research Results
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Topic:</strong> {researchResults.topic}
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Summary:</strong>
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  {researchResults.summary}
                </Typography>
              </Grid>

              {researchResults.key_insights && researchResults.key_insights.length > 0 && (
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="textSecondary">
                    <strong>Key Insights:</strong>
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    {researchResults.key_insights.map((insight: string, index: number) => (
                      <Chip 
                        key={index} 
                        label={insight} 
                        size="small" 
                        sx={{ mr: 0.5, mb: 0.5 }} 
                      />
                    ))}
                  </Box>
                </Grid>
              )}

              {researchResults.trends && researchResults.trends.length > 0 && (
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="textSecondary">
                    <strong>Trends:</strong>
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    {researchResults.trends.map((trend: string, index: number) => (
                      <Chip 
                        key={index} 
                        label={trend} 
                        size="small" 
                        variant="outlined"
                        sx={{ mr: 0.5, mb: 0.5 }} 
                      />
                    ))}
                  </Box>
                </Grid>
              )}

              {researchResults.metadata && (
                <Grid item xs={12}>
                  <Divider sx={{ my: 1 }} />
                  <Typography variant="caption" color="textSecondary">
                    <strong>Research Details:</strong> 
                    Confidence: {Math.round((researchResults.metadata.confidence_score || 0) * 100)}% | 
                    Depth: {researchResults.metadata.research_depth} | 
                    Providers: {researchResults.metadata.providers_used?.join(', ')}
                  </Typography>
                </Grid>
              )}
            </Grid>
          </CardContent>
          <CardActions>
            <Button 
              variant="outlined" 
              onClick={handleGenerateReport}
              disabled={loading}
            >
              Generate Report
            </Button>
          </CardActions>
        </Card>
      )}

      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
      
      <Button
        variant="contained"
        color="primary"
        onClick={onContinue}
        sx={{ mt: 2 }}
      >
        Continue to Next Step
      </Button>
    </Box>
  );
};

export default ResearchTestStep; 