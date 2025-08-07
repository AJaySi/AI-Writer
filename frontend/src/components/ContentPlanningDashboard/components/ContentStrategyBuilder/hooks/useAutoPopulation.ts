import { useState, useEffect } from 'react';

interface UseAutoPopulationProps {
  autoPopulateFromOnboarding: () => void;
  completionStats: any;
}

export const useAutoPopulation = ({ 
  autoPopulateFromOnboarding, 
  completionStats
}: UseAutoPopulationProps) => {
  const [autoPopulateAttempted, setAutoPopulateAttempted] = useState(false);

  // Auto-populate from onboarding on first load
  useEffect(() => {
    if (!autoPopulateAttempted) {
      autoPopulateFromOnboarding();
      setAutoPopulateAttempted(true);
    }
  }, [autoPopulateAttempted, autoPopulateFromOnboarding]);

  return {
    autoPopulateAttempted,
    setAutoPopulateAttempted
  };
}; 