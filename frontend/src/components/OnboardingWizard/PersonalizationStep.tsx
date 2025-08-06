import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Button, 
  TextField, 
  Typography, 
  Alert, 
  MenuItem, 
  FormControl, 
  InputLabel, 
  Select, 
  Chip, 
  OutlinedInput,
  FormHelperText,
  Switch,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider
} from '@mui/material';
import { ExpandMore as ExpandMoreIcon } from '@mui/icons-material';
import { 
  validateContentStyle, 
  configureBrandVoice, 
  processPersonalizationSettings,
  getPersonalizationConfigurationOptions,
  generateContentGuidelines,
  ContentStyleRequest,
  BrandVoiceRequest,
  AdvancedSettingsRequest,
  PersonalizationSettingsRequest
} from '../../api/componentLogic';

interface PersonalizationStepProps {
  onContinue: () => void;
  updateHeaderContent: (content: { title: string; description: string }) => void;
}

const PersonalizationStep: React.FC<PersonalizationStepProps> = ({ onContinue, updateHeaderContent }) => {
  // Content Style State
  const [writingStyle, setWritingStyle] = useState('Professional');
  const [tone, setTone] = useState('Neutral');
  const [contentLength, setContentLength] = useState('Standard');

  // Brand Voice State
  const [personalityTraits, setPersonalityTraits] = useState<string[]>(['Professional']);
  const [voiceDescription, setVoiceDescription] = useState('');
  const [keywords, setKeywords] = useState('');

  // Advanced Settings State
  const [seoOptimization, setSeoOptimization] = useState(false);
  const [readabilityLevel, setReadabilityLevel] = useState('Standard');
  const [contentStructure, setContentStructure] = useState<string[]>(['Introduction', 'Key Points', 'Conclusion']);

  // UI State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [configurationOptions, setConfigurationOptions] = useState<any>(null);

  useEffect(() => {
    async function loadConfigurationOptions() {
      try {
        const options = await getPersonalizationConfigurationOptions();
        setConfigurationOptions(options.options);
      } catch (e) {
        console.error('Failed to load configuration options:', e);
      }
    }
    loadConfigurationOptions();
    
    // Update header content when component mounts
    updateHeaderContent({
      title: 'Customize Your Experience',
      description: 'Personalize Alwrity to match your brand voice, content style, and writing preferences. Configure how AI generates content to ensure it aligns with your brand identity and resonates with your audience.'
    });
  }, [updateHeaderContent]);

  const handleContinue = async () => {
    setError(null);
    setSuccess(null);
    setLoading(true);

    try {
      // Validate content style
      const contentStyleRequest: ContentStyleRequest = {
        writing_style: writingStyle,
        tone: tone,
        content_length: contentLength
      };

      const contentStyleValidation = await validateContentStyle(contentStyleRequest);
      if (!contentStyleValidation.valid) {
        setError(`Content style validation failed: ${contentStyleValidation.errors.join(', ')}`);
        setLoading(false);
        return;
      }

      // Configure brand voice
      const brandVoiceRequest: BrandVoiceRequest = {
        personality_traits: personalityTraits,
        voice_description: voiceDescription,
        keywords: keywords
      };

      const brandVoiceValidation = await configureBrandVoice(brandVoiceRequest);
      if (!brandVoiceValidation.valid) {
        setError(`Brand voice validation failed: ${brandVoiceValidation.errors.join(', ')}`);
        setLoading(false);
        return;
      }

      // Process complete settings
      const advancedSettingsRequest: AdvancedSettingsRequest = {
        seo_optimization: seoOptimization,
        readability_level: readabilityLevel,
        content_structure: contentStructure
      };

      const completeSettingsRequest: PersonalizationSettingsRequest = {
        content_style: contentStyleRequest,
        brand_voice: brandVoiceRequest,
        advanced_settings: advancedSettingsRequest
      };

      const settingsValidation = await processPersonalizationSettings(completeSettingsRequest);
      if (!settingsValidation.valid) {
        setError(`Settings validation failed: ${settingsValidation.errors.join(', ')}`);
        setLoading(false);
        return;
      }

      // Generate content guidelines
      const guidelines = await generateContentGuidelines(settingsValidation.settings);
      if (guidelines.success) {
        setSuccess('Personalization settings saved successfully! Content guidelines generated.');
        // TODO: Store guidelines for later use
        onContinue();
      } else {
        setError('Failed to generate content guidelines.');
      }

    } catch (e) {
      setError('Failed to save personalization settings. Please try again.');
      console.error('Personalization error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handlePersonalityTraitsChange = (event: any) => {
    const value = event.target.value;
    setPersonalityTraits(typeof value === 'string' ? value.split(',') : value);
  };

  const handleContentStructureChange = (event: any) => {
    const value = event.target.value;
    setContentStructure(typeof value === 'string' ? value.split(',') : value);
  };

  if (!configurationOptions) {
    return (
      <Box>
        <Typography variant="h6" gutterBottom>
          Personalize Your Experience
        </Typography>
        <Alert severity="info">Loading configuration options...</Alert>
      </Box>
    );
  }

  return (
    <Box>
      {/* Enhanced Explanatory Text */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h6" color="text.secondary" sx={{ 
          mb: 3, 
          lineHeight: 1.6, 
          maxWidth: 800, 
          mx: 'auto',
          fontWeight: 500,
          opacity: 0.8
        }}>
          Configure your content style, brand voice, and advanced settings to tailor the AI experience to your needs. 
          This ensures that all generated content aligns with your brand identity and resonates with your target audience.
        </Typography>
      </Box>

      {/* Content Style Section */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1" fontWeight="bold">Content Style</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Writing Style</InputLabel>
              <Select
                value={writingStyle}
                onChange={(e) => setWritingStyle(e.target.value)}
                label="Writing Style"
              >
                {configurationOptions.writing_styles?.map((style: string) => (
                  <MenuItem key={style} value={style}>{style}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Tone</InputLabel>
              <Select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                label="Tone"
              >
                {configurationOptions.tones?.map((toneOption: string) => (
                  <MenuItem key={toneOption} value={toneOption}>{toneOption}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Content Length</InputLabel>
              <Select
                value={contentLength}
                onChange={(e) => setContentLength(e.target.value)}
                label="Content Length"
              >
                {configurationOptions.content_lengths?.map((length: string) => (
                  <MenuItem key={length} value={length}>{length}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Brand Voice Section */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1" fontWeight="bold">Brand Voice</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControl fullWidth>
              <InputLabel>Personality Traits</InputLabel>
              <Select
                multiple
                value={personalityTraits}
                onChange={handlePersonalityTraitsChange}
                input={<OutlinedInput label="Personality Traits" />}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
              >
                {configurationOptions.personality_traits?.map((trait: string) => (
                  <MenuItem key={trait} value={trait}>{trait}</MenuItem>
                ))}
              </Select>
              <FormHelperText>Select traits that best describe your brand</FormHelperText>
            </FormControl>

            <TextField
              label="Brand Voice Description"
              value={voiceDescription}
              onChange={(e) => setVoiceDescription(e.target.value)}
              fullWidth
              multiline
              rows={3}
              helperText="Describe how your brand should sound in content (optional)"
            />

            <TextField
              label="Brand Keywords"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              fullWidth
              helperText="Enter key terms that should be used in your content (optional)"
            />
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Advanced Settings Section */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="subtitle1" fontWeight="bold">Advanced Settings</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={seoOptimization}
                  onChange={(e) => setSeoOptimization(e.target.checked)}
                />
              }
              label="Enable SEO Optimization"
            />

            <FormControl fullWidth>
              <InputLabel>Readability Level</InputLabel>
              <Select
                value={readabilityLevel}
                onChange={(e) => setReadabilityLevel(e.target.value)}
                label="Readability Level"
              >
                {configurationOptions.readability_levels?.map((level: string) => (
                  <MenuItem key={level} value={level}>{level}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel>Content Structure</InputLabel>
              <Select
                multiple
                value={contentStructure}
                onChange={handleContentStructureChange}
                input={<OutlinedInput label="Content Structure" />}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Box>
                )}
              >
                {configurationOptions.content_structures?.map((structure: string) => (
                  <MenuItem key={structure} value={structure}>{structure}</MenuItem>
                ))}
              </Select>
              <FormHelperText>Select required content sections</FormHelperText>
            </FormControl>
          </Box>
        </AccordionDetails>
      </Accordion>

      <Divider sx={{ my: 2 }} />

      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
      
      <Button
        variant="contained"
        color="primary"
        onClick={handleContinue}
        sx={{ mt: 2 }}
        disabled={loading}
      >
        {loading ? 'Saving Settings...' : 'Continue'}
      </Button>
    </Box>
  );
};

export default PersonalizationStep; 