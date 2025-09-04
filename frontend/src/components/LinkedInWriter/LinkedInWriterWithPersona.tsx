/**
 * Enhanced LinkedIn Writer with Persona Integration
 * Wraps the existing LinkedIn writer with persona context and adds persona-aware chat
 * Provides intelligent, contextual assistance based on user's writing persona
 */

import React, { useState } from 'react';
import { PlatformPersonaProvider, usePlatformPersonaContext } from '../shared/PersonaContext';
import { PlatformPersonaChat } from '../shared/CopilotKit';
import LinkedInWriter from './LinkedInWriter';
import { PlatformType } from '../../types/PlatformPersonaTypes';

// Persona Info Display Component
const PersonaInfoDisplay: React.FC = () => {
  const { corePersona, platformPersona, loading, error } = usePlatformPersonaContext();

  if (loading) {
    return (
      <div className="flex items-center justify-center p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
        <span className="text-sm text-blue-700">Loading persona...</span>
      </div>
    );
  }

  if (error || !corePersona) {
    return (
      <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
        <div className="flex items-center">
          <svg className="h-4 w-4 text-yellow-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span className="text-sm text-yellow-700">Persona not available - using default LinkedIn settings</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-3 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
            <span className="text-blue-600 font-semibold text-sm">
              {corePersona.persona_name.charAt(0).toUpperCase()}
            </span>
          </div>
          <div>
            <h4 className="font-medium text-blue-900 text-sm">
              {corePersona.persona_name}
            </h4>
            <p className="text-xs text-blue-700">{corePersona.archetype}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
            LinkedIn
          </div>
          <div className="text-xs text-blue-600 mt-1">
            {corePersona.confidence_score}% confidence
          </div>
        </div>
      </div>
      
      {/* Linguistic Fingerprint Summary */}
      {corePersona.linguistic_fingerprint && (
        <div className="mt-2 pt-2 border-t border-blue-200">
          <div className="flex items-center justify-between text-xs text-blue-700">
            <span>Style: {corePersona.linguistic_fingerprint.lexical_features.vocabulary_level}</span>
            <span>Length: ~{corePersona.linguistic_fingerprint.sentence_metrics.average_sentence_length_words} words</span>
            <span>Voice: {corePersona.linguistic_fingerprint.sentence_metrics.active_to_passive_ratio}</span>
          </div>
        </div>
      )}

      {/* Platform Optimization */}
      {platformPersona && (
        <div className="mt-2 pt-2 border-t border-blue-200">
          <div className="flex items-center justify-between text-xs text-blue-700">
            <span>Optimal: {platformPersona.content_format_rules?.optimal_length || 'N/A'}</span>
            <span>Limit: {platformPersona.content_format_rules?.character_limit || 'N/A'} chars</span>
            <span>Frequency: {platformPersona.engagement_patterns?.posting_frequency || 'N/A'}</span>
          </div>
        </div>
      )}
    </div>
  );
};

// Persona-Aware Chat Panel
const PersonaChatPanel: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="border-l border-gray-200 bg-white">
      {/* Chat Header */}
      <div className="p-3 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center justify-between">
          <h3 className="font-medium text-gray-900 text-sm">AI Content Assistant</h3>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-gray-500 hover:text-gray-700 transition-colors"
          >
            <svg 
              className={`w-4 h-4 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
        <p className="text-xs text-gray-600 mt-1">
          Get personalized LinkedIn content advice based on your writing style
        </p>
      </div>

      {/* Persona Info */}
      <div className="p-3">
        <PersonaInfoDisplay />
      </div>

      {/* Chat Interface */}
      <div className={`transition-all duration-300 ease-in-out ${isExpanded ? 'max-h-96' : 'max-h-0'} overflow-hidden`}>
        <div className="p-3">
          <PlatformPersonaChat
            platform="linkedin"
            showWelcomeMessage={true}
            showSuggestedPrompts={true}
            className="border rounded-lg"
          />
        </div>
      </div>
    </div>
  );
};

// Enhanced LinkedIn Writer Container
const EnhancedLinkedInWriter: React.FC = () => {
  return (
    <PlatformPersonaProvider platform="linkedin">
      <div className="flex h-screen bg-gray-50">
        {/* Main LinkedIn Writer */}
        <div className="flex-1 flex flex-col">
          <LinkedInWriter />
        </div>
        
        {/* Persona Chat Sidebar */}
        <div className="w-80 flex-shrink-0">
          <PersonaChatPanel />
        </div>
      </div>
    </PlatformPersonaProvider>
  );
};

// Alternative: Inline Integration (if you prefer to keep the existing layout)
const LinkedInWriterInlinePersona: React.FC = () => {
  return (
    <PlatformPersonaProvider platform="linkedin">
      <div className="linkedin-writer-with-persona">
        {/* Persona Banner */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-200 p-4">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-blue-900">LinkedIn Content Writer</h2>
                  <p className="text-sm text-blue-700">Powered by your personal writing persona</p>
                </div>
              </div>
              <PersonaInfoDisplay />
            </div>
          </div>
        </div>

        {/* Main LinkedIn Writer */}
        <LinkedInWriter />

        {/* Floating Persona Chat Button */}
        <div className="fixed bottom-6 right-6 z-50">
          <button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg transition-all duration-200 hover:scale-110">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </button>
        </div>
      </div>
    </PlatformPersonaProvider>
  );
};

// Export both integration options
export { EnhancedLinkedInWriter, LinkedInWriterInlinePersona };

// Default export for the enhanced version
export default EnhancedLinkedInWriter;
