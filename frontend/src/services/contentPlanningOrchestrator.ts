import { contentPlanningApi } from './contentPlanningApi';

export interface ServiceStatus {
  name: string;
  status: 'loading' | 'success' | 'error' | 'idle';
  progress: number;
  message: string;
  data?: any;
  error?: string;
}

export interface DashboardData {
  strategies: any[];
  gapAnalyses: any[];
  aiInsights: any[];
  aiRecommendations: any[];
  calendarEvents: any[];
  healthStatus: {
    backend: boolean;
    database: boolean;
    aiServices: boolean;
  };
}

export class ContentPlanningOrchestrator {
  private serviceStatuses: Map<string, ServiceStatus> = new Map();
  private onProgressUpdate?: (statuses: ServiceStatus[]) => void;
  private onDataUpdate?: (data: Partial<DashboardData>) => void;

  constructor() {
    this.initializeServiceStatuses();
  }

  private initializeServiceStatuses() {
    const services = [
      { name: 'strategies', displayName: 'Content Strategies' },
      { name: 'gapAnalyses', displayName: 'Gap Analysis' },
      { name: 'aiAnalytics', displayName: 'AI Analytics' },
      { name: 'calendarEvents', displayName: 'Calendar Events' },
      { name: 'healthCheck', displayName: 'System Health' }
    ];

    services.forEach(service => {
      this.serviceStatuses.set(service.name, {
        name: service.displayName,
        status: 'idle',
        progress: 0,
        message: 'Ready to load'
      });
    });
  }

  public setProgressCallback(callback: (statuses: ServiceStatus[]) => void) {
    this.onProgressUpdate = callback;
  }

  public setDataUpdateCallback(callback: (data: Partial<DashboardData>) => void) {
    this.onDataUpdate = callback;
  }

  private updateServiceStatus(name: string, updates: Partial<ServiceStatus>) {
    const current = this.serviceStatuses.get(name);
    if (current) {
      const updated = { ...current, ...updates };
      this.serviceStatuses.set(name, updated);
      this.notifyProgressUpdate();
    }
  }

  private notifyProgressUpdate() {
    if (this.onProgressUpdate) {
      this.onProgressUpdate(Array.from(this.serviceStatuses.values()));
    }
  }

  private notifyDataUpdate(data: Partial<DashboardData>) {
    if (this.onDataUpdate) {
      this.onDataUpdate(data);
    }
  }

  public async loadDashboardData(): Promise<DashboardData> {
    // Reset all service statuses
    this.serviceStatuses.forEach((status, name) => {
      this.updateServiceStatus(name, {
        status: 'loading',
        progress: 0,
        message: 'Initializing...'
      });
    });

    // Start parallel requests
    const promises = [
      this.loadStrategies(),
      this.loadGapAnalyses(),
      this.loadAIAnalytics(),
      this.loadCalendarEvents(),
      this.loadHealthStatus()
    ];

    // Wait for all to complete but handle each independently
    const results = await Promise.allSettled(promises);

    // Compile final data
    const dashboardData: DashboardData = {
      strategies: [],
      gapAnalyses: [],
      aiInsights: [],
      aiRecommendations: [],
      calendarEvents: [],
      healthStatus: {
        backend: false,
        database: false,
        aiServices: false
      }
    };

    results.forEach((result) => {
      if (result.status === 'fulfilled') {
        const data = result.value;
        // Type-safe data assignment
        if ('strategies' in data) dashboardData.strategies = data.strategies;
        if ('gapAnalyses' in data) dashboardData.gapAnalyses = data.gapAnalyses;
        if ('aiInsights' in data) dashboardData.aiInsights = data.aiInsights;
        if ('aiRecommendations' in data) dashboardData.aiRecommendations = data.aiRecommendations;
        if ('calendarEvents' in data) dashboardData.calendarEvents = data.calendarEvents;
        if ('healthStatus' in data) dashboardData.healthStatus = data.healthStatus;
      }
    });

    return dashboardData;
  }

  private async loadStrategies() {
    try {
      this.updateServiceStatus('strategies', {
        status: 'loading',
        progress: 10,
        message: 'Loading content strategies...'
      });

      const strategies = await contentPlanningApi.getStrategiesSafe();
      
      this.updateServiceStatus('strategies', {
        status: 'loading',
        progress: 50,
        message: 'Processing strategy data...'
      });

      // Simulate processing time for better UX
      await new Promise(resolve => setTimeout(resolve, 500));
      
      this.updateServiceStatus('strategies', {
        status: 'success',
        progress: 100,
        message: `Loaded ${strategies.length} content strategies`,
        data: strategies
      });

      this.notifyDataUpdate({ strategies });

      return { strategies };
    } catch (error: any) {
      this.updateServiceStatus('strategies', {
        status: 'error',
        progress: 0,
        message: 'Failed to load strategies',
        error: error.message
      });
      return { strategies: [] };
    }
  }

  private async loadGapAnalyses() {
    try {
      this.updateServiceStatus('gapAnalyses', {
        status: 'loading',
        progress: 10,
        message: 'Initializing gap analysis...'
      });

      const response = await contentPlanningApi.getGapAnalysesSafe();
      
      this.updateServiceStatus('gapAnalyses', {
        status: 'loading',
        progress: 30,
        message: 'Analyzing content gaps...'
      });

      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 800));
      
      this.updateServiceStatus('gapAnalyses', {
        status: 'loading',
        progress: 70,
        message: 'Processing gap analysis results...'
      });

      await new Promise(resolve => setTimeout(resolve, 500));
      
      this.updateServiceStatus('gapAnalyses', {
        status: 'success',
        progress: 100,
        message: `Found ${response.gap_analyses?.length || 0} content gaps`,
        data: response
      });

      this.notifyDataUpdate({ gapAnalyses: response.gap_analyses || [] });

      return { gapAnalyses: response.gap_analyses || [] };
    } catch (error: any) {
      this.updateServiceStatus('gapAnalyses', {
        status: 'error',
        progress: 0,
        message: 'Failed to load gap analysis',
        error: error.message
      });
      return { gapAnalyses: [] };
    }
  }

  private async loadAIAnalytics() {
    try {
      this.updateServiceStatus('aiAnalytics', {
        status: 'loading',
        progress: 10,
        message: 'Initializing AI analysis...'
      });

      return new Promise<{ aiInsights: any[]; aiRecommendations: any[] }>((resolve, reject) => {
        contentPlanningApi.streamAIAnalytics(
          // Progress callback
          (progressData) => {
            this.updateServiceStatus('aiAnalytics', {
              progress: progressData.progress,
              message: progressData.message || 'AI analysis in progress...'
            });
          },
          // Complete callback
          (aiData) => {
            this.updateServiceStatus('aiAnalytics', {
              status: 'success',
              progress: 100,
              message: `Generated ${aiData.insights?.length || 0} insights and ${aiData.recommendations?.length || 0} recommendations`,
              data: aiData
            });

            this.notifyDataUpdate({
              aiInsights: aiData.insights || [],
              aiRecommendations: aiData.recommendations || []
            });

            resolve({
              aiInsights: aiData.insights || [],
              aiRecommendations: aiData.recommendations || []
            });
          },
          // Error callback
          (error) => {
            this.updateServiceStatus('aiAnalytics', {
              status: 'error',
              progress: 0,
              message: 'AI analysis failed',
              error: error.message
            });
            reject(error);
          }
        );
      });
    } catch (error: any) {
      this.updateServiceStatus('aiAnalytics', {
        status: 'error',
        progress: 0,
        message: 'AI analysis failed',
        error: error.message
      });
      return { aiInsights: [], aiRecommendations: [] };
    }
  }

  private async loadCalendarEvents() {
    try {
      this.updateServiceStatus('calendarEvents', {
        status: 'loading',
        progress: 10,
        message: 'Loading calendar events...'
      });

      const calendarEvents = await contentPlanningApi.getEventsSafe();
      
      this.updateServiceStatus('calendarEvents', {
        status: 'loading',
        progress: 50,
        message: 'Processing calendar data...'
      });

      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 300));
      
      this.updateServiceStatus('calendarEvents', {
        status: 'success',
        progress: 100,
        message: `Loaded ${calendarEvents.length} calendar events`,
        data: calendarEvents
      });

      this.notifyDataUpdate({ calendarEvents });

      return { calendarEvents };
    } catch (error: any) {
      this.updateServiceStatus('calendarEvents', {
        status: 'error',
        progress: 0,
        message: 'Failed to load calendar events',
        error: error.message
      });
      return { calendarEvents: [] };
    }
  }

  private async loadHealthStatus() {
    try {
      this.updateServiceStatus('healthCheck', {
        status: 'loading',
        progress: 25,
        message: 'Checking system health...'
      });

      const [backendHealth, aiHealth] = await Promise.allSettled([
        contentPlanningApi.checkBackendHealth(),
        contentPlanningApi.checkAIHealth()
      ]);

      const healthStatus = {
        backend: backendHealth.status === 'fulfilled' && backendHealth.value.status === 'healthy',
        database: backendHealth.status === 'fulfilled' && backendHealth.value.services?.database_connection === true,
        aiServices: aiHealth.status === 'fulfilled' && aiHealth.value.status === 'healthy'
      };

      this.updateServiceStatus('healthCheck', {
        status: 'success',
        progress: 100,
        message: 'System health check complete',
        data: healthStatus
      });

      this.notifyDataUpdate({ healthStatus });

      return { healthStatus };
    } catch (error: any) {
      this.updateServiceStatus('healthCheck', {
        status: 'error',
        progress: 0,
        message: 'Health check failed',
        error: error.message
      });
      return {
        healthStatus: {
          backend: false,
          database: false,
          aiServices: false
        }
      };
    }
  }

  public getServiceStatuses(): ServiceStatus[] {
    return Array.from(this.serviceStatuses.values());
  }

  public refreshService(serviceName: string) {
    const status = this.serviceStatuses.get(serviceName);
    if (status) {
      this.updateServiceStatus(serviceName, {
        status: 'loading',
        progress: 0,
        message: 'Refreshing...'
      });

      // Re-run the specific service
      switch (serviceName) {
        case 'strategies':
          this.loadStrategies();
          break;
        case 'gapAnalyses':
          this.loadGapAnalyses();
          break;
        case 'aiAnalytics':
          this.loadAIAnalytics();
          break;
        case 'calendarEvents':
          this.loadCalendarEvents();
          break;
        case 'healthCheck':
          this.loadHealthStatus();
          break;
      }
    }
  }
}

// Export singleton instance
export const contentPlanningOrchestrator = new ContentPlanningOrchestrator(); 