/**
 * Onboarding Cache Service
 * Manages client-side caching of onboarding data until final submission
 */

interface OnboardingCacheData {
  step1?: {
    apiKeys?: Record<string, string>;
    providers?: string[];
  };
  step2?: {
    website?: string;
    analysis?: any;
    businessInfo?: any;
    hasWebsite?: boolean;
  };
  step3?: {
    researchPreferences?: any;
  };
  step4?: {
    personalization?: any;
  };
  step5?: {
    integrations?: any;
  };
}

class OnboardingCacheService {
  private readonly CACHE_KEY = 'alwrity_onboarding_cache';
  private readonly EXPIRY_KEY = 'alwrity_onboarding_cache_expiry';
  private readonly CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

  /**
   * Save data for a specific step
   */
  saveStepData(stepNumber: number, data: any): void {
    try {
      const cache = this.getCache();
      const stepKey = `step${stepNumber}` as keyof OnboardingCacheData;
      cache[stepKey] = { ...cache[stepKey], ...data };
      this.setCache(cache);
      console.log(`✅ Onboarding cache: Saved step ${stepNumber} data`, data);
    } catch (error) {
      console.error(`❌ Onboarding cache: Failed to save step ${stepNumber} data`, error);
    }
  }

  /**
   * Get data for a specific step
   */
  getStepData(stepNumber: number): any {
    try {
      const cache = this.getCache();
      const stepKey = `step${stepNumber}` as keyof OnboardingCacheData;
      const data = cache[stepKey];
      console.log(`📋 Onboarding cache: Retrieved step ${stepNumber} data`, data);
      return data;
    } catch (error) {
      console.error(`❌ Onboarding cache: Failed to get step ${stepNumber} data`, error);
      return null;
    }
  }

  /**
   * Get all cached data
   */
  getAllData(): OnboardingCacheData {
    try {
      const cache = this.getCache();
      console.log('📋 Onboarding cache: Retrieved all data', cache);
      return cache;
    } catch (error) {
      console.error('❌ Onboarding cache: Failed to get all data', error);
      return {};
    }
  }

  /**
   * Clear all cached data
   */
  clearCache(): void {
    try {
      localStorage.removeItem(this.CACHE_KEY);
      localStorage.removeItem(this.EXPIRY_KEY);
      console.log('🗑️ Onboarding cache: Cleared all data');
    } catch (error) {
      console.error('❌ Onboarding cache: Failed to clear cache', error);
    }
  }

  /**
   * Check if cache is valid (not expired)
   */
  isCacheValid(): boolean {
    try {
      const expiry = localStorage.getItem(this.EXPIRY_KEY);
      if (!expiry) return false;
      
      const expiryTime = parseInt(expiry, 10);
      const now = Date.now();
      const isValid = now < expiryTime;
      
      if (!isValid) {
        console.log('⏰ Onboarding cache: Cache expired, clearing...');
        this.clearCache();
      }
      
      return isValid;
    } catch (error) {
      console.error('❌ Onboarding cache: Failed to check cache validity', error);
      return false;
    }
  }

  /**
   * Get cache from localStorage
   */
  private getCache(): OnboardingCacheData {
    if (!this.isCacheValid()) {
      return {};
    }

    try {
      const cached = localStorage.getItem(this.CACHE_KEY);
      return cached ? JSON.parse(cached) : {};
    } catch (error) {
      console.error('❌ Onboarding cache: Failed to parse cache data', error);
      return {};
    }
  }

  /**
   * Set cache in localStorage
   */
  private setCache(data: OnboardingCacheData): void {
    try {
      const expiry = Date.now() + this.CACHE_DURATION;
      localStorage.setItem(this.CACHE_KEY, JSON.stringify(data));
      localStorage.setItem(this.EXPIRY_KEY, expiry.toString());
      console.log('💾 Onboarding cache: Data saved to localStorage');
    } catch (error) {
      console.error('❌ Onboarding cache: Failed to save to localStorage', error);
    }
  }

  /**
   * Get API keys from cache
   */
  getApiKeys(): Record<string, string> {
    const step1Data = this.getStepData(1);
    return step1Data?.apiKeys || {};
  }

  /**
   * Save API key to cache
   */
  saveApiKey(provider: string, apiKey: string): void {
    const step1Data = this.getStepData(1) || {};
    const apiKeys = step1Data.apiKeys || {};
    apiKeys[provider] = apiKey;
    this.saveStepData(1, { ...step1Data, apiKeys });
  }

  /**
   * Get website data from cache
   */
  getWebsiteData(): any {
    return this.getStepData(2);
  }

  /**
   * Save website data to cache
   */
  saveWebsiteData(data: any): void {
    this.saveStepData(2, data);
  }
}

// Export singleton instance
export const onboardingCache = new OnboardingCacheService();
console.log('✅ Onboarding Cache Service loaded successfully!');
