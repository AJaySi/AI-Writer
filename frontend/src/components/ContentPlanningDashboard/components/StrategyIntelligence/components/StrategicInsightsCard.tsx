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
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Lightbulb as LightbulbIcon,
  ExpandMore as ExpandMoreIcon,
  TrendingUp as TrendingUpIcon,
  Psychology as PsychologyIcon,
  Business as BusinessIcon,
  Analytics as AnalyticsIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { StrategyData } from '../types/strategy.types';
import {
  ANALYSIS_CARD_STYLES,
  getSectionStyles,
  getAccordionStyles,
  getEnhancedChipStyles,
  getListItemStyles,
  getAnimationStyles
} from '../styles';
import ProgressiveCard from './ProgressiveCard';

interface StrategicInsightsCardProps {
  strategyData: StrategyData | null;
}

const StrategicInsightsCard: React.FC<StrategicInsightsCardProps> = ({ strategyData }) => {
  // Get style objects
  const sectionStyles = getSectionStyles();
  const accordionStyles = getAccordionStyles();
  const listItemStyles = getListItemStyles();
  const animationStyles = getAnimationStyles();

  console.log('🔍 StrategicInsightsCard - strategyData:', strategyData);
  console.log('🔍 StrategicInsightsCard - strategic_insights:', strategyData?.strategic_insights);

  if (!strategyData?.strategic_insights) {
    return (
      <Grid item xs={12} lg={6}>
        <ProgressiveCard
          title="Strategic Insights"
          subtitle="AI-powered market analysis"
          icon={<LightbulbIcon sx={{ color: 'white', fontSize: 20 }} />}
          summary={
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <Typography variant="body1" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.secondary }}>
                Strategic insights data not available
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
          trigger="click"
        />
      </Grid>
    );
  }

  // Helper function to get insight icon
  const getInsightIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'market': return <TrendingUpIcon />;
      case 'consumer': return <PsychologyIcon />;
      case 'business': return <BusinessIcon />;
      case 'analytics': return <AnalyticsIcon />;
      default: return <LightbulbIcon />;
    }
  };

  // Summary content - always visible
  const summaryContent = (
    <Box>
      {/* Market Analysis Summary */}
      <Box sx={sectionStyles.sectionContainer}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ 
              width: 40, 
              height: 40, 
              borderRadius: '50%', 
              background: `linear-gradient(135deg, ${ANALYSIS_CARD_STYLES.colors.success} 0%, ${ANALYSIS_CARD_STYLES.colors.info} 100%)`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
              color: 'white',
              fontSize: '1.2rem',
              fontWeight: 600,
              boxShadow: `0 4px 12px ${ANALYSIS_CARD_STYLES.colors.success}30`
            }}>
              85%
            </Box>
            <Box>
              <Typography variant="h6" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, fontWeight: 600 }}>
                Market Analysis
              </Typography>
              <Typography variant="caption" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.secondary }}>
                Strong market positioning identified
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Chip 
              label="High Growth"
              size="small"
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.success).chip}
            />
            <Chip 
              label="6 months"
              size="small"
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.info).chip}
            />
          </Box>
        </Box>
      </Box>

      {/* Key Insights Preview */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 1, fontWeight: 600 }}>
          Key Insights Preview
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {strategyData.strategic_insights.insights?.slice(0, 3).map((insight: any, index: number) => (
            <Chip
              key={index}
              label={insight.type}
              size="small"
              icon={getInsightIcon(insight.type)}
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.primary).chip}
            />
          ))}
          {(strategyData.strategic_insights.insights?.length || 0) > 3 && (
            <Chip
              label={`+${(strategyData.strategic_insights.insights?.length || 0) - 3} more`}
              size="small"
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.secondary).chip}
            />
          )}
        </Box>
      </Box>
    </Box>
  );

  // Detailed content - shown on expansion
  const detailedContent = (
    <Box>
      {/* Strategic Insights by Type */}
      {strategyData.strategic_insights.insights && strategyData.strategic_insights.insights.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
            Detailed Strategic Insights ({strategyData.strategic_insights.insights.length})
          </Typography>
          
          {/* Group insights by type */}
          {Object.entries(
            strategyData.strategic_insights.insights.reduce((acc: any, insight: any) => {
              const type = insight.type || 'General';
              if (!acc[type]) acc[type] = [];
              acc[type].push(insight);
              return acc;
            }, {})
          ).map(([type, insights]: [string, any]) => (
            <Accordion key={type} defaultExpanded={false} sx={accordionStyles.accordion}>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon sx={accordionStyles.expandIcon} />}
                sx={accordionStyles.accordionSummary}
              >
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Box sx={{ mr: 1.5 }}>
                    {getInsightIcon(type)}
                  </Box>
                  <Box>
                    <Typography variant="body2" sx={accordionStyles.accordionTitle}>
                      {type} Insights ({insights.length})
                    </Typography>
                    <Typography variant="caption" sx={accordionStyles.accordionSubtitle}>
                      {insights.length} strategic {insights.length === 1 ? 'insight' : 'insights'}
                    </Typography>
                  </Box>
                </Box>
              </AccordionSummary>
              <AccordionDetails sx={{ pt: 0 }}>
                <Box sx={sectionStyles.sectionContainer}>
                  <List dense>
                    {insights.map((insight: any, index: number) => (
                      <ListItem key={index} sx={listItemStyles.listItem}>
                        <ListItemIcon sx={listItemStyles.listItemIcon}>
                          <Box sx={{ 
                            width: 6, 
                            height: 6, 
                            borderRadius: '50%', 
                            background: ANALYSIS_CARD_STYLES.colors.primary,
                            opacity: 0.7
                          }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={insight.insight}
                          primaryTypographyProps={{ 
                            variant: 'body2', 
                            fontSize: '0.875rem',
                            sx: { lineHeight: 1.4, color: ANALYSIS_CARD_STYLES.colors.text.primary }
                          }}
                          secondary={
                            <Box sx={{ mt: 0.5 }}>
                              <Box sx={{ display: 'flex', gap: 1, mb: 0.5 }}>
                                <Chip
                                  label={`P: ${insight.priority || 'Medium'}`}
                                  size="small"
                                  sx={getEnhancedChipStyles(
                                    insight.priority === 'High' ? ANALYSIS_CARD_STYLES.colors.error : 
                                    insight.priority === 'Medium' ? ANALYSIS_CARD_STYLES.colors.warning : 
                                    ANALYSIS_CARD_STYLES.colors.success
                                  ).chip}
                                />
                                <Chip
                                  label={`I: ${insight.estimated_impact || 'Medium'}`}
                                  size="small"
                                  sx={getEnhancedChipStyles(
                                    insight.estimated_impact === 'High' ? ANALYSIS_CARD_STYLES.colors.error : 
                                    insight.estimated_impact === 'Medium' ? ANALYSIS_CARD_STYLES.colors.warning : 
                                    ANALYSIS_CARD_STYLES.colors.success
                                  ).chip}
                                />
                                <Chip
                                  label={`C: ${insight.confidence_level || 'Medium'}`}
                                  size="small"
                                  sx={getEnhancedChipStyles(
                                    insight.confidence_level === 'High' ? ANALYSIS_CARD_STYLES.colors.success : 
                                    insight.confidence_level === 'Medium' ? ANALYSIS_CARD_STYLES.colors.warning : 
                                    ANALYSIS_CARD_STYLES.colors.error
                                  ).chip}
                                />
                                <Chip
                                  label={`T: ${insight.implementation_time || '3 months'}`}
                                  size="small"
                                  sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.info).chip}
                                />
                              </Box>
                              {insight.reasoning && (
                                <Typography variant="caption" sx={{ 
                                  display: 'block', 
                                  fontSize: '0.75rem', 
                                  color: ANALYSIS_CARD_STYLES.colors.text.secondary,
                                  fontStyle: 'italic'
                                }}>
                                  <strong>Reasoning:</strong> {insight.reasoning}
                                </Typography>
                              )}
                            </Box>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      )}

      {/* Content Opportunities */}
      {strategyData.strategic_insights.content_opportunities && strategyData.strategic_insights.content_opportunities.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
            Content Opportunities ({strategyData.strategic_insights.content_opportunities.length})
          </Typography>
          <Box sx={sectionStyles.sectionContainer}>
            <List dense>
              {strategyData.strategic_insights.content_opportunities.map((opportunity: string, index: number) => (
                <ListItem key={index} sx={listItemStyles.listItem}>
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
                    primary={opportunity}
                    primaryTypographyProps={{ 
                      variant: 'body2', 
                      fontSize: '0.875rem',
                      sx: { lineHeight: 1.4, color: ANALYSIS_CARD_STYLES.colors.text.primary }
                    }}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </Box>
      )}
    </Box>
  );

  return (
    <Grid item xs={12} lg={6}>
      <ProgressiveCard
        title="Strategic Insights"
        subtitle="AI-powered market analysis"
        icon={<LightbulbIcon sx={{ color: 'white', fontSize: 20 }} />}
        summary={summaryContent}
        details={detailedContent}
        trigger="hover"
        autoCollapseDelay={2000}
      />
    </Grid>
  );
};

export default StrategicInsightsCard; 