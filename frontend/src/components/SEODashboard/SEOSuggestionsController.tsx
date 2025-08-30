import React, { useEffect, useMemo } from 'react';
import { useCopilotChat } from '@copilotkit/react-core';

// A lightweight controller that sets top-level suggestion groups and
// updates sub-suggestions based on the latest user message.
const SEOSuggestionsController: React.FC = () => {
  // Use a permissive cast to support variations across library versions
  const chat = useCopilotChat() as any;
  const messages = (chat && chat.messages) || [];
  const setSuggestions: ((s: { title: string; message: string }[]) => void) =
    (chat && chat.setSuggestions) || (() => {});

  // Top-level groups for progressive disclosure
  const topLevelGroups = useMemo(
    () => [
      { title: 'Content analysis', message: 'Content analysis' },
      { title: 'Website/URL analysis', message: 'Web URL analysis' },
      { title: 'Technical SEO', message: 'Technical SEO' },
      { title: 'Strategy & planning', message: 'Strategy and planning' },
      { title: 'Monitoring & health', message: 'Monitoring and health' }
    ],
    []
  );

  // Sub-suggestions mapped by group selection
  const subSuggestionsByGroup = useMemo(
    () => ({
      'Content analysis': [
        { title: 'Comprehensive content analysis', message: 'Analyze content comprehensively for my site' },
        { title: 'Optimize page content', message: 'Optimize page content for SEO' },
        { title: 'Generate meta descriptions', message: 'Generate meta descriptions for key pages' }
      ],
      'Web URL analysis': [
        { title: 'Comprehensive SEO analysis', message: 'Run comprehensive SEO analysis for a URL' },
        { title: 'Analyze page speed', message: 'Analyze page speed for a URL' },
        { title: 'Analyze sitemap', message: 'Analyze sitemap for my site' },
        { title: 'Generate OpenGraph tags', message: 'Generate OpenGraph tags for a URL' }
      ],
      'Technical SEO': [
        { title: 'Technical SEO audit', message: 'Run a technical SEO audit' },
        { title: 'Check SEO health', message: 'Check overall SEO health' },
        { title: 'Image alt text', message: 'Generate image alt text for pages' }
      ],
      'Strategy and planning': [
        { title: 'Enterprise SEO analysis', message: 'Run enterprise SEO analysis' },
        { title: 'Content strategy', message: 'Analyze content strategy and recommendations' },
        { title: 'Customize SEO dashboard', message: 'Customize the SEO dashboard' }
      ],
      'Monitoring and health': [
        { title: 'Website audit', message: 'Perform a website audit' },
        { title: 'Update SEO charts', message: 'Update SEO charts and visualizations' },
        { title: 'Explain an SEO concept', message: 'Explain an SEO concept in simple terms' }
      ]
    }),
    []
  );

  // Initialize top-level suggestions on mount
  useEffect(() => {
    setSuggestions(topLevelGroups);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // When the latest user message matches a group name, show its sub-suggestions
  useEffect(() => {
    if (!messages || messages.length === 0) return;
    const last = messages[messages.length - 1];
    if (last?.role !== 'user') return;

    const text = (last.content || '').trim();
    const group = Object.keys(subSuggestionsByGroup).find(
      key => key.toLowerCase() === text.toLowerCase()
    );

    if (group) {
      setSuggestions(subSuggestionsByGroup[group as keyof typeof subSuggestionsByGroup]);
    } else {
      if (text.length > 0 && !Object.keys(subSuggestionsByGroup).some(k => text.toLowerCase().includes(k.toLowerCase()))) {
        setSuggestions(topLevelGroups);
      }
    }
  }, [messages, setSuggestions, subSuggestionsByGroup, topLevelGroups]);

  return null;
};

export default SEOSuggestionsController;
