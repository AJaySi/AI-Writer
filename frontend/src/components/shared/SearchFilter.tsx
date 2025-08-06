import React from 'react';
import { 
  Box, 
  TextField, 
  InputAdornment, 
  IconButton, 
  Typography, 
  Tooltip 
} from '@mui/material';
import { 
  Search as SearchIcon, 
  Clear as ClearIcon, 
  FilterList as FilterIcon 
} from '@mui/icons-material';
import { SearchContainer, CategoryChip } from './styled';
import { SearchFilterProps } from './types';

const SearchFilter: React.FC<SearchFilterProps> = ({
  searchQuery,
  onSearchChange,
  onClearSearch,
  selectedCategory,
  onCategoryChange,
  selectedSubCategory,
  onSubCategoryChange,
  toolCategories,
  theme
}) => {
  return (
    <SearchContainer>
      <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search tools..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
              </InputAdornment>
            ),
            endAdornment: searchQuery && (
              <InputAdornment position="end">
                <IconButton onClick={onClearSearch} size="small">
                  <ClearIcon sx={{ color: 'rgba(255, 255, 255, 0.7)' }} />
                </IconButton>
              </InputAdornment>
            ),
          }}
          sx={{
            '& .MuiOutlinedInput-root': {
              color: 'white',
              '& fieldset': {
                borderColor: 'rgba(255, 255, 255, 0.3)',
              },
              '&:hover fieldset': {
                borderColor: 'rgba(255, 255, 255, 0.5)',
              },
              '&.Mui-focused fieldset': {
                borderColor: 'rgba(255, 255, 255, 0.8)',
              },
              '& input::placeholder': {
                color: 'rgba(255, 255, 255, 0.6)',
                opacity: 1,
              },
            },
          }}
        />
        <Tooltip title="Filter by category">
          <IconButton sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
            <FilterIcon />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Enhanced Category Filter */}
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <CategoryChip
          label="All Tools"
          onClick={() => onCategoryChange(null)}
          active={selectedCategory === null}
          theme={theme}
        />
        {Object.keys(toolCategories).map((category) => (
          <CategoryChip
            key={category}
            label={category}
            onClick={() => onCategoryChange(category)}
            active={selectedCategory === category}
            theme={theme}
          />
        ))}
      </Box>

      {/* Sub-category Filter for SEO & Analytics */}
      {selectedCategory === 'SEO & Analytics' && 'subCategories' in toolCategories['SEO & Analytics'] && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.8)', mb: 1, fontWeight: 600 }}>
            Filter by sub-category:
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <CategoryChip
              label="All SEO Tools"
              onClick={() => onSubCategoryChange(null)}
              active={selectedSubCategory === null}
              theme={theme}
            />
            {Object.keys(toolCategories['SEO & Analytics'].subCategories).map((subCategory) => (
              <CategoryChip
                key={subCategory}
                label={subCategory}
                onClick={() => onSubCategoryChange(subCategory)}
                active={selectedSubCategory === subCategory}
                theme={theme}
              />
            ))}
          </Box>
        </Box>
      )}
    </SearchContainer>
  );
};

export default SearchFilter; 