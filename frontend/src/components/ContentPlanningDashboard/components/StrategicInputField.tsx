import React, { useState } from 'react';
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Chip,
  IconButton,
  Tooltip,
  Typography,
  Alert,
  Autocomplete,
  InputAdornment
} from '@mui/material';
import {
  Help as HelpIcon,
  AutoAwesome as AutoAwesomeIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Edit as EditIcon
} from '@mui/icons-material';
import { useEnhancedStrategyStore } from '../../../stores/enhancedStrategyStore';

interface StrategicInputFieldProps {
  fieldId: string;
  value: any;
  error?: string;
  autoPopulated?: boolean;
  dataSource?: string;
  onChange: (value: any) => void;
  onValidate: () => boolean;
  onShowTooltip: () => void;
}

// Define proper types for field configurations
interface BaseFieldConfig {
  type: string;
  label: string;
  required: boolean;
}

interface TextFieldConfig extends BaseFieldConfig {
  type: 'text' | 'number' | 'json';
  placeholder: string;
}

interface SelectFieldConfig extends BaseFieldConfig {
  type: 'select';
  options: string[];
}

interface MultiSelectFieldConfig extends BaseFieldConfig {
  type: 'multiselect';
  options: string[];
  placeholder?: string;
}

interface BooleanFieldConfig extends BaseFieldConfig {
  type: 'boolean';
}

type FieldConfig = TextFieldConfig | SelectFieldConfig | MultiSelectFieldConfig | BooleanFieldConfig;

const StrategicInputField: React.FC<StrategicInputFieldProps> = ({
  fieldId,
  value,
  error,
  autoPopulated = false,
  dataSource,
  onChange,
  onValidate,
  onShowTooltip
}) => {
  const { getTooltipData } = useEnhancedStrategyStore();
  const [isEditing, setIsEditing] = useState(false);
  
  // Get field configuration from store with proper null checking
  const tooltipData = getTooltipData(fieldId);
  
  // Field configuration mapping (this would come from the store)
  const fieldConfig: Record<string, FieldConfig> = {
    business_objectives: {
      type: 'json',
      label: 'Business Objectives',
      placeholder: 'Enter your primary and secondary business goals',
      required: true
    },
    target_metrics: {
      type: 'json',
      label: 'Target Metrics',
      placeholder: 'Define your KPIs and success metrics',
      required: true
    },
    content_budget: {
      type: 'number',
      label: 'Content Budget',
      placeholder: 'Enter your content budget',
      required: false
    },
    team_size: {
      type: 'number',
      label: 'Team Size',
      placeholder: 'Enter team size',
      required: false
    },
    implementation_timeline: {
      type: 'select',
      label: 'Implementation Timeline',
      options: ['3 months', '6 months', '1 year', '2 years', 'Ongoing'],
      required: false
    },
    market_share: {
      type: 'text',
      label: 'Market Share',
      placeholder: 'Enter market share percentage',
      required: false
    },
    competitive_position: {
      type: 'select',
      label: 'Competitive Position',
      options: ['Leader', 'Challenger', 'Niche', 'Emerging'],
      required: false
    },
    performance_metrics: {
      type: 'json',
      label: 'Current Performance Metrics',
      placeholder: 'Enter current performance data',
      required: false
    },
    content_preferences: {
      type: 'json',
      label: 'Content Preferences',
      placeholder: 'Define content preferences',
      required: true
    },
    consumption_patterns: {
      type: 'json',
      label: 'Consumption Patterns',
      placeholder: 'Describe consumption patterns',
      required: false
    },
    audience_pain_points: {
      type: 'json',
      label: 'Audience Pain Points',
      placeholder: 'List audience pain points',
      required: false
    },
    buying_journey: {
      type: 'json',
      label: 'Buying Journey',
      placeholder: 'Define buying journey stages',
      required: false
    },
    seasonal_trends: {
      type: 'json',
      label: 'Seasonal Trends',
      placeholder: 'Describe seasonal content patterns',
      required: false
    },
    engagement_metrics: {
      type: 'json',
      label: 'Engagement Metrics',
      placeholder: 'Define engagement tracking metrics',
      required: false
    },
    top_competitors: {
      type: 'json',
      label: 'Top Competitors',
      placeholder: 'List your main competitors',
      required: false
    },
    competitor_content_strategies: {
      type: 'json',
      label: 'Competitor Content Strategies',
      placeholder: 'Analyze competitor content approaches',
      required: false
    },
    market_gaps: {
      type: 'json',
      label: 'Market Gaps',
      placeholder: 'Identify content gaps in the market',
      required: false
    },
    industry_trends: {
      type: 'json',
      label: 'Industry Trends',
      placeholder: 'Describe relevant industry trends',
      required: false
    },
    emerging_trends: {
      type: 'json',
      label: 'Emerging Trends',
      placeholder: 'Identify emerging content trends',
      required: false
    },
    preferred_formats: {
      type: 'json',
      label: 'Preferred Formats',
      placeholder: 'Define preferred content formats',
      required: false
    },
    content_mix: {
      type: 'json',
      label: 'Content Mix',
      placeholder: 'Define your content mix strategy',
      required: false
    },
    content_frequency: {
      type: 'select',
      label: 'Content Frequency',
      options: ['Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly'],
      required: false
    },
    optimal_timing: {
      type: 'json',
      label: 'Optimal Timing',
      placeholder: 'Define optimal posting times',
      required: false
    },
    quality_metrics: {
      type: 'json',
      label: 'Quality Metrics',
      placeholder: 'Define content quality standards',
      required: false
    },
    editorial_guidelines: {
      type: 'json',
      label: 'Editorial Guidelines',
      placeholder: 'Define editorial guidelines',
      required: false
    },
    brand_voice: {
      type: 'json',
      label: 'Brand Voice',
      placeholder: 'Define your brand voice',
      required: false
    },
    traffic_sources: {
      type: 'json',
      label: 'Traffic Sources',
      placeholder: 'Define your traffic sources',
      required: false
    },
    conversion_rates: {
      type: 'json',
      label: 'Conversion Rates',
      placeholder: 'Define target conversion rates',
      required: false
    },
    content_roi_targets: {
      type: 'json',
      label: 'Content ROI Targets',
      placeholder: 'Define ROI targets for content',
      required: false
    },
    ab_testing_capabilities: {
      type: 'boolean',
      label: 'A/B Testing Capabilities',
      required: false
    }
  };

  // Get the field configuration with fallback
  const config = fieldConfig[fieldId] || {
    type: 'text',
    label: fieldId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    placeholder: `Enter ${fieldId.replace(/_/g, ' ')}`,
    required: false
  };

  const handleChange = (newValue: any) => {
    onChange(newValue);
    if (autoPopulated && !isEditing) {
      setIsEditing(true);
    }
  };

  const renderInput = () => {
    // Safety check for config
    if (!config) {
      return (
        <TextField
          fullWidth
          label={fieldId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
          value={value || ''}
          onChange={(e) => handleChange(e.target.value)}
          placeholder={`Enter ${fieldId.replace(/_/g, ' ')}`}
          error={!!error}
          helperText={error}
          required={false}
        />
      );
    }

    switch (config.type) {
      case 'text':
        return (
          <TextField
            fullWidth
            label={config.label || fieldId}
            value={value || ''}
            onChange={(e) => handleChange(e.target.value)}
            placeholder={(config as TextFieldConfig).placeholder || `Enter ${fieldId}`}
            error={!!error}
            helperText={error}
            required={config.required || false}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={onShowTooltip} size="small">
                    <HelpIcon />
                  </IconButton>
                </InputAdornment>
              )
            }}
          />
        );

      case 'number':
        return (
          <TextField
            fullWidth
            type="number"
            label={config.label || fieldId}
            value={value || ''}
            onChange={(e) => handleChange(Number(e.target.value))}
            placeholder={(config as TextFieldConfig).placeholder || `Enter ${fieldId}`}
            error={!!error}
            helperText={error}
            required={config.required || false}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={onShowTooltip} size="small">
                    <HelpIcon />
                  </IconButton>
                </InputAdornment>
              )
            }}
          />
        );

      case 'select':
        const selectConfig = config as SelectFieldConfig;
        return (
          <FormControl fullWidth error={!!error} required={config.required || false}>
            <InputLabel>{config.label || fieldId}</InputLabel>
            <Select
              value={value || ''}
              onChange={(e) => handleChange(e.target.value)}
              label={config.label || fieldId}
              endAdornment={
                <IconButton onClick={onShowTooltip} size="small">
                  <HelpIcon />
                </IconButton>
              }
            >
              {(selectConfig.options || []).map((option: string) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );

      case 'multiselect':
        const multiSelectConfig = config as MultiSelectFieldConfig;
        return (
          <Autocomplete
            multiple
            options={multiSelectConfig.options || []}
            value={Array.isArray(value) ? value : []}
            onChange={(_, newValue) => handleChange(newValue)}
            renderInput={(params) => (
              <TextField
                {...params}
                label={config.label || fieldId}
                placeholder={multiSelectConfig.placeholder || `Select ${fieldId}`}
                error={!!error}
                helperText={error}
                required={config.required || false}
                InputProps={{
                  ...params.InputProps,
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton onClick={onShowTooltip} size="small">
                        <HelpIcon />
                      </IconButton>
                    </InputAdornment>
                  )
                }}
              />
            )}
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip
                  label={option}
                  {...getTagProps({ index })}
                  key={option}
                />
              ))
            }
          />
        );

      case 'boolean':
        return (
          <FormControlLabel
            control={
              <Switch
                checked={!!value}
                onChange={(e) => handleChange(e.target.checked)}
              />
            }
            label={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {config.label || fieldId}
                <IconButton onClick={onShowTooltip} size="small">
                  <HelpIcon />
                </IconButton>
              </Box>
            }
          />
        );

      case 'json':
        return (
          <TextField
            fullWidth
            multiline
            rows={3}
            label={config.label || fieldId}
            value={typeof value === 'string' ? value : JSON.stringify(value, null, 2)}
            onChange={(e) => {
              try {
                const parsed = JSON.parse(e.target.value);
                handleChange(parsed);
              } catch {
                handleChange(e.target.value);
              }
            }}
            placeholder={(config as TextFieldConfig).placeholder || `Enter ${fieldId} as JSON`}
            error={!!error}
            helperText={error}
            required={config.required || false}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={onShowTooltip} size="small">
                    <HelpIcon />
                  </IconButton>
                </InputAdornment>
              )
            }}
          />
        );

      default:
        return (
          <TextField
            fullWidth
            label={(config as any).label || fieldId}
            value={value || ''}
            onChange={(e) => handleChange(e.target.value)}
            placeholder={`Enter ${fieldId}`}
            error={!!error}
            helperText={error}
            required={(config as any).required || false}
          />
        );
    }
  };

  return (
    <Box sx={{ position: 'relative' }}>
      {/* Auto-population indicator */}
      {autoPopulated && (
        <Box sx={{ mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
          <Chip
            icon={<AutoAwesomeIcon />}
            label={`Auto-populated from ${dataSource}`}
            color="info"
            size="small"
            variant="outlined"
          />
          {!isEditing && (
            <Tooltip title="Edit auto-populated value">
              <IconButton size="small" onClick={() => setIsEditing(true)}>
                <EditIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
        </Box>
      )}

      {/* Field input */}
      {renderInput()}

      {/* Validation status */}
      {value && !error && (
        <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
          <CheckCircleIcon color="success" fontSize="small" />
          <Typography variant="caption" color="success.main">
            Valid
          </Typography>
        </Box>
      )}

      {/* Error display */}
      {error && (
        <Alert severity="error" sx={{ mt: 1 }}>
          <Typography variant="body2">{error}</Typography>
        </Alert>
      )}
    </Box>
  );
};

export default StrategicInputField; 