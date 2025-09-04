/**
 * Platform Persona Chat Test Component
 * Demonstrates and tests the PlatformPersonaChat component
 * Shows how to integrate persona-aware chat into different platforms
 */

import React, { useState } from 'react';
import { PlatformPersonaProvider } from '../PersonaContext';
import { PlatformPersonaChat } from './index';
import { PlatformType } from '../../types/PlatformPersonaTypes';

// Platform selection component
const PlatformSelector: React.FC<{
  selectedPlatform: PlatformType;
  onPlatformChange: (platform: PlatformType) => void;
}> = ({ selectedPlatform, onPlatformChange }) => {
  const platforms: { value: PlatformType; label: string; description: string }[] = [
    { value: 'linkedin', label: 'LinkedIn', description: 'Professional networking & thought leadership' },
    { value: 'facebook', label: 'Facebook', description: 'Community building & social engagement' },
    { value: 'instagram', label: 'Instagram', description: 'Visual storytelling & aesthetic content' },
    { value: 'twitter', label: 'Twitter', description: 'Concise messaging & viral potential' },
    { value: 'blog', label: 'Blog', description: 'Long-form content & SEO optimization' },
    { value: 'medium', label: 'Medium', description: 'Storytelling & publication strategy' },
    { value: 'substack', label: 'Substack', description: 'Newsletter & subscription focus' }
  ];

  return (
    <div className="mb-6 p-4 bg-gray-50 border border-gray-200 rounded-lg">
      <h3 className="text-lg font-semibold mb-3">Select Platform to Test</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {platforms.map((platform) => (
          <button
            key={platform.value}
            onClick={() => onPlatformChange(platform.value)}
            className={`p-3 text-left rounded-lg border transition-all ${
              selectedPlatform === platform.value
                ? 'border-blue-500 bg-blue-50 text-blue-900'
                : 'border-gray-300 bg-white hover:border-gray-400 hover:bg-gray-50'
            }`}
          >
            <div className="font-medium">{platform.label}</div>
            <div className="text-sm text-gray-600 mt-1">{platform.description}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

// Chat configuration options
const ChatConfigOptions: React.FC<{
  showWelcomeMessage: boolean;
  showSuggestedPrompts: boolean;
  onToggleWelcomeMessage: () => void;
  onToggleSuggestedPrompts: () => void;
}> = ({ showWelcomeMessage, showSuggestedPrompts, onToggleWelcomeMessage, onToggleSuggestedPrompts }) => {
  return (
    <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
      <h4 className="text-sm font-medium text-yellow-900 mb-2">Chat Configuration</h4>
      <div className="flex flex-wrap gap-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={showWelcomeMessage}
            onChange={onToggleWelcomeMessage}
            className="mr-2"
          />
          <span className="text-sm text-yellow-800">Show Welcome Message</span>
        </label>
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={showSuggestedPrompts}
            onChange={onToggleSuggestedPrompts}
            className="mr-2"
          />
          <span className="text-sm text-yellow-800">Show Suggested Prompts</span>
        </label>
      </div>
    </div>
  );
};

// Main test component
export const PlatformPersonaChatTest: React.FC = () => {
  const [selectedPlatform, setSelectedPlatform] = useState<PlatformType>('linkedin');
  const [showWelcomeMessage, setShowWelcomeMessage] = useState(true);
  const [showSuggestedPrompts, setShowSuggestedPrompts] = useState(true);

  const toggleWelcomeMessage = () => setShowWelcomeMessage(!showWelcomeMessage);
  const toggleSuggestedPrompts = () => setShowSuggestedPrompts(!showSuggestedPrompts);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          Platform Persona Chat Test
        </h1>
        <p className="text-gray-600">
          Test the persona-aware CopilotKit integration across different platforms
        </p>
      </div>

      {/* Platform Selector */}
      <PlatformSelector
        selectedPlatform={selectedPlatform}
        onPlatformChange={setSelectedPlatform}
      />

      {/* Chat Configuration */}
      <ChatConfigOptions
        showWelcomeMessage={showWelcomeMessage}
        showSuggestedPrompts={showSuggestedPrompts}
        onToggleWelcomeMessage={toggleWelcomeMessage}
        onToggleSuggestedPrompts={toggleSuggestedPrompts}
      />

      {/* Persona Chat Component */}
      <div className="border rounded-lg overflow-hidden">
        <div className="bg-gray-100 px-4 py-2 border-b">
          <h3 className="font-medium text-gray-900">
            {selectedPlatform.charAt(0).toUpperCase() + selectedPlatform.slice(1)} Persona Chat
          </h3>
          <p className="text-sm text-gray-600">
            AI-powered content assistance with your personal writing style
          </p>
        </div>
        
        <PlatformPersonaProvider platform={selectedPlatform}>
          <PlatformPersonaChat
            platform={selectedPlatform}
            showWelcomeMessage={showWelcomeMessage}
            showSuggestedPrompts={showSuggestedPrompts}
            className="p-4"
          />
        </PlatformPersonaProvider>
      </div>

      {/* Usage Instructions */}
      <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <h4 className="font-medium text-green-900 mb-2">How to Test</h4>
        <ul className="text-sm text-green-800 space-y-1">
          <li>• Select different platforms to see platform-specific chat configurations</li>
          <li>• Toggle welcome message and suggested prompts to test different chat modes</li>
          <li>• Ask questions about content strategy, writing style, or platform optimization</li>
          <li>• Notice how the AI adapts responses to your persona and platform constraints</li>
          <li>• Try the quick action buttons for platform-specific suggestions</li>
        </ul>
      </div>

      {/* Technical Details */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">Technical Implementation</h4>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            <strong>Context Injection:</strong> The chat automatically receives your writing persona, 
            linguistic fingerprint, and platform-specific constraints through CopilotKit's context system.
          </p>
          <p>
            <strong>Dynamic System Messages:</strong> System messages are generated dynamically based on 
            your persona data and selected platform, ensuring AI responses match your writing style.
          </p>
          <p>
            <strong>Platform Optimization:</strong> Each platform has specific character limits, 
            engagement patterns, and best practices that are automatically incorporated into AI responses.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PlatformPersonaChatTest;
