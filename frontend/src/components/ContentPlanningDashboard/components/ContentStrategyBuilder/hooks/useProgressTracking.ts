import { useMemo } from 'react';

interface UseProgressTrackingProps {
  completionStats: any;
  reviewedCategories: Set<string>;
}

export const useProgressTracking = ({ completionStats, reviewedCategories }: UseProgressTrackingProps) => {
  const progressData = useMemo(() => {
    const totalCategories = Object.keys(completionStats.category_completion).length;
    const reviewedCategoriesCount = reviewedCategories.size;
    const reviewProgressPercentage = (reviewedCategoriesCount / totalCategories) * 100;

    return {
      totalCategories,
      reviewedCategoriesCount,
      reviewProgressPercentage
    };
  }, [completionStats.category_completion, reviewedCategories]);

  const getCategoryProgress = (categoryId: string) => {
    return completionStats.category_completion[categoryId] || 0;
  };

  const getCategoryStatus = (percentage: number) => {
    if (percentage >= 90) return { status: 'Complete', color: 'success' as const };
    if (percentage >= 70) return { status: 'Good', color: 'primary' as const };
    if (percentage >= 50) return { status: 'Fair', color: 'warning' as const };
    return { status: 'Needs Work', color: 'error' as const };
  };

  const isNextInSequence = (categoryId: string, allCategories: string[]) => {
    const currentIndex = allCategories.indexOf(categoryId);
    return currentIndex > 0 && 
      allCategories.slice(0, currentIndex).every(cat => 
        reviewedCategories.has(cat)
      ) && 
      !reviewedCategories.has(categoryId);
  };

  return {
    ...progressData,
    getCategoryProgress,
    getCategoryStatus,
    isNextInSequence
  };
}; 