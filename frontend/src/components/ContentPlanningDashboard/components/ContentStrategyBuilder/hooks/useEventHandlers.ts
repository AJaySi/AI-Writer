import { useState } from 'react';

export const useEventHandlers = () => {
  const [showTooltip, setShowTooltip] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [showEducationalInfo, setShowEducationalInfo] = useState<string | null>(null);

  const handleReviewCategory = (categoryId: string) => {
    setActiveCategory(activeCategory === categoryId ? null : categoryId);
  };

  const handleShowEducationalInfo = (categoryId: string) => {
    setShowEducationalInfo(showEducationalInfo === categoryId ? null : categoryId);
  };

  return {
    showTooltip,
    setShowTooltip,
    activeCategory,
    setActiveCategory,
    showEducationalInfo,
    setShowEducationalInfo,
    handleReviewCategory,
    handleShowEducationalInfo
  };
};
