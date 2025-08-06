# Zustand Store Implementation

This directory contains Zustand stores for managing state across the Alwrity dashboard components.

## Overview

Zustand has been implemented to replace the previous state management approach using custom hooks and local state. This provides:

- **Centralized state management** across components
- **Automatic persistence** with Zustand's persist middleware
- **Better performance** with selective re-renders
- **Simpler state updates** with immer-like syntax
- **Better debugging** with Redux DevTools support

## Stores

### 1. `dashboardStore.ts` - Main Dashboard Store
Manages state for the main dashboard including:
- Search and filter state
- Favorites management
- Snackbar notifications
- Loading and error states

**Key Features:**
- Automatic persistence of favorites and filter preferences
- Snackbar management with automatic hiding
- Optimized re-renders with selective state subscriptions

**Usage:**
```typescript
import { useDashboardStore } from '../stores/dashboardStore';

const {
  loading,
  error,
  searchQuery,
  favorites,
  toggleFavorite,
  setSearchQuery,
  showSnackbar,
} = useDashboardStore();
```

### 2. `seoDashboardStore.ts` - SEO Dashboard Store
Manages state for the SEO dashboard including:
- Dashboard data fetching and caching
- Loading and error states
- Data refresh functionality

**Key Features:**
- Automatic data fetching on component mount
- Error handling with retry functionality
- Data caching with last updated timestamp
- DevTools integration for debugging

**Usage:**
```typescript
import { useSEODashboardStore } from '../stores/seoDashboardStore';

const {
  loading,
  error,
  data,
  fetchDashboardData,
  refreshData,
} = useSEODashboardStore();
```

### 3. `sharedDashboardStore.ts` - Shared Dashboard Store
Manages common functionality across all dashboards:
- Sidebar state
- Theme management
- Global notifications

**Key Features:**
- Theme switching with system preference detection
- Notification management with auto-cleanup
- Sidebar state management

**Usage:**
```typescript
import { useSharedDashboardStore } from '../stores/sharedDashboardStore';

const {
  isSidebarOpen,
  currentTheme,
  notifications,
  toggleSidebar,
  setTheme,
  addNotification,
} = useSharedDashboardStore();
```

## Benefits Over Previous Implementation

### Before (Custom Hooks + Local State)
```typescript
// MainDashboard - Custom hook with manual localStorage
const useDashboardState = () => {
  const [state, setState] = useState<DashboardState>({...});
  // Manual localStorage handling
  // Complex state updates
  // No cross-component communication
};

// SEODashboard - Local state
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
const [data, setData] = useState<SEODashboardData | null>(null);
```

### After (Zustand Stores)
```typescript
// Centralized, persistent, and optimized
const {
  loading,
  error,
  data,
  fetchDashboardData,
} = useSEODashboardStore();

// Automatic persistence
const {
  favorites,
  searchQuery,
  toggleFavorite,
} = useDashboardStore();
```

## Performance Improvements

1. **Selective Re-renders**: Components only re-render when their specific state changes
2. **Automatic Persistence**: No manual localStorage management needed
3. **Optimized Updates**: Zustand's internal optimizations reduce unnecessary renders
4. **DevTools Integration**: Better debugging and state inspection

## Migration Notes

- The old `useDashboardState` hook can be removed after confirming the new implementation works correctly
- All localStorage operations are now handled automatically by Zustand's persist middleware
- Error handling is more robust with centralized error states
- Snackbar management is simplified with automatic cleanup

## Future Enhancements

1. **Real-time Updates**: Can easily add WebSocket integration for live data updates
2. **Offline Support**: Zustand's persistence can be extended for offline functionality
3. **State Synchronization**: Multiple tabs can share state through storage events
4. **Advanced Caching**: Can implement more sophisticated caching strategies

## Testing

The stores can be tested independently:
```typescript
import { renderHook, act } from '@testing-library/react';
import { useDashboardStore } from './dashboardStore';

test('should toggle favorite', () => {
  const { result } = renderHook(() => useDashboardStore());
  
  act(() => {
    result.current.toggleFavorite('test-tool');
  });
  
  expect(result.current.favorites).toContain('test-tool');
});
``` 