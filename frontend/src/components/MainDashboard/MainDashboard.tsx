import React from 'react';
import {
  Box,
  Container,
  Grid,
  Alert,
  Snackbar,
  useTheme,
  useMediaQuery
} from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

// Shared components
import DashboardHeader from '../shared/DashboardHeader';
import SystemStatusIndicator from '../ContentPlanningDashboard/components/SystemStatusIndicator';
import SearchFilter from '../shared/SearchFilter';
import ToolCard from '../shared/ToolCard';
import CategoryHeader from '../shared/CategoryHeader';
import LoadingSkeleton from '../shared/LoadingSkeleton';
import ErrorDisplay from '../shared/ErrorDisplay';
import EmptyState from '../shared/EmptyState';

// Shared types and utilities
import { Tool, Category } from '../shared/types';
import { getFilteredCategories, getToolsForCategory } from '../shared/utils';

// Zustand store
import { useDashboardStore } from '../../stores/dashboardStore';

// Data
import { toolCategories } from '../../data/toolCategories';

// Main dashboard component
const MainDashboard: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  
  // Zustand store hooks
  const {
    loading,
    error,
    searchQuery,
    selectedCategory,
    selectedSubCategory,
    favorites,
    snackbar,
    toggleFavorite,
    setSearchQuery,
    setSelectedCategory,
    setSelectedSubCategory,
    setError,
    setLoading,
    showSnackbar,
    hideSnackbar,
    clearFilters,
  } = useDashboardStore();

  const handleToolClick = (tool: Tool) => {
    console.log('Navigating to tool:', tool.path);
    if (tool.path) {
      navigate(tool.path);
      return;
    }
    showSnackbar(`Launching ${tool.name}...`, 'info');
  };

  const filteredCategories = getFilteredCategories(
    toolCategories,
    selectedCategory,
    searchQuery
  );

  if (loading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return <ErrorDisplay error={error} />;
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
        padding: theme.spacing(4),
        position: 'relative',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'url("data:image/svg+xml,%3Csvg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.03"%3E%3Ccircle cx="40" cy="40" r="3"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
          pointerEvents: 'none',
        },
        '&::after': {
          content: '""',
          position: 'absolute',
          top: '50%',
          left: '50%',
          width: '600px',
          height: '600px',
          background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
          transform: 'translate(-50%, -50%)',
          pointerEvents: 'none',
          zIndex: 0,
        },
      }}
    >
      <Container maxWidth="xl" sx={{ position: 'relative', zIndex: 1 }}>
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            {/* Dashboard Header */}
            <DashboardHeader
              title="🚀 Alwrity Content Hub"
              subtitle="Your AI-powered content creation suite"
              statusChips={[]}
              rightContent={<SystemStatusIndicator />}
            />

            {/* Search and Filter */}
            <SearchFilter
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
              onClearSearch={() => setSearchQuery('')}
              selectedCategory={selectedCategory}
              onCategoryChange={setSelectedCategory}
              selectedSubCategory={selectedSubCategory}
              onSubCategoryChange={setSelectedSubCategory}
              toolCategories={toolCategories}
              theme={theme}
            />

            {/* Enhanced Tools Grid */}
            <Box sx={{ mb: 4 }}>
              {Object.entries(filteredCategories).map(([categoryName, category], categoryIndex) => (
                <motion.div
                  key={categoryName}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: categoryIndex * 0.1 }}
                >
                  <Box sx={{ mb: 5 }}>
                    {/* Category Header */}
                    <CategoryHeader
                      categoryName={categoryName}
                      category={category}
                      theme={theme}
                    />

                    <Grid container spacing={3}>
                      {getToolsForCategory(category, selectedSubCategory).map((tool: Tool, toolIndex: number) => (
                        <Grid item xs={12} sm={6} md={4} lg={3} key={tool.name}>
                          <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: (categoryIndex * 0.1) + (toolIndex * 0.05) }}
                          >
                            <ToolCard
                              tool={tool}
                              onToolClick={handleToolClick}
                              isFavorite={favorites.includes(tool.name)}
                              onToggleFavorite={toggleFavorite}
                            />
                          </motion.div>
                        </Grid>
                      ))}
                    </Grid>
                  </Box>
                </motion.div>
              ))}
            </Box>

            {/* Empty State */}
            {Object.keys(filteredCategories).length === 0 && (
              <EmptyState
                icon={<span>🔍</span>}
                title="No tools found matching your criteria"
                message="Try adjusting your search or category filter"
                onClearFilters={clearFilters}
                clearButtonText="Clear Filters"
              />
            )}
          </motion.div>
        </AnimatePresence>

        {/* Enhanced Snackbar for notifications */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={3000}
          onClose={hideSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert onClose={hideSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Container>
    </Box>
  );
};

export default MainDashboard; 