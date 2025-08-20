import { useEffect, useRef } from 'react';

interface UseModalManagementProps {
  aiGenerating: boolean;
  originalHandleCreateStrategy?: (() => Promise<void>) | null;
  setShowEnterpriseModal: (show: boolean) => void;
}

export const useModalManagement = ({ 
  aiGenerating, 
  originalHandleCreateStrategy,
  setShowEnterpriseModal 
}: UseModalManagementProps) => {
  const originalHandleCreateStrategyRef = useRef<(() => Promise<void>) | null>(null);
  
  // Update ref when originalHandleCreateStrategy changes
  useEffect(() => {
    if (originalHandleCreateStrategy) {
      originalHandleCreateStrategyRef.current = originalHandleCreateStrategy;
    }
  }, [originalHandleCreateStrategy]);

  // Monitor aiGenerating state for debugging
  useEffect(() => {
    // Removed verbose logging for cleaner console
  }, [aiGenerating]);

  // Handle proceed with current strategy (30 fields)
  const handleProceedWithCurrentStrategy = async () => {
    setShowEnterpriseModal(false);
    sessionStorage.removeItem('showEnterpriseModal'); // Clear sessionStorage
    
    // Add a small delay to ensure modal closes properly before showing educational modal
    setTimeout(async () => {
      try {
        // Ensure we're not already generating
        if (!aiGenerating && originalHandleCreateStrategyRef.current) {
          await originalHandleCreateStrategyRef.current();
        }
      } catch (error) {
        console.error('Error in handleProceedWithCurrentStrategy:', error);
      }
    }, 300); // Increased delay to ensure modal closes completely
  };

  // Handle add enterprise datapoints (coming soon)
  const handleAddEnterpriseDatapoints = async () => {
    setShowEnterpriseModal(false);
    sessionStorage.removeItem('showEnterpriseModal'); // Clear sessionStorage
    
    // For now, just proceed with current strategy
    // In Phase 2, this will enable enterprise datapoints
    setTimeout(async () => {
      try {
        // Ensure we're not already generating
        if (!aiGenerating && originalHandleCreateStrategyRef.current) {
          await originalHandleCreateStrategyRef.current();
        }
      } catch (error) {
        console.error('Error in handleAddEnterpriseDatapoints:', error);
      }
    }, 200); // Increased delay to ensure modal closes completely
  };

  return {
    handleProceedWithCurrentStrategy,
    handleAddEnterpriseDatapoints
  };
};
