import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Chip,
  IconButton,
  Tooltip as MuiTooltip,
  Card,
  CardContent,
  Grid,
  Divider,
  CircularProgress,
  Badge,
  Collapse,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Business as BusinessIcon,
  People as PeopleIcon,
  TrendingUp as TrendingUpIcon,
  ContentPaste as ContentIcon,
  Analytics as AnalyticsIcon,
  Help as HelpIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  AutoAwesome as AutoAwesomeIcon,
  Refresh as RefreshIcon,
  Save as SaveIcon,
  ArrowForward as ArrowForwardIcon,
  ArrowBack as ArrowBackIcon,
  Assessment as AssessmentIcon,
  ExpandMore as ExpandMoreIcon,
  Info as InfoIcon,
  Visibility as VisibilityIcon,
  School as SchoolIcon,
  Lightbulb as LightbulbIcon,
  Psychology as PsychologyIcon,
  Timeline as TimelineIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useEnhancedStrategyStore, STRATEGIC_INPUT_FIELDS } from '../../../stores/enhancedStrategyStore';
import StrategicInputField from './StrategicInputField';
import EnhancedTooltip from './EnhancedTooltip';
import AIRecommendationsPanel from './AIRecommendationsPanel';
import DataSourceTransparency from './DataSourceTransparency';

const EnhancedStrategyBuilder: React.FC = () => {
  const {
    formData,
    formErrors,
    autoPopulatedFields,
    dataSources,
    loading,
    error,
    saving,
    aiGenerating,
    currentStep,
    completedSteps,
    disclosureSteps,
    currentStrategy,
    updateFormField,
    validateFormField,
    validateAllFields,
    completeStep,
    getNextStep,
    getPreviousStep,
    setCurrentStep,
    canProceedToStep,
    resetForm,
    autoPopulateFromOnboarding,
    generateAIRecommendations,
    createEnhancedStrategy,
    calculateCompletionPercentage,
    getCompletionStats,
    setError,
    setCurrentStrategy,
    setAIGenerating,
    setSaving
  } = useEnhancedStrategyStore();

  const [showTooltip, setShowTooltip] = useState<string | null>(null);
  const [autoPopulateAttempted, setAutoPopulateAttempted] = useState(false);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [showEducationalInfo, setShowEducationalInfo] = useState<string | null>(null);
  const [showAIRecommendations, setShowAIRecommendations] = useState(false);
  const [showDataSourceTransparency, setShowDataSourceTransparency] = useState(false);

  // Auto-populate from onboarding on first load
  useEffect(() => {
    if (!autoPopulateAttempted) {
      autoPopulateFromOnboarding();
      setAutoPopulateAttempted(true);
    }
  }, [autoPopulateAttempted, autoPopulateFromOnboarding]);

  const handleCreateStrategy = async () => {
    try {
      setAIGenerating(true);
      setError(null);
      
      console.log('Starting strategy creation...');
      console.log('Current formData:', formData);
      console.log('FormData ID:', formData.id);

      // If we have a saved strategy, use its ID
      if (formData.id) {
        console.log('Using existing strategy ID:', formData.id);
        await generateAIRecommendations(formData.id);
      } else {
        console.log('No strategy ID found, creating new strategy...');
        // If no strategy is saved yet, save it first, then generate AI insights
        const isValid = validateAllFields();
        console.log('Form validation result:', isValid);
      
      if (isValid) {
          const completionStats = getCompletionStats();
          const strategyData = {
            ...formData,
            completion_percentage: completionStats.completion_percentage,
            user_id: 1, // This would come from auth context
            name: formData.name || 'Enhanced Content Strategy',
            industry: formData.industry || 'General'
          };

          console.log('Attempting to create strategy with data:', strategyData);
          const newStrategy = await createEnhancedStrategy(strategyData);
          console.log('New strategy created:', newStrategy);

          if (newStrategy && newStrategy.id) {
            console.log('Generating AI recommendations for new strategy ID:', newStrategy.id);
            await generateAIRecommendations(newStrategy.id);
            
            // Set the current strategy and show success message
            setCurrentStrategy(newStrategy);
            setError(null); // Clear any previous errors
            
            // Show success message
            setTimeout(() => {
              setError('Strategy created successfully! Check the Strategic Intelligence tab for detailed insights.');
            }, 100);
            
            // Auto-switch to Strategic Intelligence tab after creation
            // This would need to be handled by the parent component
          } else {
            setError('Failed to create strategy or get strategy ID for AI generation.');
            console.error('Failed to create strategy or get strategy ID for AI generation.');
          }
        } else {
          setError('Please fill in all required fields before generating AI insights.');
          console.error('Form validation failed. Cannot generate AI insights.');
        }
      }
    } catch (err: any) {
      setError(`Error generating AI recommendations: ${err.message || 'Unknown error'}`);
      console.error('Error in handleCreateStrategy:', err);
    } finally {
      setAIGenerating(false);
    }
  };

  const handleSaveStrategy = async () => {
    try {
      setSaving(true);
      setError(null);
      
      const completionStats = getCompletionStats();
      const strategyData = {
        ...formData,
        completion_percentage: completionStats.completion_percentage,
        user_id: 1,
        name: formData.name || 'Enhanced Content Strategy',
        industry: formData.industry || 'General'
      };
      
      const newStrategy = await createEnhancedStrategy(strategyData);
      setCurrentStrategy(newStrategy);
      setError('Strategy saved successfully!');
    } catch (err: any) {
      setError(`Error saving strategy: ${err.message || 'Unknown error'}`);
    } finally {
      setSaving(false);
    }
  };

  const handleReviewCategory = (categoryId: string) => {
    setActiveCategory(activeCategory === categoryId ? null : categoryId);
  };

  const handleShowEducationalInfo = (categoryId: string) => {
    setShowEducationalInfo(showEducationalInfo === categoryId ? null : categoryId);
  };

  const getCategoryIcon = (categoryId: string) => {
    switch (categoryId) {
      case 'business_context': return <BusinessIcon />;
      case 'audience_intelligence': return <PeopleIcon />;
      case 'competitive_intelligence': return <TrendingUpIcon />;
      case 'content_strategy': return <ContentIcon />;
      case 'performance_analytics': return <AnalyticsIcon />;
      default: return <HelpIcon />;
    }
  };

  const getCategoryColor = (categoryId: string) => {
    switch (categoryId) {
      case 'business_context': return 'primary';
      case 'audience_intelligence': return 'secondary';
      case 'competitive_intelligence': return 'success';
      case 'content_strategy': return 'warning';
      case 'performance_analytics': return 'info';
      default: return 'default';
    }
  };

  const getEducationalContent = (categoryId: string) => {
    switch (categoryId) {
      case 'business_context':
        return {
          title: 'Business Context',
          description: 'Understanding your business foundation is crucial for content strategy success.',
          points: [
            'Business objectives define what you want to achieve through content',
            'Target metrics help measure the success of your content strategy',
            'Content budget determines the scope and scale of your content efforts',
            'Team size affects content production capacity and frequency',
            'Implementation timeline sets realistic expectations for strategy rollout'
          ],
          tips: [
            'Be specific about your business goals',
            'Set measurable and achievable metrics',
            'Consider your available resources realistically'
          ]
        };
      case 'audience_intelligence':
        return {
          title: 'Audience Intelligence',
          description: 'Deep understanding of your audience drives content relevance and engagement.',
          points: [
            'Content preferences reveal what formats resonate with your audience',
            'Consumption patterns show when and how your audience engages',
            'Pain points help create content that solves real problems',
            'Buying journey mapping guides content at each stage',
            'Seasonal trends identify content opportunities throughout the year'
          ],
          tips: [
            'Research your audience thoroughly',
            'Create audience personas for better targeting',
            'Monitor engagement patterns regularly'
          ]
        };
      case 'competitive_intelligence':
        return {
          title: 'Competitive Intelligence',
          description: 'Understanding your competitive landscape helps differentiate your content.',
          points: [
            'Top competitors analysis reveals content gaps and opportunities',
            'Competitor strategies show what works in your industry',
            'Market gaps identify underserved content areas',
            'Industry trends keep your content current and relevant',
            'Emerging trends provide first-mover advantages'
          ],
          tips: [
            'Monitor competitors regularly',
            'Identify unique angles and perspectives',
            'Stay ahead of industry trends'
          ]
        };
      case 'content_strategy':
        return {
          title: 'Content Strategy',
          description: 'Your content approach defines how you\'ll achieve your business objectives.',
          points: [
            'Preferred formats align with audience preferences and business goals',
            'Content mix balances different types of content for maximum impact',
            'Content frequency should match audience expectations and team capacity',
            'Optimal timing maximizes content visibility and engagement',
            'Quality metrics ensure content meets audience standards'
          ],
          tips: [
            'Balance audience preferences with business goals',
            'Set realistic content production schedules',
            'Maintain consistent quality standards'
          ]
        };
      case 'performance_analytics':
        return {
          title: 'Performance & Analytics',
          description: 'Data-driven insights optimize your content strategy for better results.',
          points: [
            'Traffic sources show where your audience comes from',
            'Conversion rates measure content effectiveness',
            'ROI targets help justify content marketing investments',
            'A/B testing capabilities enable continuous optimization',
            'Regular analysis identifies improvement opportunities'
          ],
          tips: [
            'Track key metrics consistently',
            'Use data to inform content decisions',
            'Continuously optimize based on performance'
          ]
        };
      default:
        return {
          title: 'Category Information',
          description: 'Learn more about this content strategy category.',
          points: [],
          tips: []
        };
    }
  };

  const completionStats = getCompletionStats();
  const completionPercentage = calculateCompletionPercentage();

  return (
    <Box sx={{ p: 3 }}>
      {/* Header with Title (Region B) */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper 
          sx={{ 
            p: 3, 
            mb: 3, 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 2
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box>
              <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
                Enhanced Strategy Builder
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.9 }}>
                Build a comprehensive content strategy with 30+ strategic inputs
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
              {/* AI Recommendations Button */}
              <MuiTooltip title="View AI-powered recommendations and insights" placement="top">
                <IconButton 
                  onClick={() => setShowAIRecommendations(true)}
                  sx={{ 
                    color: 'white', 
                    bgcolor: 'rgba(255,255,255,0.1)',
                    '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' }
                  }}
                >
                  <Badge badgeContent={5} color="secondary">
                    <AutoAwesomeIcon />
                  </Badge>
                </IconButton>
              </MuiTooltip>
              
              {/* Data Source Transparency Button */}
              <MuiTooltip title="View data sources and transparency information" placement="top">
                <IconButton 
                  onClick={() => setShowDataSourceTransparency(true)}
                  sx={{ 
                    color: 'white', 
                    bgcolor: 'rgba(255,255,255,0.1)',
                    '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' }
                  }}
                >
                  <Badge badgeContent={Object.keys(autoPopulatedFields || {}).length} color="info">
                    <InfoIcon />
                  </Badge>
                </IconButton>
              </MuiTooltip>
              
              {/* Refresh Button */}
              <MuiTooltip title="Refresh auto-populated data" placement="top">
                <IconButton 
                  onClick={autoPopulateFromOnboarding}
                  sx={{ 
                    color: 'white', 
                    bgcolor: 'rgba(255,255,255,0.1)',
                    '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' }
                  }}
                >
                  <RefreshIcon />
                </IconButton>
              </MuiTooltip>
            </Box>
          </Box>
        </Paper>
      </motion.div>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Success Alert */}
      {!error && currentStrategy && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Strategy "{currentStrategy.name}" created successfully! Check the Strategic Intelligence tab for detailed insights.
        </Alert>
      )}

      {/* Strategy Display */}
      {currentStrategy && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Created Strategy: {currentStrategy.name}
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Industry: {currentStrategy.industry}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                Completion: {currentStrategy.completion_percentage}%
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="text.secondary">
                Created: {new Date(currentStrategy.created_at).toLocaleDateString()}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                ID: {currentStrategy.id}
              </Typography>
            </Grid>
          </Grid>
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              onClick={() => window.location.href = '/content-planning?tab=strategic-intelligence'}
              startIcon={<AssessmentIcon />}
            >
              View Strategic Intelligence
            </Button>
          </Box>
        </Paper>
      )}

      {/* Auto-population Status */}
      {autoPopulatedFields && Object.keys(autoPopulatedFields).length > 0 && (
        <Alert 
          severity="info" 
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={autoPopulateFromOnboarding}>
              <RefreshIcon />
            </Button>
          }
        >
          {autoPopulatedFields && Object.keys(autoPopulatedFields).length} fields auto-populated from onboarding data
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Category Overview Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: 'fit-content', position: 'sticky', top: 20 }}>
            {/* Enhanced Completion Tracker - Integrated into Category List */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Strategy Progress
              </Typography>
              
              {/* Overall Progress with Status */}
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Overall Completion
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {Math.round(completionPercentage)}%
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={completionPercentage} 
                  sx={{ height: 8, borderRadius: 4 }}
                />
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  {completionStats.filled_fields} of {completionStats.total_fields} fields completed
                </Typography>
              </Box>

              {/* Status Chip */}
              <Box sx={{ mb: 2 }}>
                <Chip
                  label={
                    completionPercentage >= 90 ? 'Excellent' :
                    completionPercentage >= 70 ? 'Good' :
                    completionPercentage >= 50 ? 'Fair' : 'Needs Work'
                  }
                  color={
                    completionPercentage >= 90 ? 'success' :
                    completionPercentage >= 70 ? 'primary' :
                    completionPercentage >= 50 ? 'warning' : 'error'
                  }
                  size="small"
                  icon={<TrendingUpIcon />}
                />
              </Box>

              {/* Motivational Message */}
              {completionPercentage > 0 && completionPercentage < 100 && (
                <Alert severity="info" sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    {completionPercentage < 30 && "Great start! Keep going to unlock AI insights."}
                    {completionPercentage >= 30 && completionPercentage < 60 && "You're making excellent progress! Consider reviewing completed categories."}
                    {completionPercentage >= 60 && completionPercentage < 90 && "Almost there! Just a few more fields to complete your strategy."}
                    {completionPercentage >= 90 && "Excellent work! Your strategy is nearly complete."}
                  </Typography>
                </Alert>
              )}

              {/* Status Indicators */}
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <CheckCircleIcon color="success" fontSize="small" />
                  <Typography variant="body2" color="text.secondary">
                    Auto-population: {Object.keys(autoPopulatedFields || {}).length} fields
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AutoAwesomeIcon color="primary" fontSize="small" />
                  <Typography variant="body2" color="text.secondary">
                    AI Insights: {aiGenerating ? 'Generating...' : 'Ready'}
                  </Typography>
                </Box>
              </Box>
            </Box>

            {/* Category Progress - Integrated with CompletionTracker functionality */}
            <Typography variant="h6" gutterBottom>
              Category Progress
            </Typography>
            
            <List sx={{ p: 0 }}>
              {Object.entries(completionStats.category_completion).map(([categoryId, percentage]) => {
                const category = STRATEGIC_INPUT_FIELDS.find(f => f.category === categoryId);
                const categoryName = categoryId.split('_').map(word => 
                  word.charAt(0).toUpperCase() + word.slice(1)
                ).join(' ');
                
                // Get category-specific stats
                const categoryFields = STRATEGIC_INPUT_FIELDS.filter(f => f.category === categoryId);
                const filledFields = categoryFields.filter(field => formData[field.id]).length;
                const totalFields = categoryFields.length;
                
                // Get status for this category
                const getCategoryStatus = (percentage: number) => {
                  if (percentage >= 90) return { status: 'Complete', color: 'success' as const };
                  if (percentage >= 70) return { status: 'Good', color: 'primary' as const };
                  if (percentage >= 50) return { status: 'Fair', color: 'warning' as const };
                  return { status: 'Needs Work', color: 'error' as const };
                };
                
                const categoryStatus = getCategoryStatus(percentage);
                
                return (
                  <motion.div
                    key={categoryId}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <ListItem 
                      sx={{ 
                        p: 2, 
                        mb: 1, 
                        borderRadius: 2,
                        bgcolor: activeCategory === categoryId ? 'action.hover' : 'transparent',
                        border: activeCategory === categoryId ? '2px solid' : '1px solid',
                        borderColor: activeCategory === categoryId ? 'primary.main' : 'divider',
                        flexDirection: 'column',
                        alignItems: 'stretch'
                      }}
                    >
                      {/* Category Header */}
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', mb: 1 }}>
                        <ListItemIcon>
                          {getCategoryIcon(categoryId)}
                        </ListItemIcon>
                        <ListItemText
                          primary={categoryName}
                          secondary={`${Math.round(percentage)}% complete`}
                          sx={{ flex: 1 }}
                        />
                        <Chip
                          label={categoryStatus.status}
                          color={categoryStatus.color}
                          size="small"
                          sx={{ mr: 1 }}
                        />
                      </Box>
                      
                      {/* Category Progress Bar */}
                      <Box sx={{ mb: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={percentage}
                          sx={{ 
                            height: 4, 
                            borderRadius: 2,
                            bgcolor: 'action.hover'
                          }}
                        />
                        <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                          {filledFields} of {totalFields} fields completed
                        </Typography>
                      </Box>
                      
                      {/* Category Actions */}
                      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'space-between', alignItems: 'center' }}>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          {/* Review Button */}
                          <Button
                            size="small"
                            variant="outlined"
                            startIcon={<VisibilityIcon />}
                            onClick={() => handleReviewCategory(categoryId)}
                            sx={{ minWidth: 'auto' }}
                          >
                            Review
                          </Button>
                          
                          {/* Educational Info Button */}
                          <IconButton
                            size="small"
                            onClick={() => handleShowEducationalInfo(categoryId)}
                            sx={{ color: 'primary.main' }}
                          >
                            <SchoolIcon />
                          </IconButton>
                        </Box>
                        
                        {/* Category Status Indicator */}
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                          {percentage >= 90 ? (
                            <CheckCircleIcon color="success" fontSize="small" />
                          ) : percentage >= 70 ? (
                            <TrendingUpIcon color="primary" fontSize="small" />
                          ) : (
                            <WarningIcon color="warning" fontSize="small" />
                          )}
                        </Box>
                      </Box>
                    </ListItem>
                  </motion.div>
                );
              })}
            </List>
            
            {/* Quick Actions */}
            <Box sx={{ mt: 3, pt: 2, borderTop: 1, borderColor: 'divider' }}>
              <Typography variant="subtitle2" gutterBottom>
                Quick Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<AutoAwesomeIcon />}
                  onClick={() => setShowAIRecommendations(true)}
                  fullWidth
                >
                  View AI Insights
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<InfoIcon />}
                  onClick={() => setShowDataSourceTransparency(true)}
                  fullWidth
                >
                  View Data Sources
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={autoPopulateFromOnboarding}
                  fullWidth
                >
                  Refresh Data
                </Button>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Main Content Area */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, minHeight: '600px' }}>
            {activeCategory ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                {/* Category Header */}
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  {getCategoryIcon(activeCategory)}
                  <Typography variant="h5" sx={{ ml: 1 }}>
                    {activeCategory.split('_').map(word => 
                      word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ')}
                  </Typography>
                  <Chip 
                    label={`${Math.round(completionStats.category_completion[activeCategory])}% Complete`}
                    color={getCategoryColor(activeCategory) as any}
                    sx={{ ml: 'auto' }}
                  />
                </Box>

                {/* Educational Info Dialog */}
                <Dialog 
                  open={!!showEducationalInfo} 
                  onClose={() => setShowEducationalInfo(null)}
                  maxWidth="md"
                  fullWidth
                >
                  <DialogTitle>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <SchoolIcon />
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).title}
                    </Box>
                  </DialogTitle>
                  <DialogContent>
                    <Typography variant="body1" paragraph>
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).description}
                    </Typography>
                    
                    <Typography variant="h6" gutterBottom>
                      Key Points:
                    </Typography>
                    <List>
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).points.map((point, index) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemIcon>
                            <LightbulbIcon color="primary" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText primary={point} />
                        </ListItem>
                      ))}
                    </List>
                    
                <Typography variant="h6" gutterBottom>
                      Pro Tips:
                </Typography>
                    <List>
                      {showEducationalInfo && getEducationalContent(showEducationalInfo).tips.map((tip, index) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemIcon>
                            <PsychologyIcon color="secondary" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText primary={tip} />
                        </ListItem>
                      ))}
                    </List>
                  </DialogContent>
                  <DialogActions>
                    <Button onClick={() => setShowEducationalInfo(null)}>
                      Got it!
                    </Button>
                  </DialogActions>
                </Dialog>

                {/* Category Fields */}
                <Grid container spacing={2}>
                  {STRATEGIC_INPUT_FIELDS
                    .filter(field => field.category === activeCategory)
                    .map((field) => (
                      <Grid item xs={12} key={field.id}>
                        <StrategicInputField
                          fieldId={field.id}
                          value={formData[field.id]}
                          error={formErrors[field.id]}
                          autoPopulated={!!autoPopulatedFields[field.id]}
                          dataSource={dataSources[field.id]}
                          onChange={(value: any) => updateFormField(field.id, value)}
                          onValidate={() => validateFormField(field.id)}
                          onShowTooltip={() => setShowTooltip(field.id)}
                        />
                      </Grid>
                    ))}
                </Grid>

                {/* Category Actions */}
                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                  <Button
                    variant="contained"
                    onClick={() => {
                      // Mark category as complete
                      const categoryFields = STRATEGIC_INPUT_FIELDS.filter(f => f.category === activeCategory);
                      const allFieldsFilled = categoryFields.every(field => formData[field.id]);
                      if (allFieldsFilled) {
                        completeStep(activeCategory);
                        setActiveCategory(null);
                      }
                    }}
                    disabled={!STRATEGIC_INPUT_FIELDS
                      .filter(f => f.category === activeCategory)
                      .every(field => formData[field.id])}
                  >
                    Complete Category
                  </Button>
                  
                  <Button
                    variant="outlined"
                    onClick={() => setActiveCategory(null)}
                  >
                    Back to Overview
                  </Button>
                </Box>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <Box sx={{ textAlign: 'center', py: 8 }}>
                  <TimelineIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h5" gutterBottom>
                    Select a Category to Review
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    Click on any category from the left panel to review and complete the fields.
                  </Typography>
          </Box>
              </motion.div>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Action Buttons */}
      <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <MuiTooltip 
          title={completionPercentage < 20 ? `Complete at least 20% of the form (currently ${Math.round(completionPercentage)}%)` : 'Create a comprehensive content strategy with AI insights'}
          placement="top"
        >
          <span>
            <Button
              variant="outlined"
              startIcon={<AutoAwesomeIcon />}
              onClick={handleCreateStrategy}
              disabled={aiGenerating || completionPercentage < 20}
            >
              {aiGenerating ? 'Creating...' : 'Create Strategy'}
            </Button>
          </span>
        </MuiTooltip>
        
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={handleSaveStrategy}
          disabled={saving || completionPercentage < 30}
        >
          {saving ? 'Saving...' : 'Save Strategy'}
        </Button>
      </Box>

      {/* AI Recommendations Modal */}
      <Dialog 
        open={showAIRecommendations} 
        onClose={() => setShowAIRecommendations(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <AutoAwesomeIcon />
            AI Recommendations & Insights
          </Box>
        </DialogTitle>
        <DialogContent>
          <AIRecommendationsPanel 
            aiGenerating={aiGenerating}
            onGenerateRecommendations={handleCreateStrategy}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAIRecommendations(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Data Source Transparency Modal */}
      <Dialog 
        open={showDataSourceTransparency} 
        onClose={() => setShowDataSourceTransparency(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <InfoIcon />
            Data Source Transparency
          </Box>
        </DialogTitle>
        <DialogContent>
          <DataSourceTransparency 
            autoPopulatedFields={autoPopulatedFields}
            dataSources={dataSources}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowDataSourceTransparency(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Tooltip */}
      {showTooltip && (
        <EnhancedTooltip
          fieldId={showTooltip}
          open={!!showTooltip}
          onClose={() => setShowTooltip(null)}
        />
      )}
    </Box>
  );
};

export default EnhancedStrategyBuilder; 