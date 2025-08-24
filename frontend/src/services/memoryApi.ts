/**
 * Memory API Service
 * Handles communication with ALwrity memory backend
 */

export interface MemoryStatistics {
  total_memories: number;
  categories: Record<string, number>;
  user_types: Record<string, number>;
  industries: Record<string, number>;
  recent_memories: number;
  api_calls_today: number;
  available: boolean;
  formatted_categories: Array<{
    name: string;
    count: number;
    percentage: number;
  }>;
  status_message: string;
  last_updated: string;
}

export interface Memory {
  id: string;
  strategy_name: string;
  strategy_id: number;
  industry: string;
  user_type: string;
  categories: string[];
  activation_date: string;
  content: string;
  relevance_score?: number;
}

export interface ChatResponse {
  relevant_memories: Memory[];
  memory_context: Array<{
    strategy_name: string;
    industry: string;
    categories: string[];
    summary: string;
  }>;
  total_memories_searched: number;
  chat_ready: boolean;
  suggested_questions: string[];
}

export interface MemorySearchRequest {
  query: string;
  limit?: number;
  user_type?: string;
  industry?: string;
  categories?: string[];
}

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class MemoryApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = `${API_BASE}/memory`;
  }

  /**
   * Get memory statistics for the mind icon
   */
  async getMemoryStatistics(userId: number): Promise<MemoryStatistics> {
    try {
      const response = await fetch(`${this.baseUrl}/statistics/${userId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Error fetching memory statistics:', error);
      // Return safe defaults
      return {
        total_memories: 0,
        categories: {},
        user_types: {},
        industries: {},
        recent_memories: 0,
        api_calls_today: 0,
        available: false,
        formatted_categories: [],
        status_message: 'Memory service unavailable',
        last_updated: new Date().toISOString()
      };
    }
  }

  /**
   * Search memories with advanced filtering
   */
  async searchMemories(userId: number, searchRequest: MemorySearchRequest): Promise<Memory[]> {
    try {
      const response = await fetch(`${this.baseUrl}/search/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchRequest),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.data.memories;
    } catch (error) {
      console.error('Error searching memories:', error);
      return [];
    }
  }

  /**
   * Chat with memories - get relevant context for a question
   */
  async chatWithMemories(userId: number, message: string): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/chat/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Error chatting with memories:', error);
      return {
        relevant_memories: [],
        memory_context: [],
        total_memories_searched: 0,
        chat_ready: false,
        suggested_questions: []
      };
    }
  }

  /**
   * Get all memories for a user
   */
  async getAllMemories(
    userId: number, 
    limit: number = 50, 
    userType?: string, 
    industry?: string
  ): Promise<Memory[]> {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
        ...(userType && { user_type: userType }),
        ...(industry && { industry }),
      });

      const response = await fetch(`${this.baseUrl}/all/${userId}?${params}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.data.memories;
    } catch (error) {
      console.error('Error getting all memories:', error);
      return [];
    }
  }

  /**
   * Delete a memory by strategy ID
   */
  async deleteMemory(userId: number, strategyId: number): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/delete/${userId}/${strategyId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.success;
    } catch (error) {
      console.error('Error deleting memory:', error);
      return false;
    }
  }

  /**
   * Update a memory with new strategy data
   */
  async updateMemory(
    userId: number, 
    strategyId: number, 
    strategyData: any
  ): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/update/${userId}/${strategyId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ strategy_data: strategyData }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.success;
    } catch (error) {
      console.error('Error updating memory:', error);
      return false;
    }
  }

  /**
   * Get available categories for filtering
   */
  async getUserCategories(userId: number): Promise<{
    categories: string[];
    industries: string[];
    user_types: string[];
    available_filters: {
      categories: string[];
      industries: string[];
    };
  }> {
    try {
      const response = await fetch(`${this.baseUrl}/categories/${userId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Error getting user categories:', error);
      return {
        categories: [],
        industries: [],
        user_types: [],
        available_filters: {
          categories: [],
          industries: []
        }
      };
    }
  }

  /**
   * Check memory service health
   */
  async checkHealth(): Promise<{
    mem0_available: boolean;
    service_status: string;
    features: {
      storage: boolean;
      search: boolean;
      categorization: boolean;
      chat_interface: boolean;
    };
  }> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Error checking memory health:', error);
      return {
        mem0_available: false,
        service_status: 'unavailable',
        features: {
          storage: false,
          search: false,
          categorization: false,
          chat_interface: false
        }
      };
    }
  }
}

export const memoryApi = new MemoryApiService();