import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button
} from '@mui/material';
import {
  Search as SearchIcon
} from '@mui/icons-material';
import { useContentPlanningStore } from '../../../stores/contentPlanningStore';
import { contentPlanningApi } from '../../../services/contentPlanningApi';

const KeywordResearchTab: React.FC = () => {
  const [keywordResearch, setKeywordResearch] = useState<any>(null);
  const [dataLoading, setDataLoading] = useState(false);

  useEffect(() => {
    loadKeywordResearch();
  }, []);

  const loadKeywordResearch = async () => {
    try {
      setDataLoading(true);
      const eventSource = await contentPlanningApi.streamKeywordResearch();
      
      contentPlanningApi.handleSSEData(
        eventSource,
        (data) => {
          console.log('Keyword Research SSE Data:', data);
          if (data.type === 'result' && data.data) {
            setKeywordResearch(data.data);
          }
        },
        (error) => {
          console.error('Keyword Research SSE Error:', error);
        },
        () => {
          setDataLoading(false);
        }
      );
    } catch (error) {
      console.error('Error loading keyword research:', error);
      setDataLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Keyword Research
      </Typography>

      {dataLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : keywordResearch && keywordResearch.trend_analysis ? (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  High Volume Keywords
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Keyword</TableCell>
                        <TableCell>Volume</TableCell>
                        <TableCell>Difficulty</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(keywordResearch.trend_analysis.high_volume_keywords || []).map((keyword: any, index: number) => (
                        <TableRow key={index}>
                          <TableCell>{keyword.keyword}</TableCell>
                          <TableCell>{keyword.volume}</TableCell>
                          <TableCell>
                            <Chip 
                              label={keyword.difficulty} 
                              color={keyword.difficulty === 'Low' ? 'success' : keyword.difficulty === 'Medium' ? 'warning' : 'error'}
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Trending Keywords
                </Typography>
                {(keywordResearch.trend_analysis.trending_keywords || []).map((keyword: any, index: number) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Typography variant="subtitle1">
                      {keyword.keyword}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Chip 
                        label={keyword.growth} 
                        color="success"
                        size="small"
                      />
                      <Chip 
                        label={keyword.opportunity} 
                        color={keyword.opportunity === 'High' ? 'success' : 'primary'}
                        size="small"
                      />
                    </Box>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Keyword Opportunities
                </Typography>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Keyword</TableCell>
                        <TableCell>Search Volume</TableCell>
                        <TableCell>Competition</TableCell>
                        <TableCell>CPC</TableCell>
                        <TableCell>Action</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(keywordResearch.opportunities || []).map((opportunity: any, index: number) => (
                        <TableRow key={index}>
                          <TableCell>{opportunity.keyword}</TableCell>
                          <TableCell>{opportunity.search_volume}</TableCell>
                          <TableCell>
                            <Chip 
                              label={opportunity.competition} 
                              color={opportunity.competition === 'Low' ? 'success' : opportunity.competition === 'Medium' ? 'warning' : 'error'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>${opportunity.cpc}</TableCell>
                          <TableCell>
                            <Button size="small" variant="outlined">
                              Add to Strategy
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      ) : (
        <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', p: 3 }}>
          No keyword research data available
        </Typography>
      )}
    </Box>
  );
};

export default KeywordResearchTab; 