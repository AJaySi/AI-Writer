import { useState, useEffect } from 'react';
import { DashboardState, SnackbarState } from '../components/shared/types';

const useDashboardState = () => {
  const [state, setState] = useState<DashboardState>({
    loading: true,
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
  });

  // Load favorites from localStorage
  useEffect(() => {
    const savedFavorites = localStorage.getItem('alwrity-favorites');
    if (savedFavorites) {
      setState(prev => ({
        ...prev,
        favorites: JSON.parse(savedFavorites),
        loading: false,
      }));
    } else {
      setState(prev => ({ ...prev, loading: false }));
    }
  }, []);

  // Save favorites to localStorage
  const toggleFavorite = (toolName: string) => {
    const newFavorites = state.favorites.includes(toolName)
      ? state.favorites.filter(f => f !== toolName)
      : [...state.favorites, toolName];
    
    setState(prev => ({
      ...prev,
      favorites: newFavorites,
    }));
    
    localStorage.setItem('alwrity-favorites', JSON.stringify(newFavorites));
    
    showSnackbar(
      state.favorites.includes(toolName) ? 'Removed from favorites' : 'Added to favorites',
      'success'
    );
  };

  const setSearchQuery = (query: string) => {
    setState(prev => ({ ...prev, searchQuery: query }));
  };

  const setSelectedCategory = (category: string | null) => {
    setState(prev => ({ 
      ...prev, 
      selectedCategory: category,
      selectedSubCategory: null, // Reset sub-category when changing main category
    }));
  };

  const setSelectedSubCategory = (subCategory: string | null) => {
    setState(prev => ({ ...prev, selectedSubCategory: subCategory }));
  };

  const setError = (error: string | null) => {
    setState(prev => ({ ...prev, error }));
  };

  const setLoading = (loading: boolean) => {
    setState(prev => ({ ...prev, loading }));
  };

  const showSnackbar = (message: string, severity: SnackbarState['severity'] = 'info') => {
    setState(prev => ({
      ...prev,
      snackbar: {
        open: true,
        message,
        severity,
      },
    }));
  };

  const hideSnackbar = () => {
    setState(prev => ({
      ...prev,
      snackbar: {
        ...prev.snackbar,
        open: false,
      },
    }));
  };

  const clearFilters = () => {
    setState(prev => ({
      ...prev,
      searchQuery: '',
      selectedCategory: null,
      selectedSubCategory: null,
    }));
  };

  return {
    state,
    toggleFavorite,
    setSearchQuery,
    setSelectedCategory,
    setSelectedSubCategory,
    setError,
    setLoading,
    showSnackbar,
    hideSnackbar,
    clearFilters,
  };
};

export default useDashboardState; 