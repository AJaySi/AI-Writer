import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface SharedDashboardState {
  // Common state
  isSidebarOpen: boolean;
  currentTheme: 'light' | 'dark' | 'auto';
  notifications: Array<{
    id: string;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error';
    timestamp: Date;
    read: boolean;
  }>;
  
  // Actions
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark' | 'auto') => void;
  addNotification: (message: string, type?: 'info' | 'success' | 'warning' | 'error') => void;
  markNotificationAsRead: (id: string) => void;
  clearNotifications: () => void;
  clearOldNotifications: () => void;
}

export const useSharedDashboardStore = create<SharedDashboardState>()(
  devtools(
    (set, get) => ({
      // Initial state
      isSidebarOpen: false,
      currentTheme: 'auto',
      notifications: [],

      // Actions
      toggleSidebar: () => {
        set((state) => ({ isSidebarOpen: !state.isSidebarOpen }));
      },

      setSidebarOpen: (open: boolean) => {
        set({ isSidebarOpen: open });
      },

      setTheme: (theme: 'light' | 'dark' | 'auto') => {
        set({ currentTheme: theme });
        // Apply theme to document
        if (theme === 'dark') {
          document.documentElement.classList.add('dark');
        } else if (theme === 'light') {
          document.documentElement.classList.remove('dark');
        } else {
          // Auto theme - check system preference
          const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
          if (prefersDark) {
            document.documentElement.classList.add('dark');
          } else {
            document.documentElement.classList.remove('dark');
          }
        }
      },

      addNotification: (message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info') => {
        const notification = {
          id: Date.now().toString(),
          message,
          type,
          timestamp: new Date(),
          read: false,
        };
        
        set((state) => ({
          notifications: [notification, ...state.notifications].slice(0, 10), // Keep only last 10
        }));
      },

      markNotificationAsRead: (id: string) => {
        set((state) => ({
          notifications: state.notifications.map((notification) =>
            notification.id === id ? { ...notification, read: true } : notification
          ),
        }));
      },

      clearNotifications: () => {
        set({ notifications: [] });
      },

      clearOldNotifications: () => {
        const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
        set((state) => ({
          notifications: state.notifications.filter(
            (notification) => notification.timestamp > oneDayAgo
          ),
        }));
      },
    }),
    {
      name: 'shared-dashboard-store',
    }
  )
); 