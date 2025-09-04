/**
 * Persona Test Component
 * Simple component to test and demonstrate the PlatformPersonaProvider
 * This can be used to verify the implementation works correctly
 */

import React from 'react';
import { PlatformPersonaProvider, usePlatformPersonaContext } from './index';
import { PlatformType } from '../../../types/PlatformPersonaTypes';

// Test component that uses the context
const PersonaDisplay: React.FC = () => {
  const { 
    corePersona, 
    platformPersona, 
    platform, 
    loading, 
    error, 
    refreshPersonas 
  } = usePlatformPersonaContext();

  if (loading) {
    return <div>Loading persona data...</div>;
  }

  if (error) {
    return (
      <div>
        <p>Error: {error}</p>
        <button onClick={refreshPersonas}>Retry</button>
      </div>
    );
  }

  return (
    <div className="p-4 border rounded-lg">
      <h3 className="text-lg font-semibold mb-4">Persona Data for {platform}</h3>
      
      {/* Core Persona Display */}
      {corePersona && (
        <div className="mb-4 p-3 bg-blue-50 rounded">
          <h4 className="font-medium text-blue-900">Core Persona</h4>
          <p><strong>Name:</strong> {corePersona.persona_name}</p>
          <p><strong>Archetype:</strong> {corePersona.archetype}</p>
          <p><strong>Core Belief:</strong> {corePersona.core_belief}</p>
          <p><strong>Confidence:</strong> {corePersona.confidence_score}%</p>
        </div>
      )}

      {/* Platform Persona Display */}
      {platformPersona && (
        <div className="mb-4 p-3 bg-green-50 rounded">
          <h4 className="font-medium text-green-900">Platform Optimization</h4>
          <p><strong>Platform:</strong> {platformPersona.platform_type}</p>
          <p><strong>Character Limit:</strong> {platformPersona.content_format_rules?.character_limit || 'N/A'}</p>
          <p><strong>Optimal Length:</strong> {platformPersona.content_format_rules?.optimal_length || 'N/A'}</p>
          <p><strong>Posting Frequency:</strong> {platformPersona.engagement_patterns?.posting_frequency || 'N/A'}</p>
        </div>
      )}

      {/* Linguistic Fingerprint Display */}
      {corePersona?.linguistic_fingerprint && (
        <div className="mb-4 p-3 bg-purple-50 rounded">
          <h4 className="font-medium text-purple-900">Linguistic Fingerprint</h4>
          <p><strong>Avg Sentence Length:</strong> {corePersona.linguistic_fingerprint.sentence_metrics.average_sentence_length_words} words</p>
          <p><strong>Voice Ratio:</strong> {corePersona.linguistic_fingerprint.sentence_metrics.active_to_passive_ratio}</p>
          <p><strong>Go-to Words:</strong> {corePersona.linguistic_fingerprint.lexical_features.go_to_words?.join(', ') || 'N/A'}</p>
        </div>
      )}

      {/* Refresh Button */}
      <button
        onClick={refreshPersonas}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Refresh Personas
      </button>
    </div>
  );
};

// Main test component with provider
interface PersonaTestComponentProps {
  platform: PlatformType;
  userId?: number;
}

export const PersonaTestComponent: React.FC<PersonaTestComponentProps> = ({ 
  platform, 
  userId = 1 
}) => {
  return (
    <PlatformPersonaProvider platform={platform} userId={userId}>
      <PersonaDisplay />
    </PlatformPersonaProvider>
  );
};

export default PersonaTestComponent;
