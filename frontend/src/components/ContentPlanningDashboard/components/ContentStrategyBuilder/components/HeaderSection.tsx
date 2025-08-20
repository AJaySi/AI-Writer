import React, { useState, useEffect } from 'react';
import {
  Paper,
  Box,
  Typography,
  Button,
  Chip,
  Alert,
  Collapse,
  Tooltip,
  Grid,
  LinearProgress
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Refresh as RefreshIcon,
  PlayArrow as PlayArrowIcon,
  Schedule as ScheduleIcon,
  Info as InfoIcon,
  ArrowDownward as ArrowDownwardIcon,
  Visibility as VisibilityIcon,
  DataUsage as DataUsageIcon,
  TrendingUp as TrendingUpIcon,
  Security as SecurityIcon,
  AutoAwesome as AutoAwesomeIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import AutofillDataTransparency from './AutofillDataTransparency';

interface HeaderSectionProps {
  autoPopulatedFields: any;
  dataSources: any;
  inputDataPoints: any;
  personalizationData: any;
  confidenceScores: any;
  loading: boolean;
  error: string | null;
  onRefreshAutofill: () => void;
  onContinueWithPresent: () => void;
  onScrollToReview: () => void;
  hasAutofillData: boolean;
  lastAutofillTime?: string;
  dataSource?: string;
}

const HeaderSection: React.FC<HeaderSectionProps> = ({
  autoPopulatedFields,
  dataSources,
  inputDataPoints,
  personalizationData,
  confidenceScores,
  loading,
  error,
  onRefreshAutofill,
  onContinueWithPresent,
  onScrollToReview,
  hasAutofillData,
  lastAutofillTime,
  dataSource
}) => {
  const [showTransparencyModal, setShowTransparencyModal] = useState(false);
  const [showDataInfo, setShowDataInfo] = useState(false);
  const [showNextButton, setShowNextButton] = useState(false);

  // Show next button when autofill is complete
  useEffect(() => {
    if (hasAutofillData && Object.keys(autoPopulatedFields).length > 0) {
      setShowNextButton(true);
    }
  }, [hasAutofillData, autoPopulatedFields]);

  // Determine cache status and show appropriate buttons
  const getCacheStatus = () => {
    if (hasAutofillData && Object.keys(autoPopulatedFields).length > 0) {
      return 'cached';
    } else if (Object.keys(inputDataPoints).length > 0) {
      return 'partial';
    } else {
      return 'empty';
    }
  };

  const cacheStatus = getCacheStatus();

  const formatTimeAgo = (timestamp: string) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInMinutes = Math.floor((now.getTime() - time.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)} hours ago`;
    return `${Math.floor(diffInMinutes / 1440)} days ago`;
  };

  // Calculate data quality score
  const getDataQualityScore = () => {
    const scores = Object.values(confidenceScores).filter((score): score is number => typeof score === 'number');
    if (scores.length === 0) return 0;
    return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
  };

  // Get field count by category
  const getFieldCountByCategory = () => {
    const categories: Record<string, number> = {};
    Object.keys(autoPopulatedFields).forEach(fieldId => {
      const category = fieldId.split('_')[0] || 'other';
      categories[category] = (categories[category] || 0) + 1;
    });
    return categories;
  };

  const dataQualityScore = getDataQualityScore();
  const fieldCountByCategory = getFieldCountByCategory();

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Paper 
        sx={{ 
          p: 2.5,
          mb: 3, 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
          color: 'white',
          borderRadius: 3,
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%)',
            animation: 'shimmer 3s ease-in-out infinite',
          },
          boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3), 0 0 0 1px rgba(255,255,255,0.1)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255,255,255,0.2)',
        }}
      >
        <Box sx={{ position: 'relative', zIndex: 1 }}>
          {/* Main Header */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Box sx={{ flex: 1 }}>
              <Typography 
                variant="h4"
                gutterBottom 
                sx={{ 
                  fontWeight: 'bold',
                  background: 'linear-gradient(45deg, #fff, #f0f0f0)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  textShadow: '0 0 20px rgba(255,255,255,0.5)',
                  mb: 1
                }}
              >
                AI Content Strategy Co-pilot
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.9, fontSize: '0.9rem' }}>
                Build a comprehensive content strategy with 30+ strategic inputs
              </Typography>
            </Box>
          </Box>
          
          {/* Enhanced Data Status Grid */}
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {/* Auto-populated Fields Count */}
            <Grid item xs={6} sm={3}>
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                p: 1.5,
                borderRadius: 2,
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                backdropFilter: 'blur(10px)'
              }}>
                <DataUsageIcon sx={{ fontSize: 20, color: 'rgba(255, 255, 255, 0.8)' }} />
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}>
                    {Object.keys(autoPopulatedFields).length}
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8, fontSize: '0.7rem' }}>
                    Fields Auto-populated
                  </Typography>
                </Box>
              </Box>
            </Grid>

            {/* Data Quality Score */}
            <Grid item xs={6} sm={3}>
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                p: 1.5,
                borderRadius: 2,
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                backdropFilter: 'blur(10px)'
              }}>
                <TrendingUpIcon sx={{ fontSize: 20, color: 'rgba(255, 255, 255, 0.8)' }} />
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}>
                    {dataQualityScore}%
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8, fontSize: '0.7rem' }}>
                    Data Quality
                  </Typography>
                </Box>
              </Box>
            </Grid>

            {/* Last Updated */}
            <Grid item xs={6} sm={3}>
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                p: 1.5,
                borderRadius: 2,
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                backdropFilter: 'blur(10px)'
              }}>
                <ScheduleIcon sx={{ fontSize: 20, color: 'rgba(255, 255, 255, 0.8)' }} />
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}>
                    {lastAutofillTime ? formatTimeAgo(lastAutofillTime).split(' ')[0] : 'N/A'}
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8, fontSize: '0.7rem' }}>
                    Last Updated
                  </Typography>
                </Box>
              </Box>
            </Grid>

            {/* Data Sources */}
            <Grid item xs={6} sm={3}>
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                p: 1.5,
                borderRadius: 2,
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                backdropFilter: 'blur(10px)'
              }}>
                <SecurityIcon sx={{ fontSize: 20, color: 'rgba(255, 255, 255, 0.8)' }} />
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}>
                    {Object.keys(dataSources).length}
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8, fontSize: '0.7rem' }}>
                    Data Sources
                  </Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>

          {/* Data Quality Progress Bar */}
          {dataQualityScore > 0 && (
            <Box sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                <Typography variant="body2" sx={{ opacity: 0.9, fontSize: '0.8rem' }}>
                  Data Quality Score
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9, fontSize: '0.8rem', fontWeight: 'bold' }}>
                  {dataQualityScore}%
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={dataQualityScore} 
                sx={{
                  height: 6,
                  borderRadius: 3,
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    background: dataQualityScore >= 80 
                      ? 'linear-gradient(90deg, #4caf50, #66bb6a)' 
                      : dataQualityScore >= 60 
                      ? 'linear-gradient(90deg, #ff9800, #ffb74d)' 
                      : 'linear-gradient(90deg, #f44336, #ef5350)',
                    borderRadius: 3
                  }
                }}
              />
            </Box>
          )}
            
          {/* Enhanced Status Chips */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 2, flexWrap: 'wrap' }}>
            {cacheStatus === 'cached' && (
              <Chip
                icon={<CheckCircleIcon />}
                label={`${Object.keys(autoPopulatedFields).length} fields auto-populated`}
                sx={{
                  backgroundColor: 'rgba(76, 175, 80, 0.2)',
                  color: 'white',
                  border: '1px solid rgba(76, 175, 80, 0.3)',
                  '& .MuiChip-icon': { color: 'rgba(76, 175, 80, 0.8)' },
                  fontWeight: 500,
                  fontSize: '0.8rem'
                }}
              />
            )}
            
            {dataSource && (
              <Tooltip title="Click to view data source information">
                <Chip
                  icon={<InfoIcon />}
                  label={`Source: ${dataSource}`}
                  onClick={() => setShowDataInfo(!showDataInfo)}
                  sx={{
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    color: 'white',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    cursor: 'pointer',
                    fontWeight: 500,
                    fontSize: '0.8rem',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.2)'
                    }
                  }}
                />
              </Tooltip>
            )}

            {/* Category Distribution Chips */}
            {Object.keys(fieldCountByCategory).length > 0 && (
              <Chip
                icon={<AutoAwesomeIcon />}
                label={`${Object.keys(fieldCountByCategory).length} categories`}
                sx={{
                  backgroundColor: 'rgba(156, 39, 176, 0.2)',
                  color: 'white',
                  border: '1px solid rgba(156, 39, 176, 0.3)',
                  '& .MuiChip-icon': { color: 'rgba(156, 39, 176, 0.8)' },
                  fontWeight: 500,
                  fontSize: '0.8rem'
                }}
              />
            )}
          </Box>

          {/* Data Source Information */}
          <Collapse in={showDataInfo}>
            <Alert 
              severity="info" 
              sx={{ 
                mb: 2, 
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                color: 'white',
                '& .MuiAlert-icon': { color: 'rgba(255, 255, 255, 0.8)' }
              }}
            >
              <Typography variant="body2" sx={{ mb: 1 }}>
                <strong>Data Source:</strong> {dataSource || 'Onboarding Database'}
              </Typography>
              <Typography variant="body2" sx={{ mb: 1 }}>
                <strong>Input Data Points:</strong> {Object.keys(inputDataPoints).length} available
              </Typography>
              <Typography variant="body2">
                <strong>Adaptive Monitoring:</strong> ALwrity continuously monitors databases for new data points to ensure you have the latest information.
              </Typography>
            </Alert>
          </Collapse>

          {/* Conditional Action Buttons */}
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            {cacheStatus === 'cached' ? (
              // Case 1: Data exists in cache - show refresh vs continue options
              <>
                <Tooltip title="Refresh with latest database data and AI analysis">
                  <Button
                    variant="outlined"
                    startIcon={<RefreshIcon />}
                    onClick={onRefreshAutofill}
                    disabled={loading}
                    sx={{
                      color: 'white',
                      borderColor: 'rgba(255, 255, 255, 0.3)',
                      '&:hover': {
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)'
                      }
                    }}
                  >
                    {loading ? 'Refreshing...' : 'Refresh & Autofill Inputs'}
                  </Button>
                </Tooltip>
                
                <Tooltip title="Continue with current autofilled values">
                  <Button
                    variant="contained"
                    startIcon={<PlayArrowIcon />}
                    onClick={onContinueWithPresent}
                    sx={{
                      backgroundColor: 'rgba(255, 255, 255, 0.2)',
                      color: 'white',
                      '&:hover': {
                        backgroundColor: 'rgba(255, 255, 255, 0.3)'
                      }
                    }}
                  >
                    Continue with Present Values
                  </Button>
                </Tooltip>
              </>
            ) : cacheStatus === 'partial' ? (
              // Case 2: Partial data - show refresh option
              <Tooltip title="Refresh with latest database data and AI analysis">
                <Button
                  variant="contained"
                  startIcon={<RefreshIcon />}
                  onClick={onRefreshAutofill}
                  disabled={loading}
                  sx={{
                    backgroundColor: 'rgba(255, 193, 7, 0.8)',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 193, 7, 0.9)'
                    }
                  }}
                >
                  {loading ? 'Refreshing...' : 'Refresh & Autofill Strategy Inputs'}
                </Button>
              </Tooltip>
            ) : (
              // Case 3: No data - show initial autofill
              <Tooltip title="Fetch latest data from database and autofill strategy inputs">
                <Button
                  variant="contained"
                  startIcon={<RefreshIcon />}
                  onClick={onRefreshAutofill}
                  disabled={loading}
                  sx={{
                    backgroundColor: 'rgba(76, 175, 80, 0.8)',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: 'rgba(76, 175, 80, 0.9)'
                    }
                  }}
                >
                  {loading ? 'Autofilling...' : 'Refresh & Autofill Strategy Inputs'}
                </Button>
              </Tooltip>
            )}

            {/* Next Step Button - shown after autofill completion */}
            {showNextButton && (
              <Tooltip title="Scroll to review section and mark inputs as reviewed">
                <Button
                  variant="contained"
                  startIcon={<ArrowDownwardIcon />}
                  onClick={onScrollToReview}
                  sx={{
                    background: 'linear-gradient(135deg, #4caf50 0%, #66bb6a 50%, #81c784 100%)',
                    color: 'white',
                    fontWeight: 600,
                    '&:hover': {
                      background: 'linear-gradient(135deg, #66bb6a 0%, #81c784 50%, #a5d6a7 100%)',
                      transform: 'translateY(-1px)'
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  Next: Review Strategy Inputs & Create Strategy
                </Button>
              </Tooltip>
            )}

            {/* Know More Details Button - shown when autofill data exists */}
            {hasAutofillData && Object.keys(autoPopulatedFields).length > 0 && (
              <Tooltip title="View detailed information about autofill data sources and AI analysis">
                <Button
                  variant="text"
                  startIcon={<VisibilityIcon />}
                  onClick={() => setShowTransparencyModal(true)}
                  sx={{
                    color: 'rgba(255, 255, 255, 0.8)',
                    '&:hover': {
                      color: 'white',
                      backgroundColor: 'rgba(255, 255, 255, 0.1)'
                    }
                  }}
                >
                  Know More Details
                </Button>
              </Tooltip>
            )}
          </Box>
        </Box>
      </Paper>

      {/* Autofill Data Transparency Modal */}
      <AutofillDataTransparency
        open={showTransparencyModal}
        onClose={() => setShowTransparencyModal(false)}
        autoPopulatedFields={autoPopulatedFields}
        dataSources={dataSources}
        inputDataPoints={inputDataPoints}
        personalizationData={personalizationData}
        confidenceScores={confidenceScores}
        lastAutofillTime={lastAutofillTime}
        dataSource={dataSource}
      />
    </motion.div>
  );
};

export default HeaderSection; 