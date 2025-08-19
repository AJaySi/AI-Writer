/**
 * Calendar Wizard Types
 * Phase 3A: Simplified Calendar-Specific Configuration
 */

export interface CalendarConfig {
  // Calendar Structure
  calendarType: 'weekly' | 'monthly' | 'quarterly';
  calendarDuration: number; // Number of periods to generate
  startDate: string; // ISO date string
  
  // Posting Configuration
  postingFrequency: number; // Posts per week
  contentVolume: number; // Total pieces per period
  
  // Platform Scheduling
  priorityPlatforms: string[]; // ["LinkedIn", "Twitter", "Blog"]
  timeZone: string; // User's timezone
  
  // Calendar Preferences
  excludeDates: string[]; // Holiday/blackout dates
  contentDistribution: 'even' | 'frontloaded' | 'backloaded';
  reviewCycle: 'weekly' | 'monthly' | 'quarterly';
  
  // Generation Options
  includeWeekends: boolean;
  autoSchedule: boolean;
  generateTopics: boolean;
}

export interface WizardStep {
  label: string;
  icon: React.ReactNode;
  description: string;
  isCompleted: boolean;
  hasErrors: boolean;
}

export interface ValidationError {
  field: string;
  message: string;
  step: number;
}

export interface WizardState {
  activeStep: number;
  calendarConfig: CalendarConfig;
  steps: WizardStep[];
  validationErrors: ValidationError[];
  isLoading: boolean;
  error: string | null;
  isGenerating: boolean;
  generationProgress: number;
}

export interface WizardActions {
  setActiveStep: (step: number) => void;
  updateCalendarConfig: (updates: Partial<CalendarConfig>) => void;
  validateStep: (step: number) => boolean;
  validateAllSteps: () => boolean;
  clearErrors: () => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
  setGenerating: (generating: boolean) => void;
  setGenerationProgress: (progress: number) => void;
  resetWizard: () => void;
  canProceedToStep: (step: number) => boolean;
  getStepStatus: (step: number) => 'completed' | 'current' | 'pending' | 'error';
}
