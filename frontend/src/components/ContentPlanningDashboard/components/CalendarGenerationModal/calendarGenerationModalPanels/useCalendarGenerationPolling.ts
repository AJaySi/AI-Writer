import { useState, useCallback } from 'react';

// Types
interface QualityScores {
  overall: number;
  step1: number;
  step2: number;
  step3: number;
  step4: number;
  step5: number;
  step6: number;
  step7: number;
  step8: number;
  step9: number;
  step10: number;
  step11: number;
  step12: number;
}

interface CalendarGenerationProgress {
  status: 'initializing' | 'step1' | 'step2' | 'step3' | 'completed' | 'error';
  currentStep: number;
  stepProgress: number;
  overallProgress: number;
  stepResults: Record<number, any>;
  qualityScores: QualityScores;
  transparencyMessages: string[];
  educationalContent: any[];
  errors: any[];
  warnings: any[];
}

// Polling hook for calendar generation progress
const useCalendarGenerationPolling = (sessionId: string) => {
  const [progress, setProgress] = useState<CalendarGenerationProgress | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const startPolling = useCallback(async () => {
    setIsPolling(true);
    setError(null);
    
    const poll = async () => {
      try {
        const response = await fetch(`/api/content-planning/calendar-generation/progress/${sessionId}`);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Transform backend data to frontend format
        const transformedProgress: CalendarGenerationProgress = {
          status: data.status,
          currentStep: data.current_step,
          stepProgress: data.step_progress,
          overallProgress: data.overall_progress,
          stepResults: data.step_results,
          qualityScores: data.quality_scores,
          transparencyMessages: data.transparency_messages,
          educationalContent: data.educational_content,
          errors: data.errors,
          warnings: data.warnings
        };
        
        setProgress(transformedProgress);
        
        if (data.status === 'completed' || data.status === 'error') {
          setIsPolling(false);
          if (data.status === 'error') {
            setError(data.errors?.[0]?.message || 'Unknown error occurred');
          }
          return;
        }
        
        // Continue polling every 2 seconds
        setTimeout(poll, 2000);
      } catch (error) {
        console.error('Calendar generation polling error:', error);
        setError(error instanceof Error ? error.message : 'Polling failed');
        // Retry after 5 seconds
        setTimeout(poll, 5000);
      }
    };
    
    poll();
  }, [sessionId]);
  
  const stopPolling = useCallback(() => {
    setIsPolling(false);
  }, []);
  
  return { progress, isPolling, error, startPolling, stopPolling };
};

export default useCalendarGenerationPolling;
export type { CalendarGenerationProgress, QualityScores };
