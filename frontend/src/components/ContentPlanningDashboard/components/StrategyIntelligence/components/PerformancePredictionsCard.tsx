import React from 'react';
import {
  Grid,
  Typography,
  Box,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider
} from '@mui/material';
import {
  ShowChart as ShowChartIcon,
  TrendingUp as TrendingUpIcon,
  Timeline as TimelineIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';
import { StrategyData } from '../types/strategy.types';
import {
  ANALYSIS_CARD_STYLES,
  getSectionStyles,
  getEnhancedChipStyles,
  getListItemStyles
} from '../styles';
import ProgressiveCard from './ProgressiveCard';

interface PerformancePredictionsCardProps {
  strategyData: StrategyData | null;
}

const PerformancePredictionsCard: React.FC<PerformancePredictionsCardProps> = ({ strategyData }) => {
  // Get style objects
  const sectionStyles = getSectionStyles();
  const listItemStyles = getListItemStyles();

  if (!strategyData?.performance_predictions) {
    return (
      <Grid item xs={12} lg={6}>
        <ProgressiveCard
          title="Performance Predictions"
          subtitle="ROI and success metrics"
          icon={<ShowChartIcon sx={{ color: 'white', fontSize: 20 }} />}
          summary={
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <Typography variant="body1" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.secondary }}>
                Performance predictions data not available
              </Typography>
            </Box>
          }
          details={
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <Typography variant="caption" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.secondary }}>
                Available data keys: {strategyData ? Object.keys(strategyData).join(', ') : 'No data'}
              </Typography>
            </Box>
          }
          trigger="hover"
          autoCollapseDelay={3000}
        />
      </Grid>
    );
  }

  // Summary content - always visible
  const summaryContent = (
    <Box>
      {/* ROI Summary */}
      <Box sx={sectionStyles.sectionContainer}>
        <Box sx={{ 
          display: 'flex', 
          flexDirection: { xs: 'column', sm: 'row' },
          alignItems: { xs: 'flex-start', sm: 'center' }, 
          justifyContent: 'space-between', 
          mb: 2,
          gap: 2,
          width: '100%'
        }}>
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            flex: 1,
            minWidth: 0,
            overflow: 'hidden'
          }}>
            <Box sx={{ 
              width: 40, 
              height: 40, 
              borderRadius: '50%', 
              background: `linear-gradient(135deg, ${ANALYSIS_CARD_STYLES.colors.success} 0%, ${ANALYSIS_CARD_STYLES.colors.accent} 100%)`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
              color: 'white',
              fontSize: '1.2rem',
              fontWeight: 600,
              boxShadow: `0 4px 12px ${ANALYSIS_CARD_STYLES.colors.success}30`,
              flexShrink: 0
            }}>
              {strategyData.performance_predictions.roi_predictions?.estimated_roi || '25%'}
            </Box>
            <Box sx={{ 
              minWidth: 0, 
              flex: 1,
              overflow: 'hidden'
            }}>
              <Typography variant="h6" sx={{ 
                color: ANALYSIS_CARD_STYLES.colors.text.primary, 
                fontWeight: 600,
                fontSize: '1rem',
                lineHeight: 1.2,
                mb: 0.5,
                wordBreak: 'break-word'
              }}>
                ROI Predictions
              </Typography>
              <Typography variant="caption" sx={{ 
                color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                fontSize: '0.7rem',
                lineHeight: 1.2,
                wordBreak: 'break-word'
              }}>
                Expected return on investment
              </Typography>
            </Box>
          </Box>
          <Box sx={{ 
            display: 'flex', 
            gap: 1, 
            flexWrap: 'wrap',
            justifyContent: { xs: 'flex-start', sm: 'flex-end' },
            flexShrink: 0
          }}>
            <Chip 
              label={`${(strategyData.performance_predictions as any)?.success_probability || '85%'} Success`}
              size="small"
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.success).chip}
            />
            <Chip 
              label={`${(strategyData.performance_predictions as any)?.implementation_timeline || '6 months'}`}
              size="small"
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.info).chip}
            />
          </Box>
        </Box>
        
        {/* ROI Description - Full width container */}
        <Box sx={{ mt: 2, width: '100%' }}>
          <Typography variant="body2" sx={{ 
            color: ANALYSIS_CARD_STYLES.colors.text.secondary,
            fontSize: '0.8rem',
            lineHeight: 1.5,
            wordBreak: 'break-word',
            textAlign: 'left'
          }}>
            ROI of {strategyData.performance_predictions.roi_predictions?.estimated_roi || '300-350%'} is achievable leveraging the strong cost-per-lead to lifetime-value ratio.
          </Typography>
        </Box>
      </Box>

      {/* Key Metrics Preview */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle2" sx={{ 
          color: ANALYSIS_CARD_STYLES.colors.text.primary, 
          mb: 1.5, 
          fontWeight: 600,
          fontSize: '0.85rem'
        }}>
          Key Metrics Preview
        </Typography>
        <Box sx={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: 1,
          justifyContent: 'flex-start'
        }}>
          <Chip 
            label="Traffic Growth" 
            size="small" 
            icon={<TrendingUpIcon />}
            sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.primary).chip} 
          />
          <Chip 
            label="Engagement" 
            size="small" 
            icon={<AssessmentIcon />}
            sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.secondary).chip} 
          />
          <Chip 
            label="Conversion" 
            size="small" 
            icon={<ShowChartIcon />}
            sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.accent).chip} 
          />
        </Box>
      </Box>
    </Box>
  );

  // Detailed content - shown on expansion
  const detailedContent = (
    <Box>
      {/* ROI Summary */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
          ROI Summary
        </Typography>
        <Box sx={sectionStyles.sectionContainer}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
            <Typography variant="body2" sx={{ 
              color: ANALYSIS_CARD_STYLES.colors.text.secondary, 
              fontSize: '0.85rem',
              lineHeight: 1.5,
              wordBreak: 'break-word'
            }}>
              Estimated ROI: {strategyData.performance_predictions.roi_predictions?.estimated_roi || '25%'}
            </Typography>
            <Typography variant="body2" sx={{ 
              color: ANALYSIS_CARD_STYLES.colors.text.secondary, 
              fontSize: '0.85rem',
              lineHeight: 1.5,
              wordBreak: 'break-word'
            }}>
              Success Probability: {(strategyData.performance_predictions as any)?.success_probability || '85%'}
            </Typography>
            <Typography variant="body2" sx={{ 
              color: ANALYSIS_CARD_STYLES.colors.text.secondary, 
              fontSize: '0.85rem',
              lineHeight: 1.5,
              wordBreak: 'break-word'
            }}>
              Implementation Timeline: {(strategyData.performance_predictions as any)?.implementation_timeline || '6 months'}
            </Typography>
          </Box>
        </Box>
      </Box>

      {/* Key Metrics */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
          Key Metrics
        </Typography>
        <Box sx={sectionStyles.sectionContainer}>
          <Box sx={{ 
            display: 'grid', 
            gridTemplateColumns: { xs: '1fr', sm: 'repeat(auto-fit, minmax(200px, 1fr))' }, 
            gap: 2 
          }}>
            {/* Traffic Predictions */}
            {strategyData.performance_predictions.traffic_predictions && (
              <Box sx={{ 
                p: 2, 
                border: `1px solid ${ANALYSIS_CARD_STYLES.colors.success}`, 
                borderRadius: 2,
                background: `rgba(76, 175, 80, 0.1)`,
                minHeight: 80,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                overflow: 'hidden'
              }}>
                <Typography variant="body2" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.success, 
                  fontWeight: 600, 
                  mb: 1,
                  fontSize: '0.8rem',
                  lineHeight: 1.2,
                  wordBreak: 'break-word'
                }}>
                  Traffic Growth
                </Typography>
                <Typography variant="caption" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                  fontSize: '0.7rem',
                  lineHeight: 1.3,
                  wordBreak: 'break-word'
                }}>
                  {strategyData.performance_predictions.traffic_predictions.growth_rate || '150% increase'}
                </Typography>
              </Box>
            )}

            {/* Engagement Predictions */}
            {strategyData.performance_predictions.engagement_predictions && (
              <Box sx={{ 
                p: 2, 
                border: `1px solid ${ANALYSIS_CARD_STYLES.colors.secondary}`, 
                borderRadius: 2,
                background: `rgba(118, 75, 162, 0.1)`,
                minHeight: 80,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                overflow: 'hidden'
              }}>
                <Typography variant="body2" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.secondary, 
                  fontWeight: 600, 
                  mb: 1,
                  fontSize: '0.8rem',
                  lineHeight: 1.2,
                  wordBreak: 'break-word'
                }}>
                  Engagement Rate
                </Typography>
                <Typography variant="caption" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                  fontSize: '0.7rem',
                  lineHeight: 1.3,
                  wordBreak: 'break-word'
                }}>
                  {strategyData.performance_predictions.engagement_predictions.engagement_rate || '45% improvement'}
                </Typography>
              </Box>
            )}

            {/* Conversion Predictions */}
            {strategyData.performance_predictions.conversion_predictions && (
              <Box sx={{ 
                p: 2, 
                border: `1px solid ${ANALYSIS_CARD_STYLES.colors.accent}`, 
                borderRadius: 2,
                background: `rgba(240, 147, 251, 0.1)`,
                minHeight: 80,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                overflow: 'hidden'
              }}>
                <Typography variant="body2" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.accent, 
                  fontWeight: 600, 
                  mb: 1,
                  fontSize: '0.8rem',
                  lineHeight: 1.2,
                  wordBreak: 'break-word'
                }}>
                  Conversion Rate
                </Typography>
                <Typography variant="caption" sx={{ 
                  color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                  fontSize: '0.7rem',
                  lineHeight: 1.3,
                  wordBreak: 'break-word'
                }}>
                  {strategyData.performance_predictions.conversion_predictions.conversion_rate || '3.2% to 5.8%'}
                </Typography>
              </Box>
            )}
          </Box>
        </Box>
      </Box>

      <Divider sx={{ my: 2, opacity: 0.2, borderColor: ANALYSIS_CARD_STYLES.colors.border.secondary }} />

      {/* Detailed Predictions */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
          Detailed Predictions
        </Typography>
        <Box sx={sectionStyles.sectionContainer}>
          <List dense>
            {/* Traffic Predictions */}
            {strategyData.performance_predictions.traffic_predictions && (
              <ListItem sx={{ ...listItemStyles.listItem, py: 1.5 }}>
                <ListItemIcon sx={listItemStyles.listItemIcon}>
                  <Box sx={{ 
                    width: 6, 
                    height: 6, 
                    borderRadius: '50%', 
                    background: ANALYSIS_CARD_STYLES.colors.success,
                    opacity: 0.7
                  }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Traffic Growth"
                  secondary={`${strategyData.performance_predictions.traffic_predictions.growth_rate || '150% increase'} in organic visitors`}
                  primaryTypographyProps={{ 
                    variant: 'body2', 
                    fontSize: '0.875rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.success, fontWeight: 600, mb: 0.5 }
                  }}
                  secondaryTypographyProps={{ 
                    variant: 'caption', 
                    fontSize: '0.75rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.text.secondary, lineHeight: 1.4 }
                  }}
                />
              </ListItem>
            )}

            {/* Engagement Predictions */}
            {strategyData.performance_predictions.engagement_predictions && (
              <ListItem sx={{ ...listItemStyles.listItem, py: 1.5 }}>
                <ListItemIcon sx={listItemStyles.listItemIcon}>
                  <Box sx={{ 
                    width: 6, 
                    height: 6, 
                    borderRadius: '50%', 
                    background: ANALYSIS_CARD_STYLES.colors.secondary,
                    opacity: 0.7
                  }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Engagement Rate"
                  secondary={`${strategyData.performance_predictions.engagement_predictions.engagement_rate || '45% improvement'} in user interaction`}
                  primaryTypographyProps={{ 
                    variant: 'body2', 
                    fontSize: '0.875rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.secondary, fontWeight: 600, mb: 0.5 }
                  }}
                  secondaryTypographyProps={{ 
                    variant: 'caption', 
                    fontSize: '0.75rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.text.secondary, lineHeight: 1.4 }
                  }}
                />
              </ListItem>
            )}

            {/* Conversion Predictions */}
            {strategyData.performance_predictions.conversion_predictions && (
              <ListItem sx={{ ...listItemStyles.listItem, py: 1.5 }}>
                <ListItemIcon sx={listItemStyles.listItemIcon}>
                  <Box sx={{ 
                    width: 6, 
                    height: 6, 
                    borderRadius: '50%', 
                    background: ANALYSIS_CARD_STYLES.colors.accent,
                    opacity: 0.7
                  }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Conversion Rate"
                  secondary={`${strategyData.performance_predictions.conversion_predictions.conversion_rate || '3.2% to 5.8%'} improvement`}
                  primaryTypographyProps={{ 
                    variant: 'body2', 
                    fontSize: '0.875rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.accent, fontWeight: 600, mb: 0.5 }
                  }}
                  secondaryTypographyProps={{ 
                    variant: 'caption', 
                    fontSize: '0.75rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.text.secondary, lineHeight: 1.4 }
                  }}
                />
              </ListItem>
            )}

            {/* ROI Predictions */}
            {strategyData.performance_predictions.roi_predictions && (
              <ListItem sx={{ ...listItemStyles.listItem, py: 1.5 }}>
                <ListItemIcon sx={listItemStyles.listItemIcon}>
                  <Box sx={{ 
                    width: 6, 
                    height: 6, 
                    borderRadius: '50%', 
                    background: ANALYSIS_CARD_STYLES.colors.success,
                    opacity: 0.7
                  }} />
                </ListItemIcon>
                <ListItemText 
                  primary="Revenue Impact"
                  secondary={`${(strategyData.performance_predictions.roi_predictions as any)?.revenue_impact || '$50K'} additional monthly revenue`}
                  primaryTypographyProps={{ 
                    variant: 'body2', 
                    fontSize: '0.875rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.success, fontWeight: 600, mb: 0.5 }
                  }}
                  secondaryTypographyProps={{ 
                    variant: 'caption', 
                    fontSize: '0.75rem',
                    sx: { color: ANALYSIS_CARD_STYLES.colors.text.secondary, lineHeight: 1.4 }
                  }}
                />
              </ListItem>
            )}
          </List>
        </Box>
      </Box>

      {/* Timeline Projections */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
          Timeline Projections
        </Typography>
        <Box sx={sectionStyles.sectionContainer}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <Typography variant="body2" sx={{ 
              color: ANALYSIS_CARD_STYLES.colors.text.secondary, 
              fontSize: '0.8rem',
              lineHeight: 1.5
            }}>
              • Month 1-2: Initial setup and foundation building
            </Typography>
            <Typography variant="body2" sx={{ 
              color: ANALYSIS_CARD_STYLES.colors.text.secondary, 
              fontSize: '0.8rem',
              lineHeight: 1.5
            }}>
              • Month 3-4: Content creation and optimization
            </Typography>
            <Typography variant="body2" sx={{ 
              color: ANALYSIS_CARD_STYLES.colors.text.secondary, 
              fontSize: '0.8rem',
              lineHeight: 1.5
            }}>
              • Month 5-6: Scaling and performance optimization
            </Typography>
            <Typography variant="body2" sx={{ 
              color: ANALYSIS_CARD_STYLES.colors.text.secondary, 
              fontSize: '0.8rem',
              lineHeight: 1.5
            }}>
              • Ongoing: Continuous monitoring and improvement
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Grid item xs={12} lg={6}>
      <ProgressiveCard
        title="Performance Predictions"
        subtitle="ROI and success metrics"
        icon={<ShowChartIcon sx={{ color: 'white', fontSize: 20 }} />}
        summary={summaryContent}
        details={detailedContent}
        trigger="hover"
        autoCollapseDelay={3000}
      />
    </Grid>
  );
};

export default PerformancePredictionsCard; 