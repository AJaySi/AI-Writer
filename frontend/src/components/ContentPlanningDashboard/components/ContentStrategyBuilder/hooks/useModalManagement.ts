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
    console.log('🎯 useModalManagement: aiGenerating state changed:', aiGenerating);
  }, [aiGenerating]);

  // Handle proceed with current strategy (30 fields)
  const handleProceedWithCurrentStrategy = async () => {
    console.log('🎯 User clicked "Proceed with Current Strategy"');
    setShowEnterpriseModal(false);
    sessionStorage.removeItem('showEnterpriseModal'); // Clear sessionStorage
    
    // Add a small delay to ensure modal closes properly before showing educational modal
    setTimeout(async () => {
      console.log('🎯 Calling original handleCreateStrategy after enterprise modal closes');
      try {
        // Ensure we're not already generating
        if (!aiGenerating && originalHandleCreateStrategyRef.current) {
          console.log('🎯 Starting strategy generation...');
          await originalHandleCreateStrategyRef.current();
        } else {
          console.log('🎯 Already generating, skipping duplicate call');
        }
      } catch (error) {
        console.error('🎯 Error in handleProceedWithCurrentStrategy:', error);
      }
    }, 300); // Increased delay to ensure modal closes completely
  };

  // Handle add enterprise datapoints (coming soon)
  const handleAddEnterpriseDatapoints = async () => {
    console.log('🎯 User clicked "Add Enterprise Datapoints"');
    setShowEnterpriseModal(false);
    sessionStorage.removeItem('showEnterpriseModal'); // Clear sessionStorage
    
    // For now, just proceed with current strategy
    // In Phase 2, this will enable enterprise datapoints
    setTimeout(async () => {
      console.log('🎯 Calling original handleCreateStrategy for enterprise datapoints');
      try {
        // Ensure we're not already generating
        if (!aiGenerating && originalHandleCreateStrategyRef.current) {
          await originalHandleCreateStrategyRef.current();
        } else {
          console.log('🎯 Already generating, skipping duplicate call');
        }
      } catch (error) {
        console.error('🎯 Error in handleAddEnterpriseDatapoints:', error);
      }
    }, 200); // Increased delay to ensure modal closes completely
  };

  return {
    handleProceedWithCurrentStrategy,
    handleAddEnterpriseDatapoints
  };
};
