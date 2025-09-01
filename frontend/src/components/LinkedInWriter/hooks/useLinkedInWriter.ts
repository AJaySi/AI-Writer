import { useState, useCallback, useEffect } from 'react';
import { useCopilotReadable } from '@copilotkit/react-core';
import { 
  loadHistory, 
  clearHistory, 
  getHistoryLength, 
  getPreferences, 
  savePreferences, 
  getCurrentContext, 
  saveCurrentContext, 
  summarizeHistory,
  type ChatMsg,
  type LinkedInPreferences
} from '../utils/storageUtils';
import { getContextAwareSuggestions } from '../utils/linkedInWriterUtils';

export function useLinkedInWriter() {
  // Core state
  const [draft, setDraft] = useState('');
  const [context, setContext] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [livePreviewHtml, setLivePreviewHtml] = useState('');
  const [pendingEdit, setPendingEdit] = useState<{ src: string; target: string } | null>(null);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [currentAction, setCurrentAction] = useState<string | null>(null);

  // Chat history state
  const [historyVersion, setHistoryVersion] = useState<number>(0);
  const [chatHistory, setChatHistory] = useState<ChatMsg[]>([]);
  const [userPreferences, setUserPreferences] = useState<LinkedInPreferences>(getPreferences());
  
  // UI state
  const [currentSuggestions, setCurrentSuggestions] = useState<Array<{title: string, message: string, priority?: string}>>([]);
  const [showContextPanel, setShowContextPanel] = useState(false);
  const [showPreferencesModal, setShowPreferencesModal] = useState(false);
  const [showContextModal, setShowContextModal] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  // Update suggestions when context changes
  const updateSuggestions = useCallback(() => {
    const newSuggestions = getContextAwareSuggestions(
      userPreferences,
      draft,
      chatHistory.slice(-5),
      userPreferences.last_used_actions || []
    );
    setCurrentSuggestions(newSuggestions);
  }, [userPreferences, draft, chatHistory]);

  // Track action usage and update preferences
  const trackActionUsage = useCallback((actionName: string) => {
    const currentPrefs = getPreferences();
    const updatedActions = [...(currentPrefs.last_used_actions || []), actionName].slice(-5);
    savePreferences({ last_used_actions: updatedActions });
    setUserPreferences(prev => ({ ...prev, last_used_actions: updatedActions }));
    
    // Update suggestions after action usage
    setTimeout(() => updateSuggestions(), 100);
  }, [updateSuggestions]);

  // Initialize chat history and preferences from localStorage
  useEffect(() => {
    const loadInitialData = () => {
      try {
        const history = loadHistory();
        const prefs = getPreferences();
        const savedContext = getCurrentContext();
        
        setChatHistory(history);
        setUserPreferences(prefs);
        if (savedContext && !context) {
          setContext(savedContext);
        }
        
        console.log('[LinkedIn Writer] Initialized with:', {
          historyCount: history.length,
          preferences: prefs,
          hasContext: !!savedContext
        });
      } catch (error) {
        console.warn('[LinkedIn Writer] Failed to initialize from localStorage:', error);
      }
    };

    loadInitialData();
  }, []);

  // Save context changes to localStorage
  useEffect(() => {
    if (context) {
      saveCurrentContext(context);
    }
  }, [context]);
  
  // Update suggestions when relevant state changes
  useEffect(() => {
    updateSuggestions();
  }, [updateSuggestions]);

  // Handle draft updates from CopilotKit actions
  useEffect(() => {
    const handleUpdateDraft = (event: CustomEvent) => {
      setDraft(event.detail);
      setIsGenerating(false);
      setLoadingMessage('');
      setCurrentAction(null);
    };

    const handleAppendDraft = (event: CustomEvent) => {
      setDraft(prev => prev + event.detail);
    };

    const handleAssistantMessage = (event: CustomEvent) => {
      console.log('LinkedIn Assistant:', event.detail);
    };

    const handleLoadingStart = (event: CustomEvent) => {
      const { action, message } = event.detail;
      setCurrentAction(action);
      setLoadingMessage(message);
      setIsGenerating(true);
    };

    const handleLoadingEnd = (event: CustomEvent) => {
      setIsGenerating(false);
      setLoadingMessage('');
      setCurrentAction(null);
    };

    const handleApplyEdit = (event: CustomEvent) => {
      const target: string = typeof event.detail === 'string' ? event.detail : (event.detail?.target ?? '');
      const src = draft || '';
      if (!target) return;
      setPendingEdit({ src, target });
      setIsPreviewing(true);
      
      // Use diff highlighting for professional content changes
      try {
        const { diffMarkup } = require('../utils/contentFormatters');
        setLivePreviewHtml(diffMarkup(src, target));
      } catch (error) {
        // Fallback to simple text if diffMarkup fails to load
        console.warn('Failed to load diffMarkup, using fallback:', error);
        setLivePreviewHtml(target);
      }
    };

    window.addEventListener('linkedinwriter:updateDraft', handleUpdateDraft as EventListener);
    window.addEventListener('linkedinwriter:appendDraft', handleAppendDraft as EventListener);
    window.addEventListener('linkedinwriter:assistantMessage', handleAssistantMessage as EventListener);
    window.addEventListener('linkedinwriter:applyEdit', handleApplyEdit as EventListener);
    window.addEventListener('linkedinwriter:loadingStart', handleLoadingStart as EventListener);
    window.addEventListener('linkedinwriter:loadingEnd', handleLoadingEnd as EventListener);

    return () => {
      window.removeEventListener('linkedinwriter:updateDraft', handleUpdateDraft as EventListener);
      window.removeEventListener('linkedinwriter:appendDraft', handleAppendDraft as EventListener);
      window.removeEventListener('linkedinwriter:assistantMessage', handleAssistantMessage as EventListener);
      window.removeEventListener('linkedinwriter:applyEdit', handleApplyEdit as EventListener);
      window.removeEventListener('linkedinwriter:loadingStart', handleLoadingStart as EventListener);
      window.removeEventListener('linkedinwriter:loadingEnd', handleLoadingEnd as EventListener);
    };
  }, [draft]);

  // Event handlers
  const handleDraftChange = useCallback((value: string) => {
    setDraft(value);
  }, []);

  const handleContextChange = useCallback((value: string) => {
    setContext(value);
  }, []);

  const handleClear = useCallback(() => {
    setDraft('');
    setContext('');
  }, []);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(draft);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  }, [draft]);

  const handleClearHistory = useCallback(() => {
    clearHistory(); 
    setHistoryVersion(v => v + 1);
    setChatHistory([]);
    console.log('[LinkedIn Writer] Chat memory cleared by user');
  }, []);

  // Make content available to CopilotKit
  useCopilotReadable({
    description: 'Current LinkedIn content draft',
    value: draft
  });

  useCopilotReadable({
    description: 'Context and notes for LinkedIn content',
    value: context
  });

  useCopilotReadable({
    description: 'User preferences for LinkedIn content (tone, industry, audience, style, options)',
    value: userPreferences
  });

  return {
    // State
    draft,
    context,
    isGenerating,
    isPreviewing,
    livePreviewHtml,
    pendingEdit,
    loadingMessage,
    currentAction,
    historyVersion,
    chatHistory,
    userPreferences,
    currentSuggestions,
    showContextPanel,
    showPreferencesModal,
    showContextModal,
    showPreview,
    
    // Setters
    setDraft,
    setContext,
    setIsGenerating,
    setIsPreviewing,
    setLivePreviewHtml,
    setPendingEdit,
    setLoadingMessage,
    setCurrentAction,
    setHistoryVersion,
    setChatHistory,
    setUserPreferences,
    setShowContextPanel,
    setShowPreferencesModal,
    setShowContextModal,
    setShowPreview,
    
    // Handlers
    handleDraftChange,
    handleContextChange,
    handleClear,
    handleCopy,
    handleClearHistory,
    
    // Utilities
    trackActionUsage,
    updateSuggestions,
    getHistoryLength,
    savePreferences,
    summarizeHistory
  };
}
