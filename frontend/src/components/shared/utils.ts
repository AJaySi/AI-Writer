import { Category, Tool, ToolCategories } from './types';

// Utility functions for dashboard components
export const getToolsForCategory = (category: Category, selectedSubCategory: string | null): Tool[] => {
  if ('subCategories' in category) {
    if (selectedSubCategory && category.subCategories[selectedSubCategory]) {
      return category.subCategories[selectedSubCategory].tools;
    }
    return [];
  }
  return category.tools;
};

export const getFilteredCategories = (
  toolCategories: ToolCategories,
  selectedCategory: string | null,
  searchQuery: string
) => {
  const filtered: ToolCategories = {};

  Object.entries(toolCategories).forEach(([categoryName, category]) => {
    if (selectedCategory && categoryName !== selectedCategory) {
      return;
    }

    if ('subCategories' in category) {
      const filteredSubCategories: Record<string, any> = {};
      Object.entries(category.subCategories).forEach(([subCategoryName, subCategory]) => {
        const filteredTools = subCategory.tools.filter(tool =>
          tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          tool.description.toLowerCase().includes(searchQuery.toLowerCase())
        );
        if (filteredTools.length > 0) {
          filteredSubCategories[subCategoryName] = { ...subCategory, tools: filteredTools };
        }
      });
      if (Object.keys(filteredSubCategories).length > 0) {
        filtered[categoryName] = { ...category, subCategories: filteredSubCategories };
      }
    } else {
      const filteredTools = category.tools.filter(tool =>
        tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tool.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
      if (filteredTools.length > 0) {
        filtered[categoryName] = { ...category, tools: filteredTools };
      }
    }
  });

  return filtered;
};

export const getStatusConfig = (status: string) => {
  switch (status) {
    case 'excellent':
    case 'strong':
      return { color: '#4CAF50', icon: '✓', label: 'Excellent' };
    case 'good':
      return { color: '#FF9800', icon: '⚠', label: 'Good' };
    case 'needs_action':
      return { color: '#F44336', icon: '✗', label: 'Needs Action' };
    default:
      return { color: '#9E9E9E', icon: 'ℹ', label: 'Unknown' };
  }
};

export const getStatusColor = (status: string) => {
  switch (status) {
    case 'excellent':
    case 'strong':
      return '#4CAF50';
    case 'good':
      return '#FF9800';
    case 'needs_action':
      return '#F44336';
    default:
      return '#9E9E9E';
  }
};

export const getStatusIcon = (status: string) => {
  switch (status) {
    case 'excellent':
    case 'strong':
      return '✓';
    case 'good':
      return '⚠';
    case 'needs_action':
      return '✗';
    default:
      return 'ℹ';
  }
};

export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

export const formatPercentage = (num: number): string => {
  return `${num > 0 ? '+' : ''}${num.toFixed(1)}%`;
};

export const getTrendColor = (trend: string): string => {
  switch (trend) {
    case 'up':
      return '#4CAF50';
    case 'down':
      return '#F44336';
    default:
      return '#9E9E9E';
  }
};

export const getTrendIcon = (trend: string): string => {
  switch (trend) {
    case 'up':
      return '↗';
    case 'down':
      return '↘';
    default:
      return '→';
  }
};

export const capitalizeFirst = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}; 