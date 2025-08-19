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
  const [isAutoPopulating, setIsAutoPopulating] = useState(false);

  // Auto-populate from onboarding on first load
  useEffect(() => {
    if (!autoPopulateAttempted && !isAutoPopulating) {
      setIsAutoPopulating(true);
      autoPopulateFromOnboarding();
      setAutoPopulateAttempted(true);
      setIsAutoPopulating(false);
    }
  }, [autoPopulateAttempted, isAutoPopulating]); // Removed autoPopulateFromOnboarding from dependencies

  return {
    autoPopulateAttempted,
    setAutoPopulateAttempted
  };
}; 