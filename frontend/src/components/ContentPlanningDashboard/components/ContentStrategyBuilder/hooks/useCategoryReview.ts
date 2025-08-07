import { useState, useEffect } from 'react';

interface UseCategoryReviewProps {
  completionStats: any;
  setError: (error: string | null) => void;
  setActiveCategory: (category: string | null) => void;
}

export const useCategoryReview = ({ completionStats, setError, setActiveCategory }: UseCategoryReviewProps) => {
  const [reviewedCategories, setReviewedCategories] = useState<Set<string>>(new Set());
  const [isMarkingReviewed, setIsMarkingReviewed] = useState(false);
  const [categoryCompletionMessage, setCategoryCompletionMessage] = useState<string | null>(null);

  // Clear category completion message after 3 seconds
  useEffect(() => {
    if (categoryCompletionMessage) {
      const timer = setTimeout(() => {
        setCategoryCompletionMessage(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [categoryCompletionMessage]);

  const handleConfirmCategoryReview = async (activeCategory: string | null) => {
    if (!activeCategory) return;

    setIsMarkingReviewed(true);
    setCategoryCompletionMessage('🔄 Marking category as reviewed...');
    
    try {
      // Simulate processing time for better UX
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mark category as reviewed
      setReviewedCategories(prev => new Set([...Array.from(prev), activeCategory]));
      
      // Get category name for display
      const categoryName = activeCategory.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ');
      
      setCategoryCompletionMessage(`✅ ${categoryName} reviewed and confirmed!`);
      
      // Auto-navigate to next unreviewed category
      setTimeout(() => {
        const allCategories = Object.keys(completionStats.category_completion);
        const currentIndex = allCategories.indexOf(activeCategory);
        
        // Use the updated reviewedCategories state that includes the current category
        const updatedReviewedCategories = new Set([...Array.from(reviewedCategories), activeCategory]);
        
        console.log('🔍 Navigation Debug:', {
          activeCategory,
          currentIndex,
          allCategories,
          reviewedCategories: Array.from(reviewedCategories),
          updatedReviewedCategories: Array.from(updatedReviewedCategories)
        });
        
        const nextUnreviewedCategory = allCategories.find((categoryId, index) => {
          if (index <= currentIndex) return false;
          return !updatedReviewedCategories.has(categoryId);
        });
        
        console.log('🎯 Next Category Found:', nextUnreviewedCategory);
        
        if (nextUnreviewedCategory) {
          // Actually navigate to the next category
          console.log('🚀 Navigating to:', nextUnreviewedCategory);
          setActiveCategory(nextUnreviewedCategory);
          setCategoryCompletionMessage(`🎯 Moving to next category: ${nextUnreviewedCategory.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
          ).join(' ')}`);
        } else {
          console.log('🎉 All categories reviewed!');
          setCategoryCompletionMessage('🎉 All categories reviewed and confirmed! You can now create your strategy.');
        }
      }, 1500);
    } catch (error: any) {
      setError(`Error marking category as reviewed: ${error.message || 'Unknown error'}`);
      console.error('Error in handleConfirmCategoryReview:', error);
    } finally {
      setIsMarkingReviewed(false);
    }
  };

  const isCategoryReviewed = (categoryId: string) => {
    return reviewedCategories.has(categoryId);
  };

  const getNextUnreviewedCategory = (currentCategoryId: string) => {
    const allCategories = Object.keys(completionStats.category_completion);
    const currentIndex = allCategories.indexOf(currentCategoryId);
    
    // Use the updated reviewedCategories state that includes the current category
    const updatedReviewedCategories = new Set([...Array.from(reviewedCategories), currentCategoryId]);
    
    return allCategories.find((categoryId, index) => {
      if (index <= currentIndex) return false;
      return !updatedReviewedCategories.has(categoryId);
    });
  };

  return {
    reviewedCategories,
    isMarkingReviewed,
    categoryCompletionMessage,
    handleConfirmCategoryReview,
    isCategoryReviewed,
    getNextUnreviewedCategory,
    setReviewedCategories
  };
}; 