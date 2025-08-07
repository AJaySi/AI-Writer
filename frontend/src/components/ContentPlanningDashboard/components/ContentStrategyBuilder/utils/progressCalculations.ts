export const calculateReviewProgress = (reviewedCategories: Set<string>, totalCategories: number): number => {
  return (reviewedCategories.size / totalCategories) * 100;
};

export const calculateCategoryProgress = (filledFields: number, totalFields: number): number => {
  return totalFields > 0 ? (filledFields / totalFields) * 100 : 0;
};

export const getProgressColor = (percentage: number): string => {
  if (percentage >= 90) return 'success';
  if (percentage >= 70) return 'primary';
  if (percentage >= 50) return 'warning';
  return 'error';
};

export const formatProgressPercentage = (percentage: number): string => {
  return `${Math.round(percentage)}%`;
};

export const getProgressMessage = (percentage: number): string => {
  if (percentage >= 100) return 'Complete';
  if (percentage >= 90) return 'Almost Complete';
  if (percentage >= 70) return 'Good Progress';
  if (percentage >= 50) return 'Halfway There';
  if (percentage >= 30) return 'Getting Started';
  return 'Needs Work';
}; 