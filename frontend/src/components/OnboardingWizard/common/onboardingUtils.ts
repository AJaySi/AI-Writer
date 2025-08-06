// Validation utilities
export const validateApiKey = (key: string, provider: string): boolean | null => {
  if (!key.trim()) return null;
  
  const patterns = {
    openai: /^sk-[a-zA-Z0-9]{32,}$/,
    gemini: /^AIza[a-zA-Z0-9_-]{35}$/,
    anthropic: /^sk-ant-[a-zA-Z0-9]{32,}$/,
    mistral: /^[a-zA-Z0-9]{32,}$/,
  };
  
  const pattern = patterns[provider as keyof typeof patterns];
  return pattern ? pattern.test(key) : true;
};

export const getKeyStatus = (key: string, provider: string): 'valid' | 'invalid' | 'empty' => {
  if (!key.trim()) return 'empty';
  const isValid = validateApiKey(key, provider);
  return isValid ? 'valid' : 'invalid';
};

// Animation utilities
export const getAnimationDelay = (index: number, baseDelay: number = 100): number => {
  return baseDelay * index;
};

export const getSlideDirection = (currentStep: number, targetStep: number): 'left' | 'right' => {
  return targetStep > currentStep ? 'right' : 'left';
};

// Progress utilities
export const calculateProgress = (currentStep: number, totalSteps: number): number => {
  return ((currentStep + 1) / totalSteps) * 100;
};

// Form utilities
export const isFormValid = (values: Record<string, string>): boolean => {
  return Object.values(values).some(value => value.trim() !== '');
};

// Status utilities
export const getStatusColor = (status: 'valid' | 'invalid' | 'empty'): string => {
  switch (status) {
    case 'valid':
      return '#4caf50';
    case 'invalid':
      return '#f44336';
    default:
      return 'transparent';
  }
};

export const getStatusLabel = (status: 'valid' | 'invalid' | 'empty'): string => {
  switch (status) {
    case 'valid':
      return 'Valid';
    case 'invalid':
      return 'Invalid';
    default:
      return '';
  }
};

// Auto-save utilities
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

// Error handling utilities
export const formatErrorMessage = (error: any): string => {
  if (typeof error === 'string') return error;
  if (error?.message) return error.message;
  return 'An unexpected error occurred. Please try again.';
};

// URL validation
export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

// Text validation
export const validateRequired = (value: string): boolean => {
  return value.trim().length > 0;
};

export const validateMinLength = (value: string, minLength: number): boolean => {
  return value.trim().length >= minLength;
};

export const validateMaxLength = (value: string, maxLength: number): boolean => {
  return value.trim().length <= maxLength;
}; 