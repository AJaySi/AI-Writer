/**
 * Platform Persona Provider
 * React Context provider for platform-specific persona data
 * Integrates with existing persona API client and injects data into CopilotKit
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useCopilotReadable } from '@copilotkit/react-core';
import { 
  WritingPersona, 
  PlatformAdaptation, 
  PlatformType,
  UserPersonasResponse,
  PlatformPersonaResponse
} from '../../../types/PlatformPersonaTypes';
import { 
  getUserPersonas, 
  getPlatformPersona 
} from '../../../api/persona';

// Context interface
interface PlatformPersonaContextType {
  corePersona: WritingPersona | null;
  platformPersona: PlatformAdaptation | null;
  platform: PlatformType;
  loading: boolean;
  error: string | null;
  refreshPersonas: () => Promise<void>;
}

// Create the context
const PlatformPersonaContext = createContext<PlatformPersonaContextType | null>(null);

// Provider props interface
interface PlatformPersonaProviderProps {
  children: ReactNode;
  platform: PlatformType;
  userId?: number; // Default to 1 for now, can be enhanced with auth context later
}

// Provider component
export const PlatformPersonaProvider: React.FC<PlatformPersonaProviderProps> = ({ 
  children, 
  platform, 
  userId = 1 
}) => {
  // State management
  const [corePersona, setCorePersona] = useState<WritingPersona | null>(null);
  const [platformPersona, setPlatformPersona] = useState<PlatformAdaptation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch persona data function
  const fetchPersonas = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch both core persona and platform-specific data
      const [userPersonasResponse, platformPersonaResponse] = await Promise.all([
        getUserPersonas(userId),
        getPlatformPersona(userId, platform)
      ]);

      // Handle core persona data
      if (userPersonasResponse.personas && userPersonasResponse.personas.length > 0) {
        const primaryPersona = userPersonasResponse.personas[0];
        setCorePersona(primaryPersona);
        
        console.log('✅ Core persona loaded:', {
          name: primaryPersona.persona_name,
          archetype: primaryPersona.archetype,
          confidence: primaryPersona.confidence_score
        });
      } else {
        console.warn('⚠️ No core personas found for user');
        setCorePersona(null);
      }

      // Handle platform-specific persona data
      if (platformPersonaResponse) {
        setPlatformPersona(platformPersonaResponse);
        
        console.log('✅ Platform persona loaded:', {
          platform: platformPersonaResponse.platform_type,
          characterLimit: platformPersonaResponse.content_format_rules?.character_limit,
          optimalLength: platformPersonaResponse.content_format_rules?.optimal_length
        });
      } else {
        console.warn(`⚠️ No platform-specific persona found for ${platform}`);
        setPlatformPersona(null);
      }

    } catch (error) {
      console.error('❌ Error fetching personas:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch persona data');
      
      // Set fallback data if available
      if (corePersona) {
        console.log('🔄 Using existing core persona data');
      }
    } finally {
      setLoading(false);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchPersonas();
  }, [platform, userId]);

  // Refresh function for manual updates
  const refreshPersonas = async () => {
    await fetchPersonas();
  };

  // Inject core persona into CopilotKit context
  useCopilotReadable({
    description: `Core writing persona: ${corePersona?.persona_name || 'Loading...'}`,
    value: corePersona,
    categories: ["core-persona", "writing-style", "user-preferences"],
    parentId: corePersona?.id?.toString()
  });

  // Inject platform-specific persona into CopilotKit context
  useCopilotReadable({
    description: `${platform} platform optimization rules and constraints`,
    value: platformPersona,
    categories: ["platform-persona", platform, "content-optimization"],
    parentId: corePersona?.id?.toString()
  });

  // Inject combined persona context for comprehensive understanding
  useCopilotReadable({
    description: `Complete ${platform} writing persona with linguistic fingerprint and platform optimization`,
    value: {
      core: corePersona,
      platform: platformPersona,
      combined: {
        persona_name: corePersona?.persona_name,
        archetype: corePersona?.archetype,
        platform: platform,
        linguistic_fingerprint: corePersona?.linguistic_fingerprint,
        platform_constraints: platformPersona?.content_format_rules,
        engagement_patterns: platformPersona?.engagement_patterns
      }
    },
    categories: ["complete-persona", platform, "writing-guidance"],
    parentId: corePersona?.id?.toString()
  });

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
          <p className="text-sm text-gray-600">Loading {platform} persona...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error && !corePersona) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Failed to load persona data</h3>
            <p className="text-sm text-red-700 mt-1">{error}</p>
            <button
              onClick={refreshPersonas}
              className="mt-2 text-sm text-red-600 hover:text-red-500 underline"
            >
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Success state - provide context
  return (
    <PlatformPersonaContext.Provider value={{ 
      corePersona, 
      platformPersona, 
      platform,
      loading,
      error,
      refreshPersonas
    }}>
      {children}
    </PlatformPersonaContext.Provider>
  );
};

// Custom hook to use the context
export const usePlatformPersonaContext = () => {
  const context = useContext(PlatformPersonaContext);
  if (!context) {
    throw new Error('usePlatformPersonaContext must be used within PlatformPersonaProvider');
  }
  return context;
};

// Export the context for direct access if needed
export { PlatformPersonaContext };
