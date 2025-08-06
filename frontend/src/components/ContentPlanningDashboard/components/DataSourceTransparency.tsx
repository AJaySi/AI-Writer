import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  LinearProgress,
  Alert,
  IconButton,
  Collapse,
  Tooltip
} from '@mui/material';
import {
  DataUsage as DataUsageIcon,
  AutoAwesome as AutoAwesomeIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';

interface DataSourceTransparencyProps {
  autoPopulatedFields: Record<string, any>;
  dataSources: Record<string, string>;
}

const DataSourceTransparency: React.FC<DataSourceTransparencyProps> = ({
  autoPopulatedFields,
  dataSources
}) => {
  const [expanded, setExpanded] = React.useState(true);

  const getDataSourceIcon = (source: string) => {
    const icons = {
      website_analysis: '🌐',
      research_preferences: '🔍',
      api_keys: '🔑',
      onboarding_session: '📋'
    };
    return icons[source as keyof typeof icons] || '📊';
  };

  const getDataSourceLabel = (source: string) => {
    const labels = {
      website_analysis: 'Website Analysis',
      research_preferences: 'Research Preferences',
      api_keys: 'API Configuration',
      onboarding_session: 'Onboarding Session'
    };
    return labels[source as keyof typeof labels] || source;
  };

  const getDataQualityScore = (source: string) => {
    // Mock quality scores based on data source
    const scores = {
      website_analysis: 0.85,
      research_preferences: 0.92,
      api_keys: 0.78,
      onboarding_session: 0.88
    };
    return scores[source as keyof typeof scores] || 0.7;
  };

  const getDataQualityColor = (score: number) => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  const getDataQualityLabel = (score: number) => {
    if (score >= 0.8) return 'High Quality';
    if (score >= 0.6) return 'Medium Quality';
    return 'Low Quality';
  };

  const autoPopulatedFieldsList = Object.entries(autoPopulatedFields).map(([fieldId, value]) => ({
    fieldId,
    value,
    source: dataSources[fieldId] || 'unknown',
    qualityScore: getDataQualityScore(dataSources[fieldId] || 'unknown')
  }));

  const sourceSummary = Object.entries(dataSources).reduce((acc, [fieldId, source]) => {
    if (!acc[source]) {
      acc[source] = [];
    }
    acc[source].push(fieldId);
    return acc;
  }, {} as Record<string, string[]>);

  if (Object.keys(autoPopulatedFields).length === 0) {
    return null;
  }

  return (
    <Card variant="outlined">
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <DataUsageIcon color="primary" />
          <Typography variant="h6">
            Data Sources
          </Typography>
          <Chip
            icon={<AutoAwesomeIcon />}
            label={`${Object.keys(autoPopulatedFields).length} auto-populated`}
            color="info"
            size="small"
          />
          <IconButton
            size="small"
            onClick={() => setExpanded(!expanded)}
          >
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Box>

        <Collapse in={expanded}>
          {/* Summary */}
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              {Object.keys(autoPopulatedFields).length} fields were automatically populated from your onboarding data.
            </Typography>
          </Alert>

          {/* Data Sources Breakdown */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Data Sources
            </Typography>
            <List dense>
              {Object.entries(sourceSummary).map(([source, fields]) => (
                <ListItem key={source} sx={{ px: 0 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <Typography variant="body1">
                      {getDataSourceIcon(source)}
                    </Typography>
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="body2" fontWeight="medium">
                          {getDataSourceLabel(source)}
                        </Typography>
                        <Chip
                          label={`${fields.length} fields`}
                          size="small"
                          variant="outlined"
                        />
                      </Box>
                    }
                    secondary={
                      <Box sx={{ mt: 0.5 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                          <LinearProgress
                            variant="determinate"
                            value={getDataQualityScore(source) * 100}
                            color={getDataQualityColor(getDataQualityScore(source))}
                            sx={{ flexGrow: 1, height: 4, borderRadius: 2 }}
                          />
                          <Typography variant="caption" color="text.secondary">
                            {Math.round(getDataQualityScore(source) * 100)}%
                          </Typography>
                        </Box>
                        <Typography variant="caption" color="text.secondary">
                          {getDataQualityLabel(getDataQualityScore(source))}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Box>

          <Divider sx={{ my: 2 }} />

          {/* Auto-populated Fields */}
          <Box>
            <Typography variant="subtitle2" gutterBottom>
              Auto-populated Fields
            </Typography>
            <List dense>
              {autoPopulatedFieldsList.map((field, index) => (
                <React.Fragment key={field.fieldId}>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon sx={{ minWidth: 40 }}>
                      <CheckCircleIcon color="success" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body2" fontWeight="medium">
                            {field.fieldId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </Typography>
                          <Chip
                            label={getDataSourceLabel(field.source)}
                            size="small"
                            variant="outlined"
                          />
                        </Box>
                      }
                      secondary={
                        <Typography variant="caption" color="text.secondary">
                          Source: {getDataSourceLabel(field.source)} • Quality: {getDataQualityLabel(field.qualityScore)}
                        </Typography>
                      }
                    />
                  </ListItem>
                  {index < autoPopulatedFieldsList.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Box>

          {/* Transparency Note */}
          <Box sx={{ mt: 2, p: 1, bgcolor: 'background.default', borderRadius: 1 }}>
            <Typography variant="caption" color="text.secondary">
              💡 You can modify any auto-populated field. The system learns from your changes to improve future recommendations.
            </Typography>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default DataSourceTransparency; 