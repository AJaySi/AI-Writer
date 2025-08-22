import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  Chip,
  Card,
  Alert
} from '@mui/material';

// Import styles
import {
  dataSourceCardStyles,
  dataSourceIconStyles,
  getDataSourceIconColor,
  qualityMetricsContainerStyles,
  getMetricColor
} from '../CalendarGenerationModal.styles';

interface DataSourcePanelProps {
  currentStep?: number;
  stepResults?: Record<number, any>;
}

const DataSourcePanel: React.FC<DataSourcePanelProps> = ({ 
  currentStep = 1, 
  stepResults = {} 
}) => {
  // Get data sources for current step
  const getStepDataSources = (step: number) => {
    switch (step) {
      case 1:
        return [
          {
            name: "Content Strategy",
            description: "Your existing content strategy and business goals",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Updated 2 hours ago",
            icon: "✓",
            iconColor: "strategy"
          },
          {
            name: "Business Goals",
            description: "KPI mapping and strategic objectives",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Updated 2 hours ago",
            icon: "🎯",
            iconColor: "primary"
          },
          {
            name: "Target Audience",
            description: "Audience personas and demographics",
            confidence: "Medium Confidence",
            confidenceColor: "warning" as const,
            lastUpdated: "Updated 1 day ago",
            icon: "👥",
            iconColor: "info"
          }
        ];
      case 2:
        return [
          {
            name: "Gap Analysis",
            description: "Content gaps and opportunity identification",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "📊",
            iconColor: "info"
          },
          {
            name: "Keyword Research",
            description: "High-value keywords and search volume data",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "🔍",
            iconColor: "primary"
          },
          {
            name: "Competitor Analysis",
            description: "Competitive insights and differentiation strategies",
            confidence: "Medium Confidence",
            confidenceColor: "warning" as const,
            lastUpdated: "Updated 3 hours ago",
            icon: "🏆",
            iconColor: "secondary"
          }
        ];
      case 3:
        return [
          {
            name: "Audience Data",
            description: "Detailed audience personas and preferences",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Updated 1 day ago",
            icon: "👥",
            iconColor: "info"
          },
          {
            name: "Platform Performance",
            description: "Historical platform engagement metrics",
            confidence: "Medium Confidence",
            confidenceColor: "warning" as const,
            lastUpdated: "Updated 3 days ago",
            icon: "📈",
            iconColor: "secondary"
          },
          {
            name: "Content Mix Analysis",
            description: "Optimal content type distribution",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "🎨",
            iconColor: "primary"
          }
        ];
      case 4:
        return [
          {
            name: "Calendar Configuration",
            description: "User posting preferences and calendar settings",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Just configured",
            icon: "📅",
            iconColor: "primary"
          },
          {
            name: "Timeline Optimization",
            description: "Optimal posting times and frequency analysis",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "⏰",
            iconColor: "info"
          },
          {
            name: "Duration Control",
            description: "Calendar duration and structure validation",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "📏",
            iconColor: "secondary"
          }
        ];
      case 5:
        return [
          {
            name: "Content Pillars",
            description: "Strategic content pillar definitions from Step 1",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "From Step 1",
            icon: "🏗️",
            iconColor: "primary"
          },
          {
            name: "Timeline Structure",
            description: "Calendar framework from Step 4",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "From Step 4",
            icon: "📅",
            iconColor: "info"
          },
          {
            name: "Theme Development",
            description: "Industry-specific theme generation",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "🎨",
            iconColor: "secondary"
          }
        ];
      case 6:
        return [
          {
            name: "Platform Performance",
            description: "Platform-specific engagement data from Step 3",
            confidence: "Medium Confidence",
            confidenceColor: "warning" as const,
            lastUpdated: "From Step 3",
            icon: "📈",
            iconColor: "secondary"
          },
          {
            name: "Content Adaptation",
            description: "Platform-specific content optimization",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "🔄",
            iconColor: "primary"
          },
          {
            name: "Cross-Platform Coordination",
            description: "Multi-platform strategy alignment",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "🔗",
            iconColor: "info"
          }
        ];
      default:
        return [
          {
            name: "Content Strategy",
            description: "Your existing content strategy and business goals",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Updated 2 hours ago",
            icon: "✓",
            iconColor: "strategy"
          },
          {
            name: "Onboarding Data",
            description: "Industry, audience, and platform preferences",
            confidence: "Medium Confidence",
            confidenceColor: "warning" as const,
            lastUpdated: "Updated 1 day ago",
            icon: "📊",
            iconColor: "info"
          },
          {
            name: "AI Analysis",
            description: "AI-powered content and performance insights",
            confidence: "High Confidence",
            confidenceColor: "success" as const,
            lastUpdated: "Real-time analysis",
            icon: "🤖",
            iconColor: "primary"
          }
        ];
    }
  };

  const currentDataSources = getStepDataSources(currentStep);

  return (
    <Paper elevation={1} sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Data Sources & Transparency
      </Typography>
      
      <Box mb={3}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          This calendar generation uses multiple data sources to ensure high-quality, personalized results.
          {currentStep <= 6 && (
            <span> Currently showing data sources for <strong>Step {currentStep}</strong>.</span>
          )}
        </Typography>
      </Box>

      {/* Data Source Attribution */}
      <Box mb={3}>
        <Typography variant="subtitle1" gutterBottom>
          Data Sources Used {currentStep <= 6 && `(Step ${currentStep})`}
        </Typography>
        
        <Grid container spacing={2}>
          {currentDataSources.map((source, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card variant="outlined" sx={dataSourceCardStyles}>
                <Box display="flex" alignItems="center" gap={2} mb={1}>
                  <Box
                    sx={{
                      ...dataSourceIconStyles,
                      backgroundColor: getDataSourceIconColor(source.iconColor)
                    }}
                  >
                    {source.icon}
                  </Box>
                  <Typography variant="subtitle2">{source.name}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {source.description}
                </Typography>
                <Box display="flex" alignItems="center" gap={1} mt={1}>
                  <Chip label={source.confidence} size="small" color={source.confidenceColor} />
                  <Typography variant="caption" color="text.secondary">
                    {source.lastUpdated}
                  </Typography>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Data Quality Metrics */}
      <Box mb={3}>
        <Typography variant="subtitle1" gutterBottom>
          Data Quality Metrics
        </Typography>
        
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Box sx={qualityMetricsContainerStyles}>
              <Typography variant="h4" sx={{ color: getMetricColor('Overall Data Quality') }} gutterBottom>
                94%
              </Typography>
              <Typography variant="body2">
                Overall Data Quality
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box sx={qualityMetricsContainerStyles}>
              <Typography variant="h4" sx={{ color: getMetricColor('Data Completeness') }} gutterBottom>
                87%
              </Typography>
              <Typography variant="body2">
                Data Completeness
              </Typography>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box sx={qualityMetricsContainerStyles}>
              <Typography variant="h4" sx={{ color: getMetricColor('Data Freshness') }} gutterBottom>
                91%
              </Typography>
              <Typography variant="body2">
                Data Freshness
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Box>

      {/* Transparency Note */}
      <Alert severity="info">
        <Typography variant="body2">
          <strong>Transparency Note:</strong> All data sources are processed securely and used only for calendar generation. 
          No personal data is shared with third parties. You can review and update your data sources in the settings.
        </Typography>
      </Alert>
    </Paper>
  );
};

export default DataSourcePanel;
