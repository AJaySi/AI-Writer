import React from 'react';
import {
  Box,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Grid,
  Card,
  CardContent,
  Tooltip,
  IconButton,
  Alert,
  FormHelperText
} from '@mui/material';
import {
  CalendarToday as CalendarIcon,
  Schedule as ScheduleIcon,
  Help as HelpIcon,
  TrendingUp as TrendingUpIcon,
  Public as PublicIcon,
  AccessTime as AccessTimeIcon,
  ContentPaste as ContentPasteIcon
} from '@mui/icons-material';

// Import calendar-specific types
import { type CalendarConfig } from './types';

interface CalendarConfigurationStepProps {
  calendarConfig: CalendarConfig;
  onConfigUpdate: (updates: Partial<CalendarConfig>) => void;
  strategyContext?: any;
  isFromStrategyActivation?: boolean; // Strategy context available for generation
}

// Enhanced styling with better input prominence and readability
const ENHANCED_STYLES = {
  card: {
    borderRadius: 2,
    background: 'rgba(255, 255, 255, 0.95)',
    color: '#333',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
    border: '1px solid rgba(0, 0, 0, 0.1)',
    position: 'relative' as const,
    overflow: 'hidden',
    '&:hover': {
      boxShadow: '0 6px 25px rgba(0, 0, 0, 0.15)',
      transform: 'translateY(-2px)'
    },
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
  },
  cardContent: {
    p: 3,
    position: 'relative' as const,
    zIndex: 1
  },
  sectionHeader: {
    display: 'flex',
    alignItems: 'center',
    mb: 3,
    '& .MuiTypography-root': {
      fontWeight: 600,
      color: '#2c3e50'
    }
  },
  iconContainer: {
    p: 1.5,
    borderRadius: 2,
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    mr: 2,
    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  formControl: {
    '& .MuiInputLabel-root': {
      color: '#555',
      fontWeight: 500,
      '&.Mui-focused': {
        color: '#667eea'
      }
    },
    '& .MuiOutlinedInput-root': {
      color: '#333',
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      '& fieldset': {
        borderColor: 'rgba(0, 0, 0, 0.2)',
        borderWidth: '2px'
      },
      '&:hover fieldset': {
        borderColor: 'rgba(102, 126, 234, 0.5)'
      },
      '&.Mui-focused fieldset': {
        borderColor: '#667eea',
        borderWidth: '2px'
      }
    },
    '& .MuiSelect-icon': {
      color: '#555'
    }
  },
  textField: {
    '& .MuiInputLabel-root': {
      color: '#555',
      fontWeight: 500,
      '&.Mui-focused': {
        color: '#667eea'
      }
    },
    '& .MuiOutlinedInput-root': {
      color: '#333',
      backgroundColor: 'rgba(255, 255, 255, 0.8)',
      '& fieldset': {
        borderColor: 'rgba(0, 0, 0, 0.2)',
        borderWidth: '2px'
      },
      '&:hover fieldset': {
        borderColor: 'rgba(102, 126, 234, 0.5)'
      },
      '&.Mui-focused fieldset': {
        borderColor: '#667eea',
        borderWidth: '2px'
      }
    }
  },
  platformCard: {
    background: 'rgba(255, 255, 255, 0.9)',
    border: '2px solid rgba(0, 0, 0, 0.1)',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    '&:hover': {
      background: 'rgba(102, 126, 234, 0.05)',
      border: '2px solid rgba(102, 126, 234, 0.3)',
      transform: 'translateY(-2px)'
    },
    '&.selected': {
      background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
      border: '2px solid rgba(102, 126, 234, 0.5)',
      boxShadow: '0 4px 12px rgba(102, 126, 234, 0.2)'
    }
  },
  checkbox: {
    color: '#b0b0b0',
    '&.Mui-checked': {
      color: '#667eea'
    }
  }
};

const CalendarConfigurationStep: React.FC<CalendarConfigurationStepProps> = ({
  calendarConfig,
  onConfigUpdate,
  strategyContext,
  isFromStrategyActivation = false
}) => {
  // Enhanced calendar-specific handlers
  const handleCalendarTypeChange = (type: 'weekly' | 'monthly' | 'quarterly') => {
    onConfigUpdate({ calendarType: type });
  };

  const handleDurationChange = (duration: number) => {
    onConfigUpdate({ calendarDuration: duration });
  };

  const handleStartDateChange = (date: string) => {
    onConfigUpdate({ startDate: date });
  };

  const handlePostingFrequencyChange = (frequency: number) => {
    onConfigUpdate({ postingFrequency: frequency });
  };

  const handleContentVolumeChange = (volume: number) => {
    onConfigUpdate({ contentVolume: volume });
  };

  const handlePlatformChange = (platform: string, checked: boolean) => {
    let newPlatforms = [...(calendarConfig.priorityPlatforms || [])];
    if (checked) {
      newPlatforms.push(platform);
    } else {
      newPlatforms = newPlatforms.filter(p => p !== platform);
    }
    onConfigUpdate({ priorityPlatforms: newPlatforms });
  };

  const handleTimeZoneChange = (timezone: string) => {
    onConfigUpdate({ timeZone: timezone });
  };

  const handleContentDistributionChange = (distribution: 'even' | 'frontloaded' | 'backloaded') => {
    onConfigUpdate({ contentDistribution: distribution });
  };

  const handleReviewCycleChange = (cycle: 'weekly' | 'monthly' | 'quarterly') => {
    onConfigUpdate({ reviewCycle: cycle });
  };

  const availablePlatforms = [
    { value: 'LinkedIn', label: 'LinkedIn', icon: '💼', description: 'Professional networking and B2B content' },
    { value: 'Twitter', label: 'Twitter/X', icon: '🐦', description: 'Real-time updates and engagement' },
    { value: 'Facebook', label: 'Facebook', icon: '📘', description: 'Community building and brand awareness' },
    { value: 'Instagram', label: 'Instagram', icon: '📸', description: 'Visual content and storytelling' },
    { value: 'YouTube', label: 'YouTube', icon: '📺', description: 'Video content and tutorials' },
    { value: 'Blog', label: 'Blog/Website', icon: '📝', description: 'Long-form content and SEO' },
    { value: 'Email', label: 'Email Newsletter', icon: '📧', description: 'Direct communication and nurturing' }
  ];

  const timeZones = [
    { value: 'America/New_York', label: 'Eastern Time (ET)' },
    { value: 'America/Chicago', label: 'Central Time (CT)' },
    { value: 'America/Denver', label: 'Mountain Time (MT)' },
    { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
    { value: 'Europe/London', label: 'London (GMT/BST)' },
    { value: 'Europe/Paris', label: 'Paris (CET/CEST)' },
    { value: 'Asia/Tokyo', label: 'Tokyo (JST)' },
    { value: 'Asia/Shanghai', label: 'Shanghai (CST)' },
    { value: 'Australia/Sydney', label: 'Sydney (AEST/AEDT)' }
  ];

  return (
    <Box sx={{ p: 2 }}>
      {/* Header with Strategy Context */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ 
          fontWeight: 700,
          color: '#2c3e50',
          mb: 1
        }}>
          Calendar Configuration
      </Typography>
        
        <Typography variant="body1" color="#555" sx={{ mb: 2 }}>
          Configure your content calendar settings to create an optimized publishing schedule.
      </Typography>

        {isFromStrategyActivation && (
          <Alert severity="success" sx={{ 
            background: 'rgba(76, 175, 80, 0.1)', 
            border: '1px solid rgba(76, 175, 80, 0.3)',
            color: '#2e7d32'
          }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <TrendingUpIcon />
              <Typography variant="body2">
                Strategy context available - your activated strategy will enhance calendar generation
              </Typography>
            </Box>
          </Alert>
        )}
      </Box>

      {/* Basic Calendar Setup */}
      <Card sx={{ ...ENHANCED_STYLES.card, mb: 3 }}>
        <CardContent sx={ENHANCED_STYLES.cardContent}>
          <Box sx={ENHANCED_STYLES.sectionHeader}>
            <Box sx={ENHANCED_STYLES.iconContainer}>
              <CalendarIcon sx={{ color: 'white', fontSize: 24 }} />
            </Box>
            <Typography variant="h5">
              Basic Calendar Setup
            </Typography>
            <Tooltip title="Configure the fundamental structure of your content calendar">
              <IconButton size="small" sx={{ ml: 1, color: '#555' }}>
                <HelpIcon />
                  </IconButton>
                </Tooltip>
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth sx={ENHANCED_STYLES.formControl}>
                <InputLabel>Calendar Type</InputLabel>
                <Select
                  value={calendarConfig.calendarType}
                  onChange={(e) => handleCalendarTypeChange(e.target.value as 'weekly' | 'monthly' | 'quarterly')}
                  label="Calendar Type"
                >
                  <MenuItem value="weekly">
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <span>📅</span>
                      <Box>
                        <Typography variant="body2" fontWeight={600}>Weekly</Typography>
                        <Typography variant="caption" color="#666">7-day planning cycles</Typography>
                      </Box>
                    </Box>
                  </MenuItem>
                  <MenuItem value="monthly">
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <span>📆</span>
                      <Box>
                        <Typography variant="body2" fontWeight={600}>Monthly</Typography>
                        <Typography variant="caption" color="#666">30-day planning cycles</Typography>
                      </Box>
                    </Box>
                  </MenuItem>
                  <MenuItem value="quarterly">
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <span>📊</span>
                      <Box>
                        <Typography variant="body2" fontWeight={600}>Quarterly</Typography>
                        <Typography variant="caption" color="#666">90-day strategic planning</Typography>
                      </Box>
                    </Box>
                  </MenuItem>
                </Select>
                <FormHelperText sx={{ color: '#666' }}>
                  Choose your planning cycle - affects content volume and scheduling
                </FormHelperText>
              </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Start Date"
                type="date"
                value={calendarConfig.startDate}
                onChange={(e) => handleStartDateChange(e.target.value)}
                InputLabelProps={{ shrink: true }}
                sx={ENHANCED_STYLES.textField}
                InputProps={{
                  startAdornment: <AccessTimeIcon sx={{ mr: 1, color: '#666' }} />
                }}
              />
              <FormHelperText sx={{ color: '#666' }}>
                When should your calendar begin?
              </FormHelperText>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Duration (periods)"
                type="number"
                value={calendarConfig.calendarDuration}
                onChange={(e) => handleDurationChange(parseInt(e.target.value) || 1)}
                inputProps={{ min: 1, max: 52 }}
                sx={ENHANCED_STYLES.textField}
                InputProps={{
                  startAdornment: <ContentPasteIcon sx={{ mr: 1, color: '#666' }} />
                }}
              />
              <FormHelperText sx={{ color: '#666' }}>
                Number of {calendarConfig.calendarType === 'weekly' ? 'weeks' : 
                calendarConfig.calendarType === 'monthly' ? 'months' : 'quarters'} to generate
              </FormHelperText>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Posts per Week"
                type="number"
                value={calendarConfig.postingFrequency}
                onChange={(e) => handlePostingFrequencyChange(parseInt(e.target.value) || 1)}
                inputProps={{ min: 1, max: 7 }}
                sx={ENHANCED_STYLES.textField}
                InputProps={{
                  startAdornment: <ScheduleIcon sx={{ mr: 1, color: '#666' }} />
                }}
              />
              <FormHelperText sx={{ color: '#666' }}>
                How many posts should be published weekly?
              </FormHelperText>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Content Volume per Period"
                type="number"
                value={calendarConfig.contentVolume}
                onChange={(e) => handleContentVolumeChange(parseInt(e.target.value) || 1)}
                inputProps={{ min: 1 }}
                sx={ENHANCED_STYLES.textField}
                InputProps={{
                  startAdornment: <ContentPasteIcon sx={{ mr: 1, color: '#666' }} />
                }}
              />
              <FormHelperText sx={{ color: '#666' }}>
                Total content pieces per {calendarConfig.calendarType === 'weekly' ? 'week' : 
                calendarConfig.calendarType === 'monthly' ? 'month' : 'quarter'}
              </FormHelperText>
            </Grid>
          </Grid>
            </CardContent>
          </Card>

      {/* Platform & Scheduling Preferences */}
      <Card sx={{ ...ENHANCED_STYLES.card, mb: 3 }}>
        <CardContent sx={ENHANCED_STYLES.cardContent}>
          <Box sx={ENHANCED_STYLES.sectionHeader}>
            <Box sx={ENHANCED_STYLES.iconContainer}>
              <PublicIcon sx={{ color: 'white', fontSize: 24 }} />
            </Box>
            <Typography variant="h5">
              Platform & Scheduling Preferences
            </Typography>
            <Tooltip title="Select your content distribution platforms and scheduling preferences">
              <IconButton size="small" sx={{ ml: 1, color: '#555' }}>
                <HelpIcon />
                  </IconButton>
                </Tooltip>
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom sx={{ color: '#2c3e50', mb: 2 }}>
                Priority Platforms
              </Typography>
              <Typography variant="body2" color="#666" sx={{ mb: 2 }}>
                Select the platforms where you'll publish your content. Choose platforms that align with your audience and content strategy.
              </Typography>
              <Grid container spacing={2}>
                {availablePlatforms.map((platform) => (
                  <Grid item xs={12} sm={6} md={4} key={platform.value}>
                    <Card 
                      sx={{ 
                        ...ENHANCED_STYLES.platformCard,
                        ...(calendarConfig.priorityPlatforms.includes(platform.value) && { className: 'selected' })
                      }}
                      onClick={() => handlePlatformChange(platform.value, !calendarConfig.priorityPlatforms.includes(platform.value))}
                    >
                      <CardContent sx={{ p: 2 }}>
                  <FormControlLabel
                    control={
                      <Checkbox
                              checked={calendarConfig.priorityPlatforms.includes(platform.value)}
                        onChange={(e) => handlePlatformChange(platform.value, e.target.checked)}
                              sx={ENHANCED_STYLES.checkbox}
                            />
                          }
                          label={
                            <Box>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                                <span style={{ fontSize: '1.2rem' }}>{platform.icon}</span>
                                <Typography variant="body2" fontWeight={600} color="#2c3e50">
                                  {platform.label}
                                </Typography>
                              </Box>
                              <Typography variant="caption" color="#666">
                                {platform.description}
                              </Typography>
                            </Box>
                          }
                          sx={{ m: 0, width: '100%' }}
                        />
            </CardContent>
          </Card>
        </Grid>
                ))}
              </Grid>
        </Grid>

            <Grid item xs={12} md={6}>
              <FormControl fullWidth sx={ENHANCED_STYLES.formControl}>
                <InputLabel>Time Zone</InputLabel>
                    <Select
                  value={calendarConfig.timeZone}
                  onChange={(e) => handleTimeZoneChange(e.target.value)}
                  label="Time Zone"
                >
                  {timeZones.map((tz) => (
                    <MenuItem key={tz.value} value={tz.value}>
                      {tz.label}
                    </MenuItem>
                  ))}
                    </Select>
                <FormHelperText sx={{ color: '#666' }}>Your local timezone for accurate scheduling</FormHelperText>
                  </FormControl>
                </Grid>
                
            <Grid item xs={12} md={6}>
              <FormControl fullWidth sx={ENHANCED_STYLES.formControl}>
                <InputLabel>Content Distribution</InputLabel>
                    <Select
                  value={calendarConfig.contentDistribution}
                  onChange={(e) => handleContentDistributionChange(e.target.value as 'even' | 'frontloaded' | 'backloaded')}
                  label="Content Distribution"
                >
                  <MenuItem value="even">
                    <Box>
                      <Typography variant="body2" fontWeight={600}>Even Distribution</Typography>
                      <Typography variant="caption" color="#666">Consistent posting throughout the period</Typography>
                    </Box>
                  </MenuItem>
                  <MenuItem value="frontloaded">
                    <Box>
                      <Typography variant="body2" fontWeight={600}>Front-loaded</Typography>
                      <Typography variant="caption" color="#666">More content at the beginning</Typography>
                    </Box>
                  </MenuItem>
                  <MenuItem value="backloaded">
                    <Box>
                      <Typography variant="body2" fontWeight={600}>Back-loaded</Typography>
                      <Typography variant="caption" color="#666">More content towards the end</Typography>
                    </Box>
                  </MenuItem>
                    </Select>
                <FormHelperText sx={{ color: '#666' }}>How should content be distributed across the period?</FormHelperText>
                  </FormControl>
                </Grid>
                
            <Grid item xs={12} md={6}>
              <FormControl fullWidth sx={ENHANCED_STYLES.formControl}>
                <InputLabel>Review Cycle</InputLabel>
                    <Select
                  value={calendarConfig.reviewCycle}
                  onChange={(e) => handleReviewCycleChange(e.target.value as 'weekly' | 'monthly' | 'quarterly')}
                  label="Review Cycle"
                >
                  <MenuItem value="weekly">
                    <Box>
                      <Typography variant="body2" fontWeight={600}>Weekly</Typography>
                      <Typography variant="caption" color="#666">Review and adjust every week</Typography>
                    </Box>
                  </MenuItem>
                  <MenuItem value="monthly">
                    <Box>
                      <Typography variant="body2" fontWeight={600}>Monthly</Typography>
                      <Typography variant="caption" color="#666">Review and adjust every month</Typography>
                    </Box>
                  </MenuItem>
                  <MenuItem value="quarterly">
                    <Box>
                      <Typography variant="body2" fontWeight={600}>Quarterly</Typography>
                      <Typography variant="caption" color="#666">Review and adjust every quarter</Typography>
                    </Box>
                  </MenuItem>
                    </Select>
                <FormHelperText sx={{ color: '#666' }}>How often should you review and adjust your calendar?</FormHelperText>
                  </FormControl>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
    </Box>
  );
};

export default CalendarConfigurationStep;
