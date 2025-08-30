// SEO CopilotKit Context Component
// Provides real-time context and instructions to CopilotKit

import React, { useEffect, useRef } from 'react';
import { useCopilotReadable } from '@copilotkit/react-core';
import { useSEOCopilotStore } from '../../stores/seoCopilotStore';

const SEOCopilotContext: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { 
    analysisData, 
    personalizationData, 
    dashboardLayout, 
    suggestions,
    isLoading,
    isAnalyzing,
    isGenerating,
    error,
    loadPersonalizationData
  } = useSEOCopilotStore();

  const hasLoadedPersonalization = useRef(false);

  // Load personalization data on mount
  useEffect(() => {
    if (!hasLoadedPersonalization.current && !personalizationData) {
      useSEOCopilotStore.getState().loadPersonalizationData();
      hasLoadedPersonalization.current = true;
    }
  }, [personalizationData]);

  // Register SEO analysis data with CopilotKit
  useCopilotReadable({
    description: "Current SEO analysis data and insights",
    value: analysisData,
    categories: ["seo", "analysis"]
  });
  if (process.env.NODE_ENV === 'development') {
    console.log('[CopilotContext] Registered analysis data', !!analysisData);
  }

  // Provide a flat, explicit website URL for the LLM
  useCopilotReadable({
    description: "Current website URL the user is working on",
    value: analysisData?.url || '',
    categories: ["seo", "context"]
  });
  if (process.env.NODE_ENV === 'development') {
    console.log('[CopilotContext] Registered website URL', analysisData?.url);
  }

  // Register personalization data with CopilotKit
  useCopilotReadable({
    description: "User personalization preferences and settings",
    value: personalizationData,
    categories: ["user", "preferences"]
  });
  if (process.env.NODE_ENV === 'development') {
    console.log('[CopilotContext] Registered personalization', !!personalizationData);
  }

  // Register dashboard layout with CopilotKit
  useCopilotReadable({
    description: "Current dashboard layout and configuration",
    value: dashboardLayout,
    categories: ["ui", "layout"]
  });
  if (process.env.NODE_ENV === 'development') {
    console.log('[CopilotContext] Registered layout', !!dashboardLayout);
  }

  // Register suggestions with CopilotKit
  useCopilotReadable({
    description: "Available SEO actions and suggestions",
    value: suggestions,
    categories: ["actions", "suggestions"]
  });
  if (process.env.NODE_ENV === 'development') {
    console.log('[CopilotContext] Registered suggestions', Array.isArray(suggestions) ? suggestions.length : 0);
  }

  // Register loading states with CopilotKit
  useCopilotReadable({
    description: "Current loading and processing states",
    value: {
      isLoading,
      isAnalyzing,
      isGenerating,
      error
    },
    categories: ["status", "loading"]
  });
  if (process.env.NODE_ENV === 'development') {
    console.log('[CopilotContext] Registered status', { isLoading, isAnalyzing, isGenerating, hasError: !!error });
  }

  return <>{children}</>;
};

export default SEOCopilotContext;
