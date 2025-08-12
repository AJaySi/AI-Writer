import React, { useState } from 'react';
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
  AccordionDetails,
  Popover
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  ExpandMore as ExpandMoreIcon,
  Business as BusinessIcon,
  Star as StarIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Lightbulb as LightbulbIcon
} from '@mui/icons-material';
import { StrategyData } from '../types/strategy.types';
import {
  ANALYSIS_CARD_STYLES,
  getSectionStyles,
  getAccordionStyles,
  getEnhancedChipStyles,
  getListItemStyles
} from '../styles';
import ProgressiveCard from './ProgressiveCard';

interface CompetitiveAnalysisCardProps {
  strategyData: StrategyData | null;
}

const CompetitiveAnalysisCard: React.FC<CompetitiveAnalysisCardProps> = ({ strategyData }) => {
  const [chipModal, setChipModal] = useState<{
    open: boolean;
    anchorEl: HTMLElement | null;
    content: string;
    type: 'strength' | 'weakness';
  }>({
    open: false,
    anchorEl: null,
    content: '',
    type: 'strength'
  });

  // Get style objects
  const sectionStyles = getSectionStyles();
  const accordionStyles = getAccordionStyles();
  const listItemStyles = getListItemStyles();

  // Helper function to extract company name from description
  const extractCompanyName = (description: string): string => {
    if (description.includes('Jasper')) return 'Jasper AI';
    if (description.includes('Copy.ai')) return 'Copy.ai';
    if (description.includes('Writesonic')) return 'Writesonic';
    if (description.includes('Grammarly')) return 'Grammarly';
    if (description.includes('Surfer')) return 'Surfer SEO';
    if (description.includes('Clearscope')) return 'Clearscope';
    if (description.includes('Ahrefs')) return 'Ahrefs';
    if (description.includes('SEMrush')) return 'SEMrush';
    return description.split(' ').slice(0, 2).join(' ');
  };

  if (!strategyData?.competitive_analysis) {
    return (
      <Grid item xs={12} lg={6}>
        <ProgressiveCard
          title="Competitive Analysis"
          subtitle="Market positioning insights"
          icon={<TrendingUpIcon sx={{ color: 'white', fontSize: 20 }} />}
          summary={
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <Typography variant="body1" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.secondary }}>
                Competitive analysis data not available
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
      {/* Competitive Overview */}
      <Box sx={sectionStyles.sectionContainer}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Box sx={{ 
              width: 40, 
              height: 40, 
              borderRadius: '50%', 
              background: `linear-gradient(135deg, ${ANALYSIS_CARD_STYLES.colors.warning} 0%, ${ANALYSIS_CARD_STYLES.colors.error} 100%)`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
              color: 'white',
              fontSize: '1.2rem',
              fontWeight: 600,
              boxShadow: `0 4px 12px ${ANALYSIS_CARD_STYLES.colors.warning}30`
            }}>
              {strategyData.competitive_analysis.competitors?.length || 0}
            </Box>
            <Box>
              <Typography variant="h6" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, fontWeight: 600 }}>
                Key Competitors
              </Typography>
              <Typography variant="caption" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.secondary }}>
                {strategyData.competitive_analysis.competitors?.length || 0} competitors analyzed
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Chip 
              label={`${strategyData.competitive_analysis.market_gaps?.length || 0} Gaps`}
              size="small"
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.info).chip}
            />
            <Chip 
              label={`${strategyData.competitive_analysis.opportunities?.length || 0} Opportunities`}
              size="small"
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.success).chip}
            />
          </Box>
        </Box>
      </Box>

      {/* Competitors Preview */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 1, fontWeight: 600 }}>
          Top Competitors
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {strategyData.competitive_analysis.competitors?.slice(0, 3).map((competitor: any, index: number) => (
            <Chip
              key={index}
              label={extractCompanyName(competitor.name || competitor.description || 'Unknown')}
              size="small"
              icon={<BusinessIcon />}
              sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.primary).chip}
            />
          ))}
          {(strategyData.competitive_analysis.competitors?.length || 0) > 3 && (
            <Chip
              label={`+${(strategyData.competitive_analysis.competitors?.length || 0) - 3} more`}
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
      {/* Competitors Analysis */}
      {strategyData.competitive_analysis.competitors && strategyData.competitive_analysis.competitors.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
            Competitor Analysis ({strategyData.competitive_analysis.competitors.length})
          </Typography>
          
          {strategyData.competitive_analysis.competitors.map((competitor: any, index: number) => (
            <Accordion key={index} defaultExpanded={false} sx={accordionStyles.accordion}>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon sx={accordionStyles.expandIcon} />}
                sx={accordionStyles.accordionSummary}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                  <Box sx={{ mr: 1.5 }}>
                    <BusinessIcon sx={{ color: ANALYSIS_CARD_STYLES.colors.primary, fontSize: 20 }} />
                  </Box>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="body2" sx={accordionStyles.accordionTitle}>
                      {extractCompanyName(competitor.name || competitor.description || 'Unknown Competitor')}
                    </Typography>
                    <Typography variant="caption" sx={accordionStyles.accordionSubtitle}>
                      {competitor.description || 'Competitor analysis'}
                    </Typography>
                  </Box>
                </Box>
              </AccordionSummary>
              <AccordionDetails sx={{ pt: 0 }}>
                <Box sx={sectionStyles.sectionContainer}>
                  {/* Content Strategy */}
                  {competitor.content_strategy && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" sx={{ color: ANALYSIS_CARD_STYLES.colors.primary, fontWeight: 600, mb: 1 }}>
                        Content Strategy
                      </Typography>
                      <Typography variant="body2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, fontSize: '0.875rem' }}>
                        {competitor.content_strategy}
                      </Typography>
                    </Box>
                  )}

                  {/* Strengths */}
                  {competitor.strengths && competitor.strengths.length > 0 && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" sx={{ color: ANALYSIS_CARD_STYLES.colors.success, fontWeight: 600, mb: 1 }}>
                        Strengths
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {competitor.strengths.map((strength: string, strengthIndex: number) => (
                          <Chip
                            key={strengthIndex}
                            label={strength}
                            size="small"
                            icon={<CheckCircleIcon />}
                            sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.success).chip}
                            onClick={(e) => setChipModal({
                              open: true,
                              anchorEl: e.currentTarget,
                              content: strength,
                              type: 'strength'
                            })}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}

                  {/* Weaknesses */}
                  {competitor.weaknesses && competitor.weaknesses.length > 0 && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" sx={{ color: ANALYSIS_CARD_STYLES.colors.warning, fontWeight: 600, mb: 1 }}>
                        Weaknesses
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {competitor.weaknesses.map((weakness: string, weaknessIndex: number) => (
                          <Chip
                            key={weaknessIndex}
                            label={weakness}
                            size="small"
                            icon={<CancelIcon />}
                            sx={getEnhancedChipStyles(ANALYSIS_CARD_STYLES.colors.warning).chip}
                            onClick={(e) => setChipModal({
                              open: true,
                              anchorEl: e.currentTarget,
                              content: weakness,
                              type: 'weakness'
                            })}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                </Box>
              </AccordionDetails>
            </Accordion>
          ))}
        </Box>
      )}

      {/* Market Gaps */}
      {strategyData.competitive_analysis.market_gaps && strategyData.competitive_analysis.market_gaps.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
            Market Gaps ({strategyData.competitive_analysis.market_gaps.length})
          </Typography>
          <Box sx={sectionStyles.sectionContainer}>
            <List dense>
              {strategyData.competitive_analysis.market_gaps.map((gap: string, index: number) => (
                <ListItem key={index} sx={listItemStyles.listItem}>
                  <ListItemIcon sx={listItemStyles.listItemIcon}>
                    <Box sx={{ 
                      width: 6, 
                      height: 6, 
                      borderRadius: '50%', 
                      background: ANALYSIS_CARD_STYLES.colors.info,
                      opacity: 0.7
                    }} />
                  </ListItemIcon>
                  <ListItemText 
                    primary={gap}
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

      {/* Opportunities */}
      {strategyData.competitive_analysis.opportunities && strategyData.competitive_analysis.opportunities.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
            Opportunities ({strategyData.competitive_analysis.opportunities.length})
          </Typography>
          <Box sx={sectionStyles.sectionContainer}>
            <List dense>
              {strategyData.competitive_analysis.opportunities.map((opportunity: string, index: number) => (
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

      {/* Strategic Recommendations */}
      {strategyData.competitive_analysis.recommendations && strategyData.competitive_analysis.recommendations.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, mb: 2, fontWeight: 600 }}>
            Strategic Recommendations ({strategyData.competitive_analysis.recommendations.length})
          </Typography>
          <Box sx={sectionStyles.sectionContainer}>
            <List dense>
              {strategyData.competitive_analysis.recommendations.map((recommendation: string, index: number) => (
                <ListItem key={index} sx={listItemStyles.listItem}>
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
                    primary={recommendation}
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
        title="Competitive Analysis"
        subtitle="Market positioning insights"
        icon={<TrendingUpIcon sx={{ color: 'white', fontSize: 20 }} />}
        summary={summaryContent}
        details={detailedContent}
        trigger="hover"
        autoCollapseDelay={3000}
      />

      {/* Chip Modal for detailed view */}
      <Popover
        open={chipModal.open}
        anchorEl={chipModal.anchorEl}
        onClose={() => setChipModal({ ...chipModal, open: false })}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
        PaperProps={{
          sx: {
            background: ANALYSIS_CARD_STYLES.colors.background.dark,
            border: `1px solid ${ANALYSIS_CARD_STYLES.colors.border.secondary}`,
            backdropFilter: 'blur(10px)',
            p: 2,
            maxWidth: 300
          }
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {chipModal.type === 'strength' ? (
            <CheckCircleIcon sx={{ color: ANALYSIS_CARD_STYLES.colors.success, fontSize: 16, mr: 1 }} />
          ) : (
            <CancelIcon sx={{ color: ANALYSIS_CARD_STYLES.colors.warning, fontSize: 16, mr: 1 }} />
          )}
          <Typography variant="body2" sx={{ 
            color: chipModal.type === 'strength' ? ANALYSIS_CARD_STYLES.colors.success : ANALYSIS_CARD_STYLES.colors.warning,
            fontWeight: 600 
          }}>
            {chipModal.type === 'strength' ? 'Strength' : 'Weakness'}
          </Typography>
        </Box>
        <Typography variant="body2" sx={{ color: ANALYSIS_CARD_STYLES.colors.text.primary, fontSize: '0.875rem' }}>
          {chipModal.content}
        </Typography>
      </Popover>
    </Grid>
  );
};

export default CompetitiveAnalysisCard; 