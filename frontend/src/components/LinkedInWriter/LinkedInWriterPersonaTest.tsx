/**
 * LinkedIn Writer Persona Integration Test Page
 * Demonstrates the enhanced LinkedIn writer with persona-aware features
 * Allows testing of different integration approaches
 */

import React, { useState } from 'react';
import { EnhancedLinkedInWriter, LinkedInWriterInlinePersona } from './LinkedInWriterWithPersona';

// Integration type options
type IntegrationType = 'sidebar' | 'inline' | 'original';

// Test page component
export const LinkedInWriterPersonaTest: React.FC = () => {
  const [integrationType, setIntegrationType] = useState<IntegrationType>('sidebar');
  const [showPersonaInfo, setShowPersonaInfo] = useState(true);

  const renderSelectedIntegration = () => {
    switch (integrationType) {
      case 'sidebar':
        return <EnhancedLinkedInWriter />;
      case 'inline':
        return <LinkedInWriterInlinePersona />;
      case 'original':
        return (
          <div className="p-6">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <h3 className="text-lg font-semibold text-yellow-800 mb-2">Original LinkedIn Writer</h3>
              <p className="text-yellow-700">
                This shows the original LinkedIn writer without persona integration. 
                Switch to "Sidebar" or "Inline" to see the enhanced version.
              </p>
            </div>
            <div className="border rounded-lg p-4 bg-gray-50">
              <p className="text-gray-600 text-center">
                Original LinkedIn Writer Component would render here
              </p>
            </div>
          </div>
        );
      default:
        return <EnhancedLinkedInWriter />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                LinkedIn Writer Persona Integration Test
              </h1>
              <p className="text-gray-600 mt-2">
                Test the enhanced LinkedIn writer with persona-aware AI assistance
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="showPersonaInfo"
                  checked={showPersonaInfo}
                  onChange={(e) => setShowPersonaInfo(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <label htmlFor="showPersonaInfo" className="text-sm text-gray-700">
                  Show Persona Info
                </label>
              </div>
            </div>
          </div>

          {/* Integration Type Selector */}
          <div className="mt-6">
            <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
              {[
                { value: 'sidebar', label: 'Sidebar Integration', description: 'Persona chat in right sidebar' },
                { value: 'inline', label: 'Inline Integration', description: 'Persona banner above content' },
                { value: 'original', label: 'Original Writer', description: 'No persona integration' }
              ].map((option) => (
                <button
                  key={option.value}
                  onClick={() => setIntegrationType(option.value as IntegrationType)}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                    integrationType === option.value
                      ? 'bg-white text-gray-900 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <div className="text-center">
                    <div className="font-medium">{option.label}</div>
                    <div className="text-xs opacity-75 mt-1">{option.description}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Feature Comparison */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-2">Sidebar Integration</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Persona chat in dedicated sidebar</li>
                <li>• Full-screen content editing</li>
                <li>• Collapsible chat interface</li>
                <li>• Clean separation of concerns</li>
              </ul>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h4 className="font-semibold text-green-900 mb-2">Inline Integration</h4>
              <ul className="text-sm text-green-800 space-y-1">
                <li>• Persona banner above content</li>
                <li>• Floating chat button</li>
                <li>• Maintains existing layout</li>
                <li>• Subtle persona presence</li>
              </ul>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-2">Original Writer</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• No persona integration</li>
                <li>• Standard LinkedIn writer</li>
                <li>• Baseline functionality</li>
                <li>• Comparison reference</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        {renderSelectedIntegration()}
      </div>

      {/* Footer Instructions */}
      <div className="bg-white border-t border-gray-200 p-6">
        <div className="max-w-7xl mx-auto">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">How to Test</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Testing Persona Integration</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Switch between integration types to see different approaches</li>
                <li>• Check if persona data loads correctly in the sidebar/banner</li>
                <li>• Test the persona-aware chat functionality</li>
                <li>• Verify that persona context is injected into CopilotKit</li>
                <li>• Test platform-specific LinkedIn optimizations</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Expected Behavior</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Persona info should display your writing style and preferences</li>
                <li>• Chat should provide LinkedIn-specific content advice</li>
                <li>• AI responses should match your linguistic fingerprint</li>
                <li>• Platform constraints should be respected (character limits, etc.)</li>
                <li>• Seamless integration with existing LinkedIn writer functionality</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LinkedInWriterPersonaTest;
