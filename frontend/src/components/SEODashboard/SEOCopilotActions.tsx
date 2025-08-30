// SEO CopilotKit Actions Component
// Registers all SEO-related actions with CopilotKit

import React from 'react';
import { useCopilotAction } from '@copilotkit/react-core';
import { useSEOCopilotStore } from '../../stores/seoCopilotStore';
import RegisterPageSpeed from './actions/RegisterPageSpeed';
import RegisterSitemap from './actions/RegisterSitemap';
import RegisterOnPage from './actions/RegisterOnPage';
import RegisterTechnical from './actions/RegisterTechnical';
import RegisterMetaDescription from './actions/RegisterMetaDescription';

const SEOCopilotActions: React.FC = () => {
  const { executeCopilotAction } = useSEOCopilotStore();
  const useCopilotActionTyped = useCopilotAction as any;
  const getDefaultUrl = () => useSEOCopilotStore.getState().analysisData?.url;

  // Lightweight actions without custom UI
  useCopilotActionTyped({
    name: 'generateImageAltText',
    description: 'Generate SEO-friendly alt text for images',
    parameters: [
      { name: 'imageUrl', type: 'string', description: 'Image URL', required: true },
      { name: 'context', type: 'string', description: 'Context about the image', required: false },
      { name: 'keywords', type: 'string[]', description: 'Keywords to include', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('generateImageAltText', args)
  });

  useCopilotActionTyped({
    name: 'generateOpenGraphTags',
    description: 'Generate OpenGraph tags for social media optimization',
    parameters: [
      { name: 'url', type: 'string', description: 'URL (optional)', required: false },
      { name: 'title', type: 'string', description: 'Title', required: false },
      { name: 'description', type: 'string', description: 'Description', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('generateOpenGraphTags', { ...args, url: args?.url || getDefaultUrl() })
  });

  useCopilotActionTyped({
    name: 'analyzeSEOComprehensive',
    description: 'Comprehensive SEO analysis',
    parameters: [
      { name: 'url', type: 'string', description: 'URL (optional)', required: false },
      { name: 'focusAreas', type: 'string[]', description: 'Focus areas', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('analyzeSEOComprehensive', { ...args, url: args?.url || getDefaultUrl() })
  });

  useCopilotActionTyped({
    name: 'analyzeEnterpriseSEO',
    description: 'Enterprise-level SEO analysis',
    parameters: [
      { name: 'url', type: 'string', description: 'URL (optional)', required: false },
      { name: 'competitorUrls', type: 'string[]', description: 'Competitor URLs', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('analyzeEnterpriseSEO', { ...args, url: args?.url || getDefaultUrl() })
  });

  useCopilotActionTyped({
    name: 'analyzeContentStrategy',
    description: 'Analyze content strategy and recommendations',
    parameters: [
      { name: 'url', type: 'string', description: 'URL (optional)', required: false },
      { name: 'contentType', type: 'string', description: 'Content type', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('analyzeContentStrategy', { ...args, url: args?.url || getDefaultUrl() })
  });

  useCopilotActionTyped({
    name: 'performWebsiteAudit',
    description: 'Perform comprehensive website SEO audit',
    parameters: [
      { name: 'url', type: 'string', description: 'URL (optional)', required: false },
      { name: 'auditType', type: 'string', description: 'Audit type', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('performWebsiteAudit', { ...args, url: args?.url || getDefaultUrl() })
  });

  useCopilotActionTyped({
    name: 'analyzeContentComprehensive',
    description: 'Analyze content comprehensively',
    parameters: [
      { name: 'content', type: 'string', description: 'Content to analyze', required: true },
      { name: 'targetKeywords', type: 'string[]', description: 'Target keywords', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('analyzeContentComprehensive', args)
  });

  useCopilotActionTyped({
    name: 'checkSEOHealth',
    description: 'Check overall SEO health',
    parameters: [
      { name: 'url', type: 'string', description: 'URL (optional)', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('checkSEOHealth', { ...args, url: args?.url || getDefaultUrl() })
  });

  useCopilotActionTyped({
    name: 'explainSEOConcept',
    description: 'Explain SEO concepts in simple terms',
    parameters: [
      { name: 'concept', type: 'string', description: 'Concept to explain', required: true },
      { name: 'audience', type: 'string', description: 'Audience (optional)', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('explainSEOConcept', args)
  });

  useCopilotActionTyped({
    name: 'updateSEOCharts',
    description: 'Update SEO charts and visualizations',
    parameters: [
      { name: 'chartType', type: 'string', description: 'Chart type', required: true },
      { name: 'timeRange', type: 'string', description: 'Time range', required: false }
    ],
    handler: async (args: any) => executeCopilotAction('updateSEOCharts', args)
  });

  // Modular registrars (HITL UIs)
  return (
    <>
      <RegisterMetaDescription />
      <RegisterPageSpeed />
      <RegisterSitemap />
      <RegisterOnPage />
      <RegisterTechnical />
    </>
  );
};

export default SEOCopilotActions;
