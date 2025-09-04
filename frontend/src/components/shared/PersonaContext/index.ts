/**
 * Persona Context Index
 * Central export point for all persona context components and hooks
 */

export { 
  PlatformPersonaProvider, 
  PlatformPersonaContext,
  usePlatformPersonaContext 
} from './PlatformPersonaProvider';

export { PersonaTestComponent } from './PersonaTestComponent';

// Re-export types for convenience
export type { 
  PlatformType,
  WritingPersona,
  PlatformAdaptation 
} from '../../../types/PlatformPersonaTypes';
