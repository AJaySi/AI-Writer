import React from 'react';
import {
  Business as BusinessIcon,
  People as PeopleIcon,
  TrendingUp as TrendingUpIcon,
  ContentPaste as ContentIcon,
  Analytics as AnalyticsIcon,
  Help as HelpIcon
} from '@mui/icons-material';

export const getCategoryIcon = (categoryId: string): React.ReactElement => {
  switch (categoryId) {
    case 'business_context': return <BusinessIcon />;
    case 'audience_intelligence': return <PeopleIcon />;
    case 'competitive_intelligence': return <TrendingUpIcon />;
    case 'content_strategy': return <ContentIcon />;
    case 'performance_analytics': return <AnalyticsIcon />;
    default: return <HelpIcon />;
  }
};

export const getCategoryColor = (categoryId: string): string => {
  switch (categoryId) {
    case 'business_context': return 'primary';
    case 'audience_intelligence': return 'secondary';
    case 'competitive_intelligence': return 'success';
    case 'content_strategy': return 'warning';
    case 'performance_analytics': return 'info';
    default: return 'default';
  }
};

export const getCategoryName = (categoryId: string): string => {
  return categoryId.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ');
};

export const getCategoryStatus = (percentage: number) => {
  if (percentage >= 90) return { status: 'Complete', color: 'success' as const };
  if (percentage >= 70) return { status: 'Good', color: 'primary' as const };
  if (percentage >= 50) return { status: 'Fair', color: 'warning' as const };
  return { status: 'Needs Work', color: 'error' as const };
}; 