import React from 'react';
import {
  Box,
  Typography,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Grid,
  CircularProgress
} from '@mui/material';
import {
  School as SchoolIcon,
  Lightbulb as LightbulbIcon,
  Psychology as PsychologyIcon,
  Timeline as TimelineIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import StrategicInputField from '../StrategicInputField';
import { CategoryDetailViewProps, EducationalInfoDialogProps } from '../types/contentStrategy.types';
import { useEnhancedStrategyStore } from '../../../../../stores/enhancedStrategyStore';

const EducationalInfoDialog: React.FC<EducationalInfoDialogProps> = ({
  open,
  onClose,
  categoryId,
  getEducationalContent
}) => {
  if (!categoryId) return null;
  
  const educationalContent = getEducationalContent(categoryId);
  
  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SchoolIcon />
          {educationalContent?.title}
        </Box>
      </DialogTitle>
      <DialogContent>
        <Typography variant="body1" paragraph>
          {educationalContent?.description}
        </Typography>
        
        <Typography variant="h6" gutterBottom>
          Key Points:
        </Typography>
        <List>
          {educationalContent?.points?.map((point: string, index: number) => (
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
          {educationalContent?.tips?.map((tip: string, index: number) => (
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
        <Button onClick={onClose}>
          Got it!
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const CategoryDetailView: React.FC<CategoryDetailViewProps> = ({
  activeCategory,
  formData,
  formErrors,
  autoPopulatedFields,
  dataSources,
  inputDataPoints,
  personalizationData,
  completionStats,
  reviewedCategories,
  isMarkingReviewed,
  showEducationalInfo,
  STRATEGIC_INPUT_FIELDS,
  onUpdateFormField,
  onValidateFormField,
  onShowTooltip,
  onViewDataSource,
  onConfirmCategoryReview,
  onSetActiveCategory,
  onSetShowEducationalInfo,
  getCategoryIcon,
  getCategoryColor,
  getEducationalContent
}) => {
  // Get confidence scores from store
  const { confidenceScores } = useEnhancedStrategyStore();
  if (!activeCategory) {
    return (
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
    );
  }

  return (
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
      <EducationalInfoDialog
        open={!!showEducationalInfo}
        onClose={() => onSetShowEducationalInfo(null)}
        categoryId={showEducationalInfo}
        getEducationalContent={getEducationalContent}
      />

      {/* Category Fields */}
      <Box sx={{ mt: 1 }}>
        <Grid container spacing={2}>
          {STRATEGIC_INPUT_FIELDS
            .filter(field => field.category === activeCategory)
            .map((field, index) => {
              // Determine grid size based on field type for better layout organization
              const type = field.type;
              const isWideField = type === 'json';
              const isMediumField = type === 'multiselect' || type === 'select' || type === 'text';
              const isCompactField = type === 'number' || type === 'boolean';
              const forceFullWidth = field.id === 'content_budget' || field.id === 'team_size';

              const gridMd = forceFullWidth ? 12 : (isWideField ? 12 : isMediumField ? 6 : 4);
              const gridLg = forceFullWidth ? 12 : (isWideField ? 12 : isMediumField ? 6 : 4);
              const gridSm = 12;
            
            return (
                <Grid item xs={12} sm={gridSm} md={gridMd} lg={gridLg} key={field.id}>
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }} 
                    animate={{ opacity: 1, y: 0 }} 
                    transition={{ duration: 0.25, delay: index * 0.03 }}
                  >
                    <StrategicInputField
                      fieldId={field.id}
                      value={formData[field.id]}
                      error={formErrors[field.id]}
                      autoPopulated={!!autoPopulatedFields[field.id]}
                      dataSource={dataSources[field.id]}
                      confidenceLevel={confidenceScores[field.id] || (autoPopulatedFields[field.id] ? 0.8 : undefined)}
                      dataQuality={autoPopulatedFields[field.id] ? 'High Quality' : undefined}
                      personalizationData={personalizationData[field.id]}
                      onChange={(value: any) => onUpdateFormField(field.id, value)}
                      onValidate={() => onValidateFormField(field.id)}
                      onShowTooltip={() => onShowTooltip(field.id)}
                      onViewDataSource={() => onViewDataSource(field.id)}
                      accentColorKey={getCategoryColor(activeCategory) as any}
                      isCompact={isCompactField}
                    />
                  </motion.div>
              </Grid>
            );
          })}
        </Grid>
      </Box>

      {/* Category Actions */}
      <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
        {(() => {
          const isReviewed = reviewedCategories.has(activeCategory);
          console.log('🔍 Category review status:', {
            activeCategory,
            isReviewed,
            reviewedCategories: Array.from(reviewedCategories)
          });
          return !isReviewed ? (
            <Button
              variant="contained"
              onClick={() => {
                console.log('🔘 Button clicked! activeCategory:', activeCategory);
                console.log('🔘 reviewedCategories:', Array.from(reviewedCategories));
                console.log('🔘 isMarkingReviewed:', isMarkingReviewed);
                onConfirmCategoryReview();
              }}
              startIcon={isMarkingReviewed ? <CircularProgress size={20} /> : <CheckCircleIcon />}
              disabled={isMarkingReviewed}
            >
              {isMarkingReviewed ? 'Marking as Reviewed...' : 'Mark as Reviewed'}
            </Button>
          ) : (
            <Chip
              label="Category Reviewed"
              color="success"
              icon={<CheckCircleIcon />}
              sx={{ px: 2, py: 1 }}
            />
          );
        })()}
        
        <Button
          variant="outlined"
          onClick={() => onSetActiveCategory(null)}
        >
          Back to Overview
        </Button>
      </Box>
    </motion.div>
  );
};

export default CategoryDetailView; 