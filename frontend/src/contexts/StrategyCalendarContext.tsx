import React, { createContext, useContext, useReducer, useEffect, useCallback, ReactNode } from 'react';
import { StrategyContext, CalendarContext, WorkflowProgress } from '../services/navigationOrchestrator';

// Context state interface
interface StrategyCalendarState {
  activeStrategy: any | null;
  strategyContext: StrategyContext | null;
  calendarContext: CalendarContext | null;
  workflowProgress: WorkflowProgress;
  isContextValid: boolean;
  lastUpdated: string | null;
  error: string | null;
}

// Action types
type StrategyCalendarAction =
  | { type: 'SET_ACTIVE_STRATEGY'; payload: any }
  | { type: 'SET_STRATEGY_CONTEXT'; payload: StrategyContext }
  | { type: 'SET_CALENDAR_CONTEXT'; payload: CalendarContext }
  | { type: 'UPDATE_WORKFLOW_PROGRESS'; payload: Partial<WorkflowProgress> }
  | { type: 'CLEAR_CONTEXT' }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'CLEAR_ERROR' }
  | { type: 'VALIDATE_CONTEXT' };

// Initial state
const initialState: StrategyCalendarState = {
  activeStrategy: null,
  strategyContext: null,
  calendarContext: null,
  workflowProgress: {
    currentStep: 'strategy',
    completedSteps: [],
    totalSteps: 4,
    progressPercentage: 0
  },
  isContextValid: false,
  lastUpdated: null,
  error: null
};

// Reducer function
function strategyCalendarReducer(state: StrategyCalendarState, action: StrategyCalendarAction): StrategyCalendarState {
  switch (action.type) {
    case 'SET_ACTIVE_STRATEGY':
      return {
        ...state,
        activeStrategy: action.payload,
        lastUpdated: new Date().toISOString(),
        error: null
      };

    case 'SET_STRATEGY_CONTEXT':
      return {
        ...state,
        strategyContext: action.payload,
        lastUpdated: new Date().toISOString(),
        error: null
      };

    case 'SET_CALENDAR_CONTEXT':
      return {
        ...state,
        calendarContext: action.payload,
        lastUpdated: new Date().toISOString(),
        error: null
      };

    case 'UPDATE_WORKFLOW_PROGRESS':
      return {
        ...state,
        workflowProgress: {
          ...state.workflowProgress,
          ...action.payload
        },
        lastUpdated: new Date().toISOString()
      };

    case 'CLEAR_CONTEXT':
      return {
        ...initialState,
        lastUpdated: new Date().toISOString()
      };

    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        lastUpdated: new Date().toISOString()
      };

    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null
      };

    case 'VALIDATE_CONTEXT':
      const isValid = validateContextIntegrity(state);
      return {
        ...state,
        isContextValid: isValid,
        lastUpdated: new Date().toISOString()
      };

    default:
      return state;
  }
}

// Context validation function
function validateContextIntegrity(state: StrategyCalendarState): boolean {
  try {
    // Check if strategy context exists and has required fields
    if (state.strategyContext) {
      const { strategyId, strategyData, activationStatus } = state.strategyContext;
      if (!strategyId || !strategyData || !activationStatus) {
        return false;
      }
    }

    // Check if calendar context is valid when it exists
    if (state.calendarContext) {
      const { strategyContext, autoPopulatedData } = state.calendarContext;
      if (strategyContext && !validateContextIntegrity({ ...state, strategyContext })) {
        return false;
      }
    }

    // Check workflow progress validity
    const { currentStep, totalSteps, progressPercentage } = state.workflowProgress;
    if (!currentStep || totalSteps <= 0 || progressPercentage < 0 || progressPercentage > 100) {
      return false;
    }

    return true;
  } catch (error) {
    console.error('Context validation error:', error);
    return false;
  }
}

// Context interface
interface StrategyCalendarContextType {
  state: StrategyCalendarState;
  dispatch: React.Dispatch<StrategyCalendarAction>;
  
  // Convenience methods
  setActiveStrategy: (strategy: any) => void;
  setStrategyContext: (context: StrategyContext) => void;
  setCalendarContext: (context: CalendarContext) => void;
  updateWorkflowProgress: (progress: Partial<WorkflowProgress>) => void;
  clearContext: () => void;
  setError: (error: string) => void;
  clearError: () => void;
  validateContext: () => void;
  
  // Utility methods
  getStrategyData: () => any | null;
  getCalendarData: () => any | null;
  isStrategyActive: () => boolean;
  isCalendarReady: () => boolean;
  getWorkflowStep: () => string;
  getProgressPercentage: () => number;
  isFromStrategyActivation: () => boolean;
}

// Create context
const StrategyCalendarContext = createContext<StrategyCalendarContextType | undefined>(undefined);

// Provider component
interface StrategyCalendarProviderProps {
  children: ReactNode;
}

export const StrategyCalendarProvider: React.FC<StrategyCalendarProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(strategyCalendarReducer, initialState);

  // Validate context on state changes
  useEffect(() => {
    dispatch({ type: 'VALIDATE_CONTEXT' });
  }, [state.strategyContext, state.calendarContext, state.workflowProgress]);

  // Persist context to session storage
  useEffect(() => {
    if (state.lastUpdated) {
      try {
        sessionStorage.setItem('strategyCalendarContext', JSON.stringify({
          strategyContext: state.strategyContext,
          calendarContext: state.calendarContext,
          workflowProgress: state.workflowProgress,
          lastUpdated: state.lastUpdated
        }));
      } catch (error) {
        console.error('Failed to persist context to session storage:', error);
      }
    }
  }, [state.strategyContext, state.calendarContext, state.workflowProgress, state.lastUpdated]);

  // Restore context from session storage on mount
  useEffect(() => {
    try {
      const persisted = sessionStorage.getItem('strategyCalendarContext');
      if (persisted) {
        const data = JSON.parse(persisted);
        const lastUpdated = new Date(data.lastUpdated);
        const now = new Date();
        
        // Check if context is still valid (not older than 30 minutes)
        if (now.getTime() - lastUpdated.getTime() < 30 * 60 * 1000) {
          if (data.strategyContext) {
            dispatch({ type: 'SET_STRATEGY_CONTEXT', payload: data.strategyContext });
          }
          if (data.calendarContext) {
            dispatch({ type: 'SET_CALENDAR_CONTEXT', payload: data.calendarContext });
          }
          if (data.workflowProgress) {
            dispatch({ type: 'UPDATE_WORKFLOW_PROGRESS', payload: data.workflowProgress });
          }
        } else {
          // Clear expired context
          sessionStorage.removeItem('strategyCalendarContext');
        }
      }
    } catch (error) {
      console.error('Failed to restore context from session storage:', error);
    }
  }, []);

  // Convenience methods
  const setActiveStrategy = (strategy: any) => {
    dispatch({ type: 'SET_ACTIVE_STRATEGY', payload: strategy });
  };

  const setStrategyContext = (context: StrategyContext) => {
    dispatch({ type: 'SET_STRATEGY_CONTEXT', payload: context });
  };

  const setCalendarContext = (context: CalendarContext) => {
    dispatch({ type: 'SET_CALENDAR_CONTEXT', payload: context });
  };

  const updateWorkflowProgress = (progress: Partial<WorkflowProgress>) => {
    dispatch({ type: 'UPDATE_WORKFLOW_PROGRESS', payload: progress });
  };

  const clearContext = () => {
    dispatch({ type: 'CLEAR_CONTEXT' });
    sessionStorage.removeItem('strategyCalendarContext');
  };

  const setError = (error: string) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const validateContext = () => {
    dispatch({ type: 'VALIDATE_CONTEXT' });
  };

  // Utility methods
  const getStrategyData = () => state.strategyContext?.strategyData || null;
  
  const getCalendarData = () => state.calendarContext?.autoPopulatedData || null;
  
  const isStrategyActive = () => state.strategyContext?.activationStatus === 'active';
  
  const isCalendarReady = () => {
    return state.calendarContext !== null && 
           state.calendarContext.autoPopulatedData !== null &&
           state.isContextValid;
  };
  
  const getWorkflowStep = () => state.workflowProgress.currentStep;
  
  const getProgressPercentage = () => state.workflowProgress.progressPercentage;
  
  const isFromStrategyActivation = useCallback(() => {
    // Check if we have a preserved strategy context from navigation
    const result = state.strategyContext?.activationStatus === 'active' && 
                   state.strategyContext?.activationTimestamp !== null;
    console.log('🔍 StrategyCalendarContext: isFromStrategyActivation check:', {
      activationStatus: state.strategyContext?.activationStatus,
      activationTimestamp: state.strategyContext?.activationTimestamp,
      result
    });
    return result;
  }, [state.strategyContext?.activationStatus, state.strategyContext?.activationTimestamp]);

  const contextValue: StrategyCalendarContextType = {
    state,
    dispatch,
    setActiveStrategy,
    setStrategyContext,
    setCalendarContext,
    updateWorkflowProgress,
    clearContext,
    setError,
    clearError,
    validateContext,
    getStrategyData,
    getCalendarData,
    isStrategyActive,
    isCalendarReady,
    getWorkflowStep,
    getProgressPercentage,
    isFromStrategyActivation
  };

  return (
    <StrategyCalendarContext.Provider value={contextValue}>
      {children}
    </StrategyCalendarContext.Provider>
  );
};

// Custom hook to use the context
export const useStrategyCalendarContext = (): StrategyCalendarContextType => {
  const context = useContext(StrategyCalendarContext);
  if (context === undefined) {
    throw new Error('useStrategyCalendarContext must be used within a StrategyCalendarProvider');
  }
  return context;
};

// Hook for components that only need read access
export const useStrategyCalendarState = () => {
  const { state } = useStrategyCalendarContext();
  return state;
};

// Hook for components that need to dispatch actions
export const useStrategyCalendarActions = () => {
  const { 
    setActiveStrategy, 
    setStrategyContext, 
    setCalendarContext, 
    updateWorkflowProgress, 
    clearContext,
    setError,
    clearError,
    validateContext
  } = useStrategyCalendarContext();
  
  return {
    setActiveStrategy,
    setStrategyContext,
    setCalendarContext,
    updateWorkflowProgress,
    clearContext,
    setError,
    clearError,
    validateContext
  };
};
