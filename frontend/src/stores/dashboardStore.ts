import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { DashboardState, SnackbarState } from '../components/shared/types';

export interface DashboardStore extends DashboardState {
  // Actions
  toggleFavorite: (toolName: string) => void;
  setSearchQuery: (query: string) => void;
  setSelectedCategory: (category: string | null) => void;
  setSelectedSubCategory: (subCategory: string | null) => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
  showSnackbar: (message: string, severity?: SnackbarState['severity']) => void;
  hideSnackbar: () => void;
  clearFilters: () => void;
}

export const useDashboardStore = create<DashboardStore>()(
  persist(
    (set, get) => ({
      // Initial state
      loading: false,
      error: null,
      searchQuery: '',
      selectedCategory: null,
      selectedSubCategory: null,
      favorites: [],
      snackbar: {
        open: false,
        message: '',
        severity: 'info',
      },

      // Actions
      toggleFavorite: (toolName: string) => {
        const { favorites } = get();
        const newFavorites = favorites.includes(toolName)
          ? favorites.filter(f => f !== toolName)
          : [...favorites, toolName];
        
        set({ favorites: newFavorites });
        
        // Show snackbar
        const message = favorites.includes(toolName) 
          ? 'Removed from favorites' 
          : 'Added to favorites';
        get().showSnackbar(message, 'success');
      },

      setSearchQuery: (query: string) => {
        set({ searchQuery: query });
      },

      setSelectedCategory: (category: string | null) => {
        set({ 
          selectedCategory: category,
          selectedSubCategory: null, // Reset sub-category when changing main category
        });
      },

      setSelectedSubCategory: (subCategory: string | null) => {
        set({ selectedSubCategory: subCategory });
      },

      setError: (error: string | null) => {
        set({ error });
      },

      setLoading: (loading: boolean) => {
        set({ loading });
      },

      showSnackbar: (message: string, severity: SnackbarState['severity'] = 'info') => {
        set({
          snackbar: {
            open: true,
            message,
            severity,
          },
        });
      },

      hideSnackbar: () => {
        set({
          snackbar: {
            ...get().snackbar,
            open: false,
          },
        });
      },

      clearFilters: () => {
        set({
          searchQuery: '',
          selectedCategory: null,
          selectedSubCategory: null,
        });
      },
    }),
    {
      name: 'alwrity-dashboard-storage',
      partialize: (state) => ({
        favorites: state.favorites,
        searchQuery: state.searchQuery,
        selectedCategory: state.selectedCategory,
        selectedSubCategory: state.selectedSubCategory,
      }),
    }
  )
); 