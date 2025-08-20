import { StrategyData } from '../types/strategy.types';
import { hasValidData } from './defensiveRendering';

/**
 * Validates strategy data to ensure it's safe for rendering
 */
export const validateStrategyData = (data: StrategyData | null | undefined): {
  isValid: boolean;
  errors: string[];
  warnings: string[];
} => {
  const errors: string[] = [];
  const warnings: string[] = [];

  if (!data) {
    return {
      isValid: false,
      errors: ['Strategy data is null or undefined'],
      warnings: []
    };
  }

  // Check for empty objects that could cause rendering issues
  const checkForEmptyObjects = (obj: any, path: string): void => {
    if (typeof obj === 'object' && obj !== null) {
      if (Array.isArray(obj)) {
        obj.forEach((item, index) => {
          checkForEmptyObjects(item, `${path}[${index}]`);
        });
      } else {
        const keys = Object.keys(obj);
        if (keys.length === 0) {
          warnings.push(`Empty object found at ${path}`);
        } else {
          keys.forEach(key => {
            checkForEmptyObjects(obj[key], `${path}.${key}`);
          });
        }
      }
    }
  };

  // Check each major component
  const components = [
    { name: 'strategic_insights', data: data.strategic_insights },
    { name: 'competitive_analysis', data: data.competitive_analysis },
    { name: 'performance_predictions', data: data.performance_predictions },
    { name: 'implementation_roadmap', data: data.implementation_roadmap },
    { name: 'risk_assessment', data: data.risk_assessment }
  ];

  components.forEach(({ name, data: componentData }) => {
    if (componentData) {
      checkForEmptyObjects(componentData, name);
      
      // Check if the component has meaningful data
      if (!hasValidData(componentData)) {
        warnings.push(`${name} component exists but contains no meaningful data`);
      }
    } else {
      warnings.push(`${name} component is missing`);
    }
  });

  // Check metadata
  if (data.strategy_metadata) {
    checkForEmptyObjects(data.strategy_metadata, 'strategy_metadata');
  }

  if (data.metadata) {
    checkForEmptyObjects(data.metadata, 'metadata');
  }

  // Check summary
  if (data.summary) {
    checkForEmptyObjects(data.summary, 'summary');
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings
  };
};

/**
 * Sanitizes strategy data to prevent rendering errors
 */
export const sanitizeStrategyData = (data: StrategyData | null | undefined): StrategyData | null => {
  if (!data) return null;

  const sanitizeValue = (value: any): any => {
    if (value === null || value === undefined) {
      return null;
    }
    
    if (typeof value === 'object') {
      if (Array.isArray(value)) {
        return value.map(sanitizeValue).filter(v => v !== null);
      } else {
        const keys = Object.keys(value);
        if (keys.length === 0) {
          return null; // Remove empty objects
        }
        
        const sanitized: any = {};
        keys.forEach(key => {
          const sanitizedValue = sanitizeValue(value[key]);
          if (sanitizedValue !== null) {
            sanitized[key] = sanitizedValue;
          }
        });
        
        return Object.keys(sanitized).length > 0 ? sanitized : null;
      }
    }
    
    return value;
  };

  // Create a deep copy and sanitize
  const sanitized = JSON.parse(JSON.stringify(data));
  
  // Sanitize each component
  if (sanitized.strategic_insights) {
    sanitized.strategic_insights = sanitizeValue(sanitized.strategic_insights);
  }
  
  if (sanitized.competitive_analysis) {
    sanitized.competitive_analysis = sanitizeValue(sanitized.competitive_analysis);
  }
  
  if (sanitized.performance_predictions) {
    sanitized.performance_predictions = sanitizeValue(sanitized.performance_predictions);
  }
  
  if (sanitized.implementation_roadmap) {
    sanitized.implementation_roadmap = sanitizeValue(sanitized.implementation_roadmap);
  }
  
  if (sanitized.risk_assessment) {
    sanitized.risk_assessment = sanitizeValue(sanitized.risk_assessment);
  }

  return sanitized;
};

/**
 * Creates a safe strategy data object for rendering
 */
export const createSafeStrategyData = (data: StrategyData | null | undefined): StrategyData | null => {
  if (!data) return null;

  // First validate the data
  const validation = validateStrategyData(data);
  
  if (validation.errors.length > 0) {
    console.warn('Strategy data validation errors:', validation.errors);
  }
  
  if (validation.warnings.length > 0) {
    console.warn('Strategy data validation warnings:', validation.warnings);
  }

  // Then sanitize the data
  return sanitizeStrategyData(data);
};
