import { useState, useEffect } from 'react';

interface UseModalManagementProps {
  aiGenerating: boolean;
  originalHandleCreateStrategy: (() => Promise<void>) | null;
}

export const useModalManagement = ({ aiGenerating, originalHandleCreateStrategy }: UseModalManagementProps) => {
  const [showEducationalModal, setShowEducationalModal] = useState(false);
  const [showEnterpriseModal, setShowEnterpriseModal] = useState(false);
  
  // Persist enterprise modal state across hot reloads
  useEffect(() => {
    const savedModalState = sessionStorage.getItem('showEnterpriseModal');
    if (savedModalState === 'true') {
      console.log('🎯 Restoring enterprise modal state from sessionStorage');
      setShowEnterpriseModal(true);
    }
  }, []);
  
  // Save modal state to sessionStorage when it changes
  useEffect(() => {
    sessionStorage.setItem('showEnterpriseModal', showEnterpriseModal.toString());
  }, [showEnterpriseModal]);
  
  // Cleanup sessionStorage on component unmount
  useEffect(() => {
    return () => {
      // Only clear if we're not in the middle of showing the modal
      if (!showEnterpriseModal) {
        sessionStorage.removeItem('showEnterpriseModal');
      }
    };
  }, [showEnterpriseModal]);

  // Monitor enterprise modal state for debugging
  useEffect(() => {
    console.log('🎯 Enterprise modal state changed - showEnterpriseModal:', showEnterpriseModal);
    
    // If modal was unexpectedly closed, log it
    if (!showEnterpriseModal && aiGenerating) {
      console.warn('🎯 WARNING: Enterprise modal closed while AI is generating');
    }
    
    // Only warn about unexpected closure if it's not due to hot reload
    if (!showEnterpriseModal && !aiGenerating) {
      const savedModalState = sessionStorage.getItem('showEnterpriseModal');
      if (savedModalState !== 'true') {
        console.warn('🎯 WARNING: Enterprise modal closed unexpectedly (not due to hot reload)');
      }
    }
  }, [showEnterpriseModal, aiGenerating]);

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
        if (!aiGenerating && originalHandleCreateStrategy) {
          console.log('🎯 Starting strategy generation...');
          await originalHandleCreateStrategy();
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
        if (!aiGenerating && originalHandleCreateStrategy) {
          await originalHandleCreateStrategy();
        } else {
          console.log('🎯 Already generating, skipping duplicate call');
        }
      } catch (error) {
        console.error('🎯 Error in handleAddEnterpriseDatapoints:', error);
      }
    }, 200); // Increased delay to ensure modal closes completely
  };

  return {
    showEducationalModal,
    setShowEducationalModal,
    showEnterpriseModal,
    setShowEnterpriseModal,
    handleProceedWithCurrentStrategy,
    handleAddEnterpriseDatapoints
  };
};
