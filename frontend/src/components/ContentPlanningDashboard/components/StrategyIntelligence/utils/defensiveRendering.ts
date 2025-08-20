// Utility functions for defensive rendering in strategy components

/**
 * Safely renders text content, handling objects, arrays, and other non-string types
 */
export const safeRenderText = (content: any): string => {
  if (typeof content === 'string') return content;
  if (typeof content === 'number') return content.toString();
  if (typeof content === 'boolean') return content.toString();
  if (Array.isArray(content)) return content.join(', ');
  if (typeof content === 'object' && content !== null) {
    // If it's an empty object, return a fallback message
    if (Object.keys(content).length === 0) {
      return 'Data not available';
    }
    // If it has a meaningful structure, try to extract useful information
    if (content.title) return content.title;
    if (content.name) return content.name;
    if (content.description) return content.description;
    if (content.text) return content.text;
    // As a last resort, stringify the object
    return JSON.stringify(content);
  }
  return 'Data not available';
};

/**
 * Safely renders array content, ensuring it's always an array
 */
export const safeRenderArray = (content: any): any[] => {
  if (Array.isArray(content)) return content;
  if (typeof content === 'string') return [content];
  if (typeof content === 'object' && content !== null) {
    // If it's an empty object, return empty array
    if (Object.keys(content).length === 0) {
      return [];
    }
    // Try to extract array-like data
    if (content.items && Array.isArray(content.items)) return content.items;
    if (content.data && Array.isArray(content.data)) return content.data;
    if (content.list && Array.isArray(content.list)) return content.list;
    // As a last resort, return the object as a single item
    return [content];
  }
  return [];
};

/**
 * Safely renders object content, ensuring it's always a valid object
 */
export const safeRenderObject = (content: any): Record<string, any> => {
  if (typeof content === 'object' && content !== null) {
    return content;
  }
  return {};
};

/**
 * Validates if a strategy data field contains meaningful data
 */
export const hasValidData = (content: any): boolean => {
  if (content === null || content === undefined) return false;
  if (typeof content === 'string') return content.trim().length > 0;
  if (Array.isArray(content)) return content.length > 0;
  if (typeof content === 'object') {
    // Check if it's an empty object
    if (Object.keys(content).length === 0) return false;
    // Check if it has meaningful properties
    return Object.values(content).some(value => hasValidData(value));
  }
  return true;
};

/**
 * Gets a fallback value for empty or invalid data
 */
export const getFallbackValue = (fieldName: string): string => {
  const fallbacks: Record<string, string> = {
    insight: 'Insight data not available',
    recommendation: 'Recommendation data not available',
    prediction: 'Prediction data not available',
    analysis: 'Analysis data not available',
    strategy: 'Strategy data not available',
    risk: 'Risk data not available',
    opportunity: 'Opportunity data not available',
    strength: 'Strength data not available',
    weakness: 'Weakness data not available',
    threat: 'Threat data not available',
    milestone: 'Milestone data not available',
    task: 'Task data not available',
    resource: 'Resource data not available',
    requirement: 'Requirement data not available',
    metric: 'Metric data not available',
    gap: 'Gap data not available',
    advantage: 'Advantage data not available',
    area: 'Area data not available',
    path: 'Path data not available'
  };
  
  return fallbacks[fieldName.toLowerCase()] || 'Data not available';
};
